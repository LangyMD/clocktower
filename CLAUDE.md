# Clocktower — notes for Claude sessions

An eval where language models play Blood on the Clocktower (Trouble Brewing, 9 players). It measures
holding coherent state and bluffs over a whole game. See README.md for the design.

## Running
- Setup: `pip install -e .` (Python ≥3.11). Tests: `python -m unittest discover -s tests`. No-API
  simulation: `python -m clocktower sim --games 200`.
- Keys come from the environment: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` (for `gpt-*` models). The
  Anthropic key is not workspace-scoped, so every request sends `anthropic-workspace-id`
  (`ANTHROPIC_WORKSPACE_ID`, default in `cli.py`). Without it the API returns a 400.
- A batch: `python -m clocktower run --games 10 --seed N --concurrency 30 --out games/NAME`. All games run
  in parallel; game k uses seed N+k-1 and rotates the Minion. Opus 5.5 games cost ~$3–4 and take
  10–20 minutes. Spend is logged in `games/ledger.jsonl` with a cap (`--budget`, default $1000; the
  user has said the budget can grow).
- After a batch: `python -m clocktower report games/NAME/*`, then commit `games/NAME` (conversations
  and calls.jsonl are gitignored) and push, so results survive the session.

## Design decisions the user made (don't undo without asking)
- Memory is the model's own carried-over reasoning; no notebook, no state re-sent.
- Each day: private time (3 beats, whispers only, invisible to others, up to 3 whispers per turn)
  then the town square (3 beats, public only, ends early on a majority call or a silent beat), then
  nominations. Same every day. Dead players talk and whisper; only living calls open nominations.
- The Storyteller is scripted (`state.POLICY`, `game.pick_bluffs`); an LLM Storyteller is optional
  (`--storyteller model`). Never exclude a legal Storyteller option; express style only as weights
  in POLICY, and say which numbers are judgment calls.
- Equal budget across models: same effort and per-turn output ceiling.
- Planned rating: a good Elo and an evil Elo per model, from homogeneous-team matchups (one model
  plays evil, another good), paired seeds, Bradley–Terry fit.

## Working with the user
Be concise: lead with the answer. Check realism and design before scaling up runs.
