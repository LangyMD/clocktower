# Blood on the Clocktower: what the game is

Blood on the Clocktower (BotC) is a social deduction game for 5 to 20 players, designed by Steven Medway and
published by The Pandemonium Institute (TPI); after years of playtesting it was funded on Kickstarter in 2022. It is in the same family as Mafia and
Werewolf but differs from them in ways that matter a great deal for anyone building an engine or an AI
Storyteller. Official reference: the [rules page](https://wiki.bloodontheclocktower.com/Rules) and
[Rules Explanation](https://wiki.bloodontheclocktower.com/Rules_Explanation) on the official wiki.

## The two teams

- **Good** is the majority: **Townsfolk** (useful abilities, mostly information or protection) and **Outsiders**
  (good players whose abilities hinder their own team).
- **Evil** is the minority: one **Demon** (kills at night; good wins if it dies) and some **Minions** (helpers
  with disruptive abilities). Evil players know each other from the first night (with a few exceptions) and
  the Demon receives three **bluffs**: good characters that are not in play, safe to claim.

## How a team wins

- Good wins when the **Demon dies** (and no other effect, such as the Scarlet Woman, keeps a Demon in play).
- Evil wins when **only two players are alive** (Travellers do not count), with the Demon among them.
- Some characters add other win or loss conditions (Saint, Mayor, Evil Twin, Vortox, Klutz, Leviathan and more).
  These are listed in `docs/botc/data/characters.json` under the tags `win-condition`, `loss-condition` and
  `game-ending`.

## What makes it different from Mafia

1. **Dead players keep playing.** A dead player stays at the table, may talk freely, keeps their team, and has
   one **ghost vote** to spend in any single later vote. Elimination is never the end of a player's game, which
   means the evil team cannot simply silence the people who know the most.
2. **Every player has a unique character with an ability.** Most good abilities produce information, so the good
   team solves a logic puzzle built from everyone's claims.
3. **Information can be wrong.** A player who is **drunk** or **poisoned** has no working ability, but the
   Storyteller still gives them information, and it may be false. Some characters **register** as something
   they are not. Good players therefore have to weigh which "worlds" (which assignment of characters) are
   consistent with all claims, and evil exploits the gaps.
4. **A Storyteller runs the game.** The Storyteller is not a player on either side. They know everything (the
   **Grimoire**), choose what malfunctioning abilities report, and make many judgement calls the rules leave
   open. Their goal is a fun game that comes down to the wire, not a win for either team.
5. **Scripts.** The game is played with a **script**: the list of characters that might be in play. The base
   box has three (Trouble Brewing, Bad Moon Rising, Sects & Violets); the community has built thousands of
   custom scripts from the full character pool. See [../scripts/README.md](../scripts/README.md).

## Shape of a game

The game alternates nights and days. On the first night evil learns its team and many good characters receive
starting information. Each day, players talk (publicly and in private conversations), then nominate and vote,
and at most one player is executed. Each later night the Demon kills, and other characters act. With one
death a night and up to one a day, a 10-player game usually runs four or five days. A full step-by-step account
is in [game-flow.md](game-flow.md).

## Where to go next

- [game-flow.md](game-flow.md): the turn structure, nominations, votes and executions, in detail.
- [character-types-and-setup.md](character-types-and-setup.md): character types, the setup table and setup
  modifiers, Travellers, Fabled and Loric.
- [glossary.md](glossary.md): terms such as drunk, poisoned, registers, mad, red herring, starpass.
- [rulings.md](rulings.md): the edge cases a rules engine has to decide.
