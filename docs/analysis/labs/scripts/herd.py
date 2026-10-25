"""Good voters on good nominees: yes rate by lab generation x whether earlier votes were mostly yes x thinking on the vote turn.
python docs/analysis/labs/scripts/herd.py GAMES.json"""
import json, sys, collections
R = json.load(open(sys.argv[1]))
NEW = {'claude-fable-5', 'claude-fable-5-1', 'claude-opus-5-5', 'gpt-5.6-sol', 'gpt-6-astra', 'gpt-6.1-sol'}
c = collections.defaultdict(lambda: [0, 0])
for g in R:
    k = ('A' if g['good'].startswith('claude') else 'O') + ('-new' if g['good'] in NEW else '-old')
    for v in g['votes']:
        if v['v_ev'] or v['ne_ev'] or v['order'] < 3 or v.get('think') is None: continue
        maj = 'prior-yes' if v['prior_yes'] / v['order'] >= 0.5 else 'prior-no'
        th = 'no-think' if v['think'] == 0 else 'think'
        for key in [(k, maj, th), (k, maj, 'all')]:
            c[key][0] += v['yes']; c[key][1] += 1
for k in sorted(c): print(k, f"{c[k][0]/c[k][1]:.2f} (n={c[k][1]})")
