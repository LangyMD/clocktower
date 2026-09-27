# Clocktower — notes for Claude sessions

An eval where language models play Blood on the Clocktower (Trouble Brewing, 9 players). It measures
holding coherent state and bluffs over a whole game. See README.md for the design.

## Running
- Setup: `pip install -e .` (Python ≥3.11). Tests: `python -m unittest discover -s tests`. No-API
  simulation: `python -m clocktower sim --games 200`.
- Keys come from the environment: `ANTHROPIC_API_KEY` (Claude Code on the web withholds that name, so
  the user stores it as `MY_ANTHROPIC_API_KEY`; `make_client` reads either), `OPENAI_API_KEY` (for `gpt-*` models). The
  Anthropic key is not workspace-scoped, so every request sends `anthropic-workspace-id`
  (`ANTHROPIC_WORKSPACE_ID`, default in `cli.py`). Without it the API returns a 400.
- A batch: `python -m clocktower run --games 10 --seed N --concurrency 30 --out games/v5/NAME` (games go
  under the current protocol version, `PROTOCOL` in `cli.py`; see `games/PROTOCOLS.md`). All games run
  in parallel; game k uses seed N+k-1 and rotates the Minion. Opus 5.5 games cost ~$3–4 and take
  10–20 minutes. Spend is logged in `games/ledger.jsonl` with a cap (`--budget`, default $1000; the
  user has said the budget can grow).
- After a batch: `python -m clocktower report games/v5/NAME/*`, commit the whole batch directory
  (transcripts, events, conversations, calls) and push, so results survive the session. Then
  republish the viewer: `python -m clocktower site` builds `site/`; publish `site/index.html` with the
  Artifact tool, `url: https://claude.ai/artifact/DpA1C6WTJATLvTqTi4XQiH`, and every other file under
  `site/` in `files` (same relative paths). That keeps the one viewer link the user has.
- When a change affects how games play, bump `PROTOCOL` and add a section to `games/PROTOCOLS.md`.

## Design decisions the user made (don't undo without asking)
- Memory is the model's own carried-over reasoning; no notebook, no state re-sent.
- Each day: private time (3 beats, whispers only, invisible to others, up to 3 whispers per turn)
  then the town square (3 beats, public only), then nominations. Same every day, fixed length: no
  early ends, no call-for-nominations. Dead players talk and whisper; only the living nominate.
- The Storyteller is scripted (`state.POLICY`); the LLM Storyteller was removed. Never exclude a
  legal Storyteller option: every decision is a `Choice` over all legal values with a uniform floor
  (`POLICY['any']`), and style is expressed only as weights in POLICY (all judgment calls).
- Nominations: each round everyone eligible is asked at once; one nomination is taken; accusation,
  defense, one comment turn for everyone, then the clockwise vote. Slayer shots on any public turn.
- Equal budget across models: same effort and per-turn output ceiling.
- Planned rating: a good Elo and an evil Elo per model, from homogeneous-team matchups (one model
  plays evil, another good), paired seeds, Bradley–Terry fit.

## Working with the user
Be concise: lead with the answer. Check realism and design before scaling up runs.
