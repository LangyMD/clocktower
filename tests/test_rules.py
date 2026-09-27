import asyncio
import random
import unittest

from clocktower.agents import RandomSeat, ScriptedStoryteller
from clocktower.game import NAMES, Game
from clocktower.llm import Reply
from clocktower.state import Grimoire, chef_choice, pair_choice, setup_error

A, B, C, D, E, F, G, H, I = NAMES
BLANK = {'say': '', 'whispers': [], 'nominate': None, 'vote': None, 'targets': [], 'slayer_shot': None,
         'call_nominations': False}


class Seat:
    """Follows a policy(name, request) -> partial action; everything else passes."""

    def __init__(self, name, policy, log):
        self.name, self.policy, self.log = name, policy, log

    async def act(self, text, request):
        self.log.append((self.name, request.kind, text))
        return Reply({**BLANK, **(self.policy(self.name, request) or {})})


class Storyteller:
    def __init__(self, decisions=None):
        self.decisions = decisions or {}
        self.rng = random.Random(0)

    async def decide(self, text, request):
        if request.kind == 'decisions':
            out = request.fallback(self.rng)
            for d in out['decisions']:
                d.update(self.decisions.get(d['id'], {}))
            return Reply(out)
        return Reply(request.fallback(self.rng))


def game(characters, policy=lambda n, r: None, decisions=None, **kw):
    log = []
    g = Game({n: Seat(n, policy, log) for n in NAMES}, Storyteller(decisions), characters=characters, seed=7, **kw)
    g.texts = log
    return g


def run(coro):
    return asyncio.run(coro)


def night_targets(choices):
    """Policy that answers night prompts from a {name: [targets]} dict."""
    return lambda name, req: {'targets': choices[name]} if req.kind == 'night' and name in choices else None


BASE = ['Imp', 'Poisoner', 'Monk', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']


class SetupTests(unittest.TestCase):
    def test_setup_legality(self):
        self.assertIsNone(setup_error(BASE))
        self.assertIn('Outsiders', setup_error(['Imp', 'Baron', 'Monk', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']))
        self.assertIsNone(setup_error(['Imp', 'Baron', 'Monk', 'Empath', 'Chef', 'Drunk', 'Recluse', 'Butler', 'Saint']))
        self.assertIn('one Imp', setup_error(['Poisoner', 'Spy', 'Monk', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']))

    def test_evil_learns_each_other_and_bluffs(self):
        g = game(BASE)
        run(g.setup())
        imp_intro = next(t for t in g.buf[A] if 'Your Minion' in t)
        self.assertIn(B, imp_intro)
        self.assertEqual(len(g.g.bluffs), 3)
        self.assertTrue(all(b not in BASE for b in g.g.bluffs))
        self.assertTrue(any(f'The Demon is {A}' in t for t in g.buf[B]))
        self.assertFalse(any('Your Minion' in t for t in g.buf[C]))


class NightTests(unittest.TestCase):
    def play_nights(self, characters, choices_by_night, decisions=None):
        g = game(characters, decisions=decisions)
        run(g.setup())
        for n, choices in enumerate(choices_by_night, start=1):
            g.seats = {x: Seat(x, night_targets(choices), g.texts) for x in NAMES}
            run(g.night(n))
        return g

    def test_monk_protects_unless_poisoned(self):
        g = self.play_nights(BASE, [{B: [E]}, {A: [D], C: [D], B: [E]}])
        self.assertTrue(g.g[D].alive)
        g = self.play_nights(BASE, [{B: [E]}, {A: [D], C: [D], B: [C]}])
        self.assertFalse(g.g[D].alive)

    def test_soldier_is_safe(self):
        g = self.play_nights(BASE, [{B: [E]}, {A: [G], B: [E]}])
        self.assertTrue(g.g[G].alive)

    def test_starpass_makes_the_minion_the_imp(self):
        g = self.play_nights(BASE, [{B: [E]}, {A: [A], B: [E]}])
        self.assertFalse(g.g[A].alive)
        self.assertEqual(g.g[B].character, 'Imp')
        self.assertIsNone(g.g.check_victory())
        self.assertTrue(any('you are now the Imp' in t for t in g.buf[B]))

    def test_poisoned_empath_is_asked_of_the_storyteller(self):
        g = self.play_nights(BASE, [{B: [D]}], decisions={f'Empath:{D}': {'number': 2}})
        self.assertTrue(any('2 of your living neighbours are evil' in t for t in g.buf[D]))

    def test_sober_empath_is_automatic_and_true(self):
        g = self.play_nights(BASE, [{B: [E]}], decisions={f'Empath:{D}': {'number': 2}})
        self.assertTrue(any('0 of your living neighbours are evil' in t for t in g.buf[D]))

    def test_mayor_bounce(self):
        chars = ['Imp', 'Poisoner', 'Mayor', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = self.play_nights(chars, [{B: [E]}, {A: [C], B: [E]}], decisions={f'Mayor:{C}': {'players': [F]}})
        self.assertTrue(g.g[C].alive)
        self.assertFalse(g.g[F].alive)

    def test_ravenkeeper_learns_a_character(self):
        chars = ['Imp', 'Poisoner', 'Ravenkeeper', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = game(chars)
        run(g.setup())
        run(g.night(1))
        picks = {A: [C], B: [E], C: [A], H: [D]}
        g.seats = {x: Seat(x, lambda n, r: {'targets': picks[n]}, g.texts) for x in NAMES}
        run(g.night(2))
        self.assertTrue(any(f'{A} is the Imp' in t for t in g.buf[C]))


class DayTests(unittest.TestCase):
    def prepared(self, characters, policy, decisions=None):
        g = game(characters, policy=policy, decisions=decisions)
        run(g.setup())
        g.day = 1
        return g

    def nominate(self, nominator, nominee, yes=()):
        def policy(name, req):
            if req.kind == 'nominate' and name == nominator:
                return {'nominate': nominee, 'say': 'I think so.'}
            if req.kind == 'vote':
                return {'vote': name in yes}
        return policy

    def test_execution_needs_half_the_living(self):
        g = self.prepared(BASE, self.nominate(C, D, yes=[A, B, C, E]))
        run(g.nominations())
        self.assertTrue(g.g[D].alive)
        g = self.prepared(BASE, self.nominate(C, D, yes=[A, B, C, E, F]))
        run(g.nominations())
        self.assertFalse(g.g[D].alive)

    def test_saint_execution_loses_for_good(self):
        g = self.prepared(BASE, self.nominate(C, I, yes=NAMES))
        run(g.nominations())
        self.assertEqual(g.g.winner, 'evil')

    def test_executing_the_imp_wins_for_good_or_passes_to_the_scarlet_woman(self):
        g = self.prepared(BASE, self.nominate(C, A, yes=NAMES))
        run(g.nominations())
        self.assertEqual(g.g.winner, 'good')
        sw = ['Imp', 'Scarlet Woman'] + BASE[2:]
        g = self.prepared(sw, self.nominate(C, A, yes=NAMES))
        run(g.nominations())
        self.assertIsNone(g.g.winner)
        self.assertEqual(g.g[B].character, 'Imp')

    def test_scarlet_woman_needs_five_alive(self):
        sw = ['Imp', 'Scarlet Woman'] + BASE[2:]
        g = self.prepared(sw, self.nominate(C, A, yes=NAMES))
        for x in (F, G, H, I, E):
            g.g.die(g.g[x])
        run(g.nominations())
        self.assertEqual(g.g.winner, 'good')

    def test_virgin_executes_a_townsfolk_nominator(self):
        chars = ['Imp', 'Poisoner', 'Virgin', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = self.prepared(chars, self.nominate(D, C))
        run(g.nominations())
        self.assertFalse(g.g[D].alive)
        g = self.prepared(chars, self.nominate(H, C))  # the Butler is not a Townsfolk
        run(g.nominations())
        self.assertTrue(g.g[H].alive)
        self.assertTrue(g.g.virgin_used)

    def test_slayer(self):
        chars = ['Imp', 'Poisoner', 'Slayer', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Recluse']
        g = self.prepared(chars, lambda n, r: {'slayer_shot': A} if n == D else None)  # fake Slayer
        run(g.beat(1, 1, private=False))
        self.assertTrue(g.g[A].alive)
        g = self.prepared(chars, lambda n, r: {'slayer_shot': A} if n == C else None)
        run(g.beat(1, 1, private=True))  # no shots in private time
        self.assertIsNone(g.g.winner)
        run(g.beat(1, 1, private=False))
        self.assertEqual(g.g.winner, 'good')
        g = self.prepared(chars, lambda n, r: {'slayer_shot': I} if n == C else None, decisions={f'Slayer:{I}': {'yes': True}})
        run(g.beat(1, 1, private=False))
        self.assertFalse(g.g[I].alive)
        self.assertIsNone(g.g.winner)

    def test_butler_vote_needs_master(self):
        g = self.prepared(BASE, self.nominate(C, D, yes=[A, B, C, E, H]))
        g.g.master = F  # votes before the Butler (H), and votes no
        run(g.nominations())
        self.assertTrue(g.g[D].alive)
        vote = next(e for e in g.events if e['kind'] == 'vote' and e['data']['voter'] == H)
        self.assertFalse(vote['data']['yes'])  # shown as a no: nothing public reveals the Butler
        g = self.prepared(BASE, self.nominate(C, D, yes=[A, B, C, E, H]))
        g.g.master = I  # votes after the Butler, and votes no: the Butler's yes silently doesn't count
        run(g.nominations())
        result = next(e for e in g.events if e['kind'] == 'vote_result')
        self.assertEqual(result['data']['votes'], 4)
        self.assertNotIn('voided', result['data'])

    def test_whispers_are_private_and_speech_waits_for_the_town_square(self):
        def policy(name, req):
            if req.kind == 'beat':
                return {'say': 'hello town', 'whispers': [{'to': [B], 'text': 'psst'}] if name == A else []}
        g = self.prepared(BASE, policy)
        run(g.beat(1, 1, private=True))
        self.assertFalse(any(e['kind'] == 'say' for e in g.events))
        w = next(e for e in g.events if e['kind'] == 'whisper')
        self.assertEqual(w['to'], [A, B])
        self.assertEqual(sum('psst' in x or 'whispered' in x for x in g.buf[C]), 0)
        run(g.beat(1, 1, private=False))
        self.assertEqual(sum(e['kind'] == 'say' for e in g.events), 9)
        self.assertEqual(sum(e['kind'] == 'whisper' for e in g.events), 1)

    def test_tie_means_no_execution(self):
        def policy(name, req):
            if req.kind == 'nominate' and name == C and D not in req.prompt:
                return {'nominate': D}
            if req.kind == 'nominate' and name == E:
                return {'nominate': F}
            if req.kind == 'vote':
                return {'vote': name in (A, B, C, E, G)}
        g = self.prepared(BASE, policy)
        g.rng = random.Random(3)
        run(g.nominations())
        results = [e['data'] for e in g.events if e['kind'] == 'vote_result']
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1]['outcome'], 'tie')
        self.assertTrue(g.g[D].alive and g.g[F].alive)

    def test_mayor_wins_with_three_alive_and_no_execution(self):
        chars = ['Imp', 'Poisoner', 'Mayor', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = self.prepared(chars, lambda n, r: None)
        for x in (D, E, F, G, H, I):
            g.g.die(g.g[x])
        g.private_beats, g.public_beats = (1, 1), 1
        run(g.daytime(3))
        self.assertEqual(g.g.winner, 'good')

    def test_two_alive_is_an_evil_win(self):
        g = Grimoire(NAMES, BASE)
        for x in (C, D, E, F, G, H, I):
            g.die(g[x])
        self.assertEqual(g.check_victory(), 'evil')


class InformationTests(unittest.TestCase):
    def test_chef_with_recluse_can_see_extra_pair(self):
        chars = ['Imp', 'Recluse', 'Chef', 'Empath', 'Monk', 'Washerwoman', 'Soldier', 'Poisoner', 'Saint']
        g = Grimoire(NAMES, chars)
        c = chef_choice(g, g[C], random.Random(0))
        self.assertTrue(c.legal({'number': 0}) and c.legal({'number': 1}))
        self.assertFalse(c.legal({'number': 2}))
        self.assertFalse(c.auto)

    def test_washerwoman_pair_must_contain_the_townsfolk(self):
        g = Grimoire(NAMES, BASE)
        c = pair_choice(g, g[F], 'Washerwoman', random.Random(0))
        self.assertTrue(c.legal({'players': [C, A], 'character': 'Monk'}))
        self.assertFalse(c.legal({'players': [B, A], 'character': 'Monk'}))
        self.assertFalse(c.legal({'players': [F, C], 'character': 'Monk'}))  # never shown themselves
        self.assertTrue(c.legal(c.default))

    def test_drunk_washerwoman_can_be_told_anything(self):
        chars = ['Imp', 'Poisoner', 'Monk', 'Empath', 'Chef', 'Drunk', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Washerwoman')
        c = pair_choice(g, g[F], 'Washerwoman', random.Random(0))
        self.assertTrue(c.legal({'players': [B, A], 'character': 'Mayor'}))

    def test_spy_can_register_as_townsfolk(self):
        chars = ['Imp', 'Spy', 'Monk', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars)
        c = pair_choice(g, g[F], 'Washerwoman', random.Random(0))
        self.assertTrue(c.legal({'players': [B, A], 'character': 'Mayor'}))


class ScriptedStorytellerTests(unittest.TestCase):
    def test_every_scripted_choice_is_legal(self):
        from clocktower.characters import TOWNSFOLK
        from clocktower.state import (character_choice, empath_choice, fortune_teller_choice, mayor_choice,
                                      random_setup)
        for seed in range(300):
            r = random.Random(seed)
            chars = random_setup(r)
            r.shuffle(chars)
            g = Grimoire(NAMES, chars, drunk_as=r.choice([c for c in TOWNSFOLK if c not in chars]))
            g.bluffs = r.sample([c for c in TOWNSFOLK if c not in chars], 3)
            g.red_herring = r.choice([q.name for q in g.players if not q.evil])
            g.poisoned = r.choice(NAMES)
            choices = []
            for p in (q for q in g.players if not q.evil):
                for ability in ('Washerwoman', 'Librarian', 'Investigator'):
                    choices.append(pair_choice(g, p, ability, r))
                choices += [chef_choice(g, p, r), empath_choice(g, p, r),
                            fortune_teller_choice(g, p, r.sample(NAMES, 2), r),
                            character_choice(g, p, 'Undertaker', r.choice(NAMES), r)]
            mayor = next(q for q in g.players if not q.evil and q.character != 'Soldier')
            choices.append(mayor_choice(g, mayor, g.demon()))
            for c in choices:
                for _ in range(3):
                    v = c.options(r)
                    self.assertTrue(c.legal(v), (seed, c.id, v))

    def test_drunk_information_tells_one_consistent_story(self):
        chars = ['Imp', 'Poisoner', 'Monk', 'Drunk', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Empath')
        r = random.Random(5)
        from clocktower.state import empath_choice
        answers = {empath_choice(g, g[D], r).options(r)['number'] for _ in range(20)}
        self.assertEqual(len(answers), 1)
        framed, evil = g.decoy(g[D], r)
        self.assertFalse(g[framed].evil)
        self.assertNotIn(A, evil)  # the real Imp looks good

    def test_drunk_washerwoman_vouches_for_evil(self):
        chars = ['Imp', 'Poisoner', 'Monk', 'Drunk', 'Chef', 'Empath', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Washerwoman')
        g.bluffs = ['Virgin', 'Slayer', 'Recluse']
        r = random.Random(2)
        v = pair_choice(g, g[D], 'Washerwoman', r).options(r)
        self.assertTrue({A, B} & set(v['players']))
        self.assertIn(v['character'], ('Virgin', 'Slayer'))


class WholeGameTests(unittest.TestCase):
    def test_random_games_finish(self):
        for seed in range(40):
            log = []
            rng = random.Random(seed)
            g = Game({n: RandomSeat(n, random.Random(rng.random()), NAMES) for n in NAMES},
                     ScriptedStoryteller(random.Random(seed)), seed=seed)
            result = run(g.run())
            self.assertFalse(result['errors'], result['errors'])
            self.assertIn(result['winner'], ('good', 'evil', None))

    def test_seats_receive_only_new_events_and_short_prompts(self):
        """No re-sent history or state dumps: what a seat receives is exactly the events it
        can see (each once) plus a short prompt per turn."""
        from clocktower.render import render
        seen = {n: [] for n in NAMES}

        class Recording(RandomSeat):
            async def act(self, text, request):
                seen[self.name].append((text, request.prompt))
                return await super().act(text, request)

        g = Game({n: Recording(n, random.Random(i), NAMES) for i, n in enumerate(NAMES)},
                 ScriptedStoryteller(random.Random(1)), seed=11)
        run(g.run())
        for name, turns in seen.items():
            self.assertTrue(all(len(p) < 700 for _, p in turns), 'prompts should be short')
            delivered = sum(len(t) - len(p) for t, p in turns)
            events = sum(len(x) + 1 for x in (render(e, name, set(e['dead'])) for e in g.events) if x is not None)
            pending = sum(len(x) + 1 for x in g.buf[name])
            self.assertLessEqual(delivered, events - pending + 8 * len(turns), f'{name} received repeated content')


if __name__ == '__main__':
    unittest.main()
