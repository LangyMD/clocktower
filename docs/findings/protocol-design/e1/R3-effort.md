# R3: reasoning effort, and whether "the same effort" is the same across labs

Snapshot 2026-09-30 ~06:15 UTC. Data: every `games/v9/e1-*/game-*` (60 games, 35 finished; both max-effort pairs
still running, at day 2-3). Probe calls are excluded. Effort comes from config.json (`good_effort`/`evil_effort`
for the side the model played). Scripts (scratchpad/readers/):
- `effort_stats.py`: thinking tokens per turn by model x effort (x side, x kind), writes `effort_tables.md` (full tables)
- `kinds.md`: the compact per-kind table · `zero.py`: zero-thinking beat turns · `loops.py`: repetition in summaries
- `sweep_probes.py`: per-game probe and vote metrics for the sweep · `deadmass.py`: P(Demon) put on dead players
- `seat.py GAME SEAT`: dump one seat's turns with thinking and output

## 1. Thinking tokens per turn

### Opus 5.5 vs GPT-6.1 Sol, at matched nominal effort (all e1 turns; each cell: Opus / Sol)

| effort | median | mean | Opus/Sol mean | p90 | p99 | zero-thinking turns | ceiling hits | $ per turn |
|---|---|---|---|---|---|---|---|---|
| low | 0 / 0 | 50 / 6 | **8.9x** | 180 / 17 | 342 / 61 | 62% / 85% | 0 / 0 | .009 / .003 |
| medium | 18 / 22 | 113 / 38 | **3.0x** | 324 / 94 | 892 / 266 | 50% / 32% | 0 / 0 | .012 / .003 |
| high | 50 / 137 | 175 / 242 | **0.7x** | 463 / 605 | 1747 / 1538 | 40% / 16% | 0 / 0 | .015 / .006 |
| max | 3952 / 866 | 5909 / 1315 | **4.5x** | 14837 / 2870 | 21434 / 6957 | 0% / 0% | 0 / 0 (Opus at 64K) | .22 / .020 |

Turns: Opus 323 / 620 / 3537 / 170; Sol 333 / 296 / 3043 / 313 (low / medium / high / max). Low and medium are one
side-swapped pair each; max is one unfinished pair each. The earlier 16K Opus-max pair lost one evil turn to the
ceiling (PROTOCOLS.md), so it was restarted at 64K; in the restart the longest turn so far is 40,417 thinking tokens
(463 s), so a 16K ceiling would have cut about 5% of Opus-max turns (p90 is 14.8K).

Shape of the effort curves:
- **Opus 5.5 is nearly flat from low to high, then jumps ~34x at max** (mean 50 → 113 → 175 → 5,909).
- **Sol rises steadily** (6 → 38 → 242 → 1,315, about 5-6x per step).
- So the labels do not match across labs. Opus thinks more than Sol at low (9x), medium (3x) and max (4.5x). At high
  Sol thinks a bit more (1.4x mean, 2.7x median). **High is the only level where the two are near token parity**, and
  only for this pair.
- Evil seats think more than good ones at every level (Opus max evil median 7.4K vs good 3.1K; Sol high evil 203 vs good 118).

### By turn kind (median / p90 / share with zero thinking)

| model @ effort | night | beat | nominate | comment | vote |
|---|---|---|---|---|---|
| Opus 5.5 @ low | 110 / 205 / 12% | 0 / 218 / 56% | 0 / 41 / 74% | 0 / 50 / 83% | 0 / 82 / 74% |
| Opus 5.5 @ medium | 122 / 143 / 25% | 105 / 574 / 23% | 0 / 65 / 73% | 0 / 98 / 70% | 0 / 49 / 80% |
| Opus 5.5 @ high | 124 / 403 / 17% | 132 / 638 / 19% | 0 / 151 / 64% | 0 / 119 / 67% | 0 / 71 / 73% |
| Opus 5.5 @ max | 13456 (n=2) | 5711 / 16487 / 0% | 416 / 965 / 0% | 116 / 261 / 0% (n=9) | (n=1) |
| Sol @ low | 0 / 45 / 56% | 0 / 30 / 78% | 0 / 0 / 94% | 0 / 0 / 100% | 0 / 0 / 100% |
| Sol @ medium | 19 / 95 / 29% | 32 / 102 / 16% | 0 / 44 / 71% | 18 / 84 / 32% | 0 / 41 / 68% |
| Sol @ high | 134 / 645 / 2% | 241 / 757 / 0% | 7 / 179 / 49% | 86 / 475 / 5% | 0 / 158 / 59% |
| Sol @ max | 516 / 1921 / 0% | 1333 / 3623 / 0% | 218 / 1007 / 0% | 674 / 1551 / 0% | 108 / 567 / 0% |

Adaptive-thinking Claude skips thinking on most nominate, comment and vote turns at low to high, and on 19-56% of
beats. Sol at high almost always thinks on beats (0.4% zero) and comments. At max, both think on every turn.

### Every model at high (for context; the headline chart compares these)

| model @ high | turns | median | mean | p90 | p99 | zero % | ceiling hits (16K) |
|---|---|---|---|---|---|---|---|
| Sonnet 4.5 (budget thinking, no effort) | 1456 | 356 | 405 | 710 | 1267 | 0 | 0 |
| Opus 4.5 (budget + effort) | 453 | 286 | 436 | 991 | 1933 | 0 | 0 |
| Opus 4.6 | 895 | 312 | 641 | 1752 | 4053 | 19 | 0 |
| Opus 4.7 | 327 | 248 | 518 | 1320 | 3131 | 20 | 0 |
| Opus 4.8 | 1049 | 380 | 1076 | 3016 | 9102 | 7 | 1 |
| Fable 5 / 5.1 | 265 / 1353 | 78 / 42 | 237 / 275 | 739 / 790 | 1839 / 3092 | 35 / 48 | 0 |
| Opus 5.5 | 3537 | 50 | 175 | 463 | 1757 | 40 | 0 |
| Sonnet 5.5 | 1269 | 0 | 139 | 393 | 1526 | 54 | 0 |
| o3 | 1118 | 1216 | 1959 | 4864 | 9108 | 1 | 0 |
| GPT-5.1 | 772 | 3158 | 3739 | 8098 | 14419 | 0 | 3 |
| GPT-5.2 | 695 | 840 | 1408 | 3758 | 7437 | 5 | 0 |
| GPT-5.4 | 1228 | 1378 | 1814 | 4140 | 7618 | 1 | 0 |
| GPT-5.5 | 1392 | 342 | 622 | 1552 | 3780 | 0 | 0 |
| GPT-5.6 Sol | 746 | 160 | 283 | 720 | 1673 | 0 | 0 |
| GPT-6 Astra | 1594 | 157 | 253 | 640 | 1540 | 17 | 0 |
| GPT-6 Sol | 632 | 198 | 357 | 926 | 1987 | 8 | 0 |
| GPT-6.1 Sol | 3043 | 137 | 242 | 605 | 1546 | 16 | 0 |

At "high", thinking varies ~20x across generations within each lab (GPT-5.1 mean 3.7K vs GPT-6.1 Sol 0.24K; Opus 4.8
1.1K vs Opus 5.5 0.18K). Newer models at high think far less. **So the label means different amounts of thinking
between models, not just between labs.** Note that GPT-5.1/5.2/5.4 and o3 (and Sonnet 4.5) have replies-only memory:
they re-derive the game each turn, which inflates their per-turn counts.

## 2. Does effort change play? (qualitative, plus probes)

### Outcomes and probes for the sweep (n = 1 side-swapped pair per cell; every cell is on a different seed)

| game | good | evil | days | winner | good P(Demon) on Imp | good Brier | good yes on evil / good nominees | evil executed / executions |
|---|---|---|---|---|---|---|---|---|
| opus55low/01 | Opus@low | Sol@high | 3 | good | .30 | .11 | .86 / .00 | 2/3 |
| opus55low/01-swap | Sol@high | Opus@low | 4 | good | .41 | .11 | .81 / .00 | 3/4 |
| opus55medium/01 | Opus@medium | Sol@high | 5 | evil | .11 | .19 | .38 / .24 | 1/5 |
| opus55medium/01-swap | Sol@high | Opus@medium | 3 | good | .23 | .17 | .88 / .38 | 2/3 |
| opus55-a/01 | Opus@high | Sol@high | 4 | good | .40 | .13 | .47 / .29 | 3/4 |
| opus55-a/01-swap | Sol@high | Opus@high | 3 | good | .67 | .05 | .83 / .00 | 3/3 |
| opus55-b/01 | Opus@high | Sol@high | 6 | evil | .08 | .27 | .28 / .49 | 1/5 |
| opus55-b/01-swap | Sol@high | Opus@high | 4 | good | .25 | .14 | .56 / .44 | 3/4 |
| opus55max64k/01 | Opus@max | Sol@high | running (d2) | - | .10 | .17 | - | 1/1 |
| opus55max64k/01-swap | Sol@high | Opus@max | running (d2) | - | .09 | .21 | - | 0/1 |
| sollow/01 | Sol@low | Opus@high | 3 | good | .34 | .09 | .86 / - | 3/3 |
| sollow/01-swap | Opus@high | Sol@low | 5 | evil | .14 | .23 | .57 / .57 | 1/4 |
| solmedium/01 | Sol@medium | Opus@high | 3 | good | .16 | .10 | .81 / - | 2/3 |
| solmedium/01-swap | Opus@high | Sol@medium | 2 | good | .26 | .16 | .31 / .25 | 1/2 |
| solmax/01 | Sol@max | Opus@high | running (d3) | - | .22 | .14 | .94 / .00 | 2/2 |
| solmax/01-swap | Opus@high | Sol@max | running (d3) | - | .08 | .24 | - / .78 | 0/2 |

No effort signal can be read from this. Low-effort teams won as good (Opus low, Sol low) and as evil (Sol low beat
Opus high in 5 days). The two high-vs-high pairs differ as much between themselves (seed a: good detection .40/.67;
seed b: .08/.25) as any effort cell does. Seed and setup dominate. Because every cell has its own seed, effort is
confounded with setup.

State tracking in probes: the share of good seats' P(Demon) put on already-dead players is 0% for Opus low, Sol low and
Sol max, and 0.6% / 0.0% for Opus / Sol at high (`deadmass.md`). There is no sign of forgetting at low effort.

### Reading the turns

- **Low effort does not visibly break play (medium confidence).** Example: Opus@low Empath Harper
  (`e1-opus55low-v-gpt61sol/game-01`). With 0 thinking tokens she opened with a correct private claim. With 85-322
  tokens she then correctly read her 0→2 flip as "Recluse flickering, Jules evil", used the seating
  (Jules-Alex-Blair) against the Chef 0 claim to move from Alex to Ellis as the Imp (correct), and pushed the town to
  execute Jules (a Minion), then Ellis (the Imp). The one slip was in a 57-token thought on day 3: "Alex claimed to
  protect me as Monk both nights, which lines up with me surviving", written after she had died. The action that turn
  was still right. Sol@low (`e1-gpt61sollow-v-opus55`) reasoned with almost no tokens (mean 6/turn) and still
  corrected others on the mechanics: dead neighbours don't count for the Empath (Alex), a Scarlet Woman can catch an
  executed Imp at 8 alive (Indigo). As good it executed three evils in a row, and as evil it won against Opus@high.
  Opus@medium had one clear state error: a dead Alex thinking "I'm dead now, killed by Gray" after being executed.
- **Max makes turns much more elaborate; whether it plays better is still unknown (low confidence).** Opus@max evil
  Spy Frankie (40K tokens, 463 s, one turn) worked through the whole Grimoire. The plan it produced was coherent and
  strong: frame the Saint, pick a false Empath number, tell the FT when to "ping" Gray, and list who the Imp must not
  kill (Ravenkeeper, Soldier, Mayor bounce). The Scarlet Woman (34K tokens) built on that plan. Visible output grows
  (median 150-205 tokens vs 93 at high: longer, denser whispers). But the max games are unfinished, and early probes
  for Opus@max as good are not better (P(Demon) on Imp .10).
- **No runaway reasoning in the sweep models (medium-high confidence).** There were no ceiling hits for Opus 5.5 or
  Sol at any effort (Opus max at 64K). The repeated 8-gram share in summaries is ~0 for every model; the only loop-like
  summaries are Sonnet 4.5 (max 22%). The ceiling hits in e1 at 16K were Opus 4.8 (1) and GPT-5.1 (3). All four were
  long, on-topic re-mappings of the claims ("overthinking"), not loops. The real cost of Opus max is time and money:
  median 44 s/turn (91 s for evil), ~$0.22/turn vs $0.015 at high (15x), about $27 by day 2 of one game, about an hour
  per game-day. Sol max is 3x high ($0.020/turn).
- **Matched effort, lab vs lab: I can't compare reasoning quality fairly, because the two labs' summaries differ in
  kind (see 3).** At high, both play competently. The two high-vs-high pairs split 3 good wins to 1, with similar probe
  numbers. Lab-level differences at matched effort are not detectable with this n.

## 3. Measurement caveats

1. **We see summaries, and they are not comparable across labs.**
   - Claude's summaries carry about 1.5 characters per thinking token. Raw text runs ~4 characters per token, so the
     summary is roughly 35-40% of the raw length and reads as real reasoning.
   - OpenAI "concise" summaries carry 0.14-0.24 characters per reasoning token (about 5%). At max they are pure
     headings: Sol max's 9,080-token turn is summarised as "**Analyzing complex role interactions**" repeated ~20 times.
   - So any qualitative audit finds Claude's mistakes far more easily than GPT's. Don't count reasoning errors from
     summaries across labs.
2. **Summaries add errors of their own.** In 21% of Opus@max turns (30 of 143) the summary uses non-Trouble-Brewing
   role names: "Werewolf" for Washerwoman (the model's own shorthand "WW" appears in its whispers), and "Seer" or
   "Ferryman" for the Fortune Teller. The rate at Opus high is 0.5%. No action output ever contains these words, so
   this is the summarizer, not the model. Don't read summary errors as reasoning errors.
3. **Token counts are the only direct measure, and they look internally consistent.**
   - For Claude, a turn with thinking_tokens = 0 never has summary text, and a turn with > 0 always does (2 exceptions
     in 3.5K). For Sol it is the same (7 nonzero turns with no summary).
   - Visible output (output − thinking) is similar across labs (~70-95 tokens median), so the counts are not
     obviously padded or hidden.
   - The tokenizers differ, which makes token parity approximate (~±15%).
4. **Zero thinking doesn't mean zero reasoning.**
   - At high, Opus's zero-thinking beats are mostly silent passes (67% say nothing).
   - At low, 56% of Opus beats and 78% of Sol beats have 0 thinking, yet most still speak: the median is 26 words
     (Opus) or 44 words (Sol), and only 34% (Opus) and 16% (Sol) of those turns are silent. Those turns are coherent
     (the Harper whispers above).
   - Both labs keep their earlier reasoning in context (memory "reasoning"), so a turn can rest on thinking done
     turns before. The written reply is itself reasoning.
   - So per-turn thinking tokens understate how much a model reasons, and more so for Claude's adaptive thinking.
     This is probably why low effort plays close to high: on a 12-player social game, most of the work is reading and
     writing, not search.
5. **The sweep design can't isolate effort.** Every cell is one pair on its own seed. The a/b high pairs show that
   seed-to-seed variation is larger than any effort effect seen here.

## 4. Recommendation for the headline comparison

- **Don't equate nominal levels across labs, and don't claim "same effort = same thinking" (high confidence).** The
  labels are defined per model. For Opus 5.5 vs Sol, "low" is 9x apart, "medium" 3x and "max" 4.5x. "High" is near
  parity only by coincidence, and across generations "high" ranges 20x within a lab.
- **For the headline, use one well-defined, reported policy and show that the rating doesn't depend on it
  (medium confidence).**
  1. Keep "high" for the headline, since it is the one already in all 60 e1 games. Frame it as "each model at its
     vendor's 'high'", not "equal thinking". Print the median/mean thinking tokens per turn and the cost next to each
     point, which PROTOCOLS already promises.
  2. Settle "each at max" with a proper effort-response check before adopting it. The roadmap's "each at its best"
     principle points to max, but max costs ~15x (Opus) / 3x (Sol) per turn and ~4-10x wall-clock, and it needs a
     64K ceiling for Claude, which breaks the "same per-turn ceiling" rule unless everyone gets 64K. It also has no
     demonstrated benefit yet.
- **Next step (high confidence that this is the right experiment):**
  - Rerun the sweep so that the same seeds are played at every effort level (paired design), with at least 5
    side-swapped pairs per level, for Opus 5.5 and Sol 6.1, against a fixed opponent at high.
  - Use the low-noise probe metrics (good P(Demon) on the Imp, Brier, vote accuracy) as the outcome, not win rate.
  - If ratings are flat from medium to max, which the current evidence weakly suggests from low to high, the headline
    is robust to the effort choice and "high" stands.
  - If max clearly helps one lab more, the headline should be "each at max" with a common 64K ceiling, and the
    effort-matched ratings shown as a secondary chart.
- **An alternative worth offering the user: match thinking tokens rather than labels (low confidence it's worth the
  complexity).** For example, pick per model the effort level whose median thinking per beat is nearest a common
  target. It is feasible only for models with graded levels, and a token isn't equally useful across labs, so it adds
  its own confound. I would report it only as a sensitivity check.
