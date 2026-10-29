import json,collections,statistics as st
D={d['id']:d for d in json.load(open(f'{__import__("sys").argv[1]}/dossiers.json'))}
L={}
for l in open(f'{__import__("sys").argv[1]}/lies.jsonl'):
    j=json.loads(l)
    if 'error' not in j: L[j['id']]=j
res={}
import glob
for g in set(d['game'] for d in D.values()): res[g]=json.load(open(g+'/result.json'))['winner']
rows=[]
for i,j in L.items():
    d=D[i]; cl=j.get('claims') or []
    hard=[c for c in cl if c.get('kind')=='hard_lie']
    rows.append(dict(model=d['model'],char=d['char'],shown=d['shown'],
        hard=bool(hard), hard_pub=any(c.get('channel')=='public' for c in hard),
        multi=any(c.get('kind')=='multi' for c in cl),
        info=bool(j.get('info_lies')), anylie=bool(hard) or bool(j.get('info_lies')),
        clean=j.get('came_clean'), motive=j.get('lie_motive'), win=res[d['game']]=='good',
        nhard=len(hard), nclaims=len(cl), fakes=[c.get('character') for c in hard], id=i, summary=j.get('summary')))
json.dump(rows,open(f'{__import__("sys").argv[1]}/lierows.json','w'))
def tab(key,label,minn=0):
    g=collections.defaultdict(list)
    for r in rows: g[r[key]].append(r)
    print(f"\n{label:20s} {'n':>4s} {'hard lie':>8s} {'public':>6s} {'fake info':>9s} {'any lie':>7s} {'3-for-3':>7s} {'clean':>5s}")
    for k,v in sorted(g.items(),key=lambda kv:-st.mean(x['anylie'] for x in kv[1])):
        if len(v)<minn: continue
        f=lambda c: f"{st.mean(x[c] for x in v):.0%}"
        h=[x for x in v if x['hard']]
        print(f"{k:20s} {len(v):4d} {f('hard'):>8s} {f('hard_pub'):>6s} {f('info'):>9s} {f('anylie'):>7s} {f('multi'):>7s} {(f'{st.mean(bool(x[chr(99)+chr(108)+chr(101)+chr(97)+chr(110)]) for x in h):.0%}' if h else '-'):>5s}")
tab('model','good model'); tab('char','true character')
print('\noverall', len(rows), 'hard', st.mean(r['hard'] for r in rows), 'any', st.mean(r['anylie'] for r in rows))
# which fake roles
c=collections.Counter(f for r in rows for f in r['fakes']); print('\nfake roles claimed:',c.most_common(12))
# win rate by lying (team-level: games where any good seat hard-lied)
gl=collections.defaultdict(lambda:[False,None])
for r in rows:
    g=r['id'].split('|')[0]; gl[g][0]|=r['hard']; gl[g][1]=r['win']
for v in (True,False):
    w=[x[1] for x in gl.values() if x[0]==v]; print(f'games with a good hard-liar={v}: n={len(w)} good win {st.mean(w):.0%}')
