"""Collect every spoken clip of the montage into clips.json (ids, voices, text)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
NARR = "JBFqnCBsd6RMkjVDRZzb"  # George
POOL = {"m": ["N2lVS1w4EtoT3dr4eOWO", "iP95p4xoKVk53GoZ742B", "cjVigY5qzO86Huf0OWal", "nPczCjzI2devNBz1zQrb",
              "CwhRBWXzGAHq8TQ4Fs17", "bIHbv24MWmeRgasZH58o", "pNInz6obpgDQGcFmaJgB"],
        "f": ["pFZP5JQG7iQjIQuC4Bku", "EXAVITQu4vr4xnSDxMaL", "XrExE9yKIg1WjnnlVkGX", "cgSgspJ2msm6clMCkdW9",
              "Xb7hH8MSUJpSbSDYk0k2", "hpp4J3VqNfWAUOO0d1Us", "FGY2WhTYpPnrIDTdsKH5"]}
ORDER = json.load(open(os.path.join(D, "order.json")))
def segments():
    for s in ORDER:
        p = os.path.join(D, "scenes", s + ".json")
        yield json.load(open(p))
clips = []
for seg in segments():
    used = {"m": 0, "f": 0}; vmap = {}
    for name, g in seg.get("voices", {}).items():
        vmap[name] = POOL[g][used[g] % len(POOL[g])]; used[g] += 1
    if seg.get("title") and seg.get("kind", "game") == "game":
        clips.append({"id": seg["id"] + "t", "voice": NARR, "tts": seg.get("title_tts", seg["title"] + "."), "speed": 1.0})
    for b in seg["beats"]:
        v = NARR if b["voice"] == "NARR" else vmap[b["voice"]]
        clips.append({"id": b["id"], "voice": v, "tts": b["tts"], "speed": b.get("speed", 1.1 if b["voice"] == "NARR" else 1.05)})
json.dump(clips, open(os.path.join(D, "clips.json"), "w"), indent=1)
print(len(clips), "clips,", sum(len(c["tts"].split()) for c in clips), "words")
