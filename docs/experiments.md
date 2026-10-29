# Questions to explore

Experiments we'd like to see run. Each says what to measure and how, with what the existing games already
suggest. Most can start small: one or two side-swapped pairs per matchup to check the design reads well, then
scale. If you take one on, open an issue so others know, and put the plan in `experiments/`.

## Learning over time

Do models get better at Clocktower with experience?

- **In context:** after each game, a player writes notes (what worked, how it was fooled) that it carries into
  the next game, capped at about 10K tokens and rewritten each round. Measure the rating over successive rounds
  against a fixed opponent that doesn't learn.
- **Fine-tuning:** train on transcripts of won games (or with the win as a reward) and rate the result.
- **The catch:** shared notes on the good team leak alignment (a good player could put a password in them). Clean
  designs are (1) evil-only learners (evil already knows its team), or (2) a league of individual agents with
  private notes, where each agent's alignment is dealt independently of the agent.

## Harder scripts

Trouble Brewing is the beginner script. **Bad Moon Rising** adds characters whose information is unreliable in
ways the player can't see (the Lunatic believes they are the Demon; the Demon knows and plays along), Demons that
kill several players or none, and protection roles. **Sects & Violets** adds madness (players forced to claim
something). Both test whether deduction holds up when more of the information is designed to mislead. This needs
new characters in `characters.py`, Storyteller policy for each, and rules tests like those for Trouble Brewing.

## One smart player

How much does one strong seat lift a weak team? Put one frontier model in a team of weaker ones
(`--seat-model good:MODEL:1`, or a character, e.g. `--seat-model Imp:MODEL`) and measure the uplift for good and
for evil. Which evil role carries the team: the Demon, or a Minion? Does a strong good player get believed?

## Mixed teams, systematically

The b2 batch found a team split between Opus 5.5 and GPT-5.6 Sol plays below its members' average as evil
(−158 Elo [−330, −14]), because evil cover is only as good as its weakest seat. Next: more model pairs (same lab
vs cross-lab, equal vs unequal ratings), several seat splits, and whether the effect holds for good. Pairs of
equal rating and release date across labs are rare; Fable 5.1 + GPT-5.6 Sol is the closest.

## Teammate recognition by writing style

Every seat's text is normalised to one typography, and no player in 372 games inferred a teammate from "writes
like me". But simple features of day-1 text separate the teams (AUC 0.81; see
[`findings/round-robin-2026/style-lies-probes.md`](findings/round-robin-2026/style-lies-probes.md)). If models learn to
fingerprint, single-model teams become a validity problem. Test it directly: tell players that each team is one
model and see whether detection jumps; or train a classifier on whispers and measure what a player could gain.

## Humans vs AIs

`python -m clocktower play` seats people and models at one table with identical information and moves. A human
baseline: experienced Clocktower players on one team against a model team, and humans mixed into model tables.
Does a model rate differently against people? Do people spot models better than models do?

## Memory ablation

Some older models can only see their own replies, not their earlier reasoning, which may handicap them. Run strong
models both ways (reasoning carried vs replies only; `clocktower/memory_check.py` shows how to strip reasoning from a conversation) and
measure the rating cost of losing memory. That tells us how much of the old-vs-new gap is memory.

## Forced reasoning on votes

Claude models skip thinking on about three quarters of good-side vote turns (GPT-5.6 Sol on 5%), and Claude
towns execute two or more good players in 61% of games. Does forcing a minimum of reasoning on vote turns close
the gap with OpenAI towns? A small matched-seed batch would answer it.

## Monitoring

Can a third model, reading a game as it happens, spot the evil team earlier than the good players do? Feed a
monitor the public record (or the public record plus one seat's private view, or everything including evil's
reasoning) and score its P(Demon) by day against the town's belief probes. With evil's reasoning visible this is a
test of chain-of-thought monitoring for deception; without it, of lie detection from behaviour.

## Also open

- **The timeline:** rate models back to GPT-4o (May 2024) so the trend spans two years
  (`experiments/timeline-models.json`; the 2026 games count, only older models and cross-era pairs need games).
- **Ranking the top tier:** more pairs among GPT-6 Astra, GPT-6.1 Sol, Fable 5.1, GPT-5.6 Sol and Opus 5.5, and enough
  games per side to split detection from deception reliably (about 40+ per side per model).
- **Robustness:** paraphrased prompts, different Storyteller weights, and same-seed replays to measure run-to-run
  noise.
- **Behaviour from existing logs (no spend):** lie detection rates, whisper networks, herding in votes.
