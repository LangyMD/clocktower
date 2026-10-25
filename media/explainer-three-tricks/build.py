"""audio/ + script.py -> tight/<id>.f32 (levelled, pauses shrunk) and timeline.json (clips, captions, events)."""
import json, os, re, subprocess, numpy as np
import script as S
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
TEMPO = {"N": 1.08, "BLAIR": 1.06, "ELLIS": 1.04}
SR = 44100; WIN = 0.02; THR = -40; MAXGAP = 0.24
os.makedirs("tight", exist_ok=True)
CL = S.clips()

def process(c):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"audio/{c['id']}.mp3", "-af", ("atempo=%s," % TEMPO.get(c["who"], 1.0)) + "loudnorm=I=-16:TP=-1.5:LRA=11",
                          "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).copy(); w = int(WIN * SR); n = len(x) // w
    db = 20 * np.log10(np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12)); loud = db > THR
    idx = np.where(loud)[0]; first, last = max(idx[0] - 2, 0), min(idx[-1] + 4, n - 1)
    keep = np.zeros(n, bool); keep[first:last + 1] = True
    k = first                                   # shrink long silent runs to MAXGAP
    while k <= last:
        if not loud[k]:
            j = k
            while j <= last and not loud[j]: j += 1
            if (j - k) * WIN > MAXGAP:
                h = int(MAXGAP / WIN / 2); keep[k + h:j - h] = False
            k = j
        else: k += 1
    kept = np.where(keep)[0]
    y = np.concatenate([x[i * w:(i + 1) * w] for i in kept])
    f = int(0.01 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    y.astype(np.float32).tofile(f"tight/{c['id']}.f32")
    # map original time -> new time (window granularity)
    newpos = np.cumsum(keep) - 1
    def tmap(t):
        i = min(max(int(t / WIN), first), last)
        return float(max(newpos[i], 0) * WIN + (t - i * WIN if keep[i] else 0))
    tempo = TEMPO.get(c["who"], 1.0)
    return len(y) / SR, (lambda t: tmap(t / tempo))

def chunks(text):
    parts = re.findall(r"[^.!?:]+[.!?:]?", text)
    out = []
    for p in (p.strip() for p in parts if p.strip()):
        if out and len(out[-1]) + len(p) < 48 and not out[-1].endswith((".", "?", "!")): out[-1] += " " + p
        elif out and len(p) < 14 and len(out[-1]) + len(p) < 80: out[-1] += " " + p
        elif len(p) > 86:
            cut = [m.end() for m in re.finditer(r",", p)]
            cut = min(cut, key=lambda i: abs(i - len(p) / 2)) if cut else len(p) // 2
            out += [p[:cut].strip(), p[cut:].strip()]
        else: out.append(p)
    return out

clips, T = {}, 0.5
segs = []
for seg in S.SEGMENTS:
    sd = {k: v for k, v in seg.items() if k != "clips"}; sd["start"] = round(T, 3)
    if seg.get("title"): T += 1.1                       # title card holds before the first line
    for i, (cid, who, text) in enumerate(seg["clips"]):
        c = next(c for c in CL if c["id"] == cid)
        dur, tmap = process(c)
        al = json.load(open(f"audio/{cid}.json"))["alignment"]
        chars = "".join(al["characters"]); st = al["character_start_times_seconds"]
        assert chars == c["tts"], (cid, chars)
        q = who != "N"; T += 0.35 if q else 0
        rec = {"id": cid, "seg": seg["id"], "who": who, "start": round(T, 3), "dur": round(dur, 3), "end": round(T + dur, 3),
               "text": c["tts"], "chartime": [round(T + tmap(s), 3) for s in st]}
        cap = c["caption"]
        if cap:
            caps = []; pos = 0
            for ch in chunks(cap):
                j = cap.index(ch, pos); pos = j + len(ch)
                k = j if cap == c["tts"] else int(j / len(cap) * len(c["tts"]))
                caps.append({"text": ch, "start": rec["chartime"][k]})
            for a, b in zip(caps, caps[1:] + [None]): a["end"] = b["start"] if b else rec["end"] + 0.15
            rec["captions"] = caps
        clips[cid] = rec
        last = i == len(seg["clips"]) - 1
        T += dur + (0.35 if q else 0) + (1.2 if last else 0.24)
    sd["end"] = round(T, 3); segs.append(sd)
total = round(T + 2.0, 3)

def anchor(cid, at):
    c = clips[cid]
    if at == "end": return c["end"]
    if isinstance(at, str) and at.startswith("@"):
        w, _, nth = at[1:].partition("#"); ms = list(re.finditer(r"\b" + re.escape(w) + r"\b", c["text"]))
        assert ms, (cid, at); return c["chartime"][ms[int(nth or 1) - 1].start()]
    return c["start"] + at

events = []
for cid, at, kind, data in S.EVENTS:
    data = dict(data); data["style"] = data.pop("kind", None)
    events.append({"t": round(anchor(cid, at), 3), "seg": clips[cid]["seg"], **data, "kind": kind})
events.sort(key=lambda e: e["t"])
caps = [dict(cap, seg=c["seg"]) for c in clips.values() for cap in c.get("captions", [])]
json.dump({"total": total, "segments": segs, "clips": list(clips.values()), "captions": caps, "events": events},
          open("timeline.json", "w"), indent=1)
print("total", total, "s;", ", ".join(f"{s['id']} {s['end'] - s['start']:.1f}" for s in segs))
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f} {c['text']}")
