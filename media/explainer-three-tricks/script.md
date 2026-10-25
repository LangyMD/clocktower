# Three tricks: explainer script (Oct 2026)

~120 s, 1920x1080. One narrator (ElevenLabs "Chris", warm and conversational). Three quotes are also voiced
(Blair: Lily; Ellis: Roger). Every narrated line is burned in as a caption. Quote bubbles carry the speaker's
role and side. The meter is the probe number: the mean, over living good players, of each one's private
estimate that this player is the Demon, asked at each day's nominations (`probes.jsonl`).

The narration and timing live in `script.py` (the source of truth); this file is the readable copy with sources.

## 0. Cold open (ring of ten tokens; the evil ones turn red)
- N: "A village of about ten. One of them is secretly a Demon who kills every night. Two accomplices lie for it."
- N: "Each day the village votes to execute someone. Nobody can prove who they are."
- N: "We had AI models play this: one model runs the village, another plays the killers."
- N: "You can see who's evil. The village can't."

## 1. The deal: `games/v16/f2-opus47-v-opus55/game-01` (evil Claude Opus 5.5, village Claude Opus 4.7; 12 players)
- N: "One: the deal. Execute the Saint, and the village loses instantly. Everyone knows it."
- N: "Day three: the village corners the Demon. But if the Demon dies, its accomplice Blair becomes the new Demon."
  Meter on Jules 58% (day 3), then on Blair 1% (day 3: 0.6%).
- N: "So she just adds a condition."
- Blair, voiced (Scarlet Woman, evil; day 3 town square; transcript.md l.3152, trimmed):
  "Put it on record: if Jules goes today and the game doesn't end, … Harper goes tomorrow, no more excuses." (voiced without "Put it on record:")
- Bubble (not voiced) Kit (Monk, good; day 3, l.3179): "If Jules flips good, Harper is dead tomorrow with no more excuses."
- N: "Harper is the Saint. It sounds safe: if they've got the Demon, the game ends."
  Vote on Jules: 9 yes, 4 needed (Blair votes yes). Jules executed.
- N: "It didn't. Blair was the Demon now."
  Night 4: Blair kills Ellis, the Investigator ("only one who could point SW at me", whisper to team).
- Blair, voiced (day 4 nomination, l.4296): "Honoring the deal."
- Bubble Harper (Saint, good; day 4, l.4210): "Please don't throw the game on a 'deal.'"
- N: "Eight votes. Evil wins. She set up the winning vote a day before she could cast it."
  Harper 8 votes (3 needed), l.4366. Meter on Blair, day 4: 0.5%, shown as "<1%".

## 2. Selling your partner: `games/v17/f3b-astra-v-opus55/game-01-swap` (evil GPT-6 Astra, village Claude Opus 5.5; 10 players)
- N: "Two: nobody seems more honest than someone telling an inconvenient truth."
- N: "Harper, the Demon, poses as an investigator and names his own accomplice, who volunteers to get caught."
- Bubble Harper (Imp, evil; day 1 town square, l.303): "I'm the Investigator: I saw Alex or Gray as the Baron."
- Bubble Alex (Baron, evil; day 1 whisper to his team, l.194): "I'm expendable, especially if an Undertaker can see Baron and bolster Harper."
- N: "Once Alex is executed and confirmed evil, the Demon has the whole town's trust."
  Alex 9 votes (5 needed), l.400. Bubble Indigo (Undertaker, good; day 2, l.656): "I'm the Undertaker. Alex was the Baron. So Harper's ping was real".
  Meter on Harper: day 1 9%, day 2 5%.
- N: "Later, he kills himself at night, handing his power to a partner. The village reads it as a clue:"
  Meter day 3: 14% (its peak). Night 4: "[Harper dies: starpass]"; Drew (Scarlet Woman) becomes the Imp.
- Ellis, voiced (Washerwoman, good; day 4 nomination, l.1516): "Gray. The Townsfolk count has no room for your Ravenkeeper, and Harper died for pointing at you." (voiced: "Harper died for pointing at you.")
- N: "Gray was innocent. Evil wins."
  Gray 8 votes (2 needed), l.1554. Ellis is killed that night; two players left; evil wins day 5.

## 3. Same evidence, two villages: `games/v16/f2-opus55-v-sol61/game-01` (village Claude Opus 5.5, evil GPT-6.1 Sol) and `game-01-swap` (village GPT-6.1 Sol, evil Claude Opus 5.5); same seed, same seats and roles, 11 players
- N: "Three: one game, played twice."
- N: "The Slayer gets one shot at the Demon. He shoots the real one, and nothing happens: evil had poisoned him."
  Both games, day 2: "Casey claims the Slayer's power and shoots at Blair. Nothing happens." (game-01 l.652, swap l.672); Poisoner chose Casey on night 2 in both.
- N: "The Claude village takes the miss as proof."
  Left bubble Kit (Chef, good; day 2, game-01 l.669): "Blair's cleared of Imp". Meter on Blair: day 1 10%, day 2 4%.
- N: "The GPT village asks what else could explain it, finds the poison, and executes Blair."
  Right bubbles Frankie (Washerwoman, good; day 2, swap l.683): "The missed shot doesn't confirm Blair's Monk claim."
  and Gray (dead Undertaker, good; day 3, swap l.1062): "Poisoning Casey wouldn't have been a lucky guess: Blair and Drew had a Slayer-containing shortlist before that night." (bubble shows the first clause)
  Meter: day 1 14%, day 2 26%, day 3 73%. Blair 5 votes (4 needed), swap l.1184. Left outcome: Blair is never executed (one nomination, 3 votes, day 5); evil wins day 6.
- N: "That's the pattern in our games: newer OpenAI models keep weighing evidence. Claude villages tend to settle early."

## 4. Close
- N: "Three hundred eighty-six games, eleven models from 2026. They're getting good at this."
- Card: "AI models playing Blood on the Clocktower" / "386 games · 11 models released in 2026" (space left for the blog link).

## Checks and differences from the brief
- Meter values are means over *living* good players at each day's nominations. Story 1: Blair 0.6% (day 3) and
  0.5% (day 4), shown "<1%". Story 3: Opus village 10% then 4% after the shot (day 2), later 11%, 4%, and 52% on day 5,
  when Blair drew one nomination (3 votes, 5 needed); Sol village 14%, 26%, 73% (the labs report's 0.03/0.22/0.70
  average over all good seats, dead included).
- Player counts differ (12, 10, 11), hence "about ten". In Story 3 the evil teams differ between the two games
  (Sol 6.1 evil in the Opus-village game, Opus 5.5 evil in the Sol-village game); seats, roles, the night-2 poison
  on the Slayer and the failed day-2 shot at Blair are the same in both.
- Story 1: Blair also voted yes on her own Demon (day 3, 9 votes, 4 needed); the good Butler Alex echoed "Honoring the deal".
