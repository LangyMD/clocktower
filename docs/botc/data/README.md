# Machine-readable Blood on the Clocktower data

| File | What it holds |
|---|---|
| [characters.json](characters.json) | All 181 official characters (base scripts, experimental, Travellers, Fabled, Loric). |
| [night-order.json](night-order.json) | Official first-night and other-nights wake order across all characters. |
| [setup-counts.json](setup-counts.json) | Townsfolk/Outsider/Minion/Demon counts by player count. |
| [jinxes.json](jinxes.json) | Official jinx rulings: pairs of characters and the special rule that applies when both are on a script. |
| [scripts/](scripts/) | Scripts in the official script-tool JSON format (the three base scripts so far). |
| `official/` | Not committed. TPI's raw toolmaker files (they include flavour text), downloaded by `python scripts/botc_data.py fetch`. |

## characters.json fields

| Field | Source | Meaning |
|---|---|---|
| `id` | official | Lower-case id used by the official app and script tool (`fortuneteller`, `scarletwoman`). |
| `name` | official | Display name. |
| `team` | official | `townsfolk`, `outsider`, `minion`, `demon`, `traveller`, `fabled` or `loric`. |
| `alignment` | derived | `good`/`evil` for the four core types; `null` for Travellers (set by the Storyteller), Fabled and Loric. |
| `edition` | official | `tb`, `bmr`, `snv`, `carousel` (experimental), `fabled`, `loric`. |
| `ability` | official | The official ability text. This is the rules text: when it and anything else here disagree, it wins. |
| `summary` | **ours** | Plain-language summary of the ability, with the implicit rules spelled out (for example "night*" as "except the first"). |
| `tags` | **ours** | Mechanic tags for grouping and engine dispatch (vocabulary below). |
| `setup` | official | True if the character changes setup. |
| `setup_modifier` | **ours** | Structured setup effect: `outsiders`/`minions`/`demons` (allowed changes, or `"any"`), `adds` (required characters), `note`. |
| `first_night`, `other_nights` | official | Position in `night-order.json`, or `null` if it never wakes then. |
| `first_night_reminder`, `other_night_reminder` | official | The Storyteller's instructions for waking this character (from the official night sheet). `:reminder:` marks where a reminder token is placed. |
| `reminders`, `reminders_global` | official | Reminder token labels used on the Grimoire. |
| `app_special` | official | Special app features (`grimoire`, `pointing`, `bag-disabled`, ...), see TPI's README. |
| `jinxed_with` | official | Ids of characters with a jinx ruling against this one. |
| `wiki` | derived | Official wiki page. |

### Tag vocabulary

- Information: `info-start`, `info-nightly`, `info-day`, `info-once`, `info-on-death`, `info-reward`, `grimoire`
- Action shape: `choose-players`, `day-action`, `once-per-game`, `on-death`, `night-eyes`, `wish`
- Effects: `kill`, `protection`, `droison`, `droison-cure`, `misregistration`, `madness`, `resurrection`,
  `false-death`, `self-risk`, `death-link`, `death-redirect`, `copy-ability`, `character-change`,
  `alignment-change`, `false-identity`, `hidden-ability`, `false-info`, `bluffs`, `evil-info-scramble`,
  `demon-succession`
- Rules changes: `setup-modifier`, `voting-modifier`, `voting-restriction`, `nomination-trigger`,
  `nomination-modifier`, `nomination-restriction`, `execution-modifier`, `social-restriction`
- Outcomes: `win-condition`, `loss-condition`, `game-ending`
- Storyteller-side: `storyteller-error`, `balance`, `social`, `jinx`, `homebrew`

Tags are our judgement and approximate; check the wiki for exact rules.

## Keeping it current

```sh
python scripts/botc_data.py fetch   # download TPI's roles.json, nightsheet.json, jinxes.json into official/
python scripts/botc_data.py build   # refresh official fields; keep our summaries and tags; stub new characters
python scripts/botc_data.py check   # offline consistency check (run by tests/test_botc_data.py)
```

## Copyright

The `ability` text, night reminders and jinx rulings are The Pandemonium Institute's, included because they are
the game's rules text, which game code has to follow exactly. They come from TPI's public toolmaker resources
([botc-release](https://github.com/ThePandemoniumInstitute/botc-release)), published for use in community tools
under TPI's [Community Created Content Policy](https://bloodontheclocktower.com/pages/community-created-content-policy).
Flavour quotes and script descriptions are creative writing rather than rules and are deliberately left out.
Everything else (summaries, tags, setup notes, all prose in `docs/botc/`) is this repo's own.
