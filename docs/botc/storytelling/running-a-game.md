# Running a game: the Storyteller's procedure

A checklist version of the game flow from the Storyteller's side. Steps marked **(decision)** are the points
where the Storyteller exercises judgement; they are catalogued for an AI Storyteller in
[ai-storyteller.md](ai-storyteller.md).

## Before the game

1. Choose a script and confirm the player count. **(decision)** Add Fabled/Loric if useful (Toymaker for new
   players, Djinn for jinxes).
2. Look up type counts; apply setup modifiers. **(decision)** Choose the characters.
3. Put tokens in the bag (minus Drunk/Marionette, plus their replacement tokens); players draw.
4. Fill the Grimoire. **(decision)** Choose the Drunk's believed character, the red herring, any setup-only
   choices (Bounty Hunter's evil Townsfolk, Kazali/Summoner arrangements, Village Idiot drunk).
5. Explain the script's unusual characters and any jinxes.

## First night

1. Everyone closes their eyes. Wake characters in first-night order.
2. Minion info, Demon info with **(decision)** three bluffs (good characters not in play).
3. Each character in order: show tokens or numbers; record their choices. **(decision)** For every info role:
   true information if healthy (with choices among legal options), or any information if droisoned.
4. Dawn: nobody has died (unless an ability says otherwise).

## Each day

1. Announce deaths from the night, without causes.
2. Open discussion; allow private conversations. **(decision)** How long; when to call for nominations.
3. Day abilities: Slayer shots, Gossip statements, Savant visits, Artist questions, Juggler guesses, Fisherman
   advice, Alsaahir guesses. **(decision)** For several of these (Savant statements, Fisherman advice, Artist
   answers when droisoned), the Storyteller writes the content.
4. Nominations: check eligibility; run each vote clockwise; announce the tally; track who's on the block.
   **(decision)** Registration for nomination-triggered abilities (Virgin, Witch).
5. Execution at day's end (or immediately for Virgin, Vizier). **(decision)** Execution-modifying abilities
   (Pacifist, Devil's Advocate, Scapegoat).
6. Check win conditions.

## Each later night

1. Wake characters in other-nights order. Record choices.
2. Resolve the Demon's kill against protections. **(decision)** Mayor bounce, regurgitation, arbitrary deaths,
   Tinker, Gossip victim.
3. Information roles wake after deaths. **(decision)** Information for droisoned or misregistering cases.
4. Dawn.

## End of game

1. Announce the winning team and why.
2. Reveal the Grimoire.
3. **(decision)** Tell the story: who was what, why each droisoned player got what they got, which choices
   swung the game.

## Bookkeeping

- Keep reminders on the Grimoire for every ongoing effect (poison, drunk, protection, used abilities, dead votes).
- Note every piece of information given, by whom and to whom; you will need it for consistency and for the reveal.
- In this repo, the `events.jsonl` audit stream already records Storyteller choices (`st_choice` events), which
  is the right shape for this.
