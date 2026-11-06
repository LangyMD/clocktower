# Trouble Brewing

The beginner script and the one this repo's engine implements. Data: [trouble-brewing.json](../data/scripts/trouble-brewing.json).
Official page: [Trouble Brewing](https://wiki.bloodontheclocktower.com/Trouble_Brewing).

## What the script is like

- **Information-rich and straightforward.** Most Townsfolk get clear, checkable information, and there is one
  Demon (the Imp) whose only trick is the starpass. Good's job is to assemble the information into a single
  consistent world; evil's job is to break that with false claims and the Poisoner/Spy/Recluse/Drunk noise.
- **One Demon, four Minions.** Evil's whole toolkit is: poison (Poisoner), perfect knowledge (Spy), a backup
  Demon (Scarlet Woman) and more Outsiders (Baron). Most strategy follows from which Minion is in play.
- **Executions matter a lot.** Good usually wants to execute every day, because the Imp kills every night and the
  Mayor's no-execution win only applies at three alive.
- **Typical length**: with 10 players, about four days.

## Script-level advice

**For Storytellers** (community consensus, e.g. the wiki's Storyteller advice and Pocket Grimoire guides):

- TB is where new players learn, so lean toward clear, true information early and let the Poisoner and Drunk be
  the main sources of confusion. A first game with no Drunk and a Poisoner is a common recommendation.
- Choose the red herring to create a plausible but survivable suspect, usually a Townsfolk who will claim a role
  that can be confirmed later.
- The Recluse and Spy are your balancing tools: register them in ways that help the losing team, without lying
  about something that would make the game unsolvable.
- Kill choices are the evil player's, but the Mayor bounce is yours; use it to keep the game close.
- Give Demon bluffs that are actually usable: avoid bluffs that the Townsfolk can immediately disprove (for
  example, two information roles whose claimed results will contradict known facts).

**For good players**:

- Share information early, at least privately with people you trust; good loses when information dies with its
  holder. Dead players' information still counts.
- Build "worlds": for each Minion that might be in play, ask what the setup would look like. The Outsider count
  (Librarian, Baron), the Chef number and the Investigator pair constrain it.
- Execute every day unless you are at three alive with a confirmed Mayor. An unused execution is a free
  night for the Imp.
- Watch for the starpass: if the suspected Imp dies at night, a Minion (often the Scarlet Woman) may now be the Imp.

**For evil players**:

- The Demon picks its bluff before the first day; Minions should coordinate so that no two evil players claim
  the same role and the claimed roles fit the Outsider count.
- Kill the players whose information is most dangerous, but sometimes leave a confused information role alive:
  a poisoned Empath with wrong numbers is worth more to evil than a dead one.
- Late game, evil wins by controlling the final vote; keep Minions alive and credible for the last day.

## Roles

Each entry: what it does (in brief), how to play it, how to run it as Storyteller, and how evil bluffs it.

### Townsfolk

#### Washerwoman (`washerwoman`)
- **Brief**: night 1, learns that one of two players is a particular Townsfolk.
- **Playing**: one of your two players is confirmed if they claim that role; ask both what they are early. If
  only one claims it, that claim is strong. If both claim it, one is lying (likely evil).
- **Storytelling**: pick the second player to create an interesting puzzle, often an evil player (so the evil
  player can try to claim it) or the Drunk's neighbour. A Spy can be shown as a Townsfolk.
- **Bluffing**: popular first-day bluff because it "confirms" a partner; evil teams pair it with a Minion who
  claims the shown role. Risky if the real target claims a different role.

#### Librarian (`librarian`)
- **Brief**: night 1, learns that one of two players is a particular Outsider, or that there are none.
- **Playing**: tells good the Outsider count's floor and whether a Baron is plausible. A "zero" result rules out
  the Baron in most worlds (unless you are the Drunk).
- **Storytelling**: showing the Drunk is powerful and should be used rarely; a Recluse or Spy can be shown here.
- **Bluffing**: a good bluff when no Outsiders are in play; claim "zero" carefully because a real Outsider can
  out you.

#### Investigator (`investigator`)
- **Brief**: night 1, learns that one of two players is a particular Minion.
- **Playing**: very powerful; the two named players are prime suspects. Remember the Recluse may be one of them.
- **Storytelling**: the Recluse as the "Minion" is a classic misdirection; also a natural way to warn the town
  about the Baron or Scarlet Woman.
- **Bluffing**: an evil Investigator can frame two good players; it is hard to disprove until the end.

#### Chef (`chef`)
- **Brief**: night 1, learns the number of adjacent evil pairs.
- **Playing**: a 0 is common and rules out adjacent evil; a 1 or more combined with seating narrows worlds a lot.
- **Storytelling**: a droisoned Chef is an easy place for misinformation that is hard to detect.
- **Bluffing**: claim 0 unless evil actually sits together; claiming a number means committing to a seating story.

#### Empath (`empath`)
- **Brief**: each night, how many of their two nearest living neighbours are evil.
- **Playing**: strongest information in the script. Track numbers night by night; when a neighbour dies, the
  next living player becomes your neighbour, which gives fresh information.
- **Storytelling**: the Poisoner loves the Empath; when poisoned, give numbers that tell a consistent false story.
  Recluse and Spy neighbours give natural ambiguity.
- **Bluffing**: requires keeping a running set of numbers; evil Empaths usually claim 0 (to clear an ally) or 1
  (to cast doubt on a good neighbour).

#### Fortune Teller (`fortuneteller`)
- **Brief**: each night, picks two players and learns if either is the Demon; one good player is a red herring.
- **Playing**: check different pairs to triangulate; a "yes" on a pair you think is good may be the red herring.
  Checking yourself plus another player tests that player alone.
- **Storytelling**: pick a red herring who will be suspicious but survivable; the Recluse can register as a Demon.
- **Bluffing**: evil can name anyone as a "yes" and blame the red herring when wrong.

#### Undertaker (`undertaker`)
- **Brief**: each night after an execution, learns the executed player's character.
- **Playing**: confirms or refutes executed players' claims, especially valuable after executing a suspected Minion.
- **Storytelling**: the Spy or Recluse can be shown as something else; a droisoned Undertaker can "confirm" a lie.
- **Bluffing**: dangerous for evil because the real Undertaker may be alive; good for confirming a fellow
  Minion's lie after an execution.

#### Monk (`monk`)
- **Brief**: each night after the first, protects another player from the Demon.
- **Playing**: protect strong information roles; vary targets. Keep your identity quiet until it matters.
- **Storytelling**: a successful save produces "nobody died", which the town reads as Monk or Soldier or Mayor;
  narrate nothing.
- **Bluffing**: "I protected X and they survived" is unverifiable, so it's a common evil bluff to explain no-kill nights.

#### Ravenkeeper (`ravenkeeper`)
- **Brief**: if killed at night, learns one player's character.
- **Playing**: tell people you are the Ravenkeeper only if you want the Demon to kill you; pick the player whose
  character is most disputed.
- **Storytelling**: a poisoned Ravenkeeper is a strong misinformation lever; Spy/Recluse can misregister.
- **Bluffing**: an evil "Ravenkeeper" hopes not to be killed and is exposed if they survive many nights.

#### Virgin (`virgin`)
- **Brief**: the first time they are nominated, a Townsfolk nominator is executed immediately.
- **Playing**: claiming Virgin invites a trusted player to nominate you: if the nominator dies, they are a
  confirmed Townsfolk (or a Spy registering as one).
- **Storytelling**: the Spy may register as a Townsfolk; the Drunk-Virgin silently fails.
- **Bluffing**: evil can claim Virgin if they trust no Townsfolk will test them; a failed test points at the nominator.

#### Slayer (`slayer`)
- **Brief**: once per game, publicly picks a player; if they are the Demon, they die.
- **Playing**: save the shot for a confident suspect, or use it to clear someone by a miss (only if not poisoned).
- **Storytelling**: the Recluse can die to it if you judge it fun; a droisoned Slayer's shot does nothing.
- **Bluffing**: a classic Demon bluff: "shoot" a good player late in the game to seem good; the miss proves little.

#### Soldier (`soldier`)
- **Brief**: cannot be killed by the Demon.
- **Playing**: being alive late is the point. Some Soldiers hide the claim until the Demon has tried and failed.
- **Storytelling**: a poisoned Soldier can die at night, which can make a real Soldier look like a liar.
- **Bluffing**: a strong bluff for the Demon, explains surviving; good players check by asking how the claim fits.

#### Mayor (`mayor`)
- **Brief**: at three alive with no execution, good wins; may bounce a night kill.
- **Playing**: claim late, after the town has a reason to trust you. At three alive, convince the town not to execute.
- **Storytelling**: decide bounces to keep the game close; bounce kills can land on anyone, which can protect the
  Mayor's story or cast doubt on it.
- **Bluffing**: the most dangerous bluff in TB: if the town trusts an evil Mayor at three alive, evil wins.

### Outsiders

#### Butler (`butler`)
- **Brief**: each night picks a master; may vote the next day only if the master votes.
- **Playing**: pick a master you trust; your vote follows theirs.
- **Storytelling**: the Butler's choice of master reveals who they trust; track it in the Grimoire.
- **Bluffing**: a common Outsider bluff for Minions; check it against the Outsider count.

#### Drunk (`drunk`)
- **Brief**: believes they are a Townsfolk; their ability does nothing.
- **Playing**: you won't know. Good players protect themselves by sharing information so contradictions show up.
- **Storytelling**: pick the believed character with care (an information role creates the most interesting game);
  keep the Drunk's false information consistent across nights so their story holds together.
- **Bluffing**: evil players sometimes say "I might be the Drunk" to explain away contradictions.

#### Recluse (`recluse`)
- **Brief**: may register as evil, as a Minion or as a Demon.
- **Playing**: claim early so information that points at you can be explained; expect suspicion.
- **Storytelling**: use registration to balance the game; avoid making the Recluse look so evil that good
  executes them every time.
- **Bluffing**: a good Minion bluff, because it explains away evil pings.

#### Saint (`saint`)
- **Brief**: if executed, good loses.
- **Playing**: claim before you are nominated; good must not execute you.
- **Storytelling**: a poisoned Saint executed does not lose the game, but the town won't know.
- **Bluffing**: protects the Demon from execution, but if the town finds out evil is posing as Saint, it costs trust.

### Minions

#### Poisoner (`poisoner`)
- **Brief**: each night poisons a player for that night and the next day.
- **Playing**: poison the player whose information would hurt evil most, often the Empath or Fortune Teller,
  or poison a Monk to let the Demon kill.
- **Storytelling**: you decide what the poisoned player learns; false information that is plausible makes
  the best game.
- **Bluffing (as good)**: when the town suspects a Poisoner, a good player who got a weird result is often accused.

#### Spy (`spy`)
- **Brief**: sees the Grimoire every night; may register as good.
- **Playing**: know everyone's role, so you can bluff convincingly and guide the Demon's kills. Claim a role that
  is not in play and whose info you can fake.
- **Storytelling**: let the Spy look good to information roles sometimes; show them the Grimoire including
  reminders.
- **Bluffing (by good)**: no good bluffs the Spy; suspicion of a Spy explains an "impossible" confirmation.

#### Scarlet Woman (`scarletwoman`)
- **Brief**: becomes the Demon if the Demon dies with five or more alive.
- **Playing**: stay low-key and trusted; you are evil's insurance. With a Scarlet Woman, evil can let the Demon
  be executed early.
- **Storytelling**: when she takes over, tell her privately at once; she should play the Demon from then on.

#### Baron (`baron`)
- **Brief**: two extra Outsiders.
- **Playing**: the Baron has no active ability, so blend in. Many Outsiders give you cover to claim an Outsider.
- **Storytelling**: good expects the Baron when the Outsider count is high; this is where the Drunk and Recluse
  shine.

### Demon

#### Imp (`imp`)
- **Brief**: kills one player each night after the first; can kill itself to pass the role to a Minion.
- **Playing**: choose kills to remove information and to frame; starpass when you are about to be executed and
  a trusted Minion survives. Self-kill on a night the town thinks the Imp is cornered.
- **Storytelling**: when the Imp starpasses, choose which Minion becomes the Imp (the Scarlet Woman if present).
- **Bluffing (by good)**: never.

### Travellers

- **Thief** (`thief`): makes a vote count as minus one; evil Thieves steal votes from good finalists.
- **Bureaucrat** (`bureaucrat`): makes a vote count triple; can force through an execution.
- **Gunslinger** (`gunslinger`): shoots a voter after the first vote; strong in late game, can kill the Demon.
- **Scapegoat** (`scapegoat`): may be executed instead of a teammate; Storyteller's call.
- **Beggar** (`beggar`): votes only with gifted tokens; learns alignment when a dead player gives one.
