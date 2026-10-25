"""Lay every clip on one timeline -> timeline.json (segments, beats with start/end, total)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
durs = json.load(open('tight/durs.json'))
ORDER = json.load(open('order.json'))
t = 0.4; segs = []
for sid in ORDER:
    seg = json.load(open(f'scenes/{sid}.json')); seg.setdefault('kind', 'game')
    seg['start'] = t
    if seg['kind'] == 'game':
        t += 0.5; tid = sid + 't'
        seg['tclip'] = {'start': round(t, 3), 'end': round(t + durs[tid], 3)}
        t += durs[tid] + 0.95
    beats = seg['beats']
    for i, b in enumerate(beats):
        t += b.get('pre', 0)
        b['start'] = round(t, 3); b['dur'] = durs[b['id']]; t += b['dur']; b['end'] = round(t, 3)
        last = i == len(beats) - 1
        t += b.get('post', 2.2 if last and seg['kind'] == 'game' else (0.45 if b['voice'] == 'NARR' else 0.4))
    seg['end'] = round(t, 3)
    segs.append(seg)
json.dump({'total': round(t + 0.5, 3), 'segments': segs}, open('timeline.json', 'w'), indent=1)
print('total', round(t + 0.5, 1), 's;', ', '.join(f"{s['id']} {s['end']-s['start']:.0f}s" for s in segs))
