#!/usr/bin/env python3
"""24/7 streamer: loop the rendered playlist to YouTube Live (RTMP) with ffmpeg, forever.

Environment:
  YOUTUBE_STREAM_KEY   the stream key from YouTube Studio (Go live -> Stream)            [required unless RTMP_URL]
  RTMP_URL             full RTMP URL instead (testing, or another service); overrides the key
  HF_TOKEN             read access to the dataset dwarkesh/clocktower-games (it is private)
  HF_REPO              default dwarkesh/clocktower-games;  HF_PREFIX default media/stream
  MEDIA_DIR            where the MP4s are kept (default /data/stream)
  REFRESH_HOURS        re-sync the playlist from HF and restart this often (default 24; 0 = never)
  LOCAL_ONLY=1         skip the HF sync and play whatever is already in MEDIA_DIR

The episodes are pre-encoded for streaming (H.264 high, 1080p30, 2 s GOP, ~3-4.5 Mbps; AAC 128k 44.1 kHz), so ffmpeg
only remuxes (-c copy): almost no CPU, and a small always-on machine is enough. ffmpeg reads in real time (-re),
plays the concat list in a loop (-stream_loop -1), and is restarted with backoff if it ever exits.
"""
import os, signal, subprocess, sys, time
from pathlib import Path

MEDIA = Path(os.environ.get("MEDIA_DIR", "/data/stream"))
REPO = os.environ.get("HF_REPO", "dwarkesh/clocktower-games")
PREFIX = os.environ.get("HF_PREFIX", "media/stream")
REFRESH = float(os.environ.get("REFRESH_HOURS", "24"))


def log(*a):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)


def sync():
    """Download playlist.txt and every file it lists (skips files already present with the same size)."""
    if os.environ.get("LOCAL_ONLY"):
        return
    from huggingface_hub import snapshot_download
    MEDIA.mkdir(parents=True, exist_ok=True)
    tmp = snapshot_download(REPO, repo_type="dataset", allow_patterns=[f"{PREFIX}/*"], local_dir=str(MEDIA.parent / "hf"),
                            token=os.environ.get("HF_TOKEN"))
    src = Path(tmp) / PREFIX
    for f in src.iterdir():
        dst = MEDIA / f.name
        if not dst.exists() or dst.stat().st_size != f.stat().st_size:
            if dst.exists() or dst.is_symlink(): dst.unlink()
            dst.symlink_to(f.resolve())
    log("synced", len(list(src.iterdir())), "files from", REPO, PREFIX)


def playlist():
    """The concat list, keeping only entries whose file exists (so a half-synced folder still streams)."""
    src = MEDIA / "playlist.txt"
    if src.exists():
        names = [l.split(" ", 1)[1].strip() for l in src.read_text().splitlines() if l.startswith("file ")]
    else:
        names = sorted(p.name for p in MEDIA.glob("*.mp4"))
    names = [n for n in names if (MEDIA / n).exists()]
    if not names:
        raise SystemExit(f"nothing to play in {MEDIA}")
    out = MEDIA / "loop.ffconcat"
    out.write_text("ffconcat version 1.0\n" + "".join(f"file '{(MEDIA / n).resolve()}'\n" for n in names))
    return out, len(names)


def target():
    if os.environ.get("RTMP_URL"):
        return os.environ["RTMP_URL"]
    key = os.environ.get("YOUTUBE_STREAM_KEY")
    if not key:
        raise SystemExit("set YOUTUBE_STREAM_KEY (or RTMP_URL)")
    return "rtmp://a.rtmp.youtube.com/live2/" + key


def command(lst, url):
    fmt = "flv" if url.startswith("rtmp") else ("mpegts" if url.endswith(".ts") else "flv")
    return ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-stats_period", "60",
            "-re", "-stream_loop", "-1", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-map", "0:v:0", "-map", "0:a:0", "-c", "copy",
            "-flvflags", "no_duration_filesize", "-f", fmt, url]


def main():
    stop = {"flag": False}
    signal.signal(signal.SIGTERM, lambda *a: stop.update(flag=True))
    backoff = 5
    while not stop["flag"]:
        try:
            sync()
        except Exception as e:
            log("sync failed (playing what is on disk):", e)
        lst, n = playlist(); url = target()
        log(f"streaming {n} files in a loop to", url.rsplit("/", 1)[0] + "/<key>")
        started = time.time()
        p = subprocess.Popen(command(lst, url))
        while p.poll() is None and not stop["flag"]:
            time.sleep(5)
            if REFRESH and time.time() - started > REFRESH * 3600:
                log("refresh: restarting with a fresh playlist"); p.terminate(); p.wait(30); break
        if stop["flag"]:
            p.terminate(); break
        code = p.returncode
        if time.time() - started > 600: backoff = 5
        log(f"ffmpeg exited ({code}); restarting in {backoff}s")
        time.sleep(backoff); backoff = min(backoff * 2, 120)


if __name__ == "__main__":
    main()
