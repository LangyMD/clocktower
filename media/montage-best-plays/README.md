# Montage: the best plays (Oct 2026)

~5.5 min video: intro, five games (three cunning/clever plays, then GPT-6 Astra hunting and hiding), outro.
Game picks come from `docs/analysis/astra/cunning-evil.md` and `good-strategy.md`; every quote is verbatim from the game logs.

Pipeline (each step re-runnable; TTS is cached per clip):
1. `scenes/<id>.json` — one segment each (schema: `SCHEMA.md`); `order.json` sets the order.
   `intro`, `astra`, `outro` are plain slides (`kind: plain`, each beat has `visual.html`).
2. `python3 build.py` → `clips.json` (voices: narrator George; players from male/female pools).
3. `python3 tts.py` (needs `ELEVENLABS_API_KEY`, model eleven_v4) → `audio/`.
4. `python3 tighten.py` (loudness, 1.1× tempo, shrink pauses) → `tight/`; `python3 schedule.py` → `timeline.json`.
5. `python3 mix.py` → `mix.f32` (speech, drone bed, bells/booms/vote knocks).
6. `node render.js stills T1 T2 …` to check frames; `node render.js frames 6` (~3 fps, ~55 min) → `frames/`.
7. `./encode.sh` → `montage-best-plays.mp4` (uploaded to HF `media/`).
Fonts: Cinzel + EB Garamond from Google Fonts into `fonts/` (git-ignored; see fetch snippet in git history).
