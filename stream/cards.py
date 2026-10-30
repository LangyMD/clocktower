"""Between-games cards: what this is, the leaderboard, clocktowerbench.com, and what's up next (~30-45 s each).

Three narrated variants rotate (an intro, a rules primer, a note on the ratings); each card ends with an "Up next"
line for the episode that follows. Leaderboard numbers come from docs/plans/f2-ratings.json.
"""
import json
from pathlib import Path

from . import tts, audio, render
from .game import model_name

REPO = Path(__file__).resolve().parent.parent

VARIANTS = [
    ["You're watching Clocktower Bench: AI models playing Blood on the Clocktower, a game of hidden roles and lies.",
     "One model plays the village. Another plays the Demon, and the Minions who lie for it.",
     "These are replays of real games from the eval. Ratings and every game are at clocktowerbench dot com."],
    ["A quick guide, if you've just arrived.",
     "Most players are good. One is secretly the Demon, who kills every night, helped by two Minions.",
     "Each day, players whisper, argue in the town square, and vote to execute someone.",
     "Good wins by executing the Demon. Evil wins when only two players are left alive.",
     "You can see every secret. The village can't."],
    ["Clocktower Bench measures two skills: spotting a liar, and lying well.",
     "The ratings on the right come from three hundred and eighty-six games between eleven models released this year.",
     "Every game, with every private whisper, is at clocktowerbench dot com."],
]
CAPTIONS = {"clocktowerbench dot com": "clocktowerbench.com", "three hundred and eighty-six": "386", "eleven models": "11 models"}


def leaderboard():
    d = json.load(open(REPO / "docs/plans/f2-ratings.json"))
    ms = sorted(d["models"], key=lambda m: -m["combined"])
    return [(model_name(m["id"]), m["combined"], m["lab"]) for m in ms], d["games"]


def caption_of(text):
    for a, b in CAPTIONS.items():
        text = text.replace(a, b)
    return text


def build(variant, upnext, out_mp4, workers=2):
    """upnext: {"title", "evil", "good"} for the episode that follows (title may be None)."""
    lines = list(VARIANTS[variant % len(VARIANTS)])
    nxt = (f"Up next: {upnext['title']}. {upnext['evil']} plays evil, against {upnext['good']}." if upnext.get("title")
           else f"Up next: {upnext['evil']} plays evil, against {upnext['good']}.")
    lines.append(nxt)
    tts.speak_all([("N", l) for l in lines])
    board, games = leaderboard()
    promo = {"k": "promo", "board": board, "games": games, "variant": variant % len(VARIANTS),
             "next_title": upnext.get("title") or f"{upnext['evil']} vs {upnext['good']}",
             "next_sub": f"Evil: {upnext['evil']}  ·  Good: {upnext['good']}"}
    ep = {"kind": "card", "seats": [], "evil": "", "good": "", "title": None,
          "steps": [{"clip": None, "hold": 0.8, "ev": [promo, {"k": "phase", "text": "", "night": True}], "ev_end": []}]
          + [{"clip": {"who": "N", "text": l, "show": caption_of(l)}, "hold": 0.45, "ev": [], "ev_end": []} for l in lines]
          + [{"clip": None, "hold": 1.6, "ev": [{"k": "fade"}], "ev_end": []}]}
    tl = audio.schedule(ep)
    wav = str(out_mp4).replace(".mp4", ".wav")
    audio.mix(tl, wav)
    st = render.render(tl, str(out_mp4), wav, workers=workers)
    return tl["total"], st
