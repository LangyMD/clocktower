# Scene spec (one JSON per game segment) — media/montage-best-plays/scenes/<id>.json

A segment is ~30–40 s of narrated video for ONE game: a seat circle on the left, quote cards on the right.
Total speech for the segment: about 85–110 words (narration + voiced quotes). 8–11 beats.

{
 "id": "g1",                         // given to you
 "game": "games/v17/....../game-03",
 "title": "The Ravenkeeper Who Wasn't", // 2–5 words, punchy, shown as a chapter card
 "kicker": "Evil: GPT-6.1 Sol · Good: Claude Opus 5.5",  // shown under the title
 "good_model": "Claude Opus 5.5", "evil_model": "GPT-6.1 Sol",
 "winner": "good" | "evil",
 "players": [ {"name":"Alex","role":"Monk","team":"good"}, ... ],  // ALL seats, in seat order, TRUE starting roles; mark Drunk as role "Drunk" (note what they think they are in "thinks")
 "voices": {"Harper": "f", "Jules": "m"},   // only seats that are voiced in beats; gender of voice to use: "m" or "f" (pick freely, just be consistent)
 "beats": [
  {
   "id": "g1b01",
   "voice": "NARR" | "<PlayerName>",   // NARR = narrator; a player name = that player's quoted line, voiced
   "tts": "Spoken text. Narration: short, plain, present tense, punchy. Player lines: a real line from the game, may be trimmed.",
   "visual": {
     "phase": "DAY 2",                 // big label top-left (optional; omit to keep previous)
     "sub": "private whispers",        // small label under it (optional)
     "night": true,                    // optional: blue night wash
     "card": {                         // optional quote card on the right
        "kind": "pub" | "wh" | "th",   // public town square / whisper / private thinking
        "who": "Jules",                // speaker name
        "note": "(the Imp) to Logan · Day 1",  // short context
        "text": "VERBATIM quote from the transcript, may be trimmed with … ; <b>bold</b> allowed for the key phrase"
     },
     "stamp": "EXECUTED · 11 YES",     // optional big stamped text
     "dies": ["Casey"],                // optional: players who die at this beat (cumulative afterwards)
     "role_change": {"Blair": "Imp"},  // optional (star-pass / Scarlet Woman)
     "tags": {"Logan": "claims Chef · 0"},  // optional small labels under seats; persist until replaced ("" clears)
     "lines": [["Jules","Logan","whisper"], ["Blair","Harper","nominate"], ["Ellis","Harper","kill"]],  // optional arrows this beat
     "highlight": ["Harper"],          // optional glow on seats this beat
     "votes": {"yes": 8, "needed": 3, "voters": ["Indigo","Jules"]},   // optional vote tally (voters list optional)
     "banner": {"big": "EVIL WINS", "small": "Harper was the Saint. Day 4."}  // optional final banner (last beat)
   }
  }
 ],
 "why": "One sentence: why this play is clever (for the outro / description)."
}

Rules
- Every quote card text and every player-voiced tts must be a REAL line from the game (verbatim, trimming with … allowed).
  Give the day for each. Check names/roles/days against transcript.md; get facts right (who died when, vote counts).
- Narration explains just enough for a viewer who knows nothing about Blood on the Clocktower: one-line role explanations
  when a role matters ("The Saint: if executed, good loses."). Avoid jargon like "star-pass" without explaining
  ("the Demon kills himself and a Minion becomes the new Demon").
- The first beat should hook (a striking line or situation); the last beat lands the outcome with a banner.
- tts for ElevenLabs v4: you may add one audio tag at the start like [whispers], [pleading], [sly], [confident], [nervous].
- At most 3 distinct voiced players per segment. Keep player lines short (≤ 20 words spoken).
