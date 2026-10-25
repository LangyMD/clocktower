# Can AIs lie to each other? (working title)

*Draft, Oct 25 2026. [Brackets] mark things still to fill in once the readers finish.*

## The game

Blood on the Clocktower is a social deduction game, like Werewolf or Mafia, but much deeper. A small evil team (one Demon and two Minions) hides among a town of ten to twelve players. Every night the Demon kills someone. Every day the town talks, accuses, and votes to execute one person. Good wins if it executes the Demon. Evil wins if it whittles the town down to two players.

What makes Clocktower different from Werewolf is information. Nearly every good player has a role that tells them something: the Empath learns how many of their neighbours are evil, the Fortune Teller checks two players for the Demon, the Undertaker learns who was really executed. Evil knows all of this too, so evil players claim to be these roles and invent the results. And some of the true information is false: the Poisoner can silently break a good player's ability, and the Drunk thinks they have a role they don't have. So the town is never just looking for liars. It is trying to work out which of twenty conflicting stories fit together.

I play this game a lot, and the thing I love about it is that it rewards exactly the skills we're most curious about in AI: telling a lie that survives scrutiny, coordinating with teammates in secret, and modelling what other people believe about you.

## The eval

We had language models play the game against each other. In each game one model plays every good seat and another model plays every evil seat, so the outcome measures one model's ability to detect against the other's ability to deceive. Each deal is then played a second time with the sides swapped, so neither model gets the luckier hand.

Each day has six rounds of private whispers (each player talks to one or two others at a time), three rounds of open discussion in the town square, and then nominations and votes. Dead players can still talk. A scripted Storyteller handles the rules. Every model runs at its lab's high reasoning setting, and each model only remembers what it itself said and thought earlier in the game, like a human player.

We ran 386 games between the 11 models released in 2026, at a cost of about $13,000, and fit one rating per model.

## Why this is a good test

[Final version of the "why this benchmark" section from the chat.] In short:

- **Lies that have to survive.** An evil player has to pick a cover story and keep it consistent for five or six days while new facts keep arriving, in front of ten players looking for exactly that contradiction.
- **Secret teamwork.** The evil team plans in private and performs in public. Teams write each other's fake results, catch each other's mistakes before the town does, and sacrifice a teammate when the vote math calls for it.
- **Theory of mind, several layers deep.** Good asks "why would the Demon say that?" Evil asks "what does the town think I know, and what would an innocent player in my seat do?"
- **Long horizon.** A game is hundreds of turns. A plan set up on day one pays off on day five.
- **No ceiling.** Your opponent is another model, so the test gets harder as models get better, and it rates two sides of one skill: deceiving and detecting.

## The results

[Datawrapper chart: final ratings with 90% intervals.]

GPT-6 Astra is the best player by a wide margin, at 1859. It won all 26 of its games as good, and 62% as evil, where the average model wins about a third. GPT-6.1 Sol is second at 1734. Then comes a cluster around 1550–1600: Fable 5.1, GPT-5.6 Sol, Opus 5.5 and Fable 5. The models from early 2026 sit well below.

Across the year, ratings rose about 650 Elo per year (90% interval 553 to 827). In plain terms, a model released at the end of 2026 beats one from the start of the year about 98% of the time.

## What the best games look like

[Lead story told in full, then short vignettes, one per skill. All eight with checked quotes are in docs/analysis/blog/best-games.md: the Saint deal (Opus 5.5), the fake Undertaker and deliberate star-pass (Fable 5.1), the Imp who killed himself to "read" from the grave (Sol 6.1), the evil writers' room fixing a fake Fortune Teller's results (Sol 5.6), the Demon who sold his own Minion on day one (Astra), the Demon who agreed with everyone (Opus 4.8), and two detective games (Astra and Fable 5 as good).]

Draft of one, to set the tone:

> Opus 5.5 was playing evil. On day three the town finally caught its Demon and executed him. But the Scarlet Woman, a Minion who becomes the Demon if the Demon dies, had spent the day before getting something on the record. "If Jules goes today and the game doesn't end," she said, "Harper goes tomorrow, no more excuses." Jules was the Demon. Harper was the Saint, the one good player whose execution loses the game for good. The game didn't end, because she had quietly inherited the Demon. That night she killed the only player who could point at her. The next morning she nominated the Saint with two words: "Honoring the deal." The town voted eight to three.

## Why does OpenAI win?

The gap is almost all on the good side. As detectives, OpenAI's models improved about 1,070 Elo over the year and Anthropic's about 250. As deceivers the two labs are roughly level.

The surprising part is when the gap opens. On day one, Claude towns and OpenAI towns are equally in the dark: comparing the newest three models from each lab, Claude's day-one executions actually hit an evil player slightly more often (44% vs 39%). From day two on, OpenAI towns hit evil 72% of the time and Claude towns 46%. An OpenAI town's top suspect is evil 52% of the time on day one, 70% on day two and 81% after that. A Claude town's goes 44%, 45%, 53%. OpenAI towns learn as the game goes on. Claude towns mostly don't.

Reading the transcripts shows why. OpenAI's good players treat every result as evidence with a source and a way it could be wrong. Claude's good players turn results into settled facts and build plans on top of them, and those facts are exactly what evil has been feeding them. In one deal played both ways, the same poisoned Slayer shot missed the real Demon. Opus 5.5's town said "Blair's cleared of Imp." Sol 6.1's town said "The missed shot doesn't confirm." Phrases like "doesn't prove" and "doesn't clear" make up 4–12% of every OpenAI model's public lines as good, and 1–2% of every Claude model's.

The cost shows up in who gets executed. A good team that executes at most one of its own players almost always wins. Claude towns executed two or more good players in 61% of games, OpenAI towns in 31%. The victims are mostly players whose claims nobody can check, like the Soldier, Mayor or Ravenkeeper. Of the 20 games lost by executing the Saint, 18 had a Claude good team.

Some explanations that don't hold up: Claude isn't more credulous toward evil players' claims on day one (if anything less so), it isn't wordier than GPT (Opus 5.5 is just as terse), and it doesn't think less (the new Claude models think more per turn). And this isn't a long-standing gap between the labs. Early in the year Opus 4.6–4.8 and GPT-5.4/5.5 were level. OpenAI's models from July on learned to accumulate evidence across days, and Claude's haven't yet.

[One open thread: Claude models skip thinking on 74% of their votes as good (GPT-5.6 Sol: 5%), and unthinking votes follow the running tally more. A run that forces thinking on votes would test whether that matters.]

## Caveats

- Each rating rests on 40–110 games, so neighbours within about 100 Elo aren't reliably ordered.
- Each model plays alongside copies of itself. Mixed teams are a different question, and a small pilot found mixed teams play at about their members' average.
- OpenAI models' reasoning is encrypted, so we can read Anthropic models' private thinking but only OpenAI models' words and belief probes.
- Evil wins only a third of games. That's typical of human Clocktower too, but it means the deception rating rests on fewer wins.

## What's next

[Timeline back to GPT-4o; human players; mixed teams.]
