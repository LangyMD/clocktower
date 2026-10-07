import json,glob,re,collections,math,statistics as st
EVIL={'Imp','Poisoner','Spy','Baron','Scarlet Woman'}
def feats(msgs):
    t=' '.join(msgs); w=max(1,len(t.split())); n=max(1,len(msgs))
    return [len(t.split())/n, t.count('—')/w*100, t.count('–')/w*100, t.count(' - ')/w*100, t.count(';')/w*100,
            t.count('(')/w*100, t.count('!')/w*100, t.count('?')/w*100, len(re.findall(r'\d',t))/w*100,
            t.count('’')/w*100, t.count("'")/w*100, t.count('"')/w*100, len(re.findall(r'\b[A-Z]{2,}\b',t))/w*100,
            t.count(':')/w*100, t.count('/')/w*100, len(re.findall(r'\bI\b',t))/w*100]
games=sorted(glob.glob('games/v16/f2-*/game-*')+glob.glob('games/v17/f3*/game-*'))
aucs=collections.defaultdict(list); top=collections.Counter()
for g in games:
    cfg=json.load(open(g+'/config.json')); team={}; msgs=collections.defaultdict(list)
    for l in open(g+'/events.jsonl'):
        e=json.loads(l); d=e['data']
        if e['kind']=='setup': team={s['name']:s['character'] in EVIL for s in d['seats']}
        elif e['kind']=='say' and e['day']==1: msgs[d['speaker']].append(d['text'])
        elif e['kind']=='whisper' and e['day']==1: msgs[d['from']].append(d['text'])
    ps=[p for p in team if msgs[p]]
    F={p:feats(msgs[p]) for p in ps}
    k=len(next(iter(F.values())))
    mu=[st.mean(F[p][i] for p in ps) for i in range(k)]; sd=[st.pstdev([F[p][i] for p in ps]) or 1 for i in range(k)]
    Z={p:[(F[p][i]-mu[i])/sd[i] for i in range(k)] for p in ps}
    dist=lambda a,b: math.dist(Z[a],Z[b])
    for p in ps:
        if team[p]: continue
        same=[dist(p,q) for q in ps if q!=p and not team[q]]; diff=[dist(p,q) for q in ps if team[q]]
        pairs=[(a<b)+0.5*(a==b) for a in same for b in diff]
        aucs[cfg['good_model']].append(sum(pairs)/len(pairs))
        # does "least like me" pick evil? top-3 most-distant players: fraction evil
        far=sorted((q for q in ps if q!=p),key=lambda q:-dist(p,q))[:3]
        top[cfg['good_model']]+=sum(team[q] for q in far)/3
allv=[x for v in aucs.values() for x in v]
print('overall AUC (good seat: teammates closer than evil), day-1 text only:',round(st.mean(allv),3),len(allv))
for m,v in sorted(aucs.items(),key=lambda x:-st.mean(x[1])): print(f'{m:22s} AUC {st.mean(v):.2f}  evil share of 3 least-similar {top[m]/len(v):.2f}  n={len(v)}')

# town-level rule using no hidden info: the 3 players whose day-1 style is least like the table's majority
import itertools
hit=0;n=0;exe_hit=0;exe_n=0;cl_hit=0;demon_in=0
for g in games:
    team={}; msgs=collections.defaultdict(list); ch={}
    for l in open(g+'/events.jsonl'):
        e=json.loads(l); d=e['data']
        if e['kind']=='setup': team={s['name']:s['character'] in EVIL for s in d['seats']}; ch={s['name']:s['character'] for s in d['seats']}
        elif e['kind']=='say' and e['day']==1: msgs[d['speaker']].append(d['text'])
        elif e['kind']=='whisper' and e['day']==1: msgs[d['from']].append(d['text'])
        elif e['kind']=='execution' and e['day']==1: exe_n+=1; exe_hit+=team[d['player']]
    ps=[p for p in team if msgs[p]]
    F={p:feats(msgs[p]) for p in ps}; k=len(F[ps[0]])
    mu=[st.mean(F[p][i] for p in ps) for i in range(k)]; sd=[st.pstdev([F[p][i] for p in ps]) or 1 for i in range(k)]
    Z={p:[(F[p][i]-mu[i])/sd[i] for i in range(k)] for p in ps}
    # 2-means, init from the farthest pair
    a,b=max(itertools.combinations(ps,2),key=lambda x:math.dist(Z[x[0]],Z[x[1]]))
    ca,cb=Z[a],Z[b]
    for _ in range(20):
        A=[p for p in ps if math.dist(Z[p],ca)<=math.dist(Z[p],cb)]; B=[p for p in ps if p not in A]
        if not A or not B: break
        ca=[st.mean(Z[p][i] for p in A) for i in range(k)]; cb=[st.mean(Z[p][i] for p in B) for i in range(k)]
    small=min(A,B,key=len)
    n+=1; cl_hit+=sum(team[p] for p in small)/len(small); demon_in+=any(ch[p]=='Imp' for p in small)
print(f'2-cluster rule: smaller cluster is {cl_hit/n:.0%} evil on average; contains the Imp in {demon_in/n:.0%} of games')
print(f'actual day-1 executions that hit evil: {exe_hit}/{exe_n} = {exe_hit/exe_n:.0%}')
