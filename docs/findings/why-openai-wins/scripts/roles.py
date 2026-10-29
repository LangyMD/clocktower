"""Which good characters get executed, and what the town's wrong top suspect is, by good lab and generation.
python docs/findings/why-openai-wins/scripts/roles.py GAMES.json"""
import json, sys, collections
R = json.load(open(sys.argv[1]))
NEW = {'claude-fable-5', 'claude-fable-5-1', 'claude-opus-5-5', 'gpt-5.6-sol', 'gpt-6-astra', 'gpt-6.1-sol'}
def grp(g): return ('A' if g['good'].startswith('claude') else 'O') + ('-new' if g['good'] in NEW else '-old')
ex = collections.defaultdict(collections.Counter); ng = collections.Counter(); tops = collections.defaultdict(collections.Counter)
for g in R:
    k = grp(g); ng[k] += 1
    for e in g['execs']:
        if e['died'] and not e['ev']: ex[k][e['char']] += 1
    # wrong top suspects at nomination probes
    for day in range(1, 16):
        ps = [p for p in g['probes'] if p['day'] == day and p['pt'] == 'nominations' and p['team'] == 'good' and p['alive']]
        if not ps: continue
        alive = {p['who'] for p in g['probes'] if p['day'] == day and p['pt'] == 'nominations' and p['alive']}
        agg = collections.defaultdict(list)
        for p in ps:
            for n, (pe, pd, ch) in p['P'].items():
                if n != p['who'] and pe is not None and n in alive: agg[n].append(pe)
        if not agg: continue
        top = max(agg, key=lambda n: sum(agg[n]) / len(agg[n]))
        tops[k]['evil' if top in g['evilset'] else g['char'][top]] += 1
for k in sorted(ng):
    tot = sum(ex[k].values())
    print(f"\n{k}: {ng[k]} games, {tot} good executed ({tot/ng[k]:.2f}/game)")
    print('  executed good by character (per 10 games):', ', '.join(f"{c} {v/ng[k]*10:.1f}" for c, v in ex[k].most_common(9)))
    T = sum(tops[k].values())
    print('  town top suspect (share of nomination probes):', ', '.join(f"{c} {v/T:.0%}" for c, v in tops[k].most_common(9)))

# "test" executions: nominations whose text frames the execution as a way to get information
import re
TEST = re.compile(r"\btest|undertaker|read (it|them|the)|learn (what|who)|(get|gain|yield)s? (us )?(info|information)|confirm", re.I)
print('\nNominations of good players by good players framed as a test (share), and how often they execute:')
c = collections.defaultdict(lambda: [0, 0, 0, 0])
for g in R:
    k = grp(g)
    for nm in g['noms']:
        if nm['nr_ev'] or nm['ne_ev'] or 't' not in nm: continue
        x = c[k]; x[0] += 1; t = bool(TEST.search(nm['t'])); x[1] += t
        executed = nm['outcome'] in ('block', 'executed') or any(e['p'] == nm['ne'] and e['day'] == nm['day'] for e in g['execs'])
        x[2] += executed and t; x[3] += executed
for k in sorted(c):
    n, t, et, e = c[k]
    print(f"  {k}: {n} good-on-good nominations, {t/n:.0%} framed as tests; executions {e}, of which test-framed {et/max(e,1):.0%}; per game {n/ng[k]:.2f}")
