# W1: private conversations under v14 (one whisper a turn), 4 vs 6 beats

Reader W1-conversation. I only read files: no games run, no API spend, and no repository files edited.

**Data.**
- All 50 w1 folders: 38 four-beat games (127 complete days) and 12 six-beat games (37 complete days). I counted every day whose private time had finished, including days from the 13 games still running.
- Baselines under the old rule (3 beats, up to 2 whispers): e1 (v9, 60 games) and c2 (v12, 12 games).
- The cleanest comparison is the one matchup played in all three formats: **Opus 5.5 vs Sol 6.1**, both sides. That is 10 old games, 12 four-beat games and 8 six-beat games.

**Scripts** (all in `scratchpad/readers/`):
- `w1conv.py`: metrics.
- `w1match.py`: matched matchups.
- `w1more.py`: silence, focus and pending replies.
- `w1spread.py`: how far information travels.
- `w1ex.py`: examples.
- `w1cost.py`: cost.
- `show.py GAME DAYS`: prints private time with each seat's character.

**Games read in depth (private time, and the square where needed):**

| Game | Beats | Good vs evil | What I read |
|---|---|---|---|
| opus55-v-sol61/game-02 | 4 | Opus vs Sol | day 1 |
| opus55-v-sol61-b6/game-03 | 6 | Opus vs Sol | days 1 and 4 |
| sonnet55-v-sol61/game-01 | 4 | Sonnet 5.5 vs Sol | day 1 |
| sonnet55-v-sol61-b6/game-01 | 6 | Sonnet 5.5 vs Sol | day 1 |
| gpt4o-v-sonnet45/game-01 | 4 | GPT-4o vs Sonnet 4.5 | day 1 |
| gpt4o-v-sonnet45/game-01-swap | 4 | Sonnet 4.5 vs GPT-4o | day 1 |
| o3-v-sonnet4/game-01 | 4 | o3 vs Sonnet 4 | day 1 |
| sol56-v-opus55/game-01 | 4 | Sol 5.6 vs Opus | day 2 |

I also read sampled long threads and cut-off threads from every folder, including fable51-v-astra-b6 and opus55-v-sol61-b6 game-01 and game-03-swap.

## Verdict in one paragraph
- **Private conversations read like a real table.** Questions get answered, claims are traded with haggling over who goes first, and verification chains play out over several beats.
- **The rule caused no friction.** In about 8,000 private turns there was 1 dropped second whisper and 2 whispers to three or more players.
- **Conversations did not get longer per pair at 4 beats.** Each player now holds fewer threads at once, and they are more focused, but a thread is about as long as under the old 3×2 rule, or slightly shorter.
- **6 beats buys roughly one more exchange per conversation.** It also buys wider reach (more hive mind, not less) and idle turns late in the game.
- **The hive mind barely moved.** Players compensate by whispering to two at once and by relaying third-party claims. Most day-1 knowledge becomes public in the town square anyway.
- **Recommendation: keep 4.** Use 5 if the user wants more depth. Details and reasons are in section 5.

## 1. Do private conversations read like real conversations?

Yes. Beat by beat, the strong models' private time is the most human part of the transcript. Examples follow.

**A question answered, and trust built over four messages.** opus55-v-sol61/game-01, day 1. Ellis is the real Washerwoman; Gray is the real Slayer.
- b1, Ellis → Gray: "I have first-night info that involves you... Before I say more, what's your character?"
- b2, Gray: "Tell me which character your info shows for me, and I'll tell you straight if it matches. That way neither of us can be fished."
- b3, Ellis: "Fair. I'm the Washerwoman: I saw that either you or Casey is the Slayer. Casey just told me privately they're the Investigator..."
- b3, Gray: "Yes, I'm the Slayer - matches. So you're confirmed to me too... Drew told me he's Chef with 1 evil pair, Harper says Mayor. Let's pool and pick a shot carefully."
- b4, Ellis: "Casey says Poisoner is Alex or Jules - note Alex and Jules sit next to each other, which fits Drew's 1 evil pair..."

**Evil working a conversation.** opus55-v-sol61/game-02, day 1. Ellis is the Spy, and Kit is the Soldier.
- b2, Ellis → Kit: "I'm the Washerwoman: I saw Soldier between you and Blair. Does that fit you?"
- b3, Kit: "Yes, that checks out - I'm the Soldier. Keep the exact role quiet publicly."
- b4: Ellis uses it with Alex: "Kit has confirmed my information privately."

The same day, the Imp Frankie gets pulled into a "trusted bloc" with the drunk Empath, Gray, and with Harper. He reports to his team: "Gray privately claimed Empath 0 to Harper and me, so he's shielding me already. Keep him alive."

**Who you told becomes evidence.** sol56-v-opus55/game-01, day 2. Kit is the Poisoner.
- b1, Logan (Empath) → Kit: "Did you tell anyone my role? Please keep it quiet."
- b2, Kit: "Haven't told anyone, promise..."
- b3, Logan → Indigo: "Kit alone knew my role and now claims he told nobody, yet says evil must have targeted me N2."
- b4, Indigo: "Was Kit definitely the only person who knew?"
- b4, Logan: "Yes."

A one-to-one claim becomes a traceable leak.

**Being swarmed has a cost.** Same game, day 2. Five players whisper the Slayer, Alex, "what's your exact role?". He can answer one a beat, and Jules pushes: "I need a direct answer before nominations; staying silent makes Harper's YES much harder to dismiss." That is realistic pressure the old two-whisper rule mostly hid.

**Soft-claim negotiation, even from o3** (o3-v-sonnet4/game-01, good side).
- "Want to do a quick 2-for-2 role exchange?" → "Sure. I'm either the Empath or the Librarian. You?"
- In the last beat: "still up for that 2-for-2?"

**The weak spot is older models.**
- GPT-4o spends turns on empty openers:
  - "Hey, can we chat for a moment? I have something important to share." → "Sure, what's up?" → the Saint claim arrives two beats later.
  - This happens with the Imp too: "Hey, Casey. Can we have a quick chat?" → "Sure, what's up?" → "I'm the Saint."
- Such openers are 3% of GPT-4o whispers and 5% of Sonnet 4.5's, and 0% for every current model.
- Sonnet 4.5, Sonnet 4 and o3 often think "X hasn't responded yet, I should wait", and stay silent.

**Thread length per pair per day.** A thread is all whispers between two players on one day; a 2-player whisper counts in both pairs. A "switch" is a change of speaker.

| | Old 3×2 (Opus/Sol) | 4 beats (Opus/Sol) | 6 beats (Opus/Sol) | 4 beats (all) | 6 beats (all) |
|---|---|---|---|---|---|
| Whispers per day | 54 | 40 | 55 | 37 | 54 |
| Pair-threads per day | 32.4 | 28.5 | 32.6 | 25.9 | 31.8 |
| Messages per thread (day 1) | 2.21 (2.80) | 2.01 (2.52) | 2.36 (2.78) | 2.00 (2.50) | 2.35 (2.71) |
| Speaker switches per thread | 1.09 | 0.89 | 1.19 | 0.88 | 1.20 |
| One message, never answered | 34% | 39% | 27% | 39% | 27% |
| ≥3 messages and ≥2 switches (a real exchange) | 33% | 24% | 36% | 23% | 36% |
| ≥4 messages and ≥3 switches | 12% | 6% | 11% | 6% | 11% |
| Share of a player's day spent with their top partner | 43% | 49% | 45% | 53% | 46% |
| Next whisper goes to the same partner | 6% | 14% | 14% | 16% | 14% |

What the table shows:
- Players are more focused: 49–53% of a player's day goes to one partner, against 41–43% before.
- Each thread is not longer. The old rule let a player keep two threads going each turn. At 4 beats the budget is 4 whispers a day, against 6 before.
- Six-beat games cut off after beat 4 look exactly like the 4-beat games: 23% real exchanges, 1.95 messages per thread.
- After beat 5 they reach 29%, and after beat 6, 36%. Each extra beat adds both depth and breadth; there is no natural stopping point at beat 4 on day 1.

## 2. Is 4 beats enough? What does 6 add, and what is wasted?

**4 beats does not visibly cut conversations off more than the old format did.**
- Threads whose last message is an open question in the final private beat: 12.9% at 4 beats, 10.2% at 6, and 15.8% under the old rule (Opus/Sol).
- Threads left hanging on a question earlier in the day doubled, 14% → 25%. That is the price of choosing whom to answer, and it is realistic.
- The town square follows immediately, and a question left open in private is often asked there.

**Where 4 beats does bite:**
1. **The "you go first" standoff** (Washerwoman or Librarian vs the named player) uses a whole beat. It is in 5.3% of day-1 whispers at 4 beats, against 3.7% in e1.
   - Example from six-beat game-03, day 1, Ellis (Investigator) and Casey:
     - b2, Ellis: "You go first though."
     - b3: Casey gives Recluse and asks for the pair.
     - b5, Casey: "Still keen to hear your pair, Ellis. I've given you my role, so your turn."
     - b5: Ellis finally answers.
   - At 4 beats Casey would have gone to the square without the answer.
   - In the four-beat games there are 41 cut-offs mid-conversation: at least 3 messages, and a one-to-one question in the last beat. For example, a Spy asks the Librarian: "What's your information?" There is no reply.
2. **Older models waste beats on openers**, and weak evil teams coordinate slowly (section 4).
3. **Multi-step checks.** Some take three beats: Librarian asks, both named players deny, back to the Librarian. On day 1 these often end in "Something's off" rather than being resolved.

**What 6 adds (Opus/Sol, 6 vs 4 beats):**
- About one more exchange per conversation: real exchanges 24% → 36%.
- Some verification chains finish, like Casey and Ellis above.
- Wider reach:
  - Day-1 partners per player: 4.2 → 5.4.
  - Pairs that talk on day 1: 44% → 57%.
- Beats 5–6 on day 1 are largely broadening: "Hi both - gathering claims before the square."

**What 6 wastes:**
- Silence by beat (Opus/Sol, share of turns that sent no whisper):
  - 4 beats: 0%, 4%, 14%, 21%.
  - 6 beats: 0%, 8%, 18%, 20%, 25%, 30%.
- Late days are worse. With 6 or fewer players alive, 40% of six-beat private turns are silent, against 27% at 4 beats and 20% under the old rule. The dead are 45% silent.
- Example: b6 game-03, day 4, 6 alive. Beat 1 has 12 whispers and beat 2 has 9. Beats 3–6 have 6, 3, 2 and 1, mostly "Agree: Harper today, Frankie tomorrow."
- Near-duplicate whispers are rare in both formats (0.6%), so the waste is silent turns, not repetition.

**Cost and time (Opus/Sol):**

| | 4 beats | 6 beats |
|---|---|---|
| Private time's share of spend | 37% | 40% |
| Private cost per day | $0.49 | $0.54 |
| Private time per day (median) | 2.8 min | 3.8 min |
| Whole day (median) | 6.7 min | 7.2 min |

Silent turns are cheap, so 6 beats costs about 10% more private spend and about 1 minute a day.

## 3. The hive mind

It is not reduced, and it is not slowed. Players route around the cap.

| Day 1, by the end of private time | Old 3×2 (Opus/Sol) | 4 beats (Opus/Sol) | 6 beats (Opus/Sol) |
|---|---|---|---|
| Player pairs that exchanged a whisper | 48% | 44% | 57% |
| Distinct partners per good player (quartiles) | 4.6 (4/4/5) | 4.2 (3/4/5) | 5.4 (4/5/6) |
| Good player has heard of other good players' true self-claims (regex estimate) | 42% | 44% | 48% |
| Whispers that relay a third party's claim | 28% | 36% | 37% |
| Good whispers to two players (all games) | 20% | 33% | 33% |
| Good players who self-claim in the town square on day 1 | 59% | 69% | 53% |
| Spread of P(evil) across good seats, day-1 probe | 0.062 (all e1) | 0.062 (all 4-beat) | 0.056 (all 6-beat) |

- **Compensation:** fewer whispers, but each carries more. Group whispers rose from 20% to 33%, and gossip relays rose, e.g. "FYI Indigo claims Virgin to me, Jules claims Butler (master Kit)." Information reaches about as many people by the square as before.
- **The square finishes the job.** About 60% of good players self-claim publicly on day 1, and the good seats' day-1 P(evil) estimates are as uniform as before. Private-time structure is not the main source of the hive mind. The day-1 public claim dump and one shared model are.
- **Choosing whom to talk to is now a real decision in the reasoning.**
  - "I only get one whisper this turn, so I'll prioritize whispering Drew to get their claim first and circle back to give Blair an answer next beat, even if it risks looking evasive." (Fable 5.1)
  - "Since only one whisper is allowed, I'll reply to both Blair and Ellis together." (Opus)
  - About 22% of whispers are sent while ignoring someone waiting for a reply, the same as before.
- **Evil can't see who talks to whom.** The prompt says nobody sees "even that you whispered." Whom-talks-to-whom becomes evidence only secondhand:
  - Leak tracing, as in the Logan/Kit case above.
  - Timing arguments. Gray, day 4: "Frankie's FIRST whisper to me day one didn't name a role... A real WW just says the role."
  - Complaints about silence ("X never answered me"). These roughly tripled per whisper (0.08% → 0.22%) but are still rare.

## 4. Anything awkward or broken

- **The rule is understood.** 1 second whisper was dropped, by an o3/Sonnet 4 seat. There were 2 whispers to three players and 0 private turns with a `say`. Older models occasionally think in terms of a budget per private time ("only two whispers left in this round"), but it does no harm.
- **Group whispers are used, not abused.** 33% of good whispers go to two players. Only 15% of two-player whispers merge two separate earlier threads (26% under the old rule). Most are neighbour trios or evil's team channel (85–90% of evil team whispers go to both teammates).
- **Evil coordinates fine when it uses the team whisper.**
  - The Imp and a Minion talk in beat 1 in 99 of 100 Minion-days (all-w1 day 1).
  - Evil spends about half its day-1 budget on itself: 46% of its whispers at 4 beats, 33% at 6.
  - Weaker evil teams are slow. In o3-v-sonnet4/game-01, the Sonnet 4 Imp sent the bluffs only to Blair (one recipient), in b2. Drew, the Poisoner, meanwhile claimed Virgin to Casey in b2. The real Virgin is Frankie, so evil created a contradiction that was not there before.
- **Silence is a model trait, not a rule problem.**

  | Model | Silent private turns |
  |---|---|
  | Sonnet 5.5 | 58% (55% in e1) |
  | Sonnet 4.5 | 36% (18% in e1; "wait for a reply before sending another") |
  | Opus 5.5 | 16% |
  | Others | 1–11% |

- **The swarmed player now looks evasive** (Alex in sol56-v-opus55). It is realistic, but it slightly penalises whoever holds the key information.

## 5. Recommendation

**Keep 4 beats for the flagship.**
- The conversations it produces are coherent and humanlike.
- Cut-offs in the last beat are no worse than under the old rule, and the square picks them up.
- 6 beats gives about one more exchange per conversation, but it also adds the breadth the user wants less of: 5.4 partners against 4.2, and 57% of pairs against 44%.
- 6 beats also spends 25–30% of turns in beats 5–6 (40% on late days) doing nothing.
- If the user's main worry is depth, **5 beats** is the compromise. Six-beat games cut after beat 5 have 29% real exchanges (4 beats: 23%, 6: 36%) and 42% on day 1. That costs about +5% private spend and about 30 s a day.

Small fixes. None is needed for correctness.
1. **Prompt (optional): tell players a whisper gets its reply on a later turn.** Something like "a reply usually comes on your next turn, so you don't need to wait." This would cut Sonnet 4.5's and o3's silent "wait for a reply" turns. It would also add whispers, and so a little more spread, so it only matters if the silence of older models counts as a handicap.
2. **If the goal is less hive mind, the lever is not the beat count.**
   - Whisper structure moves spread by a few points.
   - The day-1 public claim dump (about 60%) and one-model teams dominate.
   - The realistic change that would make whom-you-talk-to meaningful is to make it visible: e.g. announce "Alex and Blair talked privately" at the end of each beat, as at a physical table where you see who steps aside. Evil could then read networks, and good would pay a price for pooling.
   - That is a rule change (v15), not a wording fix, so I mention it for the user to decide.
