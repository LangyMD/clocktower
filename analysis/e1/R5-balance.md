# R5: balance and meta in v9 e1

Data: the 38 of 60 e1 games that had `result.json` at about 06:15 UTC (runs still going; 22 unfinished).
Close reads (public replays plus evil probe plans): fable5-v-opus47 (both games), gpt56sol-v-opus55
(both), opus48-v-gpt56sol swap, opus48-v-astra swap (skim), gpt55-v-fable51 (both, skim),
opus46-v-gpt55 swap (final day), sonnet55-v-gpt61sol (both), opus55-v-gpt61sol-b game-01. I also
ran `analyze` and my own scripts over events.jsonl and probes.jsonl.

## 1. Win rates and how games end

- **Evil won 9 of 38 (24%; 95% CI about 12–40%).** That matches v7 c1 (9/40, 23%), is below v6 g1
  (31/100) and above v8 t2 (1/36). It sits inside the PROTOCOLS "good wins ~70–80%" band.
- **This number is biased toward good (high confidence).** Good wins end early: days 1–4, mean
  about 3.2. Evil wins end late: day 3 once, the rest days 5–7, mean about 5.6. The unfinished games
  are the long ones (many are on day 4–5, with 3–5 good players already executed), so the final
  evil rate will probably rise. Don't quote e1 balance until the batch is done.
- **By table size:** 10 players 2/12, 11 players 4/16, 12 players 3/10. Mean days 3.5 / 3.7 / 3.8.
  No detectable size effect.
- **By relative strength** (release order from the t1/t2 timeline; GPT-6 Sol, Sonnet 5.5 and GPT-6.1
  Sol treated as newest): evil newer than good 7/15 evil wins; good newer 2/23. By model:
  GPT-6.1 Sol (any effort) won 4 of 8 as evil. Opus 5.5 (any effort) won 1 of 9 as evil, and that one
  was against Sonnet 4.5. That gap is suggestive only (Fisher p ≈ 0.13).
- **How games end:** 29 good wins. 26 were the Demon executed; 3 were a Slayer shot on the Imp (days
  1–3). 9 evil wins: 7 "two players left" and 2 Saint executions.

## 2. Why good wins, why evil wins

**Good wins mostly by solving on shared information, helped by evil slips. I found no engine
artifacts.**
- Executions hit evil 66/129 times (51%) against a base rate of about 27%. Day 1: of 24
  non-Virgin executions, 12 were evil (50%).
- What drove the 12 day-1 evil hits (from the nomination texts):
  - Investigator pings: 5.
  - Outsider-count conflicts caused by an evil Outsider bluff: 3–4.
  - Empath or Fortune Teller reads, including seating luck like an Empath 2 on two evil
    neighbours (opus48-v-gpt56sol swap): several.
  - Double claims of in-play roles: 2. Both came from older evil models (Opus 4.5, 4.8, o3, Sonnet
    4.5). About 80% of evil day-1 claims are the Demon's bluffs, so newer models rarely collide.
- Evil slips I saw:
  - Private stories that don't match, surfaced by good players comparing notes in public
    (Indigo "Townsfolk" to Jules, then Butler in public; Kit's retracted Washerwoman ping).
  - An evil team voting as a bloc to save its Imp (fable5-v-opus47 game-01, Imp executed day 1).
  - An Imp killing the Fortune Teller who had just asked it (a fake Monk) for protection
    (gpt56sol-v-opus55 game-01).
  - Evil did bus teammates. Evil voters voted yes on evil nominees 46% of the time, against 73% on
    good nominees. So bloc voting is not systematic.
- Good's tools are used well:
  - 10 real Slayer shots: 4 aimed at the Imp, 3 hit, 1 was poisoned.
  - Virgin tests in 10 of the 16 games with a Virgin (9 on day 1).
  - Undertaker confirmation, Chef-pair elimination, and counting Townsfolk slots ("9 Townsfolk
    claims for 7 slots").
- Weak good teams lose to reasoning loops. Sonnet 4.5 (replies-only memory) repeated one false
  premise about 20 times over days 5–6: "poisoned Librarian info must have some connection to
  reality".

**Evil wins are earned deception, not luck.** Examples:
- A Spy claiming Chef reported the true "1", which sold out its Imp and Baron to gain trust. The Imp
  then starpassed to the Spy, and the town executed the real Saint as the "fake Outsider"
  (gpt56sol-v-opus55 swap).
- An Imp claiming Undertaker gave a false "Poisoner" result on the real Investigator, then the town
  executed the Mayor (opus55-v-gpt61sol-b).
- A Poisoner posing as Washerwoman framed the Saint with a Virgin ping (fable5-v-opus47 swap).
- Scarlet Woman catches and starpasses to trusted Minions (starpass or Scarlet Woman in 5 of the 7
  attrition wins).
- A self-outed Poisoner "defending" good players so the town executes them (sonnet45-v-opus55).

## 3. Meta diversity: one script, with variation in the middle game

- **Everyone hard-claims on day 1.** 363 of 372 seats (97.6%) have a claim at the day-1
  pre-nomination probe. Private time is claim trading ("3-for-3"); public claims follow in town
  square 1–3. Opening lines repeat across games: "I've heard three Outsider claims privately",
  "Librarian, if you exist, speak up", "the spent Washerwoman should test the Virgin".
- **The setup dictates evil's claims.** With 3 bluffs for 3 evil players, 78% of evil day-1 claims
  are bluffs. In 6 of 14 complete pairs, two different evil models chose the identical claim
  assignment. In both gpt56sol-v-opus55 games, the Baron claimed Slayer and fake-shot its own Imp.
  Variety comes later: starpass timing, bussing, fake results, final-three play.
- **Consensus herding.** On nominations that reached the threshold, yes votes averaged 91% of the
  living count (ghost votes included), and 22% were unanimous. In homogeneous teams, many players
  post near-identical lines ("No on Alex. Keep Kit on the block."), and dead players coordinate
  ghost votes as a bloc (opus46-v-gpt55 swap, final day).

**What makes this easier for good than human play** (medium confidence):
1. Universal, honest day-1 claims make counting constraints (Outsider count, Baron detection,
   Townsfolk slots) nearly exact. Good almost never bluffs in public.
2. A single-model good team is a hive: little infighting, fast convergence, perfect recall and
   cross-checking of every private claim.
3. Storyteller policy: in Baron games the bluffs usually include an Outsider. An evil player claiming
   an Outsider bluff pushes the count over what a Baron allows unless a real Outsider is hidden (the
   Drunk). Evil Outsider claimers were executed on day 1 in 5 of 20 cases, against 8 of 100 for
   Townsfolk claimers (low–medium confidence, small n).

Things favour evil relative to humans too: whispers are fully invisible, the evil team coordinates
perfectly, and the Spy sees the whole Grimoire. Otherwise I found no leaks or engine artifacts.
Models rarely reason about the scripted Storyteller or about other players being AIs (one Opus 5.5
aside).

## 4. Table size 10–12

Worth keeping (medium confidence):
- It varies base Outsiders (0/1/2) and so the counting puzzle.
- Every size keeps two Minions (two-Minion play, Scarlet Woman catches, starpass choices).
- No size effect is visible (2/12, 4/16, 3/10).

The cost: with one pair per matchup, size is confounded with matchup. Each size also changes how many
evil claims can hide, which adds variance between matchups.

## 5. Rating design

- **Side-swapped pairs work.** 16 pairs are complete: 7 good–good, 9 sweeps (one model won both
  sides), 0 evil–evil. 8 of the 9 sweeps went to the newer or same-generation model (sign test
  p ≈ 0.02). The exception: GPT-5.6 Sol over Opus 5.5.
  - GPT-6.1 Sol accounts for 4 sweeps, at low effort too.
  - So win/loss does separate models, and the swapped pair removes setup and seating luck. Evidence:
    one seed had an Empath 2 on two evil players; another had the same fake-Slayer script on both
    sides.
- **It is data-starved.** 44% of pairs are good–good ties, which carry almost no information. With
  one pair per matchup, the Bradley–Terry output is mostly prior: gpt-5.2 1542, o3 exactly 1500.
- **The effort sweep can't be read yet.** Opus low tied Sol high, Opus medium was swept, and Sol low
  swept Opus high.

## Recommendations

1. Report e1 balance and ratings only after all 60 games finish. Finished-so-far is short-game
   biased. (High confidence.)
2. For ratings, play at least 5 pairs per matchup. Give each matchup all three table sizes (e.g. 3
   or 6 pairs), or add size as a covariate. Prefer anchor matchups where evil is stronger than good,
   so outcomes land near 50% instead of at the good-wins ceiling. (High confidence.)
3. Lean on the probes as a low-noise second measure. Probe demon% ranges from 6% to 69% across
   pairings, and it separates strong detection (Astra good at 69% against o3) where win/loss
   saturates. (Medium confidence.)
4. Keep the rules. Balance is in the intended range and evil's wins come from real deception. If more
   evil equity is wanted, the cleanest lever is the Storyteller's Outsider-bluff weighting in Baron
   games, e.g. an Outsider bluff only when a Drunk is in play. That is a judgement call; check it in
   `sim`. (Low–medium confidence.)
5. Treat the day-1 hard-claim and Virgin-test script as a known property of LLM play. It makes good
   more mechanical than in human games; mention it in any write-up rather than engineering it away.
   (Medium confidence.)
