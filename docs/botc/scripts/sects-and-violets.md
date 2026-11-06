# Sects & Violets

The advanced script about misinformation, madness and character changes. Data:
[sects-and-violets.json](../data/scripts/sects-and-violets.json). Official page:
[Sects & Violets](https://wiki.bloodontheclocktower.com/Sects_%26_Violets).

## What the script is like

- **Lots of information, lots of it unreliable.** Many Townsfolk get nightly information (Dreamer, Flowergirl,
  Town Crier, Oracle, Mathematician, Savant), but the Vortox makes all Townsfolk information false, the No Dashii
  and Vigormortis poison, and the Pit-Hag and Barber change characters mid-game.
- **Madness.** The Cerenovus and Mutant introduce "madness": players must pretend to be a character or risk
  execution. Players must think about who is pretending and why.
- **Characters change.** The Pit-Hag turns players into new characters, the Snake Charmer swaps with the Demon, the
  Barber swaps characters, the Fang Gu jumps. Claims that were true yesterday may not be true today.
- **The Vortox trap.** If the Vortox is in play, a day with no execution loses the game for good; good must
  execute every day.

## Script-level advice

**For Storytellers**:

- Keep the Grimoire meticulous: S&V has many reminders and character changes.
- Madness judgements: be consistent and generous to new players; only punish clear breaks.
- Pit-Hag creating a Demon makes that night's deaths arbitrary: use it to keep the game interesting, not to end it.
- With the Vortox, give false information that still forms a story (consistently wrong rather than random).

**For good players**:

- Identify the Demon type early (Vortox changes everything; Fang Gu means Outsiders are targets).
- Use the Mathematician to sanity-check how much misinformation is flying.
- Juggler and Savant claims are useful for testing other claims; Savant statements can be cross-checked.

**For evil players**:

- The Witch and Cerenovus can control the day; the Evil Twin can make good unable to win.
- Claim roles whose information is easily faked (Savant, Juggler).
- The Pit-Hag can create chaos late; if the Demon dies, a Pit-Hag can make a new one.

## Roles

### Townsfolk

#### Clockmaker (`clockmaker`)
- **Brief**: night 1, learns how many seats separate the Demon from its nearest Minion.
- **Playing**: combine with seat positions of suspects; a 1 means a Minion sits next to the Demon.
- **Storytelling**: a droisoned Clockmaker's number is an easy misinformation lever; keep it consistent with the
  rest of the false world you are telling.
- **Bluffing**: easy for evil to claim; pick a number that frames good neighbours.

#### Dreamer (`dreamer`)
- **Brief**: each night picks a player and sees one good and one evil character, one correct.
- **Playing**: pick contested claimants; seeing their claimed role confirms them only if the other option is evil.
- **Storytelling**: pick the false character to suggest a plausible alternative world.
- **Bluffing**: evil can "confirm" allies by reporting their claimed role.

#### Snake Charmer (`snakecharmer`)
- **Brief**: each night picks a player; hitting the Demon swaps characters and alignments, and the new Demon is poisoned.
- **Playing**: target aggressive or suspicious players. If you become the Demon, you are evil now: play for evil.
- **Storytelling**: tell both players clearly what happened; the poisoned new Demon cannot kill that night.
- **Bluffing**: evil can claim to have charmed and "missed" a player to clear them.

#### Mathematician (`mathematician`)
- **Brief**: each night learns how many abilities malfunctioned since dawn because of another ability.
- **Playing**: a 0 means every result last night was clean; a high number says a lot of droisoning or Vortox.
- **Storytelling**: count carefully, including Vortox-falsified information and failed protections.

#### Flowergirl (`flowergirl`)
- **Brief**: each night after the first learns whether the Demon voted today.
- **Playing**: encourage everyone to vote (or not) to filter suspects; vote patterns become evidence.

#### Town Crier (`towncrier`)
- **Brief**: each night after the first learns whether a Minion nominated today.
- **Playing**: track the day's nominators; a "yes" narrows Minions.

#### Oracle (`oracle`)
- **Brief**: each night after the first learns how many dead players are evil.
- **Playing**: strongest late; it tells you whether your executions have hit evil.

#### Savant (`savant`)
- **Brief**: each day may privately get two statements, one true and one false.
- **Playing**: share statements publicly so others can resolve which is true.
- **Storytelling**: craft statements that are useful in combination and avoid giving the game away in one day.

#### Seamstress (`seamstress`)
- **Brief**: once per game learns whether two players share an alignment.
- **Playing**: use late on two finalists; "same" or "different" can decide the game.

#### Philosopher (`philosopher`)
- **Brief**: once per game gains a good character's ability; if that character is in play, its owner is drunk.
- **Playing**: copy a strong information role, or a role the town suspects is being claimed falsely.
- **Storytelling**: the Philosopher stays a Philosopher in the Grimoire; mark the drunk original.

#### Artist (`artist`)
- **Brief**: once per game asks any yes-or-no question.
- **Playing**: ask compound questions that split the remaining worlds, such as "is the Demon one of X, Y or Z?".
- **Storytelling**: answer honestly if sober; if droisoned, answer as the story needs.

#### Juggler (`juggler`)
- **Brief**: on day 1 publicly guesses up to five characters; that night learns how many were right.
- **Playing**: guess claims you want tested; the count confirms or breaks them.

#### Sage (`sage`)
- **Brief**: if the Demon kills the Sage, learns the Demon is one of two players.

### Outsiders

- **Mutant** (`mutant`): must not claim to be an Outsider; may be executed for it. Play as a Townsfolk.
- **Sweetheart** (`sweetheart`): when they die, one player is drunk for the rest of the game; ST picks who.
- **Barber** (`barber`): when they die, the Demon may swap two players' characters; the town gets confusion.
- **Klutz** (`klutz`): on learning of their death, publicly picks a player; picking evil loses for good.

### Minions

- **Evil Twin** (`eviltwin`): knows a good twin, who knows them; good cannot win while both live; executing the
  good twin loses for good. Good must work out which twin is good.
- **Witch** (`witch`): curses a player each night; if they nominate tomorrow, they die. Shapes who nominates.
- **Cerenovus** (`cerenovus`): makes a player mad about being a good character; the target must pretend or risk execution.
- **Pit-Hag** (`pithag`): changes a player's character each night (not first). Can create a new Demon.

### Demons

- **Fang Gu** (`fanggu`): jumps to the first Outsider it attacks; that Outsider becomes the evil Fang Gu.
- **Vigormortis** (`vigormortis`): killed Minions keep abilities and poison a Townsfolk neighbour.
- **No Dashii** (`nodashii`): poisons its nearest Townsfolk neighbours.
- **Vortox** (`vortox`): all Townsfolk information is false; a day with no execution loses for good.

### Travellers

- **Barista** (`barista`): sobers a player or doubles an ability for a day.
- **Harlot** (`harlot`): learns a willing player's character, at the risk of both dying.
- **Butcher** (`butcher`): may nominate again after the first execution.
- **Bone Collector** (`bonecollector`): restores a dead player's ability for one day.
- **Deviant** (`deviant`): cannot be exiled if they were funny.
