# Clocktower

Blood on the Clocktower (Trouble Brewing, nine players by default; `--players 5-15`) played by language models over text,
with a scripted Storyteller and optional human seats. A clean rewrite
of the earlier `botc/` lab (kept alongside for reference).

## How a game works

- **Setup.** A uniformly random legal set of nine characters is dealt at random.
- **Storyteller.** A scripted policy (`state.POLICY`), no LLM. Every Storyteller decision is a
  `Choice` over all its legal values, and the pick comes from a random style weighted like an
  experienced human Storyteller. The style can produce every answer a working ability could give in
  some legal game (tests check this), so no plausible option is ruled out, and it never produces an
  impossible one. The Drunk usually believes they are an information role; bluffs usually include an
  information role (and an Outsider in Baron games) and rarely the Drunk's apparent character;
  impaired players get information from one consistent false world (a framed good player is the
  Demon, the real Demon looks good), answered as a working ability would answer there, though 20% of
  Drunks get true information all game; the Spy usually registers good, as a Demon bluff; the
  Recluse registers evil half the time; the red herring is usually a Townsfolk; an Investigator's
  second player is usually good. It is free, instant and reproducible, and keeps the Storyteller
  from confounding model comparisons. (An LLM Storyteller was tried in v1–v2; it repeated itself and
  undid evil's misinformation.)
- **Night.** The Poisoner, Monk and Imp choose in parallel; then, after the kill, the Fortune
  Teller and Butler (so nobody killed tonight is woken). The engine resolves abilities in the
  official night order.
- **Day = private time, then the town square.** Every day is the same: 3 beats of private time
  (`--private-beats`), then 3 of town square (`--public-beats`), then nominations; nothing ends a part early. In
  each beat every player gets one turn, in a random order, in groups of three (`--waves`); a group acts simultaneously and later groups see
  earlier ones. In private time a turn is up to two whispers, each to one or two players;
  whispers are completely private (nobody else sees the words or that they happened). In the
  town square a turn is public speech (and optionally a Slayer shot), and there is no whispering. Nominations
  open after the last town-square beat.
- **Nominations.** Rounds until one brings no nomination. Each round, every living player who
  hasn't nominated today is asked at once to nominate (with an accusation) or pass; if several
  nominate, one is taken at random. The nominee defends, everyone (the dead too) gets one comment
  turn in the usual groups, then votes go clockwise one at a time, starting from the nominee's
  left, with a running tally. The Slayer can shoot on any public turn (town square, the call for
  nominations, comments). Standard thresholds,
  ties, ghost votes, Butler, Virgin, Slayer, Saint, Mayor and Scarlet Woman rules apply. (A
  Butler who tries to vote after their master voted no is shown as voting no; nothing announces
  the Butler.)

## Models, memory and cost

Every seat is one append-only model conversation. Claude models go through
the Anthropic SDK; `gpt-*` models (e.g. `--model gpt-6-astra`) through the OpenAI Responses API
with encrypted reasoning carried forward (standard tier; `--flex` for half-price Flex, which is throttled under load). Defaults: `claude-opus-5-5`, players at `high`
effort.
- **Equal budget.** Every model gets the same effort level and the same per-turn output ceiling
  (`--max-output`, thinking included, default 8K). A truncated turn is retried once at the same
  ceiling, never given more room. Models still differ in price per token.
- **Memory is the model's own.** Each turn appends only what that seat saw since its last
  turn, plus a one-line prompt. The model's replies, including its thinking blocks, stay in
  the conversation, so it keeps its reasoning (and its bluffs) across the whole game. No
  state dumps or history is re-sent; `tests/` checks this.
- **Caching.** The system prompt is identical for every seat (so it caches across seats). Every
  request reads the whole earlier conversation from cache and writes only the new turn.
- **One fixed JSON schema** for every player decision, so the request prefix never changes.
- **Spend** goes to `games/ledger.jsonl`; `--budget` (default $1000) stops play when it's reached.
- **No queue.** Every game and seat runs at once (`--concurrency 0`); rate limits are retried.
- **Mixed tables.** `--good-model` / `--evil-model` (and `--good-effort` / `--evil-effort`) pick a model per team; seats are created once
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
- `probes.jsonl` — belief probes: at dawn of day 1 and before each day's nominations, each seat is
  asked (on a fork of its conversation that is then thrown away, so play is unaffected) for P(evil),
  P(Demon) and a character guess per player (evil seats predict what the good players believe),
  its claim and a one-line plan. `python -m clocktower analyze games/v5/*/game-*` scores them by
  model pairing, with win rates and voting accuracy. `--no-probes` turns them off.

## Code

| File | What it does |
|---|---|
| `characters.py` | Trouble Brewing characters, ability text, night order |
| `state.py` | Grimoire, registration, deaths and victory, Storyteller choices and policy |
| `game.py` | Setup, nights, beats, nominations, votes |
| `render.py` | What each viewer sees of each event |
| `prompts.py` | Player system prompt, dawn narration |
| `schema.py` | The fixed output schema |
| `llm.py` | Claude and OpenAI conversations, caching, prices, cost ledger |
| `agents.py` | Model, random (tests) and human seats; the scripted Storyteller |
| `web.py` | Local browser UI for a human seat |
| `watch.py`, `viewer/` | Spectator app: library, Grimoire circle, chronicle, playback, live-follow, per-seat views |
| `probe.py` | Belief probes (out-of-game forks of each seat's conversation) |
| `analyze.py` | Win rates, voting and probe scores by model pairing |
| `cli.py` | `run`, `play`, `sim` |
