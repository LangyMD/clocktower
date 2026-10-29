"""Speech clips -> a timed episode (timeline.json) and its soundtrack (speech + candle-dark pad + small effects).

process(): decode a cached TTS mp3, speed it up slightly, trim the ends, shrink long pauses, level it, and keep a
map from the original character times to the new ones (for captions and the karaoke highlight in quote cards).
"""
import json, re, subprocess
import numpy as np
from pathlib import Path

from . import tts

SR = 44100
TEMPO = {"N": 1.04}            # players default to PLAYER_TEMPO
PLAYER_TEMPO = 1.07
WIN, THR, MAXGAP = 0.02, -42, 0.30
PROC = Path(__file__).resolve().parent / "cache" / "proc"


def process(who, text):
    mp3, meta = tts.path(who, text)
    tempo = TEMPO.get(who, PLAYER_TEMPO)
    PROC.mkdir(parents=True, exist_ok=True)
    out = PROC / f"{mp3.stem}_{tempo}.f32"; omap = PROC / f"{mp3.stem}_{tempo}.json"
    al = json.load(open(meta))["alignment"] or {}
    chars = "".join(al.get("characters", [])); st = al.get("character_start_times_seconds", [])
    if out.exists() and omap.exists():
        return np.fromfile(out, np.float32), json.load(open(omap))
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(mp3), "-af", f"atempo={tempo}", "-ar", str(SR), "-ac", "1",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy(); w = int(WIN * SR); n = len(x) // w
    if n < 3:
        y = x; chartime = [0.0] * len(text)
    else:
        db = 20 * np.log10(np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12)); loud = db > THR
        idx = np.where(loud)[0]
        first, last = (max(idx[0] - 2, 0), min(idx[-1] + 5, n - 1)) if len(idx) else (0, n - 1)
        keep = np.zeros(n, bool); keep[first:last + 1] = True
        k = first
        while k <= last:
            if not loud[k]:
                j = k
                while j <= last and not loud[j]: j += 1
                if (j - k) * WIN > MAXGAP:
                    h = int(MAXGAP / WIN / 2); keep[k + h:j - h] = False
                k = j
            else: k += 1
        kept = np.where(keep)[0]
        y = x[:n * w].reshape(n, w)[kept].reshape(-1).copy()
        voiced = y.reshape(-1, w)[(db[kept] > THR)] if len(kept) else y.reshape(-1, w)
        rms = np.sqrt((voiced ** 2).mean()) if voiced.size else 0.05
        y *= 0.10 / max(rms, 1e-4)                           # level: voiced RMS ~ -20 dBFS
        y = np.tanh(y * 1.2) / 1.2                           # soft limit
        f = int(0.008 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        newpos = np.cumsum(keep) - 1
        def tmap(t):
            i = min(max(int(t / tempo / WIN), first), last)
            return float(max(newpos[i], 0) * WIN)
        if chars == text and st:
            chartime = [round(tmap(s), 3) for s in st]
        else:                                                 # alignment missing or normalised: spread evenly
            d = len(y) / SR; chartime = [round(d * i / max(len(text), 1), 3) for i in range(len(text))]
    y = y.astype(np.float32); y.tofile(out)
    m = {"dur": round(len(y) / SR, 3), "chartime": chartime}
    json.dump(m, open(omap, "w"))
    return y, m


def chunks(text, limit=62):
    """Caption chunks: sentences, long ones split at commas; short neighbours merged."""
    parts = [p.strip() for p in re.findall(r"[^.!?:;]+[.!?:;]?", text) if p.strip()]
    out = []
    for p in parts:
        while len(p) > limit + 20:
            cut = [m.end() for m in re.finditer(r",", p) if 20 < m.end() < limit + 10]
            c = cut[-1] if cut else (p.rfind(" ", 0, limit) if p.rfind(" ", 0, limit) > 0 else limit)
            out.append(p[:c].strip()); p = p[c:].strip()
        if out and len(out[-1]) + len(p) + 1 <= limit and not out[-1].endswith((".", "?", "!")):
            out[-1] += " " + p
        else:
            out.append(p)
    return out


def schedule(ep):
    """Episode script -> timeline (absolute times for clips, captions and visual events)."""
    T = 0.6; clips, caps, events = [], [], []
    for step in ep["steps"]:
        c = step["clip"]
        for e in step["ev"]:
            events.append(dict(e, t=round(T, 3)))
        if c:
            y, m = process(c["who"], c["text"])
            if c["who"] != "N": T += 0.12
            ci = len(clips)
            rec = {"who": c["who"], "start": round(T, 3), "dur": m["dur"], "text": c["text"], "show": c["show"],
                   "chartime": [round(T + s, 3) for s in m["chartime"]]}
            clips.append(rec)
            for e in events[-len(step["ev"]):] if step["ev"] else []:
                if e["k"] == "panel" and e.get("text") == c["show"]: e["clip"] = ci
            if c["who"] == "N":
                pos = 0
                cs = chunks(c["show"])
                for i, ch in enumerate(cs):
                    j = c["show"].find(ch, pos); pos = j + len(ch)
                    k = int(j / max(len(c["show"]), 1) * len(c["text"])) if c["show"] != c["text"] else j
                    caps.append({"text": ch, "start": rec["chartime"][min(k, len(rec["chartime"]) - 1)] if rec["chartime"] else T})
                for a, b in zip(caps[-len(cs):], caps[-len(cs) + 1:] + [None]):
                    a["end"] = b["start"] if b else round(T + m["dur"] + 0.1, 3)
            T += m["dur"]
        for e in step["ev_end"]:
            events.append(dict(e, t=round(T, 3)))
        T += step["hold"]
    events.sort(key=lambda e: e["t"])
    return {"total": round(T + 0.8, 3), "clips": clips, "captions": caps, "events": events,
            **{k: v for k, v in ep.items() if k != "steps"}}


# ---------------------------------------------------------------- soundtrack
def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def pad_loop(L=32.0):
    """A seamless 32 s loop: four soft minor-ish chords in a low register (Dm, Bb, F, C/E)."""
    n = int(L * SR); t = np.arange(n) / SR; y = np.zeros(n, np.float32)
    CH = [[50, 57, 62, 65], [46, 53, 58, 62], [41, 53, 57, 60], [40, 52, 55, 60]]
    seg = L / len(CH)
    for k, ch in enumerate(CH):
        c0 = k * seg
        d = (t - c0) % L                                         # cyclic distance from chord start
        env = np.clip(np.minimum(d / 2.5, (seg + 2.5 - d) / 2.5), 0, 1) * (d < seg + 2.5)
        part = np.zeros(n, np.float32)
        for m in ch:
            f = hz(m)
            part += (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 1.004 * t + 1.3)
                     + 0.08 * np.sin(2 * np.pi * 2 * f * t)).astype(np.float32)
        y += part * env.astype(np.float32)
    y /= np.abs(y).max() + 1e-9
    return y * (0.8 + 0.2 * np.sin(2 * np.pi * t / L * 4)).astype(np.float32)


def bell(f0=196.0, dur=4.0):
    t = np.arange(int(dur * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * dcy) for r, a, dcy in
            [(1, 1, 1.1), (2.0, 0.5, 1.6), (2.76, 0.35, 2.2), (5.4, 0.15, 3.5), (0.5, 0.4, 0.8)])
    return (y / np.abs(y).max()).astype(np.float32)


def thud(dur=0.9):
    t = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-t * 6)).astype(np.float32)


def tick():
    t = np.arange(int(0.07 * SR)) / SR
    return (np.sin(2 * np.pi * 1250 * t) * np.exp(-t * 80)).astype(np.float32)


def mix(tl, out_wav):
    N = int(tl["total"] * SR) + SR
    speech = np.zeros(N, np.float32)
    for c in tl["clips"]:
        y, _ = process(c["who"], c["text"]); i = int(c["start"] * SR)
        speech[i:i + len(y)] += y[:N - i]
    loop = pad_loop(); reps = N // len(loop) + 1
    pad = np.tile(loop, reps)[:N]
    t = np.arange(N, dtype=np.float32) / SR
    pad *= np.clip(t / 3, 0, 1) * np.clip((tl["total"] - t) / 3, 0, 1)
    fx = np.zeros(N, np.float32)
    def put(x, at, g):
        i = int(at * SR); j = min(N, i + len(x)); fx[i:j] += g * x[:j - i]
    B, TH, TK = bell(), thud(), tick()
    for e in tl["events"]:
        if e["k"] == "phase" and e.get("night") and e["text"].startswith("Night"): put(B, e["t"], 0.22)
        elif e["k"] == "dead": put(TH, e["t"], 0.35)
        elif e["k"] == "votes":
            for j in range(len(e["voters"])): put(TK, e["t"] + 0.15 + j * 0.16, 0.12)
        elif e["k"] == "outcome": put(bell(147.0, 6.0), e["t"], 0.3)
    env = np.abs(speech); w = int(0.3 * SR)
    cs = np.concatenate([[0.0], np.cumsum(env, dtype=np.float64)])
    lo = np.clip(np.arange(N) - w // 2, 0, N); hi = np.clip(np.arange(N) + w // 2, 0, N)
    sm = ((cs[hi] - cs[lo]) / w).astype(np.float32); duck = np.clip(sm / 0.02, 0, 1)
    m = speech + pad * 0.05 * (1 - 0.5 * duck) + fx
    m = m / max(np.abs(m).max(), 1e-6) * 0.89
    st = np.stack([m, m], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(out_wav)], input=st.tobytes(), check=True)
