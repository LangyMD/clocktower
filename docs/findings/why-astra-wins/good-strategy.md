# The best good-team play in the 2026 games (f2, f3, f3b)

**Verdict.** The best good-team play, and the best two-sided games, are mostly in the v17 f3/f3b top-ups. The good side wins by working out mechanics: how a Spy can register, who a star-pass can go to, which execution is safe in every world, and how to make a tie on purpose. Five good teams stand out: **Fable 5.1, GPT-6.1 Sol, GPT-5.6 Sol, Astra and Opus 5.5**. Opus 5.5 is the one that plans its endgame around the Mayor. The top three games:

1. **f3-fable5-v-fable51/game-02-swap:** solving two star-passes and a misregistering Spy at final three.
2. **f3-gpt56sol-v-opus55/game-02-swap:** a Mayor win built on an exact tie.
3. **f3b-astra-v-opus55/game-02:** a Spy caught by what it knew, plus a Drunk Slayer worked out from his miss.

## How I screened
A script scored all 372 games on: good's P(Demon) on the current Demon by day (following star-passes), deaths by role, Virgin, Slayer and star-pass events, last-day vote margins, and when good's probes first named the Drunk, Spy or Baron. I then read about 20 candidates in full, leaving out the earlier f2 report's picks.

## The picks

### 1. Two star-passes, then a Spy solved at final three: games/v17/f3-fable5-v-fable51/game-02-swap (good Fable 5.1, evil Fable 5; good wins, day 5, 10 players)
- Good had a bad run. The real Virgin was the Drunk, so a Virgin test fizzled. Over three days the town then executed its Ravenkeeper, its Undertaker and its Librarian.
- Evil played very well. The Imp star-passed on night 4 to the Spy just before a certain hanging. The Spy then killed himself on night 5 to pass the Demon to the Baron, who had been claiming Saint.
- The final three were Blair (the Drunk Virgin), Harper (the Butler) and Drew (the new Imp). The dead pieced it together. Jules had claimed Soldier but died at night, so he was not a Soldier. A Drunk Jules would make three Outsiders, which is one too many. So Jules was the Spy, and the Librarian's "Saint is Drew or Jules" was the Spy registering as Saint. Casey (D5): *"The Spy is the only thing that's both."*
- Drew slipped when he called Blair "the Drunk" while nominating her. Gray (D5): *"in your own sentence Blair is 'the Drunk' - a good Outsider - and you're putting her on the block anyway."* The vote was 6 on Drew with 2 needed, and the dead Undertaker had saved his ghost vote *"for three alive, as agreed."*
- **Why it's clever:** the good team had made every mistake possible and still solved both successions and a Spy misregistration from outsider-count arithmetic. Good's P(Demon) on Drew went from 0.23 to 0.74 on the last day. **Contrast:** in the same-seed game with the sides swapped (f3-fable5-v-fable51/game-02), Fable 5 as good named the right Imp but reached a final three of three evil players and lost.

### 2. A Mayor win built on an exact tie: games/v17/f3-gpt56sol-v-opus55/game-02-swap (good Opus 5.5, evil GPT-5.6 Sol; good wins, day 6)
- D5, at four alive: the town agreed to skip the execution. Alex (Chef): *"today's shot and tomorrow's shot are the same single guess, but waiting gives us a night kill to read and a possible Mayor win."*
- D6, final three (Harper the Mayor, Kit the Scarlet Woman turned Imp, Gray the Spy). The Spy nominated himself, which would have won for evil if executed. The Imp then nominated the Mayor and put him on the block with 2 of 2 votes.
- The Spy's yes vote gave him away. He claimed Butler, but he voted while his claimed master, Frankie, voted no. Logan: *"that's not a Butler."* Then Harper counter-nominated the Imp: *"Goal is a TIE at exactly 2 - a tie means no execution and the Mayor wins, no gamble."* The vote landed exactly 2–2.
- **Why it's clever:** the town didn't need to know which of Gray or Kit was the Imp. It made the one result that wins in both worlds. The same pattern also wins **f3b-gpt56sol-v-opus55/game-02-swap** (Opus 5.5 again: *"Exactly 3: Gray, Logan, Blair. Everyone else NO"*; a 3–3 tie on the Imp). Opus 5.5 is the only good model that wins this way twice.

### 3. The Spy caught by what it knew: games/v17/f3b-astra-v-opus55/game-02 (good Astra, evil Opus 5.5; good wins, day 3)
- D1: Jules, the Chef, died to the real Virgin. That confirmed the Spy's fake Librarian ping ("Drew or Jules is the Drunk"), and Drew, the claimed Slayer, was in fact the Drunk.
- D2: Drew's shot on Ellis, the real Imp, did nothing. The town caught the Spy anyway through role knowledge. Kit (Empath): *"Before I'd shared that beyond Alex and Jules, Harper asked for my 'Empath number.'"* When Harper said Kit had "asked about neighbours," Kit answered: *"I never asked Harper about neighbours. That defense describes..."* The Spy was executed 8–5.
- D3: Ellis's shifting account of why he had asked to be shot settled it. Drew: *"Ellis has repeatedly tried to turn my failed shot into a clearance."* Then the Baron, claiming Butler, voted to rescue Ellis, which his claimed master's vote did not allow. Gray: *"Frankie just broke their claimed Butler restriction to save Ellis."*
- **Why it's clever:** in three days Astra worked out the Drunk, the Spy and the Imp against the strongest evil model. Every step came from cross-checking who had told whom what.

### 4. Dead evil "confess" and get ignored: games/v17/f3-opus55-v-sol61/game-01-swap (good GPT-6.1 Sol, evil Opus 5.5; good wins, day 6)
- D3: the Imp, claiming Fortune Teller, was caught overselling a result in private and executed. The Scarlet Woman inherited.
- D5, at four alive: the Imp broke the agreed skip and nominated the Mayor. The town counter-nominated him and tied it exactly. Blair: *"We need exactly two votes to tie: Logan and me."*
- D6, final three: the dead evil players claimed to be evil and named the wrong heir. Jules: *"Frankie and Indigo have both privately claimed evil and named Logan as the heir... that isn't verification."* Drew was executed 8–3.
- **Why it's clever:** good beat Opus 5.5 over six days with a deliberate tie and by refusing a fake confession.

### 5. A decision table against a fake Undertaker: games/v16/f2-fable5-v-opus55/game-01 (good Fable 5, evil Opus 5.5; good wins, day 5)
- The Baron became the Imp after the night-3 star-pass. He was claiming Undertaker, and his "readings" of the bodies framed the good Librarian as the Spy and the good Monk as the Poisoner.
- On the final day the town reasoned about risk, not about who was right. Indigo: *"hanging Ellis wins now or costs one day we can afford - hanging Jules risks losing the game."* Blair: *"explain why the Imp spared the outed Undertaker four nights running."*
- They counted the votes exactly. Ellis needed 5 votes, and the counter-nomination on the Saint could reach only 4. Logan: *"If a fifth hand rises on the Saint, it belongs to evil."* Ellis was executed.
- **Why it's clever:** the town beat a better liar by not needing to beat his story. Good's P(Demon) on Ellis rose from 0.10 to 0.50 on the last day.

### 6. The "safe fork" sequence: games/v17/f3-gpt56sol-v-opus55/game-04 (good GPT-5.6 Sol, evil Opus 5.5; good wins, day 5)
- The Monk protected the Undertaker every night, so each execution was checked. D3: the town executed Gray as the *"safe fork"*: a win if Gray was the Demon, a reading if not. He came back as the Drunk, which confirmed two other info roles.
- At final four the evil ghosts used their votes to put a good player on the block. Harper: *"Kit's counter-nomination drew exactly the three evil votes."* The Imp was executed 8–4.

### 7. Two Saint claims and a "bridge": games/v17/f3b-gpt56sol-v-sol61/game-01 (good GPT-5.6 Sol, evil GPT-6.1 Sol; good wins, day 5)
- The Baron claimed Slayer and fake-shot his own Imp, and the Imp counter-claimed Saint. The town executed the Butler, who was good in both worlds: *"Alex is the mandatory bridge."* When the Imp then star-passed, they caught the Baron: *"A sober Slayer ... should shoot Gray."*

### 8. Pairs fixed in advance, results still made up: games/v17/f3-gpt56sol-v-sol61/game-01-swap (good GPT-6.1 Sol, evil GPT-5.6 Sol; good wins, day 5)
- After a double succession (Imp to Scarlet Woman to Baron), the Baron's fake Fortune Teller chain was perfectly consistent. The town's answer: *"You precommitted pairs, not predictions."* Executed 6–2 at final three.

### 9. The Spy's Slayer fish: games/v17/f3-gpt56sol-v-astra/game-04-swap (good Astra, evil GPT-5.6 Sol; good wins, day 5)
- *"Frankie opened today by offering to take my shot, before I'd told them my role."* The Spy was executed. At final three Casey published the best case against the real Slayer, then still voted out the Imp, who was claiming Saint (P(Demon) on him went from 0.09 to 0.73 that day).

### 10. The Spy jumps on the grenade: games/v17/f3b-opus55-v-sol61/game-01 (good Opus 5.5, evil GPT-6.1 Sol; good wins, day 4)
- At final four the Spy "confessed" to being the Demon and the Imp claimed Saint at the last minute. Gray: *"If Blair were really the Saint, Drew would be begging us to execute Blair."*

## Honourable mentions
- **f3-astra-v-opus55/game-03.** Astra executed the Imp on day 1 from a slip: *"Gray, who told you I have information to work overnight?"* The Poisoner nominated himself to take the Imp's place and got 3 votes.
- **f3-gpt56sol-v-sol61/game-03.** At final three the Spy fake-shot his own Imp. A ghost vote gave the evil team away: *"an old Imp would never risk putting their successor Demon on the block."*

## Patterns
- **Good-side record by model** (all 2026 games; each model faced different opponents, so this is a rough guide):

  | Good model | Wins | Executions that hit evil |
  |---|---|---|
  | Astra | 26/26 | 76% |
  | GPT-6.1 Sol | 32/35 | 65% |
  | GPT-5.6 Sol | 46/56 | 54% |
  | Fable 5.1 | 27/37 | 50% |
  | Opus 5.5 | 26/45 | 43% |
  | Opus 4.8 | 10/29 | 33% |

  Astra wins fast, mostly by day 3. The Sols and Fable 5.1 win long games through mechanics. Opus 5.5 executes more good players, but plays the cleverest endgames (Mayor ties, the fake-Butler catch).
- **Spies give themselves away by what they know** (picks 3, 9, 10): asking for a role nobody had claimed, offering to take a Slayer shot before the Slayer had claimed, or naming a role before it was revealed.
- **Deliberate ties** to protect a Mayor or a Saint appear in picks 2, 4 and 5 and in the second Opus 5.5 Mayor game. They are new in v17; I saw none in the f2 picks.
- **Late "confessions" by dead or cornered evil players almost never work** against these good teams (picks 4, 10, and the f2 Opus 4.6 v Astra game).
