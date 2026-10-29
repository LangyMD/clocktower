# f2 realism and model behaviour (109 finished games, 1 side-swapped pair per matchup)

## Verdict
- **The games read like real Trouble Brewing tables, often like good ones.** You see 3-for-3 claim
  trades, blind confirmations ("tell me your role before I show you mine"), Virgin tests, a Spy
  feeding the Grimoire to its team, poisoned Slayer shots set up as bait, Minions sacrificed to save
  the Demon, and final-day vote counting. Most of what isn't realistic comes from the **rules**, not
  the models: (1) dead players talk too much (they write 25% of all public words, and **56% on the
  final day**); (2) every seat whispers on almost every private turn, so swing voters get swarmed
  (3.5 to 4.6 whispers in one beat on average); (3) older models speak on every public turn (99%), so
  town square is a wall of 150-word speeches; (4) nominations are picked at random when several come
  at once, which decided at least one game.
- **There's a clear generational shift.** The newest models (GPT-6 Astra, GPT-6.1 Sol, Opus 5.5,
  Fable 5.1) talk less and more naturally. They skip 15–30% of public turns, use blind-claim
  discipline, and as good their executions hit evil 51–73% of the time. Opus 4.6, GPT-5.4 and
  Opus 4.8 are at 28–36%. Older Claude models are chatty and theatrical, hard-claim early, and
  **Opus 4.7 and 4.8 misread the rules**: they treat "no death on night 1" as a clue (true in 17/20
  and 16/20 of their games; the Imp can't kill on night 1).
- **Evil is where the sides differ most.** Fable 5/5.1, GPT-6 Astra, GPT-6.1 Sol and GPT-5.5 run
  coordinated, adaptive teams: they pick targets ahead of time, rewrite stories mid-day and avoid
  voting as a bloc. Opus 4.6 and GPT-5.4 as evil make basic errors: claims collide, they bluff
  roles that may be in play, and they vote as a visible bloc.
- **Caveat:** one pair per matchup, and each model plays ~10 games per side. Per-model style numbers
  are solid because they cover thousands of messages. Per-model judgements of skill are anecdotal.

## Per-model table (computed over all f2 games; G = as good, E = as evil)

| Model | Words/speech G·E | Speaks in town square (alive, G·E) | Whispers sent (alive / dead, G) | 2-person whisper · reply rate (G) | Day-1 public claim (G) | Good: execs that hit evil · yes on evil / yes on good | Elo det · dec | Character, in one line |
|---|---|---|---|---|---|---|---|---|
| Opus 4.6 | 56 · 48 | 99% · 97% | 92% / 72% | 4% · 68% | 90% | 33% · 66/52 | 1397 · 1286 | Friendly, generic, hard-claims everything day 1; clumsy evil |
| GPT-5.4 (replies only) | 43 · 44 | 99% · 98% | 99% / 98% | 47% · 62% | 53% | 36% · 42/41 | 1365 · 1290 | Terse, jargon ("claim web", 3-for-3); votes barely track alignment |
| Opus 4.7 | 49 · 64 | 99% · 98% | 99% / 95% | 5% · 63% | 56% | 44% · 62/38 | 1397 · 1286 | Rule slip on night 1 deaths; echo cascades; lost a won endgame on vote maths |
| GPT-5.5 | 44 · 45 | 100% · 99% | 100% / 100% | 44% · 78% | 48% | 40% · 42/34 | 1233 · 1494 | Abstract jargon ("bluff-package world"); clever, truthful-number evil |
| Opus 4.8 | **84** · 74 | 98% · 100% | 94% / 87% | 30% · 60% | 85% | **28%** · 54/42 | **1174** · 1317 | Longest, all-caps shouting (26% of speeches), speechy; worst detector |
| Fable 5 | 65 · 57 | 97% · 96% | 84% / 55% | 27% · 75% | 57% | 56% · 58/29 | 1700 · 1603 | Dense reasoning; strong long-game evil (planned Monk credibility, sacrifices) |
| GPT-5.6 Sol | 42 · 43 | 89% · 95% | 100% / 100% | 20% · 82% | 50% | 58% · 60/28 | 1709 · 1488 | Businesslike, 2-for-2s; solid but bland |
| Fable 5.1 | 57 · 55 | 92% · 93% | 89% / 65% | 52% · 77% | 72% | 51% · 49/29 | 1516 · 1619 | Natural ("Hey neighbours"); best-coordinated evil team seen |
| GPT-6 Astra | 39 · 36 | **69% · 68%** | 100% / 99% | 52% · **88%** | 69% | **73%** · **69/18** | **1820** · 1668 | Spare, precise, asks questions; best detector; surgical evil |
| Opus 5.5 | 39 · 40 | 85% · 79% | 89% / 50% | 45% · 73% | 70% | 56% · 62/34 | 1507 · 1696 | Natural and concise; inventive evil (bait shots, false confessions) |
| GPT-6.1 Sol | 37 · 38 | 83% · 62% | 100% / 99% | 49% · 88% | 70% | 64% · 62/25 | 1681 · **1754** | Careful blind-claim protocol; best deceiver (bluffs timed before claims) |

How each column is measured:
- **Day-1 public claim:** the share of good seats that said "I'm the X" in town square on day 1 (a
  regex, so approximate).
- **Reply rate:** the share of whispers answered by the recipient the same day.
- **Execs that hit evil:** the share of executions in that model's good games that landed on an
  evil player.
- **Yes on evil / yes on good:** how often good seats voted yes when the nominee was evil, and when
  the nominee was good.
- Elo figures are from `analyze.txt`.
- Other measures not in the table:
  - Public speeches that are questions: Astra 17%, Opus 4.6 15%, Sol 6.1 14%; GPT-5.4/5.5/5.6 only
    1–2%, almost always flat statements.
  - Hidden-claim roles get executed a lot: the Mayor in **42%** of games where in play (most of any
    good role) and the Soldier in 36%. The Saint only 9%.

## Model behaviour, with quotes

**Opus 4.6 (oldest Claude).**
- As good, its whispers are friendly but empty. `opus46-v-gpt54/game-01`, Blair: "Hey Alex, I'm your
  neighbor. What role did you get? I'm trying to piece things together early." It hard-claims
  powerful roles on the first turn. Drew: "I'm Slayer" in his very first whisper, then publicly with
  "Morning everyone. I'm the Slayer".
- The same game executed its hidden Mayor on day 1 because he wouldn't claim.
- As evil it fumbles (`opus46-v-gpt54/game-01-swap`):
  - The Imp says "I'll probably claim Empath or something safe" (not one of its bluffs) and
    "Let's not whisper each other too much publicly" (whispers are private).
  - Two Minions both claim Washerwoman. Kit: "Sorry, total brain fart - I'm the Librarian, not
    Washerwoman."
  - Gray's made-up Washerwoman ping named two players who could both deny it.

**GPT-5.4 (replies only).**
- As good it uses real table vocabulary: "Want a 3-for-3? Mine is Mayor / Soldier / Ravenkeeper"
  and "start building a claim web". But it executed its own Fortune Teller on day 1, its Slayer on
  day 2 and its Recluse on day 3, and won only through the Mayor at final three (game-01-swap).
- As evil (`opus46-v-gpt54/game-01`) its three evil seats voted as one bloc ("Gray, Jules, and Kit
  all voted YES on Drew") and got caught. The Imp also whispered the Slayer to nominate the Virgin;
  that was exposed and the Slayer shot him on day 3.

**Opus 4.7.**
- **Systematic rule slip.** `opus47-v-gpt55/game-01`, Kit: "Weird morning - no deaths. Either
  someone was protected or the Imp made a strange choice." Nearly every good seat repeats it, then
  everyone apologises in an echo: "Fair, I ate the Monk-N1 goof too". It happens in 17 of 20 games.
- In that game good worked out the Imp (Indigo) at final four, then lost on the vote: the town
  thought it couldn't beat Logan's 3 votes and voted no, when a 3–3 tie would have cancelled the
  execution and bought another day. Jules: "Vote no. We can't get 4, so Logan stays on block."

**GPT-5.5.**
- As evil it's subtle (same game):
  - The Imp claims Chef with the true number ("Chef 1") because his Minion sits next to him.
  - A Minion corrects the night-1 rule in public to earn trust: "Rules sanity: I think no death is
    just normal N1".
  - In the endgame the Scarlet Woman offers himself as the "SW-catch" new Demon to save the real Imp.
- As good it hides behind jargon and vague claims: "my role is in the 'controlled confirmation'
  bucket", "the passive bluff-package world" (`gpt55-v-fable51`). It executed its own Mayor on day 2.

**Opus 4.8.**
- Theatrical, in capitals, and long. `opus48-v-fable51/game-01`, final day: "JULES - STOP and look at
  what just happened", "Vote YES. Lamps on." Eight dead seats argued two incompatible worlds at the
  last remaining voter.
- Good executed the Soldier, Butler, Washerwoman and Slayer, then the Poisoner at final three, which
  handed evil the win.

**Fable 5.**
- As evil it plans for the long game (`opus46-v-fable5`):
  - The Baron, claiming Monk: "consider skipping a kill target I claim to guard once, so my Monk
    story gets free credibility".
  - At final four the Imp tells his Minion to take the execution: "Casey: eat the lynch".
- As good it writes dense, evidence-led reasoning (`fable5-v-astra`, Casey: "I'll be upfront: I'm
  the Empath. Night one I got a 1"), but lost that game to a Spy-run frame.

**GPT-5.6 Sol.**
- Efficient and flat: "Want to swap a 2-for-2? I'm Ravenkeeper or Undertaker."
- On the same seed it beat Opus 5.5 from both sides: as good in 3 days, as evil in 5
  (`gpt56sol-v-opus55`).
- As evil it's well organised but formulaic, e.g. Gray: "I'll claim Investigator: Scarlet Woman
  between Casey and Harper. That gives us two good pressure targets".

**Fable 5.1.**
- The most adaptive evil team seen (`opus48-v-fable51`):
  - The Spy and Poisoner rewrite the fake Undertaker reading three times in one day as the vote count
    shifts. Jules: "Change it: read Ellis as POISONER, not Spy. Spy doesn't fix the problem - Frankie(6)
    sits next to Gray(7)", then "Scrap Frankie, we don't have the votes ... reads Ellis as BARON".
  - They patch a misquote: "Updated line, match it exactly".
- As good it's natural and neighbourly ("Hey neighbours. Quiet night. I'm not going to spill my role
  to the whole town yet").

**GPT-6 Astra.**
- As good it's precise and insists on blind confirmation. `astra-v-opus55`, Kit: "Could you lock in
  the Minion and pair first? I'd like to compare independent information without feeding you names."
  It arranges a Virgin test on day 1 (6 of 7 Virgin games, the most of any model) and solved that
  game on day 2.
- As evil it's surgical (`fable5-v-astra`). Day-1 plan: "Drew execution, Casey poison, Ellis night
  kill"; it sticks to it, and avoids looking like a bloc: "keep Undertaker quiet initially so our
  claims don't look packaged together", "we shouldn't all lead the same accusation". The Imp claims
  Saint and invites the poisoned Slayer's shot.

**Opus 5.5.**
- As good it's concise, careful and fair. `opus55-v-sol61/game-01`, Ellis: "I'm the Investigator and
  I have a Minion ping on two specific players, not you. Holding the names for now."
- In the same game it executed the Soldier on day 1 and, at final four, refused a tie that would have
  saved the game: "Holding. I believe Kit is the Imp".
- As evil it's inventive but leaky:
  - The Imp baits a poisoned Slayer: "Casey, if you think I'm the Imp, shoot me now". But the team
    had collected the Slayer's three-for-three in whispers, and the town traced the poisoning back.
  - In `astra-v-opus55` the Baron falsely confessed "I'm the Imp" to save the real Imp, and it didn't
    work.

**GPT-6.1 Sol.**
- As good it runs the cleanest protocol of any model. Frankie: "Would you give me a private role
  claim before I share my information? I'd like to compare without steering your answer." Also
  "Locking my full N1 info".
- As evil it times its bluffs well. `opus55-v-sol61/game-01`, the Scarlet Woman (claiming Librarian)
  fishes for the Saint before naming the Outsider: "I'd like an independent exact claim before
  revealing the Outsider type, rather than giving someone the answer to match." Opus 5.5's town took
  that as proof ("that's hard for a Minion to fake") and executed its own Soldier.

## Old vs new
- **Talk.**
  - Old (Opus 4.6/4.7/4.8, GPT-5.4/5.5) speak on every turn, at length, often repeating each other
    (the "I ate the goof too" cascades, the "Morning everyone" openers). Opus 4.8 shouts.
  - New models skip turns, ask questions (Astra and Sol 6.1 at 14–17% vs 1–2% for GPT-5.x) and keep
    to about 38 words.
- **Private time.**
  - Opus 4.6/4.7 almost never whisper two people at once (4–5%), with a reply rate of about 65%.
  - The new models use 2-person whispers about half the time and get replies 73–88% of the time:
    real back-and-forth.
  - Fable and Opus 5.5 also let their dead seats go quiet (they whisper on 50–65% of their dead
    turns, vs about 99% for GPT models).
- **Claims.**
  - Old Claude hard-claims everything on day 1 (85–90%).
  - Old GPT hides behind soft "3-for-3" claims (about 50%), and its hidden Mayors get executed.
  - New models claim selectively and use blind confirmation.
- **Detection.** The share of executions that hit evil rises from about 33% (Opus 4.6, GPT-5.4,
  Opus 4.8) to 56–73% (Fable 5, Opus 5.5, Sol 6.1, Astra). Astra's yes votes separate evil from good
  nominees by 69% to 18%; GPT-5.4's by 42% to 41%.
- **Deception.** Old evil teams collide on claims and vote as a bloc. New evil teams fix the plan on
  day 1, spread their votes, and sacrifice Minions at final four.

## Unrealistic things that come from the rules, not the models
1. **Too many dead voices.**
   - Every dead seat gets a turn in every beat. Dead seats write 25% of public words overall and 56%
     on the final day.
   - Endgames become a "ghost chorus" telling the last living voter what to do ("Drew nominates
     Indigo first - Jules yes, Alex ghost yes, done"), as in `opus47-v-gpt55` D6 and `opus48-v-fable51`
     D5.
   - Real ghosts talk, but much less than this. Options: dead seats get 1 public turn per day, or a
     word cap.
2. **Whisper saturation and swarms.**
   - Living seats whisper on 84–100% of private turns, so day 1 has about 60 whispers.
   - On the final day 5 or 6 seats whisper the same swing voter in one beat. Real players can't hold
     six conversations at once.
   - This also gives every model a pull towards over-claiming in private.
3. **Every seat speaks every public beat (for older models).** Three rounds of 11 speeches of up to
   150 words is a debate format, not crosstalk. The newer models fix this themselves by passing; the
   rules don't force it either way.
4. **Random nomination order.** In `opus47-v-gpt55` D6, three good players nominated the Imp, but the
   evil nomination (Logan) was drawn first, and that settled the game. At a real table whoever speaks
   first is usually taken, and the Storyteller would let a team-agreed nomination happen.
5. **Day-1 shape is formulaic, but that is the real metagame.**
   - The pattern: neighbours first ("Hey neighbour"), soft or 3-for-3 claims, info roles go public in
     town square, a Virgin test if a Virgin claims.
   - Day-1 executions happen in 60–100% of games depending on the good model.
   - This matches experienced public games; not a defect.
6. **The final three all-evil "ritual"** (evil executes its own Minion to reach two alive,
   `fable5-v-astra` D5) is rules-correct and fine.
7. **Possible style tell (no evidence it's used).**
   - One model per side means that in cross-model games the two teams can write differently:
     - Opus 4.8 good averages 84 words with all-caps, against about 43 words from a GPT evil team.
     - GPT-5.x hardly ever asks questions.
   - Typography is normalised, but capitals and length are not.
   - I searched thinking and found no seat reasoning from writing style, but it's a latent
     confound for cross-lab matchups.

## Characteristic mistakes and tells (summary)
- Opus 4.7 and 4.8: "no death night 1 = protect/Soldier" (17/20 and 16/20 games); Opus 4.6 5/20.
  Opus 5.5 and all GPT-x: 0.
- Hidden or passive claims executed: the Mayor in 42% of games where in play, the Soldier in 36%. It
  happens most to models whose Mayors stay coy (GPT-5.x, Opus 4.6/4.7).
- Endgame vote maths: good models (Opus 4.7, Opus 5.5) miss that a tie means no execution and buys a
  day.
- Old evil: bloc voting (GPT-5.4), colliding claims (Opus 4.6), bluffing roles that may be in play
  (Opus 4.6).
- New evil: over-ambitious stories get traced back through the whisper record (Opus 5.5's Slayer
  bait).

## Games read (render scripts and outputs in `f2read/rz/`)
I read these closely (all public speech on every day, every whisper on day 1, and the evil team's
whispers on later days):
- `opus55-v-sol61` game-01 and game-01-swap
- `opus46-v-gpt54` game-01 and game-01-swap
- `opus47-v-gpt55/game-01`
- `opus48-v-fable51/game-01`
- `fable5-v-astra/game-01`
- `astra-v-opus55/game-01`

I skimmed these for claims, nominations and evil whispers:
- `gpt56sol-v-opus55` game-01 and game-01-swap
- `opus46-v-fable5/game-01`
- `fable51-v-astra/game-01`
- `gpt55-v-fable51/game-01`

Statistics cover all 109 finished games.
