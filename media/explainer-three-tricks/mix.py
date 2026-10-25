"""Speech + a quiet chord pad + soft vote ticks -> mix.wav (44.1 kHz stereo)."""
import json, os, numpy as np, subprocess
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SR = 44100
TL = json.load(open("timeline.json")); T = TL["total"]; N = int(T * SR)
speech = np.zeros(N, np.float32)
for c in TL["clips"]:
    x = np.fromfile(f"tight/{c['id']}.f32", np.float32); i = int(c["start"] * SR)
    speech[i:i + len(x)] += x[:N - i]
t = np.arange(N) / SR
# pad: four soft chords, 4 s each, crossfaded; sine partials with slight detune
def hz(m): return 440 * 2 ** ((m - 69) / 12)
CH = [[48, 55, 64, 71], [45, 52, 60, 67], [41, 48, 57, 64], [43, 50, 59, 62]]  # Cmaj7, Am7, Fmaj7, G
L = 4.0; pad = np.zeros(N, np.float32)
for k in range(int(T / L) + 2):
    a, b = int((k * L - 1.0) * SR), int(((k + 1) * L + 1.0) * SR)
    a0, b = max(a, 0), min(b, N)
    if a0 >= b: continue
    tt = t[a0:b]; env = np.clip((tt - (k * L - 1.0)) / 1.5, 0, 1) * np.clip(((k + 1) * L + 1.0 - tt) / 1.5, 0, 1)
    y = np.zeros(b - a0)
    for m in CH[k % 4]:
        f = hz(m + 12 * (m < 50))
        y += np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt + 1) + 0.12 * np.sin(2 * np.pi * 2 * f * tt)
    pad[a0:b] += (y * env).astype(np.float32)
pad /= np.abs(pad).max() + 1e-9
pad *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.11 * t)).astype(np.float32)
pad *= np.clip(t / 2.5, 0, 1) * np.clip((T - t) / 2.5, 0, 1)
# soft ticks for vote counting (one per yes vote, as the counter shows)
ev = np.zeros(N, np.float32)
tick_t = np.arange(int(0.06 * SR)) / SR; tick = (np.sin(2 * np.pi * 1350 * tick_t) * np.exp(-tick_t * 90)).astype(np.float32)
for e in TL["events"]:
    if e["kind"] == "votes":
        for j in range(e["yes"]):
            i = int((e["t"] + j * 0.15) * SR); ev[i:i + len(tick)] += tick[:N - i]
# duck the pad under speech
env = np.abs(speech); w = int(0.3 * SR)
sm = np.convolve(env, np.ones(w) / w, mode="same"); duck = np.clip(sm / 0.02, 0, 1)
mix = speech + pad * 0.055 * (1 - 0.45 * duck) + ev * 0.10
mix = mix / max(np.abs(mix).max(), 1e-6) * 0.89
st = np.stack([mix, mix], 1).astype(np.float32)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "mix.wav"], input=st.tobytes(), check=True)
print("mix", round(N / SR, 2), "s")
