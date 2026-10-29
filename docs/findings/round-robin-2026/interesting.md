# f2: the most interesting games

**Verdict.** About a third of the 109 finished games (roughly 35–40) are worth reading: a deception or detection plan that works over several days, and an ending that comes down to one or two votes. About half have something worth a look. About a sixth are over almost at once: 18 games end by day 2, 9 of them because a Slayer shot hit the Demon. The best play comes from **Opus 5.5, Opus 4.8, GPT-6 Astra and Fable 5 as evil**, and from **Fable 5, Opus 5.5 and Astra as good**. The worst mistakes are two evil teams (GPT-5.5 and Opus 4.6) that each missed a self-vote that would have won the game. Each matchup has only one pair, so these are stories, not rating evidence.

## How I screened
Every game was scored on: days played, players alive at the end, close votes (within one vote of the threshold, or tied), Slayer, Virgin, star-pass and Scarlet Woman events, the good team's average P(Demon) on the real Demon by day (and whether it rose and then fell), how the game ended (Saint or Mayor endings, final three), and evil self-votes at final three or four. Then I read about 15 candidates closely (public talk, evil whispers, key thinking). Base numbers:
- Game length in days: 1: 8 games, 2: 10, 3: 19, 4: 21, 5: 30, 6: 20, 7: 1.
- 59 games end with four or fewer alive; evil wins 36 of them. 31 games have a close vote on the last day.
- Evil wins 7 games in which good's average P(Demon) on the real Demon reached 0.5 or more.
- 4 Saint executions, all with an Opus model playing good. 1 Mayor win.

## The picks

### 1. A promise to execute the Saint: games/v16/f2-opus47-v-opus55/game-01 (good Opus 4.7, evil Opus 5.5; evil wins, day 4)
- Day 1: the Imp handed the Poisoner a Chef bluff that happened to be true: *"say 0 pairs, which is actually true since none of us sit adjacent."*
- The Scarlet Woman claimed Washerwoman and built her claim on Gray's real Virgin claim. The Investigator's true ping ("Blair or Casey is the SW") then got the real Mayor executed with 11 votes.
- Day 3: the town found the Imp (ghost votes from four dead good players), but the Scarlet Woman got a promise on the record: *"if Jules goes today and the game doesn't end... Harper goes tomorrow, no more excuses."*
- She inherited the Demon, killed the Investigator (*"only one who could point SW at me"*), and nominated the Saint with *"Honoring the deal."* The town voted 8 yes (3 needed), using the true Chef 0 as its "logic lock."
- **Why it matters:** the best long plan in f2, a three-day setup in which every evil claim held up. Good's P(Demon) on the Saint went from 0.14 to 0.69 on the last day.

### 2. Same deal, opposite results: the Astra and GPT-6.1 Sol pair (same seed; in both games Casey is the Imp, Gray the Spy and Jules the Mayor)
- **games/v16/f2-astra-v-sol61/game-01-swap (good GPT-6.1 Sol, evil Astra; evil wins, day 5):**
  - The Spy cast the fifth vote on his own teammate Harper, which broke the town's planned tie. He then cast the decisive sixth vote for his own execution: *"resolve my seat now."*
  - After death, he whispered a sincere request to a dead player: vote Indigo. That player revealed it publicly, and the town read it as a reverse clear: *"Gray actively recruiting a ghost vote against them doesn't look like a Spy protecting Indigo."* It swung to Jules, the real Mayor.
  - The Imp star-passed to the Poisoner, who had poisoned the Mayor that night. The new Imp cast a yes vote and the town executed its Mayor at final three, 4 votes with 2 needed.
- **games/v16/f2-astra-v-sol61/game-01 (good Astra, evil Sol; good wins, day 5):**
  - At final four the cornered Imp tried a last card: *"I'm actually the Mayor. I bluffed Fortune Teller... those checks were invented."* The Spy switched claims: *"I'm Slayer, not Monk,"* and fired a fake shot at the Imp to "clear" him.
  - Astra's real Mayor, already dead, answered: *"Casey received my exact Mayor claim privately on day one."* Casey was executed.
- **Why it matters:** the same seat assignments decided by detection quality. Sol, as good, out-reasoned itself into executing its Mayor. Astra, as good, saw through two late claims made at once.

### 3. The Imp nobody suspected: games/v16/f2-opus46-v-opus48/game-01 (good Opus 4.6, evil Opus 4.8; evil wins, day 6)
- The Poisoner poisoned the Empath on night 1, saw that the Empath got a false "2," and built a fake Investigator claim on top of it: *"Drew's false read already helps us."* The real Fortune Teller had a correct YES on Alex, the Poisoner, but was executed on day 1 with 10 votes.
- A Slayer shot "cleared" the Poisoner (he isn't the Demon), and he used that for the rest of the game.
- At final four the Imp, claiming Soldier, held the swing vote. He publicly agreed to execute Alex, then turned: *"Alex, Drew, and Jules are right, and I was wrong to drift."*
- He voted out the real Mayor, 4 votes with 3 needed, with ghost votes from two good players who had been persuaded.
- **Why it matters:** good's P(Demon) on the real Imp never went above 0.03 in six days. Meanwhile the good team convinced itself that the real, poisoned Empath was the Poisoner.

### 4. The Imp takes the Virgin test: games/v16/f2-gpt55-v-astra/game-01 (good GPT-5.5, evil Astra; evil wins, day 6)
- Day 1: the Imp volunteered to be the "spent Townsfolk" nominator for the Virgin test. The test failed, and the town executed the real Virgin with 9 votes (the Imp's among them).
- The Poisoner, claiming Undertaker, then reported *"I saw Spy for Logan,"* which sealed the story.
- Day 5: the evil team planned a handoff (*"I'd let town execute Ellis and hand off to me... Casey can take the final execution"*). The Scarlet Woman nominated her own Imp and inherited the Demon.
- At final three she nominated the evil Poisoner, and the good players voted with her.
- **Why it matters:** a good team that reasoned well still lost. It correctly saw through a poisoned Ravenkeeper "Librarian" result, found the Imp (P = 0.81), and was beaten by a planned Scarlet Woman takeover.

### 5. The scripted Fortune Teller check: games/v16/f2-fable5-v-gpt56sol/game-01 (good Fable 5, evil GPT-5.6 Sol; good wins 4–4 on the last vote, day 5)
- The Imp, faking Fortune Teller, "checked" the pair Jules (the real Saint, killed that night) had asked for, and reported YES to frame the dead Baron as the old Imp. Jules revealed he had dictated the pair with its logic attached: *"in that same whisper I spelled out the whole logic."* The town concluded *"the alibi was dictated to the machine in advance."*
- The Poisoner then claimed Slayer and "shot" his own Imp (its teammate had warned: *"Don't fake a Slayer shot - it only exposes Gray"*). The town ignored it.
- Logan: *"Five nights, four dead verifiers, and the machine never bled."* A ghost spent the exact fourth vote.
- **Why it matters:** the clearest good-side detection, built on reasoning about how the Imp's kills and the evil team's tests were chosen, not on any single result.

### 6. A Monk who protected the wrong player: games/v16/f2-gpt55-v-opus55/game-01-swap (good Opus 5.5, evil GPT-5.5; good wins, day 5)
- At final four, the Opus town arranged an exact 3–3 tie with ghost votes to keep the Mayor-win option alive. The Imp (claiming Monk) and the Poisoner killed and poisoned the Mayor that night.
- At final three the Soldier caught the Imp's protection story: *"The Monk who guarded the unkillable Soldier over the Mayor at final 4."* A dead player added: *"'Protected Ellis' wasn't an easy lie... you picked the one target nobody can check."*
- **The twist:** on the Poisoner's own nomination, his self-vote would have made it 2/2. That would have left two alive and won for evil, and the Imp had whispered *"if either you or Blair dies, I win."* GPT-5.5 voted no: *"No. I'm not the Demon."*
- **Why it matters:** sharp good deduction plus a decisive evil mistake.

### 7. A Mayor win only because evil forgot a vote: games/v16/f2-opus46-v-gpt54/game-01-swap (good GPT-5.4, evil Opus 4.6; good wins, day 5)
- Day 1: a real Virgin trigger confirmed the Virgin and killed the Fortune Teller who nominated her.
- At final three the Imp nominated his own Poisoner. His thinking assumed *"Kit votes NO (to maintain cover)."* The Poisoner's thinking: *"I need 2 YES votes. Jules will vote YES (1). I need 1 more from either Indigo or a dead ghost vote."* He never counted his own vote.
- The dead Scarlet Woman also voted no, "for cover." It ended 1/2, there was no execution, and the Mayor won.
- **Why it matters:** this and pick 6 are the only two final-three cases where evil was one self-vote from winning. Both times the model did not see that its own vote counted.

## Honourable mentions
- **games/v16/f2-opus48-v-fable5/game-01 (evil Fable 5).** Evil invented a Spy that was not in play (*"Drew flips 'Librarian' - we hold the Spy line"*) to undo a Librarian confirmation of the Saint. Opus 4.8 executed its Mayor and then its Saint.
- **games/v16/f2-opus48-v-opus55/game-01 (evil Opus 5.5).** The Poisoner claimed Fortune Teller and poisoned the real Empath every night, so the Empath kept clearing the evil players next to him. Evil framed the Mayor and executed its own Poisoner at final three.
- **games/v16/f2-opus47-v-gpt55/game-01 (good Opus 4.7; 7 days, the longest game).** Good named the Imp (P = 0.85) but had used up its ghost votes. The Scarlet Woman voted on her own nomination to put herself on the block with 3 votes, which good could not beat. Evil won on vote count, not on deception.

## Patterns worth knowing
- **Saint executions: 4 of 4 with an Opus model as good** (4.6, 4.7, and 4.8 twice). The evil arguments were a fake Spy misregistering and "tomorrow if it doesn't end."
- **Fake Slayer shots by evil players** happen 17 times. Three were aimed at their own Imp to "clear" him (f2-astra-v-sol61/game-01, f2-fable5-v-gpt56sol/game-01, f2-opus47-v-gpt56sol/game-01-swap). The two I read in detail failed.
- **A minion volunteering to be executed at final three or four** is routine for every evil model, which makes many late evil wins mechanical rather than clever.
- **Best play by side:**
  - Evil: Opus 5.5 (pick 1, and the opus48-v-opus55 mention), Opus 4.8 (pick 3), Astra (picks 2 and 4), Fable 5 (the phantom Spy).
  - Good: Fable 5 (pick 5), Opus 5.5 (pick 6), Astra (pick 2).
  - Weakest: GPT-6.1 Sol as good executed its own Mayor at final three; GPT-5.5 and Opus 4.6 as evil missed winning self-votes.
