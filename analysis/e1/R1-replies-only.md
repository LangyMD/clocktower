# R1: the replies-only models (Sonnet 4.5, o3, GPT-5.1, GPT-5.2, GPT-5.4) in v9 e1

Reader: R1. Files read only. No runs, no API spend.

## Games covered

Only six games had a `result.json` when I checked. Every other directory on the list was still running (o3-v-gpt54 x2, gpt52-v-o3 x2, sonnet45-v-gpt54 x2, gpt51-v-opus46 x2, gpt54-v-fable51 x2, gpt54-v-opus48 x2, sonnet45-v-gpt51/game-01). So no finished game has GPT-5.4 in it. I looked at calls.jsonl for the running games only to check for engine problems.

| Game (games/v9/…) | Good | Evil | Players | Result |
|---|---|---|---|---|
| e1-sonnet45-v-gpt51/game-01-swap | GPT-5.1 (replies) | Sonnet 4.5 (replies) | 10 | good, day 2 (Imp executed) |
| e1-sonnet45-v-opus55/game-01 | Sonnet 4.5 (replies) | Opus 5.5 | 11 | **evil, day 6** |
| e1-sonnet45-v-opus55/game-01-swap | Opus 5.5 | Sonnet 4.5 (replies) | 11 | good, day 5 (at 4 alive, on ghost votes) |
| e1-gpt51-v-gpt61sol/game-01-swap | GPT-6.1 Sol | GPT-5.1 (replies) | 12 | good, day 2 (Slayer shot) |
| e1-o3-v-astra/game-01-swap | GPT-6 Astra | o3 (replies) | 11 | good, day 3 |
| e1-opus45-v-gpt52/game-01-swap | GPT-5.2 (replies) | Opus 4.5 | 10 | good, day 3 (Slayer shot) |

Six games is a small sample. Everything below is qualitative.

## 1. Do they keep a coherent state across the game?

**Mostly yes.** The main reason is how the engine works. The model sees everything it has said and whispered, plus every Storyteller message. So its own claims and its night information are always in front of it. The only thing it loses is private reasoning it never put into a reply.

I checked the belief probes, which ask each seat for its current claim before each day's nominations:
- Every replies-only seat kept a stable claim across days, and each probe claim matched what the seat had actually said.
- In the Opus-good swap, Sonnet 4.5's evil team held its bluffs for five days: Alex as Chef, Drew as Soldier, Ellis as Investigator.
- In the Opus-evil game, Sonnet 4.5's Jules kept track of its own protective lie for six days. It said "Ravenkeeper (lied to protect Slayer)" on day 1, and by day 5 "I told everyone Ravenkeeper early, then claimed Slayer".

Sonnet 4.5's thinking (full text, median ~400 tokens) usually starts with a recap rebuilt from its replies, and those recaps are accurate. For example, `e1-sonnet45-v-gpt51/game-01-swap`, Drew, day 1: "I told Ellis I'm Soldier… If I claim Monk it contradicts what I told Ellis and Casey." Drew then switched publicly to Monk anyway. That was a deliberate bad choice, not a memory lapse, but it lost the game: Ellis exposed the switch from Soldier to Monk.

Evil teams also keep their night actions straight by whispering them to each other, which in effect gives them a shared notebook. Some checks against the logs:
- `…sonnet45-v-opus55/game-01-swap`: Sonnet's Drew says "I poisoned Harper last night" on nights 2, 3 and 4, and the log confirms all three.
- `…gpt51-v-gpt61sol/game-01-swap`: GPT-5.1's Frankie (Spy, bluffing Fortune Teller) repeated the same invented results in five separate whispers: N1 Kit+Indigo No, N2 Alex+Harper No.

Replies-only evil sent about as large a share of its whispers only to teammates as the reasoning models did (Sonnet 4.5 53%, o3 39%, GPT-5.1 37%, against 33–59% for the others). So I see no sign that they spend extra whispers on keeping their memory.

**The failures I found are of three kinds.**

1. **A good player believes its own invention.** This is the clearest memory-mechanism case.
   - Game: `e1-sonnet45-v-gpt51/game-01-swap`, day 2, Harper (GPT-5.1, Undertaker).
   - Harper was killed on night 2, so the Undertaker never woke. Its conversation shows "— Night 2 —" with nothing after it.
   - Indigo (the Drunk, who thinks he is the Monk) asked a leading question. Harper whispered to four players: "I'm Undertaker, and I saw you as Monk last night."
   - On its next turn, Harper's reasoning summary reads: "I'm piecing together how the Undertaker could have obtained info despite dying that night, navigating contradictions between the story text and game rules."
   - It then told the town: "Either I was poisoned N2 or Indigo was really Monk." Its probe put Indigo at 0% evil, 0% Demon.
   - With no private notes, the model could not tell whether its earlier claim was a bluff or real information, and it trusted its own reply over the rules. The invented result then decided the game: the town executed the Imp on it.
   - Nobody on either side noticed that an Undertaker killed that night cannot learn anything.
2. **Getting the timing of its own whispers wrong.**
   - Game: `e1-gpt51-v-gpt61sol/game-01-swap`, day 2, Ellis (GPT-5.1, Poisoner bluffing Librarian).
   - Ellis said in public: "I shared that with Drew, Indigo, Logan, Alex and Blair yesterday."
   - In fact only Drew heard it on day 1. The others heard it that morning, which Ellis's own reply history shows.
   - Sol's Alex, Logan and Indigo each corrected him in public ("Small timing correction, Ellis: I first heard your exact result this morning"). Casey then pressed: "Who actually heard the full pair yesterday?"
   - Ellis had to issue a correction. This is a lapse in keeping track of when things happened across his own replies.
3. **Forgetting which information was private.**
   - Game: `e1-o3-v-astra/game-01-swap`, day 1, Jules (o3, Baron).
   - Jules used Gray's Empath "1" in town. Only Kit had told him, in a whisper.
   - Astra's Gray replied at once: "Jules, who told you my Empath result? I shared it only with Harper and Kit."
   - Jules answered "Kit filled me in privately… I thought it was already common knowledge." That publicly tied Kit (the Imp) to Jules. Jules was executed that day, and Kit the next.

**Mis-reading who claimed what** happened, but it was a group reasoning failure more than memory.
- Game: `…sonnet45-v-opus55/game-01`, day 4, Sonnet 4.5 as good.
- Casey said: "If Frankie is Butler to me as neighbors, shouldn't they have voted the same way?" Frankie had never named Casey as his master; his masters were Jules, then Kit, then Alex.
- Kit, Blair, Gray and Harper all repeated this. They also said Frankie "changed his story" about his master, though a Butler picks a new master every night.
- The contexts here are small (Sonnet 4.5 at most ~38K tokens by day 6), so this is not a long-context problem.

## 2. A handicap from the memory mechanism, or a lack of skill?

**Mainly skill. The memory mechanism accounts for a small, specific part.** The reply history holds enough for claims, bluffs and night information. What it can't hold is the difference between "I said this" and "this is true" when the model never wrote that difference down. Good players who bluff are exposed to this most, since they have no teammate to record the plan with. GPT-5.1's good team made up information twice in one game:
- Harper, the invented Undertaker result above.
- Blair, a Ravenkeeper, bluffed Librarian with a made-up ping. Its probes show it knew this was a bluff.

Evil keeps its plans in team whispers and does not look handicapped. Sonnet 4.5's evil team played well against Opus 5.5 as good:
- The Poisoner hit the Fortune Teller every night, which discredited her.
- They got three wrong executions: Indigo, Blair (the Mayor) and Gray.
- It took the town's ghost votes on day 5 to beat them.

The losses I saw came from skill problems:
- **Sonnet 4.5 as good follows the herd.** Most day-1 to day-4 votes were unanimous, and players repeated the same wording. On day 4, six players repeated almost word for word the claim that no one died on the nights the Monk protected Kit. That argument is illogical (an Imp simply kills someone else). On it they executed their true Undertaker.
- **Coordination slips.** o3's evil team fake-claimed Recluse without knowing a real Recluse was in play.
- **Weak cover.** GPT-5.1's Jules offered Librarian/Soldier/Ravenkeeper, then settled on Soldier, and was shot by the Slayer.

**The cost of rebuilding the game every turn is clear, and it grows each day.** Median / p95 thinking tokens per turn, all v9 calls excluding probes:

| Model | Day 1 | Day 2 | Day 3 | Day 4 |
|---|---|---|---|---|
| o3 | 832 / 2.9K | 1.5K / 5.6K | 2.0K / 7.0K | 1.3K / 7.9K |
| GPT-5.1 | 2.0K / 7.0K | 5.0K / 11.0K | 4.9K / 11.5K | 3.7K / 13.4K |
| GPT-5.4 | 854 / 3.0K | 1.6K / 5.0K | 2.0K / 6.0K | 4.5K / 7.6K |

Carried-reasoning models stay flat: Opus 5.5 at high thinks 20–70 median, Sol 90–200. Sonnet 4.5 stays flat at ~350 but thinks very little each turn. Its setting is budget thinking with no effort parameter, so it is not really at "max effort".

## 3. How do the new models play against them?

The new models take advantage of the old models' slips at once, and the play looks realistic.
- **Astra vs o3:** caught the leaked Empath result (above) and solved the game in 3 days: Baron on day 1, Imp on day 2, the Scarlet Woman who became Imp on day 3.
- **Sol vs GPT-5.1:** caught Ellis's timing error. The Slayer then shot the Imp on day 2.
- **Opus 5.5 as evil vs Sonnet 4.5 as good:** Opus won in 6 days. It set this up with plans a real table would recognise:
  - The Spy claimed Ravenkeeper to match the Washerwoman's ping.
  - The Poisoner made up an Investigator result naming the Fortune Teller.
  - The Imp immediately made public the Fortune Teller's private "I'm the Empath" lie to him.
  - The Imp starpassed to the Spy, who had a confirmed-looking Ravenkeeper claim.
  - After his execution, the Poisoner lied that he "poisoned Gray night one" to cover the Spy's misregistration.
  - Sonnet's Harper found the Demon on night 1 (a YES on Alex and Ellis) and was executed 10–0 on day 1.
  - Most of the later wrong executions Sonnet did to itself; Opus mostly just went along.

GPT-5.2 as good beat Opus 4.5 as evil in 3 days, with a clean Undertaker chain and a Slayer shot. So the replies-only models are not uniformly weak.

## 4. Engine and prompt problems

- **Truncation and refusals.** None in the six finished games. Every call stopped normally, there were no retries, and no output was malformed. Across all v9 calls from these models there were two truncations at 16K, both GPT-5.1 in unfinished games:
  - `e1-sonnet45-v-gpt51/game-01`, Drew's night-4 choice: the retry succeeded at 6.1K tokens.
  - `e1-gpt51-v-opus46/game-01`, Alex, day 2, beat 2: the retry was not in the log yet.
  - GPT-5.1's p95 reaches 13.4K by day 4, and its biggest finished-game turn was 14.3K. Long games will lose some turns. The rate is about 0.2%, under the supervisor's 1% alarm.
- **A cosmetic bug in the whisper notice.** `game.py` line 356 runs `.capitalize()` on the whole notice, which lower-cases every name after the first letter. Sonnet's Kit got "(Your whisper to blair, frankie, gray went only to blair and frankie …)" in `…sonnet45-v-opus55/game-01`, day 2. Fix: capitalize only the first character.
- **Whispers to three players.** Sonnet 4.5 addressed one whisper to three players. The engine sent it to the first two and told the sender, which is correct behaviour. Adding `maxItems: 2` to the schema would stop it, if both APIs accept that.
- **Reasoning summaries are hard to audit.** GPT-5.1's summaries (`summary: 'concise'`) are mostly bold headings, for example "**Selecting master for Night 1**". Reviewers can barely see what it was thinking. o3 uses 'auto' and is better. The summaries are never fed back to the model, so changing them would not affect play.
- **Prompt.** The 'replies' line says what the model can't see, but unlike the 'reasoning' line it gives no advice. The Harper case suggests a one-line fix, but it would make the two prompts differ more.

## Recommendations

1. **Measure the memory handicap directly** (high value; medium-high confidence this is the right design).
   - Run 3–5 side-swapped pairs of one carried-reasoning model (Opus 5.5 or Sol) with its reasoning removed ("replies" mode, with the replies prompt line), against the same model running normally.
   - The difference separates the memory effect from the skill effect in the old models' ratings.
   - This needs one engine flag to override `spec(model)['memory']` and drop reasoning blocks from the conversation.
   - Until then, mark the five replies-only models on the headline chart as confounded.
2. **Fix the lower-casing in the whisper notice** (`game.py:356`, use `s[:1].upper() + s[1:]`) (high confidence; cosmetic).
3. **Use `summary: 'detailed'` (or 'auto') for gpt-5.1, 5.2 and 5.4** so games can be audited. It does not affect play, and it costs only summary tokens (medium confidence it's worth it).
4. **Watch GPT-5.1 for truncated turns in long games.** Don't raise the ceiling (the ceiling stays equal for all models by design), but report its lost turns next to its rating (medium confidence).
5. **Optional prompt line for replies-only seats:** "Your earlier messages may include bluffs; your character and the Storyteller's messages are your ground truth." It targets the Harper failure (low-medium confidence; the protocol changes, so it would need a `PROTOCOL` bump).
6. **Don't add a notebook** (that design is the user's choice). The reply history plus evil's team whispers is enough for coherent play. The remaining gap is private bluff-versus-truth tracking for good players, and recommendation 1 would measure it.
7. **Read the Sonnet 4.5 and GPT-5.1 results as skill, mostly.** Herding, weak logic and leaked private information explain more of their losses than memory does (medium confidence; n = 6).
