# W1 / F1 harness check (engine, llm.py, game logs)

Scope: 50 v14 w1 games (41 finished when read, the rest running: o3 v Sonnet 4 and Sonnet 4.5 v GPT-5.4 are
at day 3–4) and 16 v13 f1 pilot games (6 finished, 10 killed). ~41K API calls. No games run, no repo edits;
unit tests pass (65/65). The analysis script is in the scratchpad (`an.py`).

## Verdict
The harness is sound. No game turn was lost in any game. Every low-effort retry (136) returned valid JSON.
There were no errors, no refusals and no trimming. OpenRouter JSON parsed 1693 of 1693 times. The rule
events are consistent. Fix five things before the flagship; the first one matters most.

## 1. Thinking, the 8K ceiling and retries (game turns, first attempt)
| model | think median | p90 | hit 8K | retry thinking (median) |
|---|---|---|---|---|
| gpt-5.1 (v13) | 3.0K | 8K | **11.7%** (13% of game turns; day 2: 18%) | **52 tokens** |
| gpt-5 (v13) | 3.6K | 6.6K | 4.6% | 1.0K |
| gpt-5.4 | 0.6K (v14) / 1.2K (v13) | 2.3K / 3.9K | 0.7–0.9% | 127 |
| o3 | 1.3K | 4.0K | 0.3% (v14) / 1.4% (v13) | 256 |
| o1 | 0.5K | 1.2K | 0 | – |
| Sonnet 4.5 / Opus 4.5 (budget) | 0.26–0.35K | 0.5–0.7K | 0 | – |
| Sonnet 4 / Opus 4.1 (OpenRouter) | 0.25K / 0.18K | 0.4K / 0.27K | 0 | – |
| Opus 4.6 / 4.7 | 0.3K | 1.3K / 1.7K | 0 | – |
| gpt-4o | 0 (no reasoning) | 0 | 0 | – |
| newer models (Opus 5.5, Sonnet 5.5, Fable 5.1, Sol, Astra) | 0–95 | 0.4–0.8K | 0 (Sonnet 5.5: 4 of 2,887) | Sonnet 5.5: 2.7K |

- Lost turns: none. The two capped calls with no retry are the last calls before the machine restart
  killed their games. One GPT-5.1 probe capped and then succeeded on retry.
- GPT-5.1 matters. About 1 turn in 8 (1 in 6 on day 2) is replayed at low effort with almost no
  thinking, and 27% of GPT-5.1's spend goes on capped attempts that are thrown away. The ceiling
  sets how GPT-5.1 plays; decide deliberately whether to accept that (v13 did).
- Bug (logging only): `self.low` is shared between a seat's game turn and its background probe, which
  run at the same time. The effort actually sent is correct, because the request is built before any
  await. But the effort written to the log is read after the await, so 6 records are wrong (game turns
  logged as `low` on attempt 0; a probe retry logged as `high`). Fix: compute the effort for each
  attempt in a local variable and pass it to `record`.

## 2. Context
- Largest input per call: Opus 4.7 63K, Opus 5.5 58K, Sonnet 5.5 60K, o3 33K, Sonnet 4 37K,
  GPT-5.x ≤ 23K (replies-only models carry less), gpt-4o 19K of its 128K. No model came within 30% of
  its window, so trimming never fired and was never exercised in a live game.
- Cache: 82–97% of input tokens are read from cache. Exception: Opus 4.6/4.7 rewrote their whole
  prefix on 9–10% of calls, because the 5-minute TTL expired while they waited on slow GPT-5/5.1 seats.
  A 1-hour TTL for Claude seats facing slow models would help a little (optional).

## 3. Latency, wall-clock and cost
| model | call latency median / p90 (s) | minutes per in-game day | $ per seat-day | est. $ per pair (11 seats × 3.7 days) | flagship matchups | est. total |
|---|---|---|---|---|---|---|
| o1 | 7.5 / 15 | 5–10 | **1.35** | **55** | 11 | **~600** |
| Opus 4.7 | 9 / 28 | (with GPT-5.1) 16–41 | 0.50 | 21 | 18 | 370 |
| Opus 4.1 (OpenRouter) | **26 / 42** (~250 output tokens) | (with GPT-5) 23–50 | 0.43 | 17 | 14 | 240 |
| gpt-5 | **55 / 111** | **25–55** | 0.40 | 16 | 15 | 245 |
| gpt-5.1 | **31 / 100** | 16–52 | 0.40 | 16 | 17 | 275 |
| gpt-5.4 | 17–33 / 56–91 | 11–37 | 0.31 | 12 | 19 | 235 |
| o3 | 13 / 37–45 | 8–31 | 0.20 | 8 | 12 | 100 |
| Sonnet 4.5 / gpt-4o / Sonnet 4 | 9 / 2 / 6 | 4–8 | 0.14–0.15 | 6 | 10–16 | 60–95 each |
| newer models | 3–8 / 7–19 | 3–17 | 0.07–0.40 | 3–16 | | |

- Modern pairs finish in 0.2–0.6 h. The GPT-5, GPT-5.1 and Opus 4.1 games are the long pole, at
  roughly 30–50 min per day, so 4–6 h for a long game even with every game running at once.
- Cost: the 17 models measured come to ~$3.5K; adding the 4 unmeasured models (GPT-5.2, 5.5,
  Opus 4.8, Fable 5) gives ~$4.5–5.5K, below the plan's $8.5K. This is rough, since it extrapolates from
  partial games. o1 is the largest line item: ~$6–7 per seat-game, lower than the $10 in CLAUDE.md.
  Probes are 7–17% of each model's spend.
- Untested: rate limits with 310 games at once, especially OpenRouter/Bedrock for Opus 4.1 and OpenAI
  for o1/GPT-5. The OpenAI/OpenRouter retry budget is ~4 minutes; after that the seat fails, the game
  stops, and it resumes from its last dusk.

## 4. Output quality
- JSON: no failures. OpenRouter gave 2 replies with prose before the JSON (parsed fine) and one
  misspelled key `whiskers` on a vote turn (harmless). No invalid names; no wrong field types.
- Whisper limit (v14): o3 once sent a second whisper, which was dropped with a notice. Sonnet 5.5 twice
  addressed 3 players, trimmed to 2 with a notice.
- Missing votes: Sonnet 5.5 six times and Sonnet 4.5 once returned `vote: null`. The engine's
  re-ask fixed every one.
- Speaking in private time: o3 did it in 7 turns (in f1, GPT-5 once). The text is dropped silently, and
  the speaker is not told, unlike dropped whispers. Consider adding a notice.
- **Identity tells survive the typography filter** (only one model per team, so each tell marks a team):
  - U+2011 non-breaking hyphen appears in 34% of GPT-5.1 messages and 17% of GPT-5 messages.
  - o3 uses bullets (•, 7%), arrows (↔ → ➔ ⇄) and emoji (keycaps, 👍).
  - `… [cut off]` appears only on o3 seats (2–5% of its messages; no other model goes over the word
    limit). Everyone sees the marker.
  - Fix: add U+2010–2012, U+00A0, U+202F, • and the arrows to `TYPOGRAPHY`, strip emoji, and show
    `[cut off]` only to the writer.
- Passing: Sonnet 5.5 sends no whisper on 60% of its private turns (Opus 5.5: 19%). This is behaviour,
  not a harness fault.
- o1 returned reasoning summaries on only 44% of calls, and o3 on 62%, although nearly every call had
  thinking tokens. That is a gap in the thinking records, not in play.

## 5. Game rules seen in these games
All consistent:
- 34 Slayer shots: the two misses on the Imp were both poisoned Slayers. Fake Slayers shot too.
- 8 Virgin triggers: every nominator was a Townsfolk.
- 14 Imp successions (starpass or Scarlet Woman).
- The Saint loss, ghost votes and vote thresholds all checked out.

Every evil win came by attrition ("two players remain") on days 5–6, and every good win by killing the
Demon on days 1–5. That is a game-balance question for the w1 readers, not a harness one.

## 6. Change before the flagship
1. **The plan still writes to `games/v13/f1`** (`plans/f1-timeline.json` → `out`). With v14 code:
   - `run` would keep the 6 finished v13 pilot games as finished flagship games, mixing protocols.
   - It would delete and replay the 10 killed ones (they have no checkpoints) inside a v13 folder.

   Regenerate the plan with `--out games/v14/f1` and fresh seeds. Better still, make `run` keep a
   result only when its `config.protocol` matches `PROTOCOL`. The v13 pilot games do not count toward
   a v14 flagship.
2. Extend the typography filter and hide the `[cut off]` marker from other players (above).
3. Decide on GPT-5.1's 13% capped turns, which near-zero-thinking retries replace, and note the choice
   in the protocol history.
4. Silent-pass risk: if OpenAI returns `failed`/`incomplete` for a reason other than length, or
   OpenRouter returns HTTP 200 with an error body, the call is retried up to 4 times and then the seat
   silently passes. It does not raise `SeatFailed`. This never happened here, but Bedrock via
   OpenRouter is in 27 matchups. Fixes:
   - Raise after repeated non-answers, or at least make `supervise` alarm on them.
   - Record OpenRouter's `provider` field.
5. Minor fixes:
   - Make the logged effort a per-attempt value (the `self.low` race).
   - `llm.py`'s docstring still says a truncated turn is "retried once at the same ceiling".
   - PROTOCOL says an unreadable turn is "retried once"; the code tries up to 4 times.
   - Optional: a 1-hour cache TTL for Claude seats that face slow models.
