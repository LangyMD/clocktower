"""Per-lab improvement per year (Anthropic vs OpenAI) in combined (c), detection (d) and deception (v) ratings:
a straight line through each lab's 2026 models by release date, with 90% intervals from a bootstrap over
side-swapped pairs (the same resampling as ratings2026.py). Writes docs/charts/lab-trends.json."""
import sys, json, datetime, random, collections, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from ratings2026 import load, fit
games = load(); ms = json.load(open('plans/models-2026.json')); names = [m['id'] for m in ms]
yr = {m['id']: (datetime.date.fromisoformat(m['released']) - datetime.date(2026, 1, 1)).days / 365 for m in ms}
labs = {m['id']: m['lab'] for m in ms}
def slopes(c, d, v):
    out = {}
    for lab in ('Anthropic', 'OpenAI', None):
        ns = [n for n in names if lab is None or labs[n] == lab]
        x = [yr[n] for n in ns]
        for k, rr in (('c', c), ('d', d), ('v', v)):
            b, a = np.polyfit(x, [rr[n] for n in ns], 1); out[(lab or 'all', k)] = (b, a)
    return out
c, _, _ = fit(games, names); d, v, _ = fit(games, names, split=True)
point = slopes(c, d, v)
pairs = collections.defaultdict(list)
for g in games: pairs[g['pair']].append(g)
keys = list(pairs); rng = random.Random(1); B = collections.defaultdict(list)
for _ in range(400):
    s = [g for k in (rng.choice(keys) for _ in keys) for g in pairs[k]]
    cc, _, _ = fit(s, names); dd, vv, _ = fit(s, names, split=True)
    sl = slopes(cc, dd, vv)
    for k, (b, a) in sl.items(): B[k].append(b)
    for lk in ('d', 'v', 'c'):
        B[('gap', lk)].append(sl[('OpenAI', lk)][0] - sl[('Anthropic', lk)][0])
q = lambda xs: [round(float(np.percentile(xs, 5))), round(float(np.percentile(xs, 95)))]
res = {f'{l}|{k}': {'slope': round(float(b)), 'intercept': round(float(a)), 'ci': q(B[(l, k)])} for (l, k), (b, a) in point.items()}
for lk in 'dvc':
    res[f'gap|{lk}'] = {'slope': round(float(point[('OpenAI', lk)][0] - point[('Anthropic', lk)][0])), 'ci': q(B[('gap', lk)]),
                        'p_openai_faster': round(float(np.mean(np.array(B[('gap', lk)]) > 0)), 3)}
json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'docs/charts/lab-trends.json', 'w'), indent=1)
print(json.dumps(res))
