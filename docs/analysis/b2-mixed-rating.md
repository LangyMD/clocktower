# b2: does a team play worse when its seats are split across two models?

**Answer:** probably a little, and clearly so on the evil side. A team of half Claude Opus 5.5 and half GPT-5.6 Sol
rated **1522** [1446, 1595], against **1570** for the average of its two members playing alone. The mixing effect is
**−48 Elo** [−133, +29] overall (negative in 85% of bootstrap resamples), **−34** [−149, +66] when playing good, and
**−158** [−330, −14] when playing evil: the one split whose interval excludes zero. Mixed evil teams won 4 of 66 games.

## Design
- 58 side-swapped pairs (116 games, `plans/b2-mixed-rating.json`, ~$1.75k): the mixed team vs GPT-6.1 Sol (18 pairs ×2
  orders), Fable 5.1 (11×2) and GPT-6 Astra (4×2); two matchups per opponent with opposite list order so each model
  gets the odd seat on odd tables half the time. Plus the 16 b1 pilot games (mixed vs Sol 6.1).
- Fit: the 386-game 2026 fit plus these 132 games, with the mixed team as a 12th player (`python -m clocktower.mixed
  --rate`; output `docs/analysis/b2-mixed-rating.json`). Scale centred on the 11 models. Intervals: 500 bootstrap
  resamples of side-swapped pairs, with the members' uncertainty included jointly. The published 11-model ratings are
  unchanged; in this joint fit they shift by a few points (e.g. Astra 1828).
- A container restart stopped 8 games mid-batch; they resumed from their dusk checkpoints and finished.

## Results
| | Mixed team | Members' average | Effect |
|---|---|---|---|
| Combined | 1522 [1446, 1595] | 1570 [1530, 1609] | −48 [−133, +29] |
| Detection (good) | 1542 [1446, 1635] | 1576 [1523, 1642] | −34 [−149, +66] |
| Deception (evil) | 1395 [1234, 1532] | 1553 [1492, 1622] | **−158 [−330, −14]** |

Record by opponent (wins as good / as evil): GPT-6.1 Sol 18/36, 1/36 · Fable 5.1 13/22, 3/22 · Astra 5/8, 0/8.

## In-group behaviour (b1 + b2, 132 games; `docs/analysis/b2-mixed-behaviour.json`)
- Whispers to teammates go to a same-model teammate 2 points more often than chance [1, 3]. With more data the
  pilot's Opus preference is gone (Opus +1 [−1, +3]); Sol 5.6 leans to Sol (+3 [+2, +5]).
- Same-model pairs vote alike 69% of the time vs 64% for cross-model pairs (gap [+2, +8]); partly shared voting style.

## Reading
Evil is where coordination is explicit (team chat, agreed bluffs, planned sacrifices), and that is where the mixed
team loses most. A plausible mechanism: two models with different styles (Sol 5.6 vs Opus 5.5) make a less coherent
cover story. The overall effect is not significant at 90%; detecting −50 reliably needs roughly 3–4× more games.
