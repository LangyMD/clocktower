# Information and misinformation

The heart of Storytelling. Summarised from community advice (wiki character "How to Run" sections, TPI's
Storyteller guidance, and long-standing community practice).

## When you may give false information

Only when the ability is malfunctioning (the player is drunk, poisoned, or affected by Vortox-style effects) or
the ability says so (Savant, Dreamer, Fibbin, Puzzlemaster wrong guess). Otherwise every piece of information
must be true, though you usually still choose *which* true answer to give.

## Choosing true information

Most information abilities have several true answers. Examples:

- Washerwoman/Librarian/Investigator: which pair of players, and which character, among the valid options.
- Fortune Teller: none to choose, but the red herring is chosen at setup.
- Dreamer: which wrong character to show.
- Savant: which true and which false statement.

Guidelines: prefer answers that create a solvable puzzle; avoid answers that solve the game outright on night 1;
give new players the clearer options.

## Choosing false information

Techniques players and Storytellers commonly describe:

- **Consistent false world.** Decide on one alternative arrangement (for example, "in this player's world, X is
  the Demon") and give every piece of false information from it. This lets the droisoned player build a coherent
  but wrong case, which the town must untangle by cross-checking.
- **Plausible, not random.** A poisoned Empath who gets a 2 when both neighbours are confirmed good is quickly
  identified as poisoned. Prefer numbers that are believable given the public picture.
- **Frame, don't confirm.** False information that points at good players creates tension; false information
  that clears the Demon outright can end the game for good.
- **Sometimes tell the truth.** Giving a poisoned player true information is legal and keeps the town honest
  about assuming every poisoned result is wrong.
- **Match the evil team's story.** When the Poisoner targets someone, look at what evil has claimed; false
  information that supports evil's narrative rewards evil's play.

## Registration decisions

- **Spy**: often registers as good to information roles (otherwise the Spy is easily caught). Showing the Spy
  as a Townsfolk to the Washerwoman, or letting it survive the Virgin, are classic moves.
- **Recluse**: register as evil or a Demon sometimes, especially to the Fortune Teller or Investigator, to create
  a suspect; not every time, or the Recluse is always executed.
- **Legion, Magician, Lycanthrope's evil-registering good player** follow the same logic.

## Keep a record

Write down every piece of information and why you chose it. Consistency needs it, and the post-game reveal is
much better with it.

## How this repo's scripted Storyteller does it

The current engine (`clocktower/state.py`) implements several of these ideas as fixed probabilities in `POLICY`:
80% of poisoned nights give information from a "false world" (redrawn until it differs from the truth), the Drunk
keeps one false world all game (true in 20% of games), the Spy registers as evil 10% of the time, the Recluse 50%.
An AI Storyteller would replace these fixed rates with judgement about the current game; see
[ai-storyteller.md](ai-storyteller.md).
