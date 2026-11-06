# Experimental characters

Characters released by TPI after the three base scripts, first through the online app's experimental
"carousel" and the Kickstarter edition (`"edition": "carousel"` in [characters.json](../data/characters.json)).
They are official but newer, and some are still revised from time to time, so check the wiki page before
implementing one. Summaries below are our own; the authoritative text comes from
`python scripts/botc_data.py fetch`.

## How they change the game

- **New information shapes**: Steward, Knight, Noble, Shugenja, High Priestess, General, Balloonist,
  Village Idiot, King give information that does not fit the base scripts' patterns, so they suit custom scripts.
- **Evil-team scramblers**: Poppy Grower, Magician, Marionette, Lunatic-like effects stop evil from knowing its team,
  which makes the Demon's first days much harder.
- **Win-condition characters**: Alsaahir, Cult Leader, Politician, Heretic, Damsel, Goblin, Fearmonger, Leviathan,
  Riot. These change what each team is trying to do and are the hardest to balance.
- **Storyteller-power characters**: Wizard, Plague Doctor, Amnesiac, Fisherman, High Priestess, General ask the
  Storyteller for judgement, advice or invention. They are the hardest for an AI Storyteller, and the most
  interesting test of one.
- **Setup-bending Demons**: Kazali, Lord of Typhon, Legion, Lil' Monsta, Summoner, Riot, Leviathan change setup or
  the shape of a game.


## Townsfolk

| Character | Type | What it does (our summary) | Tags |
|---|---|---|---|
| [Acrobat](https://wiki.bloodontheclocktower.com/Acrobat) | Townsfolk | Each night except the first picks a player; if that player is or becomes drunk or poisoned that night, the Acrobat dies. | self-risk, choose-players |
| [Alchemist](https://wiki.bloodontheclocktower.com/Alchemist) | Townsfolk | Has the ability of a Minion character not in play (Storyteller picks it); the Storyteller may ask them to choose again when using it. | copy-ability |
| [Alsaahir](https://wiki.bloodontheclocktower.com/Alsaahir) | Townsfolk | Each day may publicly name who the Minions and Demons are; if fully correct, good wins. | win-condition, day-action |
| [Amnesiac](https://wiki.bloodontheclocktower.com/Amnesiac) | Townsfolk | Does not know their own ability (the Storyteller invents one). Each day privately guesses it and learns how close they are. | hidden-ability, info-day |
| [Atheist](https://wiki.bloodontheclocktower.com/Atheist) | Townsfolk | Setup: no evil characters at all. The Storyteller may break rules; if the Atheist is executed (even dead), good wins. | setup-modifier, win-condition |
| [Balloonist](https://wiki.bloodontheclocktower.com/Balloonist) | Townsfolk | Each night learns a player whose character type differs from the previous night's. Setup: may add one Outsider. | info-nightly, setup-modifier |
| [Banshee](https://wiki.bloodontheclocktower.com/Banshee) | Townsfolk | If the Demon kills the Banshee, everyone learns it, and from then on the Banshee may nominate twice per day and vote twice per nomination. | voting-modifier, on-death |
| [Bounty Hunter](https://wiki.bloodontheclocktower.com/Bounty_Hunter) | Townsfolk | Night 1: learns an evil player; when that player dies, learns another that night. Setup: one Townsfolk is evil. | info-start, info-on-death, setup-modifier |
| [Cannibal](https://wiki.bloodontheclocktower.com/Cannibal) | Townsfolk | Has the ability of the most recently executed player; if that player was evil, the Cannibal is poisoned until a good player is executed. | copy-ability, droison |
| [Choirboy](https://wiki.bloodontheclocktower.com/Choirboy) | Townsfolk | If the Demon kills the King, learns which player is the Demon. Setup: adds the King. | info-on-death, setup-modifier |
| [Cult Leader](https://wiki.bloodontheclocktower.com/Cult_Leader) | Townsfolk | Each night takes the alignment of a living neighbour. If every good player chooses to join the cult, the Cult Leader's team wins. | alignment-change, win-condition |
| [Engineer](https://wiki.bloodontheclocktower.com/Engineer) | Townsfolk | Once per game at night, chooses which Minion characters or which Demon character are in play (the evil players change accordingly). | character-change, once-per-game |
| [Farmer](https://wiki.bloodontheclocktower.com/Farmer) | Townsfolk | When the Farmer dies at night, a living good player becomes a Farmer. | on-death |
| [Fisherman](https://wiki.bloodontheclocktower.com/Fisherman) | Townsfolk | Once per game, during the day, visits the Storyteller for advice on how to win. | info-day, once-per-game |
| [General](https://wiki.bloodontheclocktower.com/General) | Townsfolk | Each night learns which team the Storyteller thinks is winning (good, evil or neither). | info-nightly |
| [High Priestess](https://wiki.bloodontheclocktower.com/High_Priestess) | Townsfolk | Each night learns which player the Storyteller thinks they should talk to most. | info-nightly |
| [Huntsman](https://wiki.bloodontheclocktower.com/Huntsman) | Townsfolk | Once per game at night picks a living player; if it is the Damsel, the Damsel becomes a Townsfolk not in play. Setup: adds the Damsel. | once-per-game, character-change, setup-modifier |
| [King](https://wiki.bloodontheclocktower.com/King) | Townsfolk | Each night, once the dead are at least as many as the living, learns one living character. The Demon knows who the King is. | info-nightly |
| [Knight](https://wiki.bloodontheclocktower.com/Knight) | Townsfolk | Night 1: learns two players who are not the Demon. | info-start |
| [Lycanthrope](https://wiki.bloodontheclocktower.com/Lycanthrope) | Townsfolk | Each night except the first picks a living player; if good, they die and the Demon does not kill. One good player reads as evil. | kill, misregistration, choose-players |
| [Magician](https://wiki.bloodontheclocktower.com/Magician) | Townsfolk | The Demon thinks the Magician is a Minion, and the Minions think the Magician is the Demon. | misregistration, evil-info-scramble |
| [Nightwatchman](https://wiki.bloodontheclocktower.com/Nightwatchman) | Townsfolk | Once per game at night picks a player, who learns who the Nightwatchman is. | once-per-game, choose-players |
| [Noble](https://wiki.bloodontheclocktower.com/Noble) | Townsfolk | Night 1: learns three players, exactly one of whom is evil. | info-start |
| [Pixie](https://wiki.bloodontheclocktower.com/Pixie) | Townsfolk | Night 1: learns an in-play Townsfolk. If they stay "mad" about being that character, they gain its ability when its owner dies. | info-start, copy-ability, madness |
| [Poppy Grower](https://wiki.bloodontheclocktower.com/Poppy_Grower) | Townsfolk | While the Poppy Grower lives, evil players do not learn who each other are; when it dies, they learn that night. | evil-info-scramble |
| [Preacher](https://wiki.bloodontheclocktower.com/Preacher) | Townsfolk | Each night picks a player; a Minion picked learns it and loses its ability for the rest of the game. | droison, choose-players |
| [Princess](https://wiki.bloodontheclocktower.com/Princess) | Townsfolk | If, on their first day, they nominate a player who is then executed, the Demon does not kill that night. | protection |
| [Shugenja](https://wiki.bloodontheclocktower.com/Shugenja) | Townsfolk | Night 1: learns whether their nearest evil player is clockwise or anticlockwise (arbitrary if tied). | info-start |
| [Steward](https://wiki.bloodontheclocktower.com/Steward) | Townsfolk | Night 1: learns one good player. | info-start |
| [Village Idiot](https://wiki.bloodontheclocktower.com/Village_Idiot) | Townsfolk | Each night picks a player and learns their alignment. Setup: up to two extra Village Idiots, one of the extras drunk. | info-nightly, setup-modifier, choose-players |

## Outsiders

| Character | Type | What it does (our summary) | Tags |
|---|---|---|---|
| [Damsel](https://wiki.bloodontheclocktower.com/Damsel) | Outsider | All Minions know a Damsel is in play. If a Minion publicly guesses the Damsel (one guess only), good loses. | loss-condition |
| [Golem](https://wiki.bloodontheclocktower.com/Golem) | Outsider | May nominate only once per game; when they do, the nominee dies unless it is the Demon. | kill, once-per-game, nomination-restriction |
| [Hatter](https://wiki.bloodontheclocktower.com/Hatter) | Outsider | If the Hatter died that day or night, the Minions and Demon may each pick new Minion or Demon characters. | character-change, on-death |
| [Heretic](https://wiki.bloodontheclocktower.com/Heretic) | Outsider | Inverts the result: the winning team loses and the losing team wins, even if the Heretic is dead. | win-condition |
| [Hermit](https://wiki.bloodontheclocktower.com/Hermit) | Outsider | Has every Outsider ability on the script. Setup: may remove one Outsider. | setup-modifier, copy-ability |
| [Ogre](https://wiki.bloodontheclocktower.com/Ogre) | Outsider | Night 1 picks another player and silently joins that player's alignment (without knowing which), even if drunk or poisoned. | alignment-change |
| [Plague Doctor](https://wiki.bloodontheclocktower.com/Plague_Doctor) | Outsider | When the Plague Doctor dies, the Storyteller gains a Minion ability. | on-death |
| [Politician](https://wiki.bloodontheclocktower.com/Politician) | Outsider | If they were the player most responsible for their team losing, they switch alignment and win, even if dead. | win-condition |
| [Puzzlemaster](https://wiki.bloodontheclocktower.com/Puzzlemaster) | Outsider | One player is permanently drunk. If the Puzzlemaster guesses who (one guess), they learn the Demon; a wrong guess gives false information. | droison, info-day |
| [Snitch](https://wiki.bloodontheclocktower.com/Snitch) | Outsider | Each Minion receives three not-in-play bluffs. | bluffs |
| [Zealot](https://wiki.bloodontheclocktower.com/Zealot) | Outsider | While five or more players live, must vote for every nomination. | voting-restriction |

## Minions

| Character | Type | What it does (our summary) | Tags |
|---|---|---|---|
| [Boffin](https://wiki.bloodontheclocktower.com/Boffin) | Minion | The Demon also has the ability of a good character not in play; Boffin and Demon both know which. | copy-ability |
| [Boomdandy](https://wiki.bloodontheclocktower.com/Boomdandy) | Minion | If executed, everyone but three players dies; then after a countdown the player pointed at by most dies. | kill, on-death |
| [Fearmonger](https://wiki.bloodontheclocktower.com/Fearmonger) | Minion | Each night picks a player (all players learn when it is a new one); if the Fearmonger nominates and executes that player, the target's team loses. | loss-condition, choose-players |
| [Goblin](https://wiki.bloodontheclocktower.com/Goblin) | Minion | If the Goblin publicly claims to be the Goblin when nominated and is executed that day, evil wins. | win-condition |
| [Harpy](https://wiki.bloodontheclocktower.com/Harpy) | Minion | Each night picks two players; the next day the first must be "mad" that the second is evil, or one or both may die. | madness, kill, choose-players |
| [Marionette](https://wiki.bloodontheclocktower.com/Marionette) | Minion | Believes they are a good character but is a Minion; the Demon knows them. Setup: sits next to the Demon. Not added to the bag directly. | false-identity, setup-modifier |
| [Mezepheles](https://wiki.bloodontheclocktower.com/Mezepheles) | Minion | Night 1: learns a secret word. The first good player to say it turns evil that night. | alignment-change |
| [Organ Grinder](https://wiki.bloodontheclocktower.com/Organ_Grinder) | Minion | Votes are cast with eyes closed and the tally is secret. Each night chooses whether to be drunk until dusk. | voting-modifier, droison |
| [Psychopath](https://wiki.bloodontheclocktower.com/Psychopath) | Minion | Each day before nominations may publicly kill a player. If executed, the Psychopath dies only if they lose a game of rock-paper-scissors. | kill, day-action |
| [Summoner](https://wiki.bloodontheclocktower.com/Summoner) | Minion | Gets three bluffs. On night 3 picks a player who becomes an evil Demon of the Summoner's choosing. Setup: no Demon at the start. | bluffs, setup-modifier, character-change |
| [Vizier](https://wiki.bloodontheclocktower.com/Vizier) | Minion | Everyone knows who the Vizier is. Cannot die by day. If any good player voted, the Vizier may execute the nominee at once. | execution-modifier |
| [Widow](https://wiki.bloodontheclocktower.com/Widow) | Minion | Night 1: sees the Grimoire and poisons a player. One good player learns that a Widow is in play. | grimoire, droison |
| [Wizard](https://wiki.bloodontheclocktower.com/Wizard) | Minion | Once per game may make a wish to the Storyteller; if granted it may carry a cost and leave a hint. | wish, once-per-game |
| [Wraith](https://wiki.bloodontheclocktower.com/Wraith) | Minion | May open their eyes at night and wakes whenever other evil players wake. | night-eyes |
| [Xaan](https://wiki.bloodontheclocktower.com/Xaan) | Minion | On night X, where X is the number of Outsiders in play, every Townsfolk is poisoned until dusk. Setup: Storyteller may vary the Outsider count. | droison, setup-modifier |

## Demons

| Character | Type | What it does (our summary) | Tags |
|---|---|---|---|
| [Al-Hadikhia](https://wiki.bloodontheclocktower.com/Al-Hadikhia) | Demon | Each night except the first may pick three players (named publicly); each silently chooses to live or die, but if all three choose life, all three die. | kill, choose-players |
| [Kazali](https://wiki.bloodontheclocktower.com/Kazali) | Demon | Each night except the first kills a player. Setup: the Kazali picks which players become which Minions, and may change the Outsider count. | kill, setup-modifier |
| [Legion](https://wiki.bloodontheclocktower.com/Legion) | Demon | Most players are Legion. A player may die each night. Executions fail if only evil players voted. Legion also registers as a Minion. | kill, setup-modifier, misregistration |
| [Leviathan](https://wiki.bloodontheclocktower.com/Leviathan) | Demon | Everyone knows a Leviathan is in play. If more than one good player is executed, evil wins; after day 5, evil wins. | win-condition, game-ending |
| [Lil' Monsta](https://wiki.bloodontheclocktower.com/Lil'_Monsta) | Demon | The Minions each night choose who holds Lil' Monsta and counts as the Demon; a player may die each night. Setup: one extra Minion instead of a Demon player. | kill, setup-modifier |
| [Lleech](https://wiki.bloodontheclocktower.com/Lleech) | Demon | Night 1 picks a host who is poisoned. Each night except the first kills a player. The Lleech dies only when its host dies. | kill, droison |
| [Lord of Typhon](https://wiki.bloodontheclocktower.com/Lord_of_Typhon) | Demon | Each night except the first kills a player. Setup: evil sits in a contiguous line with the Lord of Typhon in the middle; one extra Minion; Outsider count may change. | kill, setup-modifier |
| [Ojo](https://wiki.bloodontheclocktower.com/Ojo) | Demon | Each night except the first names a character; that player dies. If the character is not in play, the Storyteller picks who dies. | kill |
| [Riot](https://wiki.bloodontheclocktower.com/Riot) | Demon | On day 3, the Minions become Riot; every nominee dies and must immediately nominate a living player. This must happen. | kill, game-ending |
| [Yaggababble](https://wiki.bloodontheclocktower.com/Yaggababble) | Demon | Night 1: learns a secret phrase. Each time they say it publicly that day, a player may die. | kill |
