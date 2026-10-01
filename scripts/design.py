import json,glob,math,itertools,collections,numpy as np
S='/tmp/claude-0/-home-user-clocktower/77875c8e-5f76-5858-a3de-44c0d9a7a607/scratchpad/elo/'
R=json.load(open(S+'ratings.json')); h=R['h']/ (400/math.log(10))
order=[m['id'] for m in json.load(open('plans/models-2026.json'))]
r={n:(R['models'][n]['combined']-1500)/(400/math.log(10)) for n in order}
N=len(order); idx={n:i for i,n in enumerate(order)}
# cost per pair per matchup from f2
cost=collections.defaultdict(float)
for d in glob.glob('games/v16/f2-*/game-*'):
    try: res=json.load(open(d+'/result.json'))
    except: continue
    c=json.load(open(d+'/config.json')); cost[frozenset((c['good_model'],c['evil_model']))]+=res.get('cost',0)
pairs=list(itertools.combinations(order,2))
pc={p:cost.get(frozenset(p),50) for p in pairs}
def info_pair(a,b):
    v=np.zeros(N+1); I=np.zeros((N+1,N+1))
    for g,e in ((a,b),(b,a)):
        x=np.zeros(N+1); x[idx[g]]=1; x[idx[e]]=-1; x[-1]=1
        p=1/(1+math.exp(-(r[g]-r[e]+h))); I+=p*(1-p)*np.outer(x,x)
    return I
IP={p:info_pair(*p) for p in pairs}
base=sum(IP[p] for p in pairs)  # current f2: 1 pair each
prior=np.diag([1/1.5**2]*N+[1e-6])
C=np.eye(N+1)[:,:N]; Cc=np.eye(N)-1/N  # centring
def cov(I):
    full=np.linalg.inv(I+prior)[:N,:N]; return Cc@full@Cc
K=400/math.log(10)
adj=np.zeros((N-1,N))
for i in range(N-1): adj[i,i]=-1; adj[i,i+1]=1
t=np.array(range(N),float); t=(t-t.mean())/((t-t.mean())**2).sum()   # slope vs release rank
def metrics(I):
    V=cov(I); se=np.sqrt(np.diag(V))*K; sa=np.sqrt(np.diag(adj@V@adj.T))*K
    return se.mean(), sa.mean(), sa.max()
def show(name,I,spent,ngames):
    m=metrics(I); print(f"{name:42s} ${spent:6.0f} {ngames:4d} games | per-model 90% ±{1.645*m[0]:4.0f} | adjacent-gap 90% ±{1.645*m[1]:4.0f} (worst ±{1.645*m[2]:4.0f})")
show('now (f2, 1 pair each)',base,0,0)
B=int(__import__("os").environ.get("BUDGET","10000")); CAP=int(__import__("os").environ.get("CAP","1000"))
for k in (1,2,3):
    I=base+k*sum(IP[p] for p in pairs); spent=k*sum(pc.values()); show(f'uniform +{k} pairs/matchup',I,spent,k*2*len(pairs))
# greedy by objective reduction per dollar: objective = mean adjacent-gap variance + mean per-model variance
def obj(I):
    V=cov(I); return np.trace(adj@V@adj.T)/(N-1)+np.trace(V)/N
I=base.copy(); spent=0; alloc=collections.Counter()
while True:
    cur=obj(I); best=None
    for p in pairs:
        if spent+pc[p]>B or alloc[p]>=CAP: continue
        gain=(cur-obj(I+IP[p]))/pc[p]
        if best is None or gain>best[0]: best=(gain,p)
    if not best: break
    p=best[1]; I+=IP[p]; spent+=pc[p]; alloc[p]+=1
show('greedy optimal (~$10k)',I,spent,2*sum(alloc.values()))
json.dump({f'{a}|{b}':n for (a,b),n in alloc.items()},open(S+'greedy.json','w'),indent=1)
tier={n:(i>=5) for i,n in enumerate(order)}
gap=collections.Counter(); 
for (a,b),n in alloc.items(): gap[abs(idx[a]-idx[b])]+=n
print('greedy extra pairs by release distance:',dict(sorted(gap.items())))
print('greedy extra pairs per model:',{n.replace('claude-',''):sum(v for p,v in alloc.items() if n in p) for n in order})
print('mean cost/pair f2: $%.0f'%(sum(pc.values())/len(pc)))
print('opus 4.8 redo (20 games): $%.0f'%sum(v for p,v in pc.items() if 'claude-opus-4-8' in p))
