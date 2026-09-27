"""Grimoire state and Trouble Brewing rules.

The Grimoire holds the truth. Anything the Storyteller gets to decide (information
for impaired players, Spy/Recluse registration, Mayor bounces, setup) is expressed
as a Choice: a description, a legality check, a safe default and a policy. The
policy is the scripted Storyteller: what an experienced human Storyteller would
usually do, with some randomness (see POLICY). The engine never applies an illegal
Storyteller choice.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from itertools import product
import random
from typing import Callable
from .characters import (ALL, DEMONS, GOOD, MINIONS, OUTSIDERS, TOWNSFOLK,
                         is_evil_character, kind)


@dataclass
class Player:
    name: str
    seat: int
    character: str          # true character; changes only when a Minion becomes the Imp
    shown: str              # the character this player believes they are (differs only for the Drunk)
    alive: bool = True
    ghost_vote: bool = True

    @property
    def evil(self):
        return is_evil_character(self.character)


def setup_error(characters):
    """Why a list of 9 characters is not a legal Trouble Brewing setup, or None."""
    if len(characters) != 9: return 'need exactly 9 characters'
    if len(set(characters)) != 9: return 'characters must be distinct'
    bad = [c for c in characters if c not in ALL]
    if bad: return f'not on the script: {bad}'
    counts = {k: sum(1 for c in characters if kind(c) == k) for k in ('Townsfolk', 'Outsider', 'Minion', 'Demon')}
    if counts['Demon'] != 1: return 'need exactly one Imp'
    if counts['Minion'] != 1: return 'need exactly one Minion'
    want = (3, 4) if 'Baron' in characters else (5, 2)
    if (counts['Townsfolk'], counts['Outsider']) != want:
        return f'need {want[0]} Townsfolk and {want[1]} Outsiders' + (' (Baron in play)' if 'Baron' in characters else '')
    return None


def random_setup(rng, minion=None):
    minion = minion or rng.choice(MINIONS)
    tf, os_ = (3, 4) if minion == 'Baron' else (5, 2)
    return rng.sample(TOWNSFOLK, tf) + rng.sample(OUTSIDERS, os_) + [minion, 'Imp']


# How the scripted Storyteller uses its discretion.
POLICY = {
    'poisoned_false': 0.8,    # a poisoned player gets false information (a Drunk always does)
    'spy_evil': 0.25,         # the Spy registers as evil
    'recluse_evil': 0.4,      # the Recluse registers as evil (or as a Minion/Demon)
    'misregister_pair': 0.3,  # a Washerwoman/Librarian/Investigator is shown a misregistering Spy/Recluse
    'mayor_bounce': 0.5,      # an attack on the Mayor kills someone else
    'recluse_slain': 0.2,     # the Slayer's shot kills the Recluse
    'spy_virgin': 0.2,        # the Spy registers as a Townsfolk to the Virgin
}


@dataclass
class Choice:
    """A decision the Storyteller makes. Values are dicts with any of:
    players (list[str]), character (str|None), number (int|None), yes (bool|None)."""
    id: str
    description: str
    legal: Callable[[dict], bool]
    default: dict
    options: Callable[[random.Random], dict]    # the scripted Storyteller's (legal) choice
    auto: bool = False                           # only one legal value: no need to ask


class Grimoire:
    def __init__(self, names, characters, drunk_as=None):
        self.players = [Player(n, i, c, drunk_as if c == 'Drunk' else c) for i, (n, c) in enumerate(zip(names, characters))]
        self.by_name = {p.name: p for p in self.players}
        self.red_herring = None
        self.bluffs = []
        self.poisoned = None        # name of the poisoned player (tonight and tomorrow day)
        self.protected = None       # Monk protection tonight
        self.master = None          # Butler's master for today's votes
        self.slayer_used = False
        self.virgin_used = False
        self.day = 0
        self.executed_death = None  # who died by execution today (Undertaker)
        self.decoys = {}            # impaired player -> the false picture their information follows
        self.winner = None
        self.reason = None

    def __getitem__(self, name):
        return self.by_name[name]

    # ---- basic queries -------------------------------------------------------------
    def living(self):
        return [p for p in self.players if p.alive]

    def alive_count(self):
        return len(self.living())

    def with_character(self, character, alive=True):
        return next((p for p in self.players if p.character == character and (p.alive or not alive)), None)

    def demon(self):
        return self.with_character('Imp')

    def is_poisoned(self, p):
        return self.poisoned == p.name

    def impaired(self, p):
        """The player's own ability (as they understand it) is not working."""
        return p.character == 'Drunk' or self.is_poisoned(p)

    def works(self, p, character):
        """p is alive, really is `character`, and is not poisoned."""
        return p.alive and p.character == character and not self.is_poisoned(p)

    def neighbours(self, p):
        """Nearest living players clockwise and anticlockwise (excluding p)."""
        n = len(self.players)
        out = []
        for step in (-1, 1):
            i = p.seat
            for _ in range(n - 1):
                i = (i + step) % n
                q = self.players[i]
                if q.alive and q is not p:
                    out.append(q)
                    break
        if len(out) == 2 and out[0] is out[1]:
            out = out[:1]
        return out

    # ---- registration --------------------------------------------------------------
    def registers_evil(self, p):
        """Set of possible answers to 'is p evil?'"""
        if p.character in ('Spy', 'Recluse') and not self.is_poisoned(p):
            return {True, False}
        return {p.evil}

    def registers_as(self, p):
        """Set of characters p might register as."""
        if p.character == 'Spy' and not self.is_poisoned(p):
            return {'Spy', *TOWNSFOLK, *OUTSIDERS}
        if p.character == 'Recluse' and not self.is_poisoned(p):
            return {'Recluse', *MINIONS, *DEMONS}
        return {p.character}

    def registers_demon_to_ft(self, p):
        if p.character == 'Imp' or p.name == self.red_herring:
            return {True}
        if p.character == 'Recluse' and not self.is_poisoned(p):
            return {True, False}
        return {False}

    def decoy(self, p, r):
        """The false picture that an impaired player's information follows, fixed per player so it
        stays consistent from night to night: a framed good player plays the Demon, one other
        non-Demon player the Minion, and the real Demon looks good."""
        if p.name not in self.decoys:
            others = [q for q in self.players if q is not p]
            framed = r.choice([q for q in others if not q.evil])
            partner = r.choice([q for q in others if q is not framed and q.character != 'Imp'])
            self.decoys[p.name] = (framed.name, {framed.name, partner.name})
        return self.decoys[p.name]

    def misinformed(self, p, r):
        """Whether the scripted Storyteller gives this impaired player false information now."""
        return p.character == 'Drunk' or (self.is_poisoned(p) and r.random() < POLICY['poisoned_false'])

    def sample_evil(self, r):
        """Who registers as evil this time, under the scripted Storyteller's registration policy."""
        out = set()
        for q in self.players:
            chance = {'Spy': POLICY['spy_evil'], 'Recluse': POLICY['recluse_evil']}.get(q.character)
            if chance is not None and not self.is_poisoned(q):
                if r.random() < chance:
                    out.add(q.name)
            elif q.evil:
                out.add(q.name)
        return out

    def fake_good(self, r, kinds=(TOWNSFOLK,)):
        """A good character not in play for an evil player to register as: a Demon bluff if possible."""
        pool = [c for k in kinds for c in k if c not in self.in_play()]
        return r.choice([c for c in self.bluffs if c in pool] or pool)

    def in_play(self):
        return {q.character for q in self.players} | {q.shown for q in self.players}

    # ---- deaths and victory ----------------------------------------------------------
    def die(self, p):
        p.alive = False
        if p.character == 'Poisoner':
            self.poisoned = None

    def scarlet_woman_heir(self, alive_before):
        sw = self.with_character('Scarlet Woman')
        if sw and self.works(sw, 'Scarlet Woman') and alive_before >= 5:
            return sw
        return None

    def check_victory(self):
        if self.winner: return self.winner
        if not self.demon():
            self.winner, self.reason = 'good', 'The Demon is dead.'
        elif self.alive_count() <= 2:
            self.winner, self.reason = 'evil', 'Only two players remain alive.'
        return self.winner

    # ---- views ---------------------------------------------------------------------
    def grimoire_text(self, reminders=()):
        lines = []
        for p in self.players:
            tags = []
            if p.character == 'Drunk': tags.append(f'thinks they are the {p.shown}')
            if not p.alive: tags.append('DEAD' + ('' if p.ghost_vote else ', ghost vote used'))
            if self.is_poisoned(p): tags.append('POISONED')
            if p.name == self.protected: tags.append('protected by the Monk tonight')
            if p.name == self.red_herring: tags.append("Fortune Teller's red herring")
            if p.name == self.master: tags.append("Butler's master")
            team = 'evil' if p.evil else 'good'
            lines.append(f'{p.seat + 1}. {p.name}: {p.character} ({team})' + (f" [{'; '.join(tags)}]" if tags else ''))
        if self.bluffs: lines.append(f"Demon bluffs: {', '.join(self.bluffs)}")
        used = [x for x, flag in (('Slayer', self.slayer_used), ('Virgin', self.virgin_used)) if flag]
        if used: lines.append(f"Spent once-per-game abilities: {', '.join(used)}")
        lines += list(reminders)
        return '\n'.join(lines)


# ---- information choices -----------------------------------------------------------
# A value is normalised to {'players': [...], 'character': str|None, 'number': int|None, 'yes': bool|None}.

def norm(value):
    value = value or {}
    return {'players': list(value.get('players') or []), 'character': value.get('character'),
            'number': value.get('number'), 'yes': value.get('yes')}


def _status(g, p):
    if p.character == 'Drunk': return 'DRUNK (their ability does not work; any information is allowed)'
    if g.is_poisoned(p): return 'POISONED (their ability does not work; any information is allowed)'
    return 'sober and healthy (information must be true, within registration)'


def _pair(r, first, others):
    pair = [first, r.choice([x for x in others if x != first])]
    r.shuffle(pair)
    return pair


def pair_choice(g, p, ability, rng):
    """Washerwoman / Librarian / Investigator starting information."""
    group = {'Washerwoman': TOWNSFOLK, 'Librarian': OUTSIDERS, 'Investigator': MINIONS}[ability]
    others = [q.name for q in g.players if q is not p]
    impaired = g.impaired(p)

    def legal(v):
        v = norm(v)
        if ability == 'Librarian' and not v['players'] and v['character'] is None:
            # "zero Outsiders": legal if impaired, or if nobody must register as an Outsider
            return impaired or not any(g.registers_as(q) <= set(OUTSIDERS) for q in g.players)
        a = v['players']
        if len(a) != 2 or len(set(a)) != 2 or not set(a) <= set(others) or v['character'] not in group:
            return False
        return impaired or any(v['character'] in g.registers_as(g[x]) for x in a)

    def options(r):
        if impaired and g.misinformed(p, r):
            framed, _ = g.decoy(p, r)
            evil = [q.name for q in g.players if q.evil and q is not p]
            if ability == 'Washerwoman':  # vouch for an evil player, as one of the Demon's bluffs if possible
                return {'players': _pair(r, r.choice(evil), others), 'character': g.fake_good(r)}
            if ability == 'Librarian':
                return {'players': _pair(r, r.choice(evil + [framed]), others),
                        'character': g.fake_good(r, (OUTSIDERS,)) if set(OUTSIDERS) - g.in_play() else r.choice(OUTSIDERS)}
            return {'players': _pair(r, framed, others), 'character': r.choice(MINIONS)}  # frame a good player
        real = [(q.name, q.character) for q in g.players if q is not p and q.character in group]
        mis = [(q.name, c) for q in g.players if q is not p and q.character in ('Spy', 'Recluse') and q.character not in group
               for c in sorted(g.registers_as(q) & set(group))]
        pool = mis if mis and (not real or r.random() < POLICY['misregister_pair']) else real
        if not pool:
            return {'players': [], 'character': None}
        n, c = r.choice(pool)
        return {'players': _pair(r, n, others), 'character': c}

    default = options(rng)
    label = {'Washerwoman': 'Townsfolk', 'Librarian': 'Outsider', 'Investigator': 'Minion'}[ability]
    actual = sorted(f'{q.name} ({q.character})' for q in g.players if q is not p and q.character in group)
    optional = sorted(q.name for q in g.players if q is not p and q.character in ('Spy', 'Recluse')
                      and g.registers_as(q) & set(group) and q.character not in group)
    desc = (f"{ability} {p.name} is {_status(g, p)}. Show two players (not {p.name}) and a {label} "
            f"character such that one of them registers as that character.")
    if actual: desc += f" In play: {', '.join(actual)}."
    if optional: desc += f" May also misregister: {', '.join(optional)}."
    if ability == 'Librarian':
        desc += ' Use players=[] and character=null for "zero Outsiders in play".'
    desc += ' Use players=[a, b] and character=<name>.'
    return Choice(f'{ability}:{p.name}', desc, legal, default, options)


def _number_choice(cid, desc, possible, impaired, domain, policy, rng):
    legal = (lambda v: norm(v)['number'] in domain) if impaired else (lambda v: norm(v)['number'] in possible)
    return Choice(cid, desc, legal, policy(rng), policy, auto=(not impaired and len(possible) == 1))


def _pairs(ring, evil):
    return sum(1 for i in range(len(ring)) if ring[i].name in evil and ring[(i + 1) % len(ring)].name in evil)


def chef_choice(g, p, rng):
    ring = g.players
    values = set()
    for combo in product(*[sorted(g.registers_evil(q)) for q in ring]):
        values.add(sum(1 for i in range(len(ring)) if combo[i] and combo[(i + 1) % len(ring)]))
    truth = sum(1 for i in range(len(ring)) if ring[i].evil and ring[(i + 1) % len(ring)].evil)
    desc = (f"Chef {p.name} is {_status(g, p)}. Actual pairs of adjacent evil players: {truth}."
            + (f" With Spy/Recluse registration the sober answer may be any of {sorted(values)}." if len(values) > 1 else ''))

    def policy(r):
        if g.impaired(p) and g.misinformed(p, r):
            return {'number': _pairs(ring, g.decoy(p, r)[1])}
        return {'number': _pairs(ring, g.sample_evil(r))}
    return _number_choice(f'Chef:{p.name}', desc, values, g.impaired(p), set(range(0, 5)), policy, rng)


def empath_choice(g, p, rng):
    nb = g.neighbours(p)
    values = {sum(c) for c in product(*[sorted(g.registers_evil(q)) for q in nb])}
    truth = sum(1 for q in nb if q.evil)
    desc = (f"Empath {p.name} is {_status(g, p)}. Living neighbours: "
            f"{', '.join(f'{q.name} ({q.character})' for q in nb)}; actually evil: {truth}."
            + (f" With registration the sober answer may be any of {sorted(values)}." if len(values) > 1 else ''))

    def policy(r):
        evil = g.decoy(p, r)[1] if g.impaired(p) and g.misinformed(p, r) else g.sample_evil(r)
        return {'number': sum(1 for q in nb if q.name in evil)}
    return _number_choice(f'Empath:{p.name}', desc, values, g.impaired(p), {0, 1, 2}, policy, rng)


def fortune_teller_choice(g, p, targets, rng):
    ts = [g[t] for t in targets]
    values = {any(c) for c in product(*[sorted(g.registers_demon_to_ft(q)) for q in ts])}
    impaired = g.impaired(p)
    desc = (f"Fortune Teller {p.name} is {_status(g, p)}. Chose {targets[0]} ({ts[0].character}) and "
            f"{targets[1]} ({ts[1].character}); red herring is {g.red_herring}. "
            f"Sober answer: {'YES' if values == {True} else 'NO' if values == {False} else 'YES or NO (Recluse)'}. Use yes=true/false.")
    legal = (lambda v: isinstance(norm(v)['yes'], bool)) if impaired else (lambda v: norm(v)['yes'] in values)

    def policy(r):
        if impaired and g.misinformed(p, r):  # both decoy evils read as the Demon, so the Drunk still sees YESes
            _, evil = g.decoy(p, r)
            return {'yes': any(t in evil or t == g.red_herring for t in targets)}
        if len(values) == 1:
            return {'yes': next(iter(values))}
        return {'yes': r.random() < POLICY['recluse_evil']}
    return Choice(f'Fortune Teller:{p.name}', desc, legal, policy(rng), policy, auto=(not impaired and len(values) == 1))


def character_choice(g, p, ability, target, rng):
    """Undertaker (executed player) and Ravenkeeper (chosen player)."""
    t = g[target]
    possible = g.registers_as(t)
    impaired = g.impaired(p)
    desc = (f"{ability} {p.name} is {_status(g, p)}. Learns the character of {t.name}, who is the {t.character}."
            + (f" {t.name} may misregister as any of: {', '.join(sorted(possible - {t.character}))}." if len(possible) > 1 else '')
            + ' Use character=<name>.')
    legal = (lambda v: norm(v)['character'] in ALL) if impaired else (lambda v: norm(v)['character'] in possible)

    def policy(r):
        if impaired and g.misinformed(p, r):
            framed, evil = g.decoy(p, r)
            if t.evil:
                return {'character': g.fake_good(r, (TOWNSFOLK, OUTSIDERS))}
            if t.name in evil:
                return {'character': 'Imp' if t.name == framed else r.choice(MINIONS)}
            return {'character': t.shown}
        if len(possible) == 1:
            return {'character': t.character}
        if t.character == 'Spy' and r.random() > POLICY['spy_evil']:
            return {'character': g.fake_good(r, (TOWNSFOLK, OUTSIDERS))}
        if t.character == 'Recluse' and r.random() < POLICY['recluse_evil']:
            return {'character': r.choice(MINIONS)}
        return {'character': t.character}
    return Choice(f'{ability}:{p.name}', desc, legal, {'character': t.character}, policy,
                  auto=(not impaired and len(possible) == 1))


def yes_choice(cid, desc, chance=0.5, default=False):
    return Choice(cid, desc, lambda v: isinstance(norm(v)['yes'], bool), {'yes': default},
                  lambda r: {'yes': r.random() < chance})


def mayor_choice(g, mayor, imp):
    victims = [q.name for q in g.living() if q is not imp and not (g.works(q, 'Soldier')) and q.name != g.protected]
    desc = (f"The Imp attacked the Mayor ({mayor.name}), who is healthy. Choose who dies: the Mayor, or another "
            f"player instead. Options: {', '.join(victims)}. Use players=[<name>].")
    legal = lambda v: len(norm(v)['players']) == 1 and norm(v)['players'][0] in victims
    others = [n for n in victims if n != mayor.name]

    def policy(r):
        return {'players': [r.choice(others) if others and r.random() < POLICY['mayor_bounce'] else mayor.name]}
    return Choice(f'Mayor:{mayor.name}', desc, legal, {'players': [mayor.name]}, policy)


def info_text(ability, value, target=None):
    """What the recipient is told."""
    v = norm(value)
    if ability in ('Washerwoman', 'Librarian', 'Investigator'):
        if not v['players']:
            return 'You learn that there are zero Outsiders in play.'
        a, b = v['players']
        return f'You learn that either {a} or {b} is the {v["character"]}.'
    if ability == 'Chef':
        return f'You learn that there {"is" if v["number"] == 1 else "are"} {v["number"]} pair{"" if v["number"] == 1 else "s"} of evil players sitting next to each other.'
    if ability == 'Empath':
        return f'You learn that {v["number"]} of your living neighbours {"is" if v["number"] == 1 else "are"} evil.'
    if ability == 'Fortune Teller':
        return f'You chose {target[0]} and {target[1]}: {"YES, one of them is the Demon." if v["yes"] else "NO, neither is the Demon."}'
    if ability == 'Undertaker':
        return f'You learn that the player executed today ({target}) was the {v["character"]}.'
    if ability == 'Ravenkeeper':
        return f'You learn that {target} is the {v["character"]}.'
    raise KeyError(ability)
