# Character types, setup and add-ons

Sources: [Character Types](https://wiki.bloodontheclocktower.com/Character_Types),
[Setup](https://wiki.bloodontheclocktower.com/Setup), [Travellers](https://wiki.bloodontheclocktower.com/Travellers),
[Fabled](https://wiki.bloodontheclocktower.com/Fabled), [Loric](https://wiki.bloodontheclocktower.com/Loric).

## The seven types

| Type | Team | Role in the game | `team` value in data |
|---|---|---|---|
| Townsfolk | good | The good majority; abilities that help good (information, protection, a few kills). | `townsfolk` |
| Outsider | good | Good, but their abilities tend to hurt good or are liabilities. | `outsider` |
| Minion | evil | The Demon's helpers; disrupt good (poison, extra kills, misregistration, alternative win conditions). | `minion` |
| Demon | evil | Usually kills each night. If it dies, good usually wins. | `demon` |
| Traveller | either | Drop-in characters for late arrivals or early leavers; publicly known to be Travellers, alignment secret. | `traveller` |
| Fabled | none | Storyteller-side modifiers for special circumstances (small groups, accessibility, house rules). | `fabled` |
| Loric | none | Newer Storyteller-side modifiers that change the rules of play itself (for example, unknown characters). | `loric` |

## Setup counts

The same table applies to every script ([data](../data/setup-counts.json)):

| Players | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Townsfolk | 3 | 3 | 5 | 5 | 5 | 7 | 7 | 7 | 9 | 9 | 9 |
| Outsiders | 0 | 1 | 0 | 1 | 2 | 0 | 1 | 2 | 0 | 1 | 2 |
| Minions | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 3 |
| Demons | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Beyond 15 players, the extra people play Travellers. Games of 5 or 6 players are sometimes called
**Teensyville** games; TPI recommends small scripts (around six Townsfolk, two Outsiders, two Minions, two
Demons) for them.

## Setup modifiers

Characters whose official ability ends with text in square brackets change setup. In
[characters.json](../data/characters.json) they have `"setup": true`, and our `setup_modifier` field records
the effect in a structured way (`outsiders`: list of allowed changes, `minions`, `demons`, `adds`, `note`).
Rules that apply to all of them:

- Modifiers apply when the Storyteller builds the bag, before dealing.
- When an Outsider count goes up, Townsfolk go down by the same amount (and vice versa); the total never changes.
- Several modifiers can stack (Baron and Fang Gu: +3 Outsiders).
- A character that is in play but **drunk or poisoned at setup** still applies its modifier: setup happens
  before anyone can be poisoned.
- Some characters require another character in play (Huntsman adds the Damsel; Choirboy adds the King).

## Information evil receives

- 7+ players: Minions learn the Demon; the Demon learns its Minions and three not-in-play good characters as
  bluffs.
- 5 to 6 players: no evil info and no bluffs (the Storyteller may still give some under house rules).
- Characters that change this: Poppy Grower (none until it dies), Magician (confuses who is who), Snitch
  (Minions also get three bluffs), Lunatic (a fake Demon gets fake info), Marionette (unknown to itself),
  Summoner and Lil' Monsta (no Demon player at the start).

## Travellers

- Join at any point; the Storyteller chooses their alignment and may tell them it.
- Count for nothing in setup counts or the "two players left" win condition.
- Are **exiled** rather than executed (see [game-flow.md](game-flow.md#4-nominations-voting-and-execution)).
- Each base script has five Travellers designed for it, but any Traveller can be used with any script.
- Experienced groups sometimes play a Traveller deliberately (a "Traveller game") for extra chaos.

## Fabled and Loric

These are not dealt to players. The Storyteller puts them on the table, publicly, to adjust the game:

- **Common Fabled**: Toymaker (gentler Demon for new players), Fibbin and Duchess (small-game info tweaks),
  Doomsayer (accelerates the game), Sentinel (Outsider count uncertainty), Djinn (announces jinxes), Spirit of
  Ivory (caps extra evil players), Angel and Hell's Librarian (behaviour enforcement), Revolutionary, Fiddler,
  Ferryman, Buddhist, Deus ex Fiasco.
- **Loric** are a newer category for heavier rule changes: Bootlegger (lists homebrew rules), Gardener (ST
  chooses characters), Pope (duplicates), Tor (unknown characters), Stormcatcher, Bigwig, God of Ug,
  Hindu, Knaves, Ventriloquist, Zenomancer.

## Jinxes

Two characters on the same script are **jinxed** when they interact badly; TPI publishes a special ruling for
each pair, and the Djinn (Fabled) announces them. Our [jinxes.json](../data/jinxes.json) holds the 131 pairs
with their official rulings. A script builder must check jinxes, and
an AI Storyteller must apply the ruling instead of either character's normal text.
