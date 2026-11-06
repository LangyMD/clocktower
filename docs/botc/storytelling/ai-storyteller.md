# Designing an AI Storyteller

Design notes that connect the Storytelling knowledge in this folder to this repo's code. This is a proposal to
drive future work, not a description of something already built.

## What exists today

- `clocktower/agents.py` has `ScriptedStoryteller.choose(choice)`, which returns `choice.options(rng)`.
- `clocktower/state.py` defines `Choice(id, values, style)`: every Storyteller decision is a list of **all legal
  values** plus a scripted random "style". `POLICY` holds the hand-set probabilities.
- `clocktower/game.py` calls `self.decide(choice)`, which asks the Storyteller, **rejects any illegal value**,
  and logs an `st_choice` audit event.

This is the right seam for an AI Storyteller: the rules engine enumerates the legal options, and the
Storyteller only picks among them. An LLM Storyteller can be swapped in by implementing `choose(choice)`
without giving it the power to break rules.

## The decisions a Storyteller makes

Grouped by how much judgement they need (TB ids from `state.py` in brackets where they exist):

**Setup**
- Which characters go in the bag (today random via `random_setup`).
- The Drunk's believed character (`drunk_as_choice`), the red herring (`red_herring_choice`), Demon bluffs
  (`bluffs_choice`).
- On other scripts: Bounty Hunter's evil Townsfolk, Village Idiot drunk, Kazali Minion choices (the Kazali's),
  Lunatic's fake info, Summoner bluffs, Xaan's X.

**Information**
- Pair info (`pair_choice`), Chef, Empath, Fortune Teller, Undertaker/Ravenkeeper (`character_choice`).
- Everything a droisoned player is told.
- Content-generating abilities with no fixed answer set: Savant statements, Artist answers, Fisherman advice,
  High Priestess and General judgements, Amnesiac's invented ability, Wizard wishes, Djinn rules.

**Registration**
- Spy and Recluse registration per ability use (`yes_choice` with POLICY rates); Legion, Magician and others on
  other scripts.

**Deaths and executions**
- Mayor bounce (`mayor_choice`), Imp starpass heir (`heir_choice`).
- On other scripts: Gossip and Tinker deaths, Shabaloth regurgitation, Pacifist and Scapegoat, Pit-Hag Demon
  nights, Moonchild, Lil' Monsta, Al-Hadikhia, Ojo misses, Psychopath roshambo.

**Judgement calls**
- Madness (Cerenovus, Mutant, Harpy, Pixie, Bigwig): did the player try hard enough?
- Deviant ("were they funny?"), Angel and Hell's Librarian penalties, Politician ("most responsible").

**Pacing and presentation**
- When to end discussion and call nominations; how to describe events; the post-game story.

## Architecture sketch

1. **Rules engine owns legality.** For every decision the engine produces the legal set (as `Choice` does
   today). For free-text decisions (Savant, Fisherman) the engine gives constraints (one true, one false) and
   validates what it can.
2. **Storyteller model gets an omniscient briefing**: the Grimoire, every claim made publicly, a summary of private
   claims if logged, the history of information given, and the current balance estimate.
3. **Policy prompts come from this knowledge base**: the [principles](principles.md), the
   [misinformation guide](information-and-misinformation.md), the script's page, and the involved characters'
   entries (summary, tags, per-role Storytelling notes).
4. **Consistency memory**: store the "false world" chosen for each droisoned player so later nights stay
   consistent (today's engine already tracks `decoys` and `truthful`).
5. **Balance signal**: estimate who is winning (alive counts, how close good's consensus is to the Demon,
   whether evil's claims hold). The `probes.jsonl` belief probes in this repo are a natural input.
6. **Audit and explanation**: log each decision with a one-line rationale; generate the post-game story from it.
7. **Fallback**: on model failure or an illegal answer, fall back to the scripted style, so a game never stalls.

## Risks to manage

- **Leakage**: the Storyteller sees everything; its public text (death announcements, narration) must be
  templated or checked so it cannot leak the Grimoire.
- **Bias**: an LLM Storyteller may favour one side or one model; for the benchmark use it must be evaluated
  against the scripted Storyteller (win rates, rating stability) before being trusted.
- **Cost and latency**: there are dozens of decisions per game; most are cheap and can be batched per night.
- **Reproducibility**: the benchmark's seeds currently reproduce games exactly; an AI Storyteller needs logged
  decisions (and a replay mode that reads them back) to keep that property.

## Suggested first steps

1. Add an `LLMStoryteller` implementing `choose(choice)` for the existing TB choices, with the scripted
   Storyteller as fallback.
2. Give `Choice` a short human-readable description of what is being decided and why it matters, so the model
   has context.
3. Run a calibration batch against the scripted Storyteller and compare evil's win rate and game length.
4. Extend to free-text decisions once multi-script support brings Savant-like characters.
