# Designing and balancing a script

Community guidance on building scripts, in our own words. Sources include TPI's guidance on the wiki
([Script Tool](https://wiki.bloodontheclocktower.com/Script_Tool) and the Storyteller pages) and common advice in
the community (botcscripts.com reviews, r/BloodOnTheClocktower). Useful both to humans and to any code that
generates or validates scripts.

## Structure

- **Usual shape**: 13 Townsfolk, 4 Outsiders, 4 Minions, 4 Demons (the base-script shape). Fewer Demons is fine;
  one Demon makes the script easier to read.
- **Enough of each type to fill the setup**: a 15-player game needs 9 Townsfolk, so a script needs well over 9
  to keep bluffs available (the Demon's three bluffs come from unused good characters).
- **Teensyville**: around 6 Townsfolk, 2 Outsiders, 2 Minions, 2 Demons.

## Balance principles

1. **Information vs. misinformation.** Every strong information source should have something on the script that
   can make it wrong (a droisoner, a misregistering character, a Vortox-like effect). A script with lots of
   information and no corruption is solved on day 2; a script with lots of corruption and little information is
   a coin flip.
2. **Bluffability.** Evil needs believable claims. Roles whose results are private and unverifiable (Monk,
   Soldier, Savant) give evil room; roles with public mechanics (Slayer, Virgin, Juggler) let good verify claims.
3. **Kill pressure vs. protection.** Count expected deaths per day cycle. Too much protection stalls games; too
   many extra deaths end them early.
4. **Outsider count as information.** Setup modifiers (Baron, Godfather, Fang Gu, Vigormortis, Balloonist, Xaan,
   Sentinel, Kazali) make the Outsider count a clue. Include ways to learn it (Librarian, Balloonist, Godfather
   claims) if modifiers are present.
5. **Demon variety.** With several Demons, each should be distinguishable from the pattern of deaths and from
   information, or the game becomes guessing.
6. **Win-condition characters** (Saint, Mayor, Vortox, Evil Twin, Klutz, Alsaahir, Leviathan) reshape the game;
   one or two per script is plenty.
7. **Jinxes.** Check every pair on the script against the official jinx list
   ([jinxes.json](../data/jinxes.json)) and print the rulings for players.
8. **New-player load.** Count how many characters require explanation (madness, alignment change, character
   change). Beginner scripts keep these near zero.

## Checks a script validator can automate

- Each id exists in [characters.json](../data/characters.json); team counts fit the setup table at the intended
  player counts, including setup modifiers.
- Night order: every character with a night action has a position.
- Jinxed pairs present (warn, list the rulings).
- At least one source of misinformation if there are three or more nightly information roles.
- The Demon has enough bluffs: at least (Townsfolk on script) minus (largest Townsfolk count needed) plus
  Outsiders is three or more.
- Characters that need another character (Huntsman/Damsel, Choirboy/King) include it.

These are heuristics drawn from community practice, not official rules.
