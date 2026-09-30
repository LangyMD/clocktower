# R4: engine rules and Storyteller audit (v9 e1)

Scope: README, PROTOCOLS (v7–v9), game.py, state.py, characters.py, prompts.py, render.py and cli.py (table size, Minion
by seed). I read the 10 assigned transcripts closely. I then ran two mechanical checkers over all 60 e1 `events.jsonl`
files (35 finished, 25 in progress) and over 1,500 random-seat sims at 10–12 players (seeds 90000+, run with the
engine's own `build()`, no API calls). Tests pass (51/51). Checker scripts: `scratchpad/check.py`, `scratchpad/check2.py`.

## Bottom line

I found no rule violations: no impossible information went to a sober, unpoisoned player (0 of 203 sober info events
in e1, 0 of about 9,800 in the sims), and every setup, night, vote and win-condition check passed. The problems are
Storyteller judgment calls and cosmetic issues. The most important is that a sober Librarian always names the Spy
when no Outsider is in play.

## Verified correct (e1 plus sims)

- **Setup.** Counts are right for 10, 11 and 12 players (7/0/2, 7/1/2, 7/2/2), with Baron giving −2 Townsfolk and +2
  Outsiders. The table size is 10 + seed%3 and MINIONS[seed%4] is always in play (all 60 e1 games). The Drunk's
  apparent character is always a Townsfolk that is not in play. Bluffs are never characters that are in play. A red
  herring is set if and only if someone believes they are the Fortune Teller (Drunk included), and it is always a good
  player. Minions learn the Demon and each other but not each other's characters. The Imp learns its Minions and 3
  bluffs.
- **Night.** Choosers: nobody dead is woken, and the Monk and Imp do not act on night 1.
  - Poisoner: the poison lasts that night and the next day; it ends when the Poisoner dies or becomes the Imp
    (gpt61sollow-v-opus55/game-01-swap n4).
  - Monk and Soldier: every blocked kill in e1 was a Monk save (8 cases). A poisoned Imp's kill never lands (258 sim
    cases).
  - Mayor bounce: seen once in e1 (opus55max64k/game-01 n3, Casey to Alex); 117 in the sims.
  - Starpass: 9 in e1, each heir checked. The Scarlet Woman takes priority at 5+ alive (e.g.
    sonnet55-v-gpt61sol/game-01 n5, 7 alive). Otherwise the heir is a living Minion.
  - Scarlet Woman on execution or Slayer kill: 36 Imp deaths checked against "alive before ≥ 5, Scarlet Woman alive
    and unpoisoned". 0 mismatches.
  - The Ravenkeeper wakes when killed, including by a bounce.
- **Day.**
  - Nominations: no player nominated or was nominated twice in a day. Only living players nominated.
  - Votes: the threshold is max(ceil(alive/2), top+1), and every block/tie/short outcome matched. Ghost votes are
    spent once and never asked for again. Order runs clockwise with the nominee last. No eligible voter was skipped.
  - Butler: no working Butler's yes was counted without their master's hand up (1,897 sim cases where the master was
    asked early).
  - Virgin: 28 e1 nominations of the Virgin checked. It fired only when working and on the first nomination by a
    Townsfolk; the Drunk never triggered it; the Spy counted as Townsfolk 20% of the time.
  - Slayer: only a working Slayer's first shot counts; the Recluse dies 20% of the time.
  - Saint: an execution loses only if the Saint is unpoisoned.
  - Wins: evil wins at 2 alive. When the Demon dies at 3→2 alive, good wins (sonnet55-v-gpt6sol/game-01-swap). The
    Mayor's 3-alive win never came up.
- **Misinformation.** 95 impaired info events in e1: 54 false, 41 true (20% of Drunks get true information all game,
  plus places where the false world matches the real one). Each one reads as a plausible working result. Over 1,500
  sims, sober and misinformed distributions are close: Empath 0/1/2 = .45/.49/.06 sober against .53/.41/.07 drunk;
  Fortune Teller YES rate .40 against .37–.42; Chef at 12 players .52/.39/.09 against .55/.42/.03. They don't give
  impaired players away. Night-to-night consistency holds: drunk Empaths keep a stable picture as neighbours die
  (gpt61sol-v-astra/game-01 Blair: 2, 1, 1, 0 all fit one false world).

## Issues

### 1. Questionable judgment (the most important one): a sober Librarian always names the Spy in a game with no Outsiders
`state.py:405`: `pool = mis if mis and (not real or r.random() < POLICY['misregister_pair']) else real`. When no
Outsider is in play (in v9 that means a 10-player game without the Baron; the Librarian only acts on night 1) and a
Spy is alive, `real` is empty, so the Spy is shown as an Outsider every time and "zero Outsiders" is never
given.
- Sims: sober Librarian, no Outsiders, Spy in play: **78 of 78 were Spy pairs, 0 were "zero"**. (With Outsiders in
  play the Spy is shown about 50% of the time, as intended.)
- e1: `e1-gpt54-v-fable51/game-01` and `-swap` (10 players, no Baron). Harper was told "either Blair or Indigo is the
  Butler"; Blair is the Spy. In the swap game the Investigator also pinged Blair, and Frankie said publicly: "Harper
  says Librarian seeing Butler on Blair or Indigo, Blair says Butler. That's a neat little package, which is exactly
  what a Spy would build."
- Why it matters: in a 10-player game without a Baron, any Outsider ping means Spy or Baron, and here it is always the
  Spy. The ping becomes a Spy detector that no human Storyteller would hand out.
- Fix: treat "zero Outsiders" as the real answer when `real` is empty. Show the Spy with probability
  `misregister_pair`, else "zero".

### 2. Questionable judgment (rare, reveals the Drunk): a Drunk Ravenkeeper who picks themselves learns "X is the Drunk"
`state.py:489`, `character_choice`, misinformed path: `t is p` is never in the decoy's evil set (the decoy excludes
p), so it returns `t.character`, which is 'Drunk'. The truthful-Drunk path does the same. In a direct test, 300 of 300
self-picks by a Drunk-as-Ravenkeeper returned "Drunk". This did not happen in e1 (5 Ravenkeeper wakes, none were
self-picks). It contradicts the v6 rule "impaired players are never shown their own character".
- Fix: `if t is p: return {'character': p.shown}`. That is what the ability shows in every world.

### 3. Questionable judgment (minor, inconsistent with v7): a sober Undertaker or Ravenkeeper can be shown the Spy as the recipient's own character
`state.py:490–491`, sober path: `g.fake_good(r, (TOWNSFOLK, OUTSIDERS))` has no `avoid=(p.shown,)`. The pair roles
got that guard in v7. In a direct test the executed Spy showed as "Undertaker" to the Undertaker 1.2% of the time.
That result is legal, but it tells the recipient that the player was the Spy (or that they are the Drunk).
- Fix: pass `avoid=(p.shown,)`, as `pair_choice` already does.

### 4. Questionable judgment (minor): the Baron can be shown in a game that has no Baron
v7 says a misinformed Investigator is shown the Baron only in a Baron game (state.py:391). The misinformed Undertaker
or Ravenkeeper still uses `r.choice(MINIONS)` (state.py:484), and so does a Recluse registering as a Minion
(`evil_character`, and the Recluse's Investigator ping). Being shown "Baron" at a 10-player table with 0 Outsiders
visible is a count clue. It never happened in e1.
- Fix: use the same Baron guard in `character_choice` and in `evil_character`.

### 5. Cosmetic (a real code bug): the notice about dropped whispers lowercases player names
`game.py:356`: `'; '.join(dropped).capitalize()`. Python's `capitalize()` lowercases everything after the first
character. It fired 11 times in e1, e.g. `e1-gpt56sol-v-opus55/game-01-swap` d4 and
`e1-sonnet55-v-gpt61sol/game-01` d3 and d5: "(Your whisper to blair, alex, indigo went only to blair and alex …)".
The whisper itself is delivered correctly to the right names.
- Fix: `s[:1].upper() + s[1:]`.

### 6. Cosmetic: the Imp's night prompt says "your Minion" (singular) at 10–12 players
`game.py:38`: "Choosing yourself kills you and makes your Minion the new Imp." Every v9 table has two Minions, and the
Storyteller (or the Scarlet Woman rule) decides which one takes over.
- Fix: "…and one of your Minions becomes the Imp."

### 7. Cosmetic: the transcript prints raw events
`render.py` has no case for `death`, so `transcript.md` shows lines like
`[death] {'player': 'Alex', 'cause': 'demon'}` (e.g. opus55max64k/game-01 n3). This is audit-only, so players never
see it. Separately, when the Virgin fires, players see two lines: "Kit is executed immediately! The day ends." and
then "Kit is executed." (gpt56sol-v-opus55/game-01 d1).

### 8. Cosmetic: small wording artifacts players see
- The Undertaker is told at night "the player executed **today** (X)"; it should say "yesterday" or "at the last
  execution".
- On a self-nomination the defense prompt reads "Jules has nominated you" (gpt61sol-v-astra/game-01 d2). Self-nomination
  is legal.
- The nomination call produced 936 "your nomination … was not taken" notices across e1, up to 8 in one round
  (gpt56sol-v-opus55/game-01-swap d1). This is correct by design but noisy; one line per round would do.

### 9. Questionable (theoretical): asking the Butler's master early leaks information
When the master sits after the Butler, the master is asked at the Butler's seat (by design, v8). The master's prompt
then arrives while the votes between the Butler and the master are still missing, so an attentive master can infer
"the seat right after the last vote is a real Butler, and I am their master". I found no model making that inference
in e1 (I searched the thinking), so I leave it as a note.

## Game-by-game notes (assigned games)

- **fable5-v-opus47 01 / 01-swap** (11 players, Poisoner and Spy). The sober Librarian was shown the Spy as "Drunk".
  That is legal, but it sent the town to a "Baron world" that didn't exist. The Chef's "1" required the Spy's 10%
  evil registration. In the swap game, the poisoned Undertaker got true information (the 20% branch). Evil won by
  executing the Saint through a Poisoner's fake Washerwoman ping. All clean.
- **gpt56sol-v-opus55 01 / 01-swap** (12 players, Baron). The Drunk Empath read 0, 0, then 1 when the neighbour
  became Indigo (the Saint). That coherent false-world pointer fed the day-5 Saint execution and the evil win.
  Legitimate misinformation, and it shows the false world has real teeth. The starpass to the Spy at 4 alive was
  correct. Whisper-notice lowercase bug seen on d4.
- **opus48-v-astra 01-swap** (10 players, Baron). The Investigator was told the truth (Scarlet Woman). The Virgin fired
  on the Investigator; the Drunk Monk's choice was correctly ignored. Clean.
- **opus48-v-gpt56sol 01-swap** (11 players, Baron). The Drunk Undertaker saw a Washerwoman as the Washerwoman
  (true, since an unframed good player is shown as themselves), the Baron as "Chef" (a Demon bluff), and the Scarlet
  Woman as "Spy". All plausible. The Fortune Teller's night-1 YES was the red herring. Clean.
- **gpt55-v-fable51 01-swap** (12 players, Baron). The Drunk Investigator's ping ("Blair or Frankie is the Poisoner",
  where Frankie is the Recluse) was plausible, and it got the Recluse executed. Butler votes were consistent. Clean.
- **sonnet55-v-gpt61sol 01** (11 players, Baron). The Drunk Empath read 0 three times next to the Baron, then 1.
  Starpass to the Scarlet Woman at 7 alive. Evil won at 2 alive. Lowercase whisper notice twice.
- **opus55-v-gpt61sol-b 01** (12 players). A truthful Drunk Fortune Teller (the 20% branch) with the red herring on the
  Monk. The Librarian was shown the Spy as "Recluse" (a Demon bluff). Scarlet Woman starpass at 4 alive. Clean.
- **gpt61sollow-v-opus55 01-swap** (10 players, Baron). The Poisoner inherited the Imp; poison ended correctly. The
  Imp's dead "Ravenkeeper" claim was an evil bluff; the engine did not wake a Ravenkeeper. Clean.

## Suggested fix list (none of these changes the rules; items 1–4 change the Storyteller style, so they need a protocol bump)
1. Librarian with no real Outsiders: "zero" with probability 1 − misregister_pair.
2. A Ravenkeeper choosing themselves is shown `p.shown`.
3. `avoid=(p.shown,)` when a sober Undertaker or Ravenkeeper sees the Spy as a good character.
4. Baron guard in `character_choice` and `evil_character`.
5–8. `capitalize()` bug, Imp prompt wording, render `death`, Undertaker "today" wording (cosmetic; no bump needed
   except for prompt text).
