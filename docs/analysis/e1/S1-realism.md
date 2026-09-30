# S1: realism and interest in v9 e1

Reader S1. I only read files: no runs and no API spend. I skimmed R1–R5 and do not repeat their findings, except to point to them.

Scratch tools (all in `scratchpad/s1/`):
- `r.py`: a compact omniscient render. Every name is tagged with its character, and it shows whispers, speech, nominations, votes compressed to one line, and night choices.
- `stats.py`, `dead.py`, `comm.py`, `kw.py`, `claim.py`: counts over every e1 game. Most counts use the 53 games that had finished by the end of my read. `claim.py` also covers games still in progress, because it only looks at day 1.

## Games read

| Game (games/v9/…) | Good vs evil | Size | Result | How closely |
|---|---|---|---|---|
| e1-gpt56sol-v-opus55/game-01-swap | Opus 5.5 vs GPT-5.6 Sol | 12 | evil D5 (Saint executed) | every line |
| e1-opus55max64k-v-gpt61sol/game-01 | Opus 5.5 max vs Sol 6.1 | 12 | good D3 | every line |
| e1-opus55medium-v-gpt61sol/game-01 | Opus 5.5 medium vs Sol 6.1 | 11 | evil D5 (Mayor final 3) | D1, D5 in full; the rest skimmed |
| e1-gpt52-v-o3/game-01-swap | o3 vs GPT-5.2 | 10 | evil D5 | D1–D3 in full |
| e1-sonnet45-v-gpt51/game-01 | Sonnet 4.5 vs GPT-5.1 | 10 | evil D5 | D1–D2, D5 in full |
| e1-gpt61sol-v-astra/game-01 | Sol 6.1 vs Astra | 10 | good D4 | D1–D2 in full, then public talk |
| e1-opus46-v-gpt55/game-01 | Opus 4.6 vs GPT-5.5 | 12 | evil D6 | D1 in full; the rest via key events and votes |
| e1-gpt55-v-fable51/game-01 | GPT-5.5 vs Fable 5.1 | 12 | evil D6 | D1 in full; the rest via key events |
| e1-o3-v-astra/game-01 | o3 vs Astra | 11 | evil D5 | D1–D2 public talk; the rest via events |
| e1-gpt54-v-opus48/game-01-swap | Opus 4.8 vs GPT-5.4 | 10 | evil D3 (Saint executed) | events, and evil whispers at the key turn |
| e1-gpt61solmax-v-opus55/game-01 | Sol 6.1 max vs Opus 5.5 | 12 | good D3 | D1–D3 public talk |
| e1-fable5-v-opus47/game-01-swap | Opus 4.7 vs Fable 5 | 11 | evil D3 (Saint executed) | events only (R5 covers it) |

## 1. Verdict

**The best e1 games are real Trouble Brewing, and they are interesting.**
- They have genuine turning points and well-executed bluffs.
- Several endgames are as good as strong human play.
- The Storyteller's misregistration produces exactly the chaos that makes human games memorable.

**What stops them reading like a human table is mostly the talk itself:**
- Everyone speaks every beat, and every nomination gets a full round of comments and vote remarks.
- A one-model good team reasons as one mind and says the same thing many times.
- The diction is legalistic and almost all mechanics, with no social play and no humor at all.
- Whisper volume means nearly every claim reaches nearly every seat on day 1.

**Which of these are fixable:**
- Some come from the models. That is fine; it is what we measure.
- Three come from the conversation structure and are fixable with one-line rules: turn order inside a beat, whisper volume, and the ritual turns of each nomination.

## 2. What already works: moments a human would call a great game

1. **gpt56sol-v-opus55/game-01-swap. Sol evil against Opus good, 12 players, evil won on D5.**
   - D1: Blair, the Spy, claimed Chef and gave the *true* number: "I'm the Chef and got a 1."
   - Jules's real Washerwoman ping ("Gray or Blair is the Chef") then "confirmed" her. That true "1" sold out her own Imp and Baron.
   - D1: Frankie, the Baron, publicly fake-shot his own Imp: "I'm the Slayer… I'm shooting Ellis now." That "cleared" Ellis, and the town executed its own Butler 11–0.
   - D3: good solved the Chef pair. Evil bussed the Baron: Ellis the Imp *nominated* Frankie.
   - D4: the Spy talked the town into an "ordering play" that executed the real Recluse.
   - N5: the Imp starpassed to the Spy, the one player the whole town trusted.
   - D5: the town executed the real Saint, who had claimed Saint in public on D1. His last line: "remember: the Saint rule ends it."
   - It is a five-day game with a real reversal, and every evil move is one a strong human would recognise.
2. **gpt54-v-opus48/game-01-swap, D2. GPT-5.4 evil.**
   - The Imp, Alex, was on the block at 6 votes.
   - The Spy, Frankie, then nominated the Virgin, and the Storyteller registered him as a Townsfolk. The Virgin executed Frankie on the spot, which used up the day's execution, so Alex survived.
   - The day before, the Imp had whispered, "one of us can safely test Blair later if we want to muddy Virgin."
   - Frankie died looking "confirmed good." The Imp then starpassed, and the town executed the Saint on D3.
3. **opus55medium-v-gpt61sol/game-01, D5 final three (the Mayor, the Imp-by-starpass Indigo, and Blair).**
   - Good worked out the Mayor line. It needed no execution, and it would force a tie if anyone nominated Harper.
   - Two evil ghost votes put Harper on the block 2–2.
   - Harper counter-nominated Blair "purely to tie. We need exactly 2 yes votes: me plus one ghost." Alex warned, "Gray, if anyone before you sneaks a yes, hold yours."
   - Indigo sat after Gray and Harper in the clockwise order. Indigo voted yes, making it 3, and Blair was executed. Evil won.
   - This is real tension, created by the clockwise vote and ghost-vote arithmetic, and good made a real mistake.
4. **o3-v-astra/game-01, D1–D2. Astra evil, o3 good.**
   - The town executed Frankie, the Recluse, on D1.
   - The Storyteller showed the real Undertaker "Frankie was the Imp."
   - The Imp, Kit, claiming Slayer, then "shot" the Undertaker and "missed." The town executed its own Undertaker D2.
   - Later a Scarlet Woman caught the Imp and starpassed the same night.
   - This is classic Storyteller chaos, and it makes a good story.
5. **gpt55-v-fable51/game-01, D1. Fable 5.1 evil.**
   - Jules privately claimed Saint to Kit, the Scarlet Woman.
   - Kit to the team: "Don't kill Jules — we want the town to execute them. I'll play trusted Ravenkeeper and slowly build a case on Jules over a couple of days."
   - GPT-5.5 good ran a proper soft-claim meta: "3-for-3" trades, and roles held back.
6. **opus55max64k-v-gpt61sol/game-01. Opus 5.5 at max effort, good.**
   - This is the most human-sounding good team in e1: "Straight up: I'm the Saint", "Deal's a deal", a Ravenkeeper hiding to draw the kill.
   - It reasoned about behaviour, not only mechanics:
     - D2: "Teammates don't out their own Spy."
     - D3: "Evil distances from doomed teammates, it doesn't hand over healthy ones."
     - D3: "Drew nominating a Chef who was already going to die costs him nothing."
7. **gpt52-v-o3/game-01-swap. GPT-5.2 evil.**
   - The Imp offered o3's Investigator a "role swap" and wore his Investigator result in public, while Casey hid as "Chef 0."
   - The Baron faked Undertaker ("Drew was the Baron") to confirm the Imp's borrowed ping.
   - Dead Drew spent two days shouting "I was the VIRGIN" from the grave, and nobody believed him.

Endgames are often the most interesting part: ghost-vote plans, Mayor ties, starpass timing, Saint gambles. Length is healthy. Of 53 finished games, 9 ended on D1–D2, 23 on D3–D4 and 21 on D5–D7. Evil won 16 of 53.

## 3. What is unlike human play

### A. The town square is rounds of statements, not a conversation (structure plus models)

**Everyone gets a turn every beat.** Older models take nearly all of them; newer ones take most.

| | Share of public beat turns with speech | Median words per statement |
|---|---|---|
| o3, GPT-5.1, 5.2, 5.4, 5.5, Opus 4.5–4.8, Fable 5 | 93–100% | 43–84 |
| Opus 5.5, Sol 6.1, Astra, Sonnet 5.5 | 65–80% | 35–46 |

The prompt asks for "one to three sentences, rarely more than 60 words".

**Groups of three act simultaneously.** Players can react only to earlier groups, so the same ask gets made six times, often while its target is answering in a later group.
- opus46-v-gpt55/game-01, D1 town square 2: six players make the same point in near-identical words:
  - Drew: "A no-execution Day 1 is a gift to the Demon"
  - Blair: "Drew's right that passing Day 1 is a gift to the Demon"
  - Jules: "passing Day 1 just hands the Demon a free kill"
  - Ellis: "Kit's right — passing Day 1 is a free night for the Demon"
  - Indigo: "passing Day 1 just hands evil a free night"
  - Frankie: "passing today just gives the Demon a free kill"
- Same game, town square 3: six players ask Kit for his two names, and Kit gives them in the middle of that beat. Alex, who spoke after Kit, still said: "Kit, we're out of time — drop those two names now."
- gpt52-v-o3/game-01-swap, D3 town square 1: Alex, Harper, Gray, Frankie and Indigo all ask Jules for his Undertaker read. Jules gives it in the same beat.
- gpt56sol-v-opus55/game-01-swap, D1 town square 1: "Librarian, if you exist, now's the time" three times, from Logan, Indigo and Kit.

### B. Ritual turns on every nomination (structure plus models)

**Each nomination adds a comment turn for all 10–12 players, then a vote remark for each.**

| | Comment turns used | Vote remarks used |
|---|---|---|
| o3, GPT-5.1, 5.2, 5.4, 5.5, Opus 4.5, 4.7, 4.8, Fable 5 | 96–100% | 47–96% (older GPT and Opus 4.8) |
| Sol 6.1, Astra, Opus 5.5, Sonnet 5.5 | 35–48% | 2–15% |

The filler repeats from game to game:
- "Voting yes." ×5 (gpt56sol-v-opus55 swap D1)
- "Saving my ghost vote; living votes have this." (gpt55-v-fable51, every late nomination)
- "Saving my ghost vote for tomorrow if needed. This has the numbers." ×3 in one roll (opus46-v-gpt55 D5)
- "No. Nobody dies today." ×6 (opus55medium D5)

These are not all noise, though. Remarks like "Harper, nominate Blair; ghosts tie it at exactly 2" were real coordination in the best endgame.

### C. Hive-mind good team (mostly the homogeneous-team design; amplified by volume)

A single-model team reaches the same conclusion at the same time, and every seat broadcasts it.
- gpt56sol-v-opus55 swap, D3 private time 1:
  - Nine different good players (Kit, Alex, Indigo, Casey, Logan, Jules, Harper, Drew; Gray too) whisper essentially the same "Chef math" message: "the only possible adjacent evil pairs are Ellis–Frankie or Frankie–Gray. Frankie is in both."
  - They mostly send it to the same two "confirmed" players, Logan and Blair. Blair is the evil Spy.
  - Then all nine say it again in town square 1.
- sonnet45-v-gpt51/game-01:
  - D2: "Blair's right" ×5, in one beat.
  - D5: six dead good players repeat "The logic is clear: if Jules is Drunk, they're NOT the Empath character… Gray is the Demon."
- **Unanimous votes that include evil.** Humans usually have holdouts:
  - Casey 11–0 (gpt56sol swap D1)
  - Casey 10–0 (gpt61sol-v-astra D1, with the nominee voting yes on his own execution)
  - Jules 10–0 (opus55medium D1)
  - Logan 0–12 (gpt61solmax D1)

### D. Mechanics nearly crowd out social play and humour (models)

**Behavioural vocabulary is rare in public statements.** I counted "defensive", "gut", "vibes", "tone", "too quiet", "convenient" and similar words:
- Opus 5.5 and Fable 5.1: 3%
- Sol 6.1: 6%
- Sonnet 4.5: 10%
- Opus 4.8: 13%, the highest

**Mechanical vocabulary is common.** Words like "ping", "registers", "world" and role names appear in 40–80% of statements.

**Humour is essentially absent.** A search for joke markers found one match in about 7,000 good-side statements. The prompt explicitly invites players to "joke". Frankie's "Quick update from the great-beyond" (o3, dead Recluse) is about as playful as it gets.

**Diction:**
- Sol 6.1 is legalistic and hedges everything:
  - "That's my lead, not a guarantee I'm sober and healthy" (gpt61sol-v-astra D1)
  - "four Demon negatives, not four alignment clears"
  - "That's a counterexample, not a claimed solve" (opus55max D2, evil Sol)
  - Hedge phrases appear in 20% of its good statements, 35% at low effort.
- o3 and GPT-5.2 write memos:
  - bold text, "1) … 2) …" lists and "• " bullets inside speech
  - "Quick odds-check before noms:", "Final recap before noms:"
  - 150-word turns ending "[cut off]" (gpt52-v-o3 swap D2, Frankie)
- Sonnet 4.5 and Opus 4.6 open with generic lines: "Indigo's death is interesting" ×8 (sonnet45-v-gpt51 D2), and "Hey X, what are you working with?"
- Only Opus 5.5 at max, and in places Fable 5.1, sound like people.

### E. Information saturation (structure)

- Almost every model uses 1.9 of its 2 whispers per private turn. The exceptions are Opus 5.5 (1.35) and Sonnet 5.5 (0.5–0.75).
- At 12 players that is about 22 whispers a beat and 66 a day, so a seat hears about 5–6 whispers a day.
- 85–100% of good seats say their role name in a whisper on D1, and 50–80% say it in public. My check is a regex, so this is an upper bound.
- So by the D1 nominations, the claim count is mostly solvable ("Twelve good claims for nine good seats", Casey, opus55max D1). R5 found the same from the probes.
- Human tables have far less contact per day. Players pick whom to talk to, and plenty of people never hear some claims.

### F. The day's fixed length produces some empty theatre (a user design decision; low cost)

- sonnet45-v-gpt51/game-01 D5: all three living players were evil (Imp, Poisoner, Baron).
- They still played 3 private beats and 3 public beats of pretend argument for the benefit of seven dead good players. Then the Baron self-nominated: "I'll bite the bullet and nominate myself… My Empath is clearly broken."
- It is harmless and faithful to the rules, but it is dead air.
- Dead players generally carry 22% of whispers, 23% of town-square speech and 27% of nomination comments. That is realistic for BotC, where dead players do lobby.
- Dead evil lobbying even became a tell: "Dead Frankie just whispered me pushing Kit… evil's dead Minion steering away from Indigo is about as loud a tell as we'll get" (gpt56sol swap D5).

### G. Other artifacts (small)

- **Opus Butler, night 1 thinking:** "I need to pick a specific example person for this — I'll go with Drew, maybe a neighbor." The model seems to read the choice as a hypothetical.
- **An o3 good seat sent the identical whisper twice in one day:** Frankie to Jules, "Morning—what character did you get on Drew last night?…", in private time 1 and again in private time 2 (gpt52-v-o3 swap D2). This fits R1's point about replies-only memory.
- **GPT reasoning summaries are titles only.** An example: "**Analyzing voting dynamics** **Evaluating nomination strategies** ×20". I could not tell from the summaries whether GPT-5.4's Spy-into-Virgin save was deliberate. The day-1 whisper suggests it was.

## 4. Which differences come from where

| Difference | Source | Fixable without distorting the measurement? |
|---|---|---|
| Hedging, legalese, memo-style bullets, no humour, few social reads | Models | No: that is the thing being measured. Report it. |
| 100% speaking rate and long turns in older models | Models, which ignore the prompt | Partly: an equal hard cap (Recommendation 4) |
| Redundant asks within a beat; unanswered questions until next beat | **Engine**: simultaneous groups; "named goes first" only works across beats | **Yes** (Recommendation 1) |
| Claim saturation by D1 nominations | **Engine**: whisper volume; also the prompt's pooling advice | **Yes** (Recommendation 2) |
| Comment and vote-remark filler | **Engine**: a turn for everyone on every nomination; models fill it | Partly (Recommendation 3) |
| Hive-mind convergence, unanimous votes | **Design**: homogeneous teams, plus volume | Mixed tables are already on the roadmap (Recommendation 6) |
| Empty final days | **Design**: fixed-length day | Leave it (user decision) |
| Storyteller chaos (Recluse as Imp, Spy into Virgin, drunk pings) | Scripted Storyteller | Keep: it is a strength |

## 5. Recommendations, ranked by expected impact × confidence

**1. Whoever is named speaks next, within the beat as well as across beats.** High impact on realism, medium-high confidence. No wall-clock cost.
- **Rule:** "In the town square, players named by a speaker take their turn in the next group, if they haven't spoken this beat."
- **Today:** `Game.beat()` sorts named players to the front of the *next* beat only (`self.addressed`, game.py ~390).
- **Change:** re-sort the remaining order after each group.
- **What it fixes:** it turns "Kit, give the names" ×6 into a question and an answer. Answers land before the next wave piles on.
- **Cost:** none. The groups are already sequential, so there are no new serial calls.
- **Checks:** it generalizes an existing rule rather than adding a special case. Needs a protocol bump.

**2. One whisper per private-time turn (still to one or two players).** High impact, medium confidence.
- **Rule:** one line; the same knob v7 turned from 3 to 2.
- **Why:** almost every model uses 1.9 of its 2. Halving it halves how far claims travel on D1. Whom to talk to and whom to trust then become real choices, and the town square has to carry more of the work, the way a human table does.
- **It also taxes evil's free coordination.** Evil sends 33–59% of its whispers only to teammates (R1), and a Spy dumps the whole Grimoire in one whisper.
- **Balance risk:** good has less information, so evil's win rate probably rises from about 30%. That direction is welcome given the good-side ceiling (R5).
- **Alternative:** 2 whispers to one player each.
- **Before scaling up:** check with a small calibration pair.
- **Checks:** does not undo a user decision (it continues v7's change). Needs a protocol bump.

**3. Trim the ritual turns of each nomination.** Medium impact, medium confidence.
- **Option (a), preferred:** "Votes carry no remark."
  - This removes the "Yes." / "Saving my ghost vote; living votes have this" roll that older models fill 50–96% of the time.
  - Coordination moves into the comment turn, which already exists. The "tie at exactly 2" instruction in opus55medium D5 was also said in comments.
- **Option (b):** keep remarks but give them the comment turn's word cap.
- **Checks:** the comment turn for everyone is a user decision. Keep it; I do not recommend cutting it.

**4. An equal, stated length cap closer to the prompt's own norm.** Medium impact, medium confidence.
- **Change:** 80 words per town-square turn and comment (now 150), 40 per vote remark (now 60), and say it in the prompt: "at most 80 words; longer is cut off."
- **Current state:** cuts are rare (0–16 per game, all in older-model games). The median older-model statement is 55–84 words, and some reach 150 with bullet lists.
- **Why:** it applies equally to every model, keeps the table readable and punishes memo-writing.
- **Risk:** v6 raised the caps because real content was being cut. With the cap stated in the prompt, models can plan for it. Check truncation rates on one pair first.

**5. Leave the prompt's strategy tips alone (medium confidence), but fix one tilt (low confidence).**
- **The tilt:** "Good wins by pooling true information, but not blindly" reads, to a model, as an instruction to claim everything.
- **Clean even-handed edit:** add the cost ("…and every claim you make also reaches the Demon"). Human veterans weigh exactly that.
- **Why the rest stays:** the day-1 claim meta is mostly model behaviour, and GPT-5.5 already soft-claims with 3-for-3s. More coaching would change what the eval measures (R2 and R5 agree).

**6. Heterogeneous tables for interest, not for ratings.** High impact on how interesting games are, high confidence, but no rating value.
- **What:** the "sociological experiments" already on the roadmap (per-seat models). A few mixed-model tables would break the single-mind good team (§3C) and make social reads matter, because different seats really do reason differently.
- **Status:** needs engine work (per-seat model assignment). Keep it separate from the rating grid, which rightly stays homogeneous (user decision).
- **Not recommended:** per-seat "personas". That is an arbitrary addition and would confound the measurement.

**7. Keep the Storyteller as it is.** High confidence.
- The misregistrations produced the best moments I read:
  - the Recluse registering as the Imp to a real Undertaker;
  - the Spy registering as a Townsfolk to the Virgin, two of three tries in e1 (the weight is 20%, so that was luck);
  - a Drunk Investigator's "Poisoner" ping that got the real Virgin executed.
- A human Storyteller would also *pace* the game, feeding misinformation to the side that is losing. Do not add that: it would make the Storyteller a factor in model comparisons.

**8. Do not add "evil wins when only evil players are alive".** High confidence.
- It is not an official rule, and it would be a special case. The empty final day in §3F is cheap and rare.
- If the cost ever matters, the clean lever is an existing user decision (the fixed day length). Ask the user before touching it.

**9. For the viewer (no protocol change): tag the turning points in each game.**
- Tags: Virgin trigger, Slayer hit or fake shot, starpass, Scarlet Woman catch, Saint execution, Mayor final three, and a ghost vote that decided an execution.
- Then the user can find the good games. The 5–6-day evil wins listed in §2 are the showcase games.

## 6. What to measure after changes 1–4 (cheap, from existing logs)

- **Redundancy:** repeated asks per beat, meaning a public question to X after X has already answered it in that beat. Expect far fewer after Recommendation 1.
- **Claim spread:** the share of good seats that have heard each claim before the D1 nominations. It is near 100% today; expect roughly half after Recommendation 2.
- **Probes:** mean good P(Demon) on the real Imp at the D1 and D2 probes. Uncertainty should last a day longer.
- **Turn use:** speaking rate and median words by model. Compare against the tables in §3A and §3B.
- **Game length and win rate:** watch the day distribution (now 17% of games end D1–D2) and the evil win rate (now 30%).
