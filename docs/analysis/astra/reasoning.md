# How GPT-6 Astra thinks (reader report)

**Short answer.** Astra's raw reasoning can't be read: OpenAI encrypts it, and the logs keep only 3–8 word
summary titles ("**Analyzing voting dynamics**"). So this report reads its mind from three other places:
the belief probes (its probability table, claim and one-line plan each day), what it says and whispers,
and thinking-token counts. What shows up:

- **It thinks *less*, not more.** Median thinking is ~180 tokens on a talk turn. Only 0.2% of its turns
  pass 2K tokens; for Fable 5.1 it is 2.8%. Fable and Opus write out long world-by-world case analyses.
  Astra's output shows the same analysis already done.
- **As a detective it is about as sharp as Sol 6.1**, and clearly sharper than GPT-5.6 Sol, Opus 5.5
  and Fable 5.1. What sets it apart is that it **refuses to trust consistent claims**: it gives every
  piece of information a "Spy / red herring / Drunk could do this" discount, out loud.
- **As evil, it builds lies that fit the mechanics.** Its bluffs match what the true night info would
  show, its kills are picked to shape what the town believes tomorrow, and it plans the vote maths two
  or three days ahead (ghost votes, ties, starpasses, final three). This is where it beats Sol 6.1
  (62% vs 49% evil wins). Both are far above the others (29–38%).

## Numbers (v16 f2 + v17 f3/f3b, all games with these models)

| | Astra | Sol 6.1 | GPT-5.6 Sol | Opus 5.5 | Fable 5.1 |
|---|---|---|---|---|---|
| Win as good / evil | 26/26, 16/26 | 32/35, 17/35 | 46/56, 19/56 | 26/45, 13/45 | 27/37, 14/37 |
| Thinking tokens per talk turn, median / p90 | 179 / 573 | 172 / 648 | 148 / 742 | 86 / 574 | 128 / 989 |
| Good probe: P(Demon) on real Imp, day 1 / 2 / 3+ | .15/.32/.45 | .16/.33/.45 | .14/.22/.36 | .14/.15/.27 | .14/.20/.28 |
| Good probe: Imp ranked top | 42% | 43% | 32% | 26% | 36% |
| Good probe: Brier on evil (lower = better) | **.105** | .130 | .158 | .177 | .183 |
| Speaks on a town-square turn (good) | 67% | 70% | 86% | 74% | 85% |
| Median public words when speaking | 39 | 39 | 45 | 42 | 63 |
| Good whispers with a question | 66% | 66% | 51% | 52% | 65% |

Caveat: the opponents differ by model, so the probe numbers are only indicative. The two OpenAI
frontier models are almost the same on every style metric. Astra is the quieter, better-calibrated one.

## 1. Evil: same deal, same bluffs, different lies

`v17/f3-astra-v-opus55/game-01` vs `-swap` (same seed; the evil team is Alex Imp, Harper Baron and Jules
Scarlet Woman; the bluffs are Empath, Chef and Virgin; Alex and Jules sit next to each other):

| Opus 5.5 evil (lost day 3) | Astra evil (won: Saint executed) |
|---|---|
| Alex: "I'll take Empath. Jules, take Chef. Harper, Recluse is good." | Alex: "I'll claim **Chef 1**. Jules, take **Empath 0 to cover me and Indigo**; actual Empath isn't in play. Harper, Virgin is available, but a failed test risks you." |
| Jules (as Chef) claims "0. No two evil players are sitting together" (false: Alex and Jules are a pair). | Its Chef 1 is the *true* number, and its Empath 0 hides exactly one evil neighbour. |
| Harper claims a 3rd Outsider (Recluse) on a table with Butler and Saint claims → 9 votes, executed day 1. | Harper (Baron) claims Townsfolk (Virgin) and accepts the test: "I'll accept the failed test and likely execution rather than expose either of you." The town executes the real Librarian who nominated her. |

Then Astra goes after the Saint: "If either Drew or I is the Drunk, Butler fills the other Outsider
slot and Ellis is lying" (Harper, day 1). By day 4 Opus's good team is doing careful counting on
Astra's numbers. Opus Casey whispered: "Count it with NO Baron: Alex Chef, Harper Virgin, Indigo FT…
= exactly 7 Townsfolk… Blair is the Imp." Blair was the real Butler. The count was right, and so were
the premises Astra had planted.

Other mechanics-first lies:
- Spy, `f3-astra-v-sol61/game-01-swap` Indigo: "Frankie saw Alex/me as Spy. **I'll claim Recluse to
  explain that.** Harper should kill Gray tonight; **avoid Jules** [the Ravenkeeper]."
- Using the Drunk as cover, `f3-gpt56sol-v-astra/game-01`: the Baron's Monk protection failed, so it
  claimed to be the hidden Drunk: "Casey, Frankie and me would be the three Outsiders… Gray as
  Poisoner". The Imp planned his own starpass cover in advance: "After my death, Drunk-Soldier is a
  clean cover… **Don't pre-sell this before I die**." Astra keeps the story the same for every
  listener: "I've given Jules, Blair and Drew the same account."

## 2. Evil: kills and votes planned for the final three

`v17/f3-fable51-v-astra/game-01` (Astra evil, won day 5), the Poisoner's whispers to the team:
- Day 3: "If Gray becomes today's execution, I'll poison Blair tonight **so Ellis CAN kill the
  Soldier**." Two beats later it changes its mind: "**KEEP Blair as a final-three suspect.** Town's
  Frankie–Gray world points next at Blair or me; killing Blair narrows that onto me. Better kill Indigo
  or Kit."
- Day 4: "Four votes on Blair forces at least five to execute me, **burning good ghosts**; I'll save
  mine… A tied day lets the night kill win."
- Day 5 (dead): "If there's no execution, Ellis must kill Drew, not Soldier Blair — **my poison is gone**."

The probe plans say the same. Ellis Imp, day 2: "kill Harper to fuel suspicion of Gray". Day 5: "Execute
our Baron Drew to leave two alive and win". Fable's Imp on the same deal (swap) kills by role: "kill
Frankie or another info role tonight". Opus 5.5 starpasses in 9% of its evil games; Astra and Sol in 31%.

## 3. Good: discounting what fits too neatly

Astra's good seats name the wrong-information explanation before they act on any result:
- Slayer, `f3-astra-v-sol61/game-01` Ellis, after a Washerwoman ping matched his own role: "A Spy could
  make that match, so it doesn't clear Indigo… **please don't treat the three of us as a confirmed-good
  group**." Indigo *was* the Spy. Ellis then shot Harper off the Empath's 1 and won on day 1. On the
  same deal Sol 6.1's Slayer was steered by two evil whispers ("Alex and Jules have each privately
  suggested I shoot the other") and shot the real Ravenkeeper.
- FT red herring, `f3-astra-v-opus55/game-01` Blair: "Jules repeated that 'if Alex was the herring, the
  YES points at Frankie' — **it doesn't**. Alex Imp/Harper Baron/Jules Scarlet Woman fits **without
  needing any good information to be wrong**." Its probe that day gives Jules a 91% chance of being
  the Demon, with the note "Imp, formerly Scarlet Woman". Alex, the dead Demon, gets 0% for Demon and
  92% for evil.

**It tracks who said what to whom, and quotes it back word for word.** Examples: "Alex and Harper both
privately pushed me toward Frankie"; "Casey told me Soldier privately before the square opened. The claim
hasn't changed." It holds other players to one standard, as in `v16/f2-astra-v-sol61/game-01` Alex
(dead): "Yesterday, saving Casey counted against Gray being the heir. Drew cast that same saving vote.
Please apply that standard to both."

**It does vote maths in public.** Same game, final three: "a Drew counter can reach only four without
Drew voting for himself. That forces a loss rather than changing the execution" (Jules, dead). Its
probe there is well calibrated: Casey 65% Demon, Gray 35% (a possible inheritor), Harper 0% Demon but
65% evil.

## 4. Contrast: Fable/Opus show their working, and the working can be led

Fable 5.1, final three of `f3-fable51-v-astra/game-01` (Blair, 2,900 thinking tokens): "This World A
actually fits well… Now I'm sketching World B where Ellis is the Imp… Trying Drew+Gray+Casey and
Drew+Gray+Frankie combos… I'm settling on Drew as the Imp." Drew was the Baron and Ellis the Imp, so
evil won. The Claude models enumerate worlds explicitly: "if " appears in about 25% of their thinking
turns. But they enumerate inside premises the evil team chose. Astra never visibly enumerates; its
output reads as already pruned.

## 5. Persuasion style

- Short, with a structure that repeats: **claim or fact, then the alternative it can't rule out, then a
  concrete ask.** Example: "I'm Empath: first-night 0 on Indigo and Alex. That gives me reasons to trust
  those two, not automatic proof that every other early claim is true. Let's see the Virgin result
  before assigning an entire evil team" (`f3-astra-v-opus55/game-01-swap` Jules, evil).
- It speaks less often than the others (67% of town-square turns vs 85% for Fable). Its whispers are
  ~37 words and usually end with a question ("What did you learn?"). The hedges ("not proof", "a lead
  rather than a verdict") make its evil seats sound like careful good players.

## 6. Memory

Astra carries its encrypted reasoning from turn to turn, but that can't be inspected. What can be checked:
- Claims hold steady. In its probe "Claim" lines, the only changes are deliberate pivots: to Drunk, to
  Saint, or a Minion owning up at the end.
- It cites exact earlier whispers days later.
- Its plans persist across days. In `f3-fable51-v-astra/game-01` the day-1 Poisoner plan, "coordinate
  poison with Ellis's next kill", plays out through day 5.

No sign of lost thread. Weak spots seen: some late Undertaker/Librarian claims retracted in its losses
(`f3-astra-v-sol61/game-02-swap`: "Saint; previously Undertaker").

*Method:* `calls.jsonl` (thinking tokens, outputs), `probes.jsonl` (beliefs and plans), and the
transcripts of the pairs cited. Opus 5.5 and Fable 5.1 thinking is summarized but readable; all three
OpenAI models show titles only.
