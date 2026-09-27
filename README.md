# Clocktower

Blood on the Clocktower (Trouble Brewing, nine players) played by language models over text,
with a scripted Storyteller (or optionally an LLM one) and optional human seats. A clean rewrite
of the earlier `botc/` lab (kept alongside for reference).

## How a game works

- **Setup.** A uniformly random legal set of nine characters is dealt at random (`--setup
  storyteller` lets an LLM Storyteller choose instead).
- **Storyteller.** By default a scripted policy (`state.POLICY`, `game.pick_bluffs`) that does
  what experienced human Storytellers do, with randomness: the Drunk believes they are an
  information role more often than not; bluffs include an information role to fake (and an
  Outsider in Baron games, occasionally the Drunk's apparent role); drunk and poisoned players
  get information from one consistent false picture per player (a framed good player plays the
  Demon, the real Demon looks clean, a drunk Washerwoman vouches for an evil player as one of
  the Demon's bluffs); the Spy usually registers good and the Recluse sometimes evil. It is
  free, instant and reproducible, and keeps the Storyteller from confounding model comparisons.
  `--storyteller model` uses an LLM Storyteller instead (it tended to repeat itself and to undo
  evil's misinformation).
- **Night.** Players with night abilities choose in parallel. The engine resolves them in the
  official night order.
- **Day = private time, then the town square.** Private time is 3 beats (`--private-beats`;
  `--later-private-beats` can shorten it after day 1); the town square is 3 (`--public-beats`). In
  each beat every player gets one turn, in a random order, in groups of three (`--waves`); a group acts simultaneously and later groups see
  earlier ones. In private time a turn is up to three whispers, each to one or two players;
  whispers are completely private (nobody else sees the words or that they happened). In the
  town square a turn is public speech (or a Slayer shot), there is no whispering, and players
  named in one beat go first in the next so they can answer. Nominations
  open after the last beat, when most living players ask for them, or when a beat is silent.
- **Nominations.** Each round, living players who haven't nominated may nominate (with an
  accusation) or pass. One nomination is taken, the nominee defends, then votes go clockwise
  one at a time, starting from the nominee's left, with a running tally. Standard thresholds,
  ties, ghost votes, Butler, Virgin, Slayer, Saint, Mayor and Scarlet Woman rules apply. (A
  Butler who tries to vote after their master voted no is shown as voting no; nothing announces
  the Butler.)

## Models, memory and cost

Every seat (and an LLM Storyteller, if used) is one append-only model conversation. Claude models go through
the Anthropic SDK; `gpt-*` models (e.g. `--model gpt-6-astra`) through the OpenAI Responses API
with encrypted reasoning carried forward (Flex tier). Defaults: `claude-opus-5-5`, players at `high`
effort.
- **Equal budget.** Every model gets the same effort level and the same per-turn output ceiling
  (`--max-output`, thinking included, default 16K). A truncated turn is retried once at the same
  ceiling, never given more room. Models still differ in price per token.
- **Memory is the model's own.** Each turn appends only what that seat saw since its last
  turn, plus a one-line prompt. The model's replies, including its thinking blocks, stay in
  the conversation, so it keeps its reasoning (and its bluffs) across the whole game. No
  state dumps or history is re-sent; `tests/` checks this.
- **Caching.** The system prompt is identical for every seat (so it caches across seats). Every
  request reads the whole earlier conversation from cache and writes only the new turn.
- **One fixed JSON schema** per role (players / Storyteller), so the request prefix never changes.
- **Spend** goes to `games/ledger.jsonl`; `--budget` (default $300) stops play when it's reached.
- **Mixed tables.** `--good-model` / `--evil-model` pick a model per team; seats are created once
  characters are dealt, and each game's `result.json` records the model at every seat.

## Running

```sh
python3 -m venv .venv && .venv/bin/pip install anthropic
export ANTHROPIC_API_KEY=...            # the default workspace id is in cli.py (--workspace)
.venv/bin/python -m clocktower run                  # a full AI game
.venv/bin/python -m clocktower run --days 1         # stop after day 1
.venv/bin/python -m clocktower play --seat Casey    # play Casey at http://127.0.0.1:8765
.venv/bin/python -m clocktower run --games 6 --parallel 3 --effort high   # a batch
.venv/bin/python -m clocktower run --evil-model claude-opus-5 --good-model claude-opus-5-5  # mixed teams
.venv/bin/python -m clocktower sim --games 100      # random players, no API calls
.venv/bin/python -m clocktower report games/batch-001/*               # outcomes, cost, speech, thinking
.venv/bin/python -m clocktower watch                                   # spectator app, http://127.0.0.1:8800
.venv/bin/python -m clocktower site                                    # the same app as static files (site/), published as an Artifact
.venv/bin/python -m clocktower replay games/X --view public           # what the town saw
.venv/bin/python -m clocktower replay games/X --view Casey --thinking # one seat, with its reasoning
.venv/bin/python -m unittest discover -s tests
```

Each game writes to `games/<time>-<seed>/`:
- `transcript.md` — omniscient replay, including Storyteller choices and each seat's thinking
  summaries (`> 💭`)
- `events.jsonl` — every event with its visibility
- `calls.jsonl` — every API call: seat, decision, latency, tokens, cost, thinking summary, output
- `conversations/` — each seat's full conversation
- `result.json` — winner, cost, token totals

## Code

| File | What it does |
|---|---|
| `characters.py` | Trouble Brewing characters, ability text, night order |
| `state.py` | Grimoire, registration, deaths and victory, legal Storyteller choices |
| `game.py` | Setup, nights, beats, nominations, votes |
| `render.py` | What each viewer sees of each event |
| `prompts.py` | Player and Storyteller system prompts |
| `schema.py` | The two fixed output schemas |
| `llm.py` | Claude and OpenAI conversations, caching, prices, cost ledger |
| `agents.py` | Model, random (tests) and human seats |
| `web.py` | Local browser UI for a human seat |
| `watch.py`, `viewer/` | Spectator app: library, Grimoire circle, chronicle, playback, live-follow, per-seat views |
| `cli.py` | `run`, `play`, `sim` |
