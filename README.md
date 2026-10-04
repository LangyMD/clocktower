# Clocktower

An eval in which language models play Blood on the Clocktower (Trouble Brewing) against each other,
with a scripted Storyteller. One model plays the good team and another the evil team, so every game
pits one model's detection (finding the Demon) against another's deception (hiding it) over a whole
game of claims, whispers, bluffs and votes. It measures whether a model can hold coherent state and
a consistent story for hours of play.

- **The rules of the eval:** [`docs/PROTOCOL.md`](docs/PROTOCOL.md) (v17). Why each rule is what it
  is: [`docs/protocol-history.md`](docs/protocol-history.md).
- **Experiments so far and planned:** [`CLAUDE.md`](CLAUDE.md) (also the handbook for agent sessions).
- **Game logs:** the private Hugging Face dataset `dwarkesh/clocktower-games` (every transcript, event,
  call and conversation). Git keeps each game's `config.json` and `result.json`.

## Running

```sh
pip install -e .                       # Python 3.11+
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... HF_TOKEN=...
python -m unittest discover -s tests   # rules, Storyteller and engine tests (no API)
python -m clocktower sim --games 200   # random players, no API

python -m clocktower run --good-model claude-opus-5-5 --evil-model gpt-6.1-sol --games 2 --swap --seed 1 --out games/v13/demo
python -m clocktower run --good-model claude-opus-5-5,gpt-6.1-sol ...      # a mixed team (seats split evenly)
python -m clocktower run ... --seat-model good:claude-opus-5-5:1          # upgrade one good seat
python -m clocktower run ... --seat-model Imp:gpt-6-astra                 # a different model plays the Imp

python -m clocktower plan plans/timeline-models.json --within 10 --pairs 1 --seed 120000 --out games/v16/f1 > plans/f1.json
python -m clocktower tournament plans/f1.json      # every matchup at once, resumable
python -m clocktower analyze games/v16/f1-*/game-* # win rates, probes, detection and deception ratings
python -m clocktower fetch v9/e1-*                 # download logs from the dataset
python -m clocktower play                          # you and friends vs the AIs (see below)
python -m clocktower watch                         # spectator app; `site` builds it as static files
python -m clocktower replay games/X --view Casey --thinking
```

Each game directory holds `transcript.md` (omniscient replay with every seat's thinking), `events.jsonl`,
`calls.jsonl` (every API call with tokens and cost), `probes.jsonl` (belief probes), `conversations/`,
`config.json` and `result.json`. Spend is logged to `games/ledger.jsonl`, capped by `--budget`.

## Playing with friends

`python -m clocktower play` opens a table at port 8765 and prints two links: one for you (the host) and one
for friends. Everyone joins from their own phone or laptop, picks a name and an allegiance (good, evil or
either; secret from everyone), and the host picks the table size (5-15), the models for the good and evil
AI seats (`random` = free practice bots) and an optional turn timer, then rings the bell. Each person's seat
gets exactly what a model in that seat gets: the same events, the same prompts, the same moves (one whisper
per private-time turn, speech, nominations, votes, night choices, Slayer shots) and word limits. The rules
panel shows the AI system prompt word for word. After the game the Grimoire is revealed, along with
who played each seat and a link to the full transcript with every AI's reasoning. Logs go to `games/play/`
(not in git); `--budget` caps this session's spend (default $100).

Friends on the same Wi-Fi open the printed address directly. For friends elsewhere, put a tunnel in front of
it, e.g. `cloudflared tunnel --url http://localhost:8765` (free, no account) or Tailscale, and share that URL.
API keys stay on the host's machine.

No computer to host from? `render.yaml` deploys the table to Render's free tier: in Render, New → Blueprint →
this repo, then enter the API keys. Everyone opens the app's URL; the first to join hosts, and anyone can
tap "Make me the host". The lobby offers
only models whose key the server has (`random` practice bots always). A free instance sleeps when unused and
loses an unfinished game if it restarts.

## Code

| File | What it does |
|---|---|
| `characters.py` | Trouble Brewing characters, setups by table size, night order |
| `state.py` | Grimoire, registration, deaths and victory; the Storyteller's choices and `POLICY` |
| `game.py` | Setup, nights, beats, nominations, votes; one typography for all speech |
| `prompts.py`, `schema.py` | The player system prompt and the fixed output schema |
| `llm.py` | Claude and OpenAI conversations, per-model settings (`MODELS`), prices, context trimming, ledger |
| `probe.py` | Belief probes (out-of-game forks of each seat's conversation) |
| `analyze.py`, `report.py` | Ratings, win rates, voting and probe scores; batch reports |
| `tournament.py` | Experiment plans and the parallel launcher |
| `supervise.py` | Batch health numbers (lost turns, capped turns, refusals, spend) |
| `store.py` | The Hugging Face log store |
| `agents.py`, `web.py`, `table/` | Seats; the multiplayer table (lobby, API and page) for human play |
| `watch.py`, `viewer/`, `site.py`, `render.py` | Spectator app |
| `cli.py` | Every command |
