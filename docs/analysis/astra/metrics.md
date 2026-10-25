# Why GPT-6 Astra wins: behaviour metrics

372 finished games (v16 f2 + v17 f3/f3b), 26 with Astra on each side. Each model's numbers are averaged over its
games, each game counting once. Brackets are rough 90% bootstrap intervals over games. "Adjusted" means the
value minus the average for the same opponent against everyone else. That removes most of the difference in
who each model happened to face. Scripts are in the session scratchpad (`extract.py`, `aggregate.py`,
`extra.py`, `extra2.py`, `topsuspect.py`, `evilside.py`, `invpair.py`). They make no API calls.

## The answer

**As good, Astra finds a Minion on day 1 and keeps its votes off good players.** Its reads of who the Demon
is are no sharper than GPT-6.1 Sol's.
- At day-1 nominations, the player Astra's town rates most likely evil really is evil 87% of the time. That
  is 20 of 23 games, and 18 of the 20 were Minions. Sol 6.1 manages 53% and the field about 45%.
- So Astra's day-1 executions hit evil 57% of the time, against 34% for Sol 6.1 and 37% for everyone else.
- In each day's votes, Astra's good players vote for a good nominee 15% of the time; the field does so 31%.
- Measured by the belief probes, Astra's town is no surer about the real Demon than Sol 6.1's: mean P(Demon)
  is 0.32 vs 0.33 on day 2. What Astra does better is finding *an* evil player early and not being fooled
  about who is good.

**As evil, Astra keeps the town off its whole team, and it does so cheaply.**
- The town executes evil players 19 points less often against Astra than its usual rate. Against Sol 6.1 the
  drop is 13 points.
- On day 1, towns hit evil 15 points less often than usual against Astra. Against Sol 6.1 they do no worse
  than usual (+5).
- Astra's evil players nominate their own Minions more than any other model does: 30% of evil nominations
  (field 16%). They avoid Minion deaths anyway: 0.96 Minion executions per game, the fewest of any model
  (field about 1.15).

**Several traits are shared by the whole GPT-6 family, so they cannot explain Astra's lead over Sol 6.1:**
- Astra and Sol 6.1 pass 28–39% of town-square turns; GPT-5.6 Sol passes 12% and the rest 1–20%.
- They speak in short public messages, about 37 words.
- They whisper to two players at once (68% as evil, vs 44% for the field).
- As good, they let the Demon's P(Demon) rise faster than other models do.
- As evil, they keep their Demon's P(Demon) low: 9 points below what the same town usually gives a Demon on
  day 2.

**None of these explain it either:**
- Thinking effort: Astra writes the *fewest* output tokens per turn of any model (236 as good, 299 as evil,
  against a field average of about 700 and 620). It never hit the output ceiling and lost no turns.
- How often good players claim a character publicly on day 1.
- Evil kill targets: 47% of Astra's kills hit a player who had claimed an info role, against 46% for the field.
- Setup: Astra's games have a normal mix of Minions and table sizes (Poisoner 10, Spy 5, Baron 6, Scarlet
  Woman 5; 11.2 players on average). As good it won all 26, so no setup term can matter there.

## The table

| Metric | Astra | Sol 6.1 | GPT-5.6 Sol | All non-Astra |
|---|---|---|---|---|
| **Good side** (n games) | 26 | 35 | 56 | 346 |
| Wins (opponent-adjusted) | 100% (+0.33) | 91% (+0.23) | 82% (+0.14) | 65% |
| Town's top suspect (highest mean P(evil), alive) is evil, all nomination probes | **0.92** [0.87, 0.96] | 0.72 [0.63, 0.80] | 0.63 [0.57, 0.69] | 0.56 [0.53, 0.58] |
| Same, adjusted for the evil model faced | **+0.32** [+0.27, +0.37] | +0.13 [+0.05, +0.20] | +0.05 [0.00, +0.11] | – |
| Same, at day-1 nominations only | **0.87** (n=23) | 0.53 | 0.36 | ~0.45 |
| Executions that hit evil, all days | **0.78** [0.70, 0.86] | 0.68 [0.61, 0.76] | 0.59 [0.53, 0.65] | 0.51 [0.49, 0.54] |
| Day-1 executions that hit evil | **0.57** [0.39, 0.74] | 0.34 [0.22, 0.50] | 0.31 [0.22, 0.42] | 0.37 [0.32, 0.41] |
| Good players' yes votes on good nominees | **0.15** [0.09, 0.21] | 0.18 [0.13, 0.24] | 0.23 [0.20, 0.27] | 0.31 [0.30, 0.33] |
| Good players' yes votes on evil nominees | 0.69 | 0.67 | 0.59 | 0.58 |
| Good nominations that name an evil player | 0.77 | 0.70 | 0.62 | 0.59 |
| Town's mean P(Demon) on the real Demon, day 2 | 0.32 [0.24, 0.41] | 0.33 [0.25, 0.42] | 0.22 | 0.20 |
| Days to finish (good games) | 2.8 | 3.1 | 3.8 | 4.0 |
| **Evil side** (n games) | 26 | 35 | 56 | 346 |
| Wins (opponent-adjusted) | 62% (+0.30) | 49% (+0.18) | 34% (+0.01) | 30% |
| Town's executions that hit evil, adjusted for the good model | **−0.19** [−0.26, −0.12] | −0.13 [−0.20, −0.06] | −0.05 | – |
| Same, day 1 only | **−0.15** [−0.29, 0.00] | +0.05 [−0.09, +0.18] | −0.15 | – |
| Town's P(Demon) on the Demon at day 2, adjusted | −0.09 [−0.13, −0.04] | −0.09 [−0.11, −0.06] | +0.01 | – |
| Evil nominations that name their own Minion | **0.30** [0.19, 0.43] | 0.19 | 0.15 | 0.16 |
| Minions executed per game | **0.96** | 1.14 | 1.14 | ~1.15 |
| **Style (both sides, family traits)** | | | | |
| Town-square turns passed (good / evil) | 31% / 39% | 28% / 38% | 12% / 11% | 9% / 11% |
| Words per public message (good) | 37 | 38 | 41 | 50 |
| Whispers sent to two players (evil) | 68% | 67% | 48% | 44% |
| Output tokens per turn (good / evil) | **236 / 299** | 259 / 329 | 304 / 268 | 704 / 620 |

## Notes and surprises

- **Most of Astra's day-1 hits are Minions, not the Demon.** Only 2 of its 20 correct day-1 top suspects were
  the Imp. Elsewhere, wrong day-1 top suspects are mostly good players with claims nobody can check
  (Ravenkeeper, Mayor, Monk, Undertaker, Soldier). Astra's town almost never suspects those: only 3 of its 23
  day-1 top suspects were good. Its top suspect is also no more confident than Sol 6.1's (mean P(evil) 0.60
  for both), so the difference is *which* player tops the list, not how hard the town believes it.
- **Astra does not just follow the Investigator.** Across the field, a day-1 execution usually lands inside
  the Investigator's pair, with hit rates of 44–86%. Astra executed inside that pair less often (7 of 14
  games where an Investigator was in play). When no Investigator was in play it still hit evil on day 1 in 8
  of 9 games; every other model managed 5–38%. The sample is tiny, but whatever Astra uses on day 1 is not one
  role's ping. Checking claims against each other in whispers is the likely source. Astra has the highest
  whisper reply rate as good (46%, field 38%), but that difference is small. A transcript reader should pin
  this down.
- **Astra's executions follow its town's belief less closely than other models' do.** Only 64% of Astra's
  executions hit the town's top P(evil) player, the same as Sol 6.1 and GPT-5.6 Sol; most other models are at
  75–84% (Opus 4.8 is lower, at 53%). Yet the GPT models are right more often. The mean probe flattens disagreement between seats, so the
  likely reading is that Astra's seats coordinate on a lead in whispers, not by consensus.
- **Sol 6.1 is the better Demon-hider on day 2.** Against Sol 6.1 evil, the town's top suspect on day 2 is the
  Demon 22 points less often than usual; against Astra, 7 points less. Astra's edge as evil is protecting the
  *whole team*: fewer Minion executions, and towns going wrong on day 1. It is not about concealing the Demon.
- **Astra's evil players nominate their own Minions often (0.46 per game) and still lose fewer Minions.** This
  looks like cheap credibility: a nomination that seldom passes (half did), not a real bus.
- **Head to head with Sol 6.1:** Astra-good won 4 of 4; Sol-good won 2 of 4. That is too few games to say more.

## Caveats

- 26 games per side; the day-1 numbers rest on 23 probe points and 14–23 executions. Intervals overlap
  Sol 6.1's on most single metrics. The top-suspect gap (+0.32 vs +0.13 adjusted) and Astra-good's 100% win
  rate are the clearest signals.
- Public claims are detected with a regex for "I'm (the) X"; it misses forms like "On record: Investigator",
  so claim rates are undercounts (applied the same way to every model).
- The town's belief is the mean over good seats, so it mixes accuracy with agreement between seats.
- Metrics were chosen from the list in the brief; I computed about 40 and report the ones that separate models.
  Treat the weaker ones (reply rate, kill targets) as descriptive.
