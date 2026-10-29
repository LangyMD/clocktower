# b2: why a team split across two models does worse as evil

**Answer.** The mixed evil team doesn't fall apart in its own chat. It votes together, keeps its bluffs apart and
argues no more than a single-model team does, and no good player ever spotted the model split. What it loses is
*hiding*, and hiding works like a weakest link. A team of Opus 5.5 and GPT-5.6 Sol (Sol 5.6) survives day 1 better
than either pure team. But the Opus seats are more visible: they talk more, nominate more and write most of the team's
plans. So they get caught first, and once one evil seat is executed the town tracks its links to the rest. The
mixed team ends up exposed at about Opus's rate. The Sol seats lose what they are best at: a Sol Demon that keeps
its cover deep into the game. Averaging the two ratings assumes the strengths add up. Evil cover doesn't add up: it
lasts as long as its weakest seat holds.

Data: 66 mixed evil games (b1 + b2, 4 evil wins; members' average predicts 11.3). Baselines are pure Opus 5.5
evil (23 games, 2 wins, 3.0 predicted) and pure Sol 5.6 evil (20 games, 3 wins, 3.8 predicted), both against the same
three opponents (GPT-6.1 Sol, Fable 5.1, GPT-6 Astra; v16 f2 + v17 f3/f3b/f4/f5). "P(evil)" and "P(demon)" are the
good players' belief probes at nominations.

## 1. Evil cover is a weakest link, and the mixed team collapses at Opus's pace

| Executions that hit evil | Day 1 | Day 2 | Day 3 |
|---|---|---|---|
| Pure Opus 5.5 evil | 11/23 (48%) | 14/18 (78%) | 12/15 (80%) |
| Pure Sol 5.6 evil | 7/20 (35%) | 13/20 (65%) | 8/16 (50%) |
| Mixed evil | 19/63 (30%) | 46/64 (72%) | 36/47 (77%) |

The mixed team does best on day 1, then from day 2 it is caught as often as pure Opus. Pure Sol is the one team that
keeps the town guessing. The link from one exposed seat to the rest is association. After the first evil
execution, good players' P(evil) on the surviving teammates rises **+0.20** overnight in mixed games (Opus +0.15, Sol
+0.11), and the next day's execution hits another evil player in 40 of 52 mixed games. About 55% of nominations against
an evil player cite a dead evil teammate by name, in mixed and pure games alike. The cases read like this:

> "Nominating Ellis. Alex spent a minion's only ghost vote to save Drew - and Ellis is the one living Townsfolk
> claimant who fought alongside him to do it." (`b2-mixA-v-fable51/game-06-swap`, day 3, Harper, nomination.
> Alex was the dead Opus Poisoner, Ellis the Sol Imp.)

> "Jules repeatedly turned uncertain information into a case for executing the Saint, ... and defended Blair. Blair's
> last-minute confession looks aimed at rescuing Jules." (`b2-mixA-v-sol61/game-13-swap`, day 3, Casey, nomination.
> Blair was the Opus Poisoner, Jules the Sol Imp.)

## 2. Inside a mixed team, the Opus seats are the lightning rods

- Evil seats executed by the end of day 2: **Opus 40 of 99, Sol 25 of 99**. The first evil player executed was an Opus
  seat in 38 of 66 games. Against GPT-6.1 Sol, Opus seats on a mixed team fell by day 2 46% of the time (37% on
  pure-Opus teams), and Sol seats 24% (28% on pure-Sol teams). Evil execution shifts onto Opus.
- On a mixed team the Opus seats do the visible work. In days 1–2 they make 6.2 public statements per seat (5.0 on a
  pure-Opus team), nominate 0.37 times per seat (0.22), and write about 70% of the evil team-chat words (56-word
  whispers against Sol's 31). In team chat Opus proposes the schemes, such as framing the real Saint, building a whole fake
  world from the Spy's Grimoire, or pushing a named player, and Sol mostly asks for its assignment:

> Sol Baron: "Send me the bluffs and preferred claim split. I can play outsider-heavy/quiet early unless one bluff
> suits me." Opus Spy, same beat: "WIN CONDITION: Gray (the real Saint) has claimed Saint to me ... Let's frame Gray as
> the Minion lying about Saint, and push hard for Gray's execution today or tomorrow." (`b2-mixA-v-sol61/game-12-swap`,
> day 1, evil whispers.) The next day the Opus Imp was executed for "treating the repeated 0 as growing support for
> Harper" (the Opus Spy): Frankie, day 2, nomination.

## 3. Sol Demons lose their cover; a lone-model Demon almost always dies

- Good players' P(demon) on a **Sol Demon** at day-3 nominations is 0.17 on a pure-Sol team and **0.31 on a mixed
  team**. The Sol Demon is the town's top Demon suspect 21% vs 43% of the time. Against GPT-6.1 Sol alone the
  numbers are 0.07 (6 games) vs 0.35 (12 games). An **Opus Demon** looks the same either way (0.33 pure, 0.31 mixed).
  Sol's best evil asset gets spent covering for Opus teammates.
- If the Demon's model is alone on the evil team (both Minions are the other model), evil won **0 of 17** and the
  Demon was executed in 16. With one same-model Minion, evil won 4 of 49 and the Demon was executed in 39. That gap is
  suggestive only (Fisher p > 0.2).
- The Demon's model alone doesn't decide it: Opus Demons won 2 of 34, Sol Demons 2 of 32.

## What doesn't explain it

- **Incoherent team chat.** Evil teammates vote the same way 75% of the time across models and 76% within
  a model (pure teams 73–79%). Minions include the Demon in 93–94% of team whispers either way. Disagreement words in team replies
  ("careful", "disagree", "please don't") are a model trait (Opus about 10%, Sol 1–4%), with no rise across models.
- **Bluff collisions.** No two evil players claimed the same role. 8 of 196 day-1 evil claims overlapped a
  good player's claim (4%), against 4/69 for pure Opus and 2/60 for pure Sol.
- **Bussing differences.** Opus votes to execute a Minion teammate 49% of the time whatever that teammate's model,
  and Sol about 40%.
- **Style odd-one-out and fingerprinting.** The minority-model seat on the evil team is *less* suspected on days 1–2
  (P(evil) 0.32 / 0.47, against 0.36 / 0.53 for majority seats). On day 2 the mixed team's P(evil) (0.51) falls between pure Sol
  (0.44) and pure Opus (0.58), as averaging predicts. A text search found no good player inferring teams from writing
  style or model identity ("writes like", "same phrasing" and similar). The losses come later and through
  association, not from early tells.

## Caveats

- Small samples: 4 mixed evil wins, and only 43 pure baseline games against these opponents. The pure teams also ran
  slightly under prediction against these three (5 wins vs 6.8), so some of the −158 may be specific to the
  top opponents rather than to mixing. The fit's interval [−330, −14] already allows a much smaller effect.
- Opponent mix differs: 36 of the 66 mixed games are against GPT-6.1 Sol, against 15 of the 43 baseline games. Where it
  matters I compared within an opponent. Per-opponent cells are 5–15 games.
- The mechanism is correlational, read from logs. A clean test would fix which model holds the Demon and which the Minions.
