# Diversity: old 3 beats x 2 whispers vs 1 whisper at 4 / 6 / 8 beats

Reader: DIVERSITY. I only read files: no API calls, no games run, no repo edits. Scripts are in `scratchpad/proto/div/`: `load.py`, `feat.py`, `report.py`, `pairs.py`, `text.py`, `stock.py` and `summary.py`. Raw outputs are in `report_out.txt` and `pairs_out.txt`.

## Verdict

**The private-time design barely changes how varied the games are. The models and the deal decide that.** Games are already varied where it matters to a viewer: how they end, the order of executions, and which mechanic decides the game. They are formulaic in the same places under every design.

The design leaves two traces:

1. **One whisper per turn makes evil's opening more rigid, not less.** Under the old rule, the Imp briefed both Minions in beat 1 and also opened a conversation with a good player in the same turn (67% of core games, about 2 evil-to-good whispers per game in beat 1). Under one whisper per turn, beat 1 is a pure three-person evil huddle in every game:
   - core W4 + W6: 36 of 36 games had the Imp briefing both Minions, and 0 evil-to-good whispers in beat 1;
   - 97–100% of Minions' beat-1 whispers stayed inside the team (old rule: 35%).

   Only the public whisper log (v15) broke this, which is why the user dropped the log.
2. **More beats make the whisper network denser and broader, but not more varied in shape.** On day 1 at 6 beats, each player talks to 5.4 different people (old rule: 4.3). Clustering rises from 0.44 to 0.63, and the share of whispers that go to seat neighbours falls from 51% to 38%. When I compare the first 40 whisper recipients of each game, so the volume is equal, every design looks the same: about 55% go to neighbours, with about 19–20 distinct pairs. So the change is just more talk, not a different structure.

Some things look more varied at 6 beats than in the old design. There are more endings types per game, fewer games where evil claims exactly the 3 bluffs, and a less stock day 1. Each of these comes from 8–12 games and a confound:
- the W6 deals had a Spy in 10 of 12 games, against about 45% elsewhere;
- W6 had a higher evil win rate.

None of them survives the matchup control with any confidence. **Recommendation:** for diversity, v16 (6 x 1, private) is neither better nor worse than the old design. Choose the design on realism and cost, not on diversity.

## Data and control

- Designs:
  - **OLD** = v9 e1, v12 c2 and v13 f1: 88 games, 75 finished. v7 c1 (40 games) is shown only as context, because it used older rules, same-model teams and some 9-player tables.
  - **W4** = v14 w1 plus x0: 40 games.
  - **W6** = the v14 w1 "-b6" games: 12 games. This is the closest to v16.
  - **C6** and **C8** = v15 c3 at 6 and 8 beats, with the public whisper log: 20 + 20 games.
  - **C6h** = c3h: 10 games.
- **Control:** "core" means the 4 matchups that appear in both OLD and the new designs: Opus 5.5–Sol 6.1, Sonnet 5.5–Sol 6.1, Fable 5.1–Astra and Sonnet 4.5–GPT-5.4. That gives OLD 30, W4 24, W6 12, C6 18 and C8 18 games. The cleanest single control is **Opus 5.5 vs Sol 6.1 alone**: OLD 22, W4 14, W6 8, C6 10, C8 10 games. I quote that control where it matters.
- **Seeds differ between OLD and the w1 games.** Only c3 b6, b8 and c3h share deals. So the deal mix, especially Spy and Virgin frequency, is a confound, and I note it where it bites.
- **How claims were detected:** first-person regexes ("I'm the X", "X here", "Name, X.", "my X info"), with quoted speech stripped first.
  - Spot checks show they still miss some claims.
  - They count a three-for-three offer ("I'm FT, Undertaker or Ravenkeeper") as a claim of its first role.
  - So I hand-checked the good-bluff numbers.

## 1. Evil openings

| core matchups | OLD | W4 | W6 | C6 (log) | C8 (log) |
|---|---|---|---|---|---|
| Imp briefs both Minions in beat 1 | 97% | 100% | 100% | 56% | 83% |
| Imp also whispers a good player in beat 1 | 67% | 0% | 0% | 6% | 0% |
| Minion's beat-1 whispers all go to the team | 35% | 98% | 100% | 97% | 100% |
| Evil's day-1 first claims are exactly the 3 bluffs | 72% | 62% | 42% | 71% | 67% |
| Same seed, both games: identical evil claim split (pairs) | 5/15 | 2/12 | 0/6 | 1/9 | 2/9 |
| Same seed, both games: same Imp claim | 53% | 50% | 67% | 44% | 33% |

- **Who evil whispers first is fixed under every private design: their own team, in beat 1.**
  - The Imp's beat-1 message is a template in all designs: "Bluffs are X, Y, Z. I'll take X." It appears in 89–100% of games.
  - Example from the old rule, `v9/e1-gpt61solmax-v-opus55/game-01-swap`. The Sol Imp Gray sends "Bluffs are Undertaker, Investigator, Chef. I'll take Undertaker..." to the Minions. In the same turn he also tells Harper, a good player: "I'm Undertaker, so nothing to report yet."
  - Under one whisper per turn, the second message has to wait until beat 2. The evil table spends beat 1 closed.
- **Bluff assignment.** The Imp takes a Demon bluff in 93–100% of games under every design (Opus–Sol: 100% in OLD, W4 and W6). The apparent W6 variety, where only 42% of games use exactly the 3 bluffs, comes from the Spy:
  - 10 of the 12 W6 deals had a Spy. Spies use the Grimoire to double-claim a real Outsider. Examples:
    - `w1-opus55-v-sol61-b6/game-02`: the Spy claims Saint in both games of the pair.
    - `game-01`: the Spy claims Butler in both.
    - `w1-fable51-v-astra-b6/game-01`: "Drew's Librarian saw Harper/me as Saint - I'll claim Saint."
  - In non-Spy games, the 3-bluff rate is 81% for OLD and 92% for W4 (core).
  - Verdict: setup-driven, not design-driven.
- **Same-seed repeats.** S4 found that Opus–Sol pairs repeated the whole evil split 5 of 9 times under the old rule. With one whisper it happened 1 of 11 times (W4 + W6) against 5 of 11 (OLD, Opus–Sol). Fisher p = 0.15, so this is suggestive at most.

## 2. Good strategies

| core matchups (share of good seats) | OLD | W4 | W6 | C6 | C8 |
|---|---|---|---|---|---|
| Claimed publicly on day 1 | 0.67 | 0.65 | 0.62 | 0.64 | 0.67 |
| Claimed only in a whisper on day 1 | 0.23 | 0.23 | 0.25 | 0.23 | 0.25 |
| Unclaimed through day 1 | 0.10 | 0.12 | 0.14 | 0.13 | 0.08 |
| First-night info roles (WW, Lib, Inv, Chef) that claimed publicly on day 1 | 0.97 | 0.96 | 0.94 | 0.91 | 0.88 |
| Good seat's first whisper asks without claiming | 0.43 | 0.44 | 0.50 | 0.44 | 0.51 |
| Beat-1 good whispers to seat neighbours | 0.75 | 0.84 | 0.71 | 0.79 | 0.77 |
| Same seed: same good seat lands in the same claim-timing category | 0.66 | 0.60 | 0.62 | 0.57 | 0.61 |

- **Claim timing is the same under every design.** The between-game SD is about 0.2 everywhere.
- **Good almost never bluffs, under any design.** After hand-checking every flagged case in the core games, only two real good bluffs remain:
  - one under the old rule: `v9/e1-gpt61solmax-v-opus55/game-01-swap`, Kit, an Opus Ravenkeeper: "I'm the Undertaker - so if someone goes today, I'll know what they were. Keep it quiet please."
  - one under the new rule: `v15/c3-opus55-v-sol61-b6/game-02-swap`, Harper, a Sol Ravenkeeper: "I'm Undertaker, so nothing from the first night."

  The other flags were three-for-three offers or reported speech.
- **The three-for-three is a ritual of the good model, not of the design.** Sol 6.1 and Astra open with near-identical words:
  - "Want to trade three-for-threes? Mine are Mayor, Soldier, Ravenkeeper." (`w1-opus55-v-sol61-b6/game-01-swap`, Alex)
  - "Want to trade three-for-threes? Mine are Fortune Teller, Undertaker, or Ravenkeeper." (`c3-fable51-v-astra-b8/game-01-swap`, Blair)
  - the old-rule version: "Want to trade broad claims? I'm Fortune Teller / Undertaker / Ravenkeeper." (`c2-opus55-v-gpt61sol-c/game-01-swap`, Gray)

  It appears in 41% of OLD games, 38% of W4, 42% of W6 and 40–50% of C games.
- **W6 shows slightly more holding back**, but on 8–12 games:
  - Opus–Sol: 16% of good seats unclaimed through day 1 (OLD 9%);
  - 90% of first-night info roles claimed publicly on day 1 (W4 100%);
  - e.g. `w1-opus55-v-sol61-b6/game-04`, where the Washerwoman stays hidden on day 1.

  These are consistent with more private time making a private-only claim viable, but they are within noise.

## 3. Who talks to whom

| day 1, all games | OLD | W4 | W6 | C6 | C8 |
|---|---|---|---|---|---|
| Whispers sent | 59 | 40 | 62 | 60 | 81 |
| Distinct partners per player | 4.3 | 3.9 | 5.4 | 5.6 | 6.6 |
| Density of the pair graph | 0.43 | 0.39 | 0.54 | 0.56 | 0.67 |
| Per-sender target entropy (bits) | 1.85 | 1.71 | 2.12 | 2.16 | 2.43 |
| Clustering coefficient | 0.44 | 0.44 | 0.63 | 0.62 | 0.72 |
| In-degree Gini (swarming) | 0.19 | 0.23 | 0.21 | 0.23 | 0.18 |
| Share of recipients who are seat neighbours | 0.51 | 0.51 | 0.38 | 0.40 | 0.36 |
| Same, over the first 40 recipients only | 0.58 | 0.56 | 0.47 | 0.52 | 0.53 |
| Distinct pairs in the first 40 recipients | 18.5 | 18.4 | 20.0 | 19.9 | 19.8 |

(Opus–Sol alone gives the same ordering.)

- **Network breadth follows whisper volume.** W4 has the thinnest network; it is the only design that cut volume. W6 matches OLD's volume and spreads it over more partners, because each turn reaches 1–2 people rather than up to 4.
- **The structure of the network barely changes.** Over the first 40 recipients, the designs differ by 1–2 pairs and a few points of neighbour share.
- **How often the same network repeats:**
  - **Across a side-swapped pair** (same seats, different models), the day-1 pair sets overlap with Jaccard 0.52–0.58 in every design. The random baseline at the same density is 0.25–0.5.
  - So seating and roles fix much of who talks to whom. The excess over random shrinks as beats rise (OLD +0.26, W6 +0.19, C8 +0.07), but that is mostly because a denser graph overlaps more by chance.
  - **Within a game**, the day-to-day Jaccard is 0.50–0.64 and rises with beats. Again, that is density.

## 4. Executions, lengths and endings (finished games)

| | OLD | W4 | W6 | C6 | C8 |
|---|---|---|---|---|---|
| Games (all) | 75 | 40 | 12 | 19 | 20 |
| Distinct execution sequences per 8 games (rarefied; max 8) | 7.5 | 7.4 | 8.0 | 7.5 | 7.8 |
| Most common sequence (share) | gD / gmD (8%) | mmD / mD (10%) | all unique | mD (11%) | mD (10%) |
| Ending-type entropy (bits) | 1.52 | 1.34 | 1.78 | 1.19 | 1.46 |
| Game length, mean (SD), days | 3.8 (1.4) | 3.9 (1.4) | 3.8 (1.6) | 3.5 (1.2) | 3.8 (1.2) |
| Evil win rate | 31% | 35% | 42% | 21% | 20% |

Sequence notation: g = good executed, m = Minion executed, D = Demon executed, - = no execution that day.

- **Execution sequences almost never repeat in any design.**
  - 51 distinct sequences in 75 OLD games, 28 in 40 W4 games, 12 in 12 W6 games.
  - Within a side-swapped pair, the sequence was identical in 0–2 pairs in every design (OLD 0 of 44).
- **Ending types are the same 4–5 in every design:** Demon executed, evil reaching the final two, Slayer shot, Saint executed, and rarely a Mayor win (1 game: C6h).
  - The higher ending entropy at W6 (1.78 bits) comes from 12 games with 5 evil wins and 2 Slayer wins:
    - `w1-fable51-v-astra-b6/game-01-swap` ended with a day-1 Slayer shot.
    - `w1-opus55-v-sol61-b6/game-02` ended with a Saint executed.
  - That is win-rate variance, not new kinds of game.
- **Opus–Sol control:** 5–8 distinct ending-and-day combinations per 8–14 games in every design. The C6 Opus–Sol games were the most uniform (9 of 10 ended with the Demon executed); that is a balance effect of the public log.

## 5. How formulaic is day 1?

**The day-1 script** has four parts:
- the Imp briefs both Minions with all 3 bluffs in beat 1;
- every first-night info role claims publicly;
- the Virgin, if in play, is tested;
- someone is executed.

| share of games running the whole day-1 script | OLD | W4 | W6 | C6 | C8 |
|---|---|---|---|---|---|
| core | 76% | 79% | 58% | 47% | 56% |
| Opus–Sol | 91% | 93% | 62% | 50% | 60% |

- **Opus–Sol day 1 is close to scripted under OLD and W4.**
  - The Virgin is tested on day 1 in 100% of Opus–Sol games that have one, in every design.
  - Town-square beat 1 is a claim dump: 55–62% of first public speeches contain a role claim, in every design.
  - A Spy who reads out the Grimoire to the team on day 1 appears in 83–100% of Spy games.
- **The lower W6 figure (5 of 8 Opus–Sol games) is the clearest hint of a less formulaic day 1 at 6 beats.** It comes from first-night info roles holding back, as in game-01 (Chef private only) and game-04 (Washerwoman hidden).
  - Weight it lightly: 8 games, and the W6 deals had no Virgin in 6 of 8.
- **Day-1 signature** (first nominee's team, Virgin test, execution type, number of nominations): distinct signatures per 8 games are 6.0 for OLD, 5.1 for W4, 5.7 for W6, 4.8 for C6 and 5.7 for C8 (core). OLD has more days with several nominations (SD 0.96 against about 0.5).
- **Wording is not templated at the game level.** Pairwise TF-IDF cosine of day-1 text (names, roles and numbers masked) is 0.01–0.03 in every design. The formula lives in moves, not in sentences, apart from the per-model stock phrases above ("Hey neighbours, I'm the Chef", "three-for-threes", "Bluffs are X, Y, Z. I'll take X").

## What survives the matchup control

- **Real, and robust (100% vs 27–35%, n = 36 and 30 core games):** one whisper per turn turns beat 1 into an invisible, fixed evil huddle, with no evil-to-good contact in beat 1. It is less varied than the old rule. In v16 it is harmless because nobody can see it, but it is the least varied moment of every game.
- **Real, but mechanical:** 6 beats give a broader, more clustered whisper network than the old rule; 4 beats give a narrower one. The change goes away when whisper volume is held equal.
- **Not distinguishable from the old rule:**
  - good claim timing, good bluffing (essentially none), the three-for-three ritual and neighbour-first openings;
  - endings, execution sequences and game length;
  - the Imp taking a Demon bluff.
- **Possible, not established (n = 8–12):**
  - W6 has a less scripted day 1 and fewer same-seed repeats of the evil split;
  - W6 has more varied evil claims, but that is confounded by Spy-heavy deals.

  A run of about 30 v16 games on the old e1/c2 Opus–Sol seeds would settle these.
