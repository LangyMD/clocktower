# Rulings and edge cases an engine must decide

These are the points where implementations most often go wrong. Each line is a summary of the official ruling
as we understand it (from the wiki's character pages, the Rules Explanation and TPI's published clarifications);
where a ruling is a Storyteller judgement rather than a fixed rule, it says so. When in doubt, check the
character's wiki page (the `wiki` field in [characters.json](../data/characters.json)).

## Drunkenness and poison

- A droisoned player's ability does nothing, but they still wake and act as normal; they are never told.
- Information given to a droisoned player may be true or false, at the Storyteller's choice. Choosing *true*
  is legal and sometimes the better story.
- A droisoned character's **passive** effects stop too: a poisoned Soldier can be killed; a poisoned Saint
  executed does not lose the game; a poisoned Virgin does not execute a Townsfolk nominator; a poisoned
  Mayor does not win; a poisoned Recluse/Spy registers normally.
- **Setup modifiers still apply** (Baron's Outsiders exist even if the Baron is later poisoned).
- Droisoning does **not** remove the Demon's identity: a poisoned Demon still counts as the Demon for good's
  win condition and for the Fortune Teller.
- A poisoned Demon's kill fails (for Imp-style Demons). A poisoned Scarlet Woman does not become the Demon.
- Effects already done stay done: if the Poisoner dies, the poison ends immediately, but information already
  given stays as given.

## Registration

- Registration is decided **per ability use**: the Recluse might register as a Demon to the Fortune Teller
  tonight and as good to the Empath in the same night.
- It applies to abilities, not to game rules: an executed Recluse is not the Demon, so good does not win.
- Registering as a character also changes type and alignment as needed (a Recluse registering as an Imp
  registers as evil and as a Demon).

## Deaths and executions

- Only one execution per day. If a Virgin executes a nominator, no further nominations happen that day.
- If a nominee would be executed but does not die (Pacifist, Devil's Advocate, Fool), the execution still
  happened (no second execution that day; the Undertaker learns nothing because nobody died by execution).
- A player who "dies" twice (Zombuul, Fool) is treated as dead by the group after the first death only when the
  Storyteller announces it.
- The Imp choosing itself makes a living Minion the Imp; the Storyteller chooses which (usually the Scarlet
  Woman if present, since she would become the Demon anyway).
- The Scarlet Woman counts living players **before** the Demon's death, and Travellers do not count.
- "If the Demon kills you" triggers only on the Demon's own night kill, not on other night deaths (Godfather,
  Assassin, Gossip, Moonchild).
- The Mayor's bounce is the Storyteller's choice and can land on any player, including a Minion or no-one
  else at all (the Mayor just dies).

## Votes

- A vote counts if the hand is up when the clock hand reaches it; changing your mind afterwards does nothing.
- Ties: if two nominations have the same highest count, neither is executed.
- Butler: may vote only if the master is voting on that nomination. Groups handle a master who sits later in the
  vote order differently; this repo's engine asks the master first (see docs/PROTOCOL.md).
- Dead players can vote on a Traveller's exile without spending their ghost vote.

## Evil information

- Minion and Demon info happens only with 7 or more players.
- Demon bluffs must be good characters not in play. A Drunk's believed character is not in play, so it may be
  given as a bluff; experienced Storytellers usually avoid that because it confirms the Drunk to evil.

## Information choices

- Pair information (Washerwoman, Librarian, Investigator) must include one player who really has the shown
  character, unless the info role is droisoned or a misregistering character (Spy, Recluse) is used.
- Librarian with no Outsiders in play learns "zero". If the only Outsider is the Drunk, the Librarian can be
  shown the Drunk (which reveals a Drunk is in play) or zero (if the ST registers nothing).
- The Chef counts pairs around the whole circle, dead players included, with the circle wrapping round.
- The Empath skips dead neighbours and counts the nearest living players on each side.
- The Undertaker learns the character, not the alignment, and nothing if the execution killed nobody.

## Travellers

- Travellers can be the target of most abilities, but count for nothing in win conditions or setup.
- A Traveller's alignment is set by the Storyteller (often to balance the game) and may be told to them privately.

## Storyteller discretion

The rules leave many choices open on purpose. The ones that change outcomes most are listed in
[../storytelling/information-and-misinformation.md](../storytelling/information-and-misinformation.md) and,
as a decision catalogue for an AI Storyteller, in [../storytelling/ai-storyteller.md](../storytelling/ai-storyteller.md).
