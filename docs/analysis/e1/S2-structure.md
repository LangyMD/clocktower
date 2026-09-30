# S2: does the day structure work? (v9 e1)

Reader: S2. I only read files: no `run`, no API spend, no repository edits. Data: all 60 `games/v9/e1-*/game-*`
directories (53 finished when I last refreshed; the in-progress games are included in the per-turn statistics),
26,867 game calls, 12,455 delivered whispers, 8,604 public lines, 363 nominations. Scripts are in
`scratchpad/s2/` (`load.py` builds per-turn tables, `segs.py` maps events to beats, `a1.py`–`a10.py` do the
analyses, and `show.py GAME DAY [parts]` prints a day with waves and characters).

**Waves are reconstructed, not logged.** Calls in `calls.jsonl` are written as they finish, and a wave finishes
before the next one starts. So within a (kind, day, beat) block, the first ceil(n/3) distinct seats are wave 1, and
so on. I checked this against event order: in 1,000 of 1,000 public and comment segments the `say` events come out
in non-decreasing reconstructed wave order.

## Bottom line

The day structure works. Beats are rarely empty: 8% of private turns and 17% of town-square turns pass. Most speech
is new: about 90% of each public line's word-trigrams have not been said earlier that day. Private time produces
realistic claim trading, softclaims, cross-checks and evil scheming. Waves almost never cause collisions a human
table would not have.

The weak spots are small:
- The comment round is the most repetitive part (6.6% near-echoes; 36% of comments just announce a vote).
- The "named players go first" rule is nearly inert: 80% of the table is named in every beat.
- Late days (six or fewer alive) are usually decided in the first private beat. Five more beats of mostly
  reaffirmation follow, and 61% of those turns belong to dead players.
- Randomly picking one of several simultaneous nominations rarely decides who dies.

None of this needs a design change. I have three one-line wording or ordering fixes and two optional rule tweaks
(flagged below).

## 1. Beats: used or wasted?

| part | turns | silent | words/turn (mean) | thinking tok/turn | cost | share of spend |
|---|---|---|---|---|---|---|
| private time | 7,439 | 8.3% | 62 (whispers) | 1,331 | $342 | 34% |
| town square | 7,238 | 16.6% | 43 | 1,051 | $293 | 30% |
| comments | 3,807 | 31.7% | 26 | 438 | $89 | 9% |
| nominate calls | 3,997 | 62.9% | 15 | 472 | $78 | 8% |
| votes | 3,589 | 68.6% (no remark) | 3 | 240 | $70 | 7% |
| defense | 346 | 0% | 67 | 477 | $8 | 1% |
| night | 446 | — | — | 1,215 | $13 | 1% |
| probes (telemetry) | 3,053 | — | — | — | $100 | 10% |

**By beat.**
- Silence rises within each part: private 2.3% → 8.7% → 13.8%; town square 6.8% → 15.9% → 27.1%.
- The share of novel trigrams falls: town square 0.95 → 0.91 → 0.87.
- The share of lines echoing an earlier line in the same beat (content-word Jaccard > 0.4) is 2.1%, 1.8% and
  3.0%.
- Beat 3 is thinner but not empty. Town square 3 still had 1,748 lines, often the last defences, answers to beat-2
  questions and final plans ("Last try. I'm the Recluse…").

**Where claims come out.** 558 of 660 seats make a first-person public claim at some point:
- 276 in town square 1 of day 1, 78 in square 2, 37 in square 3, and 15 in day-1 comments.
- 66 in town square 1 of day 2.

So square 1 is the claim dump and squares 2–3 are for argument. That is healthy.

**Private time feeds the public game.** 12% of town-square lines cite a whisper ("Ellis whispered me his Librarian
claim before I'd told him anything"), and private claim timing is used as evidence. Private time is not redundant
with the public claim dump.

**By day.**
- Private-time silence rises from 4% (day 1) to 15% (day 5); town square from 12% to 14–20%.
- Novelty falls from 0.94 (day 1) to 0.82 (day 5) in the town square, and from 0.89 to 0.70 in comments.
- Thinking per turn doubles from day 1 to day 3–4 (private 637 → 1,920 tokens).
- Cost per turn doubles once 8 or fewer are alive ($0.025 → $0.05), because the context grows (input 11K → 40K
  tokens a turn).
- Mean cost per game-day: $2.2, $3.4, $5.5, $5.0, $4.4 for days 1–5.

**Do late days drag? Somewhat, but cheaply, and the dead keep them useful.** A rough convergence test: the first
beat in which at least half of the talkers name the day's first nominee next to "vote / execute / nominate".
- With **six or fewer alive**, it is private beat 1 on 28 of 59 days (47%), and within private time on 39 of 59.
- With **more than six alive**, it is usually town square 2–3 (73 of 118), and 47 days never pass the threshold.

Example: `e1-sonnet55-v-gpt61sol/game-01` day 6, four alive. Everyone lines up on Harper in private beat 1. The next
five beats reaffirm it ("Locked in: Harper"). Harper (the real Recluse) makes three defences, and the vote goes 8–1
with 5 unnecessary ghost votes.

It still works as a game. The evil team (dead Imp, dead Baron, living Scarlet Woman-turned-Imp) spends those beats
whispering to lock in the wrong execution ("With my vote and both your ghosts, that's six… an Alex counter can get
at most five"). With six or fewer alive, beat and comment turns cost about $157 (16% of spend), and 61% of those
turns are dead players'.

**Is 3+3 right?** Yes, for 10–12 players. Each extra beat costs about $1.5 a game and still carries mostly new
content. Cutting the third beat of each part would save about 19% but remove the reply beat. One wave of seats
answers questions from the previous beat, so a two-beat part leaves questions from late waves unanswered until the
next part. Fixed length every day is a user decision, and I see no evidence that argues against it.

## 2. Whispers

- **Use.** Per private turn: 0 whispers 8%, 1 whisper 14%, 2 whispers 78%. Nobody ever tried to send 3 (0 attempts
  over the cap; the only interface notices were 12 whispers to 3+ recipients cut to two). 76% of whispers go to one
  recipient and 24% to two. Median whisper 34 words; none reached the 150-word cap.
- **The cap binds as intended.** 78% of turns use both slots, which is what the v7 cut from 3 to 2 wanted. Reach is
  limited: 42% of player pairs exchange a whisper on day 1 (39% of directed pairs). In 12.6% of player-beats a player
  receives more than 4 whispers (more than one turn can answer). Swarming the key information holder is realistic;
  e.g. five players asking Ellis "what did Blair read?" in `e1-opus55-v-sonnet55/game-01` d2.
- **Who whispers to whom.**
  - good → good 50%, good → evil 19%, evil → good 17%, evil → evil only 10%, mixed 4%.
  - Whispers including a seat neighbour: 36% (chance is about 20%).
  - 51% of whispers answer someone who whispered the sender earlier that day; 24% of links are never returned that
    day.
- **Evil scheming is real and costs evil slots.**
  - 61% of evil whispers in day-1 private beat 1 go only to teammates, then 33–38%. Days 2–3 follow the same shape
    (about 50% in beat 1, 25–30% after).
  - Evil use the channel for bluff allocation ("I'll grab one so we don't collide"), Spy Grimoire dumps, kill and
    poison plans, Saint-execution plans and ghost-vote counting.
  - Coordination lags by a wave. In `e1-opus55-v-gpt61sol-b/game-01-swap` d1 the Imp's "SWAP" whisper (private 3,
    wave 2) came after both Minions had privately claimed Undertaker and Recluse (private 3, wave 1). That is ordinary
    latency; human tables have it too.
- **Dead players** send 23% of whispers (2,805) and are 16.6% silent in private time (alive: 5.4%).
- **Misreads.** 20 thinking summaries misread the cap as "two whispers per private time" (o3 10, Sonnet 4.5 8), for
  example "we already used two whispers in the earlier beats". These are mostly replies-only models re-deriving
  their state. The fix is one word in the private-time prompt.
- **Model differences are large.** Private-time silence: Sonnet 5.5 55% (only 10% of its turns use two whispers),
  Opus 5.5 15%, Sonnet 4.5 17%, everyone else 0–8%.

## 3. Waves

- **Sizes.** Three waves of ceil(n/3): 4/4/4 at 12 players, 4/4/3 at 11, 4/4/2 at 10. README.md says "in groups of
  three"; it is three groups of up to four. At 10 players the last wave is only two seats, who then get the last word
  with the most information.
- **Collisions.**
  - Public same-character counterclaims: 13 in all.
  - Only 1 had both claims in the same beat and wave: `e1-o3-v-astra/game-01-swap` d1, square 1, where the Baron and
    the real Recluse both claimed Recluse.
  - Two evil players never publicly claimed the same character (0 cases).
  - Private evil claims of the same character: 0 in the same wave, 4 at different times, all deliberate (e.g. a
    Drunk claim picked up later).
  - I found no contradictory evil plans that simultaneity caused.
- **Redundancy from simultaneity is small.** Comment pairs that open with the same two words: 9.9% in the same wave
  against 7.2% across waves. Near-echo pairs: 1.44% in the same wave against 1.12% across. Most repetition is herding
  across waves, not blind simultaneity.
- **Fairness across seats.**
  - The order is shuffled every beat, and positions are even by team in private time and town square 1.
  - In town squares 2–3, the named-first sort puts living evil players in wave 1 41% of the time (good 36%) and in
    wave 3 21% (good 28%). Evil gets the last word slightly less often, because they are named (suspected) more.
  - The rule barely sorts anyone: after each town-square beat, 78–80% of the table has been named. In practice it
    means "unnamed players go last".

## 4. Nominations

**Rounds.** 562 nomination calls; 199 were the closing call with no nomination ($16.5).
- Rounds with at least one nomination averaged 3.9 simultaneous nominators (up to 12).
- 1,039 nominations were dropped (the dropped nominators' turns cost $26, 3% of spend), and each produced a
  separate notice line.
- Nominations per day: 1 on 88 days, 2 on 98, 3 or more on 23.

**Does the random pick decide outcomes? Rarely.**
- In 207 of 363 rounds every nominator named the same target, so the pick only chose whose accusation was read.
- In 156 rounds the targets differed. The pick is uniform over nominators, so it is weighted toward the popular
  target.
- An unpicked alternative was nominated later that day in 127 cases and never in 51.
- A minority target (fewer nominators than another) went first in 31 rounds (9% of rounds with a nomination). In
  those rounds the majority target was nominated later in 30 of 31, and was executed anyway in 19. The minority pick
  was executed in 5. Two of those 5 hit the evil team (Poisoner, Imp); one executed a Librarian while the Imp with
  two nominators was voted down later (`e1-gpt51-v-opus46/game-01-swap` d4).
- Order matters because a later nominee must beat the block: the first nomination of a day is executed 69% of the
  time (144 of 209), the second 32%, the third 22%.

**Comment round.** 3,807 turns, 32% silent, 26 words each, $89 (9%).
- It is the most repetitive part: 6.6% near-echoes, and novelty 0.83 against 0.91 in the town square.
- 36% of comments announce a vote ("No trigger. Don't vote Kit.", six times in a row in
  `e1-opus55-v-gpt61sol-a/game-01` d1). The declared stance matches the actual vote in 94% of cases (yes→no 44,
  no→yes 11).
- It still adds value: responses to the defence, claim reversals and counter-cases. Example: in
  `e1-gpt61sol-v-astra/game-01` d2 the Imp drops a fake Slayer for a Mayor claim in his defence, and the comments
  test it. Only 6% of comments are content-free short lines.
- Older models never pass: comment silence is 0–4% for GPT-5.x, o3, Opus 4.5–4.8 and Fable 5, against 52–65% for
  Opus 5.5, Sonnet 5.5, Astra and GPT-6.1 Sol. Their comment rounds are 10–12 full speeches.
- The nominee also gets a comment turn in a random wave. One time in three that is wave 1, so they cannot answer the
  comments.

**Votes.** 209 blocks, 136 short, 1 tie.
- Living Butlers voted yes 64 times and no 83. No Butler notice fired, so no Butler tried an illegal yes.
- Vote remarks are made on 31% of votes (mean 9.5 words). They are cheap and informative ("Fair on Kit — I did
  offer…").
- Votes are sequential and take about 9% of summed wall-clock.

## 5. Dead players and ghost votes

- The dead stay engaged. Silence: private 16.6% (alive 5.4%), town square 23% (alive 14%), comments 34% (alive 31%).
  They send 23% of all whispers.
- Dead evil players coordinate ghost votes. Dead good players lobby with their own results ("Gray here, dead, and I
  was the real Empath").
- **Ghost votes matter.**
  - 189 were spent.
  - 19 blocks needed them, 13 of which ended in that execution: 10 evil players, including 4 Imps. Good won
    `gpt61sol-v-astra` swap d4 on 6 ghost votes.
  - 132 of the 189 were surplus to the threshold, sometimes deliberately, to stop a counter-nomination.
  - 148 of the 327 players dead at the end never used theirs.

## 6. Prompts and word limits

- **No leaks found in the day flow.** The dropped-nomination notice names only the nomination that was taken.
  Whisper metadata shows co-recipients only.
- **The comment prompt lacks the pile-on reminder.** It says "Say something to the town before the vote, or
  nothing". The vote prompt already says "don't just restate your vote". The comment round is where herding is worst.
- **Private-time prompt.** "(up to 2 whispers)" is misread by some replies-only models as a per-phase limit (20
  cases). "(up to 2 whispers this turn)" fixes it.
- **Word caps rarely bind.**
  - `[cut off]` appears on 54 of 6,015 town-square lines: 45 of them o3 (12% of its lines) and 9 Opus 4.8. Also 3
    defences and 4 vote remarks; 0 whispers and 0 nominations.
  - The prompt's "rarely more than 60 words" is ignored by older models (median line: Opus 4.8 79 words, GPT-5.2 77,
    o3 77) and followed by newer ones (Opus 5.5 44, GPT-6.1 Sol 37, Astra 38).
  - Keep 150: verbosity is a measured behaviour, and the cap only stops runaways.
- **Nomination passes.** 83 passes (2%) carried text that is never heard ("Pass."). Harmless.

## 7. Cost against value

- Private time is the largest cost (34% of spend, 44% of output tokens). It is also where the deception and
  cross-checking happen, so it is money well spent.
- The town square takes 30%.
- The smallest-value items are:
  - the dropped nominations ($26, 3%);
  - the closing nomination call ($16.5, 2%);
  - comment turns of models that never pass.
- None is worth a rule change.
- Probes are 10% of spend.

## Ranked recommendations

1. **Keep 3+3, 2 whispers and 3 waves unchanged.** (No change; consistent with CLAUDE.md.) The evidence: low
   silence, high novelty, a working reply cadence, one same-wave collision in 60 games, and realistic private
   scheming.
2. **Comment-turn prompt: add "don't just announce your vote".** One clause, mirroring the vote prompt. It targets
   the 36% of comments that are vote announcements. It is a prompt change that affects play, so bump PROTOCOL.
3. **Drop or sharpen "named players go first".** It sorts 80% of the table, so it is close to noise, and it slightly
   skews evil toward early waves.
   - Option A: remove it. That is simpler and removes one line from the prompt.
   - Option B: "players named in a beat go first in the next, most-named first". Still one line.
   - Not in CLAUDE.md's fixed list (it dates from v4).
4. **Say "this turn" in the private-time prompt.** One word; it fixes the per-phase misread.
5. **Cosmetic, no protocol change.**
   - One notice per nomination round instead of one per dropped nominator (1,039 lines).
   - README: "in three groups", not "in groups of three".
6. **Optional, low value.** Split waves as evenly as possible (10 players: 4/3/3, not 4/4/2), and let the nominee's
   comment turn come last. Each is one line and changes play (bump PROTOCOL).
7. **Optional, flag: touches a CLAUDE.md decision.** "If several nominate, the most-nominated target is taken (ties
   at random)". It would remove the 31 minority picks, 5 of which were executed. The current weighted-random pick
   already follows hands most of the time, so I would not change it without the user.
8. **Do not shorten late days or limit the dead.** Either would change a user decision (fixed length; dead players
   talk and whisper). Late days are only 16% of spend, and ghost votes decided 13 executions, including 4 Imps.
