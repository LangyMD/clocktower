# Which private-time design makes more interesting games?

Reader: INTERESTING / DRAMATIC PLAY. I only read files. I ran no games, made no API calls and edited nothing in the repo. Scripts and data are in `scratchpad/proto/int/`: `metrics.py` builds `rows.json`, `score.py` builds `scored.json`, and `skel.py` and `wh.py` are viewers.

## Verdict
- **No design makes clearly more dramatic games.** On a rough interestingness score, 4 beats x 1 whisper (NEW4) beats the old 3 x 2 (OLD) on matched matchups: +0.38 SD, p≈0.02, 35 vs 23 games.
- **That lead comes from outcomes, not from private time.** NEW4 had more evil wins and longer games: evil won 16 percentage points more often on matched matchups, which W1-balance found not significant. Comparing good wins with good wins, the designs score the same (OLD −0.23, NEW4 −0.21, NEW6 −0.30). Comparing evil wins with evil wins, NEW4 is a little higher (+0.57 vs +0.41).
- **6 beats (NEW6, the nearest data to current v16) is not more dramatic than 4.** Its matched score is −0.12 against NEW4 (n=12, not significant). It had fewer changes in who the town suspects most (−0.40 per game) and fewer close votes (−0.48 per game). It did reach the final 3–4 a little more often.
- **About 1 game in 5 is dull under every design.** These are good wins by day 2: OLD 20%, NEW4 20%, NEW6 17%, public-log versions 20–26%. They come from a lucky Slayer shot at the Imp, or from day-1 public claims solving the table. The number of beats does not touch either cause.
- **What private time changes is the texture of the drama, not how much there is.** Under one whisper a turn, the best moments are traceable one-to-one events:
  - a claim given to a single person that later becomes evidence;
  - a Minion's "confession" whispered pair by pair to the town;
  - a first whisper quoted on the final day as proof of guilt.

  OLD games have the same kinds of moments, such as a leaked Chef pair caught by comparing notes and a Spy's lying Undertaker result.
- **Implication for v16:** keep 6 beats, since nothing here argues against it. To get more watchable games, move the balance toward evil (longer games, more reaching the final 3) or cut the day-1 Slayer kills. Changing beats will not do it.

## How I scored a game
Each game gets 8 components, each standardised over all 216 finished games. The score is the mean of the z-scores:
1. **Length:** days, capped at 7.
2. **Lead changes:** how often the town's top Demon suspect changed. This uses the mean P(demon) from living good seats' probes before nominations.
3. **Close votes:** votes within ±1 of the threshold, plus days where two or more nominations reached the threshold.
4. **Swing:** the summed day-to-day change in the true Demon's share of the town's suspicion.
5. **Deception events:** these are added together.
   - Bluff wars: a good and an evil player claiming the same character on the same day.
   - Exposures: an evil seat whose good-mean P(evil) jumps from below 0.4 to 0.6 or more in one day.
   - Bluff switches: an evil player changing claimed character, at most 2 counted.
6. **Went to the wire:** 4 or fewer alive on the final day.
7. **Comeback:** a good win where the Demon ranked 3rd or lower after day 1, or an evil win where the Demon was the top suspect at some point.
8. **Steamroll penalty:** a good win by day 2 with the Demon as the day-1 top suspect.

It is crude. It rewards long and evil-won games by construction, which is fair, because those are the games worth watching.

## Numbers

### Pooled
v7 (mirror matches) is excluded from the share columns. Score is over all games.

| Design | n | Evil win | Good win by day 2 | 5+ days | ≤4 alive on final day | Score |
|---|---|---|---|---|---|---|
| OLD 3x2 (v9/v12/v13) | 75 | .31 | .20 | .36 | .29 | −0.03 |
| NEW4 (v14 w1 + x0) | 40 | .35 | .20 | .45 | .35 | +0.06 |
| NEW6 (w1 -b6) | 12 | .42 | .17 | .42 | .42 | −0.06 |
| LOG6 (v15 c3 -b6, public log) | 19 | .21 | .26 | .26 | .21 | −0.24 |
| LOG8 (v15 c3 -b8, public log) | 20 | .20 | .25 | .40 | .30 | +0.13 |

### Matched
The comparison is stratified by ordered matchup (good model, evil model), weighted by the smaller cell. p is from a permutation test within matchups. Component differences are raw units per game.

| Comparison | Score | Days | Lead changes | Close votes | Deception events | Evil win |
|---|---|---|---|---|---|---|
| NEW4 − OLD (35 v 23) | **+0.38** (p .02) | +0.47 | +0.48 | +0.84 | +0.75 | +.16 |
| NEW6 − OLD (12 v 13) | +0.21 (p .39) | +0.10 | −0.08 | +0.47 | +0.73 | +.17 |
| NEW6 − NEW4 (12 v 22) | −0.12 (p .54) | −0.08 | −0.40 | −0.48 | −0.30 | +.05 |
| LOG8 − LOG6 (19 v 19) | +0.44 (p .03) | +0.42 | +0.42 | +0.37 | n/a | n/a |

### Opus 5.5 vs GPT-6.1 Sol only (both sides)

| Design | n | Evil wins | Score | 5+ days | ≤4 alive at the end |
|---|---|---|---|---|---|
| OLD | 9 | 2 | −0.16 | .22 | .22 |
| NEW4 | 14 | 6 | +0.13 | .50 | .43 |
| NEW6 | 8 | 3 | −0.11 | .38 | .38 |

### Confounds
- **Rule changes:** OLD includes v9 games, before the v12 Storyteller changes.
- **The closest-rules old data is duller, not livelier.** c2 (v12, Opus vs Sol) averaged −0.36, against +0.10 for e1 (v9) on the same matchup. So the Storyteller changes do not explain NEW4's edge.
- **Thin strata:** many OLD cells hold one game.
- **Cross-version text proxies were unusable** (relayed claims, "caught/contradicts" language, evil players giving different claims to different people). Most hits were hedges like "I'm the X, or the Drunk".
- **Genuine split claims are rare in every design**, roughly 0–10% of games.

## The best and worst games, with key moments

### NEW4 (4 x 1)

**Best: v14/x0-opus55-v-sol61/game-01-swap.** Opus played evil (Imp Blair, Scarlet Woman Drew, Poisoner Harper). Evil won with 2 alive. Score +1.28, 5 close votes.

*The frame.* On day 1 the Scarlet Woman tells the team: "I'll take Investigator and say one of two good players is the Spy, since the Spy can misregister and that's hard to disprove." He then whispers Ellis and Jules: "I got that one of Gray or Indigo is the Spy." Both of them were good. The town executed both (Indigo on day 1, Gray on day 2).

*The tense vote.* On day 3 the Imp went on the block 4/4. A 5/5 vote on Jules then replaced him.

*The catch.* The Imp was executed on day 4, and Drew caught the Demon role as Scarlet Woman.

*The final three: Alex (good), Drew (now Imp), Harper (Poisoner).* Every dead seat spent its beats lobbying, one conversation at a time. Drew whispered his team: "I'm telling good I 'lean Harper' for cover. Ignore it." The town reasoned its way to Harper, the wrong evil player. Harper voted for himself: "Fine - take me." That left 2 alive, and evil won.

**Best: v14/w1-opus55-v-sonnet55/game-01-swap.** Sonnet 5.5 played evil. Evil won after 6 days. The Imp was the town's 11th suspect on day 1 and its 1st on day 4.

*Day 4.* There were four nominations. The Imp went on the block 4/3, then a 4/5 tie wiped the block. Ghost votes then decided between Drew and nobody. Gray: "Correction for the ghosts: the tie wiped the block, so Blair is NOT on it anymore."

*Day 5.* The Baron "confesses" to being the Demon to save the real Imp. She whispers the town in pairs:
- To Gray and Harper: "No point hiding anymore. Drew was my Poisoner, and I'm the one you want... Execute Blair and you lose."
- Publicly: "I'm the Imp."

The town executes her, and the Imp's night kill wins. This was planned in private: the Imp told his team, "the winning play: publicly 'confess' you're the Imp".

**Worst: v14/w1-opus55-v-astra/game-02.** A Slayer shot the Imp on day 2 before a single nomination. **Also worst: w1-opus55-v-sol61/game-04.** The Demon was the top suspect on both days, and good won on day 2.

### NEW6 (6 x 1, nearest to v16)

**Best: v14/w1-sonnet55-v-sol61-b6/game-01.** Sol played evil and won after 6 days. The town executed four good players in a row: Empath, Mayor, Undertaker, Soldier.

*A private moment that decided an execution.* The Poisoner poisoned the Empath, whose number then flipped from 0 to 1. The Imp, posing as Fortune Teller, gave out a fabricated "Casey/Jules = yes", one listener at a time: "I shared it with Gray and Jules, but it could still be a red herring."

Ellis and Frankie each put the two facts together in private ("Jules's Empath went 0 to 1 with both neighbours unchanged"). The Empath was executed 9/5. The Imp reported back to his team: "Ellis and Frankie both now favour executing Jules... I'm open to that publicly rather than forcing Casey."

*The end.* Indigo, last good seat: "If you're wrong about me, she's the last one standing with you." Indigo was executed, and the Imp killed his own Poisoner to reach 2 alive.

**Best: v14/w1-opus55-v-sol61-b6/game-03.** Evil won after 6 days through a Scarlet Woman catch.

On the final day the Ravenkeeper nominates the real Washerwoman because of her first private message, five days earlier: "your first whisper fished before naming a ping." That whisper was "Tell me your character first and I'll tell you if it matches." She was executed 11/2.

**Worst: v14/w1-fable51-v-astra-b6/game-01-swap.** A Slayer killed the Imp on day 1.

**Lie caught, at 4 beats: v14/w1-fable51-v-astra/game-01.** The Scarlet Woman-turned-Imp told four people "Monk", then switched to "Soldier... Monk was cover to draw a kill" with others. The Investigator compared notes: "Gray claimed Monk to four people, reported a protection they now admit never happened". Gray was executed 7/2.

### OLD (3 x 2)

**Best: v9/e1-sonnet55-v-gpt6sol/game-01-swap.** Good won on day 5 at 4 alive. The Imp ranked 11th, 8th, 5th, 5th and then 1st.

*A lie caught on day 1.* Gray: "Harper gave me the Chef pair before I checked with Kit or Ellis, and Kit says he didn't tell her." Harper was the Baron, fed by the Spy.

*The Spy's lie.* The Spy, claiming Undertaker, reported that the executed real Slayer was "Baron": "the Undertaker result for Blair was Baron. Blair obviously says otherwise, but she would."

*The end.* The Saint at final 4 found the Imp. Alex: "your claimed evil team has no Poisoner. Your 'reveal' contradicts the result."

This is as rich as any NEW game.

**Best: v9/e1-gpt55-v-fable51/game-01.** Evil won after 6 days with a starpass and 4 close votes.

**Worst: v9/e1-sonnet55-v-gpt61sol/game-01-swap.** On day 1 a Recluse noticed "Indigo's private claim changed from Townsfolk to Butler". Then the Slayer shot Indigo, the Imp, and the Scarlet Woman was executed the same day. That is a nice catch inside a dull one-day game. **Also worst: v12/c2-fable5-v-gpt55/game-01-swap,** a day-2 steamroll.

## What this means
- **The OLD design produces great games too.** Interestingness tracks balance and length. The beat structure barely matters to it.
- **One whisper a turn gives the best moments a cleaner shape.** Each private claim has a known audience, which makes leaks and lies traceable and gives watchers a "who told whom" story. Examples are the Monk/Soldier catch and the "fished first" final-day vote. That is a reason to keep the new rule for watchability, but it is not measurable in these numbers.
- **More beats (6 or 8) did not add measurable drama without the log.** With the log, LOG8 beat LOG6 (+0.44, p .03), but the log is gone in v16.
