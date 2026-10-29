import json,glob,sys,os
EVIL={'Imp','Poisoner','Spy','Baron','Scarlet Woman'}
games=sorted(glob.glob('games/v16/f2-*/game-*')+glob.glob('games/v17/f3*/game-*'))
out=[]
for g in games:
    cfg=json.load(open(g+'/config.json')); shown={}; lines={}
    for l in open(g+'/events.jsonl'):
        e=json.loads(l); k=e['kind']; d=e['data']
        if k=='setup':
            shown={s['name']:(s['character'],s['shown']) for s in d['seats']}; lines={p:[] for p in shown}
        elif k=='info':
            for p in e['to']: lines[p].append(f"[D{e['day']} STORYTELLER→you] {d['text']}")
        elif k=='say': lines[d['speaker']].append(f"[D{e['day']} PUBLIC] {d['text']}")
        elif k=='whisper': lines[d['from']].append(f"[D{e['day']} WHISPER→{','.join(d['to'])}] {d['text']}")
        elif k=='nomination': lines[d['nominator']].append(f"[D{e['day']} NOMINATES {d['nominee']}] {d['text']}")
        elif k=='defense': lines[d['nominee']].append(f"[D{e['day']} DEFENSE] {d['text']}")
    for p,(ch,sh) in shown.items():
        if ch in EVIL: continue
        out.append(dict(id=f"{g}|{p}",game=g,model=cfg['good_model'],evil_model=cfg['evil_model'],player=p,char=ch,shown=sh,text='\n'.join(x for x in lines[p] if x.split('] ',1)[1].strip())))
json.dump(out,open(sys.argv[1],'w'))
n=sum(len(x['text']) for x in out); print(len(out), n/4/1e6,'M tokens approx')
