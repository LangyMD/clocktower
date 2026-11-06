# Custom and homebrew scripts

## Custom scripts

A custom script is any selection of official characters. Since the base box and the online app made all
characters available, custom scripts are the main way experienced groups play.

**Where to find them** (community resources; check each site's terms before using its data):

- [botcscripts.com](https://botcscripts.com/): the largest community script library, with ratings, tags
  (teensyville, beginner, homebrew) and downloadable JSON in the official format.
- The official [script tool](https://script.bloodontheclocktower.com/) for building and exporting scripts and
  printable character sheets.
- [r/BloodOnTheClocktower](https://www.reddit.com/r/BloodOnTheClocktower/) and the official Discord, where scripts
  are shared and discussed.
- Official Teensyville scripts published by TPI for 5 and 6 player games (on the wiki and in the app).

**Common kinds of custom scripts**:

- **Base-script variants**: TB with a few experimental characters swapped in, to refresh a familiar script.
- **Teensyville**: tiny scripts for 5 to 6 players.
- **Themed scripts**: built around one mechanic (heavy drunkenness, alignment changes, madness, a single win
  condition such as the Cult Leader).
- **Mega/"kitchen sink" scripts**: many characters, very hard to solve, played by veteran groups.

Script names and authors are worth recording in `_meta` when a script is added to
[../data/scripts/](../data/scripts/), and the author's licence respected. We have not imported community scripts
into this repo; a future importer should fetch by id from the library and keep attribution.

## Homebrew

Homebrew means characters or rules not made by TPI. Fan-made characters are described as full objects in the
script JSON, using TPI's [script schema](https://github.com/ThePandemoniumInstitute/botc-release/blob/main/script-schema.json):

```json
{
  "id": "example_lamplighter",
  "name": "Lamplighter",
  "team": "townsfolk",
  "ability": "Each night, choose a player: you learn if they woke tonight.",
  "firstNight": 0,
  "otherNight": 40,
  "otherNightReminder": "The Lamplighter points at a player. Nod if they woke tonight.",
  "reminders": ["Checked"]
}
```

(The Lamplighter above is an invented example for illustration.)

Things to know when supporting homebrew in an engine:

- **The ability text is the only definition.** There is no machine-readable rule for a homebrew ability. An
  engine either implements each character by hand or relies on an AI Storyteller that reads the text and decides
  outcomes. This is one of the strongest arguments for an AI Storyteller.
- **Night order**: homebrew characters give a numeric position (`firstNight` / `otherNight`) relative to the
  official ordering, or the script's `_meta` lists the full order explicitly.
- **Bootlegger**: the Loric character that tells players homebrew rules are in use; `_meta.bootlegger` lists them.
- **Jinxes** with official characters can be written by the author in a `jinxes` list on the character.

## Using custom scripts in this repo

The data layer is ready: a script is a list of ids, each id resolves to an entry in
[characters.json](../data/characters.json) with type, night order positions, reminders and setup modifiers. What
the engine still lacks is behaviour for characters beyond Trouble Brewing; see
[../engineering/multi-script-support.md](../engineering/multi-script-support.md).
