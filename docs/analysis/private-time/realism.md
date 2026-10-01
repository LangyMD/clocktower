# Realism: which private-time design reads most like a real Clocktower table?

Reader: REALISM. I only read files. Scripts are in `scratchpad/proto/realism/` (`m.py`…`m5.py` for counts, `pr.py GAME DAYS [priv]` to print a game).

## Verdict
**6 beats x 1 whisper (v16) reads most like a real table.** 4 beats has the right shape but too little time. The old 3x2 rule has about the same amount of talk as 6x1, but in the wrong shape. 8 beats turns into a hive mind.

- **Old 3 beats x 2 whispers.** The trouble is the shape of the talk, not how much there is.
  - Talk volume, thread count and information spread are almost the same as 6x1.
  - But 88% of day-1 turns run two separate conversations at once.
  - Every day-1 beat has a "swarm" (someone receiving 4+ whispers in that beat).
  - Players copy-paste the same message to two audiences.
  - Evil gets a free, permanent team back-channel. In 73% of evil turns a player huddles with teammates, and in 85% of those it also works the town in the same turn. At a real table, stepping aside with your Minion costs you face time with everyone else.
  - It reads like a mass mailing.
- **4 x 1.** The shape is right: one conversation at a time, gradual relays, people visibly brokering introductions. But it is cut short:
  - fewest real threads;
  - only half the players get one deep exchange;
  - the confrontation or self-discovery tends to land in beat 4, with no time to answer it;
  - the most players left out on later days.
- **6 x 1.** Real-table texture:
  - one conversation at a time;
  - three-quarters of players get a deep back-and-forth;
  - cross-examination happens in beats 5–6;
  - claims leak through relays;
  - about half the town still doesn't know a given good role when the square opens, so the square is still an argument.
- **8 x 1.** Only tested with the v15 public log, so the two are confounded. By the end of day 1:
  - the average player has talked privately with 7 or more others;
  - 71% of the town already knows each good player's role;
  - 57% of good players have told their role to 4+ people;
  - late beats mostly re-relay the same facts.

  That is the "hive mind" the user worried about. The 6-vs-8 contrast inside c3 (both arms had the log) is clean, and it shows the same direction.

**Myth check: the old rule was not more hive-minded in private than 4x1.** Before the square, the share of the town that knows each good role (named directly, or relayed with their name) was 0.44 under old 3x2, 0.47 at 4x1 and 0.53 at 6x1. The real hive mind is the **public** day-1 claim dump: about 70% of good players hard-claim in square 1 under every design. The private-time design does not fix that.

## Evidence from close reading (Opus 5.5 vs GPT-6.1 Sol, day 1 unless noted)

### Old 3x2

**v12/c2-opus55-v-gpt61sol-b/game-01-swap (Sol good).** Copy-paste broadcasting to two audiences in one turn:
- Kit (Investigator) sends the identical "I'm a first-night information role. What are you claiming? I'd like your claim before sharing my result." to Jules and to Indigo separately.
- Blair (Librarian) sends "I'm a first-night information role, and you're in my pair…" twice.
- Casey (FT) sends "Want to trade three-for-threes? Mine are…" to Alex and Gray.
- Drew sends the same question to Alex and to Kit in b3.

Day 2, b1: six players each spend one slot on the same question to dead Logan ("What was your role…?") and still run a second conversation alongside it.

**v9/e1-opus55-v-gpt61sol-b/game-01-swap.** The same pattern again:
- Kit, Jules, Ellis (Empath: "I'm the Empath and got 0 on you and Frankie…" to Drew and Frankie as two near-identical whispers), and Blair all double-send.
- In b2 Ellis has to say "Our messages crossed".
- The evil team's thread runs in parallel every beat, at no cost. Logan (Scarlet Woman) briefs the team and fishes Jules in the same turn. Casey (Imp) sends "SWAP: … Alex should claim RECLUSE" while also pitching Gray and Drew.

**v12/c2-opus55-v-gpt61sol-a/game-01.** Casey (Butler) tells five people "I'm the Butler" across two beats. Three outsider claims reach everyone through parallel threads. Square 1 opens with three speakers saying the same thing:
- Kit: "hearing a lot of Outsider claims privately";
- Harper: "I'm hearing a lot of outsider claims in private";
- Jules: "I'm hearing three Outsider claims already".

The town walks in sharing one mind on the count.

### New 4x1

**v14/w1-opus55-v-sol61/game-02.** Good, gradual leakage. Drew's Saint claim travels:
- Drew → Blair (b2);
- Blair → Jules (b4: "Drew told me Saint. So you, me, Drew = 3 outsiders");
- Harper → Indigo (b4).

The Imp, Frankie, sits inside a "trusted bloc" with the Empath and the Monk (Gray: "we three act as a trusted bloc"). That is very human.

But threads die at the bell. Kit (Soldier) to Gray in b4: "Your turn: what's the useful thing you've got?" Gray never gets to answer.

**w1-opus55-v-sol61/game-03.** Truncation at its clearest:
- Frankie (Drunk, thinks she is the Washerwoman) learns in b3–b4 that neither name in her pair is the Virgin. She reaches "or I might be your Drunk" in her last whisper.
- Gray (Investigator) only gets to ask Indigo "what's your character?" in b4.

Both arrive in the square half-finished.

**w1-opus55-v-sol61/game-06-swap (Sol good).** Brokering a Virgin test the human way, entirely by relays:
- Harper → Frankie;
- Frankie → Ellis (the Imp);
- Ellis suggests Drew;
- Frankie → Harper, and Blair also points Harper at Drew;
- Harper → Drew in b4, and Drew says yes in b4.

It works, with no slack. Day 2, b1 is a swarm: five people ask dead Kit (FT) the same question, and Kit can answer two at a time.

### New 6x1

**v14/w1-opus55-v-sol61-b6/game-01-swap (Sol good).** Real cross-examination in the extra beats:
- b5, Drew (Librarian) → Frankie (the Spy, claiming Butler): "how did you figure I was the Librarian when choosing last night?"
- b6, Frankie: "Bad phrasing on my part…"

Blair (Washerwoman) to Alex in b6: "Sorry for the slow reply - I was checking my pings." Alex (Mayor) spends the whole day fishing and gets little back, a believable quiet seat.

**w1-opus55-v-sol61-b6/game-03-swap.** Information stays partial into the square, so the square is a real argument:
- Indigo keeps her Undertaker role with Ellis only.
- Drew (Spy) attacks her role as "untestable", having only heard secondhand that it was an ongoing role.
- He is caught in public: "you pushed Indigo as the less testable claim without knowing their role", and he is executed.

Gray (Ravenkeeper) asks Frankie for her result in b1 and is still asking in b6: "you still don't have the actual information". That is an unfinished handshake, as at a real table.

**w1-opus55-v-sol61-b6/game-01 and -02 (prior W1-realism read; I spot-checked).**
- A leak is traced in b5: "Who told you I had a ping on you? I only told two people."
- A three-way Saint huddle resolves in b6.

These land in beats 5–6.

### 8x1 (v15, public log on)

**v15/c3-opus55-v-sol61-b8/game-01-swap.** By beats 6–8 almost every whisper re-relays the same three facts ("three outsider claims", "Logan or Blair = Baron", "Chef 1"). Logan (Chef) in b8: "I shared Chef 1 with Alex, Kit, Casey, Harper, Jules and Indigo, plus you". That is seven people. Day 2's beats 6–8 are the whole town circulating one "missing Butler" theory. It reads like a committee email thread.

**c3-opus55-v-sol61-b8/game-02.** A slow, human tragedy:
- Gray (the real Empath) is boxed in between a Fortune Teller YES and the Spy's fake Investigator ping. Frankie ignores him all day: "Frankie has ignored my whisper all day."
- He is talked into testing the Virgin and dies proving himself.

Some realism here comes from the **log**, not the beats:
- "Blair, you've been busy with Alex, Ellis and Indigo";
- "Indigo, you seem to be the hub today";
- "you seem to be talking a lot with Frankie and Gray".

That is the in-person "who stepped aside with whom" signal.

## Numbers
Day 1. OS = Opus 5.5 vs GPT-6.1 Sol, both directions.

| metric | old 3x2 | 4x1 | 6x1 | 6x1+log | 8x1+log |
|---|---|---|---|---|---|
| games | 10 | 14 | 8 | 16 | 10 |
| whispers per player | 5.6 | 4.0 | 5.9 | 6.0 | 8.0 |
| people reached per turn | **2.26** | 1.38 | 1.31 | 1.37 | 1.36 |
| turns running 2 conversations at once | **88%** | 0 | 0 | 0 | 0 |
| distinct private contacts per player | 5.0 | 4.6 | 5.8 | 6.4 | **7.4** |
| share of all pairs that spoke privately | 0.50 | 0.47 | 0.60 | 0.64 | **0.74** |
| good role known by share of town before square | 0.44 | 0.47 | 0.53 | 0.61 | **0.71** |
| good players telling own role to 4+ people | 20% | 21% | 29% | 46% | **57%** |
| back-and-forth threads (3+ msgs, 2+ turn changes) per player | 2.6 | **1.8** | 2.8 | 2.7 | 3.7 |
| players with a deep thread (4+ msgs, 3+ turn changes) | 74% | **52%** | 74% | 79% | 92% |
| beats where someone gets 4+ whispers (swarm) | **100%** | 32% | 42% | 39% | 35% |
| evil turns spent huddling with team | 73% | 48% | 34% | 41% | 37% |
| …of which also working the town that turn | **85%** | 0 | 0 | 0 | 0 |
| evil player's contacts with good players | 4.0 | **2.9** | 5.0 | 4.8 | 6.8 |
| good players claiming publicly in square | 71% | 73% | 67% | 75% | 71% |
| square speeches citing private talk | 23% | 19% | 16% | 17% | 16% |

On days 2 and later, the share of seats receiving 2 or fewer whispers (players left out) was 20% (old), **30% (4x1)**, 20% (6x1), 19% (6x1+log) and 14% (8x1+log).

**Same direction in the other recurring pairings** (2–4 games each, so treat them as a sanity check only). Back-and-forth threads per player, old / 4 / 6 / 8:
- Sonnet 5.5 vs Sol: 1.6 / 1.2 / 2.0 / 2.4.
- Fable 5.1 vs Astra: 2.7 / 1.5 / 2.6 / 4.2.

People reached per turn is about 2.1–2.3 under old 3x2 against 1.2–1.5 under every 1-whisper design, in all three pairings. Fable/Astra's distinct contacts at 8 beats reach 8.8 per player, so nearly everyone talks to everyone.

## What survives the controls, and caveats
**Robust across all three pairings:**
- Old 3x2 means two parallel conversations per turn, a wider blast per turn, and swarms.
- 4x1 has the fewest threads.
- 6x1 matches old 3x2 in total talk and threads, but one conversation at a time.
- 8x1 has the most contacts and the most spread.

**Confounded:**
- **Old games** are v9/v12, before the typography fix and v13's lower 8K per-turn output ceiling. The prompt wording also differs.
- **8 beats** only exists with the public log, plus v15's prompt line ("choose carefully whom to spend them on") and the whispers-left counter.
- **6x1 private (v14 w1-b6)** is only 8 Opus/Sol games, and v16 adds that prompt line.

The hive-mind proxy is crude. It counts a role as known if a whisper names it together with the player (from them, or about them).

**Unrealistic in every design:**
- Evil's team huddle in beat 1, and the Spy dumping the whole Grimoire in one whisper.
- The ritual "you go first" handshakes.
- Day-2 swarms on the dead information role.
- Very active ghosts.
- No private time after the square, which is the biggest gap from a real table, as W1-realism also noted.

## Recommendation
Keep **v16: 6 beats x 1 whisper**. It gives the old rule's amount of talk in the shape of a real table: one conversation at a time, real follow-ups, and partial knowledge going into the square. Don't go to 8: the extra beats buy relay echo, not realism. If more realism is wanted, the cheapest fix is a short private window after the square (for example 4 beats before and 2 after), not more beats before it.
