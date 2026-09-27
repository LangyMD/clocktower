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

from .agents import Request, STRequest
from .characters import FIRST_NIGHT, GOOD, MINIONS, OTHER_NIGHTS, OUTSIDERS, TOWNSFOLK, card
from .llm import BudgetExceeded, Reply
from .prompts import dawn_narration
from .render import render
from .state import (POLICY, Grimoire, character_choice, chef_choice, empath_choice, fortune_teller_choice, info_text,
                    mayor_choice, norm, pair_choice, random_setup, setup_error, yes_choice)

INFO_ROLES = {'Washerwoman', 'Librarian', 'Investigator', 'Chef', 'Empath', 'Fortune Teller', 'Undertaker', 'Ravenkeeper'}
NAMES = ['Alex', 'Blair', 'Casey', 'Drew', 'Ellis', 'Frankie', 'Gray', 'Harper', 'Indigo']
WORDS = {'beat': 100, 'whisper': 100, 'nominate': 120, 'defense': 150, 'vote': 30, 'narration': 80}

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
    return text if len(w) <= words else ' '.join(w[:words]) + '…'


def fmt(value):
    return {k: v for k, v in norm(value).items() if v not in (None, [])}


def pick_bluffs(r, options, baron):
    """Three Demon bluffs that suit the setup: at least one information role (so evil can invent
    checkable results) and an Outsider when the Baron is in play (the town can count Outsiders).
    The rest are drawn uniformly from every legal option (the Drunk's apparent role included)."""
    info = [c for c in options if c in INFO_ROLES]
    outsiders = [c for c in options if c in OUTSIDERS]
    picks = []
    if info:
        picks.append(r.choice(info))
    if baron and outsiders:
        picks.append(r.choice(outsiders))
    rest = [c for c in options if c not in picks]
    return (picks + r.sample(rest, 3 - len(picks)))[:3] if len(rest) >= 3 - len(picks) else r.sample(options, 3)


class Game:
    def __init__(self, seats, storyteller, *, names=NAMES, seed=None, private_beats=3, public_beats=3, max_days=10,
                 waves=3, characters=None, setup='random', minion=None, out=None, seat_factory=None):
        """`seats` maps names to seats; alternatively `seat_factory(name, team)` creates them once the
        characters are dealt (so, for example, the evil team can use a different model). Every day has
        `private_beats` of private time and `public_beats` of town square. `minion` forces the Minion
        character of a random setup (batches rotate it so every Minion is covered)."""
        self.seats, self.st, self.names, self.seat_factory = seats, storyteller, list(names), seat_factory
        self.meta = {}
        self.seed = seed if seed is not None else random.randrange(2 ** 32)
        self.rng = random.Random(self.seed)
        self.private_beats, self.public_beats, self.minion = private_beats, public_beats, minion
        self.max_days, self.waves, self.forced = max_days, waves, characters
        self.setup_mode = setup  # 'random': a uniformly drawn legal setup; 'storyteller': the Storyteller picks
        self.out = Path(out) if out else None
        if self.out:
            self.out.mkdir(parents=True, exist_ok=True)
        self.g: Grimoire | None = None
        self.day, self.phase = 0, 'setup'
        self.events, self.calls, self.errors = [], [], []
        self.buf = {n: [] for n in self.names}
        self.st_buf = []
        self.executed_today = False
        self.starting = None
        self.addressed = set()  # players named in the last town-square beat

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
        text = render(ev, 'storyteller', dead)
        if text is not None:
            self.st_buf.append(text)
        self._write('events.jsonl', json.dumps(ev))
        self._write('transcript.md', render(ev, 'omniscient', dead))

    def st_note(self, text):
        self.emit('text', {'text': text}, 'st')

    def record_call(self, record):
        self.calls.append(record)
        self._write('calls.jsonl', json.dumps(record))

    # ---- asking seats and the Storyteller ------------------------------------------------------
    async def ask(self, name, request: Request) -> dict:
        text = '\n'.join(self.buf[name]).strip()
        self.buf[name] = []
        text = (text + '\n\n' if text else '') + '>>> ' + request.prompt
        try:
            reply = await self.seats[name].act(text, request)
        except BudgetExceeded:
            raise
        except Exception as e:  # a failed seat passes rather than crashing the table
            self.errors.append(f'{name}: {e!r}')
            self.emit('text', {'text': f'[error] {name}: {e!r}'}, 'audit')
            reply = Reply({})
        if reply.thinking:
            self.emit('thinking', {'player': name, 'kind': request.kind, 'text': reply.thinking}, 'audit')
        return reply.action or {}

    async def ask_many(self, requests: dict) -> dict:
        names = list(requests)
        results = await asyncio.gather(*(self.ask(n, requests[n]) for n in names))
        return dict(zip(names, results))

    async def st_ask(self, prompt, request: STRequest) -> dict:
        text = '\n'.join(self.st_buf).strip()
        self.st_buf = []
        text = (text + '\n\n' if text else '') + '>>> ' + prompt
        try:
            reply = await self.st.decide(text, request)
        except BudgetExceeded:
            raise
        except Exception as e:
            self.errors.append(f'Storyteller: {e!r}')
            self.emit('text', {'text': f'[error] Storyteller: {e!r}'}, 'audit')
            reply = Reply({})
        if reply.thinking:
            self.emit('thinking', {'player': 'Storyteller', 'kind': request.kind, 'text': reply.thinking}, 'audit')
        return reply.action or {}

    async def decide(self, choices, context, narrate=None):
        """Ask the Storyteller for every non-automatic choice (and optional dawn narration)."""
        ask = [c for c in choices if not c.auto]
        values = {c.id: c.default for c in choices}
        if not ask and narrate is None:
            return values, ''
        lines = [context, '', 'Grimoire:', self.g.grimoire_text()]
        if ask:
            lines += ['', 'Decisions needed (one entry in `decisions` per id):']
            lines += [f'- id "{c.id}": {c.description}' for c in ask]
        if narrate is not None:
            lines += ['', 'Also write `narration`: one or two sentences for dawn. '
                      + (f"Deaths to announce: {', '.join(narrate)}." if narrate else 'Nobody died.')]

        def fallback(r):
            return {'decisions': [{'id': c.id, **norm(c.options(r))} for c in ask],
                    'narration': dawn_narration(r, narrate) if narrate is not None else ''}

        out = await self.st_ask('\n'.join(lines), STRequest('decisions', fallback))
        got = {d.get('id'): d for d in out.get('decisions') or [] if isinstance(d, dict)}
        for c in choices:
            if c.auto:
                continue
            v = got.get(c.id)
            ok = v is not None and c.legal(v)
            values[c.id] = norm(v) if ok else c.default
            self.emit('st_choice', {'id': c.id, 'value': fmt(values[c.id]), 'valid': ok}, 'audit')
            if not ok:
                self.st_note(f'(Your decision "{c.id}" was missing or illegal, so the default was used: {fmt(c.default)}.)')
        return values, clip(out.get('narration'), WORDS['narration'])

    # ---- setup -------------------------------------------------------------------------------
    async def setup(self):
        names, seating = self.names, ', '.join(self.names)
        if self.forced:
            chars = list(self.forced)
        elif self.setup_mode == 'random':
            chars = random_setup(self.rng, self.minion)
            self.rng.shuffle(chars)
        else:
            suggestion = random_setup(self.rng, self.minion)
            out = await self.st_ask(
                f'A new game is about to begin. The nine players, clockwise: {seating}.\n'
                'Choose the nine characters in play (`characters`): the Imp, one Minion, and 5 Townsfolk with 2 '
                'Outsiders, or 3 Townsfolk with 4 Outsiders if the Baron is in play. For variety, here is a '
                f'randomly drawn legal setup you may use as-is or change: {", ".join(suggestion)}.',
                STRequest('characters', lambda r: {'characters': suggestion}))
            chars = out.get('characters') or []
            err = setup_error(chars)
            if err:
                self.st_note(f'(Your setup was not legal — {err} — so the suggested setup was used.)')
                chars = suggestion
            chars = list(chars)
            self.rng.shuffle(chars)  # dealt at random, as from the bag
        err = setup_error(chars)
        if err:
            raise ValueError(err)
        self.g = g = Grimoire(names, chars)  # a forced setup (tests, --characters) keeps its seating order

        in_play = set(chars)
        drunk = g.with_character('Drunk')
        has_ft = 'Fortune Teller' in in_play
        drunk_opts = [c for c in TOWNSFOLK if c not in in_play]
        bluff_opts = [c for c in GOOD if c not in in_play]
        self.rng.shuffle(bluff_opts)
        good = [p.name for p in g.players if not p.evil]


        def fallback(r):  # the scripted Storyteller's setup
            d = None
            if drunk:  # a Drunk who thinks they have information is the most interesting Drunk
                d = r.choices(drunk_opts, [3 if c in INFO_ROLES else 1 for c in drunk_opts])[0]
            return {'drunk_as': d, 'red_herring': r.choice(good) if has_ft else None,
                    'bluffs': pick_bluffs(r, bluff_opts, 'Baron' in in_play)}

        asks = []
        if drunk:
            asks.append(f'`drunk_as`: the Townsfolk the Drunk ({drunk.name}) believes they are, one not in play: '
                        f'{", ".join(drunk_opts)}.')
        if has_ft:
            asks.append('`red_herring`: a good player who registers as a Demon to the Fortune Teller.')
        suggested = pick_bluffs(self.rng, bluff_opts, 'Baron' in in_play)
        asks.append(f'`bluffs`: three good characters not in play, shown to the Imp as safe bluffs. Options: '
                    f'{", ".join(bluff_opts)}. A random draw you may use or change: {", ".join(suggested)}.')
        out = await self.st_ask('The characters have been dealt:\n' + g.grimoire_text() + '\n\nNow choose:\n- '
                                + '\n- '.join(asks), STRequest('setup', fallback))
        fb = fallback(self.rng)
        if drunk:
            d = out.get('drunk_as')
            if d not in drunk_opts:
                self.st_note(f'(drunk_as was not legal; {fb["drunk_as"]} was used.)')
                d = fb['drunk_as']
            drunk.shown = d
        if has_ft:
            rh = out.get('red_herring')
            if rh not in good:
                self.st_note(f'(red_herring was not a good player; {fb["red_herring"]} was used.)')
                rh = fb['red_herring']
            g.red_herring = rh
        bluffs = list(out.get('bluffs') or [])
        if len(set(bluffs)) != 3 or not set(bluffs) <= set(bluff_opts):
            self.st_note(f'(bluffs were not legal; {", ".join(fb["bluffs"])} were used.)')
            bluffs = fb['bluffs']
        g.bluffs = bluffs
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
                self.st_note(f'{heir.name} (Scarlet Woman) has become the Imp.')

    async def night(self, n):
        g, names, first = self.g, self.names, n == 1
        self.day, self.phase = n, 'night'
        g.poisoned = g.protected = None
        self.emit('header', {'text': f'Night {n}'})

        requests = {}
        for p in g.living():
            if p.shown not in NIGHT_ACTIONS or (first and p.shown in ('Monk', 'Imp')):
                continue
            k, text, may_self = NIGHT_ACTIONS[p.shown]
            options = [x for x in names if may_self or x != p.name]
            requests[p.name] = Request('night', f'Night {n} — {p.shown}: {text} Put your choice in `targets`.', n,
                                       n_targets=k, options=options)
        acts = await self.ask_many(requests)
        chosen = {}
        for name, req in requests.items():
            chosen[name] = self.targets(name, acts[name], req)
            self.emit('night_choice', {'player': name, 'role': g[name].shown, 'targets': chosen[name]}, 'audit')

        def choice_of(character):
            p = g.with_character(character)
            return (p, chosen[p.name][0]) if p and p.name in chosen else (p, None)

        _, t = choice_of('Poisoner')
        if t:
            g.poisoned = t
        monk, t = choice_of('Monk')
        if t and g.works(monk, 'Monk'):
            g.protected = t
        butler, t = choice_of('Butler')
        g.master = t if butler and butler.alive else None

        deaths = []
        imp, t = choice_of('Imp')
        if imp and t and not g.is_poisoned(imp):
            target = g[t]
            if target is imp:
                self.kill(imp, 'starpass')
                deaths.append(imp)
                heir = next((q for q in g.living() if q.character in MINIONS), None)
                if heir:
                    heir.character = heir.shown = 'Imp'
                    self.emit('becomes', {'player': heir.name, 'character': 'Imp'}, 'audit')
                    self.emit('notice', {'text': f'Night {n}: the Imp killed themselves, and you are now the Imp! '
                                                 'From tomorrow night you choose who dies.'}, [heir.name])
                    self.st_note(f'{imp.name} (Imp) killed themselves; {heir.name} is now the Imp.')
            elif target.alive and not g.works(target, 'Soldier') and target.name != g.protected:
                victim = target
                if g.works(target, 'Mayor'):
                    c = mayor_choice(g, target, imp)
                    values, _ = await self.decide([c], f'Night {n}: the Imp ({imp.name}) attacks the Mayor.')
                    victim = g[norm(values[c.id])['players'][0]]
                self.kill(victim, 'demon')
                deaths.append(victim)

        info = []  # (recipient, ability, choice, target for the message)
        for d in deaths:
            if d.shown == 'Ravenkeeper':
                req = Request('ravenkeeper', f'Night {n}: you were killed in the night. Ravenkeeper: choose a player '
                                             'to learn their character (`targets`).', n, n_targets=1, options=names)
                t = self.targets(d.name, await self.ask(d.name, req), req)[0]
                info.append((d, 'Ravenkeeper', character_choice(g, d, 'Ravenkeeper', t, self.rng), t))
        for role in (FIRST_NIGHT if first else OTHER_NIGHTS):
            for p in g.players:
                if not p.alive or p.shown != role:
                    continue
                if role in ('Washerwoman', 'Librarian', 'Investigator'):
                    info.append((p, role, pair_choice(g, p, role, self.rng), None))
                elif role == 'Chef':
                    info.append((p, role, chef_choice(g, p, self.rng), None))
                elif role == 'Empath':
                    info.append((p, role, empath_choice(g, p, self.rng), None))
                elif role == 'Fortune Teller' and p.name in chosen:
                    info.append((p, role, fortune_teller_choice(g, p, chosen[p.name], self.rng), chosen[p.name]))
                elif role == 'Undertaker' and g.executed_death:
                    info.append((p, role, character_choice(g, p, 'Undertaker', g.executed_death, self.rng),
                                 g.executed_death))

        values, narration = await self.decide(
            [c for _, _, c, _ in info],
            f'Night {n}. Player choices: '
            + ('; '.join(f'{name} ({g[name].shown}) chose {", ".join(t)}' for name, t in chosen.items()) or 'none')
            + f'. Deaths tonight: {", ".join(d.name for d in deaths) or "none"}.',
            narrate=[d.name for d in deaths])
        given = []
        for p, role, c, target in info:
            text = info_text(role, values[c.id], target)
            self.emit('info', {'text': f'Night {n} — {role}: {text}'}, [p.name])
            given.append(f'{role} ({p.name}): {text}')
        if given:
            self.st_note(f'Information given on night {n}:\n' + '\n'.join(given))
        spy = g.with_character('Spy')
        if spy and spy.alive:
            self.emit('info', {'text': f'Night {n} — Spy: you look at the Grimoire.\n'
                                       + g.grimoire_text([f'Information given tonight: {x}' for x in given])}, [spy.name])

        self.phase = 'day'
        self.emit('header', {'text': f'Day {n}'})
        self.emit('dawn', {'day': n, 'deaths': [d.name for d in deaths], 'narration': narration})

    # ---- day ---------------------------------------------------------------------------------
    def whispers(self, name, action):
        out = []
        for w in (action.get('whispers') or [])[:3]:
            if not isinstance(w, dict):
                continue
            to = [t for t in dict.fromkeys(w.get('to') or []) if t in self.names and t != name][:2]
            text = clip(w.get('text'), WORDS['whisper'])
            if to and text:
                out.append({'to': to, 'text': text})
        return out

    async def beat(self, n, k, private):
        """Everyone gets one turn, in a random order, a wave of a few players at a time.
        Players in a wave act simultaneously; later waves see what earlier waves said.
        In private time players can only whisper; in the town square they can only speak."""
        g = self.g
        total = self.private_beats if private else self.public_beats
        order = list(self.names)
        self.rng.shuffle(order)
        if not private and k > 1:  # whoever was just named or asked gets to answer first
            order.sort(key=lambda x: x not in self.addressed)
        self.addressed = set()
        size = math.ceil(len(order) / self.waves)
        waves = [order[i:i + size] for i in range(0, len(order), size)]
        self.emit('header', {'text': f'Day {n} · {"private time" if private else "town square"} {k}'})
        for w, wave in enumerate(waves, start=1):
            requests = {}
            for name in wave:
                if private:
                    prompt = (f'Day {n}, private time {k} of {total} — your turn (group {w} of {len(waves)}). '
                              'Whisper to anyone you like (up to three whispers), or no one. Nobody can address the town '
                              'until the town square.')
                else:
                    prompt = (f'Day {n}, town square {k} of {total} — your turn (group {w} of {len(waves)}). '
                              'Say something to the town, or nothing. No whispering now.')
                if not g[name].alive:
                    prompt += ' (You are dead, but you can still ' + ('whisper.)' if private else 'talk.)')
                if not private and k == total:
                    prompt += ' This is the last beat before nominations.'
                requests[name] = Request('beat', prompt, n, beat=k, alive=g[name].alive,
                                         mode='private' if private else 'public')
            acts = await self.ask_many(requests)
            if private:
                for name in wave:
                    for msg in self.whispers(name, acts[name]):
                        self.emit('whisper', {'from': name, **msg}, [name, *msg['to']])
                continue
            for name in wave:
                say = clip(acts[name].get('say'), WORDS['beat'])
                if say:
                    self.emit('say', {'speaker': name, 'text': say})
                    self.addressed |= {x for x in self.names if x != name and re.search(rf'\b{x}\b', say)}
            for name in wave:
                t = acts[name].get('slayer_shot')
                if t in self.names and t != name:
                    await self.slayer(name, t)
                    if g.winner:
                        return

    async def slayer(self, shooter, target):
        g = self.g
        s, t = g[shooter], g[target]
        died = False
        if s.alive and s.character == 'Slayer' and not g.slayer_used:
            g.slayer_used = True
            if not g.is_poisoned(s) and t.alive:
                if t.character == 'Imp':
                    died = True
                elif t.character == 'Recluse' and not g.is_poisoned(t):
                    c = yes_choice(f'Slayer:{t.name}', f'The Slayer ({s.name}) shot the Recluse ({t.name}). Does the '
                                                       'Recluse register as the Demon (and die)? Use yes=true/false.',
                                   POLICY['recluse_slain'])
                    values, _ = await self.decide([c], f'Day {self.day}: a Slayer shot.')
                    died = bool(norm(values[c.id])['yes'])
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
            saint = g.works(p, 'Saint')
            self.kill(p, 'execution')
            g.executed_death = name
            if saint:
                g.winner, g.reason = 'evil', f'{name} was the Saint, and the Saint was executed.'
        g.check_victory()

    async def virgin(self, nominator, nominee):
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
            c = yes_choice(f'Virgin:{nominator}', f'The Spy ({nominator}) nominated the Virgin ({nominee}). Does the '
                                                  'Spy register as a Townsfolk (and get executed)? Use yes=true/false.',
                           POLICY['spy_virgin'])
            values, _ = await self.decide([c], f'Day {self.day}: the Virgin is nominated.')
            townsfolk = bool(norm(values[c.id])['yes'])
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
            if g.works(p, 'Butler') and g.master:
                seen = (f'they voted {"yes" if g.master in yes else "no"}' if g.master in voted
                        else 'they vote after you')
                lines.append(f'Your master is {g.master} ({seen}): your vote only counts if they vote yes.')
            lines.append('Set `vote` to true or false; `say` may hold a very short remark (optional; don\'t just restate your vote).')
            a = await self.ask(voter, Request('vote', ' '.join(lines), n, options=[nominee]))
            v = a.get('vote') is True
            if v and g.works(p, 'Butler') and g.master in voted and g.master not in yes:
                v = False  # the Butler cannot raise their hand when their master has not
                self.emit('notice', {'text': f'(Your master {g.master} did not vote yes, so you cannot vote.)'}, [voter])
            ghost = v and not p.alive
            if ghost:
                p.ghost_vote = False
            self.emit('vote', {'voter': voter, 'nominee': nominee, 'yes': v, 'ghost': ghost,
                               'text': clip(a.get('say'), WORDS['vote'])})
            voted.add(voter)
            if v:
                yes.append(voter)
        butler = g.with_character('Butler')
        if butler and g.works(butler, 'Butler') and butler.name in yes and g.master not in yes:
            # voted before their master, who then did not vote: the Storyteller does not count it (not announced)
            yes.remove(butler.name)
            self.emit('text', {'text': f'({butler.name}, the Butler, voted before their master, who then did not '
                                       'vote yes, so the vote did not count.)'}, 'audit')
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
                      'You may nominate someone (set `nominate`; your `say` is the accusation), or not. If you are '
                      'not nominating, leave `say` empty unless you have something important to add. No whispering now.')
            acts = await self.ask_many({name: Request('nominate', prompt, n, options=options) for name in eligible})
            noms, remarks = [], []
            for name in eligible:
                a = acts[name]
                say = clip(a.get('say'), WORDS['nominate'])
                if a.get('nominate') in options:
                    noms.append((name, a['nominate'], say))
                elif say:
                    remarks.append((name, say))
            self.rng.shuffle(remarks)
            for name, say in remarks:
                self.emit('say', {'speaker': name, 'text': say})
            if not noms:
                break
            nominator, nominee, accusation = self.rng.choice(noms)
            for other, t, _ in noms:
                if other != nominator:
                    self.emit('notice', {'text': f'(Your nomination of {t} was not taken: {nominator} nominated '
                                                 f'{nominee} first. You can nominate again later.)'}, [other])
            nominators.add(nominator)
            nominees.add(nominee)
            self.emit('nomination', {'nominator': nominator, 'nominee': nominee, 'text': accusation})
            if await self.virgin(nominator, nominee):
                return
            d = await self.ask(nominee, Request('defense', f'Day {n}: {nominator} has nominated you. '
                                                           'Give your defense in `say`.', n))
            self.emit('defense', {'nominee': nominee, 'text': clip(d.get('say'), WORDS['defense'])})
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
