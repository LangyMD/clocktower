# Scripts

A **script** is the list of characters that may be in play in a game: typically 13 Townsfolk, 4 Outsiders,
4 Minions and 1 to 4 Demons, plus optional Travellers and Fabled/Loric. Players see the whole script; they
know what *could* be in play, never what *is*. Everything in a game (what to bluff, which worlds to consider,
what a death means) depends on the script.

## The base scripts (official, in the box)

| Script | Difficulty | Central idea | Page | Data |
|---|---|---|---|---|
| Trouble Brewing (TB) | Beginner | Clear information vs. poison and lies; one Demon (Imp) | [trouble-brewing.md](trouble-brewing.md) | [json](../data/scripts/trouble-brewing.json) |
| Bad Moon Rising (BMR) | Intermediate | Death and protection; which Demon is it? | [bad-moon-rising.md](bad-moon-rising.md) | [json](../data/scripts/bad-moon-rising.json) |
| Sects & Violets (S&V) | Advanced | Misinformation, madness and character changes | [sects-and-violets.md](sects-and-violets.md) | [json](../data/scripts/sects-and-violets.json) |

Each base script has 5 Travellers designed for it. The community's usual learning path is TB, then BMR, then S&V,
then custom scripts.

## Everything else

- **Experimental characters** ([experimental-characters.md](experimental-characters.md)): official characters
  released after the base three. They appear only on custom scripts.
- **Travellers, Fabled and Loric** ([travellers-fabled-loric.md](travellers-fabled-loric.md)).
- **Custom scripts**: any selection of official characters, built with the official script tool. Thousands are
  shared online. See [custom-and-homebrew.md](custom-and-homebrew.md).
- **Homebrew**: scripts that include characters or rules not made by TPI. See
  [custom-and-homebrew.md](custom-and-homebrew.md).
- **Teensyville**: scripts designed for 5 or 6 players (about 6 Townsfolk, 2 Outsiders, 2 Minions, 2 Demons).
- **Script design**: how scripts are balanced, in [script-design.md](script-design.md).

## Script file format

The official app and the [script tool](https://script.bloodontheclocktower.com/) use a JSON array: an optional
`_meta` object, then character ids (strings) or full character objects for homebrew characters. Example:

```json
[
  {"id": "_meta", "name": "Trouble Brewing", "author": "The Pandemonium Institute"},
  "washerwoman", "librarian", "investigator", "chef", "empath"
]
```

`_meta` may also hold `logo`, `background`, `almanac`, `bootlegger` (house rules) and custom `firstNight` /
`otherNight` orders. The schema is published by TPI
([script-schema.json](https://github.com/ThePandemoniumInstitute/botc-release/blob/main/script-schema.json)).
This repo's script files in [../data/scripts/](../data/scripts/) use exactly this format, so any script exported
from the script tool or downloaded from a script library can be dropped in.
