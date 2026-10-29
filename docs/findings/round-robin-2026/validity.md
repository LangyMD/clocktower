# f2 validity check (109 of 110 games; f2-gpt54-v-gpt56sol/game-01 still running, day 4)

## Verdict
**Valid enough to scale, with three fixes first.** I found no engine bugs. Harness failures are small and
limited to two models, and I estimate they changed about one game at most. The data clearly shows
**two tiers**. The six models from Fable 5 (Jun 2026) on beat the five earlier ones in **53 of 59 cross-tier
games**: the newer tier is +364 Elo, 90% CI [+299, +471]. **Inside each tier the order is noise.** One pair
per matchup cannot order neighbours. The split detection and deception ratings are not interpretable yet:
there are only 10 binary games behind each, and the setup confounds them.

Fix first:
1. **Turns lost at the 8K ceiling (Opus 4.8).** The low-effort retry does not bound Opus 4.8's thinking.
   40% of its retries hit 8K again, so 76 turns were lost, all on the good side and late in games. Make
   the retry hard-bounded (a fixed thinking budget, if the API allows it for adaptive models), or raise
   the ceiling for everyone. That is the user's call, because it touches the equal-settings rule. GPT-5.4
   loses no turns, but on day 5 as good 21% of its turns are low-effort retries.
2. **The Minion rotation is broken: every game has a Poisoner.** The minion is `MINIONS[seed % 4]`, and the
   seeds are base 130000 plus 100 per matchup, so `seed % 4 == 0` every time. f1 (base 80000) has the same
   bug. Scaling to 4 pairs per matchup fixes this by itself: game-02 to game-04 get Spy, Scarlet Woman and
   Baron. Otherwise, change the seed stride, for example to 101.
3. **Report a combined rating (one skill per model) as the headline, and adjust for the setup.** When the
   second Minion is a Baron, evil wins 8 of 43 games. With a Scarlet Woman it wins 19 of 42, and with a Spy
   12 of 24. That is a good-side swing of about 370 Elo against roughly 0–70. Each model plays both sides of
   its own seeds, so setup luck moves rating from one of its columns to the other. Example: GPT-5.6 Sol's
   easy-for-good seeds raise its detection and lower its deception.

## 1. Engine and Storyteller: sound
I checked all 109 games with independent re-implementations, not the engine's own `valid` flags (those
are all true anyway).
- **Information.** I recomputed every info result from a role holder who was neither poisoned nor Drunk:
  Empath, Chef, Fortune Teller, Undertaker, Ravenkeeper, Washerwoman, Librarian, Investigator (339
  results). All 40 that differ from the plain truth involve a Spy registering as good or a Recluse
  registering as evil, which the rules allow.
  - Example: f2-fable5-v-fable51 Chef "2 pairs" comes from Recluse Frankie next to Baron Gray, plus Imp
    Indigo next to Poisoner Jules.
  - Healthy Fortune Teller results were right 84 of 84 times.
  - Poisoned or Drunk results were false about 64% of the time. That fits the 80% rule, given the Drunk's
    20% true-world games and cases where no false answer is possible.
- **Votes.** 703 vote results. The threshold always matched max(ceil(alive/2), previous block + 1), the
  yes-voter lists matched the individual votes, and block, tie and short outcomes were right. Each ghost
  vote was used at most once. Every execution went to the player on the block. All 21 Virgin triggers
  ended nominations correctly.
- **Deaths and endings.**
  - Every Imp kill that failed is explained: 11 Monk saves, 6 Mayor targets, 1 Soldier, 1 target already
    dead. A poisoned Soldier died correctly (f2-opus46-v-gpt54/game-01-swap, night 5).
  - All 109 endings match their stated reason.
  - The 4 Saint losses were all unpoisoned Saints.
  - In both games where good won with the Scarlet Woman alive, only 4 players were left, so she could not
    take over.
  - There was one Mayor win (3 alive, no execution).
- **Pairs.** Same-seed pairs get identical night-1 information, so the side swap works.
- **Restarts.** A container restart paused 44 games for about 3.5 hours each. They resumed from dusk
  checkpoints and the logs were cut back cleanly: no duplicated events, `seq` is monotonic, and
  conversations were restored.
- **No context trimming in any game.** The largest input was 178K tokens (Opus 4.8).
- **Day-1 wins look legitimate.** I read the 8 day-1 good wins. Five were informed Slayer shots, for example:
  - f2-opus48-v-opus55/game-01-swap: the Empath's "2 evil neighbours" leaves a 50/50 shot.
  - f2-opus47-v-astra/game-01-swap: Indigo: "Drew's information points that way… I'm shooting Casey".

## 2. Harness: small, concentrated in two models; probably decided at most one game
Game turns only. "Capped" means the first attempt hit 8K. "Lost" means the low-effort retry hit 8K too and
the seat passed.

| model | turns | capped | lost | notes |
|---|---|---|---|---|
| Opus 4.8 as good | 4653 | 184 (4.0%) | **76 (1.6%)** | capped 9% of day-4 turns, 13% of day 5; 40% of retries also cap |
| Opus 4.8 as evil | 1338 | 6 | 0 | |
| GPT-5.4 as good | 4490 | 235 (5.2%) | 0 | capped 21% of day-5 turns, so those were played at low effort; 34 of 551 probes lost (6%, late game) |
| Fable 5 as good | 5510 | 73 | 14 | 9 of the 14 in f2-fable5-v-astra/game-01, mostly by dead seats |
| Opus 4.6 / 4.7 / Fable 5.1 | – | 20–32 | 5 / 2 / 1 | |
| Opus 5.5, GPT-5.5, 5.6 Sol, 6 Astra, 6.1 Sol | – | 0 | 0 | |

- **No refusals.** About 39 replies were malformed JSON; all were retried successfully. No game stopped or
  logged an error.
- **"Silent" seats are a choice, not a failure.** Newer models leave 60–79% of their comment turns empty
  (Opus 5.5, GPT-6 Astra, GPT-6.1 Sol). Older ones leave 0–6% empty.
- **The lost Opus 4.8 turns are real reasoning, not loops.** In f2-opus48-v-gpt56sol/game-01, Blair (the
  Washerwoman) weighs "world A" against "world C" for 8K tokens. She loses all 6 private beats on day 3, and
  the low-effort retry is 9–11K characters long and also cut off.
- **Did the lost turns decide games?** Probably not, apart from about one game.
  - 74 of the 76 lost turns came in 6 games where Opus 4.8 was good against new-tier evil, and it lost all 6.
  - The other old-tier models lose that kind of game 18 times in 23 (78%). So about 4.7 losses were
    expected, against 6 observed.
  - The lost turns fall on days 3–5, and long games are the ones evil wins. Some of the correlation is
    simply game length.
  - Case read, f2-opus48-v-fable5/game-01: Logan (Investigator) lost all of day 4's private beats. He was
    already convinced, though, and led the fatal Saint execution in public ("execute ALEX… Hold the
    line"). The mistake was in his reasoning, not in silence.
  - Opus 4.8's probes are the worst of any model as good (mean Brier 0.285, against 0.08–0.23 for the
    rest), and towns read it best as evil (0.086). That points to skill.
- **Systematic risk.** The handicap grows with game length and hits the hardest turns. It will hurt any
  long-thinking model in the timeline run, and it explains why GPT-5.1 needed a 32K ceiling. GPT-5.4's
  probe scores are slightly flattered, because it loses late, hard probes.

## 3. Outcomes
- **Evil wins 39 of 109 (36%).** The fitted good-side advantage is +150 Elo. One side does not dominate.
- **By table size:** 10 players 13/35, 11 players 15/38, 12 players 11/36. Balanced.
- **By second Minion:** Baron 8/43 (19%), Scarlet Woman 19/42 (45%), Spy 12/24 (50%). Poisoner is in every
  game.
- **By Outsider count:** with 3–4 Outsiders evil wins 4 of 26.
- **Length:** good wins on days 1–6 (median 3). Evil wins almost all fall on days 5–6, and all but 4 come
  from "only two players remain" (the other 4 are Saint executions).
- **How good wins:** an executed Demon 61 times, a Slayer shot 8 times (5 of them on day 1), the Mayor once.
- **Cost:** $4.3k in total, $25 median per game (max $182). Median game length is 1.1 hours.

## 4. Ratings: tiers are solid, order within a tier is not
Records as good/evil, then my combined rating with a 90% bootstrap interval (resampling the 54 complete
pairs):

| model | good W | evil W | combined Elo (90% CI) | rank 90% |
|---|---|---|---|---|
| GPT-6.1 Sol | 9/10 | 7/10 | 1756 (1633–1922) | 1–4 |
| GPT-6 Astra | 10/10 | 6/10 | 1756 (1591–1912) | 1–5 |
| Fable 5 | 9/10 | 5/10 | 1665 (1587–1771) | 2–5 |
| Opus 5.5 | 7/10 | 6/10 | 1623 (1501–1754) | 2–6 |
| GPT-5.6 Sol | 9/10 | 3/9 | 1610 (1491–1752) | 2–6 |
| Fable 5.1 | 7/10 | 5/10 | 1581 (1488–1703) | 3–6 |
| Opus 4.6 | 5/10 | 1/10 | 1336 (1158–1506) | 7–11 |
| Opus 4.7 | 5/10 | 1/10 | 1336 (1181–1489) | 7–11 |
| GPT-5.5 | 3/10 | 3/10 | 1336 (1160–1466) | 7–11 |
| GPT-5.4 | 4/9 | 1/10 | 1305 (1170–1427) | 7–11 |
| Opus 4.8 | 2/10 | 1/10 | 1194 (994–1347) | 8–11 |

- **Release order holds at tier level.** Spearman correlation with release order: combined 0.80,
  deception 0.95, detection 0.63. Split-half reliability of the combined rating is about 0.8.
- **Pairs.** In 30 of 54 pairs the newer model swept. In 5 the older model swept, and in 19 each side won
  once (17 good–good, 2 evil–evil). Inside the tiers it is close to a coin flip: old tier 3 newer sweeps, 3
  older sweeps, 4 splits; new tier 4, 2 and 9.
- **Adjacent releases cannot be separated.** The bootstrap probability that each newer model beats the one
  before it ranges from 0.12 to 0.89. The one exception is Fable 5 over Opus 4.8, at 1.00.
- **Identical ratings are expected, not a bug.** In a single round robin, each rating depends only on a
  model's win count, so Opus 4.6 and Opus 4.7 get the same ratings in `analyze` (1397 and 1286) because
  their records are identical. The 1-pair ratings are just win counts.
- **The detection/deception split is mostly noise plus setup luck.** 90% intervals are about 310 Elo wide.
  Adjusting for the second Minion moves single ratings by 30–80 Elo (GPT-6.1 Sol detection 1681 → 1765,
  GPT-5.6 Sol detection 1709 → 1662). The only profiles that hold up in the bootstrap, and only weakly, are
  GPT-5.5 (evil better than good) and GPT-5.6 Sol (good better than evil).
- **Sample size needed.** Now the standard error of a difference between two models is about 120 Elo. To
  separate 100 Elo at about 2 standard errors needs roughly 6 times the games, which is about 6 pairs per
  matchup across the round robin. Cross-tier games are 90% predictable and carry little information, so
  spend new pairs **within tiers** (or within a release-order band), not on a full round robin.

## 5. Possible biases
- **Ceiling handicap.** See section 2. It falls on Opus 4.8 and GPT-5.4, both in the old tier, and could
  slightly overstate the gap between the tiers. The size is about one game.
- **Setup luck.** Each matchup has its own seed, and the seed shapes the outcome strongly (the Baron
  effect). Swap pairs cancel this for the combined rating but not for the detection/deception split. Add
  the setup as a covariate, or play more pairs.
- **Which model plays good first.** In game-01 the older model is always good. This cannot bias the pairs,
  because both orientations are played. Note it, though: game-01 evil win rate 32/54 against swap 7/55 is
  entirely newer against older, not an artifact.
- **Probe metrics.** GPT-5.4 loses 6% of its probes, all late, hard ones, so they look slightly better than
  they are. Probe Brier scores are also confounded by game length.
- **Lab pairing.** Claude good against GPT evil: evil wins 13/30. GPT good against Claude evil: 7/30.
  Watch this, but it fits the newer-model effect.

## Scale-up recommendation
- Fix the ceiling handling, so no turn is lost.
- Add pairs 2 to 4 for within-tier and near-neighbour matchups. That also completes the Minion rotation.
- Lead with the combined rating, adjusted for setup. Show detection and deception only once each model has
  at least about 40 games per side.
