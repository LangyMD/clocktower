# Clocktower — notes for Claude sessions

An eval where language models play Blood on the Clocktower (Trouble Brewing, 9 players by default; `--players` 5–15). It measures
holding coherent state and bluffs over a whole game. See README.md for the design.

## Running
- Setup: `pip install -e .` (Python ≥3.11). Tests: `python -m unittest discover -s tests`. No-API
  simulation: `python -m clocktower sim --games 200`.
- Keys come from the environment: `ANTHROPIC_API_KEY` (Claude Code on the web withholds that name, so
  the user stores it as `MY_ANTHROPIC_API_KEY`; `make_client` reads either), `OPENAI_API_KEY` (for `gpt-*` models). The
  Anthropic key is not workspace-scoped, so every request sends `anthropic-workspace-id`
  (`ANTHROPIC_WORKSPACE_ID`, default in `cli.py`). Without it the API returns a 400.
- A batch: `python -m clocktower run --games 10 --seed N --out games/v7/NAME` (`--swap` adds each seed with sides swapped) (games go
  under the current protocol version, `PROTOCOL` in `cli.py`; see `games/PROTOCOLS.md`). All games and seats run
  in parallel with no request cap (`--concurrency 0`; rate limits are retried); game k uses seed N+k-1 and rotates the Minion.
  Per-team models and efforts: `--good-model/--evil-model`, `--good-effort/--evil-effort`. Rough cost
  per game (v5): Opus 5.5 ~$4, Sonnet 5 ~$4, GPT-6 Astra ~$8–10 (standard tier; `--flex` is throttled).
  A batch takes as long as its slowest game (Claude ~15 min, Astra ~45 min). Spend is logged in `games/ledger.jsonl` with a cap (`--budget`, default $1000; the
  user has said the budget can grow).
- After a batch: `python -m clocktower report games/v7/NAME/*` and `python -m clocktower analyze games/v7/*/game-*`, commit the whole batch directory
  (transcripts, events, conversations, calls) and push, so results survive the session. Then
  republish the viewer: `python -m clocktower site` builds `site/`; publish `site/index.html` with the
  Artifact tool, `url: https://claude.ai/artifact/DpA1C6WTJATLvTqTi4XQiH`, and every other file under
  `site/` in `files` (same relative paths). That keeps the one viewer link the user has.
- When a change affects how games play, bump `PROTOCOL` and add a section to `games/PROTOCOLS.md`.

## Design decisions the user made (don't undo without asking)
- Memory is the model's own carried-over reasoning; no notebook, no state re-sent.
- Each day: private time (3 beats, whispers only, invisible to others, up to 2 whispers per turn from v7; v5–v6 had 3)
  then the town square (3 beats, public only), then nominations. Same every day, fixed length: no
  early ends, no call-for-nominations. Dead players talk and whisper; only the living nominate.
- The Storyteller is scripted (`state.POLICY`); the LLM Storyteller was removed. Every decision is a
  `Choice` over all legal values, picked by a random style whose weights are all in POLICY (judgment
  calls). No random floor (removed in v7): instead the style must be able to produce every answer a
  working ability could give in some legal game, and never an impossible one (tests check both).
- Keep the protocol clean: no arbitrary special cases; every rule should be explainable in a line.
- Nominations: each round everyone eligible is asked at once; one nomination is taken; accusation,
  defense, one comment turn for everyone, then the clockwise vote. Slayer shots on any public turn.
- Equal budget across models: same effort and per-turn output ceiling (8K tokens, thinking included).
- Every game in an experiment gets its own seed (more distinct transcripts for later review); the one
  exception worth making is a side-swapped pair sharing a seed (see the roadmap).
- Minimise wall-clock time: run every game of an experiment at once, no request queues.
- Rating: a good (detection) Elo and an evil (deception) Elo per model, from homogeneous-team
  matchups (one model plays evil, another good), Bradley–Terry fit.

## Experiment roadmap (brainstormed with the user, Sept 27; not yet run unless noted)
- **Headline chart:** detection Elo and deception Elo against model release date, one point per
  model, coloured by lab: is deception improving faster or slower than detection? Hold fixed "each
  model at its best (max effort) under the same per-turn ceiling", print cost beside each point.
  (Alternatives considered: equal dollars per game, which mixes in pricing; equal thinking tokens.)
- **Rating design:** one Bradley–Terry fit with a detection and a deception rating per model plus a
  shared good-side advantage, so both are in the same units; anchor a reference model at 1500. Play
  side-swapped pairs (A good vs B evil and B good vs A evil on one seed) so side advantage and setup
  luck cancel. Several anchor opponents across the skill range, since strong good teams win 90–100%
  against weak evil ones (ceiling). 10 games a cell gives about ±25 points of win rate (±150 Elo),
  so lean on the belief probes too.
- **Generation sweeps:** GPT-5 → 5.1 → 5.2 → 5.5 → 5.6 → 6 (Astra, Sol); Claude Fable 5, 5.1, Opus 5,
  5.5, Sonnet. Mirror matches are confounded (both sides improve), so rate against anchors instead.
  Older models need engine work (thinking budgets instead of effort; check they are still served).
- **Other charts:** a CursorBench-style cost frontier (Elo against cost per seat-game, one line per
  model through its effort levels; the user decided efficiency is secondary); a skill map (good Elo
  against evil Elo); probe-based detection (probability good puts on the real Demon) against
  deception (how little the town puts on it), a low-noise check on the ratings.
- **Sociological experiments** (need per-seat models; the engine only assigns per team today): one
  good player upgraded to a stronger model; one player of a weak team upgraded; only the evil team
  stronger; mixed tables. The user also asked "what happens if there's a ton?" (unclear; ask).
- **Done:** v5 x1 (Opus/Sonnet/Astra 2x2s, 10 seeds, `games/v5/x1-*`); v6 g1 (Opus high, Opus low,
  Sonnet 5, Astra, GPT-6 Sol; all 20 good-vs-evil pairings, 5 games each, seeds 20000–20099,
  `games/v6/g1-*`).

## Working with the user
Be concise: lead with the answer. Check realism and design before scaling up runs.
