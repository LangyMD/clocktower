# Why GPT-6 Astra wins every game as good (detection)

Read for this: 26 Astra-good games (v16 f2, v17 f3/f3b), with close reads of the pairs against sol61,
gpt56sol, opus55 and fable51 and of the long games. Numbers come from `events.jsonl`/`probes.jsonl`
across all 372 games.

## The answer

Astra's good team doesn't find the Demon much faster than anyone else. **It almost never executes its
own players, and it won't be talked out of a correct execution.** It does this as a whole table, not
through one star seat. Three habits do most of the work:

1. **It tracks where each claim came from.** Who said what to whom, and whether before or after
   they heard the result.
2. **It corrects false premises on the spot.** It says "that doesn't prove X" every time someone
   overstates.
3. **It treats inconsistency as evidence.** A player who reverses a stance or keeps swapping
   explanations gets noted.

It also gets real luck from Slayer shots (6 of 26 wins), and its opponents are never Astra-as-evil,
the strongest deceiver in the eval.

| good team | games | win | executions that hit evil | good players executed / game | good "yes" votes on good nominees |
|---|---|---|---|---|---|
| **Astra** | 26 | 100% | **76%** (83% without Virgin tests) | **0.62** | **12%** |
| GPT-6.1 Sol | 35 | 91% | 65% | 1.00 | 14% |
| GPT-5.6 Sol | 56 | 82% | 54% | 1.64 | 21% |
| Fable 5.1 | 37 | 73% | 50% | 1.78 | 28% |
| Opus 5.5 | 45 | 58% | 43% | 2.16 | 32% |

- Astra executes evil about as often per game as everyone else (1.9). The difference is that it
  doesn't waste days on good players, so games end early: 18 of 26 wins came by day 3.
- On the probes, its individual reads are better than the field's but close to Sol 6.1's. At day-1
  nominations, an Astra good seat gives evil players a mean P(evil) 0.19 higher than good players.
  Sol 6.1's gap is 0.16 and the other good models average 0.06 (games against Astra-evil excluded).
  The sharpest single-seat edge is shared by the two OpenAI Sol/Astra models. Astra's further edge is
  in group decisions.
- Against the same evil model, Astra good beats the field: vs Opus 5.5 9/9 (others 64%), vs Sol 6.1
  4/4 (others 45%), vs GPT-5.6 Sol 5/5 (others 63%), vs Fable 5.1 2/2 (others 60%).

## Mechanisms, with examples

**1. Ask for the claim before giving the info.** Day-1 good whispers that ask "give me your claim
before I share" make up 6.3% of Astra's, against 0.6–2.6% for most models (Sol 6.1 4.2%, Opus 4.7
4.5%). Townsfolk then report the order publicly. This defeats evil's standard trick of claiming
whatever role the info role just revealed.
- "I have first-night information involving you. Would you give me your role claim before I share
  the details?" (`v17/f3b-astra-v-opus55/game-02`, D1 whisper)
- "I told Alex my role before he gave me his Washerwoman claim, so his matching result does not
  independently confirm him." (Blair/Chef, `v17/f3-astra-v-opus55/game-02`, D1). Alex was the Imp
  and was executed that day.
- In public talk, Astra good seats mention claim timing or independence about twice as often as
  most models (timing 9% of public lines, "independent" 7%, "doesn't prove/confirm" 5%; field
  1–6%, 0–6% and 1–2%).

**2. Refuse the free "confirmation" an evil bluff gets.** Same deal, opposite outcomes
(`v17/f3-fable51-v-astra`):
- With Astra good (`game-01-swap`), the Investigator pair was Casey (Undertaker) or Alex (Poisoner,
  claiming Mayor and backed by a matching Washerwoman). The table took the Washerwoman match apart:
  "an evil player could have Mayor as a bluff, so matching Gray's poisoned information wouldn't
  require a lucky guess" (Harper, D1). It also chased a slip: "Alex, who specifically told you
  Casey's role? 'Claims were bouncing around' isn't a source" (Indigo, D1). It executed Alex, the
  Poisoner, then the Imp on D2.
- With Fable 5.1 good (`game-01`, Astra's evil, the identical pair), the table bought "two
  coincidences" and executed the real Undertaker 10–1. It lost on D5.
- A general rule shows up across games: between two suspects, execute the spent claim and keep the
  ongoing information role alive ("a spent claim versus an ongoing role we can test", Blair,
  `f3-astra-v-opus55/game-02` D1).

**3. Correct bad reasoning, then read the person who keeps making it.** Evil's arguments get
checked line by line, and the overpusher becomes the target.
- `v17/f3-astra-v-opus55/game-03` D1: the Imp (Gray, claiming Investigator) argued that Harper was
  "the only name in both pings". Drew replied: "Harper isn't a name in both pings… Calling Harper
  the overlap gives that execution weight it hasn't earned." Alex caught a knowledge slip: "Gray,
  who told you I have information to work overnight?" Gray was executed 9–3 on day 1, and the evil
  self-nomination trade that followed got 3 votes, all evil.
- The same game-02 table rejected a Baron's real confession offered to save the Imp: "Indigo
  doesn't get to choose our execution by admitting to a lie" (Drew). It then caught the Imp
  reversing a promised self-vote (Harper and Kit, D1).

**4. Private talk becomes public evidence.** Astra good seats whisper more than most (2.5 whispers
per public line; Sol 6.1 2.3, most others 1.0–1.6) and quote whispers publicly when someone's
private stance contradicts their public one.
- "Ellis privately accepted Alex as Poisoner, then switched to accusing Frankie…" (Blair,
  nominating the Imp, `f3-fable51-v-astra/game-01-swap` D2).
- "Alex privately moved from Kit-Imp… to Gray-Imp… Alex acknowledged there was no new evidence."
  (Casey, `v16/f2-gpt56sol-v-astra/game-01-swap` D6).

**5. Use test mechanics on purpose.** The Virgin test is an agreed nomination of the Virgin by a
spent info role: it fired 6 times in 26 games, each one confirming two players. Undertaker reads get
planned, and Slayer shots are aimed at claims that would be dangerous to execute. "Blair's Saint
claim is risky to test by execution… I'm taking my shot at Blair" hit the Imp
(`f2-fable5-v-astra/game-01-swap` D1).

**6. Final three: count the votes and judge which worlds evil's behaviour can explain.** In the
deciding games the whole table works the problem, including the dead with their ghost votes.
- `v16/f2-astra-v-sol61/game-01` D5 (Casey the Imp, Gray the Spy, Drew good). The good side counted
  the votes: "If Drew, Frankie, Blair and I vote Casey, a Drew counter can reach only four… That
  forces a loss rather than changing the execution" (Jules, dead Mayor). They then ignored the Imp's
  last-second Mayor claim and the Spy's last-second Slayer claim: "Both claimed sources behind the
  alternative executions have collapsed together." Good won. On the same seed with Sol 6.1 good
  (`game-01-swap`), the town talked itself into executing the real Mayor at three and lost.
- `f2-gpt56sol-v-astra/game-01-swap` D6: the Imp and two dead Minions offered three "clean" worlds
  that pointed at Kit (Mayor). Good seats priced each one: "they still need either a deliberate
  Minion night-kill or prolonged campaigning against their own Imp" (Drew). The vote was 9 yes on
  the Imp, all of them good.

## One seat or the whole team?

The whole team.
- The nominators of executed evil players are spread across roles. Mayor 5, Monk 4, Drunk 4,
  Soldier 3, Investigator 2, Ravenkeeper 2 and others. Info roles don't do the work alone.
- On evil nominees, almost every living good seat plus the ghosts votes yes (6.6 good yes votes per
  executed evil).
- Corrections come from Outsiders and blank roles as often as from info roles (Drew the Recluse,
  Frankie the Saint, Blair the Soldier in the examples above).
- The weak spots are individual seats briefly swayed by a clever world (Indigo in `f2-astra-v-sol61`
  D5), and the table pulls them back.

## Luck and confounds (honest accounting)

- **The Slayer decided 6 of 26 wins** (3 on day 1). Astra's Slayers hit the Demon on 6 of 10 shots;
  other models hit on 0–40%. The shots were reasoned (an Empath 1 neighbour, a Saint claim too risky
  to execute, a voting bloc), but each was still roughly a 1-in-2 or 1-in-3 guess. On the same deals
  Fable 5 and Opus 4.7 never fired, and Sol 6.1 fired at the wrong player.
- **Good fortune from bad info.** In `f3-astra-v-opus55/game-02`, a poisoned Investigator's false
  Baron pair happened to name the Imp.
- **Weaker opposition.** Astra-good never faces Astra-evil, which beats the field's good teams 62%
  of the time (they win 38% against it). The swap comparisons therefore mix "Astra detects better"
  with "Astra deceives better". Opus 5.5 as evil also made its own mistakes (a Baron confession, an
  Imp who overpushed). Against the field excluding Astra-evil, good teams still win only 64%.
- **Small samples.** Only 1–2 games against most older models. The 26/26 record is mostly 9 games
  against Opus 5.5, 5 against GPT-5.6 Sol and 4 against Sol 6.1.
- Bottom line: luck and opposition explain some single wins (perhaps 6–8 of the 26). The underlying
  rates (76% of executions on evil, 12% yes votes on good nominees, 0.6 good players executed per
  game) are well clear of every other model. Those rates are skill.
