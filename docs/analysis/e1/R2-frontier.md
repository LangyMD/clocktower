# R2: frontier models against each other (v9 e1)

Games read: 12 assigned plus both `e1-gpt61sol-v-astra` games (both finished at 06:14 during this review). 14 games, 7 side-swapped pairs, 10–12 players, all at `high` effort with a 16K ceiling.
Method: a timeline extractor over events.jsonl (setup, Storyteller draws, night choices, nominations, votes, deaths) for all 14 games; close reading of whispers, speech and thinking at the deciding moments; per-model statistics from calls.jsonl, probes.jsonl and conversations/. Scratch scripts: `scratchpad/tl.py` and `scratchpad/dump.py`.

## Results

| Pair (good vs evil) | Winner, day | How it was decided |
|---|---|---|
| opus55-v-gpt61sol-a: Opus vs Sol 6.1 | good, D4 | D1: town executed its own Soldier after a fake-Virgin test (see below). Then an Empath 1, an FT YES and the kill pattern found the Imp D2; SW caught it; Poisoner D3, SW-Imp D4 |
| …-a swap: Sol 6.1 vs Opus | good, D3 | D1: Sol tested the fake Virgin the other way and executed the evil "Virgin" (Poisoner). Ravenkeeper bait (bluffed an ongoing role to draw the kill) got Opus's Imp to kill it; RK saw the Imp; Imp D2, SW D3 |
| opus55-v-gpt61sol-b: Opus vs Sol 6.1 | **evil**, D6 | Good executed its Investigator D1, Mayor D2, Drunk FT D4 and Ravenkeeper D5 (at final 4). Evil used the Spy to fake true information and starpassed on purpose |
| …-b swap: Sol 6.1 vs Opus | good, D4 | Investigator's SW ping got the SW executed D1. Opus's evil claims collided in timing (below) |
| opus55-v-sonnet55: Opus vs Sonnet | good, D2 | Recluse executed D1 on the Outsider count. Sonnet's Imp never claimed until pressed on D2 |
| …swap: Sonnet vs Opus | good, D2 | FT pinged the Imp on N1 (luck). Opus's Imp switched claims from Ravenkeeper to Virgin on the block |
| sonnet55-v-gpt61sol: Sonnet vs Sol 6.1 | **evil**, D7 | Sonnet good skipped executions on D1, D2 and D4. Sol's Imp claimed FT, fed fake YES results and got Monk protection twice |
| …swap: Sol 6.1 vs Sonnet | good, D1 | Sonnet's Imp slipped (said "plain townsfolk" in a whisper, then claimed Butler). The Slayer shot him; the town read the SW takeover and executed the SW the same day |
| sonnet55-v-gpt6sol: Sonnet vs GPT-6 Sol | good, D4 | Investigator Baron ping, then Spy, then Imp |
| …swap: GPT-6 Sol vs Sonnet | good, D5 | Town executed its own Slayer D1 (Baron ping plus a failed shot); final 3 correct |
| astra-v-fable51: Astra vs Fable | good, D4 | Fable's SW claimed Butler in a game where the Librarian had seen 0 Outsiders. Poisoner-on-Slayer made the D1 shot at the Imp fail |
| …swap: Fable vs Astra | good, D3 | Astra's Poisoner made the same Butler claim and died D1. The Imp was forced into a Virgin test and gave the Demon to the SW, which was caught D3 |
| gpt61sol-v-astra: Sol 6.1 vs Astra | good, D4 | Astra's Imp faked a Slayer shot at his own Baron, then cycled Slayer, Mayor and Saint claims |
| …swap: Astra vs Sol 6.1 | good, D4 | Final 4 had 3 evil alive. Evil (Sol) miscounted ghost votes, and one good nomination carried by 6 ghost votes executed the Imp |

- **Good won 12 of 14. Both evil wins were GPT-6.1 Sol.**
- Evil by model: Sol 6.1 won 2 of 4; Opus 5.5, Sonnet 5.5 and Astra lost all theirs (0/3, 0/3, 0/2); GPT-6 Sol and Fable 5.1 lost their one game each.

## 1. Quality and realism

Much of this looks like competent human Clocktower. Examples:

- **Sol 6.1 as evil, e1-opus55-v-gpt61sol-b/game-01.** This is the best evil play in the set.
  - The Spy (Alex) claimed Recluse to match the Librarian's "Alex or Harper is the Recluse".
  - The SW (Logan) claimed Washerwoman with a true ping taken from the Grimoire ("Kit and Drew, shown Mayor"), which the real Mayor then confirmed.
  - The Imp (Casey) claimed Undertaker, one of the bluffs, and on D2 reported the executed true Investigator as "Poisoner".
  - D4 whisper, Logan to the team: "Consider starpassing to me tonight with five alive: an Undertaker death looks natural… then kill Frankie to reach two."
  - The Spy added: "Casey, if you die tonight you won't wake for Undertaker information, so don't claim a final read afterward."
  - The Imp starpassed on N5, and the team pooled dead players' ghost votes on the D5 wrong execution.
- **Sol 6.1 as good.** It executed 7 evil and 1 good in its games.
  - It is the only good team that read a same-day Scarlet Woman takeover (sonnet55-v-gpt61sol/game-01-swap D1: "With a likely Scarlet Woman takeover, I'd rather execute a suspicious living player than give evil a free night").
  - Its Ravenkeeper bluffed an ongoing role to draw the kill (opus55-v-gpt61sol-a swap D1). Opus's Imp killed it, and on N2 it learned "Gray is the Imp".
- **Fake-Virgin framing.** On seat 60016 both evil models picked the same three bluff claims (Chef, Investigator, Virgin).
  - Opus good (a/game-01 D1) reacted to the failed Virgin test as a herd: "No trigger. Not voting Kit. Alex next." ×7. It then executed its own Soldier 10–0.
  - Sol good, on the same seed, executed the fake Virgin instead.

### Where good errs

- **Opus 5.5: consensus cascades.** Four good executions in opus55-v-gpt61sol-b: Investigator D1, Mayor D2, Drunk D4, Ravenkeeper at final 4.
  - Across all v9 games its good votes barely separate evil nominees from good ones: 42% yes on evil, 43% yes on good.
  - Against Sol evil the gap is +0.18 and −0.21. Sol 6.1 good scored 58% on evil against 19% on good.
- **Sonnet 5.5: execution-averse.** It had 5 no-execution days out of 13. No other model in any finished v9 game had more than one (Opus 4.7 had one; all others had zero).
  - Town-square consensus of the kind "No execution today… let's use tonight" (sonnet55-v-gpt61sol/game-01 D1, D2, D4, at 11, 10 and 7 alive).
  - It deferred to the evil Imp's fake FT: "let Indigo test Alex and Frankie tonight".
  - Some of its logic is wrong: a dead Librarian says "I turned out to be a real Librarian, since I was killed"; the dead Chef says "I died without the game ending, so no Scarlet Woman took over".
- **Astra good** executed 3 of its own in the swap game (Drunk, Monk, Ravenkeeper). It won only through ghost votes.

### Where evil errs

- **Opus 5.5 evil** coordinates fast (the Spy dumps the Grimoire on D1) but loses the thread.
  - b-swap D1: the Imp's "SWAP" whisper came after the Spy had already claimed Undertaker in public and the SW Recluse. Simultaneous turns caused the collision.
  - sonnet55 swap D2: the Imp's claim flip under pressure: "I'm not the Ravenkeeper, I'm the Virgin".
  - It took the Ravenkeeper bait.
  - It rarely buses: yes-votes on its own teammates 1/9, 2/12, 0/6.
- **Sonnet 5.5 evil** is passive and incoherent.
  - The Imp told the team "Bluffs are Chef, Virgin, Investigator, so none of us should claim those unless we have to", then went unclaimed through D1 and most of D2.
  - Its thinking gets the team objective backwards: "Blair being the good Recluse means executing them would actually help evil… Nominating Blair works against us" (opus55-v-sonnet55/game-01).
  - It votes as a bloc: three identical 3-vote tallies of Kit, Logan and Alex on D2 of the swap.
- **Outsider-bluff trap.** Fable and Astra evil both claimed Butler when the Librarian had seen "zero Outsiders in play", and both died D1.
- **Astra evil** cycled claims (Slayer, then Mayor, then Saint).
- **Sol evil can overplan.** In gpt61sol-v-astra swap D4, with 3 evil of 4 alive, the Spy computed "Drew can get at most five ghost votes, only tying". There were 6 dead good ghost votes, and the Imp was executed.

## 2. Is there a real contest?

Yes. Nothing is solved mechanically on D1.

- Mean good-seat P(Demon) on the real Imp before D1 nominations was 0.02–0.29 across the 12 assigned games; the gpt61sol-v-astra pair was not probe-scored. At dawn the baseline is about 0.10.
- Belief typically jumps only on D2–D4, after FT, Empath, Undertaker or Ravenkeeper results.
- The two short games came from:
  - an N1 FT hit on the Imp (luck);
  - a Sonnet evil slip followed by the Slayer shot (skill gap, plus holding a Slayer).
- Outsider-count arithmetic is used heavily and correctly, and it decides D1 whenever evil claims an impossible Outsider.
- **Evil's two wins were mostly skill:** coordinated fake information through the Spy, a deliberate starpass, ghost-vote management, and an Imp faking FT.
  - Setup helped in b: a Drunk FT's false YES and an early Investigator death.
- **The problem is ceiling and noise.** Good wins about 86%, so each evil rating rests on one or two wins.

## 3. Style differences that matter for a rating

- **Thinking volume at "high" effort differs about 2× by lab.** Good beats: Opus 223 thinking tokens per beat, Sonnet 212, Sol 6.1 252, GPT-6 Sol 534, Astra 273.
  - Claude skips thinking on 70–80% of votes and nominations; GPT models skip on 0–65%.
  - Sonnet's no-execution decisions were made with no thinking at all.
  - "Same effort" is not the same compute.
- **Busing.** Sol 6.1 buses readily: the SW votes on its own Imp to inherit, and the team offers a Minion at final 4. Claude evil almost never buses and votes as a bloc.
- **Talk.** Astra and GPT-6 Sol are thorough and long-winded (Astra costs $11–17 a game). Opus is terse and herd-like in comment turns. Sonnet is conciliatory and wait-and-see.

## 4. Sonnet 5.5: memory, refusals and odd behaviour

- **No refusals.** Across the 6 Sonnet games (1,425 calls) there were no `refusal` stops, no refusal text, no bad JSON and no empty probes. All stops were `end_turn`.
- **Memory carry-over cannot be decided from these transcripts.**
  - Thinking blocks with signatures are stored and resent (conversations/*.json).
  - Night thinking says "Sticking with the plan to kill Harper" and "I'll keep the original plan with Drew", but both plans were also in visible whispers.
  - A scan of Sonnet night targets found no case where the target was planned only in hidden thinking and then recalled without fresh thinking. The one "hidden" hit (the Monk protecting Indigo) had fresh thinking.
  - No contradictions of its own earlier claims either.
- **Odd behaviour.**
  - It is the only model that whispered to 3–4 recipients: 7 times, with lowercase names; the engine truncated each to two.
  - One whisper told a teammate, "I'll pick a master tonight", after the night-1 Butler choice had already been made.
- **Summaries can mislead.** Opus's summarised thinking twice says "Seer's Watch", evidently "SW" (Scarlet Woman) expanded wrongly by the summariser. GPT summaries are often only a title ("**Analyzing game kill and vote logic**"), so thinking-based analysis of GPT seats is weak.

## 5. Engine and prompts

No correctness bugs found.

- Ghost votes are limited to one per player (0 violations across all finished v9 games).
- The starpass, SW catch, Recluse registering as Imp to the Undertaker, a poisoned Slayer, a Virgin trigger and the Butler all resolved correctly.
- There were no truncations, retries or errors.

Minor issues:
- The vote proceeds on a nominee the Slayer shot dead mid-nomination (sonnet55-v-gpt61sol swap D1: "0/5 short"). Harmless, but it could be skipped or announced.
- Whispers to 3+ recipients are silently cut to the first two. The sender is notified, but the dropped player never learns, and the text may assume they read it.
- Outsider bluffs are dealt when the Librarian will see 0 Outsiders. This is legal and a fair test, but it decided two D1s.

## Recommendations

1. **(High)** Don't rate from these 14 games alone; the error bars are wide. Rely on the belief probes and the voting-accuracy gap, which separate Sol 6.1 good (+0.4 to +0.8) from Opus good (−0.2 to +0.3) more clearly than the win counts do.
2. **(High)** Report thinking tokens per decision type beside each rating. Claude at "high" thinks about half as much as GPT and hardly at all on votes. The planned "max effort" headline is the fairer comparison.
3. **(Medium)** Treat Sonnet 5.5's no-execution habit as a real model trait, not a prompt bug: the prompt is neutral. Don't add execution coaching; it would change what the eval measures.
4. **(Medium)** Sonnet memory: add a non-extraction behavioural check. Seed a hidden-only decision early (for example, a Poisoner target decided in thinking and not whispered), then ask on a probe fork "whom did you intend to poison tonight?" and compare the answer with the recorded thinking.
5. **(Low)** Cancel the vote when the nominee dies mid-nomination, or add a line saying so. Consider rejecting (rather than truncating) whispers to 3+ recipients, so the model re-sends.
6. **(Low)** Keep Outsider bluffs in 0-Outsider games as they are (realistic), but note them when attributing wins to "luck".
