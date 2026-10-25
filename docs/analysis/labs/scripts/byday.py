"""Town top suspect evil, and Brier, by day; good win by number of good players executed. By good lab x generation.
python docs/analysis/labs/scripts/byday.py GAMES.json"""
import json, sys, collections
R = json.load(open(sys.argv[1]))
NEW = {'claude-fable-5', 'claude-fable-5-1', 'claude-opus-5-5', 'gpt-5.6-sol', 'gpt-6-astra', 'gpt-6.1-sol'}
def grp(g): return (('A' if g['good'].startswith('claude') else 'O') + ('-new' if g['good'] in NEW else '-old')) if MODE == 'lab' else g['good']
MODE = sys.argv[2] if len(sys.argv) > 2 else 'lab'
top = collections.defaultdict(lambda: [0, 0]); br = collections.defaultdict(lambda: [0, 0]); win = collections.defaultdict(lambda: [0, 0])
alive_d = collections.defaultdict(lambda: [0, 0])
for g in R:
    k = grp(g)
    ge = sum(1 for e in g['execs'] if e['died'] and not e['ev'])
    w = win[(k, min(ge, 2))]; w[0] += g['goodwin']; w[1] += 1
    for day in range(1, 16):
        ps = [p for p in g['probes'] if p['day'] == day and p['pt'] == 'nominations' and p['team'] == 'good' and p['alive']]
        if not ps: continue
        alive = {p['who'] for p in g['probes'] if p['day'] == day and p['pt'] == 'nominations' and p['alive']}
        agg = collections.defaultdict(list)
        for p in ps:
            for n, (pe, pd, ch) in p['P'].items():
                if n != p['who'] and pe is not None and n in alive:
                    agg[n].append(pe)
                    b = br[(k, min(day, 3))]; b[0] += (pe - p['truth'][n][1]) ** 2; b[1] += 1
        if not agg: continue
        t = max(agg, key=lambda n: sum(agg[n]) / len(agg[n]))
        x = top[(k, min(day, 3))]; x[0] += t in g['evilset']; x[1] += 1
for k in (['A-old', 'O-old', 'A-new', 'O-new'] if MODE == 'lab' else sorted({g['good'] for g in R})):
    print(k, 'top suspect evil d1/d2/d3+:', ' / '.join(f"{top[(k,d)][0]/top[(k,d)][1]:.2f} (n={top[(k,d)][1]})" for d in (1, 2, 3)),
          '| Brier (living) d1/d2/d3+:', ' / '.join(f"{br[(k,d)][0]/br[(k,d)][1]:.3f}" for d in (1, 2, 3)))
    print('   good win by good players executed 0/1/2+:', ' / '.join(f"{win[(k,n)][0]/max(1,win[(k,n)][1]):.2f} (n={win[(k,n)][1]})" for n in (0, 1, 2)))
