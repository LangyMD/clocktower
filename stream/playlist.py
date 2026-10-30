"""The stream's playlist: curated highlights first, then every other finished game ranked by an interestingness
score, with a between-games card before each episode.

    python3 -m stream.playlist rank [--top 40]          # the ranking, with the features behind each score
    python3 -m stream.playlist build [--episodes 10]    # render missing episodes + cards, write the concat list
    python3 -m stream.playlist upload                   # push MP4s and playlist.txt to HF media/stream/

Score (fixed in advance, from the logs only): longer games up to 6 days; close votes on the last two days;
star-passes and Scarlet Woman catches; Saint and Mayor endings; the good team's belief in the real Demon rising
past 50% and the game still being decided late (evil escaping, or good finally converging); minus games over by
day 2 and day-1/2 Slayer hits.
"""
import argparse, json, subprocess, sys
from pathlib import Path

from . import highlights, cards
from .game import Game, ROOTS
from .build import build as build_episode, episode_name, OUT

PATTERNS = ["v16/f2-*/game-*", "v17/f3-*/game-*", "v17/f3b-*/game-*", "v17/f4-*/game-*", "v17/f5-*/game-*",
            "v17/b1-*/game-*", "v17/b2-*/game-*"]
PL = OUT / "playlist"


def all_games():
    seen = {}
    for root in ROOTS:
        for pat in PATTERNS:
            for d in sorted(root.glob(pat)):
                if (d / "events.jsonl").exists() and (d / "result.json").exists():
                    rel = str(d).split("games/", 1)[1]
                    seen.setdefault(rel, d)
    return list(seen)


def score(rel):
    try:
        g = Game(rel)
    except Exception:
        return None
    r = g.result
    if r.get("stopped") or g.winner not in ("good", "evil"):
        return None
    f = {}
    f["days"] = min(g.days, 6)
    last = [e["data"] for e in g.events if e["kind"] == "vote_result" and e["day"] >= g.days - 1]
    f["close"] = 1.5 * sum(1 for v in last if abs(v["votes"] - v["needed"]) <= 1)
    f["handoff"] = 3 * sum(1 for e in g.events if e["kind"] == "becomes")
    reason = g.reason.lower()
    f["saint"] = 4 if "saint" in reason else 0
    f["mayor"] = 3 if "mayor" in reason or ("three" in reason and g.winner == "good") else 0
    sus = g.suspicion()
    def at(d, p):
        k = "dawn" if p == "dawn" else "nominations_open"
        return next((e["seq"] for e in g.events if e["day"] == d and e["kind"] == k), 10 ** 9)
    dem = [(d, p, m.get(g.demon_at(at(d, p)))) for d, p, m in sus]
    peak = max((v for _, _, v in dem if v is not None), default=0)
    lastv = next((v for _, _, v in reversed(dem) if v is not None), 0)
    f["escape"] = 3 if g.winner == "evil" and peak >= 0.5 else 0
    f["converge"] = 2 if g.winner == "good" and g.days >= 4 and lastv >= 0.5 and min((v for _, _, v in dem[1:] if v is not None), default=1) < 0.25 else 0
    slay = [e for e in g.events if e["kind"] == "slayer" and e["data"]["died"] and e["day"] <= 2]
    f["short"] = -5 if g.days <= 2 else 0
    f["slayer_dud"] = -4 if slay else 0
    return {"rel": rel, "score": round(sum(f.values()), 2), "f": f, "evil": g.team_models(True), "good": g.team_models(False),
            "winner": g.winner, "days": g.days}


def ranking():
    hl = [r for r, _, _ in highlights.HIGHLIGHTS]
    rows = [s for s in (score(r) for r in all_games() if r not in hl) if s]
    rows.sort(key=lambda s: (-s["score"], s["rel"]))
    return hl, rows


def order(n_extra=None):
    hl, rows = ranking()
    rest = [r["rel"] for r in rows if r["score"] >= 8]
    return hl + (rest if n_extra is None else rest[:n_extra])


def build(episodes, workers=4):
    PL.mkdir(parents=True, exist_ok=True)
    games = order()[:episodes]
    entries = []
    for i, rel in enumerate(games):
        name = episode_name(rel)
        mp4 = OUT / name / f"{name}.mp4"
        if not mp4.exists():
            build_episode(rel, workers=workers)
        meta = json.load(open(OUT / name / "meta.json"))
        card = PL / f"card-{i + 1:03d}-{name}.mp4"
        if not card.exists():
            cards.build(i, {"title": meta["title"], "evil": meta["evil"], "good": meta["good"]}, card, workers=2)
        entries += [card.name, f"{name}.mp4"]
    with open(PL / "playlist.txt", "w") as f:
        f.write("ffconcat version 1.0\n")
        for e in entries: f.write(f"file {e}\n")
    json.dump({"games": games, "files": entries}, open(PL / "playlist.json", "w"), indent=1)
    print(f"playlist: {len(games)} episodes, {len(entries)} files -> {PL / 'playlist.txt'}")


def upload():
    meta = json.load(open(PL / "playlist.json"))
    for fn in meta["files"]:
        src = PL / fn if fn.startswith("card-") else OUT / fn[:-4] / fn
        subprocess.run(["hf", "upload", "dwarkesh/clocktower-games", str(src), f"media/stream/{fn}", "--repo-type", "dataset"], check=True)
    for fn in ("playlist.txt", "playlist.json"):
        subprocess.run(["hf", "upload", "dwarkesh/clocktower-games", str(PL / fn), f"media/stream/{fn}", "--repo-type", "dataset"], check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["rank", "build", "upload"])
    ap.add_argument("--top", type=int, default=40); ap.add_argument("--episodes", type=int, default=10)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "rank":
        hl, rows = ranking()
        print("highlights:", *hl, sep="\n  ")
        for r in rows[:a.top]:
            print(f"{r['score']:5.1f}  {r['rel']:45s} {r['winner']:4s} d{r['days']}  {r['evil']} (evil) v {r['good']}  {r['f']}")
        print(len(rows), "ranked;", sum(1 for r in rows if r["score"] >= 8), "with score >= 8")
    elif a.cmd == "build":
        build(a.episodes, a.workers)
    else:
        upload()
