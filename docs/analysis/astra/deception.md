# Why GPT-6 Astra wins as evil (16/26)

**Answer.** Astra's Demon is rarely the one people suspect. Its team spends days 1 and 2 getting good players executed, and it plans how the Demon role passes on. Four habits do most of the work:
1. It picks **cheap claims** (one-shot first-night info) and **tunes its fake numbers** to fit whatever theory the town is already building.
2. It **follows the town's wrong theories instead of leading them**, and talks less in public than the good players do.
3. It **chooses kills to keep the confusion going**: it leaves alive the good players who are pushing wrong reads, and it keeps one info role poisoned.
4. It **plans who becomes the Demon next** (star-pass, Scarlet Woman catch), then ends the game by **executing its own Minion at final 3–4**.

It loses when the Demon claims an info role that needs fresh results (Undertaker or Ravenkeeper), when it switches claims late on the block, or to Slayer luck.

## Numbers (all 372 games, by evil model)

| | Astra | field range |
|---|---|---|
| Executions that hit a good player | **68%** | 34–63% |
| First execution lands on good (paired deal: Astra evil vs opponent evil) | **19/26** | opp. 10/26 |
| Share of days the Demon is nominated at all | **22%** | 22–42% |
| P(Demon on block \| nominated) | 62% | 48–85% (ordinary) |
| Evil alive at dawn of day 3 | **2.55** | 1.90–2.55 |
| Win rate once ≤4 players are alive | **83%** | 23–83% |
| Wins by executing own Minion down to 2 alive | **6** | 0–5 |
| Games with Demon succession (pass/SW), evil win rate | 11, **64%** | Opus 5.5 25%, GPT-5.6 Sol 32% |
| Evil public words per player, relative to good | **0.60×** | 0.51× (Sol 6.1) to 1.66× (Opus 4.8) |

**P(Demon) probes.** At each nomination phase, the share of good players' Demon probability that sits on the real Demon:
- **Day 1:** Astra's Demon gets 0.12, the same as other models' Demons (0.12–0.17). Chance is about 0.10.
- **Day 2:** Astra's Demon is still at chance (0.11, top suspect in 13% of probes). Other Demons climb to 0.12–0.33, top suspect in 9–44%. Sol 6.1 is the only other model this low (0.12).
- **Same deal, other evil team:** Astra's Demon is less suspected than the opponent's Demon in 15 of 17 pairs on day 2 (0.12 vs 0.33).
- **Caveat:** in that swap game Astra is the good team (the best detector), which inflates the gap. Against the same good model the gap is smaller: vs Opus 5.5 good, 0.10 vs 0.15 on day 1. So the edge is mostly that Astra's Demon **never becomes the obvious candidate**, not that it survives nominations: once nominated, it dies at the usual rate.

## Mechanisms, with examples

**1. Claims that can't be checked later, with numbers kept flexible.**
- The Astra Demon won **8/8** games when it claimed a first-night info role (Chef, Washerwoman, Librarian, Investigator). Other models won 27/91 with the same kind of claim.
- With an Undertaker or Ravenkeeper claim it won **1/5**.
- Minions pair with the Demon so their stories vouch for each other. `games/v17/f3-astra-v-opus55/game-01-swap` d1, Imp to team: *"Bluffs: Empath, Chef, Virgin. I'll claim Chef 1. Jules, take Empath 0 to cover me and Indigo."*
- Its Minions rarely claim an Outsider (15%, vs 20–29% for Opus 5.5 and Fable).
- Same deal, played by Opus 5.5: its Baron claimed Recluse, which made three Outsider claims for two slots, and was executed day 1 by 9 votes. Astra's Baron claimed Virgin and took a test that "failed". Town then executed the real Librarian who had nominated him (d1).

**2. Follow, don't lead.**
- Astra lets good players build the wrong theory and then joins it. `f3-astra-v-opus55/game-01-swap` d2 Baron: *"That gives us a natural direction without another Saint push. I'll let Indigo lead and avoid making this look coordinated."* d3 Imp: *"let's follow rather than force Ellis today."*
- Teammates take opposite sides on purpose. In `f3-astra-v-opus55/game-02-swap` the Baron, claiming Librarian, keeps "confirming" the real Saint while the Imp and Poisoner vote him out: *"Indigo, keep defending Jules - no need for a suspicious reversal"* (d3). The Saint was executed 5–4.

**3. Engineered Saint executions.** All 3 were against Opus 5.5 good.
- `f3-astra-v-opus55/game-02-swap` d2, Imp: *"poison Kit again tonight and I'll kill them, then claim Empath 1 on Jules/Blair… Could get Jules executed outright."* Then: *"Don't float Kit specifically being Drunk before their death; that would look suspiciously convenient."*
- In `game-01-swap` the Imp star-passed so the Scarlet Woman sat next to the Saint. She announced *"My number changed to 1"* (d4), and the Saint was executed 7–2.

**4. Kills that keep the confusion going.**
- Only 48% of Astra's kills hit info roles (field 49–65%). It removes Monks and Slayers first, and keeps alive good players who are useful to evil.
- `f3-astra-v-opus55/game-03-swap` d1: *"Keep Alex poisoned for now. We can kill Ellis and leave Alex generating bad information."* The Fortune Teller was poisoned 5 nights running, and his false YES got the Librarian executed. Astra's Poisoner repeats its target 50% of the time (median 0.25).
- `f3-fable51-v-astra/game-01`: *"I'd keep Gray and Kit alive for now: Gray backs Alex, and Kit's Butler vote can help us."*
- `f2-astra-v-opus55/game-01-swap`: *"kill Blair and leave Frankie alive to push Casey."*

**5. Planned succession.** The Demon role is treated as a token to hand off:
- `f2-gpt55-v-astra/game-01` d5, Imp: *"execute me today while Indigo can catch… Let my death look like another good execution and Casey look like the surviving Demon."* The Scarlet Woman nominated her own Imp, caught the Demon role, and then framed the Poisoner at final 3.
- `f3-gpt56sol-v-astra/game-01`: *"I passed because Harper's execution was leaving me as the clean next Demon candidate."* The Demon passed twice: Imp → Spy → Baron.

**6. Endgame vote control.** With two evil players alive near the end, executing a Minion is a win.
- `f2-fable5-v-astra/game-01` d5: *"Only nominate Gray today… that execution reaches two alive and wins."*
- `f3-fable51-v-astra/game-01`: *"Drew, vote for yourself if needed to make that execution unbeatable."*
- Astra's evil votes yes on its own teammates 47% of the time, which reads as clean distancing.

## The 10 losses: what goes wrong

- **Slayer luck, 2 games:** the Demon was shot on day 1 (`f2-gpt56sol-v-astra/game-01`, `f3-astra-v-sol61/game-03-swap`).
- **Claims needing fresh results, then a late Saint claim, 3 games.** The Demon claimed Undertaker or Ravenkeeper, invented reads, and claimed Saint once it was on the block:
  - `f3-gpt56sol-v-astra/game-02` d4: *"I am the Saint, not Undertaker. I used Undertaker as night-kill bait and fabricated the two reads."*
  - `f3-astra-v-sol61/game-02-swap` d3: *"I lied to maintain a cover… But I'm the uncounterclaimed Saint."*
  - `f3b-astra-v-opus55/game-02-swap` d2: *"I need to drop the cover: I'm the Saint, not Ravenkeeper."*
  - A late switch to Saint or Outsider on the block went **0 for 4**.
- **Minions sacrificing themselves in plain view.** In `f3b-astra-v-opus55/game-02-swap` the Baron offered to die and the Spy swapped to a new claim (Fortune Teller) to save the Imp. Town: *"Third volunteer to save Ellis. Keep Ellis."* That game also shows the deeper risk: the Imp held a private claim, told others to stay soft, and the Chef/Washerwoman math put him *"in every world."*
- **Hard math from strong detectors.** GPT-6.1 Sol and GPT-5.6 Sol held Astra to 4/9. In Astra's games where an Opus 4.x was the good team, Minions got exposed and Poisoners inherited (`f2-opus46`, `f2-opus47`: messy Saint → Ravenkeeper → Baron re-claims, and the new Imp was caught on day 5–6).

## Contrast with other evil teams

- **Opus 4.x and Fable** over-talk as evil (1.0–1.7× good players' words). Their first execution is usually a Minion (day-1 evil execution 52–63% for Opus 4.6–4.8). They kill info roles mechanically.
- **Opus 5.5** builds similar Saint plans (4 Saint wins), but it opens with conflicting Outsider claims and loses a Minion on day 1 (42%). Its successions win 25%.
- **GPT-6.1 Sol** is the closest twin: equally quiet, Demon equally hidden on day 2, 49% evil wins. Astra converts more endgames: 83% vs 59% once ≤4 are alive.

Caveats: n = 26. The Saint wins all came against one opponent (Opus 5.5). The probe gap on paired deals includes Astra's own detection skill as the good team.
