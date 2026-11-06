# Supporting more scripts: gap analysis

What the codebase hard-codes today, and what the data in [../data/](../data/) makes possible. A starting point
for planning, not a finished design.

## Where Trouble Brewing is hard-coded

- `clocktower/characters.py`: character lists, ability text, setup table, night order, all TB-only.
- `clocktower/state.py`: Grimoire fields specific to TB (`poisoned`, `protected`, `master`, `slayer_used`,
  `virgin_used`, `red_herring`), and per-character choice functions (`chef_choice`, `empath_choice`,
  `fortune_teller_choice`, `mayor_choice`, ...).
- `clocktower/game.py`: night actions keyed on character names (`'Poisoner'`, `'Monk'`, `'Imp'`), the Virgin,
  Slayer and Butler in the day flow, and the Imp's starpass.
- `clocktower/prompts.py` and `docs/player-prompt.md`: player instructions written for TB.
- `docs/PROTOCOL.md`: the frozen benchmark protocol (v17). Any change to how games play is a protocol bump; new
  scripts should be a new mode rather than a change to the benchmark's TB games.

## What the data layer provides

- [characters.json](../data/characters.json): every official character with type, alignment, edition, our
  summary, tags, setup flag and structured setup modifier, night order positions, reminder tokens, app special
  features and jinxed partners.
- [night-order.json](../data/night-order.json): the official first-night and other-nights orders across all
  characters; the order for a script is this list filtered to the script's characters.
- [setup-counts.json](../data/setup-counts.json): the shared type-count table.
- [scripts/](../data/scripts/): scripts in the official JSON format.
- [jinxes.json](../data/jinxes.json): jinxed pairs.

## Suggested direction

1. **Load the script from data.** Replace `characters.py` constants with a loader that reads a script JSON and
   the character data, keeping TB as the default so the benchmark is unchanged.
2. **Grimoire generalisation.** Replace per-character fields with a generic reminder system (token name, the
   player it sits on, the source character, expiry), which is how the physical Grimoire works and what
   `reminders` in the data describes.
3. **Ability registry.** One handler per character, keyed by id, with hooks for setup, first night, other
   nights, day actions, nomination, vote, execution, death, and registration. Tags in the data (for example
   `droison`, `protection`, `misregistration`) group handlers that share mechanics.
4. **Implement a script at a time**: BMR (deaths, protection, drunkenness) then S&V (madness, character
   change). Each new mechanic (madness, character change, alignment change) needs engine support beyond its
   first character.
5. **AI Storyteller as the generic fallback.** Characters without a hand-written handler, including homebrew,
   could be adjudicated by an AI Storyteller reading the ability text (see
   [../storytelling/ai-storyteller.md](../storytelling/ai-storyteller.md)); hand-written handlers remain the
   source of truth where they exist.
6. **Tests per character**, in the style of `tests/test_rules.py`, plus `python scripts/botc_data.py check` to
   keep the data consistent.
