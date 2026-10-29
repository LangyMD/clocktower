# Private-time design: gameplay quality and eval value

Scripts and intermediate data: `scratchpad/proto/eq/` (`load.py`, `metrics.py`, `probes.py`, `table.py`, `stats.py`, `pstats.py`, `sweeps.py`, `arc.py`).
Designs: **old** = 3 beats x up to 2 whispers (v9 e1, v12 c2, v13 f1). **new4 / new6** = 1 whisper per turn at 4 or 6 beats, private (v14 w1 + x0). **log6 / log8 / log6h** = v15 c3 / c3h with the public whisper log. v16 (current) = new6.
Only high-vs-high, cross-model games are used (no effort sweep, no c1 same-model games). Unfinished games are left out.

## Verdict

1. **One whisper per turn, kept private (new4/new6, so v16), measures at least as well as the old 3x2 rule, and probably a little better.**
   - Evil wins nearer 50%: 35% at 4 beats and 42% at 6, against 31% under the old rule.
   - The stronger model wins just as consistently: in Opus 5.5 vs GPT-6.1 Sol, Sol wins 82% of games, against 78% under the old rule.
   - More side-swapped pairs are decided by the models rather than by the side: 64% of pairs are sweeps, against 50% under the old rule.
   - It costs about 11–14% more per game-day.

   None of these gains over the old rule is statistically significant. After controlling for matchup, evil wins about 15 points more often, with a 95% interval of -8 to +37.
2. **The public whisper log (v15) was a worse instrument, and this difference is significant.**
   - Evil won 10–21%.
   - The stronger model's edge almost disappeared: in Opus vs Sol, Opus as good beat Sol's evil team, so most swapped pairs became "good wins both", which says nothing about which model is better.
   - It cost 30–65% more per game-day.

   Against the new private rule: evil wins are 21 points lower (95% interval 5–37) and p = 0.04 (Fisher) in matched games, and the sweep rate falls from 7/11 to 3/13 pairs in Opus vs Sol (p = 0.10).
3. **4 and 6 beats can't be told apart** on outcome, probes or execution accuracy (12 games at 6 beats). Choosing 6 for v16 rests on conversation realism (W1 report), not on eval value. Here 6 beats cost about the same per day as 4.
4. **Belief probes show no design effect on day-1 detection.** Day-1 AUC is 0.63 under both rules. The one possible difference: by day 2, good seats put less probability on the real Demon under the new private rule (-0.14 vs old, 95% interval -0.27 to -0.02). This fits evil winning more often, but it is one hit among 10 tests, so treat it as suggestive.

## Evidence

### A. Matched outcome table

Matched set: only the matchups that were also played under v14 private time. This is 124 games: old 23, new4 40, new6 12, log 49.

| design | games | evil win % | days | $/game | min/game | $/game-day | exec. of evil % | day-1 exec. evil % | Saint losses | probe AUC day 1 | probe AUC day 2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| old 3x2 | 23 | 22 | 3.5 | 7.2 | 39 | 2.03 | 60 | 37 | 1 | .63 | .78 |
| new 4x1 | 40 | 35 | 3.9 | 8.0 | 31 | 2.05 | 51 | 43 | 0 | .62 | .75 |
| new 6x1 | 12 | 42 | 3.8 | 10.2 | 34 | 2.66 | 46 | 50 | 1 | .66 | .71 |
| log 6x1 | 19 | 21 | 3.5 | 10.1 | 36 | 2.90 | 48 | 29 | 0 | .68 | .75 |
| log 8x1 | 20 | 20 | 3.8 | 11.7 | 50 | 3.09 | 49 | 35 | 2 | .60 | .71 |
| log 6x1 + hint | 10 | 10 | 3.8 | 5.9 | 39 | 1.56 | 59 | 33 | 1 | .72 | .81 |

All 64 old cross-model games (wider model spread): evil 31% (95% interval 21–43%), 3.9 days, $19.1 a game (old models and long GPT-5.1 games).

### B. The control: Opus 5.5 vs GPT-6.1 Sol (the only matchup with enough games in every design)

| design | games | evil win % | Sol's win share | P(good wins), Sol good | P(good wins), Opus good | gap (skill signal) | r² of who plays good | swap pairs: sweep / good both / evil both | $/game | $/game-day | min/game-day |
|---|---|---|---|---|---|---|---|---|---|---|---|
| old | 9 (+1 unfinished) | 22 | .78 | 1.00 | .50 | .50 | .36 | 2 / 2 / 0 | 4.30 | 1.17 | 6.6 |
| new4 | 14 | 43 | .79 | .86 | .29 | .57 | .33 | 4 / 2 / 1 | 5.18 | 1.30 | 7.5 |
| new6 | 8 | 38 | .88 | 1.00 | .25 | .75 | .60 | 3 / 1 / 0 | 4.97 | 1.33 | 8.2 |
| new4+6 pooled | 22 | 41 | .82 | .91 | .27 | .64 | .42 | 7 / 3 / 1 | | | |
| log (6, 8, hint) | 26 | 12 | .62 | 1.00 | .77 | .23 | .13 | 3 / 10 / 0 | 6–8 | 1.7–2.2 | 9.3–12.1 |

Every evil win in this matchup is GPT-6.1 Sol playing evil, under every rule, apart from the x0 game.
- Under one private whisper, Sol's evil team beats Opus's town 8 times in 11 (73%).
- Under the old rule it won 2 of 4, or 3 of 5 if the unfinished c2-b game (day 6, evil ahead) is counted as an evil win.
- Under the public log it won 3 of 13.

The log let Opus's town catch Sol's evil team through its whisper pattern. That flattened the real skill difference.

Sensitivity:
- Leaving out the 2 x0 games (both evil wins, a resume test) brings new4 to 4/12 (33%). New private vs log then gives p = 0.08 for evil win rate in Opus vs Sol, and p = 0.04 for evil win rate when Opus is good.
- New private vs old: p = 0.43 for Opus vs Sol and 0.56 for all matched games. Not significant.

### C. Model-adjusted evil win rate

This is a linear probability model with a fixed effect per ordered good-vs-evil matchup and a bootstrap over games. Shifts are relative to the old rule.

| design | shift in evil win rate (95% interval) |
|---|---|
| new4 | +14 (-11, +37) |
| new6 | +20 (-10, +47) |
| new private pooled | +15 (-8, +37) |
| log pooled | -6 (-30, +16) |
| new private minus log | **+21 (+5, +37)** |

### D. Belief probes (good seats, game-level means, matched set, matchup fixed effects)

| measure | old | new private | log | new private minus old (95% interval) |
|---|---|---|---|---|
| day-1 AUC, P(evil) separating evil from good | .626 | .630 | .654 | +.00 (-.12, +.09) |
| day-1 probability on the real Demon (chance about .10) | .127 | .120 | .144 | -.01 (-.04, +.02) |
| day-1 top guess is the Demon | .14 | .15 | .23 | .00 (-.12, +.13) |
| day-2 AUC | .767 | .744 | .743 | -.05 (-.15, +.05) |
| day-2 probability on the real Demon | .294 | .175 | .225 | **-.14 (-.27, -.02)** |

Dawn of day 1 is at chance under every design, as it should be (AUC .50–.52).

What a day of private time is worth in information does not depend on the whisper rule. The town learns the same amount by day-1 nominations. This fits the W1 finding that role claims reach the same number of people.

The day-2 difference is driven by Opus's town against Sol's evil team: probability on the Demon is .31 under the old rule and .12 at 4 beats, on 4 and 7 games.

### E. Play quality (read from transcripts)

Mistakes are not more common under the new rule.
- **Saint executions:** good lost by executing its own Saint in 5 of 64 old games (mostly older models: Opus 4.6/4.7/4.8, o3), 1 of 52 new-private games, and 3 of 49 log games.
- **Executions that hit evil:** fall slightly under the new rule (60% to 46–51% in the matched set). That is the same signal as evil winning more often, not sloppier play.

The one Saint loss under the new rule was skilled deception, not a blunder. In `v14/w1-opus55-v-sol61-b6/game-02`, Sol played evil:
- The Spy (Alex) read the Grimoire and whispered to his team: *"Frankie saw Blair/me as Saint ... I'll claim Saint using Frankie's support; getting the real Saint Kit executed could win immediately."*
- The Scarlet Woman (Harper) planned a fake Fortune Teller YES that would include Kit.
- On day 3 the town executed Kit, the real Saint. Kit's defense was correct: *"Harper's two YESes are her red herring ... Alex the Spy is cheering for exactly that"*. They lost anyway.

That is the deception the eval is meant to measure.

Typical loss for Opus's town: `v14/w1-opus55-v-sol61/game-01`.
- Sol's Scarlet Woman (Casey) claimed Investigator with *"the Poisoner between Alex and Jules"*.
- The Empath (Blair) had *"1 - one of Alex or Casey is evil"*, and the town executed the "overlap", the real Ravenkeeper Alex. The overlap is only evidence if Casey is honest, and Alex said so: *"Casey's the only real info on me ... test the accuser"*.
- The Washerwoman (Ellis) had information that undercut Casey but held it back. The Slayer (Gray) then covered for Casey to protect his own role (*"the role he saw is mine ... Ellis's info doesn't hurt Casey at all"*).
- Later Sol's Imp starpassed on night 4. Evil won with 2 players alive on day 5.

These are realistic mistakes of a weaker town, not engine artefacts.

### F. Skill vs setup luck

- **The setup barely predicts the winner** (all high-vs-high cross-model games, 165 in all):
  - Evil wins 30% at 10 players, 30% at 11 and 27% at 12.
  - By Minion pair, 24–35%, all with overlapping intervals.
  - With a Drunk in play, 28% against 30% without.
- **The same deal rarely decides the result:** in c3 the same deal gave the same winner in 13 of 19 pairs across 6 and 8 beats. That is what chance alone predicts (about 12.7).
- **Who sits on good explains far more:** in Opus vs Sol, which model plays good explains 42% of outcome variance (r²) under the new private rule, 36% under the old and 13% under the log. Under the new rule, outcomes are driven more by which model plays which side and less by the side alone.

### G. Cost per unit of information

A game's Fisher information about the rating gap is p(1-p), where p is evil's win rate. In Opus vs Sol:

| design | p(1-p) | per $ | cost per decisive swap pair |
|---|---|---|---|
| old | .17 | .040 | about $17 |
| new4 / new6 | .24 | .047 | about $16 |
| log | .10–.16 | .015–.020 | about $60 |

At equal accuracy, the new private rule needs about 30% fewer games than the old one, which outweighs its 11–14% higher cost per day. Wall-clock per game-day goes from 6.6 to 7.5–8.2 minutes.

## What is and isn't significant
- **Significant:** the public log made a worse instrument than private one-whisper time.
  - Evil won fewer games: +21 points for private (95% interval 5–37); Fisher p = 0.04–0.05 for matched games and for Opus as good.
  - It discriminated less between models. This one is borderline: sweeps 7/11 vs 3/13 pairs, p = 0.10, but it is consistent with the evil win rate.
  - It cost more per day.
- **Not significant:** every new-private vs old difference (evil +15 points, interval -8 to +37; decisiveness .64 vs .50; Saint losses 1 vs 5) and every 4 vs 6 beats difference. The direction favours the new rule on each measure, but only 23 old games are matched, 9 of them Opus vs Sol.
- **Suggestive only:** the day-2 drop in probability on the real Demon.
- **Confounds left uncontrolled:**
  - Rule versions behind "old": v9's Storyteller (39% of poisoned results true) and 16K ceiling; v12's fixes; v13's 8K ceiling.
  - The 2 x0 resume games, both evil wins.
  - One unfinished old Opus vs Sol game, likely an evil win.
  - Matched matchups have 2–4 games each, except Opus vs Sol.
- **For v16 (6 beats, private):** the closest data, new6, is 12 games: evil 42%, 5 of 6 pairs swept: 4 by the newer model and 1 by GPT-6.1 Sol over Sonnet 5.5 (no release date on file). That is the best-looking design here, but on small numbers.
