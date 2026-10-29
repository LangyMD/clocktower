# f2 duds: which games fell flat, and why

## Verdict
- **27 of 109 games (25%) are duds.** 18 were over by the end of day 2 (all good wins, 6 of them on a day-1 Slayer shot). The other 9 were decided by one blunder, or were a steamroll where one side never landed a hit.
- **Model blunders are the biggest cause: 13 of 27.** 11 of those 13 come from the three weakest older models: GPT-5.4 (3), Opus 4.7 (2) and Opus 4.8 (6, on both sides). Fable 5 has the other 2. These games are not noise. They show real weakness, the kind the eval exists to measure.
- **Luck of the deal: 9.** Examples are a night-1 Empath sitting between two evil players, or a near-blind Slayer hit. This floor holds even among the newest models: 4 of the 8 duds between two newer models are deal luck.
- **Storyteller: 1. Harness: 0 as the main cause.** Opus 4.8's lost turns contributed to 2 of its losses as good, and they skew its detection rating.
- **4 "duds" were earned.** One side was outplayed with no fault in the design.
- **So the design is mostly sound.** Older evil teams lost flat in 32% of their games (16/50) and newer ones in 19% (11/59). Old-vs-old games were duds 35% of the time and new-vs-new 27%.
- **What to change:** two harness fixes and one optional table-size change. Leave the Trouble Brewing rules alone. More pairs will average out the deal luck. See the last section.
- **Caveat:** 1 pair per matchup. Per-model counts are 0 to 6, so read them as anecdotes, not rates.

## How I classified
A game counts as a dud if it meets one of these:
- it was over by day 2;
- it was decided by a single unforced error or fluke;
- it was a steamroll (the loser never executed an evil player or never lost a good one, and it was short).

I read the public log, nominations, defenses and key whispers or thinking of every candidate. I left out two Saint-execution losses (`f2-opus46-v-sol61/game-01`, `f2-opus47-v-opus55/game-01`). Both were real deception wins: GPT-6.1 Sol's fake Undertaker, and Opus 5.5's fake Empath plus a Scarlet Woman takeover.

| Cause | Count | Games (folder; the side that collapsed) |
|---|---|---|
| (b) model weakness | 13 | gpt54-v-opus55 swap (GPT-5.4 evil), gpt54-v-sol61 swap (GPT-5.4 E), opus46-v-gpt54 g1 (GPT-5.4 E), opus46-v-opus47 g1 (Opus 4.7 E), opus47-v-gpt56sol swap (Opus 4.7 E), opus48-v-sol61 swap (Opus 4.8 E), opus48-v-astra swap (Opus 4.8 E), opus48-v-gpt56sol swap (Opus 4.8 E), opus48-v-sol61 g1 (Opus 4.8 good), opus48-v-fable5 g1 (Opus 4.8 G), gpt54-v-opus48 swap (Opus 4.8 G), fable5-v-astra swap (Fable 5 E), fable5-v-sol61 swap (Fable 5 E) |
| (d) luck of deal | 9 | astra-v-opus55 g1, gpt56sol-v-astra g1, opus46-v-sol61 swap, opus47-v-astra swap, opus47-v-opus48 g1 and swap, opus48-v-opus55 swap, fable5-v-fable51 g1 and swap |
| (a) Storyteller / mechanics | 1 | gpt54-v-gpt55 swap |
| (c) harness | 0 main (2 contributing) | opus48-v-sol61 g1 (5 lost turns), opus48-v-fable5 g1 (9 lost turns) |
| earned (no fault) | 4 | gpt54-v-gpt55 g1, gpt56sol-v-fable51 swap, opus46-v-gpt56sol g1, fable51-v-opus55 g1 |

"g1" is game-01 and "swap" is game-01-swap. All folders are under `games/v16/f2-*`.

**Flat losses by model** (each model played 10 games per side):

| Model (release order) | Lost flat as evil | of which blunders | Lost flat as good |
|---|---|---|---|
| Opus 4.6 | 1 | 0 | 0 |
| GPT-5.4 | 4 | 3 | 0 |
| Opus 4.7 | 4 | 2 | 0 |
| GPT-5.5 | 1 | 0 | 0 |
| Opus 4.8 | 5 | 3 | 3 (all blunders, 2 with lost turns) |
| Fable 5 | 3 | 2 | 0 |
| GPT-5.6 Sol | 2 | 0 | 0 |
| Fable 5.1 | 1 | 0 | 1 (vs Opus 5.5, earned) |
| GPT-6 Astra | 1 | 0 | 0 |
| Opus 5.5 | 1 | 0 | 0 |
| GPT-6.1 Sol | 0 | 0 | 0 |

**Winners of duds:** GPT-6 Astra and GPT-6.1 Sol 4 each, GPT-5.6 Sol and Opus 4.6 3 each, the rest 1 or 2. Nearly all duds are good-side wins. Evil won flat only 4 times, 3 of them against Opus 4.8.

## Examples
1. **GPT-5.4 Imp nominates the Virgin** (`f2-gpt54-v-opus55/game-01-swap`, day 1). Drew, the Imp claiming Soldier, said: "I'll nominate Alex. We've got a claimed Virgin sitting here untested." Alex replied: "if you're a real Soldier, you just executed yourself." There was no trigger, and Drew was executed 7/7 that day. The same blunder happens in `f2-gpt54-v-sol61/game-01-swap`: Gray, the Imp claiming Chef, said "Frankie asked for the test all day. Let's just resolve it now", got no trigger, and was executed.
2. **A dead Opus 4.7 Scarlet Woman aims the Slayer** (`f2-opus46-v-opus47/game-01`, day 2). Blair said: "Gray - if you fire tonight, do NOT shoot Ellis. Killing a real Fortune Teller ends the game for you." Gray, the Slayer, shot Ellis, the Imp, at once.
3. **A Fable 5 Imp tells the Slayer it is the Saint** (`f2-fable5-v-astra/game-01-swap`, day 1). The Spy had already whispered "Alex=Slayer" to the evil team. Blair, the Imp, thought: "he's the Slayer, which makes him dangerous to me... I'll... tell him I'm Saint too." Alex: "Blair's Saint claim is risky to test by execution... I'm taking my shot at Blair." The game was over on day 1.
4. **GPT-5.4 Imp hands the Slayer the proof** (`f2-opus46-v-gpt54/game-01`, day 3). Jules, the Imp, privately suggested that the Slayer test the Virgin, which would have killed the Slayer. Drew, the Slayer, said: "two deliberate attempts to eliminate the one person who can end this game... Jules is the Imp." The shot hit.
5. **Deal: Empath between two evil players, both seat orders** (`f2-opus48-v-opus55/game-01-swap`, day 1). The night-1 Empath read 2 on Harper (Poisoner) and Jules (Imp), and Harper had also double-claimed Investigator. Frankie, the Slayer: "Jules's FT claim is the likely Imp bluff. Shooting Jules." The same pattern decided both games of fable5-v-fable51 (Empath 2 plus Chef 2) and both games of opus47-v-opus48 (Empath 1 next to the Imp). The swapped pair cancels that luck in the rating, but it still wastes the games.
6. **Storyteller misinformation lands on the Demon** (`f2-gpt54-v-gpt55/game-01-swap`). The Poisoner hit the Investigator on night 1. The false world showed "either Harper or Drew is the Baron", and Harper was the Imp. Harper had said "No first-night info from me, and I'm not a setup-count role" and claimed Undertaker only on the block. Executed day 1, 7/5.
7. **Near-blind Slayer hit** (`f2-gpt56sol-v-astra/game-01`, day 1). Casey, the Slayer: "The current Baron accounting compresses the unclaimed seats; Alex, I'm taking the shot." It was one of about 4 unclaimed seats. Overall, real Slayers hit 6 of 14 day-1 shots (43%) but only 3 of 25 later. Most day-1 hits were informed, but two were close to coin flips: this one, and `opus46-v-sol61 swap`, where the shot was "Soldier is otherwise difficult to test."
8. **Opus 4.8 town executes its own Saint, with lost turns** (`f2-opus48-v-fable5/game-01`, day 4). The town executed the Mayor on day 2 and the Librarian on day 3, then the Saint. Logan, the Investigator, had lost 7 private turns that day to the ceiling. He nominated Alex, the Saint, and argued "The Spy reads as a Townsfolk even in death, so Drew's 'Librarian' flip is the disguise". There was no Spy in play.

## Is it the design or the older models?
- **Mostly the older models.** Blunders are 13 of 27 duds and almost all come from GPT-5.4, Opus 4.7 and Opus 4.8. The recurring blunders:
  - nominating the Virgin as an evil player with a Townsfolk claim (GPT-5.4, twice);
  - claiming a Townsfolk role that is in play (Opus 4.7 and 4.8, at least 4 times);
  - Saint bluffs at a known Slayer, or in a game with zero Outsiders;
  - dead Minions talking about their Demon;
  - a Spy revealing Grimoire knowledge ("Frankie knew my full result before I shared it", `opus48-v-gpt56sol swap`).

  This is the deception skill the eval rates, so it is signal, not a flaw.
- **The design's share is the Trouble Brewing luck floor:** night-1 Empath and Chef reads that solve the game, plus day-1 Slayer shots. That is about 9 games (8%), present at every skill level. It is noise, and more pairs is the cure.
- **Table size matters.** Duds were 34% at 10 players (12/35), 24% at 11 (9/38) and 17% at 12 (6/36). Ten-player games have 3 evil among 10 and usually no Outsider cover, so night-1 information isolates the Demon more often. This is suggestive at n of about 35 each.

## What to change (and not)
1. **Fix the Minion rotation (harness/plan bug).** Every f2 game had a Poisoner (`config.json` minion = Poisoner in all 110). The reason: `cli.py` picks `MINIONS[(base + k - 1) % 4]`, and the plan steps seeds by 100 per matchup (≡ 0 mod 4). Game-01 of every matchup will always get the Poisoner, however many pairs are added. Rotate on the matchup index, or hash the seed. Spy appeared in only 24 games, Baron in 43, Scarlet Woman in 42.
2. **Make the ceiling retry unloseable.** Opus 4.8's low-effort retry still spends all 8K on thinking: "I've deliberated enough - I'll go with Case II..." and then it is cut off. That made 76 lost turns, 1.2% of its turns, concentrated in 6 of its good games at 5 to 18 each. Give the retry an explicit small thinking budget (or none) instead of effort=low. Its 2-8 record as good (detection 1174) is partly this.
3. **Optional, if you scale: play 11–12 players only.** That roughly halves the flat games without touching any rule.
4. **Optional, low priority: a Storyteller weight** so a poisoned or Drunk Minion-pair ping (Investigator) avoids naming the real Demon, as a human Storyteller would. It decided 1 game. False Investigator pairs named the Imp 2 times in 16.
5. **Don't change:** day-1 Slayer, the Virgin, or the night-1 Empath and Chef. They are standard Trouble Brewing swing, and the hits are mostly earned reads on evil mistakes.
6. **For the scale-up decision:** dud games are not wasted. Older-model blunders are exactly the signal. Deal-luck duds (about 8%) are variance that more pairs average out. Nothing here argues against scaling. Scale after fixes 1 and 2.
