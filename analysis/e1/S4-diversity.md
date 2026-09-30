# S4: diversity in v9 e1

Reader S4. I only read files. I ran no games and spent no API money.
Data: all 60 e1 games (30 side-swapped pairs, seeds 60000–60029). 53 had finished when I last checked.
The 7 still running are included in the opening, strategy and language numbers. They are left out of the endings.
Scripts are in `scratchpad/s4/` (`load.py`, `openings.py`, `pairs.py`, `strat.py`, `lang.py`, `dup.py`, `stock.py`, `stylo.py`, `hive.py`, `noms.py`, `endings.py`).
How claims were counted: first-person regexes such as "I'm the X", "my X info" and "X here" over speech and whispers. Spot checks show the detector misses a few claims and has almost no false hits.
Model labels: effort variants are merged into the base model unless a table says otherwise. Samples are small: most models have 1–4 games per side, and only Opus 5.5 and Sol 6.1 have 11.

## Verdict

- **There is enough diversity in the things we measure.** Setups, how good plays, how evil plays in the mid-game, and endings all vary. They differ clearly by model.
- **Evil's opening is nearly the same in every game.** This comes mostly from the rules and structure, not from anything we can cleanly fix:
  - The Imp gets 3 bluffs, and at 10–12 players there are 3 evil players.
  - Whispers are free and invisible.
- **The most important finding is a leak, not a diversity problem.** It is a typography side channel. In cross-lab games, a detector that uses only surface features picks out the evil team far above chance, before it reads any content. Nobody exploits it yet, and it has a one-line fix (section 4).

## 1. Setups

There are 30 distinct setups. Each pair shares its seed, so the two games of a pair have identical characters, seating, bluffs and red herring (checked: 30 of 30).

| | |
|---|---|
| Table sizes | 10 / 11 / 12 players: 10 setups each |
| Outsider count | 0: 2 · 1: 4 · 2: 14 · 3: 6 · 4: 4 |
| Baron in play | 18 of 30. The forced Minion rotates by seed and the second Minion is random, so the expected rate is about 15. |
| Minion pairs | Baron+Spy 7, Baron+SW 6, Poisoner+Spy 5, Baron+Poisoner 5, SW+Spy 4, Poisoner+SW 3 |
| Townsfolk (setups in play, of 30) | Librarian 18, Monk 17, Ravenkeeper 17, Virgin 17, Empath 16, Investigator 12, Fortune Teller 12, Undertaker 12, Mayor 12, Washerwoman 11, Slayer 11, Soldier 11, Chef 8 |
| Outsiders | Drunk 19, Saint 18, Recluse 16, Butler 13 |
| Minions | Baron 18, Spy 16, Poisoner 13, Scarlet Woman 13 |
| Demon bluffs (of 90 slots) | Chef 14, Butler 11, Washerwoman 8, Undertaker, Recluse, Slayer, Investigator 7 each … Monk 1, Mayor 1 |
| Bluff shapes | 2 Townsfolk + Outsider: 20; 3 Townsfolk: 10 |
| Drunk believes it is | Empath 8 of 19, then Undertaker, Fortune Teller and Monk 2 each, … |

- Every character appears in 8–19 of the 30 setups.
- The spread is what uniform random dealing gives (the expected count is about 13, with a standard deviation of about 2.7). Nothing dominates and nothing is missing.
- Empath is the Drunk's apparent role 8 of 19 times. That is chance on top of the 3x info-role weight. Watch it, but it is no bug.
- **Limit:** seat names are the same 10–12 in every game (Alex…Logan, alphabetical and clockwise). Transcripts look alike, and a name carries across every game.

## 2. Openings

### 2a. When players claim, by true character (good seats, all games)

| true character | seats | public claim on day 1 | whispered claim on day 1 | never claimed in public |
|---|---|---|---|---|
| Librarian | 36 | 94% | 97% | 0 |
| Chef | 16 | 94% | 94% | 1 |
| Investigator | 24 | 92% | 92% | 0 |
| Virgin | 34 | 85% | 85% | 2 |
| Recluse | 32 | 84% | 91% | 1 |
| Washerwoman | 22 | 82% | 95% | 2 |
| Butler | 26 | 77% | 92% | 4 |
| Saint | 36 | 75% | 78% | 3 |
| Empath | 32 | 56% | 72% | 1 |
| Drunk (as a Townsfolk) | 38 | 55% | 68% | 1 |
| Fortune Teller | 24 | 54% | 71% | 2 |
| Slayer | 22 | 45% | 73% | 3 |
| Undertaker | 24 | 33% | 42% | 0 |
| Soldier | 22 | 32% | 59% | 2 |
| Mayor | 24 | 29% | 50% | 3 |
| Ravenkeeper | 34 | 24% | 47% | 4 |
| Monk | 34 | 24% | 50% | 3 |

- Timing fits each role, as in good human play. Roles with first-night information claim at once. Roles with ongoing information and hidden protective roles wait.
- Overall, 61% of good seats claim in public by the end of the day-1 town square and 74% claim in a whisper. That is well below the near-universal day-1 claiming that c1 found under v7.
- **Good players almost never bluff.** Only about 12 of 480 good seats (2.5%) made a first public claim that was not their character. Several of those were "I might be the Drunk".

### 2b. Per model (team model at the seat)

| model | games good / evil | good: public claim by end of day-1 town | good: whispered claim, day 1 | evil: public claim, day 1 |
|---|---|---|---|---|
| Sol 6.1 | 11 / 11 | 58% | 87% | 88% |
| Opus 5.5 | 11 / 11 | 64% | 78% | 70% |
| Astra | 4 / 4 | 66% | 79% | 83% |
| GPT-5.4 | 4 / 4 | 42% | 48% | 67% |
| Fable 5.1 | 3 / 3 | 61% | 96% | 78% |
| GPT-5.1 | 3 / 3 | 44% | 52% | 44% |
| o3 | 3 / 3 | 39% | 35% | 78% |
| Opus 4.8 | 3 / 3 | 73% | 55% | 78% |
| Sonnet 5.5 | 3 / 3 | 80% | 52% | 67% |
| Sonnet 4.5 | 3 / 3 | 79% | 83% | 89% |
| GPT-5.5 | 2 / 2 | 33% | 44% | 17% |

- Evil claims in public on day 1 more often than good does: 73% against 61% overall, and in most models. Evil also claims slightly earlier (mean normalised rank 0.46 against 0.52).
- Models range widely, from GPT-5.5 and o3 (about 35%, quiet) to Sonnet 5.5 and 4.5 (about 80%, open). That is real model variation.

### 2c. Tests and plays

- **Virgin.** In play in 34 games.
  - Nominated in 28 of them, 21 times on day 1. This agreed "Virgin test" is the most common day-1 set piece. The Virgin was tested on day 1 in every Sol 6.1 and Astra game that had one.
  - The Virgin's first nomination came from a good player 19 times and from an evil player 9 times.
  - It triggered 17 times.
- **Slayer.** A real Slayer was in 22 games. They shot 11 times (days 1–3, 3 hits) and 9 died without shooting.
  - There were 13 fake shots, all by evil players. Astra made 4 of them in 4 games, o3 2 and GPT-5.5 2. That is a genuine model-specific tactic.
- **Mayor.** In play in 24 games.
  - It never won. A living Mayor reached the final three once.
  - The town executed the Mayor 7 times, often after a day-1 Mayor claim. The Imp never killed the Mayor at night.

### 2d. How evil chooses bluffs

- Of evil first public claims, 72% are Demon bluffs, 16% are Outsiders, 7% are characters in play (double claims) and 14% are other characters not in play.
- In 25 of 60 games the three evil players publicly claimed exactly the three bluffs.
- The Imp shared the bluffs with both Minions in 53 of 60 games, 51 of those on the very first private-time turn. The standard message is "Imp here. Bluffs are X, Y, Z. I'll take X."
- The Spy wrote out the whole Grimoire to teammates on day 1 in almost every Spy game (Sonnet 4.5 and Opus 4.8 were the exceptions).
- In 44% of evil day-1 whispers, every recipient is on evil's own team.

**Side-swapped pairs.** The same seats are evil in both games of a pair, so I compared each evil seat's first claim across the two games:
- It matched for 32 of 90 seats. The Imp's claim matched in 17 of 30 pairs.
- The whole evil team's assignment was identical in 5 pairs: gpt56sol-v-opus55, gpt61sollow-v-opus55, gpt61solmedium-v-opus55, opus55-v-gpt61sol-a and opus55medium-v-gpt61sol.
  - All five are Opus 5.5 against a GPT Sol model: 5 of the 9 such pairs, against 0 of the 21 other pairs.
  - Two frontier models find the same "obvious" split. The Baron takes the Outsider, the Imp takes Chef 0 or Soldier, and the Poisoner takes the first-night role that backs the Imp.

Imp first claims: Chef 13, Soldier 8, Undertaker 7, Slayer 7, Ravenkeeper 6, Fortune Teller 4, …

The trajectories still split within a pair:
- Same day-1 execution in 4 of 30 pairs.
- Same first nominee in 12 of 30.
- Same night-2 kill in 8 of 28.

## 3. Strategies

### 3a. Evil

| evil model | evil games | bus (yes votes on an evil nominee) | yes on a good nominee | evil nominations that target good | fake Slayer shots | starpass + SW takeover |
|---|---|---|---|---|---|---|
| Sol 6.1 | 11 | 34% | 69% | 86% (21) | 1 | 5+1 |
| Opus 5.5 | 11 | 23% | 64% | 94% (17) | 1 | 2+1 |
| Astra | 4 | 31% | 81% | 75% (12) | 4 | 1+2 |
| GPT-5.4 | 4 | 35% | 81% | 85% (13) | 0 | 2+1 |
| Fable 5.1 | 3 | 18% | 51% | 100% (3) | 1 | 0+2 |
| o3 | 3 | 8% | 89% | 67% (6) | 2 | 0+1 |
| Sonnet 5.5 | 3 | 4% | 76% | 100% (5) | 0 | 0+1 |
| Sonnet 4.5 | 3 | 33% | 67% | 75% (4) | 0 | 0 |
| GPT-5.2 | 2 | 0% | 87% | 100% (8) | 0 | 0 |
| GPT-5.5 | 2 | 17% | 60% | 86% (7) | 2 | 0 |

- **Overall.** Evil votes yes on a teammate 23% of the time and on a good nominee 70%. 14% of evil nominations (15 of 109) target a teammate.
- **Changes of Demon.** 12 starpasses (Imp self-kills) and 9 Scarlet Woman takeovers. The Demon's identity changed in about a third of games.
- **Imp kills.** 50% hit roles with first-night information, 14% the Monk, 6% the Slayer. 67% of kills hit a player who had claimed in public. 1 kill hit an evil player.
- **Poisoner.** 56% of targets are first-night or ongoing information roles. 40% of doses fall on night 1.
- **Saint.** All 4 Saint-execution wins came in games with a Spy, who had told the team where the Saint sat. This strategy works, and it is tied to the setup.
- **Evil opening plans (probe `plan` at dawn of day 1) differ by model:**
  - Opus 5.5: "quiet / low profile" 54%, "frame a good player" 62%.
  - Sol 6.1 and Astra: "coordinate bluffs" 96–100%, "stay quiet" 0%.
  - Sonnet 5.5: quiet 89%, frame 78%.
  - GPT-5.4, o3 and Opus 4.8: rarely mention coordination (0–17%).

### 3b. Good

| good model | games | good yes on evil nominees | good yes on good nominees | good nominations that target evil |
|---|---|---|---|---|
| Sol 6.1 (high) | 8 | 62% | 35% | 66% |
| Opus 5.5 (high) | 8 | 44% | 45% | 47% |
| Astra | 4 | 66% | 17% | 62% |
| Fable 5.1 | 3 | 50% | 28% | 83% |
| Sonnet 5.5 | 3 | 63% | 18% | 75% |
| o3 | 3 | 42% | 49% | 44% |
| Opus 4.6 | 2 | 75% | 49% | 25% |

**Nominations converge.**
- In the first nomination round, about 4.9 living players nominate at once. On average they name 1.7 different people, and 79% name the same one.
- 95% of days end in an execution.
- Sonnet 5.5 as good is the exception: 42% of its days had no execution, and often nobody nominated at all.

**Beliefs converge, but not too early.**
- The probes give each good seat's P(Demon) for every other player. Between pairs of good seats, the mean correlation is:

  | point | correlation |
  |---|---|
  | dawn of day 1 | −0.02 |
  | day-1 nominations | 0.57 |
  | day 2 | 0.77 |
  | day 3 | 0.86 |

- Good seats agree on their top Demon suspect 56% of the time at day-1 nominations.
- So the town pools information over the day. It is not one mind from the start.

**How the Demon was caught.** I tagged the evidence named in the accusation that executed the Demon (35 games):
- night-kill or starpass logic 12
- Outsider count or Baron 11
- Empath 5
- Monk/Soldier 5
- Chef 5
- Fortune Teller 4
- Slayer, Virgin, Undertaker, Ravenkeeper, Investigator, Washerwoman or double claims 2–3 each

No single evidence path dominates.

## 4. Language

### 4a. No hive mind in the wording

- Near-duplicates are rare. I counted public messages of 6+ words whose word-trigram Jaccard similarity is ≥0.5 with a message from a teammate of the same model in the same game.
  - Every model is at 0–2.8%.
  - The duplicates are short vote remarks ("Vote no. Drew stays on the block.").
- Players almost never repeat themselves (o3 is highest at 1.8%).
- The phrases that recur across games carry content, such as "X or Y is the ROLE" and "what did you get last night". There are no stock speeches.

| model | messages | words per public message | em-dashes per message | top opener (share of public messages) | marker words (% of messages) |
|---|---|---|---|---|---|
| Sol 6.1 | 3553 | 36 | 0.13 | "I'm the" 5% | "worlds" 8.6 |
| Opus 5.5 | 3467 | 37 | 0.36 | "I'm the" 5% | "fair" 3.9 |
| GPT-5.4 | 1834 | 45 | 0.21 | "I’m" 17% | "clean" 12.5 |
| GPT-5.5 | 1468 | 47 | 0.23 | "I’m" 17% | "worlds" 24.1 |
| Sonnet 4.5 | 1458 | 37 | 0.01 | "I'm the" 5% | "confirm" 16.9 |
| o3 | 1435 | 74 | 0.63 | "I’m" 6% | "confirm" 14.5 |
| Opus 4.8 | 1276 | 77 | 1.36 | "This is" 4% | "confirm" 21 |
| GPT-5.1 | 1137 | 64 | 0.29 | "I’m" 14% | "worlds" 25.9 |
| GPT-5.2 | 881 | 81 | 0.55 | "I’m" 21% | "confirm" 25.8; markdown bold 4.5 per message |

- Each model has a clear voice (its idiolect) that every seat on the team shares.
- That is expected with teams of one model, and it is part of the signal. But see 4b.
- Sonnet 4.5 and Opus 4.5 have the lowest trigram diversity (0.66 and 0.68 distinct trigrams per trigram in a fixed sample; the others score 0.78–0.91).

### 4b. The typography leak (fixable, and it matters)

The engine passes each model's raw characters through to every other seat. Surface habits differ sharply by lab and by generation:

| model | curly apostrophe share | em-dashes per message | en-dashes per message | markdown bold per message |
|---|---|---|---|---|
| GPT-5.1 / 5.2 / 5.4 / 5.5, o3, Sol 5.6 | 0.96–1.00 | 0.2–0.7 | 0–0.3 | 0–4.5 |
| Sol 6 | 0.30 | 0.18 | 0 | 0 |
| Sol 6.1, Astra | 0.02–0.03 | 0.2 | 0 | 0 |
| every Claude model | 0.00 | 0.0–1.6 | 0 | 0 |

**Example** (gpt54-v-opus48/game-01, day 1): the three evil Opus 4.8 seats write "I'm the Washerwoman", "I'm the Investigator" and "I'm the Chef". All seven good GPT-5.4 seats write "I’m the Empath", "I’ve heard…" and so on.

**A test with no content.**
- For each seat I took 8 surface features from its public text: apostrophe style, three dash counts, words per message, bold, semicolons, "worlds".
- I then picked the 3 seats furthest from the table median.
- Cross-lab games (44): on average 2.1 of those 3 seats are evil, against 0.82 by chance. In 23 of 44 games all three evil players come out on top.
- Same-lab games (16): 1.9 of 3 are evil, driven by dash habits and message length.

**Consequences.**
- No player has used this yet: 0 mentions of style, apostrophes or punctuation in 60 games.
- But a stronger or more reflective model could use it. That would inflate the detection Elo of good teams facing another lab, and nobody would see it happen.
- It also hurts any future mixed table.

## 5. Endings (53 finished games)

| outcome | games | days |
|---|---|---|
| good: Demon executed | 35 | days 1–5 (mode 3–4) |
| good: Slayer shot | 2 | days 2–3 |
| evil: two players left | 12 | days 3–7 (mode 5) |
| evil: Saint executed | 4 | days 3–5 (all Spy games) |
| Mayor win | 0 | |

- Good games end on day 1 ×2, day 2 ×7, day 3 ×12, day 4 ×11 and day 5 ×5. Evil games end on day 3 ×2, day 4 ×1, day 5 ×8, day 6 ×4 and day 7 ×1.
- The 53 games have 27 distinct execution sequences (E = evil executed, g = good). The most common are "EEE" 7 (Minion, Minion, Imp on consecutive days), "gEEE" 5, "gE" 5 and "E" 3.
- So endings vary in length and path, but come in four types. A good win is either an unbroken run of evil executions or a single decisive late catch. An evil win is a long game of good executions.
- The Mayor and Virgin never decide a game directly. The Slayer rarely does.

## 6. What lacks diversity, and whose fault it is

| pattern | cause | fix? |
|---|---|---|
| Evil claims are almost fixed by the setup (72% bluffs; 25 of 60 games use exactly the three) | Rules: 3 bluffs for 3 evil players; models take few risks (7% double claims) | No, it is the official rule. Models could bluff roles in play or not in the bluffs, and seldom do. That is fine to measure. |
| The evil opening script is identical (bluffs shared on the first turn in 53 of 60; Spy writes out the Grimoire) | Structure: invisible, free whispers (a user decision); also correct play | No. Note it for readers. |
| Opus 5.5 vs Sol pairs repeat the whole bluff split in 5 of 9 pairs | Models converge on the best split; the pair shares the setup | No. When reviewing, read one game per pair for the opening. |
| Good almost never bluffs (about 2.5%) | Models | No. The prompt already allows it. |
| Mayor never wins; the Mayor is executed 7 of 24 times | Models | No. |
| Nominations converge (79% on one nominee in round 1) and 95% of days execute | Town-square consensus. Asking everyone at once shows it but does not cause it | No. |
| Same seat names every game | Setup | Yes, optional (R2). |
| Per-model typography identifies the evil team | Engine passes raw text | **Yes (R1).** |

## Recommendations

**R1 (do it).** "Players' text is shown with normalised typography."
- Before rendering any say, whisper, accusation, defense or vote remark: curly quotes and apostrophes become straight, em and en dashes become " - ", non-breaking hyphens become "-", and markdown emphasis is stripped.
- This is one line in `render.py` or where the reply is parsed. Keep the raw text in `events.jsonl` for review.
- It takes away the strongest style tells without touching what anyone says.
- Add a test: every seat sees the same characters for the same apostrophe. Rerun the `stylo.py` check after the change (the target is close to chance for the surface features).
- Message length and word choice stay. They are part of how each model plays.
- Needs a protocol bump (v11).

**R2 (optional).** "Seat names are drawn per seed from a fixed pool."
- It makes transcripts easier to tell apart and removes any prior attached to a name.
- The pair still shares its seed and so its names. The system prompt is unchanged, so caching is unaffected.

**R3 (analysis, no protocol change).** Add these per-model style metrics to `analyze`:
- day-1 claim rate by role class
- bus rate
- fake Slayer shots
- starpasses
- share of first claims that are bluffs
- a count of identical pair bluff splits

They are cheap and show strategic differences between models that win rates hide.

I recommend no change to the bluff count, the day structure, whisper visibility or the nomination procedure. Where diversity is low in those areas, the cause is the rules or the models' own convergence, which is what the eval should measure.
