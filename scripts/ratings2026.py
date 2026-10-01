"""Final 2026 ratings: one Bradley-Terry fit over f2 (minus Opus 4.8's 20 bugged v16 games) + f3 + f3b.
P(good wins) = logistic(r[good] - r[evil] + h + setup), setup = which Minions were in play and table size.
Combined rating per model, plus detection/deception split; 90% intervals from a bootstrap over side-swapped
pairs (both games of a pair resampled together). Writes JSON for the ratings page."""
import json, glob, os, math, random, collections, datetime, sys
import numpy as np
K = 400 / math.log(10)
MINIONS = ['Spy', 'Scarlet Woman', 'Baron']  # vs Poisoner
OUT = sys.argv[1] if len(sys.argv) > 1 else 'docs/plans/f2-ratings.json'

def load():
    games = []
    for d in glob.glob('games/v16/f2-*/game-*') + glob.glob('games/v17/f3*-*/game-*'):
        if not os.path.exists(d + '/result.json'):
            continue
        r = json.load(open(d + '/result.json')); c = json.load(open(d + '/config.json'))
        if r.get('winner') not in ('good', 'evil'):
            continue
        if '/v16/' in d and 'claude-opus-4-8' in (c['good_model'], c['evil_model']):
            continue
        ev = open(d + '/events.jsonl').readline()
        setup = next(json.loads(l) for l in open(d + '/events.jsonl') if '"kind": "setup"' in l)
        inplay = {s['character'] for s in setup['data']['seats']}
        games.append({'pair': d.split('/')[2] + '/' + d.split('/')[3].replace('-swap', ''), 'good': c['good_model'],
                      'evil': c['evil_model'], 'won': r['winner'] == 'good', 'minions': [m in inplay for m in MINIONS],
                      'players': c.get('players') or len(setup['data']['seats'])})
    return games

def fit(games, names, split=False, prior=1.5, iters=40):
    N = len(names); idx = {n: i for i, n in enumerate(names)}
    P = (2 * N if split else N) + len(MINIONS) + 2 + 1
    X = np.zeros((len(games), P)); y = np.array([g['won'] for g in games], float)
    for k, g in enumerate(games):
        if split:
            X[k, idx[g['good']]] = 1; X[k, N + idx[g['evil']]] = -1
        else:
            X[k, idx[g['good']]] += 1; X[k, idx[g['evil']]] -= 1
        base = 2 * N if split else N
        X[k, base:base + 3] = g['minions']
        X[k, base + 3] = g['players'] == 11; X[k, base + 4] = g['players'] == 12
        X[k, -1] = 1
    w = np.zeros(P); pr = np.full(P, 1 / prior ** 2); pr[-6:] = 1 / 3 ** 2; pr[-1] = 1e-6
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w)); H = (X.T * (p * (1 - p))) @ X + np.diag(pr)
        w += np.linalg.solve(H, X.T @ (y - p) - pr * w)
    if split:
        d = w[:N] - w[:N].mean(); v = w[N:2 * N] - w[N:2 * N].mean()
        return {n: 1500 + K * d[i] for n, i in idx.items()}, {n: 1500 + K * v[i] for n, i in idx.items()}, w[-6:] * K
    r = w[:N] - w[:N].mean()
    return {n: 1500 + K * r[i] for n, i in idx.items()}, None, w[-6:] * K

if __name__ == '__main__':
    games = load()
    ms = json.load(open('plans/models-2026.json')); names = [m['id'] for m in ms]
    years = np.array([(datetime.date.fromisoformat(m['released']) - datetime.date(2026, 1, 1)).days / 365 for m in ms])
    comb, _, extra = fit(games, names); det, dec, _ = fit(games, names, split=True)
    pairs = collections.defaultdict(list)
    for g in games:
        pairs[g['pair']].append(g)
    keys = list(pairs); rng = random.Random(0); B = collections.defaultdict(list)
    for _ in range(int(os.environ.get('BOOT', 500))):
        s = [g for k in (rng.choice(keys) for _ in keys) for g in pairs[k]]
        c, _, _ = fit(s, names); d, v, _ = fit(s, names, split=True)
        for n in names:
            B['c' + n].append(c[n]); B['d' + n].append(d[n]); B['v' + n].append(v[n])
        for key, rr in (('slope_c', c), ('slope_d', d), ('slope_v', v)):
            B[key].append(np.polyfit(years, [rr[n] for n in names], 1)[0])
    q = lambda xs: [round(float(np.percentile(xs, 5))), round(float(np.percentile(xs, 95)))]
    wins = collections.defaultdict(lambda: [0, 0, 0, 0])
    for g in games:
        wins[g['good']][0] += g['won']; wins[g['good']][1] += 1; wins[g['evil']][2] += not g['won']; wins[g['evil']][3] += 1
    out = {'games': len(games), 'evil_win_rate': round(sum(not g['won'] for g in games) / len(games), 3),
           'good_advantage': round(float(extra[-1])), 'setup_effects': {**dict(zip(MINIONS, map(lambda x: round(float(x)), extra[:3]))), '11 players': round(float(extra[3])), '12 players': round(float(extra[4]))},
           'trend_per_year': {k: [round(float(np.polyfit(years, [rr[n] for n in names], 1)[0])), q(B['slope_' + k])] for k, rr in (('c', comb), ('d', det), ('v', dec))},
           'models': [{'id': m['id'], 'date': m['released'], 'lab': m['lab'], 'combined': round(comb[m['id']]), 'c90': q(B['c' + m['id']]),
                       'detection': round(det[m['id']]), 'd90': q(B['d' + m['id']]), 'deception': round(dec[m['id']]), 'v90': q(B['v' + m['id']]),
                       'good_games': wins[m['id']][1], 'good_wins': wins[m['id']][0], 'evil_games': wins[m['id']][3], 'evil_wins': wins[m['id']][2]} for m in ms]}
    json.dump(out, open(OUT, 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'models'}))
    for m in out['models']:
        print(f"{m['id']:20s} {m['combined']:5d} {m['c90']}  det {m['detection']} {m['d90']}  dec {m['deception']} {m['v90']}")
