# W1: does v14 private time (one whisper per turn) tilt balance?

Snapshot at 23:39 UTC, Sep 30. In w1, 45 of 50 games have finished. The 5 still running are
fable51-v-astra game-02, fable51-v-astra-b6 game-01, both o3-v-sonnet4 games, and sonnet45-v-gpt54
game-01. The x0 resume test (Opus 5.5 vs GPT-6.1 Sol, 4 beats, v14, 2 games, both evil wins) is
reported separately. It is added to the "new4" per-matchup and behaviour tables and marked where it is.

Old-regime baseline ("old", 3 beats with up to 2 whispers per turn): every high-vs-high game in v9 e1
(48 games) and v12 c2 (12 games), 60 games in all. The effort-sweep games are excluded. 58 finished;
2 stopped (one on a transport error, one killed at day 3).

Caveat on the baseline: e1 ran v9 rules. Its Storyteller, its typography handling and its 16K
per-turn ceiling all differ from v14. c2 (v12) is the closest match, but it has only 10 finished
games (1 evil win). On its own, e1 is 18/48 evil (38%).

Scripts are in `scratchpad/w1.py` (per-game metrics), `agg.py` and `reg.py`.

## Verdict

**No detectable tilt in either direction.** Evil's win rate is about one-third under both regimes:
- Old: 33%.
- v14, 4 beats: 29% of finished games, about 32% once the running games are estimated.
- v14, 6 beats: 36%.

Both the matched and the model-adjusted comparisons put the effect near zero. But the 95% intervals
are about ±20 points, so a real shift of 10–15 points either way cannot be ruled out.

The premise behind the change is mostly not in the data. Under the old rules, good players did not
blast their claims to the whole town in private. The new rule cut the volume of day-1 whispering by
about a third, but role claims reached the same number of people. The "hive mind" forms in public,
in town square, and that part is unchanged.

## 1. Evil win rate

| set | games | finished | evil wins (95% Wilson CI) | if running games all go good / all go evil | estimate for running games* |
|---|---|---|---|---|---|
| old 3×2, all high-vs-high (e1+c2) | 60 | 58 | 19/58 = 33% (22–46%) | 32–35% | 34% |
| old, matchups also played in w1 | 20 | 19 | 5/19 = 26% (12–49%) | 25–30% | 30% |
| **v14 4×1, all w1** | 38 | 34 | **10/34 = 29% (17–46%)** | 26–37% | ~32% |
| v14 4×1, matchups also played in old | 30 | 28 | 8/28 = 29% (15–47%) | 27–33% | 31% |
| **v14 6×1 (-b6)** | 12 | 11 | **4/11 = 36% (15–65%)** | 33–42% | ~36% |
| v14 w1 all | 50 | 45 | 14/45 = 31% (20–46%) | 28–38% | ~33% |
| x0 resume test (4×1) | 2 | 2 | 2/2 | | |

\* Estimated from each running game's current state (alive count, evil alive, Imp alive). The
evil-win probabilities used are 0.3, 0.5, 0.6, 0.5 and 0.7, listed in `scratchpad/imp1.json`.

Censoring is small now: all Opus/Sol games have finished. Evil wins take about 5.5 days and good
wins about 3, so the unfinished games lean evil.

Model-adjusted and matched estimates of the regime effect:

| comparison | 4 beats vs old | 6 beats vs old |
|---|---|---|
| Matched by exact direction (same good model and same evil model): Mantel–Haenszel odds ratio | 1.25 (new 10/30 vs old 5/18; permutation p ≈ 0.5) | 3.0 (4/11 vs 3/12; p ≈ 0.5) |
| Logistic model with good-model and evil-model effects, finished games only | OR 0.89 (0.28–2.83) → 30% at a 33% baseline (12–58%) | OR 1.28 (0.21–7.8) |
| Same model, running games estimated from their state | OR 1.06 (0.37–3.04) → 34% (15–60%) | OR 1.38 (0.26–7.3) |

Win rate by direction (G = good wins, E = evil wins, with the day it ended). The "new4" row for
Opus 5.5 vs Sol 6.1 includes x0.

| good → evil | old | v14 4 beats | v14 6 beats |
|---|---|---|---|
| Opus 5.5 → Sol 6.1 | 2/4 evil (+1 stopped day 6) | **5/7** (w1 4/6, x0 1/1) | 3/4 |
| Sol 6.1 → Opus 5.5 | 0/5 | 1/7 (the x0 game; w1 0/6) | 0/4 |
| Sonnet 5.5 → Sol 6.1 | 1/1 | 1/2 | 1/1 |
| Sol 6.1 → Sonnet 5.5 | 0/1 | 0/2 | 0/1 |
| Opus 5.5 → Sonnet 5.5 | 0/1 | 1/2 | |
| Sonnet 5.5 → Opus 5.5 | 0/1 | 2/2 | |
| Fable 5.1 → Astra | 0/1 | 0/1 (+1 running) | (1 running) |
| Astra → Fable 5.1 | 0/1 | 0/2 | 0/1 |
| Sol 5.6 → Opus 5.5 | 0/1 | 0/2 | |
| Opus 5.5 → Sol 5.6 | 1/1 | 0/2 | |
| GPT-5.4 → Sonnet 4.5 | 1/1 | 0/1 | |
| Sonnet 4.5 → GPT-5.4 | 0/1 | (running, day 4, evil favoured) | |
| Opus 5.5 ↔ Astra (w1 only) | | Opus good 1/2, Astra good 0/2 | |
| GPT-4o ↔ Sonnet 4.5 (w1 only) | | 4o good 1/1, Sonnet 4.5 good 0/1 | |

**The good team's model matters far more than the regime.**
- GPT models as good lost 2 of 17 finished 4-beat games and 0 of 6 at 6 beats. Under the old rules
  they lost 7 of 31.
- Claude models as good lost 10 of 19 at 4 beats and 4 of 5 at 6 beats. Under the old rules they lost
  12 of 27.
- The Opus-good-vs-Sol-evil cell moved from 2/4 to 5/7. That is suggestive at most (n = 11).

Side-swapped pairs:
- Old: 9 good–good, 19 sweeps, 0 evil–evil.
- 4 beats: 7 good–good, 8 sweeps, 2 evil–evil. One is opus55-v-sonnet55 seed 90200, where the Imp
  bussed both Minions and survived on both sides. The other is the x0 seed.
- 6 beats: 1 good–good, 4 sweeps.

The first evil–evil pairs appear under v14, a weak hint of a little more evil equity. Under
independence, about 1–2 such pairs are expected in 17.

## 2. How games end and how long they last (finished games)

| | old | 4 beats | 6 beats |
|---|---|---|---|
| good wins: n, mean day | 39, 3.31 | 24, 2.96 | 7, 2.86 |
| evil wins: n, mean day | 19, 5.21 | 12, 5.50 | 4, 5.0 |
| evil wins by Saint execution | 5 of 19 | 0 of 12 | 1 of 4 |
| evil wins with two players left | 14 | 12 | 3 |
| good has won by end of day 3 | 21/59 (36%) | 18/40 (45%) | 6/12 |
| evil has won by end of day 4 | 3/59 | 0/38 | 1/11 |
| day-1 executions that hit evil | 17/50 (34%) | 15/35 (43%) | 5/10 |
| games with no day-1 execution | 10/60 | 5/40 | 2/12 |
| all executions that hit evil | 95/208 (46%) | 69/134 (51%) | 18/37 (49%) |

Every good win is a dead Demon.

Under v14, good catches the Demon a little earlier when it catches it at all. Otherwise evil still
wins the long attrition games (day 5–6). Neither difference is statistically meaningful. The drop to
zero Saint wins is probably noise: Saint wins need a Saint in play and a particular seed.

## 3. How fast information spreads (day 1)

Definitions:
- "Reveal" is a whisper by a good player that names their own shown character. It includes
  "Soldier, Fortune Teller or Undertaker"-style 3-for-3 offers.
- "Known" is the share of other good seats whose pre-nomination probe on day 1 names that player's
  shown character.

| per good player, day 1 | old (60) | old, matched (20) | 4 beats (40) | 6 beats (12) |
|---|---|---|---|---|
| whispers sent | 5.36 | 5.06 | 3.60 | 5.62 |
| recipient slots (sum of recipients) | 5.74 | 5.72 | 4.45 | 6.81 |
| distinct whisper partners | 3.65 | 3.71 | 3.21 | 4.51 |
| share of whispers to two players | 17% | 26% | 34% | 29% |
| **named own role in a whisper** | 80% | 84% | 81% | 89% |
| **distinct recipients of that role whisper** | 2.23 | 2.61 | 2.14 | 3.18 |
| named own role in town square on day 1 | 66% | 68% | 66% | 69% |
| has a claim at the day-1 probe | 94% | 95% | 98% | 100% |
| **other good seats who correctly name them before day-1 nominations** | 75% | 77% | 73% | 76% |

Cumulative share of good players who have named their role in a whisper, by the end of each private beat:
- old: 44%, 70%, 80%
- 4 beats: 51%, 63%, 78%, 81%
- 6 beats: 51%, 63%, 80%, 87%, 89%, 89%

**Reading.** Under the old rules, good players did not broadcast their roles in private. Each told
about 2.2 people, often as a 3-for-3; transcripts show the same cautious trading in both regimes.
v14 removed about a third of the day-1 whisper volume, but role claims reached the same number of
people, and the town's knowledge of good roles before day-1 nominations is unchanged (75% vs 73%).

The two-thirds of good players who claim publicly in town square on day 1 is identical in both
regimes. That public step is what makes the good team read as one mind. Six beats spread claims
further in private (3.2 recipients, 89%) but not in the probe (76%).

The breakdown by good model tells the same story. Opus 5.5 as good reached 2.2 people with its role
under the old rules and 2.0 under v14, and was known to 82% and 79% of the other good seats. Sol 6.1
reached 3.3 and 3.0 people, known to 72% and 71%.

Good's P(Demon) on the real Imp before nominations (mean per game, ±95%):

| day | old | 4 beats | 6 beats |
|---|---|---|---|
| 1 | 0.12 ± 0.02 (60) | 0.11 ± 0.02 (40) | 0.13 ± 0.03 (12) |
| 2 | 0.24 ± 0.05 (54) | 0.17 ± 0.05 (38) | 0.16 ± 0.08 (11) |
| 3 | 0.27 ± 0.08 (46) | 0.28 ± 0.11 (31) | 0.22 ± 0.18 (10) |
| 4+ | 0.37 (62 game-days) | 0.27 (32) | 0.37 (7) |

Day-1 reads are identical. Day 2 is somewhat lower under v14 (−0.07, borderline). Day 4+ values are
selection-affected: they come from the games the Imp survived.

Other day-1 measures:
- Brier score for good seats: 0.21 old, 0.20 at 4 beats, 0.20 at 6 beats.
- Good players' yes votes on evil nominees: 58% old, 68% at 4 beats, 76% at 6 beats.
- Good players' yes votes on good nominees: 33%, 30% and 31%.

On these, good votes slightly better under v14, which matches the higher rate of executions hitting evil.

## 4. Evil coordination

| | old (60) | 4 beats (40) | 6 beats (12) |
|---|---|---|---|
| Imp in contact with both Minions in private beat 1 | 56 | 39 | 12 |
| … by the end of day-1 private time | 59 | 40 | 12 |
| Imp sends one whisper to both Minions together | 51 | 39 | 12 |
| **share of evil whispers in beat 1 that go only to teammates** | 62% | **97%** | 100% |
| share of evil whispers on day 1 that go only to teammates | 45% | 46% | 33% |
| distinct good players each evil whispers on day 1 | 2.51 | 2.33 | 3.75 |
| good players who hear each evil player's bluff by whisper on day 1 | 1.61 | 1.76 | 3.33 |
| other good seats who name each evil player's claimed role at the day-1 probe | 66% | 64% | 75% |
| evil–evil claim collisions (pairs) | 1 | 0 | 0 |
| games where evil claimed a character a good player holds | 6 (7 claims) | 7 (8) | 2 |

Coordination survives intact. The Imp still briefs both Minions in beat 1 with a single two-person
whisper, in 39 of 40 games (37 of 40 in the Imp's own beat-1 turn). The cost is that all three evil
players spend their first beat entirely on the team conference: 97% of their beat-1 whispers are
team-only, against 62% before. Evil's reach to good players over the day is unchanged all the same
(2.3 vs 2.5 good partners; bluffs heard by 1.8 vs 1.6 good players), because the extra beat makes up for it.

There are no evil–evil collisions under v14. Claiming a character a good player holds is about as
common as before. Some of these claims are deliberate: in b6 game-02, evil claimed Saint over the
real Saint, and the town then executed the real Saint.

## 5. Four beats vs six beats

With 6 beats, private time roughly doubles in volume:
- 5.6 whispers per good player.
- 89% reveal their role, to 3.2 people.
- Evil reaches 3.75 good players, and 3.3 good players hear each evil bluff.

Evil wins 4/11 at 6 beats vs 10/34 at 4. In the only matchup run under both, Opus good vs Sol evil
went 3/4 at 6 beats and 4/6 in w1 at 4 beats, and Sol good vs Opus evil went 0/4 and 0/6. **No
detectable difference.** The extra private time boosts both sides' information flow symmetrically,
and it costs about 30% more private-time spend. The data gives no balance reason to prefer 6 beats
over 4.

## 6. What would settle it

- **Same-seed replay.** Rerun the w1 seeds with identical matchups under v13's 3×2 rule. There is
  no whispers-per-turn flag today: `--private-beats 3` alone gives 3×1, so the old rule needs the
  v13 code or a small flag. That gives a within-seed paired
  comparison and removes setup and seating luck, which is the dominant noise here (for example, seed
  90200 went evil both ways).
  - Concentrate it on the matchups near 50/50, such as Opus 5.5 good vs Sol 6.1 evil; the GPT-good
    cells sit at the good-wins ceiling and carry no information.
- **Sample size.** An unpaired design needs about 165 games per arm to detect a ±15-point shift and
  about 365 per arm for ±10 points. Pairing on seeds should cut this substantially (perhaps to 60–100
  seed pairs per arm for ±15 points).
- **Secondary outcomes.** Use the low-noise measures from the probes: day-2 P(Demon) on the Imp,
  day-1 execution accuracy, and day-1 claim knowledge. The day-2 P(Demon) drop (0.24 → 0.17) is the
  one behavioural hint of an evil advantage worth checking.
- **Finish the running games.** The 5 unfinished w1 games involve older models (o3, Sonnet 4/4.5,
  Fable 5.1 vs Astra). With no old baseline for o3-v-sonnet4 or gpt4o-v-sonnet45, they cannot move
  the matched comparison.
