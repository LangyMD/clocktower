"""Supplementary allocation: base = f2 without Opus 4.8's bugged games + the f3 allocation already
running; spend BUDGET on the side-swapped pairs that most reduce rating uncertainty per dollar
(at most CAP per matchup), then choose each new pair's guaranteed Minion to balance the totals."""
import json, glob, math, itertools, collections, os, numpy as np
S = '/tmp/claude-0/-home-user-clocktower/77875c8e-5f76-5858-a3de-44c0d9a7a607/scratchpad/elo/'
B, CAP, DROP = float(os.environ.get('BUDGET', 1200)), int(os.environ.get('CAP', 4)), 'claude-opus-4-8'
K = 400 / math.log(10)
R = json.load(open(S + 'ratings.json')); h = R['h'] / K
order = [m['id'] for m in json.load(open('plans/models-2026.json'))]
r = {n: (R['models'][n]['combined'] - 1500) / K for n in order}
N = len(order); idx = {n: i for i, n in enumerate(order)}
cost = collections.defaultdict(float)
for d in glob.glob('games/v16/f2-*/game-*'):
    try: res = json.load(open(d + '/result.json'))
    except FileNotFoundError: continue
    c = json.load(open(d + '/config.json')); cost[frozenset((c['good_model'], c['evil_model']))] += res.get('cost', 0)
pairs = list(itertools.combinations(order, 2)); pc = {p: cost.get(frozenset(p), 50) for p in pairs}
def IP(a, b):
    I = np.zeros((N + 1, N + 1))
    for g, e in ((a, b), (b, a)):
        x = np.zeros(N + 1); x[idx[g]] = 1; x[idx[e]] = -1; x[-1] = 1
        p = 1 / (1 + math.exp(-(r[g] - r[e] + h))); I += p * (1 - p) * np.outer(x, x)
    return I
IPs = {p: IP(*p) for p in pairs}
f3 = json.load(open('plans/f3-2026-topup.json'))
base = sum(IPs[p] for p in pairs if DROP not in p)
for m in f3['matchups']:
    p = tuple(sorted((m['good'], m['evil']), key=order.index)); base = base + m['pairs'] * IPs[p]
prior = np.diag([1 / 1.5 ** 2] * N + [1e-6]); Cc = np.eye(N) - 1 / N
adj = np.zeros((N - 1, N))
for i in range(N - 1): adj[i, i] = -1; adj[i, i + 1] = 1
def cov(I): return Cc @ np.linalg.inv(I + prior)[:N, :N] @ Cc
def obj(I): V = cov(I); return np.trace(adj @ V @ adj.T) / (N - 1) + np.trace(V) / N
def show(name, I): V = cov(I); print(f"{name:34s} per-model 90% ±{1.645*K*np.sqrt(np.diag(V)).mean():4.0f}  Opus 4.8 ±{1.645*K*np.sqrt(V[idx[DROP],idx[DROP]]):4.0f}  adjacent ±{1.645*K*np.sqrt(np.diag(adj@V@adj.T)).mean():4.0f}")
show('f2 (minus Opus 4.8) + f3', base)
I = base.copy(); spent = 0; alloc = collections.Counter()
while True:
    cur = obj(I); best = None
    for p in pairs:
        if spent + pc[p] > B or alloc[p] >= CAP: continue
        g = (cur - obj(I + IPs[p])) / pc[p]
        if best is None or g > best[0]: best = (g, p)
    if not best: break
    I += IPs[best[1]]; spent += pc[best[1]]; alloc[best[1]] += 1
show(f'+ top-up (${spent:.0f}, {2*sum(alloc.values())} games)', I)
# Minions: counts so far (f2 minus dropped: Poisoner; f3: as assigned), then balance
M = ['Poisoner', 'Spy', 'Scarlet Woman', 'Baron']
per = collections.defaultdict(collections.Counter); tot = collections.Counter()
for p in pairs:
    if DROP not in p:
        for x in p: per[x]['Poisoner'] += 1
        tot['Poisoner'] += 1
for m in f3['matchups']:
    for mi in m['args'][1].split(','):
        for x in (m['good'], m['evil']): per[x][mi] += 1
        tot[mi] += 1
assign = collections.defaultdict(list)
for p in [p for p, n in alloc.most_common() for _ in range(n)]:
    m = min(M, key=lambda m: (per[p[0]][m] + per[p[1]][m], tot[m]))
    per[p[0]][m] += 1; per[p[1]][m] += 1; tot[m] += 1; assign[p].append(m)
print('Minion totals after:', dict(tot)); print('Opus 4.8:', dict(per[DROP]))
short = {m['id']: m['short'] for m in json.load(open('plans/models-2026.json'))}
ms = [{'name': f'{short[a]}-v-{short[b]}', 'good': a, 'evil': b, 'pairs': n, 'seed': 150000 + 100 * i,
       'args': ['--minions', ','.join(assign[(a, b)])]} for i, ((a, b), n) in enumerate(alloc.most_common())]
json.dump({'out': 'games/v17/f3b', 'seed': 150000, 'players': '10-12', 'budget': 19200, 'matchups': ms},
          open('plans/f3b-2026-topup.json', 'w'), indent=1)
print(len(ms), 'matchups:', ', '.join(f"{m['name']} x{m['pairs']}" for m in ms))
