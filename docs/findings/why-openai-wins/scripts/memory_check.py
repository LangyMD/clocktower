"""Does each model's next request still contain its previous turn's output (thinking included)?
For consecutive committed turns of a seat after a turn with >=300 thinking tokens: growth of the billed context
minus the previous turn's output tokens. Negative = the earlier output (its thinking) was dropped from context.
python docs/findings/why-openai-wins/scripts/memory_check.py"""
import json, glob, collections, statistics as st
res = collections.defaultdict(list)
for d in sorted(glob.glob('games/v17/f3-*/game-*')):
    by = collections.defaultdict(list)
    for l in open(d + '/calls.jsonl'):
        r = json.loads(l)
        if r['kind'] != 'probe': by[r['label']].append(r)
    for rs in by.values():
        turns = []
        for r in rs:
            if r['attempt'] == 0: turns.append(r)
            elif turns: turns[-1] = r
        prev = None
        for r in turns:
            u = r['usage']; ctx = u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0)
            th = (u.get('output_tokens_details') or {}).get('thinking_tokens', 0) or 0
            if prev and prev[2] >= 300: res[r['model']].append(ctx - prev[0] - prev[1])
            prev = (ctx, u['output_tokens'], th)
for m, v in sorted(res.items()):
    print(f"{m:18s} n={len(v):5d}  context grew by less than the previous output: {sum(x < 0 for x in v)/len(v):.1%}  median surplus {st.median(v):.0f}")
