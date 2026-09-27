# Game logs by protocol version

Each game directory holds `events.jsonl` (every event, with who could see it), `transcript.md`
(omniscient replay with summarized thinking), `conversations/` (each seat's full API conversation),
`calls.jsonl` (per-call usage and cost), `config.json` (settings, including `protocol`),
`result.json` and, from v5 on, `probes.jsonl` (belief probes; see below). The current version is `PROTOCOL` in `clocktower/cli.py`; bump it (and add a section
here) whenever a change affects how games play.

## v1 — development (Sept 25–26, 2026)
Beats where a turn could both speak publicly and whisper; everyone saw who whispered whom (not the
words). LLM Storyteller (Opus 5.5). `batch-001` let the Storyteller choose setups (it chose the same
information-heavy one every game); from `batch-002` setups are uniformly random. Good won 11 of 12.

## v2 — baseline 40 (Sept 26–27)
v1 plus even-handed strategy tips in the player prompt. `opus-20` (Opus 5.5) and `astra-20`
(GPT-6 Astra), same seeds. Good won 40 of 40. Diagnosis: public whisper metadata let good find the
evil pair; everyone claimed truthfully on day 1; the LLM Storyteller undid evil's misinformation
and mode-collapsed (Drunk as Empath 25 of 34 times); the engine announced voided Butler votes.

## v3 — private time, then town square; scripted Storyteller (Sept 27)
Each day: 3 private beats (whispers only, invisible to others, up to 2 per turn), then 3
town-square beats (public only), then nominations. Scripted Storyteller policy (consistent false
picture for impaired players). Butler leak fixed. `phased-10`: good 6, evil 4.

## v4
v3 plus: up to 3 whispers per turn; players named in the town square answer first in the next
beat; batches rotate the Minion; the scripted Storyteller no longer excludes any legal option (the
Saint or Drunk can be the red herring, the Drunk's apparent role can be a bluff, a Mayor kill can
bounce to anyone); a drunk Fortune Teller's false picture has two "evil" players.

## v5
v4 plus a fixed day: 3 private beats, 3 town-square beats, then nominations, every day. No
early end (v4 ended the town square when most living players called for nominations or a beat
was silent, which cut 20 of 34 v3 days short); `call_nominations` is gone, and day 1 no longer
has its own private-beat setting. Nominations gain a comment turn for everyone between the defense
and the vote; remarks during the call for nominations are gone (only accusations are heard). The
Slayer can shoot on any public turn, not just the town square. The scripted Storyteller rules
nothing legal out: 10% of each decision is uniform over all legal values, and the style is
weights only (20% of Drunks get true information all game; the Spy can register as an in-play
character; the Recluse can register as the Imp; a misinformed Washerwoman sometimes shows only
good players; a misinformed Librarian is sometimes told zero Outsiders). The LLM Storyteller
option is removed.

Telemetry (does not change play, so no version bump): from Sept 27, v5 games also record belief
probes. At dawn of day 1 and just before each day's nominations, every seat answers an
out-of-game question on a fork of its conversation (same model, effort, thinking and schema, so it
reads from cache); the question and answer never enter the seat's conversation, and its pending
events stay pending. Good seats give P(evil), P(Demon) and a character guess for every other
player; evil seats predict what the good players believe; everyone states their claim and a
one-line plan. `tests/` checks that probes leave every seat's turns identical. Scores:
`python -m clocktower analyze`.

## v6 — current (Sept 27)
Changes from v5, after reading 61 v5 games (seven model pairings) and auditing the rules and the
Storyteller against 2,750 simulated games:
- Night order: the Poisoner, Monk and Imp choose first; the Fortune Teller and Butler are woken
  after the kill, so a player killed that night is never asked to choose (v5 asked everyone at
  once, and a Fortune Teller killed that night "chose" and heard nothing, which read as a lie).
- Starpass: a Monk-protected Imp cannot starpass; poison ends when the Poisoner becomes the Imp.
- Interface: whispers to more than two players (or beyond three a turn) tell the sender what was
  dropped; a blocked Butler's vote remark is not shown; a vote with neither yes nor no is asked
  again; speech caps rise (turn 150 words, defense 200) and a cut line ends "[cut off]"; the
  nomination notice says the pick among simultaneous nominations was random.
- Player prompt: the night order, and that nothing is revealed when a player dies.
- Storyteller: misinformation is false (when the style misleads an impaired player, a value a
  working ability could show is moved to the nearest plausible one it could not; in v5 about half
  of drunk/poisoned Chef, Empath, Fortune Teller and Undertaker results were true). A misinformed
  Undertaker is never shown "Imp", and impaired players are never shown their own character.
  The uniform floor drops from 10% to 3% (still over every legal value). The Drunk's apparent
  character is among the Demon bluffs 5% of the time (v5: 32% of Drunk games), the Drunk 5%. An
  Investigator's second player is good 90% of the time; a Mayor bounce lands on the Minion 5%;
  the red herring is a Townsfolk other than the Fortune Teller 85%. A Spy registering to a
  Washerwoman or Librarian as a good character uses the bluff / in-play / other weights.
- Budget: the per-turn output ceiling is 8K tokens (v5: 16K), identical for every model. It cuts
  runaway thinking loops (0.2% of Sonnet 5 turns went past 8K) and no Opus or Astra turn.
- Runs: no request cap (every game and seat at once); every game in an experiment has its own
  seed; teams can have their own effort (`--good-effort`, `--evil-effort`). OpenAI reasoning
  summaries use `concise`, the only setting that reliably returns text (logging only).
