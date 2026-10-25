# Why GPT-6 Astra wins (Oct 5 2026 readers, 372 games: v16 f2 + v17 f3/f3b)

Astra: 26/26 as good, 16/26 (62%) as evil (field ~65% good, ~32% evil). Six parallel readers:
`detection.md`, `deception.md`, `metrics.md`, `reasoning.md` (why), `cunning-evil.md`, `good-strategy.md` (best games).

**As good:** not sharper Demon beliefs (town P(Demon) on the real Demon ≈ Sol 6.1's) but better group
decisions: the town's top suspect is evil 92% of the time (Sol 6.1 72%, field 56%), executions hit
evil 76–78% (Sol 6.1 65–68%, field ~51%), good seats vote yes on good nominees 12–15% (field 31%).
Habits: info roles ask for the other player's claim before revealing their own info; claims that fit
together are not taken as confirmation ("a Spy could make that match"); false premises are corrected
at once; private whispers quoted publicly as evidence; whole-table vote counting at final three.
Luck/opposition: Slayer decided 6 wins (6/10 shots hit); it never faces Astra-evil. Maybe 6–8 of 26 wins.

**As evil:** the Demon stays out of view: nominated on 22% of days (others up to 42%), day-2 suspicion
at chance (0.11). Its evil seats speak 0.6× the public words of good seats (Opus/Fable 1.0–1.7×),
follow the town's wrong theories instead of leading them, and teammates take opposite sides.
Lies fit the real night info and the rules (true Chef numbers, Outsider counts, Drunk/Recluse covers).
Its Demon won 8/8 games where it claimed a one-shot day-1 info role, e.g. Chef or Washerwoman (others 27/91). Kills
remove Monks/Slayers and leave misleading good players alive; planned succession (star-pass, SW)
wins 64%; 83% of games reaching ≤4 alive. Losses: day-1 Slayer hits, invented Undertaker/Ravenkeeper
reads, late Saint claims (0/4). The two Sols hold it to 4/9.

**Style:** it thinks *less* (~180 thinking tokens per talk turn, fewest output tokens of any model),
writes short messages (claim, alternative it can't rule out, concrete ask), passes 28–39% of town turns.
Raw reasoning is encrypted (OpenAI); only summaries and probes are readable.

**Best games to watch:** see `cunning-evil.md` (top: `f3-opus47-v-fable51/game-03`,
`f3-gpt54-v-opus55/game-02`, `f3-opus55-v-sol61/game-02`) and `good-strategy.md` (top:
`f3-fable5-v-fable51/game-02-swap`, `f3-gpt56sol-v-opus55/game-02-swap`, `f3b-astra-v-opus55/game-02`).
