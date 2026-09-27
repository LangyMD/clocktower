"""Summaries and replays of finished games.

    python -m clocktower report games/*                   # outcome, cost, speech and thinking stats
    python -m clocktower replay games/X --view Casey      # the game as Casey saw it
    python -m clocktower replay games/X --view public     # what the whole town saw
    python -m clocktower replay games/X --thinking        # omniscient, with every seat's thinking
"""
from __future__ import annotations
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def load(path):
    path = Path(path)
    result = json.loads((path / 'result.json').read_text()) if (path / 'result.json').exists() else None
    events = [json.loads(l) for l in (path / 'events.jsonl').read_text().splitlines()] if (path / 'events.jsonl').exists() else []
    calls = [json.loads(l) for l in (path / 'calls.jsonl').read_text().splitlines()] if (path / 'calls.jsonl').exists() else []
    return result, events, calls


def game_summary(path):
    result, events, calls = load(path)
    if not result:
        return None
    team = {n: ('evil' if c in ('Imp', 'Poisoner', 'Spy', 'Scarlet Woman', 'Baron') else 'good')
            for n, c in (result.get('starting') or {}).items()}
    thinking, per_day = defaultdict(list), defaultdict(float)
    for c in calls:
        t = c.get('usage', {}).get('output_tokens_details', {}).get('thinking_tokens', 0)
        thinking[team.get(c['label'], 'storyteller')].append(t)
        per_day[c.get('day')] += c.get('cost', 0)
    kinds = Counter(e['kind'] for e in events)
    words = sum(len(e['data'].get('text', '').split()) for e in events if e['kind'] in ('say', 'nomination', 'defense'))
    whisper_words = sum(len(e['data'].get('text', '').split()) for e in events if e['kind'] == 'whisper')
    latency = [c['latency'] for c in calls if 'latency' in c]
    return {
        'game': Path(path).name, 'winner': result['winner'], 'reason': result['reason'], 'days': result['days'],
        'cost': result['cost'], 'calls': result['calls'], 'minutes': round(result['seconds'] / 60, 1),
        'public_messages': kinds['say'], 'whispers': kinds['whisper'], 'nominations': kinds['nomination'],
        'public_words': words, 'whisper_words': whisper_words,
        'median_latency': round(statistics.median(latency), 1) if latency else None,
        'thinking_per_call': {k: round(statistics.mean(v)) for k, v in thinking.items() if v},
        'cost_by_day': {str(k): round(v, 2) for k, v in sorted(per_day.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))},
        'tokens': result['tokens'], 'setup': result.get('starting'),
    }


def main(paths):
    rows = [s for s in (game_summary(p) for p in paths) if s]
    for r in rows:
        print(f"{r['game']}: {str(r['winner']).upper()} after {r['days']} days — {r['reason']}")
        print(f"  ${r['cost']:.2f}, {r['calls']} calls, {r['minutes']} min, median call {r['median_latency']}s; "
              f"{r['public_messages']} public messages ({r['public_words']} words), {r['whispers']} whispers "
              f"({r['whisper_words']} words), {r['nominations']} nominations")
        print(f"  thinking tokens per call: {r['thinking_per_call']}; cost by day: {r['cost_by_day']}")
    if len(rows) > 1:
        wins = Counter(r['winner'] for r in rows)
        print(f"\n{len(rows)} games: good {wins['good']}, evil {wins['evil']}, unfinished {wins[None]}; "
              f"mean ${statistics.mean(r['cost'] for r in rows):.2f}/game, {statistics.mean(r['days'] for r in rows):.1f} days")
    return rows


def replay(path, view='omniscient', thinking=False):
    from .render import render
    _, events, _ = load(path)
    for ev in events:
        if ev['kind'] == 'thinking' and not (thinking and view in ('omniscient', ev['data']['player'])):
            continue
        viewer = 'omniscient' if ev['kind'] == 'thinking' else view
        if view == 'public':
            viewer = '(public)'
            if ev['to'] != 'public':
                continue
        text = render(ev, viewer, set(ev.get('dead', [])))
        if text is not None:
            print(text)
