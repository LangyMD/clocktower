# Blood on the Clocktower knowledge base

Reference material about the game itself, collected to help turn this benchmark (which plays only Trouble
Brewing with a scripted Storyteller) into a fuller game with multiple scripts and an AI Storyteller. Everything
is summarised in our own words; [sources.md](sources.md) lists where it comes from.

> Blood on the Clocktower is a trademark of The Pandemonium Institute. This is unofficial fan material.

## Map

| Folder | For | Start with |
|---|---|---|
| [rules/](rules/) | How the game works | [overview.md](rules/overview.md), [game-flow.md](rules/game-flow.md), [character-types-and-setup.md](rules/character-types-and-setup.md), [glossary.md](rules/glossary.md), [rulings.md](rules/rulings.md) |
| [scripts/](scripts/) | The base scripts, experimental characters, custom and homebrew scripts, script design; per-role advice | [README.md](scripts/README.md) |
| [storytelling/](storytelling/) | Running a game: principles, procedure, misinformation, and the AI Storyteller design | [principles.md](storytelling/principles.md), [ai-storyteller.md](storytelling/ai-storyteller.md) |
| [players/](players/) | Strategy for good and evil | [good-team.md](players/good-team.md), [evil-team.md](players/evil-team.md) |
| [data/](data/) | Machine-readable characters, night order, setup counts, jinxes, scripts | [README.md](data/README.md) |
| [engineering/](engineering/) | How this repo's code would need to change for more scripts | [multi-script-support.md](engineering/multi-script-support.md) |

## How the pieces fit the two goals

- **More scripts**: the [data](data/) gives every official character's type, night order, setup effect and
  jinxes in a form code can load; scripts use the official JSON format. The gap analysis in
  [engineering/multi-script-support.md](engineering/multi-script-support.md) lists what the engine
  hard-codes today.
- **AI Storyteller**: [storytelling/](storytelling/) captures what good Storytellers do and why, and
  [ai-storyteller.md](storytelling/ai-storyteller.md) maps every Storyteller decision onto the existing
  `Choice` seam in `clocktower/state.py`. Per-role "Storytelling" notes in the script pages are meant to be
  fed to the model when that character is involved.

## Maintenance

`python scripts/botc_data.py fetch && python scripts/botc_data.py build` refreshes the data from TPI's
toolmaker resources; `python scripts/botc_data.py check` (also a unit test) keeps it consistent.
