import json,glob,math,random,collections,numpy as np
K=400/math.log(10)
def load():
    games=[]
    for d in sorted(glob.glob('games/v16/f2-*/game-*')):
        try: r=json.load(open(d+'/result.json'))
        except FileNotFoundError: continue
        c=json.load(open(d+'/config.json'))
        if r.get('winner') not in ('good','evil'): continue
        games.append((d.split('/')[2], c['good_model'], c['evil_model'], r['winner']=='good', c.get('players')))
    return games
def fit(games, names, split=False, prior=1.5, iters=60):
    # Newton/IRLS logistic regression with gaussian prior; params: per-name r (combined) or d,v (split) + h
    idx={n:i for i,n in enumerate(names)}; N=len(names)
    P=2*N+1 if split else N+1
    X=np.zeros((len(games),P)); y=np.array([1.0 if g[3] else 0.0 for g in games])
    for k,(_,gm,em,won,_) in enumerate(games):
        if split: X[k,idx[gm]]=1; X[k,N+idx[em]]=-1
        else: X[k,idx[gm]]+=1; X[k,idx[em]]-=1
        X[k,-1]=1
    w=np.zeros(P); pr=np.full(P,1/prior**2); pr[-1]=1e-6
    for _ in range(iters):
        p=1/(1+np.exp(-X@w)); g=X.T@(y-p)-pr*w; H=(X.T*(p*(1-p)))@X+np.diag(pr)
        w+=np.linalg.solve(H,g)
    if split:
        d=w[:N]-w[:N].mean(); v=w[N:2*N]-w[N:2*N].mean()
        return {n:1500+K*d[i] for n,i in idx.items()},{n:1500+K*v[i] for n,i in idx.items()},K*w[-1]
    r=w[:N]-w[:N].mean(); return {n:1500+K*r[i] for n,i in idx.items()},K*w[-1]
if __name__=='__main__':
    games=load(); names=sorted({g[1] for g in games}|{g[2] for g in games})
    by=collections.defaultdict(list)
    for g in games: by[g[0]].append(g)
    keys=list(by); rng=random.Random(1)
    comb,h=fit(games,names); det,dec,_=fit(games,names,split=True)
    B={'c':collections.defaultdict(list),'d':collections.defaultdict(list),'v':collections.defaultdict(list)}
    for b in range(1000):
        s=[g for k in (rng.choice(keys) for _ in keys) for g in by[k]]
        c,_=fit(s,names); d,v,_=fit(s,names,split=True)
        for n in names: B['c'][n].append(c[n]); B['d'][n].append(d[n]); B['v'][n].append(v[n])
    q=lambda xs:(float(np.percentile(xs,5)),float(np.percentile(xs,95)))
    out={'games':len(games),'h':h,'models':{n:{'combined':comb[n],'c90':q(B['c'][n]),'detection':det[n],'d90':q(B['d'][n]),'deception':dec[n],'v90':q(B['v'][n])} for n in names}}
    json.dump(out,open('/tmp/claude-0/-home-user-clocktower/77875c8e-5f76-5858-a3de-44c0d9a7a607/scratchpad/elo/ratings.json','w'),indent=1)
    for n in sorted(names,key=lambda n:-comb[n]): m=out['models'][n]; print(f"{n:20s} {m['combined']:6.0f} [{m['c90'][0]:5.0f},{m['c90'][1]:5.0f}]  det {m['detection']:5.0f} dec {m['deception']:5.0f}")
    print('games',len(games),'h',round(h))
