# Clocktower — handbook for Claude sessions

An eval where language models play Blood on the Clocktower (Trouble Brewing) against each other: one
model plays the good team, another the evil team, so each game rates detection against deception.
The rules are protocol v17 (frozen): read `docs/PROTOCOL.md` first, then `README.md`. Why each rule
is what it is, and every past run: `docs/protocol-history.md`.

This file has two parts. **Part 1 (guidelines)** is durable: keep it short and true, and edit it when
something changes. **Part 2 (dated session notes)** holds longer, perishable observations, each block
headed with its date; treat them as context, not rules. Sessions add to and prune Part 2 on their own (see "Keeping this file current").

# Part 1 — guidelines

## Where things are
- Code: `clocktower/` (table in README). Tests: `python -m unittest discover -s tests` (no API calls).
- Game logs: the private Hugging Face dataset `dwarkesh/clocktower-games` (v1–v17, plus `media/` for
  videos and `backup/` for a git bundle of the repo's history before logs were removed from it). Git
  keeps each game's `config.json` and `result.json` only (see `.gitignore`).
  `python -m clocktower fetch v16/f2-*` downloads logs into `games/`.
- Plans: `plans/` (one JSON per experiment; `models-2026.json` and `timeline-models.json` are model lists).
- Analysis scripts: `scripts/` (2026 ratings, allocation, resume helper; see the cleanup note in Part 2).
- Planning and results pages (published as Artifacts): `docs/plans/*.html`. Reader reports:
  `docs/analysis/<batch>/`. The full player prompt with example turns: `docs/player-prompt.md`.
- Spend ledger: `games/ledger.jsonl` (all-time API spend, ~$21.3k through Oct 2 2026).
- Human play: `python -m clocktower play` (lobby + table in `clocktower/web.py` and `clocktower/table/`;
  multi-device, secret allegiances, `random` practice bots; logs in `games/play/`, git-ignored).
- Videos: `media/trailer-f2-opus47-v-opus55/` (one game) and `media/montage-best-plays/` (multi-game montage:
  scene JSONs → ElevenLabs → Playwright frames → ffmpeg; see its README). MP4s are on HF under `media/`.

## Keys and access (all in the environment)
- `ANTHROPIC_API_KEY` (the web environment withholds that name, so it is `MY_ANTHROPIC_API_KEY`;
  `make_client` reads either). Every request sends `anthropic-workspace-id` (`ANTHROPIC_WORKSPACE_ID`,
  default in `cli.py`); without it the API returns 400.
- `OPENAI_API_KEY` (standard tier; `--flex` is throttled). GPT-5 needs a verified OpenAI organization.
- `OPENROUTER_API_KEY`: only for models no longer on Anthropic's API (Opus 4.1, Sonnet 4, via Bedrock):
  `openrouter:anthropic/claude-opus-4.1`, `openrouter:anthropic/claude-sonnet-4`.
- `HF_TOKEN`: the log dataset. `.claude/settings.json` allows `hf upload dwarkesh/clocktower-games ...`.
- `ELEVENLABS_API_KEY`: voices for videos (model `eleven_v4`).
- The user has auto-reload on the Anthropic and OpenAI accounts; a call that fails for lack of credit
  waits up to 30 minutes and retries (both providers), so a batch pauses rather than fails.
- Not served anywhere any more: Claude Opus 4, 3.7 Sonnet, 3.5 Sonnet, 3 Opus, Haiku 3.5; OpenAI
  o1-preview, GPT-4.5.

## Running an experiment
1. Write a plan: `python -m clocktower plan MODELS.json --within K --pairs P --seed S --out games/v17/NAME > plans/NAME.json`,
   or by hand: matchups with `good`, `evil`, `pairs`, optional `seed`, `args` (extra run flags such as
   `["--minions", "Spy,Baron"]`), `good_effort`, `evil_effort`, `seat_models`; a plan `budget` caps the
   all-time ledger. Every experiment gets fresh seeds (blocks of 100 per matchup).
2. New model? Add it to `llm.PRICES` and `llm.MODELS` (thinking style, memory, context window), run a
   two-turn smoke test and a memory check (does it see its earlier reasoning next turn?), and check
   whether it accepts `thinking: disabled` (else add it to `llm.ALWAYS_THINKS`).
3. Launch in the background: `python -m clocktower tournament plans/NAME.json` (one process per
   matchup, every game at once; resumable: rerun the same command and finished games are kept).
4. Keep a `run_in_background` Bash waiter running for the whole batch
   (`while pgrep -f '[c]locktower run'; do sleep 60; done`, max 2 h, re-arm it): **an idle session's
   container is reclaimed within minutes and every game dies.** Schedule check-ins with `send_later`.
5. Watch it yourself (the user wants an agent, not a script that kills batches):
   `clocktower.supervise.scan(['games/v17/NAME-'])`, `report`, `alarms` for spend, lost/capped turns and
   stopped games; read a few transcripts early; check CPU (`vmstat`) and memory (`free -m`).
   - A stopped game (seat failed, budget, halted) keeps its checkpoint: `python scripts/resume_stopped.py PLAN`
     relaunches each one alone. To halt one game: `touch <game>/STOP`. To rerun one game:
     `tournament PLAN --only MATCHUP/gNN` (or `gNN-swap`).
   - After a container restart, rerun the `tournament` commands; games resume from their last dusk.
   - Kill processes by exact PID. `pkill -f PATTERN` (and `pgrep` inside `$(...)`) matches your own
     shell's command line and kills it; write patterns like `'[c]locktower run'`.
6. After: `python -m clocktower analyze games/v17/NAME-*/game-*` (or `scripts/ratings2026.py`); upload
   logs with `hf upload dwarkesh/clocktower-games games/v17 v17 --repo-type dataset`; commit configs,
   results and the ledger; merge to main (fast-forward push). Republish the viewer if asked
   (`python -m clocktower site`, then the Artifact tool with `url: https://claude.ai/artifact/DpA1C6WTJATLvTqTi4XQiH`
   and the changed files under `site/` in `files`; it holds ~140 MB, so send new data files only).
7. While a batch runs the stop hook complains about the changing ledger and results: commit them as they
   land (`git add -A games/v16 games/v17`), or hide the ledger with `git update-index --skip-worktree
   games/ledger.jsonl` and undo that when the batch ends.

## Design decisions the user made (don't undo without asking)
- Memory is the model's own carried-over conversation; no notebook, no state re-sent.
- Each day: 6 private beats (one whisper per turn, to one or two players: one conversation at a time),
  3 town-square beats, nominations; same every day, fixed length. Whispers are private (v15's public
  who-whispered-to-whom log cut evil to ~20% and the user dropped it). No talk after the town square
  (the user: real games don't do that). Dead players talk and whisper; only the living nominate.
- Scripted Storyteller (`state.POLICY`), no LLM; every rule explainable in one line, no special cases.
- Equal settings: every model at its lab's "high" effort, one per-turn ceiling (8K); a turn that hits it
  is retried once with the least thinking the model allows (bounded thinking was the user's call).
- Every game has its own seed; a side-swapped pair shares one. Run every game of an experiment at once.
  The guaranteed Minion is chosen per game so a batch balances Minions.
- Ratings: one Bradley–Terry fit with a good-side advantage and setup terms; lead with one combined
  rating per model; split detection (good) and deception (evil) once each model has ~40+ games a side.
- 10–12 players by seed (two Minions).
- Allocate extra games by uncertainty per dollar with a rule fixed in advance, never by which way results lean.

## Keeping this file current (every session, unprompted)
- Before ending a session that ran games, changed code or design, or learned something non-obvious,
  add a dated block to Part 2 (`## YYYY-MM-DD: topic`): what was done, results with numbers, lessons,
  open questions, next steps. Write it for a future session that has none of this context.
- Promote anything that became a rule or a lasting fact (a new protocol, a decision the user made, a
  path, a command) into Part 1, and fix Part 1 wherever it went stale.
- Prune Part 2: delete or shorten blocks that are superseded or done (git keeps the history), so Part 2
  stays a page or two. Newest block first.
- Commit CLAUDE.md with the work, and tell the user in one line what you added or pruned.

## Working with the user
Be concise: lead with the answer, plain words, short tables; the user reads on their phone. Check
realism and design before scaling up; ask before any rule change or spending past the stated budget
(report early when a batch is heading over). Minimise wall-clock time and waste. Explain choices
plainly. When the user asks for readers, spin up several subagents on separate questions in parallel.

# Part 2 — dated session notes

## 2026-10-07: mixed-team pilot (b1), design decisions
- **Pilot B** (`plans/b1-mixed-pilot.json`, 16 games, $118): half Opus 5.5 + half GPT-5.6 Sol (seats random; two
  matchups with opposite list order so each model gets the odd seat half the time) vs pure GPT-6.1 Sol, both sides.
  Analysis `scripts/mixed_pilot.py` → `docs/analysis/b1-mixed-pilot.json`. Wins match the members' average rating
  (good 4/8 vs 4.2 expected; evil 1/8 vs 1.1), too few games to see a mixing penalty. In-group: Opus seats start
  conversations with Opus teammates 15 points above chance; Sol 5.6 leans 6 points toward Opus (seat/role pull), so
  Opus's own preference ≈ 9–15 points; Sol shows none. Same-model vote agreement 72% vs 63% cross (partly voting style).
- Opus 4.8's low rating: no bug (0 lost turns in v17); 1–15 vs GPT-5.5, only 3 opponents (its f2 round robin was
  dropped). Rule agreed in principle: every model plays every other at least one pair before top-ups.
- Learning-from-experience design (not built): shared notes on the good team leak alignment (a password), so
  only (1) evil-only learners (evil already knows teams) or (2) a league of individual agents with private notes and
  alignment dealt independently of agent are clean. Notes cap ~10K tokens rewritten each round; reflection budget large.
- Rating scale: anchor 1500 to the mean of the 11 2026 models permanently (not the mean of whatever is in the fit).
- **Allocation rule in code:** `python -m clocktower.allocate MODELS RATINGS GAMEGLOBS... --target T` (floor of one pair
  per matchup, one extra pair for a >2.5 SE style clash, then precision per dollar on models above ±T; cap 4 pairs per
  matchup, no opponent >25% of a model's games; Minions least dealt). Half-widths calibrated to the bootstrap.
- **f4 floor batch** (`plans/f4-floor.json`, 16 games, $986): Opus 4.8's 7 missing opponents + Opus 4.7 v Astra (clash).
  Opus 4.8 won 2 of 14 → 1203 [1077, 1288] (was 1194 [1051, 1306]). Refit over 368 games (`scripts/ratings2026.py`
  now includes f4): trend +650/yr. Worst half-width now Opus 4.7 ±109; reaching ±100 for all costs ~$575 more.
- **f5 precision top-up** (`plans/f5-precision.json`, 18 games, $649): chosen by the rule for ±100. Refit over 386 games:
  GPT-6 Astra 1859 > GPT-6.1 Sol 1734 > Fable 5.1 1595 ≈ GPT-5.6 Sol 1591 > Opus 5.5 1549 ≈ Fable 5 1544 > GPT-5.5 1482
  > Opus 4.6 1432 > GPT-5.4 1276 > Opus 4.7 1241 > Opus 4.8 1198; trend +651/yr [553, 827]; evil wins 33%. Every model
  within ±100 except Astra ±102 (lopsided range: it rarely loses). Ratings and leaderboard pages rebuilt with these numbers (Oct 25);
  lab-trends page not yet.
- Parser gap: GPT-5.5 once sent several JSON objects in one reply four times running (seat failed; game relaunched).
  Fix to consider: accept the first object.

## 2026-10-05: why Astra wins + best-games readers
- Six parallel readers over all 372 2026 games (logs fetched with `HF_HUB_DISABLE_XET=1` and
  `snapshot_download(..., ignore_patterns=['*.pkl'])`: Xet downloads of checkpoint.pkl fail size checks here,
  and fetching everything at once hits HF 429s). Reports and summary: `docs/analysis/astra/README.md`.
- Astra 26/26 good, 62% evil. Good edge = group decisions (top suspect evil 92%, executions 76–78% hit evil),
  not sharper Demon beliefs (≈ Sol 6.1). Evil edge = quiet, following Demon (day-2 suspicion at chance),
  lies consistent with real info, planned succession, endgame conversion 83%. It thinks the least of any model.
- OpenAI models' reasoning is encrypted in logs: use probes.jsonl and outputs to study them.
- Made a 5.5 min montage (`media/montage-best-plays/`, HF `media/montage-best-plays.mp4`): 5 games (Sol 6.1 dead
  Ravenkeeper con, Fable 5.1 poisoned vision, Opus 5.5 deliberate Mayor tie, Astra catching a Spy, Astra's Saint
  trap) + Astra stats. Subagents wrote one scene JSON per game (quotes checked). Rendering ~3 fps (55 min).

## 2026-10-07: style fingerprinting, good-side lying, probes (report: `docs/analysis/f2/style-lies-probes.md`)
- No player ever inferred teams from "writes like me" or model identity (4 readers, 372 games). The signal
  exists, though: 16 punctuation/length features of day-1 text separate teams with AUC 0.81, and a blind
  2-cluster split is 69% evil, versus 38% evil for day-1 executions. Same-model good players echo each
  other, and their teammates misread it as an evil bloc. This is a validity risk if models learn to
  fingerprint.
- Good seats rarely lie: 2.7% hard role lies and 4.6% fake info. Opus 4.7 lies most (17%), GPT-5.5 and
  Astra least. Ravenkeeper bluffs most (18%, as bait). Data is in `docs/analysis/f2/good-lies.json`, from a
  Sonnet 5.5 pass (~$53, not in the ledger).
- Probes: good P(true Imp) correlates 0.87 with good win rate and 0.89 with detection Elo across models.
  Day 1 is near chance for everyone.

## 2026-10-04: multiplayer human table
- Replaced the one-seat `play` page with a lobby + table for several people on their own devices
  (stdlib HTTP, 1 s polling, per-browser tokens). Host link carries a key (`#host=`); friends use the LAN
  URL or a tunnel. Allegiance prefs are never shown to others (only counts in errors); seat mapping is
  revealed at game end. Deaths shown to a seat are the publicly announced ones (the engine's own `dead`
  list runs ahead at night). `build(humans=fn)` replaces `human=`; model `random` = RandomSeat.
- Tested: `tests/test_web.py` (a whole two-person game through the API) and Playwright runs (desktop host
  + phone friend, full games vs random bots). Not yet played against real models: first real game should
  check AI latency vs human patience and the 1 h cache TTL cost.
- Hosting: this cloud container can't serve players (no inbound; cloudflared's edge port 7844 is blocked).
  `render.yaml` deploys to Render free tier (user's app: https://clocktower-ogul.onrender.com). No host
  password (the user trusts players): the first joiner hosts, anyone can tap "Make me the host"; links follow the
  request's Host header; the lobby lists only models with a key present.
- Human-game spend goes to `games/play/ledger.jsonl` (git-ignored), not the eval ledger, so a 0.1-CPU host
  doesn't parse 42 MB at start; `--budget` caps it per server start.
- Live test (Oct 4, user's Render app, 1 scripted human + 9 Opus 5.5, 10 players): whole game in 23 min
  (4 days, 65 human turns, 5-100 s between turns, median ~20 s); evil won (Spy read the Grimoire and claimed
  the Slayer the Washerwoman was shown). Fixed after: double-tap double-submit (dock now seals at once),
  phone dock prompt clamps to 2 lines. Absent players pass after 120 s (`web.AWAY`); host can end a game.
- Testing the live app from a cloud session: the sandbox proxy drops Chromium's parallel requests
  (ERR_TOO_MANY_RETRIES); run a localhost relay (urllib + /root/.ccr/ca-bundle.crt) and point the browser
  at it. Right after a Render deploy, requests can hit the old and new instance for a few minutes.
- Ideas: show the seat's own past whispers grouped by person; spectator mode for dead/late joiners.

## 2026-10-04: state at the end of the Sept 30 – Oct 2 sessions

### Where the project stands
- Protocol history in one breath: v14 one whisper per turn → v15 public whisper log (dropped) → v16
  private whispers, 6 beats → v17 bounded retries, per-game Minion choice, credit waits. Details and
  every batch's numbers: `docs/protocol-history.md`.
- **2026 study done** (352 games: f2 round robin + f3/f3b top-ups; ~$11.6k incl. f2): the 11 models
  released in 2026 gain ~645 Elo/year (90% CI 530–820); detection +634, deception +692, not separable.
  GPT-6 Astra 1858 > GPT-6.1 Sol 1729 > Fable 5.1 1595 ≈ GPT-5.6 Sol 1593 > Fable 5 1561 > Opus 5.5 1538
  > GPT-5.5 1472 > Opus 4.6 1427 > GPT-5.4 1268 ≈ Opus 4.7 1265 > Opus 4.8 1194. Page:
  https://claude.ai/artifact/BEapb2nuJGL1Tfrb96ke58 (data `docs/plans/f2-ratings.json`, built by
  `scripts/ratings2026.py` + `scripts/build_ratings_page.py`). Evil wins ~32%.
- **Not started:** the full timeline back to GPT-4o (21 models, `plans/f1-timeline.json`, page
  https://claude.ai/artifact/MAbeLPxmENkdfEQT8j75mt). That plan predates v17: regenerate it with balanced
  Minions and the 2026 results folded in (the 2026 games count; only pre-2026 models and cross-era pairs
  need new games). Biggest costs there: o1 (~$7/seat-game) and Opus 4.1 (~$7).
- **User asked for, not yet done:** consolidate and clean the repo (see "Cleanup" below).

### Pages and artifacts
- Ratings (current): https://claude.ai/artifact/BEapb2nuJGL1Tfrb96ke58 (by release date)
- Gains by lab (detection/deception vs release date, per-lab trends): https://claude.ai/artifact/HiPbbNTToUydW6Sjes6asq
  (`scripts/lab_trends.py` → `docs/charts/lab-trends.json`, filled into `lab-trends.template.html`). Per year: detection
  OpenAI +1083 vs Anthropic +186 (gap 608–1272, clear); deception +764 vs +590 (gap could be chance).
- Leaderboard chart (ranked, overall/detection/deception tabs): https://claude.ai/artifact/Sc8dfYHJMLHBQdQeLcWSMu
  plus a head-to-head expected-win-rate grid (`docs/charts/leaderboard.html`; PNGs `docs/charts/*.png`)
- Flagship plan explainer: https://claude.ai/artifact/MAbeLPxmENkdfEQT8j75mt (pre-v17 numbers)
- Detection vs deception explainer (simulated): https://claude.ai/artifact/RwxbjAyo42RzzAM6FK7MiX
- Spectator viewer, v1–v15 games (no v16/v17 yet): https://claude.ai/artifact/DpA1C6WTJATLvTqTi4XQiH
- Trailer (65 s, Opus 5.5 evil vs Opus 4.7, the Scarlet Woman "deal"): HF `media/trailer-f2-opus47-v-opus55.mp4`.

### Engineering lessons (things that cost hours)
- **Idle reclaim:** with no background task running, the container was reclaimed ~4 minutes after the
  session went idle, three times in a row (games made no progress 08:00–10:00 on Oct 1). A
  `run_in_background` waiter fixes it; each lasts at most 2 h, so re-arm at check-ins. Real restarts
  still happen (~every 10–12 h); checkpoints make them cheap.
- **Checkpoint semantics:** a game checkpoints at each dusk; a resume replays from there and truncates
  `calls.jsonl`/`events.jsonl` back, so replayed spend shows in the ledger but not in the game's own logs
  (projections from game logs undercount; use the ledger). A resumed game deletes its stopped
  `result.json` (git sees a deletion until it finishes).
- **Budget cap** is the all-time ledger, read when each process starts: processes started early keep
  running past it, relaunched ones stop at once. Set a plan's `budget` to ledger-now + batch budget + margin.
- **CPU:** the box has 4 vCPUs and 16 GB. Games are I/O-bound (~0.6–1% CPU each after the fix), so one
  asyncio process runs hundreds of calls (tested: 100 fake games in one process ≈ 1 game's wall time,
  832 calls in flight). Loading the CA bundle per OpenAI request was 60% of CPU: one shared TLS context
  now (`llm.TLS`). ~200 MB per process, so not one process per game. ~300 concurrent games is the ceiling.
- **Retries by model:** Opus 4.6/4.7/4.8 accept `thinking: disabled`; Fable 5, Fable 5.1, Opus 5.5 and
  Sonnet 5.5 reject it (they retry at low effort; `ALWAYS_THINKS`). Opus 4.8 overthinks late in games
  (v16: 40% of its low-effort retries re-hit 8K; 76 lost turns) — the reason for v17.
- **Latency sets wall-clock:** GPT-5.4's median turn is 42 s (others 5–15 s), so batches end ~6 h after
  launch, gated by its games; a full day of nominations can take an hour. Waves inside a beat are serial
  by design (later players react to earlier ones); everything else is parallel.
- **Seeds and Minions:** plan seeds stepping by 100 (≡ 0 mod 4) made every f2 game a Poisoner game; the
  Minion is now set per game (`--minions`), balanced across the batch.
- The Anthropic "requests to retired models are failing" emails (Oct 1) were one probe request each to
  old models on Sept 30 from the "mac mini" key: harmless.

### Game design: what the readers found (reports in `docs/analysis/`)
- Private time: one whisper per turn reads far more like a real table than the old 2-per-turn (which
  ran parallel conversations, copy-pasted messages and gave evil a free back-channel). 6 beats beats 4
  (real follow-up, evil gets enough reach) and 8 (repetition, hive mind; +25% cost). Diversity and drama
  barely depend on private time; they come from models, deals and balance.
- The good team's "hive mind" comes from ~60–70% of good players claiming publicly on day 1, in every design.
- Evil's beat 1 is always a closed three-way team briefing (the most repetitive moment of a game);
  telling models the whisper log was evidence (c3h) didn't change it.
- Three-person huddles work mechanically; most are one-shot; lasting three-way threads are mostly evil team chat.
- Realism gaps from the rules: dead players write ~25% of public words (56% on the final day); swing
  voters get 4–6 whispers a beat; random nomination order decided at least one game. All left as is.
- Duds (~25% of games): mostly older-model blunders and deal luck (day-1 Slayer hits, night-1 Empath
  between evil players); 10-player tables dud more (34%) than 12 (17%). Setup effects (Elo toward good
  vs a Poisoner game): Spy +67, Baron +80, Scarlet Woman −67; 12 players +68.
- Model styles: newer models whisper to two people and get replies; older ones speak every public turn
  in 150-word speeches. Sonnet 5.5 passes most private turns. GPT-6 Astra is the best detective (73% of
  its executions hit evil). Sol and Astra open with "trade three-for-threes".
- Best games for a video: `f2-opus47-v-opus55/game-01` (Scarlet Woman's deal → Saint executed),
  `f2-astra-v-sol61` pair, `f2-opus46-v-opus48/game-01`, `f2-gpt55-v-astra/game-01`,
  `f2-fable5-v-gpt56sol/game-01` (see `docs/analysis/f2/interesting.md`).

### How I think about the eval (statistics)
- One pair per matchup can't rank neighbours; ~6 pairs separate 100 Elo. Far-apart matchups are ~90%
  predictable and carry little information: spend on near neighbours and cheap models (greedy
  information-per-dollar, `scripts/design.py`/`topup.py`), capped per matchup (4–8 pairs) so one
  non-transitive pairing can't dominate.
- Cost per game varies 30×: Fable 5 ~$54 of own seats per game, Opus 4.8 $42, GPT-6.1 Sol $2.
- Bootstrap over side-swapped pairs (both games together); intervals from the analytic Fisher
  approximation run narrower than the bootstrap's.
- Per-lab trends halve the data per line; pool for the headline.

### Cleanup the user asked for (do when asked to resume work)
- Replace `--minions` + per-plan lists with built-in balanced Minion assignment (e.g. the plan
  generator assigns Minions per game, or the seed picks via a hash, not `seed % 4`).
- Move `scripts/fit.py`, `design.py`, `topup.py`, `ratings2026.py`, `build_ratings_page.py`,
  `resume_stopped.py` into the package (`clocktower/ratings.py`, `clocktower/allocate.py`, a
  `tournament --resume-stopped` option); drop `greedy*.json` intermediates.
- Model quirks into `MODELS` (e.g. a `can_disable_thinking` key instead of `ALWAYS_THINKS`).
- Prune `docs/plans/` (several superseded planning pages) and old plans; keep `f2-ratings.*` and the
  flagship page; refresh README for v17 and the per-game controls.
- Add v16/v17 games to the spectator viewer.

### Ideas for next experiments (rough priority)
1. Timeline back to 2024 (regenerated f1) so the chart spans GPT-4o → GPT-6.1 Sol.
2. More pairs among the 2026 top tier (Astra, Sol 6.1, Fable 5.1, Sol 5.6, Opus 5.5) to rank them, and
   enough per side to split detection from deception.
3. Memory ablation (reasoning carried vs replies only) on Opus 5.5 and Sol: measures the handicap of
   the replies-only older models.
4. One strong seat among weak ones (good and evil), and which evil role carries the team.
5. Mixed-model teams vs homogeneous (coordination without a shared mind), and in-group trust on mixed tables.
6. Human seats for a baseline (`play`).
7. Robustness: prompt paraphrase, Storyteller weight changes, same-seed replays.
8. Behavioural readouts from existing logs: lie detection rates, whisper networks, herding.
9. More trailers/clips for the video (the pipeline is in `media/`; pick games from the readers' lists).
The older brainstorm (22 ideas with mechanics: `--good-model A,B`, `--seat-model`, `MODEL@effort`) is
in git history of this file before Oct 4.

### User preferences seen in these sessions
- Wants an agent that watches runs, not brittle scripts; parallel subagents for reading games.
- Cares about realism first (rejected talk after the town square; chose one whisper per turn and 6 beats;
  dropped the public whisper log because it hurt evil).
- Budget-aware: set $5k for the top-up, approved finishing at ~$7.2k once told early.
- Wants single games killable/restartable, maximal parallelism, and no needless serial time.
- Plans a video about the experiment: trailers with ElevenLabs voices and real transcript lines.
