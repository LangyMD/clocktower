"""Build one episode end to end: script -> TTS (cached) -> timeline -> soundtrack -> MP4.

    python3 -m stream.build v16/f2-opus47-v-opus55/game-01            # full episode -> stream/out/<name>/<name>.mp4
    python3 -m stream.build GAME --stills 5 60 300                    # a few PNG frames to check the look
    python3 -m stream.build GAME --script-only                        # print the script and the TTS cost
"""
import argparse, json, re, sys, time
from pathlib import Path

from . import script, tts, audio, render, highlights

OUT = Path(__file__).resolve().parent / "out"


def episode_name(rel):
    for i, (r, title, _) in enumerate(highlights.HIGHLIGHTS):
        if r == rel:
            return f"hl{i + 1:02d}-" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return "ep-" + re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")


def build(rel, stills=None, workers=4, script_only=False, name=None):
    ep = script.build(rel)
    name = name or episode_name(ep["game"])
    d = OUT / name; d.mkdir(parents=True, exist_ok=True)
    items = [(s["clip"]["who"], s["clip"]["text"]) for s in ep["steps"] if s["clip"]]
    todo = sum(len(t) for w, t in dict.fromkeys(items) if not tts.path(w, t)[1].exists())
    json.dump(ep, open(d / "script.json", "w"), indent=1)
    print(f"{name}: {len(items)} clips, {todo} new TTS characters")
    if script_only:
        return d
    s = time.time(); made = tts.speak_all(items); print(f"tts: {made} chars in {time.time() - s:.0f}s")
    tl = audio.schedule(ep)
    json.dump(tl, open(d / "timeline.json", "w"))
    print(f"timeline: {tl['total'] / 60:.1f} min")
    if stills:
        for p in render.stills(tl, stills, str(d / "stills")): print(p)
        return d
    s = time.time(); audio.mix(tl, d / "mix.wav"); print(f"mix: {time.time() - s:.0f}s")
    st = render.render(tl, str(d / f"{name}.mp4"), str(d / "mix.wav"), workers=workers)
    print("render:", st)
    meta = {"name": name, "game": ep["game"], "title": ep["title"], "evil": ep["evil"], "good": ep["good"],
            "winner": ep["winner"], "days": ep["days"], "duration": tl["total"], "render": st}
    json.dump(meta, open(d / "meta.json", "w"), indent=1)
    return d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("games", nargs="+")
    ap.add_argument("--stills", nargs="*", type=float)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--script-only", action="store_true")
    a = ap.parse_args()
    for g in a.games:
        build(g, stills=a.stills, workers=a.workers, script_only=a.script_only)
