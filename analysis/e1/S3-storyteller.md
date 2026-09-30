# S3: the scripted Storyteller, judged as an expert human would run Trouble Brewing (v9 e1, v10 code)

Data:
- The e1 games. When I read them, 52 of 60 had finished (evil won 15, 29%) and 8 were still running. The unfinished
  games are the long ones, so the final evil rate will probably be a bit higher.
- Every information event reconstructed from `events.jsonl` (304 results) and checked against what a sober
  player could have been told.
- Day-1 evil claims from the probes (180 evil seats).
- A Storyteller-level Monte Carlo: 4,000 setups dealt exactly as the engine deals them (10–12 players, Minion by
  seed), with night-1 information drawn by the engine's own `Choice` styles.
- 300 `sim` games under v10.

Scripts: `scratchpad/s3/{e1info.py, claims.py, stsim.py, stsim2.py, stats.py}`. Tests pass (53/53). I did not edit
any repository file.

## Bottom line

1. The policy is close to how a good human Storyteller runs Trouble Brewing. Registration, bluffs, the red herring,
   the Mayor bounce and the Drunk's apparent role are all weighted sensibly, and the results the engine hands out
   look like real results.
2. The one judgment call that is clearly weaker than human practice is poison. The Poisoner hit an information
   role in 40 of 66 e1 poisonings, but only **11 of 28 poisoned results were actually false (39%)**. The cause is
   the v7 "one false world" design: it often agrees with the truth where the ability looks (an Empath with no evil
   neighbours, a Fortune Teller "NO", a Chef's "0"). A human Storyteller makes poisoned information false about 80–90%
   of the time, because that is what the Poisoner is for.
3. Storyteller policy is not what makes good win about 71%. Early information that points at the Demon made no
   difference to the result (good won 10 of 14 such games against 27 of 38 without). No character's presence
   moved evil's win rate beyond noise. Every clean lever I can find adds perhaps **3–6 points for evil in total**.
   That is worth doing for realism, but it cannot bring strong-player games to 50/50. The claim meta and good's
   hive-like consistency (R5) dominate.

## 1. Every POLICY weight and judgment call

Verdicts: "good" = what an expert would do; "ok" = defensible; "change" = recommended below.

| Decision | Ours | Expert human practice | Verdict |
|---|---|---|---|
| Setup | Uniform legal setup; one Minion fixed by seed, the other random, so each Minion is in 50% of games (and so are the Baron, Drunk, Saint and Recluse). A 12-player Baron game always has all four Outsiders. | Picks setups by hand for variety and balance, often avoiding piles of strong information roles. | ok. Uniform is the only clean, uncontroversial rule. e1 shows no significant setup effect (below). |
| `drunk_info_weight` 3 | The Drunk believes they are an information role 82% of the time (MC). | The Drunk is usually an information role. | good |
| `drunk_truthful` 0.2 per game | 67 Drunk results in e1: 43 false (64%), 24 true. | Mostly false; some Storytellers give true information on night 1, then false. | ok |
| `poisoned_false` 0.8 per night | Effective false rate 39% in e1 (11/28). MC with a Poisoner who targets information roles: Chef 33%, Empath 44%, Fortune Teller 23%, Washerwoman 69%, Librarian 73%, Investigator 79%. | Poisoned information is false almost always; that is the point of poisoning. | **change (R1)** |
| False world | A framed good player is the Demon, as many random non-Demon players as the game has Minions are the Minions, the real Demon looks good; fixed per player. | A consistent story is exactly right for the Drunk, who gets information every night. Human Storytellers don't keep a false world for a one-night poisoning. | good for the Drunk; see R1 for poison |
| `false_vouch_evil` 0.7 | A misinformed Washerwoman's pair usually includes an evil player shown as a Townsfolk. | A classic vouch for evil. | good |
| Misinformed Librarian | Shows an evil or framed player as an Outsider; never "zero". | At 9 players "never zero" was right, since zero is impossible there. At a 10-player table with no Outsiders it is not (§4). | **change (R4)** |
| `spy_evil` 0.1, `as_bluff` 0.7, `as_in_play` 0.1 | The Spy usually registers good, and as a Demon bluff. | Standard; the Spy can then claim what it was shown as. In e1 the Spy claimed exactly the character it was shown as in 12 of 20 Washerwoman/Librarian pings. | good |
| `misregister_pair` 0.5 | The Washerwoman, Librarian or Investigator is shown the Spy or Recluse half the time. | Common. | good |
| `recluse_evil` 0.5, `recluse_as_imp` 0.3 | | Scary enough to matter. The Recluse was executed in 11 of 32 Recluse games. | good |
| `recluse_slain` 0.2, `spy_virgin` 0.2 | | Rare, as humans do. | good |
| Red herring | `herring_townsfolk` 0.85: a Townsfolk other than the Fortune Teller; else any good player (Outsider 1.8%, the Fortune Teller itself 0.7%). | Usually a Townsfolk. | good |
| `pair_partner_good` 0.9 | The Investigator's second player is usually good. | Usually a believable good player. | good. A pinged Minion was executed by day 2 in 12 of 18 e1 pings (other Minions 2 of 28). The town just executes both players; that is play, not policy. |
| Demon bluffs | Always includes an information role (99.9%); includes an Outsider in Baron games; the Drunk's role 5%; the Drunk 5%. | Give a safe information bluff; an Outsider in Baron games is common advice. Experts also avoid bluffs that break the Outsider count. | **change (R3)**: a Baron game without the Drunk makes the Outsider bluff a trap (§2d). |
| `mayor_bounce` 0.5, `bounce_evil` 0.05 | | Bounce often, onto a good player. | good. Irrelevant in practice: 1 bounce decision in 52 games. |
| Starpass heir | A uniformly random living Minion when no Scarlet Woman can take over. | A deliberate pick, often the Minion whose ability is spent (the Baron). | ok. Only 1 Storyteller starpass decision in e1; a "Baron first" rule is clean but worth ~0. |
| Spy's Grimoire | Characters, the Drunk, poison, Monk protection, red herring, Butler's master, bluffs. No Washerwoman/Librarian/Investigator reminders (dropped in v7 together with the verbatim information). | The real Grimoire carries those reminder tokens, so the Spy sees who each pair ability was shown. | **change (R2)** |
| Poisoner and Drunk themselves | No extra information; the Drunk's ability silently fails. | Rules-correct. | good |

Two doc nits:
- The POLICY comment says registration is weighted "as a Storyteller balancing a 9-player game would". Tables are
  now 10–12.
- R4's issue #4 (the Baron shown at a table with no Baron) is not in the v10 list and is still in the code. See §4.

**A Storyteller who keeps games close.** Our Storyteller is blind to the game state. A clean state-blind rule can
still help evil on average: more effective poison, better bluffs, and a Spy who sees the reminders all shift the
mean. What it cannot do is cut down blowouts. A rule that reads the game (for example "more misinformation once
evil has lost a Minion") could be stated in one line, but I recommend against it for an eval: it couples the
Storyteller to the good team's skill. A stronger good team would face more misinformation, which compresses the
detection-Elo gaps the eval is trying to measure. Keep the policy state-blind.

## 2. What the e1 games and the simulations show

**(a) How often impaired players get false information.**
- In e1, 95 of 304 results went to impaired players; 54 of those were false.
  - Drunk: 43 of 67 false.
  - Poisoned: 11 of 28 false.
- In the MC, the misinformation branch fires about 80% of the time, as the weights intend. The false world then
  often agrees with reality. For the Fortune Teller the misinformed answer is YES only if the framed player or the
  red herring is among the targets, so most checks answer "NO" in both worlds.
- Sober results were always legal: 0 of 209 sober results were impossible.

**(b) How often false information misleads the town.**
- False *clears* work. Evil players cleared by a false result (a Drunk or poisoned Empath under-counting, a
  Fortune Teller "NO" on the Demon, a Washerwoman or Librarian vouch) had a town-average P(evil) of **0.32**, against
  **0.45** for the other evil players at the same probes (368 against 928 probe readings).
- False *frames* barely register: framed good players 0.23 against 0.21 (n=80).
- Example: `e1-sonnet55-v-gpt6sol/game-01`. The Drunk Empath Drew read 0 on four nights while sitting next to the Imp
  Casey. Casey's town P(Demon) stayed at 1–9% through day 3; the town found Casey on day 4, and good won.
- Games with at least one false result: evil won 7 of 22 (32%); games without: 8 of 30 (27%). The difference is in
  the right direction but is noise at this n.
- Misinformation also costs good executions. The Drunk was executed in 14 of 34 Drunk games.

**(c) Which information roles decide games.**
- Investigator: the Minion-finder. A pinged Minion was executed by day 2 in 12 of 18 pings, against 2 of 28
  unpinged Minions. Yet evil won 30% of the games with an Investigator and 28% of those without, because losing a
  Minion rarely decides the game.
- Fortune Teller: 15 of 36 sober results were Demon hits (7 of 20 on night 1). Only 5 of the 15 hits led to the Imp's
  execution within two days.
- Presence effects (evil win rate with the role in play / absent) are all within noise (n=52):
  - Fortune Teller 22% / 34%; Empath 23% / 35%; Washerwoman 24% / 31%.
  - Drunk 32% / 22%; Baron 32% / 22%.
  - By Minion, evil's win rate is 26–32% for all four.
- Early Demon-implicating information (a Fortune Teller hit, an Empath next to the Imp, the Imp in an
  Investigator or Washerwoman pair, nights 1–2) made no difference: good won 10 of 14 such games against 27 of 38.
- Games are decided by the collective claim-and-count process more than by any one role.

**(d) Are evil's bluffs good?**
- 142 of 180 evil day-1 claims were Demon bluffs. Execution by day 2:
  - bluff claims 24%;
  - other characters not in play 20%;
  - double claims of an in-play role 56% (n=9).
  - An Imp claiming an information role: 16%, the safest claim.
- Outsider claims were executed by day 2 34% of the time, against 23% for Townsfolk claims.
- Where the trap comes from: the town can legally see base, base−1 (a hidden Drunk), base+1 or base+2 Outsider
  claims. An evil Outsider claim is illegal only in a **Baron game without the Drunk** (base+3), which is exactly
  when the policy is most eager to give an Outsider bluff.
  - MC: 9.2% of games are "Baron, no Drunk, Outsider bluff". All of them are 10-player tables; at 11–12 players with
    a Baron there is no non-Drunk Outsider left to bluff.
  - e1: evil Outsider claims in that situation were executed by day 2 in 3 of 4 cases.
  - With the Drunk in play, the Outsider bluff fills the hidden seat and is the safest claim going (25% by day 2).
- Other bluff risks are ordinary play: the Virgin is testable (3 evil Virgin claims in e1), and a fake Slayer has to
  "shoot".
- The Spy as a bluff works: the Spy picked up the character it was shown as in most e1 cases.

## 3. Clean levers toward 50/50, with effect estimates

Ranked by expected evil gain and realism. None changes a rule.

- **R1. Poison makes information false (+1–3 points).**
  - Rule, one line: "a poisoned player's result comes from a false world redrawn until tonight's result differs
    from the truth (if one can)". Keep `poisoned_false` 0.8, and keep the per-game false world for the Drunk (it
    matters that the Drunk's story holds night to night).
  - MC effect on the poisoned false rate: Chef 33→80%, Empath 44→77%, Investigator 79→85%, Librarian 73→81%,
    Fortune Teller 23→56% (it stays lower because a red herring among the targets forces YES in both worlds).
  - In e1 terms, about 11 more false results per 60 games.
  - Cost, the new tells: impaired results skew away from the common truth. A Chef "2" comes up 24% of the time
    against 8% sober; an Empath "2" 15–20% against 6%; a Fortune Teller YES 65% against 39%. That is a likelihood
    ratio of about 2–3 on rare results. A human Storyteller produces the same skew, and the chance of any one
    result being poisoned is low, so I judge this realistic. If it is judged too revealing, redraw once instead of
    until different.
- **R2. The Spy sees the pair-ability reminders (+0.5–1.5 points).** Rule: "the Spy's Grimoire shows which two
  players the Washerwoman, Librarian and Investigator were shown". This is the official Grimoire. It lets the Spy
  know that it was pinged, and that its partner was.
- **R3. Outsider bluffs follow the count (+0.3–1 point).** Rule: "one bluff is an Outsider when the Drunk is in
  play; none in a Baron game without the Drunk". This removes the 9% trap and gives evil the hidden-seat claim in
  Drunk games. (Changing only the Baron clause is enough to remove the trap.)
- **R4. A misinformed Librarian at a table with no Outsiders learns "zero" (tiny, but it removes a detector).**
  Details in §4.
- **R5. Starpass: prefer the Baron (≈0).** Rule: "prefer the Baron (whose ability is spent), else random". Realism
  only.

Together R1–R5 plausibly move evil from about 29% to about 33–35%. Bigger moves would cost realism or the design:
- Weighted setups: Drunk- and Baron-heavy, fewer Demon-finders. Each shows about 10 points in e1, but none is
  significant, and "a uniformly random setup" is the one uncontroversial rule.
- Higher `drunk_truthful` or `herring` tweaks: effects are tiny.
- A Storyteller that adapts to the game state: it compresses the ratings (§1).
- Removing sober information. That is not Trouble Brewing.

For ratings you don't need 50/50: the Bradley–Terry fit carries a side-advantage term. Choose anchor matchups where
evil is the stronger team rather than distorting the Storyteller.

## 4. Checking the v10 fixes

All three are correct. Tests pass, and 300 `sim` games at 10–12 players ran with no illegal value.
- **Librarian with no Outsider in play and a Spy**: now the Spy with probability 0.5, otherwise "zero" (MC: 102
  pings in 209). The legal-value set already includes "zero" there. No new tell. The remaining tell is older:
  - At a table with no Outsiders, any Outsider ping contains an evil player. Sober: 102 of 102 (the Spy). Poisoned:
    56 of 68, because a misinformed Librarian always shows an evil or framed player as an Outsider and never says
    "zero".
  - Once the town sees no Outsider claims, the ping is close to an evil detector.
  - R4 fixes the poisoned half; the Spy half is inherent in `misregister_pair`.
- **A Ravenkeeper who picks themselves** learns `p.shown`, which is legal in every branch (ALL when impaired,
  {Ravenkeeper} when sober). A Drunk is no longer exposed. No tell.
- **An executed Spy shown to a sober Undertaker or Ravenkeeper** now goes through `as_good`, so it is never the
  recipient's own character, and is still a Demon bluff 70% of the time. Correct.
- **Still open from R4 (#4)**: the Baron shown at a table with no Baron. `evil_character` and the misinformed
  Undertaker use `r.choice(MINIONS)`, and a sober Investigator's Recluse ping can say "Baron". MC: 1.6% of sober
  Investigator results name the Baron in a non-Baron game. The Outsider count then exposes the Recluse (or the
  impairment).
  - Fix: use the same Baron guard as the misinformed Investigator.
  - Related: a sober Undertaker can be told the executed Recluse "was the Imp" with fewer than 5 alive, which the
    game carrying on contradicts. The same ≥5-alive guard the misinformed path uses would fix it.
