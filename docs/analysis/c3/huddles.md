# Do three-person huddles work? (w1 / c3 logs)

## Verdict
**The mechanics work, and I found no bug.** When A whispers to B and C, the event goes to all three. Each recipient sees the whole address line, e.g. Jules saw `[whisper] Drew → Jules (you), Frankie: …` (v14/w1-opus55-v-sol61-b6/game-01). So both know the message went to both, and a reply to both reaches both. Across 18,198 whispers parsed from calls.jsonl:
- no invalid or self names;
- 3 whispers addressed to more than two players (trimmed, and the sender was told);
- 2 extra whispers dropped (sender told).

The models understand the setup. For example, Ellis (Fable 5.1, w1-fable51-v-astra-b6/game-01, day 5) reasoned: "Since Blair whispered both of us together, Alex already knows about this — so I should reply to Blair alone." I found one misreading in the thinking: o3 (w1-o3-v-sonnet4/game-01, Ellis) said "I can only whisper to one person this turn."

**Prompt gaps (small).**
1. The w1 prompt said "Players pair off and whisper … one private conversation at a time", which pushes against huddles. v16 replaced it with "choose carefully whom to spend them on".
2. Neither version says outright that a whisper to two players is a shared three-way conversation. Suggested fix: add one line after "to one or two players" in `prompts.py`: *"A whisper to two players is a three-way conversation: both see it and see who else got it, and either can answer both."* The models already behave as if they know this, so expect little change in play. It mainly helps the older models: o3, Sonnet 4 and GPT-4o send only 2–8% of their whispers to two players.
3. A code nit with zero cases so far: `whispers()` silently drops an invalid or self name in `to`, and a `to` given as a string, without telling the sender. It could tell the sender the same way it does for over-addressed whispers.

**Behaviour.** Huddles work, but mostly as a one-off broadcast, not a lasting three-way thread:
- Only about a quarter of recipients answer the whole group with their next whisper.
- Most go to an outsider instead, usually because someone else just whispered them.
- Lasting three-way threads are mostly the evil team's private chat.
- Good and mixed huddles fall back to pairs or to new contacts.

## Numbers
Unit: one recipient of a two-recipient whisper (A → B, C). I classified that recipient's **next whisper the same day** after they could have seen A's (a later wave in the same beat, or a later beat). Wave = the cluster of whisper timestamps within a beat.

| Next whisper by B (or C) | w1-b6: 12 games, 6 beats | w1-b4: 38 games, 4 beats | c3: 40 games, public log ⚠ | c3h: 10 games, log + hint ⚠ |
|---|---|---|---|---|
| Recipients (n) | 1,794 | 4,034 | 7,990 | 1,796 |
| **Whole group (A + other)** | **23%** | **24%** | 17% | 17% |
| A only | 4% | 3% | 5% | 4% |
| Other recipient only | 3% | 5% | 3% | 4% |
| A or other + an outsider | 9% | 10% | 16% | 15% |
| Outsider(s) only | 48% | 40% | 46% | 46% |
| No whisper left that day: last beat | 9% | 15% | 9% | 10% |
| No whisper left that day: other | 3% | 3% | 4% | 4% |
| *1-to-1 baseline: recipient's next whisper goes back to A* | *43%* | *39%* | *40%* | *40%* |

- **Timing of group replies** (w1-b6): 216 in the same beat (later wave), 197 the next beat, 4 later. Replies that come back, come back at once.
- **Ever answered that day** (w1-b6): 35% of huddle recipients whisper the whole group at some point. 47% whisper A at all, against 60% for a 1-to-1 recipient. A huddle gets fewer answers than a direct whisper.
- **Persistence**, one triad on one day (w1-b6, 444 triad-days):
  - 56% are a single message;
  - 19% get a reply from a second member;
  - 23% have all three members speaking to the group;
  - 29% reach 3+ group messages.
  - w1-b4 is similar: 58% single message, 21% all three speak.
- **Competing whispers** (w1-b6): a recipient replies to the group 31% of the time when no one else whispered them in the meantime, and 24% when someone did. Of the "outsider" next whispers in established threads (w1-b4 and w1-b6 together), 41% answer an outsider who had just whispered them, 26% resume an earlier thread with that outsider, and 32% open a new contact.

**Good vs evil** (w1-b6; w1-b4 is the same):

| | Evil team (all three evil) | Good or mixed |
|---|---|---|
| Next whisper goes to the whole group | 34% | 20% |
| Triad-days where all three speak | 35/41 | 69/403 (17%) |
| Recipients going straight back to A only | 0% | 3–7% |
| Share of own whispers sent to two players | evil senders: 54% | good senders: 36% |

- The evil team's three-way chat is a real, persistent channel: the Spy's Grimoire dump, kill and poison plans, assigned bluffs. Evil recipients also leave it for outsiders 54% of the time; that is the bluffing work.
- Good huddles break into pairs ("other only" or "A only": 7–9%) and into relays to new people.
- **c3/c3h ⚠ (public who-whispered log, not today's rules):** group replies fall to 17%. In c3h, after the hint that huddles get read as a team, evil senders' two-player share fell from 47% to 34% and all-evil triad-days per game from 3.2 to 2.0. Don't pool these with w1.

**By model** (recipient's next whisper goes to the whole group; w1 b4+b6; n in brackets; anything under ~100 is noisy):

| Model | Good | Evil |
|---|---|---|
| Opus 5.5 | 19% (1,489) | 31% (498) |
| GPT-6.1 Sol | 19% (978) | 27% (931) |
| Fable 5.1 | 18% (420) | — |
| Astra | 20% (157) | 32% (310) |
| Sonnet 5.5 | 28% (334) | 31% (127) |
| Sonnet 4.5 | 51% (77) | 45% (64) |
| o3 (good) | 4% (23) | — |
| Sonnet 4 (good) | 0% (16) | — |

- Opus 5.5 good is the most likely to narrow a huddle to one member (other only 8%, A only 7%).
- GPT-6.1 Sol almost never narrows (1–2%); it widens instead, by adding an outsider (12%).
- Sonnet 5.5 good often sends no whisper at all (25% none).
- Model differences are small next to the good/evil gap.

## Why players leave a group
I read about 70 cases where a recipient of an established thread (a second or later group message) sent their next whisper only to people outside it. Most of the quotes below come from the Claude models, whose full reasoning is logged; Sol only logs headings like "**Coordinating team communication**".

1. **Another conversation is waiting** (the most common; about 41% by count). Example: Jules (Opus, good), w1-opus55-v-sol61-b6/game-01, day 1, beats 2→2: *"Since only one whisper is allowed, I'll reply to both Blair and Ellis together"*. He answered a different huddle rather than Drew/Frankie's.
2. **Evil leaves the team chat to work the town.** Logan (Opus, evil), w1-opus55-v-sol61-b6/game-03-swap, day 1, right after the Spy's Grimoire dump: *"I should whisper to my neighbors, Kit and Alex, claiming Butler… to start building trust."* Frankie (Opus, evil), b6/game-01-swap, day 1: fixed a slip with Drew: *"that was sloppy phrasing… I should clarify."*
3. **Checking or relaying a claim with the player who can test it.** Jules (Opus, good), b6/game-02, day 1: *"worth flagging to Harper, whose Fortune Teller ability could check Kit."* Blair (Opus, good), w1-opus55-v-astra/game-02, day 2: *"I'll whisper Frankie quickly to verify the claim."*
4. **The group has agreed, so spread its plan or vote** (vote whipping). Logan (Sol, evil), w1-opus55-v-sol61/game-03, day 4: *"Kit is willing to back Gray… I asked Kit and Casey together"* (sent to Blair and Ellis). Frankie (Opus, good), b6/game-02, day 3: *"Maybe I should loop in Ellis Monk on this."*
5. **Private disclosure to one trusted player.** These cases leave the group to speak to one person, or narrow the group to one member. Harper (Opus, good), w1-opus55-v-sol61/game-02, day 2: *"Indigo is mechanically confirmed good, telling Indigo I'm Monk… feels like a safe move."* Indigo (Opus, good), game-05, day 1: told only Jules *"I'm the Soldier."*
6. **Distrust of the third member, so drop them.** Harper (Opus, good), game-02, day 3: left Gray out and told Frankie *"Gray asking me to keep protecting him is…"*. Jules (Opus, good), game-06, day 4: dropped Logan, whom he suspected, and wrote only to Casey.
7. **Structural.**
   - No beat left: about a quarter of departures happen at the last beat.
   - A dead triad member: 26–28% of departures, but whether that is the cause is unclear.
   - Two recipients in the same wave reply at once, so they can't see each other.

Being swarmed (several whispers arriving at once) is the root of reason 1 rather than a separate reason. I found no cases of a player leaving because the group was "done talking" without a next step. Players leave to do something with what they learned.

**Side effect worth knowing:** the huddle's membership is itself evidence. Logan (Fable 5.1, good), w1-fable51-v-astra-b6/game-01, day 3, quoting Drew: *"Ellis's very first day-one whisper to him was a group with Frankie… evil teammates often cluster that way."* That is evidence even with whispers fully private.

## Caveats
- The current-rules sample is small: w1-b6 is 12 games covering 5 models.
- The wave of a player who sent nothing is unknown, so "no whisper" can't be split by opportunity.
- "Next whisper" measures the first move only, not the whole day.
- Scripts are in the scratchpad: `huddle.py`, `an.py`, `an2.py`, `an3.py`, `dis.py`.
