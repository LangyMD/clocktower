# W1 realism: a close read of private time, 4 beats vs 6

Reader W1-realism. I only read files: no games run, no API spend, no repository files edited. I read as a
Trouble Brewing player and Storyteller would, and kept the numbers to a few counts that back up what I saw.
The thread-length statistics are in W1-conversation.md and I don't repeat them.

## What I read

**End to end (every whisper, speech, nomination and vote):**

| Game | Beats | Good vs evil | What happened |
|---|---|---|---|
| opus55-v-sol61/game-04 | 4 | Opus vs Sol | Fortune Teller and Investigator overlap on Frankie. The Spy dies on day 1. The Imp starpasses to frame the Saint and fails. Good wins on day 2. |
| opus55-v-sol61/game-01 | 4 | Opus vs Sol | The Scarlet Woman frames the Ravenkeeper. On the last day the town talks itself onto a Minion while the Imp stands by. Evil wins on day 5. |
| fable51-v-astra/game-01 | 4 | Fable 5.1 vs Astra | The Poisoner volunteers to test the Virgin and the test fails. The Imp fakes a Fortune Teller YES and is caught. Good wins. |
| opus55-v-sol61-b6/game-02 | 6 | Opus vs Sol | The Spy claims Saint to clash with the real Saint. The town avoids both claimants for two days, then executes the real Saint. Evil wins on day 3. |
| sonnet55-v-sol61-b6/game-01-swap | 6 | Sol vs Sonnet 5.5 | A Drunk Investigator, a missed Slayer shot, and an Empath reading of 0→1→0 that catches the Poisoner. The Imp is executed on day 3. |
| fable51-v-astra-b6/game-01-swap | 6 | Astra vs Fable 5.1 | A Virgin test is arranged and the two Empath claims settle into a coin flip. Then the Slayer shoots the Imp on day 1. |

**Private time only, plus the square where needed:**
- opus55-v-sol61 game-05 (days 1–2) and game-05-swap.
- opus55-v-sol61-b6 game-01 (days 3–4 plus the final square), game-03 (day 1) and game-04-swap (day 1).
- sonnet55-v-sol61/game-02 (day 1, Sonnet 5.5 as good).
- gpt4o-v-sonnet45/game-01 (day 1), for contrast.
- Sampled three-way relay chains from every Opus/Sol game in both formats.

The scripts are in `scratchpad/readers/`:
- `rr.py GAME DAYS [private]` prints a readable game with each seat's character.
- `rstats.py` counts swarms.
- `rchain.py` and `rloop.py` find three-player chains.
- `ropen.py` measures the day-1 opening whisper.

## Verdict in five lines
- **These are good Clocktower games.** The plots are the real Trouble Brewing plots: a Saint double-claim, a Virgin test arranged by committee, a Drunk confirming a Minion, a starpass framing, a Mayor's last stand. Each is argued out with real table logic. Good players trace leaks and check when things were said; evil players adapt their bluffs to what the Spy saw.
- **Private time reads like a real table, but like one run by email.** Each whisper is a dense little report: a claim, two relayed claims and a question. There is almost no small talk and no reading of tone. Conversations are message-passing more than chat.
- **4 beats is enough for one good exchange per pair. It is not enough for a day.** Most day-1 threads at 4 beats stop when they get interesting: the check with a third player, or the confrontation, lands in beat 4 with no room to answer it.
- **6 beats feels like a real day 1.** Three-way huddles form, a Virgin test gets organised, leaks get traced to their source, and handshakes that start slow get finished. On later days beats 5–6 are mostly quiet or "agreed, X today", which is realistic and cheap.
- **Recommendation: 6 beats, every day** (5 if cost forces it). One small rule change would add the thing a real day has that this one lacks: a little private time *after* the town square.

---

## 1. How realistic, interesting and diverse?

**Realistic.** I would accept almost every strong-model game I read as a transcript of a competent human table, with three exceptions:
- **Nobody hesitates, and nobody plays on vibes or social reads.**
- **Everyone is reasonable.** The angriest line in six games is a dead Spy's fake confession mid-vote: "Fine. I'm the Spy; Drew was the Imp. Harper was Baron and is now Imp." It is a deliberate scramble (opus/game-04, day 2).
- **The dead are far more active than at a real table.** Ghosts whisper the living every beat and swing final votes. Dead Casey's pleading swung the final vote in opus-b6/game-01. In game-02 a different dead Casey's defence of Kit backfired: the town read it as the Spy protecting the Imp.

The Storyteller's setups produce exactly the dilemmas experienced players love:
- Two Saint claims next to each other.
- A Librarian Saint ping on two people who both deny it.
- A Drunk Washerwoman whose false confirmation makes the Scarlet Woman look trusted.
- A Virgin test whose volunteer turns out to be the Drunk. In opus-b6/game-04-swap, Casey, the Drunk who thinks they are the Washerwoman, nominated the real Virgin, nothing fired, and the Virgin was executed.

**Interesting.** The best moments are about *private information as evidence*:
- **Who knew what, and when.** "Who told you I had a ping on you? I only told two people."
- **Whether a claim was made before or after hearing a result.** "Gray claimed Librarian before I revealed that."
- **Whether a whisper says what someone says it said.** In fable/game-01, Alex quotes Drew's whisper "Casey has that claim too" in the square, and the two argue in public about what it meant.

About 5% of public speeches refer to the provenance or timing of private talk. That is the part of Clocktower that makes private time matter, and it is clearly working.

**Diverse in plot, formulaic in rhythm.** Section 5 covers this.

---

## 2. What a day looks like

### Day 1, 4 beats (Opus good vs Sol evil, opus55-v-sol61/game-04)

**Beat 1.** The evil team huddles, as it does in 39 of 40 games:
- The Baron asks for bluffs.
- The Spy dumps the whole Grimoire ("Jules is a priority kill. Executing Gray wins outright").
- The Imp hands out Ravenkeeper, Virgin and Undertaker.

Meanwhile nearly every good player opens to their two neighbours:
- Ellis: "Hi neighbours. I'm the Chef: I got 0 pairs."
- Gray: "Straight up: I'm the Saint."
- Indigo, the Librarian, asks Alex and Harper which of them is the Butler.

Harper answers inside the same beat, because she acts in a later wave. Casey (Fortune Teller) asks Blair to trade. Blair (Investigator), also a wave later, replies "Happy to trade... You go first."

**Beat 2.** Second-round threads start:
- Casey gives Blair the Fortune Teller result.
- The Imp and the Baron start feeding fake claims to the people who asked.
- Ellis widens out to Casey and Gray.

**Beat 3.** Answers arrive:
- Blair gives Casey the Spy pair.
- Several players start relaying ("Harper says Butler, and Indigo's info backs that").
- Indigo chases the one quiet player, Alex.

**Beat 4.** People summarise and plan. Casey writes to Blair: "Let's not dump everything in town yet, just steer toward Frankie." Some last questions go out with no chance of an answer. Blair finally asks Gray "What's your role?" and the town square opens.

**What it feels like.** Each player has had about two real conversations. Most of what they heard is secondhand. They walk into the square knowing a lot, but not having *tested* anyone.

### Day 1, 6 beats (opus55-v-sol61-b6/game-03 and game-02)

Beats 1–4 look the same. Then:

**Beat 5.** The slow threads close:
- Casey: "Still keen to hear your pair, Ellis. I've given you my role, so your turn." Ellis answers.
- Drew, the Investigator, finally asks Alex: "Who told you I had a ping on you? I only told two people."
- Alex, the Spy, names his own Imp: "Ellis mentioned you had a ping on me."

**Beat 6.** People make records and plans:
- Ellis, the Fortune Teller: "For a record if I die: I'm actually the Fortune Teller. Night one, Drew/Frankie gave YES." He told Gray, who was the Scarlet Woman. Gray relays it to the Imp, and Ellis dies that night.
- Frankie tells the Fortune Teller whom to check tonight.

**What it feels like.** By the square, people have tested each other, three-way huddles have formed and dissolved, and players walk in with *plans* ("Ellis nominates, Drew is backup").

### A later day, either format

**Beat 1 is a swarm.** Everyone mobs whoever holds the night's information:
- The dead Ravenkeeper.
- The Undertaker.
- The Empath whose neighbour just died.

In opus/game-04, day 2, beat 1, *seven* players send dead Drew the same message: "If you're really the Ravenkeeper, who did you pick and what did you see?" Drew answers his own team. In beat 2 the same seven ask Casey "what did you check last night?"

**Numbers:**
- In 54% of 4-beat beats (41% at 6), some player receives four or more whispers in one beat.
- On days 2 and later, beat 1 almost always has such a swarm.
- Only 63% of the swarmers (71% at 6) get a private answer that day. The rest hear it in the square.

**The middle beats** are theory-building. Players trade "worlds" in two-player whispers: "Two worlds: (A) Drew good RK, Gray = Spy... (B) Drew was Imp, starpassed."

**The last beats:**
- At 4 beats they are vote-counting.
- At 6 beats, beats 4–6 thin out to a few whispers: "I'm in. Casey today."

**The final day** at 6 beats is the most human scene in the data. In opus-b6/game-01 (4 alive), beats 3–6 are just Alex, the real Mayor, lobbying the two swing votes one by one: "A good player loses nothing by waiting; only evil needs the hang TODAY." One of the people he is pleading with is the Imp, Frankie. Frankie calmly turns him down in private, then Alex wins the square and the town hangs its own Slayer.

---

## 3. The best and worst threads

### 4 beats: best

**1. The FT/Investigator trade (opus55-v-sol61/game-04, day 1).** Casey is the Fortune Teller; Blair is the Investigator.
- b1, Casey → Blair: "I have some info from last night that could matter a lot. What's your role? If you tell me, I'll trade."
- b1 (later wave), Blair: "Happy to trade. I'm the Investigator, and I've got a Minion ping on two specific players. You go first."
- b2, Casey: "Fortune Teller. Checked Drew + Frankie last night: YES... Your Minion ping names?"
- b3, Blair: "My ping: Gray or Frankie is the Spy. Frankie overlaps with your Drew+Frankie hit... Check Frankie+Gray tonight?"
- b4, Casey: "Good overlap. If Frankie's Spy then Drew's likely my Demon hit... Let's not dump everything in town yet, just steer toward Frankie."

The Spy, Frankie, is executed that day. This is the ideal 4-beat thread. The same-beat reply in b1 saves a whole beat, and it still uses all four.

**2. A last-day lobbying cascade (opus55-v-sol61/game-01, day 4, 4 alive).**
- b2: Gray, the Slayer, sells the "Harper starpassed to Indigo" theory.
- b3: He asks the ghosts for votes on Indigo.
- b3, Drew (dead Chef) → Casey, Indigo: "Gray just whispered me begging ghost votes on INDIGO... That's the Imp steering the final vote onto a good player... Do NOT execute Indigo." Drew does not know Casey is the real Imp.
- b3, Casey → her team: "I'll join their theory; don't fight so hard that they reconsider me."
- b4, Casey → Drew: "the starpass theory doesn't break my Alex/Jules ping."
- b4, Drew: "You've convinced me, I retract."

The town hangs Indigo (the Poisoner), and the Imp wins at final two. A ghost relays one player's lobbying to a third player, who happens to be the Imp, and the Imp talks him out of it. That is real table politics, all inside four beats.

**3. A frame relayed and defused (fable51-v-astra/game-01, day 2).** Drew is the Imp, bluffing Fortune Teller.
- b2, Drew → Jules: "Last night I checked you and Harper: YES."
- b3, Jules → Casey: "Heads up: Drew just whispered me that his FT check last night was me + Harper = YES. Very convenient frame the same morning your number lands on me and Drew."
- b4, Indigo (Slayer) → Harper: "I'm going to shoot Jules in town. If nothing happens, Drew's 'yes' was a lie... and we execute Drew."

The shot misses, Drew is hanged, and the Empath's numbers confirm it. Same game, day 1: Casey offered Blair "I'll go second", got Blair's Virgin claim, and never replied. Blair opens the square with "Casey asked to swap claims, I gave mine, and never got one back. Casey, what are you?" A dropped private thread becomes public evidence, exactly as at a real table.

### 4 beats: worst

**4. The swarm (opus55-v-sol61/game-04, day 2).** Seven identical "who did you pick?" whispers go to a dead Ravenkeeper claimant who can answer at most two people. In beat 2 the same seven swarm Casey. Two of four beats go to everyone asking one person the same question. At a physical table that person would say it once to the group, or the crowd would wait for the square.

**5. The confrontation that comes too late (opus55-v-sol61/game-05-swap, day 2).**
- b2, Alex (Drunk; he thinks he is the Ravenkeeper) → Gray: "I checked Harper: I learned Monk."
- b3, Gray → Blair: "Alex privately claims Ravenkeeper and seeing Harper as Monk; I'd like your exact result."
- b4, Blair → Alex, Gray: "Gray, was Alex's Harper-as-Monk result locked with you before he heard mine?"

This is the exact A-tells-B, B-checks-with-C, C-confronts-A loop the user asked about. It closes in the last beat, so nobody can answer it before the square. Across Opus/Sol, many of the closed loops I sampled at 4 beats end in beat 4 this way.

**6. Older models, for contrast (gpt4o-v-sonnet45/game-01, day 1, GPT-4o as good).**
- b1, Drew → Ellis: "Hey, can we chat for a moment? I have something important to share."
- b1, Ellis: "Sure, what's up?"
- b2, Drew: "I'm the Saint."
- Gray (Butler), to the Baron who has just fake-claimed Butler: "I'm the Butler too, funny enough. I picked you. Let's keep each other updated!"

At 4 beats, a model that spends a beat on "can we chat?" has two beats left.

### 6 beats: best

**7. A leak traced to its source over two days: Drew → Ellis → Alex → Drew → Ellis (opus55-v-sol61-b6/game-02).** Drew is the Investigator; Ellis is the Imp, claiming Monk; Alex is the Spy.
- D1 b3, Drew → Ellis: "Investigator. I saw 'Casey or Alex is the Spy'... Keep it quiet for now."
- D1 b3, Ellis → his team: "he shared the Casey/Alex Spy ping."
- D1 b4, Alex → Drew: "I've heard you have an Investigator ping involving me."
- D1 b5, Drew → Alex: "Who told you I had a ping on you? I only told two people, so I want to know who's passing it around."
- D1 b5, Alex: "Ellis mentioned you had a ping on me."
- D2 b1, Drew → Ellis: "Why did you tell Alex about my ping yesterday? Not accusing."
- D2 b2, Ellis: "You'd asked me to keep it quiet, though - that was my mistake."

The Spy carelessly names his own Imp, and the Imp has to own it. The key exchange happens in beat 5.

Same game, day 3:
- b5, Gray → Harper, Frankie: "Odd: Kit already whispered me that your Kit/Gray was YES before it was public. Harper, did you tell Kit? I told Ellis only."
- b6, Harper (the Scarlet Woman, choosing honesty to stay credible): "Yes, I told Kit and Blair together when they asked. Nothing suspicious about Kit knowing."

**8. A three-way huddle (opus55-v-sol61-b6/game-03, day 1).** Alex is Drunk and thinks he is the Librarian.
- b1, Alex → Blair, Frankie: "One of you two is the Saint. Which of you is it?"
- b2: Blair denies.
- b3, Frankie → Alex, Blair: "I'm not the Saint - I'm the Washerwoman."
- b4, Blair → Alex, Frankie: "So one of you is off - Alex drunk/lying, or Frankie a Spy registering as Saint, or Frankie hiding."
- b5: Alex takes it to two more players.
- b6, Frankie → Kit (Fortune Teller): "check Alex + Blair tonight - one of them is off."

Three people use two-recipient whispers to hold an actual group conversation, reach "something's off", and hand it to the Fortune Teller. This is the closest thing to a real-table huddle in the data. At 4 beats it would have stopped at Blair's analysis.

**9. Organising a Virgin test by committee (fable51-v-astra-b6/game-01-swap, day 1).**
- b1, Harper (Virgin) → Gray: she wants a spent information role to nominate her.
- b3, Gray → Ellis, Harper: "would you two be happy to arrange that?" Gray introduces two people who haven't spoken.
- b3: Ellis and Drew both volunteer.
- b4, Harper → Ellis, Drew: "Let's use Ellis as the sole nominator today, with Drew as backup."
- b6, Drew → Harper, Ellis: "Could we switch to me testing Harper? A trigger would rule out me being the Drunk."

Harper switches testers in the square. This is precisely how a day-1 Virgin test is set up at a real table. It takes all six beats.

**10. Trust placed in the wrong person (opus55-v-sol61-b6/game-04-swap, day 1).**
- b5, Casey (Drunk; thinks she is the Washerwoman) → Alex, Gray: "Connecting our independent claims: Alex told me Butler before hearing any ping; Gray told me Librarian, seeing Alex or Ellis as Butler."
- b6, Ellis (Fortune Teller) → Gray: "For a record if I die: I'm actually the Fortune Teller. Night one, Drew/Frankie gave YES."
- b6, Gray (the Scarlet Woman, who looks confirmed thanks to the Drunk) → Imp: "Kill Ellis tonight."

Ellis dies that night. The tragedy depends on beats 5 and 6.

### 6 beats: worst

**11. Extra beats used as a broadcast (sonnet55-v-sol61-b6/game-01-swap, day 3, Sol as good).** Kit, the dead Undertaker, sends almost the same sentence in three consecutive beats to three different pairs:
- b4: "Casey's failed shot happened before Alex's execution. If Alex was the Imp, a Scarlet Woman... could have inherited."
- b5: "Casey's failed shot was before Alex's execution. If Alex was the Imp..."
- b6: "Casey's failed shot was before Alex's execution..."

On the same game's day 1, Gray (Monk) sends six "trade threes?" or "any first-night lead?" whispers. By b6 he reports: "I offered Frankie and Harper Monk/Soldier/Ravenkeeper but haven't had replies."

**12. A handshake that takes five beats (fable51-v-astra-b6/game-01-swap, day 1).** Logan is the Drunk and thinks he is the Washerwoman.
- b1, Logan → Jules: "I've got starting information involving you. Would you give me a private claim before I say what it is?"
- b2, Jules: "I'm the Empath. What starting information did you get?"
- b3, Logan: "I'm the Washerwoman; you and another player are my pair... What's your first Empath number?"
- b4, Jules: "lock which Townsfolk you saw before I give the number."
- b5, Logan: "I saw Ravenkeeper."

Two facts traded in five beats. Six beats lets over-cautious play finish, but it also shows how procedural the "you go first" ritual has become.

**13. Late-day quiet (opus55-v-sol61-b6/game-01, day 3, 6 alive).** Whispers per beat: 10, 10, 3, 3, 3, 4. Everything after beat 2 is "Casey today, Alex tomorrow" and "I'm in. Casey today." It does no harm: silent turns are nearly free, and real tables also go quiet late. But it is filler.

---

## 4. Judgment as a Clocktower player

**Does 4 beats feel cramped? Yes, on day 1, and on any day with a fresh revelation.**
- At a real table, the first private chat of day 1 runs 5–10 minutes. A player has three to five conversations, each several exchanges long, and comes back to check.
- At 4 beats a player has one real exchange with their neighbour and one with someone else. Everything else they know is relayed.
- The interesting structure, test then cross-check then confront, needs three beats after first contact. At 4 beats it usually runs into the square.
- The standard handshakes (Washerwoman/Librarian/Investigator "you go first", Virgin-test volunteers, Empath/Fortune Teller trades) eat the first two beats.
- My counts are crude (name mentions), but they agree. Per day:
  - Three-player triads (each whispered the other two): 6.4 at 4 beats, 16.6 at 6.
  - A-tells-B-about-C, B-takes-it-to-C chains: 14 at 4 beats, 22 at 6.
  - Fully closed loops (C then comes back to A about B): 3.2 at 4 beats, 5.9 at 6.

**Does 6 feel like a real day? On day 1, yes, for the first time in this protocol's history.**
- Beats 5–6 are where leaks get traced, huddles conclude, tests get organised, and "records if I die" get left.
- On later days 6 is more than needed. Beats 4–6 thin out, as at a real table where late-game private chat is short and pointed.
- The fixed-length rule means you pay for those quiet beats. In the matched Opus/Sol set, cost per game-day was essentially unchanged ($1.33 at 6 vs $1.34 at 4, all phases). The earlier reader measured about +10% private spend.

**What's missing compared with an in-person game:**

1. **Coming back after the square.** At a real table the day isn't private-then-public-then-vote. People step aside again after the claims come out ("you said Chef in the square, but you told me Soldier"), and between nominations. Here, everything private happens *before* the public claim dump, so private follow-up on public claims waits a full night. This is the biggest gap.
2. **Seeing who talks to whom.** In person you notice the Imp and a Minion stepping aside together, and that someone has talked to everyone but you. Here, networks become evidence only secondhand ("I only told two people"). Evil's beat-1 team huddle, which happens every game, would be the first thing a real table noticed.
3. **Group conversations bigger than three.** The two-recipient cap allows three-way huddles (and they happen), but not the 4–5 person cluster that forms around a confirmed player. The swarm on the dead Ravenkeeper is that cluster trying to form and being forced into single file.
4. **Tone, hesitation and small talk.** Whispers are compact reports; nobody "seems nervous". This is a model trait, not a protocol problem, and arguably right for an eval.

**What's better than in person:**
- **Rigour.** Every claim is tracked, timing is checked ("claimed before hearing my result"), and worlds are enumerated. Even weak players never forget who told them what.
- **No social exclusion.** Quiet players get asked; nobody is left out of the loop because they're shy.
- **Ghosts stay in the game,** often decisively, where human ghosts tend to drift off.
- **Lies about private conversations are a real weapon,** because nobody can check them. The dead Spy's line "Jules, you told me privately this morning that you protected Gray" (Jules never said it) is exactly the in-person bluff, done well.
- **The reader sees everything.** Every one of these games is a perfect Grimoire replay.

---

## 5. Diversity

**Plots are diverse.** The six games I read end to end turned on six different mechanics:
1. FT/Investigator overlap plus a Saint-framing starpass.
2. A framed Ravenkeeper and a final-day starpass.
3. A poisoned Virgin test.
4. A Spy/Saint double claim.
5. A Drunk Investigator plus an Empath 0→1→0.
6. A double Empath claim and a day-1 Slayer kill.

The side-swapped pairs share a setup, so they share a central conflict (both b6/game-02 games revolve around the Spy's Saint counter-claim), but they diverge in play and result.

**Rhythm is formulaic:**
- **Beat 1 of day 1 is the same in every game.** Evil huddles. 70–80% of good players' first whispers go only to their two neighbours: Opus 68%, Sol 6.1 80%, Astra 88%. Opus opens with "Hey neighbours" 71% of the time.
- **Each model has its own day-1 dialect.** Sol 6.1 and Astra trade "three-for-threes" (Sol does this in 29% of first whispers, an authentic experienced-player habit). Opus and Fable hard-claim to neighbours or fish with "I have info involving you, you go first". Sonnet 5.5 hard-claims almost always (88%).
- **Later days always open with a swarm** on the night's information holder.
- **The square follows its own pattern:** day-1 square 1 is a claim dump. About 60% of good players hard-claim publicly on day 1 (the earlier reader's figure).

None of this is bad. Real groups have house rituals too. But a viewer will recognise "Hey neighbours. I'm the Chef: I got 0" by the third game.

---

## 6. Recommendation and two protocol ideas

**Recommendation: 6 private beats, every day.**
- **Confident** that it makes day 1 read like a real Clocktower day: the threads that make these games interesting (leak traces, three-way huddles, organised tests, confrontations) mostly land in beats 5–6.
- **Moderately confident** that it is worth it on later days, where beats 5–6 are mostly quiet. The cost is small because silent turns are cheap.
- **If budget forces a compromise, 5 beats.** It keeps most closing confrontations and cuts the late-day dead air.
- It does not change balance detectably: evil won 5/12 at 6 beats vs 12/38 at 4, with wide intervals (W1-balance).

**Idea 1 (my preferred change; fairly confident it is clean): split private time around the town square.**
- One line: *"Private time comes in two parts: four beats before the town square and two after it, before nominations."*
- Same six beats, and the same cost as 6.
- It gives players what a real day has and this one lacks: a chance to step aside *after* the public claims and say "you told me Soldier, you just said Chef", line up votes, or check a new claim with its info holder.
- It also uses the dead air of late-day beats 5–6: they would sit after the square, where there is something new to discuss.
- Untested, so run a small pilot first. I expect it to raise good's checking power slightly and evil's vote-coordination power slightly.

**Idea 2 (realistic, but test before adopting; less confident): show who whispered whom.**
- One line: *"After each private beat, everyone sees who whispered whom, but not what was said."*
- This is the in-person signal of seeing two people step aside.
- It would make networks real evidence and force evil to camouflage its beat-1 huddle, as at a real table.
- The risk is balance: evil briefs both teammates in beat 1 in 39 of 40 games, so a model that doesn't adapt is exposed on day 1. That tests adaptation as much as deception.
- Worth a w2-style test, not a direct adoption.

I would not change the one-whisper rule or the two-recipient cap. The cap creates the one-at-a-time choices that make "who did you tell?" meaningful, and three-way huddles already form within it.
