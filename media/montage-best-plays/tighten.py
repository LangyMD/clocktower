"""Normalise loudness and shrink long pauses in each clip; writes tight/<id>.f32 and tight/durs.json."""
import numpy as np, subprocess, glob, os, json
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SR = 44100; MAXGAP = 0.2; THR = -42
os.makedirs('tight', exist_ok=True)
ids = [c["id"] for c in json.load(open("clips.json"))]
durs = {}
for b in ids:
    f = f"audio/{b}.mp3"
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-af', 'atempo=1.1,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    win = int(0.02 * SR); n = len(x) // win
    db = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12)); loud = db > THR
    idx = np.where(loud)[0]; first, last = idx[0], idx[-1]
    run, out = [], []
    for k in range(first, last + 1):
        if loud[k]:
            if run and len(run) * 0.02 > MAXGAP:
                h = int(MAXGAP / 0.02 / 2); run = run[:h] + run[-h:]
            out += run; run = []; out.append(k)
        else: run.append(k)
    y = np.concatenate([x[k * win:(k + 1) * win] for k in out])
    pad = np.zeros(int(0.06 * SR), dtype=np.float32); y = np.concatenate([pad, y, pad * 2])
    fl = int(0.01 * SR); y[:fl] *= np.linspace(0, 1, fl); y[-fl:] *= np.linspace(1, 0, fl)
    y.astype(np.float32).tofile(f'tight/{b}.f32'); durs[b] = len(y) / SR
json.dump(durs, open('tight/durs.json', 'w'), indent=1)
print('speech total', round(sum(durs.values()), 1), 's')
