# Evil's deception and good's information flow under each private-time design

I only read files: no games run, no API calls, no repository files edited. Scripts are in `scratchpad/proto/dec/`: `load.py`, `metrics.py`, `m2.py`, `multi2.py`, and `show.py GAME DAY` (prints private time with evil's thinking).

## Verdict

**v16 (6 beats, one whisper a turn, private) gives evil the fairest and most interesting deception task.**

1. **The one-whisper rule adds a real coordination cost; under the old rule evil had none.**
   - Old 3x2: in beat 1, 64% of evil seats briefed the team *and* worked a good player in the same turn (Opus/Sol games: 73%).
   - Under one whisper a turn: 0–1%, in every arm. The Demon's beat 1 goes entirely to the team (98–100%).
   - So evil now reaches the town about one beat later (first whisper to a good player: beat 1.3 before, 2.0–2.3 now).
   - Evil's plans also fall behind the town. A Minion can be locked into a story before the team's correction arrives.
   - This matches a real table, where evil has to step aside to confer.
2. **At 4 beats that cost is too heavy; at 6 beats it is paid back.**
   - At 4 beats evil spends beat 1 on the team and re-syncs in beat 4 (45% of beat-4 evil whispers; Opus/Sol 62%).
   - That leaves each evil seat 2.1 day-1 whispers to good players, against 3.1 under the old rule, a third fewer.
   - At 6 beats each evil seat sends 3.9 whispers to good players and reaches 3.75 distinct good players (old rule: 2.6; 4 beats: 2.3). Coordination still costs one beat.
3. **The public whisper log (v15) made the task "hide your huddle", and evil failed it.**
   - 97% of evil seats still opened with a team huddle.
   - With the same models, GPT-6.1 Sol as evil won 10 of 15 games without the log and 3 of 13 with it (Fisher p≈0.03).
   - Dropping the log was right.
4. **Most of the deception doesn't depend on the design.** Evil runs one consistent bluff in every arm:
   - The bluff comes from the Demon's bluffs, shared in beat 1.
   - When cornered, evil retracts it ("X was cover, I'm actually Y").
   - Evil almost never tells different stories to different people, never isolates a good player, and the town's beliefs converge just as much in every design.
5. **Win rates point the same way, but are weak evidence.**
   - Evil wins: old 28% (115 finished games), 4 beats 35% (40), 6 beats 42% (12), public log 10–21%.
   - Prior adjusted odds ratios for 4 and 6 beats against the old rule are 1.06 and 1.38, with wide intervals.

## Evidence

### A. How evil coordinates

| Day 1 (all games) | old 3x2 | 4 beats | 6 beats (v16) | v15 log, 6 | v15 log, 8 |
|---|---|---|---|---|---|
| Games (finished) | 128 (115) | 40 | 12 | 20 (19) | 20 |
| Evil's first whisper goes to a teammate | 89% | 98% | 100% | 97% | 98% |
| Team fully linked in beat 1 | 77% | 92% | 100% | 80% | 90% |
| **Beat 1: briefs the team AND contacts a good player** | **64%** | **1%** | **0%** | 0% | 0% |
| Evil's first whisper to a good player (mean beat) | 1.33 | 2.13 | 2.11 | 2.30 | 2.30 |
| Evil whispers that include a teammate (chance ≈27–30%) | 44% | 47% | 33% | 42% | 37% |
| **Whispers to good players, per evil seat** | 3.14 | **2.08** | **3.92** | 3.38 | 4.90 |
| Distinct good players reached, per evil seat | 2.58 | 2.33 | 3.75 | 3.35 | 4.52 |
| Imp shares the bluffs with the team on day 1 | 99% | 100% | 100% | 100% | 100% |

Share of evil whispers that include a teammate, by day-1 beat:
- Old: b1 62%, b2 32%, b3 37%.
- 4 beats: b1 98%, b2 17%, b3 25%, b4 45%.
- 6 beats: b1 100%, then 9%, 28%, 17%, 26%, 18%.

Under the old rule the team channel ran alongside the town work. Now it takes whole turns.

The Opus 5.5 vs GPT-6.1 Sol games alone give the same picture:
- Did both in beat 1: 73% under the old rule, against 0% in every new arm.
- Whispers to good players per evil seat: 3.37, 2.10 and 3.96 (old, 4 beats, 6 beats).

**Old rule: brief the team and bluff a good player in one turn.** v12/c2-opus55-v-gpt61sol-a/game-01-swap, day 1, beat 2. Blair (Imp, Opus) does two things at once:
- To Harper: *"I'm the Investigator. I got that one of Gray or Kit is the Scarlet Woman."*
- To the team: *"Drew = Recluse claim, Indigo = Mayor claim, me = Investigator. My ping: one of Gray/Kit is Scarlet Woman (told Harper already)."*
- In the same beat, Indigo (Poisoner) probes Jules and also tells the team to hunt the Saint.
- The team is never out of sync.

**v16: the lag is real.** v14/w1-opus55-v-sol61-b6/game-01-swap (Sol good, Opus evil).
- b1: the Spy dumps the Grimoire to the team. The Imp Ellis assigns the claims: Gray is to claim Investigator and frame Jules.
- b2: Gray tells Harper (the Slayer) *"I'm the Investigator. Got: Jules or Indigo is the Scarlet Woman."*
- b3: Ellis tells the team *"Jules is claiming Chef 0... DON'T frame Jules. Gray, just claim Undertaker instead."*
- b4, Gray's thinking: *"I'm locked into that story with both of them now and can't pivot to Undertaker."*
- b5, Gray to the team: *"Too late for Undertaker."*
- Good won on day 3.
- That is the kind of planning error a real evil team makes. The two-slot rule hid it.

**4 beats: the plan arrives with no time to act on it.** v14/w1-opus55-v-sol61/game-02-swap, day 1, beat 4 (the last private beat). Drew (Baron, Opus) tells the team: *"Idea: nudge Casey into being Indigo's Virgin tester... the Slayer's gone for free."* No private turn is left to do the nudging.

### B. Does evil tell different stories to different people?

Almost never, in any design. I counted first-person claims ("I'm the X", "my X claim", "X here", a leading "X:"), with good recipients only, then read the flagged cases.

| | old | 4 beats | 6 beats | log 6 | log 8 |
|---|---|---|---|---|---|
| Evil seats that self-claim on day 1 | 86% | 95% | 97% | 98% | 98% |
| Good players told the claim privately, per evil seat | 1.6 | 2.0 | 3.2 | 2.9 | 3.7 |
| Two different claims at once to different people, flagged / read as genuine | 3% / ~1% | 1% | 6% / ~0 | 5% | 5% |
| A retraction ("X was cover, I'm Y"), any day | 7% | 5% | 8% | 5% | 15% |
| Executed after a retraction | 60% | 4/6 | 1/3 | 2/3 | 5/9 |
| Public claim differs from the private one (day 1) | 2% | 2% | 0% | 2% | 2% |
| Imp claims one of its three bluffs | 96% | 100% | 100% | 95% | 95% |
| A Minion claims one of the bluffs | 76% | 78% | 70% | 85% | 87% |

- Most "concurrent" flags were false positives: "I got Monk for Indigo" is an Undertaker result, and "No Slayer here - still Saint" denies a role.
- The genuine split stories number about two in 230 games. For example, Harper (Baron) in c3h-sonnet55-v-sol61/game-02-swap: *"I'm the Soldier. I gave Indigo Butler because Gray fished me first and I wanted to see what leaked."*
- Evil's real repertoire is:
  - **One bluff, told widely and kept consistent.** 6 beats simply puts it in front of more people.
  - **Framing with fake information** (fake Investigator or Fortune Teller results).
  - **The Spy's Grimoire counter-claim.**
  - **A fallback retraction.** These usually fail. Ellis (Baron), w1-opus55-v-sol61/game-03-swap: *"Coming clean: I'm not the Butler, I'm the Librarian. I said Butler to Drew as cover"* (executed day 2). Drew (Baron), w1-sol56-v-opus55/game-01: *"I told Casey and Harper I was Chef, because a Recluse who gets pinged..."* (executed day 1).
- Evil seats use soft claims (*"one of X, Y or Z"* / three-for-three) 10–21% of the time, with no design trend.

**The best deception I read is in v16.** v14/w1-opus55-v-sol61-b6/game-02 (Opus good, Sol evil).
- The Spy Alex sees from the Grimoire that the Librarian Frankie was shown *"Alex or Blair is the Saint"*. In beat 2 he counter-claims Saint against the real Saint, Kit.
- Frankie walks into it in b2: *"So Alex, that backs you - and it means Kit's Saint claim is a lie."*
- The Scarlet Woman gives the Imp cover with a fake Fortune Teller "no on Gray/Ellis".
- The Imp tells his team *"don't turn it into an obvious coordinated pile-on."*
- The town executed the real Empath on day 1 (9 votes) and the real Saint on day 3, so evil won.
- One-to-one whispers also nearly gave the Spy away. Drew asked him: *"Who told you I had a ping on you? I only told two people."* Alex had learned it from the Grimoire.
- This is how private one-at-a-time talk makes deception both possible and catchable.

### C. How fast true roles reach the town (the "hive mind")

| Day 1 | old | 4 beats | 6 beats | log 6 | log 8 |
|---|---|---|---|---|---|
| Good players who tell their role privately | 72% | 74% | 84% | 83% | 91% |
| Players told privately, mean | 1.75 | 1.78 | 2.57 | 3.09 | 3.58 |
| Of whom evil | 0.46 | 0.51 | 0.73 | 0.92 | 1.06 |
| Evil share of those told (chance ≈30%) | 26% | 29% | 28% | 30% | 30% |
| First private claim in beat 1 | 54% | 60% | 51% | 60% | 45% |
| Public self-claim on day 1 | 59% | 62% | 59% | 64% | 69% |
| Probes, good seats name good players' roles (day-1 nominations) | 61% | 63% | 65% | 69% | 73% |
| Probes, evil seats name good players' roles | 73% | 74% | 80% | 83% | 86% |
| Agreement between good seats' P(evil), mean r | 0.72 | 0.74 | 0.83 | 0.74 | 0.73 |
| Good probe AUC, day 1 / day 2 | 0.58 / 0.70 | 0.62 / 0.75 | 0.66 / 0.71 | 0.67 / 0.73 | 0.60 / 0.70 |

- **The hive mind is the same size in every design.**
  - Good seats agree with each other at r≈0.72–0.83 in all arms.
  - In the Opus/Sol games alone it is 0.79, 0.73 and 0.83 (old, 4 beats, 6 beats), with no trend.
  - About 60% of good players claim publicly on day 1 in every arm. That, not private time, is what synchronises the town.
- **More beats spread true roles further, to evil as much as to good.**
  - Good players tell their role to evil at the chance rate in every arm, so on day 1 they cannot filter.
  - In every arm evil knows the good roles better than good does: the Spy's Grimoire plus pooling. At 6 beats: 80% against 65%.
  - 6 beats lets good players spread their roles but gives evil a better map too. That trade is a fair one.

### D. Do good players hide or bluff their roles?

Rarely, and the design does not change it.
- A false good-role claim in private: 1–5% of good seats in every arm.
- No claim at all on day 1: 18% under the old rule, 17% at 4 beats, 14% at 6, 8–11% with the log.
- The usual hedge is the soft claim: about a quarter of good seats send *"I'm Slayer, Soldier or Ravenkeeper"*.

### E. How the Demon's bluffs get used

Use is uniform in every arm and with every model:
- The Imp sends the three bluffs to both Minions in beat 1 (99–100%).
- The Imp claims one of them (95–100%).
- Most Minions take another (70–90%).
- The Spy usually picks a claim from how the Grimoire registered it, e.g. "Drew got 'Jules or Frankie is Butler', so I'll claim Butler".

The one-whisper rule changes when the bluffs reach the Minions only if the Demon wastes beat 1. None did.

### F. Can evil isolate or mislead individual good players?

No, in any design.
- Good players whose only day-1 partners were evil: 1–2% under private rules (0 of 254 in Opus/Sol).
- A good player's top partner is evil 19–21% of the time, against 30% by chance, because evil spends a third of its whispers on itself.
- The spread of probe accuracy across good seats in the same game is the same everywhere (SD of AUC 0.10–0.13).
- Evil works the whole table rather than capturing one player.

## Model mix: what survives the control

- In the Opus 5.5 vs GPT-6.1 Sol games, every behavioural difference above holds:
  - beat-1 dual-use 73% → 0%;
  - whispers to good players per evil seat 3.37 / 2.10 / 3.96;
  - the beat-4 re-sync at 4 beats (62%);
  - no split stories;
  - the same hive mind.
- Outcomes depend on the model more than the design:
  - **Opus as evil** lost 15 of 16 private-rule games (old 0/5, 4 beats 1/7, 6 beats 0/4) and 13 of 13 with the log.
  - **Sol as evil** won 2/4, 5/7 and 3/4 under private rules, against 3/13 with the log.
- The only outcome difference that survives the control is the log's cost to evil. 4 against 6 beats cannot be told apart on wins.

## Caveats

- The 6-beat private arm has only 12 games (8 Opus/Sol, 2 Sonnet 5.5/Sol, 2 Fable 5.1/Astra), so its win rate and its 0.83 agreement are noisy.
- Claims were detected by regex on first-person forms. I checked flagged cases by reading them, but soft or implied claims are missed.
- Sol's logged thinking is headings only, so evil's intent was read from Claude evil seats (Opus 5.5, Sonnet 4.5) and from Sol's whispers.
- The old-rule pool mixes v7, v9, v12 and v13 rules and older models. The Opus/Sol rows are the fair comparison.
