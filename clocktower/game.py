"""The table: setup, nights, beats, nominations and votes.

A day has two parts, each a series of beats: private time (whispers only; nobody
else sees them, or that they happened) and then the town square (public talk only).
In a beat every seat gets one turn, in a random order, a wave of a few seats at a
time: a wave acts in parallel and later waves see what earlier ones said. Then
nominations: each round, living players who have not nominated may nominate (or
just speak); one nomination is taken, the nominee defends, and votes go clockwise
one at a time with a running tally.
"""
from __future__ import annotations
import asyncio
import json
import math
import random
import re
import time
from pathlib import Path

from .agents import Request, ScriptedStoryteller
from .characters import FIRST_NIGHT, GOOD, MINIONS, OTHER_NIGHTS, TOWNSFOLK, card
from .llm import BudgetExceeded, Reply, SeatFailed
from . import probe
from .prompts import dawn_narration
from .render import render
from .state import (POLICY, Grimoire, bluffs_choice, character_choice, chef_choice, drunk_as_choice, empath_choice,
                    fortune_teller_choice, info_text, mayor_choice, norm, pair_choice, random_setup, red_herring_choice,
                    setup_error, yes_choice)
NAMES = ['Alex', 'Blair', 'Casey', 'Drew', 'Ellis', 'Frankie', 'Gray', 'Harper', 'Indigo']
WHISPERS = 2  # per private-time turn
WORDS = {'beat': 150, 'whisper': 150, 'nominate': 150, 'defense': 200, 'comment': 150, 'vote': 60}

NIGHT_ACTIONS = {  # role: (number of targets, prompt, may choose self)
    'Poisoner': (1, 'Choose a player to poison tonight and tomorrow.', True),
    'Monk': (1, 'Choose a player (not yourself) to protect from the Demon tonight.', False),
    'Imp': (1, 'Choose a player to kill. (Choosing yourself kills you and makes your Minion the new Imp.)', True),
    'Fortune Teller': (2, 'Choose two players: you learn whether either of them is the Demon.', True),
    'Butler': (1, 'Choose your master (not yourself): tomorrow you may only vote if they vote too.', False),
}


def clip(text, words):
    text = ' '.join((text or '').split())
    w = text.split(' ')
    return text if len(w) <= words else ' '.join(w[:words]) + '… [cut off]'


def fmt(value):
    return {k: v for k, v in norm(value).items() if v not in (None, [])}


class Game:
    def __init__(self, seats, storyteller=None, *, names=NAMES, seed=None, private_beats=3, public_beats=3, max_days=10,
                 waves=3, characters=None, minion=None, out=None, seat_factory=None, probes=True):
        """`seats` maps names to seats; alternatively `seat_factory(name, team)` creates them once the
        characters are dealt (so, for example, the evil team can use a different model). `probes` asks
        seats that support it for their beliefs at dawn of day 1 and before each day's nominations,
        outside the game (probe.py). Every day has
        `private_beats` of private time and `public_beats` of town square. `minion` forces the Minion
        character of a random setup (batches rotate it so every Minion is covered). The Storyteller
        defaults to the scripted one (state.POLICY)."""
        self.seats, self.names, self.seat_factory = seats, list(names), seat_factory
        self.meta = {}
        self.seed = seed if seed is not None else random.randrange(2 ** 32)
        self.rng = random.Random(self.seed)
        self.st = storyteller or ScriptedStoryteller(random.Random(self.seed ^ 0x5eed))
        self.private_beats, self.public_beats, self.minion = private_beats, public_beats, minion
        self.max_days, self.waves, self.forced = max_days, waves, characters
        self.out = Path(out) if out else None
        if self.out:
            self.out.mkdir(parents=True, exist_ok=True)
        self.g: Grimoire | None = None
        self.day, self.phase = 0, 'setup'
        self.events, self.calls, self.errors = [], [], []
        self.buf = {n: [] for n in self.names}
        self.executed_today = False
        self.starting = None
        self.addressed = set()  # players named in the last town-square beat
        self.probes, self.probe_tasks, self.probe_log = probes, [], []

    # ---- logging -----------------------------------------------------------------------
    def _write(self, filename, line):
        if self.out:
            with (self.out / filename).open('a') as f:
                f.write(line + '\n')

    def emit(self, kind, data, to='public'):
        dead = {p.name for p in self.g.players if not p.alive} if self.g else set()
        ev = {'seq': len(self.events), 'time': round(time.time(), 2), 'day': self.day, 'phase': self.phase,
              'kind': kind, 'data': data, 'to': to, 'dead': sorted(dead)}
        self.events.append(ev)
        for n in self.names:
            text = render(ev, n, dead)
            if text is not None:
                self.buf[n].append(text)
        self._write('events.jsonl', json.dumps(ev))
        self._write('transcript.md', render(ev, 'omniscient', dead))

    def record_call(self, record):
        self.calls.append(record)
        self._write('calls.jsonl', json.dumps(record))

    # ---- belief probes (outside the game) ---------------------------------------------------------
    def probe(self, point):
        """Fork a belief question to every seat that supports it. Runs in the background on a snapshot
        (the seat's conversation and its pending events, which stay pending), so play never waits."""
        if not self.probes:
            return
        for p in self.g.players:
            seat = self.seats.get(p.name)
            if not hasattr(seat, 'probe'):
                continue
            pending = '\n'.join(self.buf[p.name]).strip()
            text = (pending + '\n\n' if pending else '') + '>>> ' + probe.prompt(p.evil)
            meta = {'day': self.day, 'point': point}
            record = {**meta, 'player': p.name, 'character': p.character, 'shown': p.shown,
                      'team': 'evil' if p.evil else 'good', 'alive': p.alive,
                      'truth': {q.name: {'character': q.character, 'evil': q.evil} for q in self.g.players}}
            self.probe_tasks.append(asyncio.create_task(self._probe(seat, text, meta, record)))

    async def _probe(self, seat, text, meta, record):
        try:
            reply = await seat.probe(text, meta)
        except Exception as e:  # a failed probe never touches the game
            record.update(error=repr(e))
        else:
            say = (reply.action or {}).get('say') or ''
            record.update(raw=say, thinking=reply.thinking, **probe.parse(say, self.names))
        self.probe_log.append(record)
        self._write('probes.jsonl', json.dumps(record))

    # ---- asking seats and the Storyteller ------------------------------------------------------
    async def ask(self, name, request: Request) -> dict:
        text = '\n'.join(self.buf[name]).strip()
        self.buf[name] = []
        text = (text + '\n\n' if text else '') + '>>> ' + request.prompt
        try:
            reply = await self.seats[name].act(text, request)
        except BudgetExceeded:
            raise
        except Exception as e:  # after the client's own retries: stop the game, never play on without a seat
            self.errors.append(f'{name}: {e!r}')
            self.emit('text', {'text': f'[error] {name}: {e!r}'}, 'audit')
            raise SeatFailed(f'{name}: {e!r}') from e
        if reply.thinking:
            self.emit('thinking', {'player': name, 'kind': request.kind, 'text': reply.thinking}, 'audit')
        return reply.action or {}

    async def ask_many(self, requests: dict) -> dict:
        names = list(requests)
        results = await asyncio.gather(*(self.ask(n, requests[n]) for n in names))
        return dict(zip(names, results))

    def decide(self, choice):
        """The Storyteller's value for a Choice. Choices with one legal value need no decision."""
        if choice.auto:
            return choice.values[0]
        value = norm(self.st.choose(choice))
        if not choice.legal(value):
            raise ValueError(f'illegal Storyteller value for {choice.id}: {value}')
        self.emit('st_choice', {'id': choice.id, 'value': fmt(value), 'valid': True}, 'audit')
        return value

    # ---- setup -------------------------------------------------------------------------------
    async def setup(self):
        names, seating = self.names, ', '.join(self.names)
        if self.forced:
            chars = list(self.forced)  # a forced setup (tests, --characters) keeps its seating order
        else:
            chars = random_setup(self.rng, self.minion)
            self.rng.shuffle(chars)
        err = setup_error(chars)
        if err:
            raise ValueError(err)
        self.g = g = Grimoire(names, chars)

        in_play = set(chars)
        drunk = g.with_character('Drunk')
        if drunk:
            drunk.shown = self.decide(drunk_as_choice([c for c in TOWNSFOLK if c not in in_play]))['character']
        if any(p.shown == 'Fortune Teller' for p in g.players):  # the Drunk-as-Fortune-Teller too
            g.red_herring = self.decide(red_herring_choice(g))['players'][0]
        g.bluffs = self.decide(bluffs_choice([c for c in GOOD if c not in in_play], 'Baron' in in_play,
                                             drunk.shown if drunk else None))['characters']
        self.starting = {p.name: p.character for p in g.players}
        if self.seat_factory:
            self.seats = {p.name: self.seat_factory(p.name, 'evil' if p.evil else 'good') for p in g.players}
        self.emit('setup', {'seats': [{'name': p.name, 'character': p.character, 'shown': p.shown} for p in g.players],
                            'red_herring': g.red_herring, 'bluffs': g.bluffs}, 'audit')

        for p in g.players:
            left, right = names[(p.seat - 1) % len(names)], names[(p.seat + 1) % len(names)]
            lines = [f'You are {p.name}. The players, clockwise: {seating} (and back to {names[0]}). '
                     f'You sit between {left} and {right}.',
                     f'Your character: {card(p.shown)}']
            if p.character == 'Imp':
                minions = [q.name for q in g.players if q.character in MINIONS]
                lines.append(f'Your Minion: {", ".join(minions)} (you do not know which Minion character). '
                             f'Three good characters not in play, for evil to bluff: {", ".join(g.bluffs)}.')
            elif p.character in MINIONS:
                lines.append(f'The Demon is {g.demon().name}.')
            self.emit('intro', {'text': '\n'.join(lines)}, [p.name])

    # ---- night -------------------------------------------------------------------------------
    def targets(self, name, action, request):
        chosen = [x for x in dict.fromkeys(action.get('targets') or []) if x in request.options][:request.n_targets]
        if len(chosen) < request.n_targets:
            chosen += self.rng.sample([x for x in request.options if x not in chosen], request.n_targets - len(chosen))
            self.emit('notice', {'text': f'(Your choice was incomplete, so the Storyteller chose for you: '
                                         f'{", ".join(chosen)}.)'}, [name])
        return chosen

    def kill(self, p, cause):
        g = self.g
        before = g.alive_count()
        g.die(p)
        self.emit('death', {'player': p.name, 'cause': cause}, 'audit')
        if p.character == 'Imp' and cause != 'starpass':
            heir = g.scarlet_woman_heir(before)
            if heir:
                heir.character = heir.shown = 'Imp'
                self.emit('becomes', {'player': heir.name, 'character': 'Imp'}, 'audit')
                self.emit('notice', {'text': 'The Demon has died — and because you are the Scarlet Woman, you are '
                                             'now the Imp! From the next night you choose who dies.'}, [heir.name])

    async def night(self, n):
        g, names, first = self.g, self.names, n == 1
        self.day, self.phase = n, 'night'
        g.poisoned = g.protected = None
        self.emit('header', {'text': f'Night {n}'})

        chosen = {}

        async def wake(roles):
            """Ask the living players with these (apparent) night abilities for their choices, at once."""
            requests = {}
            for p in g.living():
                if p.shown not in roles or (first and p.shown in ('Monk', 'Imp')):
                    continue
                k, text, may_self = NIGHT_ACTIONS[p.shown]
                options = [x for x in names if may_self or x != p.name]
                requests[p.name] = Request('night', f'Night {n} — {p.shown}: {text} Put your choice in `targets`.', n,
                                           n_targets=k, options=options)
            acts = await self.ask_many(requests)
            for name, req in requests.items():
                chosen[name] = self.targets(name, acts[name], req)
                self.emit('night_choice', {'player': name, 'role': g[name].shown, 'targets': chosen[name]}, 'audit')

        # Official night order: the Poisoner, Monk and Imp act before the Fortune Teller and Butler, so
        # a player killed tonight is never woken to choose. (Night 1 has no kill: one round.)
        await wake(('Poisoner', 'Monk', 'Imp') if not first else tuple(NIGHT_ACTIONS))

        def choice_of(character):
            p = g.with_character(character)
            return (p, chosen[p.name][0]) if p and p.name in chosen else (p, None)

        _, t = choice_of('Poisoner')
        if t:
            g.poisoned = t
        monk, t = choice_of('Monk')
        if t and g.works(monk, 'Monk'):
            g.protected = t

        deaths = []
        imp, t = choice_of('Imp')
        if imp and t and not g.is_poisoned(imp):
            target = g[t]
            if target is imp and imp.name != g.protected:  # a Monk-protected Imp cannot die, so no starpass
                self.kill(imp, 'starpass')
                deaths.append(imp)
                heir = next((q for q in g.living() if q.character in MINIONS), None)
                if heir:
                    if heir.character == 'Poisoner':
                        g.poisoned = None  # the Poisoner's poison ends when they stop being the Poisoner
                    heir.character = heir.shown = 'Imp'
                    self.emit('becomes', {'player': heir.name, 'character': 'Imp'}, 'audit')
                    self.emit('notice', {'text': f'Night {n}: the Imp killed themselves, and you are now the Imp! '
                                                 'From tomorrow night you choose who dies.'}, [heir.name])
            elif target.alive and not g.works(target, 'Soldier') and target.name != g.protected:
                victim = target
                if g.works(target, 'Mayor'):
                    victim = g[self.decide(mayor_choice(g, target, imp))['players'][0]]
                self.kill(victim, 'demon')
                deaths.append(victim)
        if not first:
            await wake(('Fortune Teller', 'Butler'))
        butler, t = choice_of('Butler')
        g.master = t if butler and butler.alive else None

        info = []  # (recipient, ability, choice, target for the message)
        for d in deaths:
            if d.shown == 'Ravenkeeper':
                req = Request('ravenkeeper', f'Night {n}: you were killed in the night. Ravenkeeper: choose a player '
                                             'to learn their character (`targets`).', n, n_targets=1, options=names)
                t = self.targets(d.name, await self.ask(d.name, req), req)[0]
                info.append((d, 'Ravenkeeper', character_choice(g, d, 'Ravenkeeper', t), t))
        for role in (FIRST_NIGHT if first else OTHER_NIGHTS):
            for p in g.players:
                if not p.alive or p.shown != role:
                    continue
                if role in ('Washerwoman', 'Librarian', 'Investigator'):
                    info.append((p, role, pair_choice(g, p, role), None))
                elif role == 'Chef':
                    info.append((p, role, chef_choice(g, p), None))
                elif role == 'Empath':
                    info.append((p, role, empath_choice(g, p), None))
                elif role == 'Fortune Teller' and p.name in chosen:
                    info.append((p, role, fortune_teller_choice(g, p, chosen[p.name]), chosen[p.name]))
                elif role == 'Undertaker' and g.executed_death:
                    info.append((p, role, character_choice(g, p, 'Undertaker', g.executed_death),
                                 g.executed_death))

        for p, role, c, target in info:
            text = info_text(role, self.decide(c), target)
            self.emit('info', {'text': f'Night {n} — {role}: {text}'}, [p.name])
        spy = g.with_character('Spy')
        if spy and spy.alive:
            self.emit('info', {'text': f'Night {n} — Spy: you look at the Grimoire.\n'
                                       + g.grimoire_text()}, [spy.name])

        self.phase = 'day'
        self.emit('header', {'text': f'Day {n}'})
        self.emit('dawn', {'day': n, 'deaths': [d.name for d in deaths],
                           'narration': dawn_narration(self.rng, [d.name for d in deaths])})
        if first:
            self.probe('dawn')

    # ---- day ---------------------------------------------------------------------------------
    def whispers(self, name, action):
        """Up to WHISPERS whispers, each to one or two players. Anything beyond that is dropped, and the
        sender is told (so they don't believe a player heard what they never received)."""
        out, dropped = [], []
        sent = [w for w in (action.get('whispers') or []) if isinstance(w, dict)]
        for i, w in enumerate(sent):
            to = [t for t in dict.fromkeys(w.get('to') or []) if t in self.names and t != name]
            text = clip(w.get('text'), WORDS['whisper'])
            if not (to and text):
                continue
            if i >= WHISPERS:
                dropped.append(f'your whisper to {", ".join(to)} was not sent (at most {WHISPERS} whispers a turn)')
                continue
            if len(to) > 2:
                dropped.append(f'your whisper to {", ".join(to)} went only to {to[0]} and {to[1]} '
                               '(a whisper goes to one or two players)')
            out.append({'to': to[:2], 'text': text})
        if dropped:
            self.emit('notice', {'text': '(' + '; '.join(dropped).capitalize() + '.)'}, [name])
        return out

    async def turns(self, n, order, kind, head, tail, words, beat=None, private=False):
        """One turn each for `order`, a wave of a few players at a time: a wave acts simultaneously
        and later waves see what earlier ones said. A private turn is whispers; a public turn is
        speech plus, for anyone claiming to be the Slayer, a shot."""
        g = self.g
        size = math.ceil(len(order) / self.waves)
        waves = [order[i:i + size] for i in range(0, len(order), size)]
        for w, wave in enumerate(waves, start=1):
            requests = {}
            for name in wave:
                prompt = f'{head} — your turn. {tail}'
                if not g[name].alive:
                    prompt += ' (You are dead, but you can still ' + ('whisper.)' if private else 'talk.)')
                requests[name] = Request(kind, prompt, n, beat=beat, alive=g[name].alive,
                                         mode='private' if private else 'public')
            acts = await self.ask_many(requests)
            if private:
                for name in wave:
                    for msg in self.whispers(name, acts[name]):
                        self.emit('whisper', {'from': name, **msg}, [name, *msg['to']])
                continue
            for name in wave:
                say = clip(acts[name].get('say'), words)
                if say:
                    self.emit('say', {'speaker': name, 'text': say})
                    self.addressed |= {x for x in self.names if x != name and re.search(rf'\b{x}\b', say)}
            self.shots(wave, acts)
            if g.winner:
                return

    async def beat(self, n, k, private):
        """Everyone gets one turn, in a random order. In private time players can only whisper;
        in the town square they can only speak, and whoever was just named answers first."""
        total = self.private_beats if private else self.public_beats
        order = list(self.names)
        self.rng.shuffle(order)
        if not private and k > 1:
            order.sort(key=lambda x: x not in self.addressed)
        self.addressed = set()
        self.emit('header', {'text': f'Day {n} · {"private time" if private else "town square"} {k}'})
        if private:
            tail = (f'Whisper to anyone you like (up to {WHISPERS} whispers), or no one. Nobody can address the town '
                    'until the town square.')
        else:
            tail = 'Say something to the town, or nothing. No whispering now.'
            if k == total:
                tail += ' This is the last beat before nominations.'
        await self.turns(n, order, 'beat', f'Day {n}, {"private time" if private else "town square"} {k} of {total}',
                         tail, WORDS['beat'], beat=k, private=private)

    def shots(self, names, acts):
        """Slayer shots taken on these public turns, in order."""
        for name in names:
            t = acts[name].get('slayer_shot')
            if t in self.names and t != name and not self.g.winner:
                self.slayer(name, t)

    def slayer(self, shooter, target):
        g = self.g
        s, t = g[shooter], g[target]
        died = False
        if s.alive and s.character == 'Slayer' and not g.slayer_used:
            g.slayer_used = True
            if not g.is_poisoned(s) and t.alive:
                if t.character == 'Imp':
                    died = True
                elif t.character == 'Recluse' and not g.is_poisoned(t):
                    died = self.decide(yes_choice(f'Slayer:{t.name}', POLICY['recluse_slain']))['yes']
        self.emit('slayer', {'shooter': shooter, 'target': target, 'died': died})
        if died:
            self.kill(t, 'slayer')
            g.check_victory()

    def execute(self, name):
        g, p = self.g, self.g[name]
        died = p.alive
        self.executed_today = True
        self.emit('execution', {'player': name, 'died': died})
        if died:
            g.alive_at_execution = g.alive_count()
            saint = g.works(p, 'Saint')
            self.kill(p, 'execution')
            g.executed_death = name
            if saint:
                g.winner, g.reason = 'evil', f'{name} was the Saint, and the Saint was executed.'
        g.check_victory()

    def virgin(self, nominator, nominee):
        """Returns True if the Virgin's ability executed the nominator."""
        g, v = self.g, self.g[nominee]
        if v.character != 'Virgin' or g.virgin_used:
            return False
        g.virgin_used = True
        if not g.works(v, 'Virgin'):
            return False
        nom = g[nominator]
        townsfolk = nom.character in TOWNSFOLK
        if nom.character == 'Spy' and not g.is_poisoned(nom):
            townsfolk = self.decide(yes_choice(f'Virgin:{nominator}', POLICY['spy_virgin']))['yes']
        if not townsfolk:
            return False
        self.emit('virgin', {'nominator': nominator, 'nominee': nominee})
        self.execute(nominator)
        return True

    def vote_order(self, nominee):
        i = self.names.index(nominee)
        return [self.names[(i + k) % len(self.names)] for k in range(1, len(self.names) + 1)]

    async def vote(self, nominee, block, top):
        g, n = self.g, self.day
        needed = math.ceil(g.alive_count() / 2)
        required = max(needed, top + 1)
        yes, voted = [], set()
        for voter in self.vote_order(nominee):
            p = g[voter]
            if not p.alive and not p.ghost_vote:
                continue
            lines = [f'Vote: should {nominee} be executed? It takes {required} yes votes to put them on the block']
            if block:
                lines[0] += f' (replacing {block}, who has {top})'
            elif top:
                lines[0] += f' (more than the {top} of an earlier tied vote)'
            lines[0] += '.'
            lines.append(f'Yes so far: {", ".join(yes) if yes else "none"} ({len(yes)}).')
            if not p.alive:
                lines.append('You are dead: voting yes uses your one ghost vote.')
            if p.character == 'Butler' and p.alive and g.master:  # poisoned or not: the Butler can't tell
                if g.master in yes:
                    seen = 'they voted yes, so you may vote'
                elif g.master in voted:
                    seen = 'they voted no, so you may not vote yes'
                else:
                    seen = 'they vote after you, so their hand is not up and you may not vote yes'
                lines.append(f'Your master is {g.master} ({seen}).')
            lines.append('Set `vote` to true or false; `say` may hold a very short remark (optional; don\'t just restate your vote).')
            a = await self.ask(voter, Request('vote', ' '.join(lines), n, options=[nominee]))
            if not isinstance(a.get('vote'), bool):  # no vote given: ask once more rather than assume no
                a = await self.ask(voter, Request('vote', 'Your vote was missing. Set `vote` to true (yes) or '
                                                          f'false (no): should {nominee} be executed?', n,
                                                  options=[nominee]))
            v = a.get('vote') is True
            remark = clip(a.get('say'), WORDS['vote'])
            if v and g.works(p, 'Butler') and g.master and g.master not in yes:
                v, remark = False, ''  # a Butler may only raise their hand while their master's is up
                self.emit('notice', {'text': f'(Your master {g.master} has not voted yes, so you cannot vote.)'}, [voter])
            ghost = v and not p.alive
            if ghost:
                p.ghost_vote = False
            self.emit('vote', {'voter': voter, 'nominee': nominee, 'yes': v, 'ghost': ghost, 'text': remark})
            voted.add(voter)
            if v:
                yes.append(voter)
        count = len(yes)
        if count >= needed and count > top:
            block, top, outcome = nominee, count, 'block'
        elif count >= needed and count == top:
            block, outcome = None, 'tie'
        else:
            outcome = 'short'
        self.emit('vote_result', {'nominee': nominee, 'votes': count, 'needed': required, 'outcome': outcome,
                                  'voters': yes})
        return block, top

    async def nominations(self):
        """Rounds until a call gets no nomination. Each round: every living player who hasn't
        nominated today is asked at once whether to nominate (if several do, one is taken at random,
        as when hands go up together); then the accusation, the defense, one round of comments from
        everyone, and the clockwise vote."""
        g, n = self.g, self.day
        self.phase = 'nominations'
        self.emit('nominations_open', {})
        nominators, nominees = set(), set()
        block, top = None, 0
        while not g.winner:
            eligible = [p.name for p in g.living() if p.name not in nominators]
            options = [x for x in self.names if x not in nominees]
            if not eligible or not options:
                break
            status = (f'{block} is on the block with {top} votes.' if block else
                      f'Nobody is on the block (an earlier vote tied at {top}).' if top else 'Nobody is on the block yet.')
            prompt = (f'Day {n}, nominations. {status} Already nominated today: {", ".join(sorted(nominees)) or "nobody"}. '
                      'You may nominate someone (set `nominate`; your `say` is the accusation), or pass. Only '
                      'nominations are heard now: everyone can comment after the defense. No whispering now.')
            acts = await self.ask_many({name: Request('nominate', prompt, n, options=options) for name in eligible})
            self.shots(eligible, acts)
            if g.winner:
                return
            noms = [(name, acts[name]['nominate'], clip(acts[name].get('say'), WORDS['nominate']))
                    for name in eligible if acts[name].get('nominate') in options]
            if not noms:
                break
            nominator, nominee, accusation = self.rng.choice(noms)
            for other, t, _ in noms:
                if other != nominator:
                    self.emit('notice', {'text': f'(Your nomination of {t} was not taken: several players nominated at '
                                                 f'once, and {nominator}\'s nomination of {nominee} was picked at '
                                                 'random. You can nominate again later.)'}, [other])
            nominators.add(nominator)
            nominees.add(nominee)
            self.emit('nomination', {'nominator': nominator, 'nominee': nominee, 'text': accusation})
            if self.virgin(nominator, nominee):
                return
            d = await self.ask(nominee, Request('defense', f'Day {n}: {nominator} has nominated you. '
                                                           'Give your defense in `say`.', n))
            self.emit('defense', {'nominee': nominee, 'text': clip(d.get('say'), WORDS['defense'])})
            order = list(self.names)
            self.rng.shuffle(order)
            await self.turns(n, order, 'comment', f'Day {n}, comments on the nomination of {nominee}',
                             'Say something to the town before the vote, or nothing. No whispering now.', WORDS['comment'])
            if g.winner:
                return
            block, top = await self.vote(nominee, block, top)
        if g.winner:
            return
        if block:
            self.execute(block)
        else:
            self.emit('no_execution', {})

    async def daytime(self, n):
        g = self.g
        g.executed_death, self.executed_today = None, False
        for private, total in ((True, self.private_beats), (False, self.public_beats)):
            for k in range(1, total + 1):
                await self.beat(n, k, private)
                if g.winner:
                    return
        self.probe('nominations')
        await self.nominations()
        if g.winner:
            return
        mayor = g.with_character('Mayor')
        if not self.executed_today and g.alive_count() == 3 and mayor and g.works(mayor, 'Mayor'):
            g.winner, g.reason = 'good', 'Three players remain, there was no execution, and the Mayor lives.'

    # ---- the whole game ------------------------------------------------------------------------
    async def run(self):
        start = time.time()
        stopped = None
        try:
            await self.setup()
            n = 1
            while True:
                await self.night(n)
                if self.g.check_victory():
                    break
                await self.daytime(n)
                if self.g.check_victory():
                    break
                if n >= self.max_days:
                    stopped = f'stopped after day {n}'
                    break
                n += 1
        except BudgetExceeded as e:
            stopped = f'budget: {e}'
        except SeatFailed as e:
            stopped = f'seat failed: {str(e)[:300]}'
        if self.probe_tasks:
            await asyncio.gather(*self.probe_tasks)
        g = self.g
        if g and g.winner:
            self.emit('game_over', {'winner': g.winner, 'reason': g.reason})
        result = self.result(time.time() - start, stopped)
        if self.out:
            (self.out / 'result.json').write_text(json.dumps(result, indent=2))
        return result

    def result(self, seconds, stopped):
        g = self.g
        usage = {'input': 0, 'cache_read': 0, 'cache_write': 0, 'output': 0}
        for c in self.calls:
            u = c.get('usage', {})
            usage['input'] += u.get('input_tokens', 0)
            usage['cache_read'] += u.get('cache_read_input_tokens', 0)
            usage['cache_write'] += u.get('cache_creation_input_tokens', 0)
            usage['output'] += u.get('output_tokens', 0)
        return {'winner': g.winner if g else None, 'reason': (g.reason if g else None) or stopped,
                'stopped': stopped, 'days': self.day, 'seed': self.seed, 'starting': self.starting,
                'final': {p.name: p.character for p in g.players} if g else None,
                'bluffs': g.bluffs if g else None, 'red_herring': g.red_herring if g else None,
                'drunk_as': next((p.shown for p in g.players if p.character == 'Drunk'), None) if g else None,
                'cost': round(sum(c.get('cost', 0) for c in self.calls), 4), 'calls': len(self.calls),
                'tokens': usage, 'seconds': round(seconds, 1), 'errors': self.errors, **self.meta}
