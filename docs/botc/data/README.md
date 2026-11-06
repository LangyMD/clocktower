# Machine-readable Blood on the Clocktower data

| File | What it holds |
|---|---|
| [characters.json](characters.json) | All 181 official characters (base scripts, experimental, Travellers, Fabled, Loric). |
| [night-order.json](night-order.json) | Official first-night and other-nights wake order across all characters. |
| [setup-counts.json](setup-counts.json) | Townsfolk/Outsider/Minion/Demon counts by player count. |
| [jinxes.json](jinxes.json) | Pairs of characters with an official jinx ruling. |
| [scripts/](scripts/) | Scripts in the official script-tool JSON format (the three base scripts so far). |
| `official/` | Not committed. TPI's toolmaker data, downloaded by `python scripts/botc_data.py fetch`. |

## characters.json fields

| Field | Source | Meaning |
|---|---|---|
| `id` | official | Lower-case id used by the official app and script tool (`fortuneteller`, `scarletwoman`). |
| `name` | official | Display name. |
| `team` | official | `townsfolk`, `outsider`, `minion`, `demon`, `traveller`, `fabled` or `loric`. |
| `alignment` | derived | `good`/`evil` for the four core types; `null` for Travellers (set by the Storyteller), Fabled and Loric. |
| `edition` | official | `tb`, `bmr`, `snv`, `carousel` (experimental), `fabled`, `loric`. |
| `summary` | **ours** | One-sentence summary of the ability in our own words. Not the official text. |
| `tags` | **ours** | Mechanic tags for grouping and engine dispatch (vocabulary below). |
| `setup` | official | True if the character changes setup. |
| `setup_modifier` | **ours** | Structured setup effect: `outsiders`/`minions`/`demons` (allowed changes, or `"any"`), `adds` (required characters), `note`. |
| `first_night`, `other_nights` | official | Position in `night-order.json`, or `null` if it never wakes then. |
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

The official ability text, flavour text and jinx rulings belong to The Pandemonium Institute and are not
committed here: the fetch step downloads them from TPI's public toolmaker resources
([botc-release](https://github.com/ThePandemoniumInstitute/botc-release), subject to TPI's
[Community Created Content Policy](https://bloodontheclocktower.com/pages/community-created-content-policy)).
What is committed is factual structure (names, types, night order, token labels) and our own summaries.
