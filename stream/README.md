# Clocktower Bench: the 24/7 stream

An always-on YouTube stream (also embeddable on clocktowerbench.com) that loops condensed replays of games from
the eval: curated highlight games first, then every other finished game ranked by an interestingness score, with
a short between-games card (what this is, the leaderboard, the URL, what's next) before each episode.

Episodes are rendered offline from the game logs; the stream host only loops MP4s (`ffmpeg -c copy`), so it needs
almost no CPU and no API keys beyond YouTube and Hugging Face.

## Episodes (rendered here)
`python3 -m stream.build GAME` turns one game's logs into a 12-20 minute 1080p30 MP4:
1. `script.py` picks the moments (deterministic rules, verbatim excerpts cut at sentence boundaries) and writes
   the narration from templates filled with events (night actions, deaths, claims vs true roles, votes, the
   probe polls). Only the curated highlights (`highlights.py`) add a hand-written hook and pinned quotes, taken from
   the checked write-ups in `docs/analysis/`.
2. `tts.py` voices every line with ElevenLabs `eleven_v4` (narrator George; one fixed voice per seat name), cached by
   voice + text in `cache/tts/`, so repeated lines are free.
3. `audio.py` levels and tightens the speech, times every clip, caption and visual event (`timeline.json`), and
   mixes the soundtrack (speech, a quiet looping pad, a bell at nightfall, a thud for deaths, ticks for votes).
4. `render.py` draws frames with Pillow (no browser): cached sprites keyed by state, and a frame identical to the
   previous one is reused, so only ~10% of frames are drawn; 4 processes render chunks in parallel straight into
   ffmpeg (~100 fps on 4 vCPUs, i.e. a 13-minute episode in about 4 minutes).

What a viewer sees: the ring of seats (evil in red, the Demon thicker; true role beside each seat, plus the role it
claims in public), an amber arc per seat for the village's average P(Demon) from `probes.jsonl`, a right-hand panel
with the current quote (karaoke-highlighted as it is spoken), secret evil chat and Claude private thoughts on
red/purple cards, night summaries, polls and vote counts, and burned-in captions for the narrator. The end shows
the result and a chart of the village's suspicion over the game.

Useful commands:
```
python3 -m stream.dryrun v16/f2-opus47-v-opus55/game-01        # the script as text: what gets said and shown
python3 -m stream.build GAME --stills 30 300 600                # a few PNG frames to check the look
python3 -m stream.build GAME                                    # full episode -> stream/out/<name>/<name>.mp4
python3 -m stream.playlist rank --top 40                        # interestingness ranking of all finished games
python3 -m stream.playlist build --episodes 12                  # render what's missing + cards + playlist.txt
python3 -m stream.playlist upload                               # MP4s + playlist to HF media/stream/
```
Logs are read from `games/` (or `$CLOCKTOWER_GAMES`, or the main checkout). Outputs (`out/`) and the TTS cache
(`cache/`) are git-ignored. TTS spend: about 10k characters per new episode, 400 per card.

## State (Oct 30 2026)
The 12 curated highlights (`highlights.py`, 10-17 min each, 171 min in all) and 12 cards are rendered and uploaded
to HF `media/stream/` with `playlist.txt` (card, episode, card, episode, ...). Next: `python3 -m stream.playlist
build --episodes 30` adds the top-ranked other games (207 finished games score >= 8), then `upload`. Known gaps:
claim detection only catches "I'm (the) X", so some public claims never show on the ring; OpenAI models' private
reasoning is encrypted, so GPT episodes show their whispers but no thought cards; episodes average ~1.7 Mbps
(static frames), under YouTube's recommended 4.5 Mbps for 1080p, which may draw a Studio warning but streams fine.

## Streaming (the always-on host)
`streamer/stream.py` downloads `media/stream/` from the HF dataset, then runs

```
ffmpeg -re -stream_loop -1 -f concat -safe 0 -i loop.ffconcat -map 0:v:0 -map 0:a:0 -c copy -f flv \
       rtmp://a.rtmp.youtube.com/live2/$YOUTUBE_STREAM_KEY
```
and restarts it with backoff if it exits; once a day it re-syncs the playlist and restarts (a few seconds' gap).
The files are encoded the way YouTube asks (H.264 high, yuv420p, 30 fps, 2 s keyframe interval, ~3 Mbps average
and 4.5 Mbps peak; AAC 128 kbps 44.1 kHz stereo).

Run it on Fly.io (any small always-on Linux box works the same way):
```
cd stream/streamer
fly launch --no-deploy --copy-config --name clocktower-stream
fly volumes create data --size 20
fly secrets set YOUTUBE_STREAM_KEY=xxxx-xxxx-xxxx-xxxx HF_TOKEN=hf_...   # HF token with read access (dataset is private)
fly deploy
```
Or Render: a Background Worker from `stream/streamer/Dockerfile` (Docker context `stream/streamer`), a 20 GB disk
mounted at `/data`, and the same two environment variables. Or plain Docker:
```
docker build -t clocktower-stream stream/streamer
docker run -d --restart=always -v clocktower-data:/data -e YOUTUBE_STREAM_KEY=... -e HF_TOKEN=... clocktower-stream
```
YouTube side: YouTube Studio -> Go live -> Stream; copy the stream key; set the stream to not end automatically
(Settings -> "Enable auto-start" and "Enable auto-stop" off, DVR on); 1080p, "Normal latency".

Embed on clocktowerbench.com:
`<iframe src="https://www.youtube.com/embed/live_stream?channel=CHANNEL_ID&autoplay=1&mute=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>`
(CHANNEL_ID is the channel's `UC...` id; the embed always shows the channel's current live stream.)

Test without a key (what was done here): run a local RTMP sink and point the streamer at it.
```
ffmpeg -listen 1 -i rtmp://127.0.0.1:1935/live2/test -c copy sink.flv &
LOCAL_ONLY=1 MEDIA_DIR=stream/out/playlist RTMP_URL=rtmp://127.0.0.1:1935/live2/test python3 stream/streamer/stream.py
```
