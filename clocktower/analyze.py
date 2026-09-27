"""Experiment analysis across games: `python -m clocktower analyze games/v5/*/game-*`.

Groups games into cells by (good model, evil model) and reports, per cell: evil win rate with a
95% Wilson interval, how often executions hit evil, how good players vote, and the belief-probe
scores (probes.jsonl):
- demon%: the probability good seats put on the true Demon before nominations (higher = good
  is reading the table; lower = evil is hiding). Scored against the Demon at the time of the probe.
- brier: good seats' Brier score for "is X evil" over the other players (lower is better;
  always answering 2/8 scores about 0.19).
- tom: evil seats' mean absolute error when predicting the good seats' average demon% for each
  player (lower = evil knows what the town thinks).
"""
from __future__ import annotations
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

EVIL = {'Imp', 'Poisoner', 'Spy', 'Scarlet Woman', 'Baron'}


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _jsonl(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def game_metrics(path):
    path = Path(path)
    if not (path / 'result.json').exists():
        return None
    result = json.loads((path / 'result.json').read_text())
    config = json.loads((path / 'config.json').read_text()) if (path / 'config.json').exists() else {}
    events, probes = _jsonl(path / 'events.jsonl'), _jsonl(path / 'probes.jsonl')
    start = result.get('starting') or {}
    team = {n: 'evil' if c in EVIL else 'good' for n, c in start.items()}
    executed = [(e['day'], e['data']['player']) for e in events if e['kind'] == 'execution' and e['data']['died']]
    votes = defaultdict(list)  # nominee team -> good voters' yes/no
    for e in events:
        if e['kind'] == 'vote' and team.get(e['data']['voter']) == 'good':
            votes[team.get(e['data']['nominee'])].append(e['data']['yes'])
    m = {'game': str(path), 'seed': result.get('seed'), 'winner': result.get('winner'), 'days': result.get('days'),
         'good_model': config.get('good_model') or config.get('model'),
         'evil_model': config.get('evil_model') or config.get('model'), 'cost': result.get('cost', 0),
         'executions': len(executed), 'evil_executed': sum(team.get(p) == 'evil' for _, p in executed),
         'yes_on_evil': mean(votes['evil']), 'yes_on_good': mean(votes['good']),
         'errors': len(result.get('errors') or []), 'probe_cost': 0.0}
    for c in _jsonl(path / 'calls.jsonl'):
        if c.get('kind') == 'probe':
            m['probe_cost'] += c.get('cost', 0)
    # probes
    demon, brier, tom = defaultdict(list), [], []
    by_point = defaultdict(list)
    for r in probes:
        by_point[(r['day'], r['point'])].append(r)
    for (day, point), rs in by_point.items():
        truth = rs[0]['truth']
        imp = next((n for n, t in truth.items() if t['character'] == 'Imp'), None)
        good_reads = [r for r in rs if r['team'] == 'good' and r.get('players')]
        town = {}
        for n in truth:
            town[n] = mean([r['players'].get(n, {}).get('demon') for r in good_reads if n != r['player']])
        for r in good_reads:
            if point == 'nominations' and imp and imp in r['players']:
                demon[day].append(r['players'][imp]['demon'])
            b = [(v['evil'] - truth[n]['evil']) ** 2 for n, v in r['players'].items()
                 if n != r['player'] and v.get('evil') is not None]
            if b and point == 'nominations':
                brier.append(statistics.mean(b))
        for r in rs:
            if r['team'] == 'evil' and r.get('players'):
                err = [abs(v['demon'] - town[n]) for n, v in r['players'].items()
                       if v.get('demon') is not None and town.get(n) is not None]
                if err:
                    tom.append(statistics.mean(err))
    m['demon_by_day'] = {d: mean(v) for d, v in sorted(demon.items())}
    m['demon'] = mean([x for v in demon.values() for x in v if x is not None])
    m['brier'] = mean(brier)
    m['tom'] = mean(tom)
    m['probe_failures'] = sum(1 for r in probes if r.get('error') or not r.get('players'))
    return m


def fmt(x, pct=False):
    if x is None:
        return '  -  '
    return f'{100 * x:4.0f}%' if pct else f'{x:.3f}'


def main(paths):
    rows = [m for m in (game_metrics(p) for p in paths) if m]
    cells = defaultdict(list)
    for m in rows:
        cells[(m['good_model'], m['evil_model'])].append(m)
    print(f"{'good model':<18} {'evil model':<18} {'n':>3} {'evil win':>9} {'95% CI':>11} {'days':>5} "
          f"{'evil exec':>9} {'yes→evil':>8} {'yes→good':>8} {'demon%':>7} {'brier':>6} {'tom':>6} {'$/game':>7}")
    for (gm, em), ms in sorted(cells.items()):
        done = [m for m in ms if m['winner'] in ('good', 'evil')]
        k = sum(m['winner'] == 'evil' for m in done)
        lo, hi = wilson(k, len(done))
        ex = sum(m['executions'] for m in ms)
        print(f"{gm:<18} {em:<18} {len(ms):>3} {k:>3}/{len(done):<3}  {100 * lo:3.0f}–{100 * hi:3.0f}% "
              f"{mean([m['days'] for m in ms]):5.1f} "
              f"{fmt(sum(m['evil_executed'] for m in ms) / ex if ex else None, True):>9} "
              f"{fmt(mean([m['yes_on_evil'] for m in ms]), True):>8} {fmt(mean([m['yes_on_good'] for m in ms]), True):>8} "
              f"{fmt(mean([m['demon'] for m in ms]), True):>7} {fmt(mean([m['brier'] for m in ms])):>6} "
              f"{fmt(mean([m['tom'] for m in ms])):>6} {mean([m['cost'] for m in ms]):7.2f}")
    failures = sum(m['probe_failures'] for m in rows)
    errors = sum(m['errors'] for m in rows)
    if failures or errors:
        print(f'\n{failures} probe replies unparsed or failed; {errors} seat errors')
    return rows
