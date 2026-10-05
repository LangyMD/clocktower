"""Speech + ambient bed + sound events -> mix.f32 (mono 44.1k)."""
import numpy as np, json, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SR = 44100
TL = json.load(open('timeline.json')); T = TL['total']; N = int(T * SR) + SR
speech = np.zeros(N, np.float32)
def place(cid, start):
    x = np.fromfile(f'tight/{cid}.f32', dtype=np.float32); i = max(int(start * SR) - int(0.06 * SR), 0)
    speech[i:i + len(x)] += x[:N - i]
for s in TL['segments']:
    if s['kind'] == 'game': place(s['id'] + 't', s['tclip']['start'])
    for b in s['beats']: place(b['id'], b['start'])
t = np.arange(N) / SR; rng = np.random.default_rng(7)
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
drone = (0.5 * np.sin(2 * np.pi * 55 * t) + 0.35 * np.sin(2 * np.pi * 82.41 * t + 1) + 0.18 * np.sin(2 * np.pi * 110.3 * t + 2) + 0.08 * np.sin(2 * np.pi * 164.8 * t)) * lfo
n = rng.standard_normal(N).astype(np.float32); F = np.fft.rfft(n); f = np.fft.rfftfreq(N, 1 / SR); F *= 1 / (1 + (f / 250) ** 4)
wind = np.fft.irfft(F, N); wind /= np.abs(wind).max(); wind *= 0.5 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.05 * t + 1))
bed = (drone * 0.6 + wind * 0.5).astype(np.float32) * np.clip(t / 2, 0, 1) * np.clip((T - t) / 2, 0, 1) * 0.09
ev = np.zeros(N, np.float32)
def add(at, sig, g):
    i = int(at * SR); j = min(N, i + len(sig))
    if i < N: ev[i:j] += g * sig[:j - i]
def knock():
    tt = np.arange(int(0.25 * SR)) / SR
    return (np.sin(2 * np.pi * 180 * tt) * np.exp(-tt * 25) + 0.3 * np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 40)).astype(np.float32)
def boom(dur=2.5, f0=60):
    tt = np.arange(int(dur * SR)) / SR; fr = f0 * (1 + 1.5 * np.exp(-tt * 12)); ph = 2 * np.pi * np.cumsum(fr) / SR
    nz = rng.standard_normal(len(tt)); Fz = np.fft.rfft(nz); fz = np.fft.rfftfreq(len(tt), 1 / SR); Fz *= 1 / (1 + (fz / 400) ** 2)
    nz = np.fft.irfft(Fz, len(tt)); nz /= np.abs(nz).max()
    return (np.sin(ph) * np.exp(-tt * 2.2) + 0.35 * nz * np.exp(-tt * 8)).astype(np.float32)
def bell(f=196, dur=6.0):
    tt = np.arange(int(dur * SR)) / SR
    parts = [(0.5, 1.0, 0.9), (1.0, 0.8, 1.3), (1.19, 0.5, 1.8), (1.56, 0.35, 2.4), (2.0, 0.3, 2.8), (2.51, 0.2, 3.5), (3.0, 0.12, 4.5), (4.07, 0.08, 6)]
    y = sum(a * np.sin(2 * np.pi * f * r * tt + r) * np.exp(-tt * d * 0.6) for r, a, d in parts); y *= np.clip(tt / 0.004, 0, 1)
    return (y / np.abs(y).max()).astype(np.float32)
for s in TL['segments']:
    if s['kind'] == 'game':
        add(s['start'] + 0.3, bell(147, 6), 0.16)
    elif s['id'] == 'intro':
        add(s['beats'][2]['start'] - 0.1, bell(147, 6), 0.16)
    elif s['id'] == 'outro':
        add(s['beats'][-1]['start'] - 0.1, bell(196, 5), 0.10)
    for b in s.get('beats', []):
        v = b.get('visual', {})
        if v.get('votes'):
            k = v['votes']['yes']; span = max(b['dur'] * 0.6, 0.5)
            for i in range(1, k + 1): add(b['start'] + 0.2 + span * i / k - 0.02, knock(), 0.2)
        if v.get('banner'):
            add(b['start'] - 0.12, boom(3.5, 45), 0.45); add(b['start'] - 0.1, bell(98 if s.get('winner') == 'evil' else 131, 7), 0.2)
        elif v.get('dies'):
            add(b['start'] + 0.1, boom(2.2, 55), 0.28)
        elif v.get('stamp'):
            add(b['start'] + 0.15, boom(1.5, 70), 0.16)
e = np.abs(speech); se = np.convolve(e, np.ones(int(0.05 * SR)) / int(0.05 * SR), mode='same')
se = np.convolve((se > 0.01).astype(np.float32), np.ones(int(0.3 * SR)) / int(0.3 * SR), mode='same')
mix = speech + bed * (1 - 0.55 * np.clip(se, 0, 1)) + ev * (1 - 0.35 * np.clip(se, 0, 1))
mix = mix[:int(T * SR)]; mix = mix / max(np.abs(mix).max(), 1e-6) * 0.89
mix.astype(np.float32).tofile('mix.f32'); print('dur', len(mix) / SR)
