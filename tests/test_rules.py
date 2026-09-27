import asyncio
import random
import unittest

from clocktower.agents import RandomSeat, ScriptedStoryteller
from clocktower.game import NAMES, Game
from clocktower.llm import Reply
from clocktower.state import POLICY, Grimoire, chef_choice, pair_choice, setup_error

A, B, C, D, E, F, G, H, I = NAMES
BLANK = {'say': '', 'whispers': [], 'nominate': None, 'vote': None, 'targets': [], 'slayer_shot': None}


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

    def choose(self, choice):
        return {**choice.options(self.rng), **self.decisions.get(choice.id, {})}


class policy:
    """Temporarily override POLICY numbers."""

    def __init__(self, **kw):
        self.kw, self.old = kw, {}

    def __enter__(self):
        self.old = {k: POLICY[k] for k in self.kw}
        POLICY.update(self.kw)

    def __exit__(self, *exc):
        POLICY.update(self.old)


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

    def test_nomination_has_accusation_defense_comments_then_votes(self):
        def policy(name, req):
            if req.kind == 'nominate' and name == C and req.options and D in req.options:
                return {'nominate': D, 'say': 'Suspicious.'}
            if req.kind == 'comment':
                return {'say': f'{name} comments.'}
        g = self.prepared(BASE, policy)
        run(g.nominations())
        kinds = [e['kind'] for e in g.events if e['kind'] in ('nomination', 'defense', 'say', 'vote')]
        self.assertEqual(kinds[:2], ['nomination', 'defense'])
        self.assertEqual(kinds[2:11], ['say'] * 9)  # everyone, the dead too, comments once
        self.assertEqual(kinds[11:], ['vote'] * 9)

    def test_slayer_can_shoot_during_nominations(self):
        chars = ['Imp', 'Poisoner', 'Slayer', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Recluse']
        def policy(name, req):
            if req.kind == 'nominate' and name == D and req.options and E in req.options:
                return {'nominate': E}
            if req.kind == 'comment' and name == C:
                return {'slayer_shot': A}
        g = self.prepared(chars, policy)
        run(g.nominations())
        self.assertEqual(g.g.winner, 'good')
        self.assertFalse(any(e['kind'] == 'vote' for e in g.events))

    def test_every_day_runs_all_beats_even_when_silent(self):
        g = self.prepared(BASE, lambda n, r: None)  # nobody ever says or whispers anything
        run(g.daytime(1))
        beats = [e['data']['text'] for e in g.events if e['kind'] == 'header' and '·' in e['data']['text']]
        self.assertEqual(beats, [f'Day 1 · private time {k}' for k in (1, 2, 3)]
                         + [f'Day 1 · town square {k}' for k in (1, 2, 3)])

    def test_mayor_wins_with_three_alive_and_no_execution(self):
        chars = ['Imp', 'Poisoner', 'Mayor', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = self.prepared(chars, lambda n, r: None)
        for x in (D, E, F, G, H, I):
            g.g.die(g.g[x])
        g.private_beats, g.public_beats = 1, 1
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
        c = chef_choice(g, g[C])
        self.assertTrue(c.legal({'number': 0}) and c.legal({'number': 1}))
        self.assertFalse(c.legal({'number': 2}))
        self.assertFalse(c.auto)

    def test_washerwoman_pair_must_contain_the_townsfolk(self):
        g = Grimoire(NAMES, BASE)
        c = pair_choice(g, g[F], 'Washerwoman')
        self.assertTrue(c.legal({'players': [C, A], 'character': 'Monk'}))
        self.assertFalse(c.legal({'players': [B, A], 'character': 'Monk'}))
        self.assertFalse(c.legal({'players': [F, C], 'character': 'Monk'}))  # never shown themselves
        self.assertTrue(c.legal(c.options(random.Random(0))))

    def test_drunk_washerwoman_can_be_told_anything(self):
        chars = ['Imp', 'Poisoner', 'Monk', 'Empath', 'Chef', 'Drunk', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Washerwoman')
        c = pair_choice(g, g[F], 'Washerwoman')
        self.assertTrue(c.legal({'players': [B, A], 'character': 'Mayor'}))

    def test_spy_can_register_as_townsfolk(self):
        chars = ['Imp', 'Spy', 'Monk', 'Empath', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars)
        c = pair_choice(g, g[F], 'Washerwoman')
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
                    choices.append(pair_choice(g, p, ability))
                choices += [chef_choice(g, p), empath_choice(g, p),
                            fortune_teller_choice(g, p, r.sample(NAMES, 2)),
                            character_choice(g, p, 'Undertaker', r.choice(NAMES))]
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
        with policy(any=0, drunk_truthful=0):
            answers = {empath_choice(g, g[D]).options(r)['number'] for _ in range(20)}
        self.assertEqual(len(answers), 1)
        framed, evil = g.decoy(g[D], r)
        self.assertFalse(g[framed].evil)
        self.assertNotIn(A, evil)  # the real Imp looks good

    def test_drunk_washerwoman_vouches_for_evil(self):
        chars = ['Imp', 'Poisoner', 'Monk', 'Drunk', 'Chef', 'Empath', 'Soldier', 'Butler', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Washerwoman')
        g.bluffs = ['Virgin', 'Slayer', 'Recluse']
        r = random.Random(2)
        with policy(any=0, drunk_truthful=0, false_vouch_evil=1, as_bluff=1):
            v = pair_choice(g, g[D], 'Washerwoman').options(r)
        self.assertTrue({A, B} & set(v['players']))
        self.assertIn(v['character'], ('Virgin', 'Slayer'))


    def test_nothing_legal_is_ruled_out(self):
        from clocktower.state import character_choice, empath_choice
        r = random.Random(0)
        # a drunk Empath can be told any number, a sober Undertaker can see the Recluse as the Imp,
        # and the Spy can register as a good character that is in play
        chars = ['Imp', 'Spy', 'Monk', 'Drunk', 'Chef', 'Washerwoman', 'Soldier', 'Recluse', 'Saint']
        g = Grimoire(NAMES, chars, drunk_as='Empath')
        c = empath_choice(g, g[D])
        self.assertEqual({c.options(r)['number'] for _ in range(2000)}, {0, 1, 2})
        c = character_choice(g, g[E], 'Undertaker', H)
        self.assertIn('Imp', {c.options(r)['character'] for _ in range(2000)})
        c = character_choice(g, g[E], 'Undertaker', B)
        self.assertTrue({'Monk', 'Chef', 'Washerwoman'} & {c.options(r)['character'] for _ in range(2000)})
        # every legal value has a chance, and only legal values are drawn
        c = pair_choice(g, g[F], 'Washerwoman')
        with policy(any=1):
            seen = {tuple(sorted(v['players'])) + (v['character'],) for v in (c.options(r) for _ in range(20000))}
        self.assertTrue(all(c.legal({'players': list(k[:2]), 'character': k[2]}) for k in seen))
        self.assertEqual(len(seen), len(c.keys))

    def test_the_drunk_is_sometimes_told_the_truth_all_game(self):
        from clocktower.state import empath_choice
        chars = ['Imp', 'Poisoner', 'Monk', 'Drunk', 'Chef', 'Washerwoman', 'Soldier', 'Butler', 'Saint']
        truthful = 0
        with policy(any=0):
            for seed in range(200):
                g = Grimoire(NAMES, chars, drunk_as='Empath')
                r = random.Random(seed)
                answers = {empath_choice(g, g[D]).options(r)['number'] for _ in range(5)}
                self.assertEqual(len(answers), 1)  # consistent either way
                truthful += answers == {0}  # the Drunk's real neighbours are good
        self.assertTrue(20 < truthful < 120, truthful)


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



class ProbeTests(unittest.TestCase):
    def test_parse(self):
        from clocktower.probe import parse
        text = ('Alex | 80% | 60 | Imp\n`Blair (dead)` | 10% | 0% | Chef\nnoise\nClaim | Empath\nPlan | Push Alex | today')
        out = parse(text, NAMES)
        self.assertEqual(out['players']['Alex'], {'evil': 0.8, 'demon': 0.6, 'character': 'Imp'})
        self.assertEqual(out['players']['Blair']['evil'], 0.1)
        self.assertEqual((out['claim'], out['plan']), ('Empath', 'Push Alex | today'))

    def test_probes_leave_the_game_unchanged(self):
        """Same seed with and without probes: identical events and identical turns for every seat."""
        def play(probes):
            seen, asked = [], []

            class Probed(RandomSeat):
                async def act(self, text, request):
                    seen.append((self.name, text))
                    return await super().act(text, request)

                async def probe(self, text, meta):
                    asked.append((self.name, meta['point'], text))
                    return Reply({**BLANK, 'say': 'Alex | 50 | 20 | Chef\nClaim | none\nPlan | wait'})

            seats = {n: Probed(n, random.Random(i), NAMES) for i, n in enumerate(NAMES)}
            g = Game(seats, ScriptedStoryteller(random.Random(3)), seed=5, probes=probes)
            run(g.run())
            return [(e['kind'], e['data']) for e in g.events], seen, asked, g
        events, seen, _, _ = play(False)
        events2, seen2, asked, g = play(True)
        self.assertEqual(events, events2)
        self.assertEqual(seen, seen2)
        points = [p for _, p, _ in asked]
        self.assertEqual(points.count('dawn'), 9)
        self.assertGreaterEqual(points.count('nominations'), 9)
        self.assertEqual(len(g.probe_log), len(asked))
        self.assertTrue(all(r['players']['Alex']['evil'] == 0.5 for r in g.probe_log))

    def test_claude_fork_does_not_touch_the_conversation(self):
        from types import SimpleNamespace as NS
        from clocktower.llm import ClaudeConversation, Ledger
        sent = []

        class Stream:
            def __init__(self, **kw):
                sent.append(kw['messages'])

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def get_final_message(self):
                usage = NS(model_dump=lambda **k: {'input_tokens': 1, 'output_tokens': 1})
                block = NS(type='text', text='{"say": "hi"}', model_dump=lambda **k: {'type': 'text', 'text': '{"say": "hi"}'})
                return NS(usage=usage, content=[block], stop_reason='end_turn', stop_details=None)

        import tempfile, pathlib
        client = NS(messages=NS(stream=lambda **kw: Stream(**kw)))
        ledger = Ledger(pathlib.Path(tempfile.mkdtemp()) / 'l.jsonl')
        c = ClaudeConversation(client, 'sys', {}, label='Alex', ledger=ledger, semaphore=asyncio.Semaphore(1))
        run(c.send('turn 1'))
        before = [dict(m) for m in c.messages]
        reply = run(c.send('probe?', commit=False))
        self.assertEqual(reply.action, {'say': 'hi'})
        self.assertEqual(c.messages, before)
        self.assertEqual(sent[-1], before + [{'role': 'user', 'content': 'probe?'}])
        run(c.send('turn 2'))
        self.assertEqual(sent[-1][:len(before)], before)
        self.assertEqual(len(c.messages), 4)


if __name__ == '__main__':
    unittest.main()
