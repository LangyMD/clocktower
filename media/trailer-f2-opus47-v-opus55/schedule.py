import json
d=json.load(open('tight/durs.json'))
order=[('c01',0.5,0.25),('c02',0,0.55),('c03',0,0.45),('c04',0,0.2),('c05',0,0.35),('c06',0,0.45),('c07',0,0.45),('c08',0,0.25),('c09',0,0.2),('c10',0,0.4),('c11',0,0.45),('c13',0,0.3),('c14',0,0.2),('c15',0,1.15),('c16',0,0.45),('c17',0,1.4)]
t=0;S={}
for cid,pre,post in order:
    t+=pre; S[cid]={'start':round(t,3),'dur':d[cid]}; t+=d[cid]
    S[cid]['end']=round(t,3); t+=post
S['total']=round(t,3)
json.dump(S,open('schedule.json','w'),indent=1)
print({k:(v['start'] if isinstance(v,dict) else v) for k,v in S.items()})
