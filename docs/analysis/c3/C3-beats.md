# c3: 6 vs 8 private beats (v15, public whisper log)

Data: 19 finished games at 6 beats (b6) and 20 at 8 beats (b8), on the same deals (10 seeds, side-swapped).
`c3-sonnet45-v-gpt54-b6/game-01-swap` was still running (day 3, last event a few minutes before this read), so it is excluded;
matched comparisons use the 19 complete pairs. Scripts are in the scratchpad (`load.py`, `outcomes.py`, `talk.py`, `probes2.py`, ...).

## Headline findings

1. **Outcomes are the same.** Evil won 4/19 at 6 beats and 4/20 at 8. Only one evil win falls on the same deal in both arms (sonnet45-v-gpt54/game-01).
   The same deal gave the same winner in 13/19 pairs, which is about what chance predicts at a 79% good-win rate (~12.7). So the seed decides little,
   and with 8 evil wins in total nothing here separates the arms. Two of b8's four evil wins came from good executing its own Saint on the final day
   (opus55-v-sol61-b8/game-04, sonnet55-v-sol61-b8/game-02). That is a mistake by good and has nothing to do with beats.

2. **8 beats deepens conversations; it doesn't widen them.** Messages per pair per day went from 2.30 to 2.69. The share of pair-conversations that became
   real threads (3+ messages, 2+ turn changes) went from 31% to 40%, and threads per game-day from 10.8 to 14.9. More whispers got a reply later
   that day (39% to 46%). The number of distinct people each player talked to barely moved (6.3 to 6.7). Swarms (4+ people whispering one player in a beat)
   hit 54% of beats at 6 and 40% at 8. Per day that is the same count (~3.2), just spread over more beats. This is the one clear behavioural signal, and it matches w1's 4-to-6 trend.

3. **Late beats are not filler, but the last beat is always the weakest.** Novelty (share of content words the sender hasn't used earlier that day) falls
   smoothly by beat: 1.00, 0.76, 0.67 ... 0.54 at beat 6 in both arms, then 0.52 and 0.50 at beats 7 and 8. Near-duplicate whispers stay rare (1.1% vs 1.4%).
   What changes is the content: talk moves from claims toward nomination and vote planning (whispers mentioning nominate/vote/execute/test: 30% at beat 1, about 50% at beats 6-8).
   Empty turns rise toward the end. The *final* beat is the emptiest whatever it is numbered (35% empty at b6 beat 6, 45% at b8 beat 8, but only 26% at b8 beat 6).
   A last-beat whisper can never be answered that day. Overall empty share: 18% vs 22%. Day 1 is nearly full in both arms (92% of turns used). The extra beats go unused mostly on later days and among the dead
   (dead seats used 45-58% of turns at 8, 68-69% at 6).

4. **More private time did not help the town read evil; if anything it hurt on day 1.** Good seats' P(evil) probes before day-1 nominations
   sorted evil from good with AUC 0.67 at 6 beats and 0.60 at 8. That is matched-pair diff -0.08, p≈0.06 by sign-flip, and b8 was better in only 8/19 pairs. By day 2 the gap is gone
   (-0.04, p≈0.45). Role knowledge is unchanged: by day-1 nominations good seats correctly name 68% vs 70% of good players' shown roles.
   73% vs 72% of good players claim publicly on day 1. Good players tell their role directly to more people at 8 (4.5 vs 3.7 recipients), but by beat 6 the counts are equal (3.70 vs 3.71).
   Good players also claim slightly later (first-claim beat 1.98 vs 1.68). On the same deal the day-1 town square reads almost the same in both arms:
   same Virgin-test plan, same Outsider count, same speech length (~40 words) and density of role mentions. Treat the AUC dip as a weak signal.
   One plausible cause is log-dependent: at 6 beats the evil huddles make up a larger share of a shorter public log (evil's day-1 whispers to teammates were 41% vs 37%).

5. **Evil coordination is identical; the extra beats go to working the town.** In both arms 98% of evil seats sent their first whisper to a teammate (beat 1: 71% vs 63% of evil whispers),
   and evil re-syncs in the last beat (43% vs 42% of last-beat evil whispers go to teammates; chance ~20%). At 8 beats evil sends 1.8 more day-1 whispers per seat, and only 0.4 of those go to teammates.
   By a rough regex for self-claims, about as many evil seats tell two different role stories in private (35% vs 38%). No sign that more beats either help evil lie to more people or get it caught more.
   The best deception in the set did use the 8th beat. In opus55-v-sol61-b8/game-05, at 3 alive on day 5, the Poisoner Indigo (GPT-6.1 Sol)
   sent the good Drew a fake "misfired" whisper in beat 8, written as if to the Imp: *"Alex, stay on Mayor... I'll kill Harper tonight; poison him again. If they execute you, we still win with me alive."*
   Drew read it out in the square. Indigo answered *"Oh, damn. That was supposed to go to Alex."* (his thinking: "Crafting subtle fake leak"). The real Imp Alex played along (*"Fine. I'm the Poisoner; Mayor was a bluff."*).
   The town executed Indigo 7-2, and evil won with two players left. The town had been one vote from executing the real Imp.

6. **Model habits matter more than beat count.** Share of private turns used, 6 vs 8 beats: Sonnet 5.5 30-32% (it passes most turns, often with no thinking at all), Sonnet 4.5 ~50%,
   Opus 5.5 80% vs 75%, GPT-6.1 Sol 97% vs 93%, GPT-6 Astra 99% vs 96%. The arm effect on emptiness is small next to this.

## Numbers (pooled; b6 n=19, b8 n=20)

| | 6 beats | 8 beats |
|---|---|---|
| Evil wins | 4/19 (21%) | 4/20 (20%) |
| Days per game, mean (median) | 3.47 (3) | 3.80 (4) |
| 5+ day games | 5 | 8 |
| Day the game ended, good wins only | 2.87 | 3.44 (12 matched good-good pairs: 2.92 vs 3.50) |
| Executions hitting evil | 29/60 | 34/69 |
| Execution went to the day's first nominee | 65% | 78% |
| Cost per game / per day | $10.08 / $2.90 | $11.72 / $3.09 |
| Opus-v-Sol only (10 games each), cost and wall-clock per day | $1.73, 560 s | $2.16 (+25%), 728 s (+30%) |
| Wall-clock per game | 0.59 h | 0.83 h |
| Whispers per player per day | 4.9 | 6.2 |
| Empty private turns (last beat) | 18% (35%) | 22% (45%) |
| Distinct partners per player per day | 6.3 | 6.7 |
| Messages per pair per day; thread share | 2.30; 31% | 2.69; 40% |
| Whispers answered later that day | 39% | 46% |
| Day-1 nominations probe AUC (P evil) | 0.67 | 0.60 |
| Day-2 nominations probe AUC | 0.73 | 0.70 |
| Evil first whisper to a teammate | 98% | 98% |
| Evil day-1 whispers to teammates | 41% | 37% |

Noise check: game length (+0.4 days, matched 9 longer / 7 shorter / 3 same) and first-nominee executions (+13 points) are suggestive at most.
The thread, answer-rate and turn-use differences rest on thousands of whispers and are real. The outcome comparison has 8 evil wins in total and says nothing.

## What depends on the public whisper log (dropped in v16)
- Swarm and huddle numbers, and any evil restraint. Evil did adapt a little: *"they noticed our early whisper cluster, so I'll avoid more group huddles"*
  (Harper, sonnet55-v-sol61-b8/game-02); *"I'll stay quiet and avoid adding to the whisper pattern"* (Casey, opus55-v-sol61-b8/game-05).
- Public reasoning from the log, about 0.7-0.8 mentions per day in both arms. Good players sometimes caught real teams with it: *"From the very first beat it was Casey, Frankie and Gray whispering each other and nobody else"* (Alex, opus55-v-sol61-b8/game-01, correct).
  Evil turned it into frames just as often: *"Blair, Ellis and Indigo have whispered in a closed triangle"* (Frankie, evil, opus55-v-sol61-b8/game-02).
  Players also used it for timeline checks (*"Blair whispered you in private time 1... Your story's impossible"*, Jules, b8/game-01).
- The possible day-1 AUC dip (mechanism above). Thread depth, last-beat emptiness, novelty decay and late-beat vote planning probably carry over to private whispers.

## Realism
It reads like a real table in both arms: neighbours swap info, Virgin tests get arranged, players count Outsiders, and people chase who said what in which beat.
At 8 beats day 1 has slightly more of the real-game pattern of "hearing the same claim from three people and checking it". Herding is high in both arms:
executions pass with yes votes from about 93-97% of the living (ghost votes included), and at 8 beats the first nominee is executed more often, which suggests more of the wagon is settled privately before the square.

## Recommendation: keep 6
8 beats buys more real back-and-forth (threads 31% to 40%, replies 39% to 46%) and allowed one great deception. It costs ~25% more per game-day and
~30% more wall-clock per day, plus longer games: about +16% cost and +41% wall-clock per game pooled. It doesn't change outcomes, role spread or evil's coordination,
and day-1 detection is no better (if anything slightly worse). The final beat is always the emptiest and least answerable, so adding beats mostly moves that dead beat later.
6 beats, as v16 already uses, captures most of the realism gain for less. If more conversation depth is wanted later, test it without the public log, since part of the b6/b8 contrast here runs through the log.
