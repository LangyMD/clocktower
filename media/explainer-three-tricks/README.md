# Explainer: three tricks (Oct 2026)

~2 min Twitter video for the blog post: three games, each told as a puzzle (the problem the player faced, the
insight that solved it). Clean flat look: a ring of player tokens (the viewer sees evil in red; the village
doesn't), quote bubbles labelled with role and side, one recurring "village suspicion" meter from `probes.jsonl`,
and burned-in captions for every narrated line. Script and sources: `script.md`; data: `script.py`.

Pipeline (each step re-runnable; TTS is cached per clip):
1. `python3 script.py` -> `clips.json`; `python3 tts.py` (ElevenLabs eleven_v4 with character timestamps) -> `audio/`.
2. `python3 build.py` -> `tight/` (levelled speech, long pauses shrunk) and `timeline.json` (clip times, caption
   chunks timed to the words, visual events resolved from word anchors like `"@Demon"`).
3. `python3 mix.py` -> `mix.wav` (speech, quiet chord pad ducked under speech, soft vote ticks).
4. `node render.js stills 30 60 ...` to check frames in `test/`; `node render.js frames 4` -> `frames/` (~30 min).
5. `./encode.sh` -> `explainer-three-tricks.mp4` (HF dataset: `media/explainer-three-tricks.mp4`).
Voices: narrator Chris; Blair Lily; Ellis Roger. Font: Inter (system).
