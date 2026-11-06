# Experimental characters

Characters released by TPI after the three base scripts, first through the online app's experimental
"carousel" and the Kickstarter edition (`"edition": "carousel"` in [characters.json](../data/characters.json)).
They are official but newer, and some are still revised from time to time, so check the wiki page before
implementing one. Each row gives the official ability text
and our plain-language summary.

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

| Character | Type | Official ability | In plain terms (our summary) |
|---|---|---|---|
| [Acrobat](https://wiki.bloodontheclocktower.com/Acrobat) | Townsfolk | Each night*, choose a player: if they are or become drunk or poisoned tonight, you die. | Each night except the first picks a player; if that player is or becomes drunk or poisoned that night, the Acrobat dies. |
| [Alchemist](https://wiki.bloodontheclocktower.com/Alchemist) | Townsfolk | You have a Minion ability. When using this, the Storyteller may prompt you to choose differently. | Has the ability of a Minion character not in play (Storyteller picks it); the Storyteller may ask them to choose again when using it. |
| [Alsaahir](https://wiki.bloodontheclocktower.com/Alsaahir) | Townsfolk | Each day, if you publicly guess which players are Minion(s) and which are Demon(s), good wins. | Each day may publicly name who the Minions and Demons are; if fully correct, good wins. |
| [Amnesiac](https://wiki.bloodontheclocktower.com/Amnesiac) | Townsfolk | You do not know what your ability is. Each day, privately guess what it is: you learn how accurate you are. | Does not know their own ability (the Storyteller invents one). Each day privately guesses it and learns how close they are. |
| [Atheist](https://wiki.bloodontheclocktower.com/Atheist) | Townsfolk | The Storyteller can break the game rules, and if executed, good wins, even if you are dead. [No evil characters] | Setup: no evil characters at all. The Storyteller may break rules; if the Atheist is executed (even dead), good wins. |
| [Balloonist](https://wiki.bloodontheclocktower.com/Balloonist) | Townsfolk | Each night, you learn a player of a different character type than last night. [+0 or +1 Outsider] | Each night learns a player whose character type differs from the previous night's. Setup: may add one Outsider. |
| [Banshee](https://wiki.bloodontheclocktower.com/Banshee) | Townsfolk | If the Demon kills you, all players learn this. From now on, you may nominate twice per day and vote twice per nomination. | If the Demon kills the Banshee, everyone learns it, and from then on the Banshee may nominate twice per day and vote twice per nomination. |
| [Bounty Hunter](https://wiki.bloodontheclocktower.com/Bounty_Hunter) | Townsfolk | You start knowing 1 evil player. If the player you know dies, you learn another evil player tonight. [1 Townsfolk is evil] | Night 1: learns an evil player; when that player dies, learns another that night. Setup: one Townsfolk is evil. |
| [Cannibal](https://wiki.bloodontheclocktower.com/Cannibal) | Townsfolk | You have the ability of the recently killed executee. If they are evil, you are poisoned until a good player dies by execution. | Has the ability of the most recently executed player; if that player was evil, the Cannibal is poisoned until a good player is executed. |
| [Choirboy](https://wiki.bloodontheclocktower.com/Choirboy) | Townsfolk | If the Demon kills the King, you learn which player is the Demon. [+the King] | If the Demon kills the King, learns which player is the Demon. Setup: adds the King. |
| [Cult Leader](https://wiki.bloodontheclocktower.com/Cult_Leader) | Townsfolk | Each night, you become the alignment of an alive neighbor. If all good players choose to join your cult, your team wins. | Each night takes the alignment of a living neighbour. If every good player chooses to join the cult, the Cult Leader's team wins. |
| [Engineer](https://wiki.bloodontheclocktower.com/Engineer) | Townsfolk | Once per game, at night, choose which Minions or which Demon is in play. | Once per game at night, chooses which Minion characters or which Demon character are in play (the evil players change accordingly). |
| [Farmer](https://wiki.bloodontheclocktower.com/Farmer) | Townsfolk | When you die at night, an alive good player becomes a Farmer. | When the Farmer dies at night, a living good player becomes a Farmer. |
| [Fisherman](https://wiki.bloodontheclocktower.com/Fisherman) | Townsfolk | Once per game, during the day, visit the Storyteller for some advice to help your team win. | Once per game, during the day, visits the Storyteller for advice on how to win. |
| [General](https://wiki.bloodontheclocktower.com/General) | Townsfolk | Each night, you learn which alignment the Storyteller believes is winning: good, evil, or neither. | Each night learns which team the Storyteller thinks is winning (good, evil or neither). |
| [High Priestess](https://wiki.bloodontheclocktower.com/High_Priestess) | Townsfolk | Each night, learn which player the Storyteller believes you should talk to most. | Each night learns which player the Storyteller thinks they should talk to most. |
| [Huntsman](https://wiki.bloodontheclocktower.com/Huntsman) | Townsfolk | Once per game, at night, choose a living player: the Damsel, if chosen, becomes a not-in-play Townsfolk. [+the Damsel] | Once per game at night picks a living player; if it is the Damsel, the Damsel becomes a Townsfolk not in play. Setup: adds the Damsel. |
| [King](https://wiki.bloodontheclocktower.com/King) | Townsfolk | Each night, if the dead equal or outnumber the living, you learn 1 alive character. The Demon knows you are the King. | Each night, once the dead are at least as many as the living, learns one living character. The Demon knows who the King is. |
| [Knight](https://wiki.bloodontheclocktower.com/Knight) | Townsfolk | You start knowing 2 players that are not the Demon. | Night 1: learns two players who are not the Demon. |
| [Lycanthrope](https://wiki.bloodontheclocktower.com/Lycanthrope) | Townsfolk | Each night*, choose an alive player. If good, they die & the Demon doesn’t kill tonight. One good player registers as evil. | Each night except the first picks a living player; if good, they die and the Demon does not kill. One good player reads as evil. |
| [Magician](https://wiki.bloodontheclocktower.com/Magician) | Townsfolk | The Demon thinks you are a Minion. Minions think you are a Demon. | The Demon thinks the Magician is a Minion, and the Minions think the Magician is the Demon. |
| [Nightwatchman](https://wiki.bloodontheclocktower.com/Nightwatchman) | Townsfolk | Once per game, at night, choose a player: they learn you are the Nightwatchman. | Once per game at night picks a player, who learns who the Nightwatchman is. |
| [Noble](https://wiki.bloodontheclocktower.com/Noble) | Townsfolk | You start knowing 3 players, 1 and only 1 of which is evil. | Night 1: learns three players, exactly one of whom is evil. |
| [Pixie](https://wiki.bloodontheclocktower.com/Pixie) | Townsfolk | You start knowing 1 in-play Townsfolk. If you were mad that you were this character, you gain their ability when they die. | Night 1: learns an in-play Townsfolk. If they stay "mad" about being that character, they gain its ability when its owner dies. |
| [Poppy Grower](https://wiki.bloodontheclocktower.com/Poppy_Grower) | Townsfolk | Minions & Demons do not know each other. If you die, they learn who each other are that night. | While the Poppy Grower lives, evil players do not learn who each other are; when it dies, they learn that night. |
| [Preacher](https://wiki.bloodontheclocktower.com/Preacher) | Townsfolk | Each night, choose a player: a Minion, if chosen, learns this. All chosen Minions have no ability. | Each night picks a player; a Minion picked learns it and loses its ability for the rest of the game. |
| [Princess](https://wiki.bloodontheclocktower.com/Princess) | Townsfolk | On your 1st day, if you nominated & executed a player, the Demon doesn't kill tonight. | If, on their first day, they nominate a player who is then executed, the Demon does not kill that night. |
| [Shugenja](https://wiki.bloodontheclocktower.com/Shugenja) | Townsfolk | You start knowing if your closest evil player is clockwise or anti-clockwise. If equidistant, this info is arbitrary. | Night 1: learns whether their nearest evil player is clockwise or anticlockwise (arbitrary if tied). |
| [Steward](https://wiki.bloodontheclocktower.com/Steward) | Townsfolk | You start knowing 1 good player. | Night 1: learns one good player. |
| [Village Idiot](https://wiki.bloodontheclocktower.com/Village_Idiot) | Townsfolk | Each night, choose a player: you learn their alignment. [+0 to +2 Village Idiots. 1 of the extras is drunk] | Each night picks a player and learns their alignment. Setup: up to two extra Village Idiots, one of the extras drunk. |

## Outsiders

| Character | Type | Official ability | In plain terms (our summary) |
|---|---|---|---|
| [Damsel](https://wiki.bloodontheclocktower.com/Damsel) | Outsider | All Minions know a Damsel is in play. If a Minion publicly guesses you (once), your team loses. | All Minions know a Damsel is in play. If a Minion publicly guesses the Damsel (one guess only), good loses. |
| [Golem](https://wiki.bloodontheclocktower.com/Golem) | Outsider | You may only nominate once per game. When you do, if the nominee is not the Demon, they die. | May nominate only once per game; when they do, the nominee dies unless it is the Demon. |
| [Hatter](https://wiki.bloodontheclocktower.com/Hatter) | Outsider | If you died today or tonight, the Minion & Demon players may choose new Minion & Demon characters to be. | If the Hatter died that day or night, the Minions and Demon may each pick new Minion or Demon characters. |
| [Heretic](https://wiki.bloodontheclocktower.com/Heretic) | Outsider | Whoever wins, loses & whoever loses, wins, even if you are dead. | Inverts the result: the winning team loses and the losing team wins, even if the Heretic is dead. |
| [Hermit](https://wiki.bloodontheclocktower.com/Hermit) | Outsider | You have all Outsider abilities. [-0 or -1 Outsider] | Has every Outsider ability on the script. Setup: may remove one Outsider. |
| [Ogre](https://wiki.bloodontheclocktower.com/Ogre) | Outsider | On your 1st night, choose a player (not yourself): you become their alignment (you don't know which) even if drunk or poisoned. | Night 1 picks another player and silently joins that player's alignment (without knowing which), even if drunk or poisoned. |
| [Plague Doctor](https://wiki.bloodontheclocktower.com/Plague_Doctor) | Outsider | When you die, the Storyteller gains a Minion ability. | When the Plague Doctor dies, the Storyteller gains a Minion ability. |
| [Politician](https://wiki.bloodontheclocktower.com/Politician) | Outsider | If you were the player most responsible for your team losing, you change alignment & win, even if dead. | If they were the player most responsible for their team losing, they switch alignment and win, even if dead. |
| [Puzzlemaster](https://wiki.bloodontheclocktower.com/Puzzlemaster) | Outsider | 1 player is drunk, even if you die. If you guess (once) who it is, learn the Demon player, but guess wrong & get false info. | One player is permanently drunk. If the Puzzlemaster guesses who (one guess), they learn the Demon; a wrong guess gives false information. |
| [Snitch](https://wiki.bloodontheclocktower.com/Snitch) | Outsider | Each Minion gets 3 bluffs. | Each Minion receives three not-in-play bluffs. |
| [Zealot](https://wiki.bloodontheclocktower.com/Zealot) | Outsider | If there are 5 or more players alive, you must vote for every nomination. | While five or more players live, must vote for every nomination. |

## Minions

| Character | Type | Official ability | In plain terms (our summary) |
|---|---|---|---|
| [Boffin](https://wiki.bloodontheclocktower.com/Boffin) | Minion | The Demon (even if drunk or poisoned) has a not-in-play good character’s ability. You both know which. | The Demon also has the ability of a good character not in play; Boffin and Demon both know which. |
| [Boomdandy](https://wiki.bloodontheclocktower.com/Boomdandy) | Minion | If you are executed, all but 3 players die. After a 10 to 1 countdown, the player with the most players pointing at them, dies. | If executed, everyone but three players dies; then after a countdown the player pointed at by most dies. |
| [Fearmonger](https://wiki.bloodontheclocktower.com/Fearmonger) | Minion | Each night, choose a player: if you nominate & execute them, their team loses. All players know if you choose a new player. | Each night picks a player (all players learn when it is a new one); if the Fearmonger nominates and executes that player, the target's team loses. |
| [Goblin](https://wiki.bloodontheclocktower.com/Goblin) | Minion | If you publicly claim to be the Goblin when nominated & are executed that day, your team wins. | If the Goblin publicly claims to be the Goblin when nominated and is executed that day, evil wins. |
| [Harpy](https://wiki.bloodontheclocktower.com/Harpy) | Minion | Each night, choose 2 players: tomorrow, the 1st player is mad that the 2nd is evil, or one or both might die. | Each night picks two players; the next day the first must be "mad" that the second is evil, or one or both may die. |
| [Marionette](https://wiki.bloodontheclocktower.com/Marionette) | Minion | You think you are a good character, but you are not. The Demon knows who you are. [You neighbor the Demon] | Believes they are a good character but is a Minion; the Demon knows them. Setup: sits next to the Demon. Not added to the bag directly. |
| [Mezepheles](https://wiki.bloodontheclocktower.com/Mezepheles) | Minion | You start knowing a secret word. The 1st good player to say this word becomes evil that night. | Night 1: learns a secret word. The first good player to say it turns evil that night. |
| [Organ Grinder](https://wiki.bloodontheclocktower.com/Organ_Grinder) | Minion | All players keep their eyes closed when voting and the vote tally is secret. Each night, choose if you are drunk until dusk. | Votes are cast with eyes closed and the tally is secret. Each night chooses whether to be drunk until dusk. |
| [Psychopath](https://wiki.bloodontheclocktower.com/Psychopath) | Minion | Each day, before nominations, you may publicly choose a player: they die. If executed, you only die if you lose roshambo. | Each day before nominations may publicly kill a player. If executed, the Psychopath dies only if they lose a game of rock-paper-scissors. |
| [Summoner](https://wiki.bloodontheclocktower.com/Summoner) | Minion | You get 3 bluffs. On the 3rd night, choose a player: they become an evil Demon of your choice. [No Demon] | Gets three bluffs. On night 3 picks a player who becomes an evil Demon of the Summoner's choosing. Setup: no Demon at the start. |
| [Vizier](https://wiki.bloodontheclocktower.com/Vizier) | Minion | All players know you are the Vizier. You cannot die during the day. If good voted, you may choose to execute immediately. | Everyone knows who the Vizier is. Cannot die by day. If any good player voted, the Vizier may execute the nominee at once. |
| [Widow](https://wiki.bloodontheclocktower.com/Widow) | Minion | On your 1st night, look at the Grimoire & choose a player: they are poisoned. 1 good player knows a Widow is in play. | Night 1: sees the Grimoire and poisons a player. One good player learns that a Widow is in play. |
| [Wizard](https://wiki.bloodontheclocktower.com/Wizard) | Minion | Once per game, choose to make a wish. If granted, it might have a price & leave a clue as to its nature. | Once per game may make a wish to the Storyteller; if granted it may carry a cost and leave a hint. |
| [Wraith](https://wiki.bloodontheclocktower.com/Wraith) | Minion | You may choose to open your eyes at night. You wake when other evil players do. | May open their eyes at night and wakes whenever other evil players wake. |
| [Xaan](https://wiki.bloodontheclocktower.com/Xaan) | Minion | On night X, all Townsfolk are poisoned until dusk. [X Outsiders] | On night X, where X is the number of Outsiders in play, every Townsfolk is poisoned until dusk. Setup: Storyteller may vary the Outsider count. |

## Demons

| Character | Type | Official ability | In plain terms (our summary) |
|---|---|---|---|
| [Al-Hadikhia](https://wiki.bloodontheclocktower.com/Al-Hadikhia) | Demon | Each night*, you may choose 3 players (all players learn who): each silently chooses to live or die, but if all live, all die. | Each night except the first may pick three players (named publicly); each silently chooses to live or die, but if all three choose life, all three die. |
| [Kazali](https://wiki.bloodontheclocktower.com/Kazali) | Demon | Each night*, choose a player: they die. [You choose which players are which Minions. -? to +? Outsiders] | Each night except the first kills a player. Setup: the Kazali picks which players become which Minions, and may change the Outsider count. |
| [Legion](https://wiki.bloodontheclocktower.com/Legion) | Demon | Each night*, a player might die. Executions fail if only evil voted. You register as a Minion too. [Most players are Legion] | Most players are Legion. A player may die each night. Executions fail if only evil players voted. Legion also registers as a Minion. |
| [Leviathan](https://wiki.bloodontheclocktower.com/Leviathan) | Demon | If more than 1 good player is executed, evil wins. All players know you are in play. After day 5, evil wins. | Everyone knows a Leviathan is in play. If more than one good player is executed, evil wins; after day 5, evil wins. |
| [Lil' Monsta](https://wiki.bloodontheclocktower.com/Lil'_Monsta) | Demon | Each night, Minions choose who babysits Lil' Monsta & "is the Demon". Each night*, a player might die. [+1 Minion] | The Minions each night choose who holds Lil' Monsta and counts as the Demon; a player may die each night. Setup: one extra Minion instead of a Demon player. |
| [Lleech](https://wiki.bloodontheclocktower.com/Lleech) | Demon | Each night*, choose a player: they die. You start by choosing a player: they are poisoned. You die if & only if they are dead. | Night 1 picks a host who is poisoned. Each night except the first kills a player. The Lleech dies only when its host dies. |
| [Lord of Typhon](https://wiki.bloodontheclocktower.com/Lord_of_Typhon) | Demon | Each night*, choose a player: they die. [Evil characters are in a line. You are in the middle. +1 Minion. -? to +? Outsiders] | Each night except the first kills a player. Setup: evil sits in a contiguous line with the Lord of Typhon in the middle; one extra Minion; Outsider count may change. |
| [Ojo](https://wiki.bloodontheclocktower.com/Ojo) | Demon | Each night*, choose a character: they die. If they are not in play, the Storyteller chooses who dies. | Each night except the first names a character; that player dies. If the character is not in play, the Storyteller picks who dies. |
| [Riot](https://wiki.bloodontheclocktower.com/Riot) | Demon | On day 3, Minions become Riot & nominees die but nominate an alive player immediately. This must happen. | On day 3, the Minions become Riot; every nominee dies and must immediately nominate a living player. This must happen. |
| [Yaggababble](https://wiki.bloodontheclocktower.com/Yaggababble) | Demon | You start knowing a secret phrase. For each time you said it publicly today, a player might die. | Night 1: learns a secret phrase. Each time they say it publicly that day, a player may die. |
