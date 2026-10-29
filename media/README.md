# Media: videos made from game logs

Three short videos were made from real games: every spoken line is a verbatim quote from the logs, read by
ElevenLabs voices over animated frames. The finished MP4s are in the Hugging Face dataset under `media/`; this
folder holds the pipelines that made them, so you can make your own from any game.

| Folder | Video | Length |
|---|---|---|
| [`trailer-f2-opus47-v-opus55/`](trailer-f2-opus47-v-opus55/) | One game: Opus 5.5's evil team vs Opus 4.7, the Scarlet Woman's "deal" that gets the Saint executed (`games/v16/f2-opus47-v-opus55/game-01`) | 65 s |
| [`montage-best-plays/`](montage-best-plays/README.md) | Five games of cunning plays, then GPT-6 Astra hunting and hiding | 5.5 min |
| [`explainer-three-tricks/`](explainer-three-tricks/README.md) | Three games told as puzzles, with a "village suspicion" meter from the belief probes | 2 min |

## How a pipeline works

All three follow the same steps (each folder's README gives its exact commands):

1. **Script.** Pick moments from a game's `events.jsonl` (and `probes.jsonl` for suspicion meters) and write
   them as clips: who speaks, the exact line, and what the screen shows (`script.json`, `scenes/*.json` or
   `script.py`).
2. **Voices.** `tts.py` sends each clip to ElevenLabs (model `eleven_v4`; needs `ELEVENLABS_API_KEY`) and caches
   the audio per clip, so reruns only pay for changed lines.
3. **Timing.** `tighten.py` / `build.py` level the speech and shrink long pauses with ffmpeg; `schedule.py` lays the
   clips on a timeline.
4. **Sound.** `mix.py` mixes speech with a quiet music bed and effects (numpy).
5. **Frames.** `render.js` drives `scene.html` in a headless browser (Playwright) to render each frame;
   `node render.js stills T1 T2` renders a few frames to check before the full run (which takes 30–60 minutes).
6. **Encode.** `encode.sh` joins frames and audio with ffmpeg.

Requirements: Python 3 with numpy, Node with Playwright (`npm i playwright && npx playwright install chromium`),
ffmpeg on the path (or `FFMPEG=/path/to/ffmpeg`), an ElevenLabs API key, and the game's logs
(`python -m clocktower fetch 'v16/f2-opus47-v-opus55'`). Generated audio, frames and video are not kept in git.
