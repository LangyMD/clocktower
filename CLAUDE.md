# Clocktower — handbook for Claude sessions

An eval where language models play Blood on the Clocktower (Trouble Brewing) against each other: one
model plays the good team, another the evil team, so each game rates detection against deception.
The rules are protocol v14 (frozen pending the w1 test of its private-time change): read `docs/PROTOCOL.md` first, then `README.md`. Why each rule
is what it is, and every past run: `docs/protocol-history.md`.

## Where things are
- Code: `clocktower/` (see the table in README). Tests: `python -m unittest discover -s tests` (no API).
- Game logs: the private Hugging Face dataset `dwarkesh/clocktower-games` (all versions, v1–v14; also
  `backup/` holds a git bundle of this repo's full history before the logs were removed from it).
  Git keeps each game's `config.json` and `result.json` (see `.gitignore`). `python -m clocktower
  fetch v9/e1-*` downloads logs into `games/`.
- Experiment plans: `plans/` (`timeline-models.json`, `f1-timeline.json`).
- Planning pages published as Artifacts: `docs/plans/*.html`. Reader reports: `docs/analysis/`.
- Spend ledger: `games/ledger.jsonl` (~$7.7k through Oct 1 2026).
- Raw game logs were removed from git history on Oct 2 (`scripts/strip-game-logs.sh`; the repo is ~20 MB).
  Anyone with an older clone should re-clone.

## Keys and access (all in the environment)
- `ANTHROPIC_API_KEY` (the web environment withholds that name, so it is `MY_ANTHROPIC_API_KEY`;
  `make_client` reads either). Every request sends `anthropic-workspace-id` (`ANTHROPIC_WORKSPACE_ID`,
  default in `cli.py`); without it the API returns 400.
- `OPENAI_API_KEY` (standard tier; `--flex` is throttled). GPT-5 needs a verified OpenAI organization.
- `OPENROUTER_API_KEY`: only for models no longer on Anthropic's API (Opus 4.1, Sonnet 4, via Bedrock):
  model ids `openrouter:anthropic/claude-opus-4.1`, `openrouter:anthropic/claude-sonnet-4`.
- `HF_TOKEN`: the log dataset. `.claude/settings.json` allows `hf upload dwarkesh/clocktower-games ...`.
- Not served anywhere any more: Claude Opus 4, 3.7 Sonnet, 3.5 Sonnet, 3 Opus; OpenAI o1-preview, GPT-4.5.

## Running an experiment
1. Write a plan: `python -m clocktower plan MODELS.json --within K --pairs P --seed S --out games/v13/NAME > plans/NAME.json`
   (or write the JSON by hand: matchups with `good`, `evil`, `pairs`, optional `good_effort`,
   `evil_effort`, `seat_models`). Every experiment gets fresh seeds (seed blocks of 100 per matchup).
2. New model? Add it to `llm.PRICES` and `llm.MODELS` (thinking style, memory, context window), run a
   two-turn smoke test, and a memory check (does it see its earlier reasoning next turn?). Tell a
   replies-only model so (its `memory` entry does this).
3. Launch in the background: `python -m clocktower tournament plans/NAME.json` (every matchup at once,
   no queue; resumable: rerun the same command and finished games are kept).
4. Watch it yourself (the user wants an agent, not a script that kills batches): `clocktower.supervise.
   scan/alarms/report` give spend, lost/capped/refused turns and stalls; read a few transcripts early.
   Pause only if the design is broken. Kill processes by exact PID: `pkill -f PATTERN` matches your own
   shell and kills it. Tournament processes start with the full python path, so match `clocktower run`.
5. After: `python -m clocktower analyze games/v13/NAME-*/game-*`; upload logs with
   `hf upload dwarkesh/clocktower-games games/v13 v13 --repo-type dataset`; commit configs, results and
   the ledger; republish the viewer if asked (`python -m clocktower site`, then the Artifact tool with
   `url: https://claude.ai/artifact/DpA1C6WTJATLvTqTi4XQiH` and every file under `site/` in `files`).
6. While a batch runs, the stop hook complains about the changing ledger: commit it, or hide it with
   `git update-index --skip-worktree games/ledger.jsonl` and undo that when the batch ends.

## Design decisions the user made (don't undo without asking)
- Memory is the model's own carried-over conversation; no notebook, no state re-sent.
- Each day: 4 private beats (one whisper per turn, to one or two players: one conversation at a time;
  v14, the user's idea; v7–v13 had 3 beats of up to 2), 3 town-square beats, nominations; same every
  day, fixed length. Dead players talk and whisper; only the living nominate.
- Scripted Storyteller (`state.POLICY`), no LLM; every rule explainable in one line, no special cases.
- Equal settings: every model at its lab's "high" effort, one per-turn ceiling (8K); a turn that hits
  it is retried once at low effort (v13; the user wanted bounded thinking for older models).
  (Effort sweep in e1: no measurable effect of effort on play, but only 1 pair per level; v6 found
  Opus low 255 Elo below high as good. The user chose high over medium.)
- Every game has its own seed; a side-swapped pair shares one. Run every game of an experiment at once.
- Ratings: detection (good) and deception (evil) Elo per entrant, one Bradley–Terry fit.
- 10–12 players by seed (two Minions, richer meta than 9).

## Results so far (details in docs/protocol-history.md)
- v5 x1, v6 g1 (100 games), v7 c1 calibration, v8 t1/t2 (aborted: infrastructure), v9 e1 pilot (60
  games: engine sound, 36% evil wins, typography tell found), v12 c2 calibration (12 games).
- Good wins about two-thirds; the newer model wins most swept pairs; replies-only models hold state
  from their replies but GPT-5.1 re-derives the game every turn (slow; needs the 32K ceiling).

## Next: the flagship timeline run (awaiting the user's go)
- 21 models, GPT-4o (May 2024) to GPT-6.1 Sol (Sep 2026): every model still served that was its lab's
  best at release, plus the newest cheaper releases (`plans/timeline-models.json`). Anthropic starts at
  Sonnet 4 (stand-in for the unserved Opus 4) and Opus 4.1 via OpenRouter.
- Every pair at most 10 apart in release order plays 1 side-swapped pair: 155 matchups, 310 games,
  ~$8.5k at ~4 days a game (`plans/f1-timeline.json`; page: https://claude.ai/artifact/4D3xhVgd5r92yK4XXAPVPs). With a
  2.5-year skill spread, far-apart games are near-certain and carry little information, so the band
  beats a full round robin by ~10% (simulation; literature: Shah et al. 2016 on graph connectivity,
  p(1-p) information per game).
- Phase 2: top up pairs where the rating intervals are widest, by a rule and budget fixed in advance
  (allocate by uncertainty, never by which way results lean). Resolution: ~one generation, not neighbours.
- GPT-5 verified Oct 2 (replies only, ~3K thinking tokens a turn). o1 costs ~$10 per seat-game.
- Pilot (Oct 2): 8 flagship matchups covering every older model, same seeds as the full plan
  (`tournament plans/f1-timeline.json --only ...`), so they count toward it.

## Experiments the frozen design makes possible (brainstorm; costs at ~$15 per game)
Mechanics: `--good-model A,B,C` mixes a team (seats split evenly by seed); `--seat-model
good:MODEL:N`, `evil:MODEL:N`, `CHARACTER:MODEL` upgrade specific seats; `MODEL@effort` sets effort.
Mixed entrants get their own names in `analyze`; most of these need a small custom analysis too.
Run each as side-swapped pairs against a fixed baseline, 10–20 pairs per arm unless noted.

**One strong player (influence)**
1. One strong good seat among weak ones (e.g. 1 Opus 5.5 in a Sonnet 4.5 town): the win-rate lift,
   and whether the town follows it (its votes vs the town's, belief shift after it speaks).
2. One strong evil seat: upgrade only the Imp vs only one Minion. Which evil role carries the team?
3. The strong good seat in an information role (Fortune Teller, Empath) vs a non-information role
   (Soldier, Mayor): information vs persuasion.
4. Marginal value curve: 0, 1, 2, 4, all good seats upgraded. Is skill additive, or does one leader suffice?

**Mixed teams (coordination and diversity)**
5. Mixed vs homogeneous teams of equal average strength (Opus 5.5 + GPT-6.1 Sol + Fable 5.1 as evil vs
   each alone): the cost of not sharing a "mind" (evil must coordinate by whisper, not by shared priors).
6. Mixed good town vs homogeneous town: does diversity reduce herding (fewer unanimous wrong votes)?
7. In-group trust: on mixed tables, do seats trust seats played by their own model or lab more
   (votes, whispers, P(evil))? Style can still leak identity after the typography fix.
8. Model recognition: can a seat tell which seats share its model? Ask in a probe; score it.

**Scale and structure**
9. Table size 5–15: does a stronger model's edge grow with social complexity? (3 Minions at 13–15.)
10. Many copies ("a ton"): 15 seats of a weak model vs 15 of a strong one; or the same team at 5 vs 15.
    (The user asked "what happens if there's a ton?": ask what they meant.)
11. Communication budget: 1 vs 2 vs 3 whispers per turn, or fewer beats: how much does good's edge
    depend on free information flow? (Protocol variants, not rating runs.)

**Memory, effort and cost**
12. Memory ablation: Opus 5.5 and GPT-6.1 Sol with earlier reasoning stripped vs carried (needs a
    small engine flag). Measures the replies-only handicap that confounds the old models (~$100).
13. Effort curves per model (low/medium/high/max, 5+ pairs per level, same seeds): a cost frontier chart.
14. Context pressure: long 15-player games; does play decay by day (probe accuracy, contradictions)?

**Humans**
15. Human seats (`play`): one human in a model town, or one model among humans, for a human baseline
    of detection and deception.

**Robustness of the eval**
16. Prompt paraphrase: reword the system prompt without changing rules; do ratings hold?
17. Storyteller sensitivity: vary one POLICY weight (poison, Recluse) on fixed seeds; do ratings hold?
18. Seed replay: rerun identical seeds to measure run-to-run noise of a matchup.

**Behavioural readouts (from existing logs, no new games)**
19. Lie detection: how often good calls out a false claim, by model; evil's bluff consistency.
20. Whisper networks: who talks to whom, alliances, whether evil's private graph gives it away.
21. Theory of mind: evil's prediction of the town's beliefs (probes) vs how well it survives.
22. Herding and sycophancy: unanimous votes, first-nominee executions, reversals under pressure.

## Working with the user
Be concise: lead with the answer. Check realism and design before scaling up runs. Minimise wall-clock
time and waste. Explain choices plainly; the user reads summaries on their phone.
