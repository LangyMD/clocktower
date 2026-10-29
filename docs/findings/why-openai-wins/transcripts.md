# Why OpenAI good teams beat Anthropic good teams: what the transcripts show

Reader report, Oct 25 2026 (about 400 games, v16 f2 and v17 f3–f5). I read side-swapped pairs, where the same
seed, seats and night information were played with an Anthropic good team in one game and an OpenAI good team in
the other: Opus 5.5 v Sol 6.1, Fable 5.1 v Astra, Opus 5.5 v Sol 5.6, Fable 5 v Sol 5.6, Opus 5.5 v Astra and
Fable 5.1 v Sol 6.1, plus reverse cases. Every quote was checked against `events.jsonl`; the counts are only
supporting evidence.

## The answer

Both labs' good teams start out equally blind (day-1 executions hit evil 46% of the time for Anthropic, 51% for
OpenAI). The gap opens afterwards: from day 2 on, OpenAI towns hit evil 64% of the time and Anthropic towns 41%
(Sol 6.1 rises from 62% to 81%, Opus 5.5 falls from 50% to 47%). The transcripts show why. OpenAI good players
treat each result and claim as **evidence with a source and a failure mode**. Anthropic good players turn results
into **settled facts** and plan on top of them. Supplying such "facts" is evil's job: a poisoned shot, a Librarian
ping built around a hint, a fake Fortune Teller log, a last-second Saint claim. So Anthropic towns reason
carefully, but inside premises that evil chose, and they reach a consensus quickly and rarely re-open it.

## Traits

**1. "Cleared" versus "doesn't clear".** Anthropic towns turn ability results into conclusions and forget the
Poisoner. OpenAI towns say out loud what a result does *not* prove.
- A Slayer shot on the real Imp failed because the Slayer had been poisoned. Opus 5.5's town concluded: "Blair's
  cleared of Imp" (Kit, Chef) and "Blair's clear of Demon." (Casey, Slayer), in `v16/f2-opus55-v-sol61/game-01`
  D2. Blair went on to win. On the same deal, Sol 6.1's town said: "The missed shot doesn't confirm Blair's Monk
  claim." (Frankie, `game-01-swap` D2).
- An Opus 5.5 Fortune Teller judged an Empath who had been poisoned every night: "Alex's 0 is decisive: the Imp
  can't hide from an Empath ... Only a Poisoner breaks that, and it's a stretch." (`v16/f2-gpt56sol-v-opus55/game-01-swap`
  D4). The town executed the Poisoner and lost that night to the Imp it had "cleared".
- Good players' public lines containing "doesn't prove / doesn't clear / not mechanical / not independent" and
  similar phrases: 4.3–12% for every OpenAI model (Sol 6.1 12%, Astra 10.6%), 1.0–2.1% for every Anthropic model
  (Opus 5.5 1.0%). The ranges don't overlap. It is a crude regex count, but it matches what reading the games shows.

**2. Matching claims counted as independent confirmation.** Anthropic towns don't ask who told whom first.
- An Opus 5.5 Recluse whispered to his neighbour: "If anyone's info pings me as evil, just know I may not be what
  it looks like." The neighbour was the Baron, who told his team: "Jules strongly hinted Recluse, so I can build a
  Recluse pair around Jules plus Harper". The Recluse then told the town that the Baron's "Librarian info
  independently confirms a Recluse in play" (`v16/f2-gpt56sol-v-opus55/game-01-swap` D1). On the same seed, Sol
  5.6's Recluse said: "Indigo, your Librarian claim came after I had already told you privately that I was
  Recluse, so it isn't independent confirmation." (`game-01` D2). The Baron was executed that day.
- Opus 5.5's Chef said: "Drew's Saint ping landed before Harper claimed - that's hard for a Minion to fake."
  (`v16/f2-opus55-v-sol61/game-01` D1). A good Soldier was executed on that basis. The correction came a day late:
  "Drew never actually named Saint first - Harper filled it in."

**3. Following the table, and "cheap test" executions.** Anthropic towns agree out loud and spend executions on
players they don't actually suspect. OpenAI towns look at who is pushing the cheap test.
- Fable 5.1 good players on day 2: "I'm with the table on Gray." (twice) and "Same place as the table: Gray
  today." Gray was their real Undertaker, executed with 9 votes (`v16/f2-fable51-v-astra/game-01`). Open agreement ("with the table",
  "agreed", "consensus") appears in 3.1–5.0% of good public lines for Opus 4.7, 4.8 and 5.5 and Fable 5 and 5.1.
  For Astra and Sol 6.1 it is 0.2–0.4% (Opus 4.6 1.5%, GPT-5.5 2.0%).
- Opus 5.5 on day 1: "Gray is the execution today - and executing a Recluse loses us nothing."
  (`v17/f3-opus55-v-sol61/game-03`). The Recluse was good, and so were the next two players executed.
- Sol 5.6 faced the same push in a Baron game: "Executing Drew doesn't actually test anything - his death won't
  reveal Recluse versus Baron." It nominated the player who proposed the test: "Harper's framing of Drew as a
  cheap, useful test was the weakest argument today" (`v17/f3-fable5-v-gpt56sol/game-03-swap` D1). Harper was the
  Imp, and good won on day 1. On the same deal Fable 5's town executed its Soldier on a fake Investigator ping,
  with every other player voting yes: "the chronology favors Gray's story, and Ellis checks the result tomorrow
  either way."

**4. Letting evil set the agenda.** When evil makes a dramatic move, an Anthropic town reacts to it. An OpenAI
town asks who benefits.
- A Scarlet Woman on the block suddenly said: "I need to come clean before this locks: I'm the Saint, not the
  Soldier." Opus 5.5's Virgin replied: "I don't buy a Saint claim at the last second, but I'm not betting the game
  on it." Jules's thinking read: "better to play it safe with Blair." The town voted 8 to swap the execution onto
  Blair, its own Mayor (`v17/f3-opus55-v-sol61/game-02` D2).
- In the same-seed swap, the Opus Spy confessed to save his Imp: "Fine. Frankie's right - I'm the Spy." Sol 6.1's
  town replied: "A confessed evil player telling us Frankie is the wrong execution is not a reason to change
  course." Another player: "let's not give them control of today's choice." The town executed the Imp
  (`game-02-swap` D3).
- Astra's Spy only asked a question: "why kill a spent Slayer instead of the Fortune Teller about to catch him?" An
  Opus 5.5 good player took it up: "Wait. Casey's question is the key." The good players built the rest of the
  frame themselves. They executed their Librarian despite their own Fortune Teller's YES on the Imp, and two days
  later executed the Saint: "Consensus is right; let's lock it in." (`v17/f3-astra-v-opus55/game-03-swap`).
- Across all games, a good team executed its own Saint in 20 of 213 Anthropic-good games (9%) and in 2 of 193
  OpenAI-good games (1%). Opus 5.5 lost three of its four f3 games against Astra this way.

**Evil side.** Astra's and Sol 6.1's evil seats speak 0.49× the public words per seat of good seats; Fable 5/5.1
(1.15–1.19×) and Opus 4.7/4.8 (1.28–1.6×) out-talk good; Opus 5.5 is in between (0.74×). Anthropic evil
teams favour theatrical gambits (late Saint claims, confessions, loud fake Fortune Tellers). In the pairs I read, these worked against Anthropic towns and failed against OpenAI
ones. Astra's evil seats mostly ask questions and let good players draw the conclusions.

## Three side-by-side pairs

**A. The poisoned shot** (`v16/f2-opus55-v-sol61/game-01`, Opus 5.5 good; `-swap`, Sol 6.1 good). In both games
the town executed its Soldier on day 1, and the Slayer, poisoned on night 2, shot Blair, the real Imp, with no effect.

In the Opus game, the town took the miss as a verdict. Its probes put P(Blair is the Demon) at a mean of 0.03 that
day, with all 8 good seats at or below 0.05, and at 0.09 the next day. Blair drew only one nomination all game (3
votes, day 5), and evil won on day 6.

The Sol town treated the miss as one possible world: "In that specific world, this miss rules out Blair as Imp -
not in every world." By the next day it had found the mechanism: "Poisoning Casey wouldn't have been a lucky
guess: Blair and Drew had a Slayer-containing shortlist before that night." That also answered the Opus Imp's
earlier dare ("Casey, if you think I'm the Imp, shoot me now"): "Begging to be shot after the night's poisoning
cannot clear him." Its probe on Blair rose from 0.22 to 0.70; he was executed on day 3.

**B. The fake Fortune Teller** (`v16/f2-fable51-v-astra/game-01`, Fable 5.1 good; `-swap`, Astra good). In both
games Jules, the Poisoner, claimed Fortune Teller.

In the Fable game, his YES pings and a poisoned Undertaker result decided three executions in a row, all by large
majorities: the Undertaker, the Ravenkeeper and the Slayer. The town raised poisoning but preferred the story with one
liar: "One evil Gray explains all of it." On day 5 Astra's Spy said it aloud: "We've followed Jules's information into executing Gray, Blair and Kit." Evil won.

In the Astra game, the same claim was audited at once: "If you're using it to argue for his execution, please give
the exact pair and result so everyone can assess it." The Slayer shot Jules for repeating a corrected argument. He
survived because he was not the Demon, but the town kept the thread. It executed Jules on day 3, then Frankie, the
Imp, on day 4 for defending him: "Calling Frankie your only living clear is another rewrite of your own
information to protect him."

**C. Same mistake, different recovery** (`v16/f2-gpt56sol-v-opus55`: Sol 5.6 good in `game-01`, Opus 5.5 good in
the swap). In both games a fake Investigator ping cost the town a good player on day 1: the Mayor in the Sol game,
the Undertaker in the Opus game.

The Sol town then reasoned across worlds: "Blair is evil in both fully coherent branches" and "I favor Ellis
strongly, not mechanically." It caught the Baron on claim timing (trait 2) on day 2, then executed Blair, the
Imp, on day 3 as the choice that risked no Saint loss.

The Opus town kept its fake Librarian "independently" confirmed and executed the Baron only on day 3. It then
trusted the poisoned Empath's 0 (trait 1). The Imp, claiming Monk, was never nominated.

## Caveats

- **Each swap mixes detection with deception.** The opposing evil team is always the other lab's model. Pair A is
  the cleanest, since the same night actions produced the same failed shot.
- **OpenAI towns make these mistakes too.** Sol 5.6 executed its Mayor in pair C. In
  `v17/f3b-gpt56sol-v-fable51/game-02`, its timing argument misfired: "Alex's exact Investigator pair appeared only
  after both supporting clues were available" got the real Investigator executed, and Fable 5.1 evil won. The
  difference is in how often these mistakes happen and how well the town recovers, not in kind.
- **Some of this is generation, not lab.** GPT-5.4 and 5.5 hedge more than any Claude model yet still lose often
  as good.
- **Selection.** I chose pairs whose outcomes diverged; the regex counts are crude.
- **Visibility.** OpenAI reasoning is encrypted (outputs and probes only); Claude's mistakes are easier to see.
