"""Watch a running experiment and pause it when something is wrong.

    python -m clocktower supervise games/v8/t2 --max-spend 400 --review-after 20

Every minute it reads the games under the given directories and checks, per model: games stopped
by a failed seat, turns lost (truncated or refused twice, so the seat passed), the share of game
calls that hit the output ceiling, refusals, stalls (no new calls for 10 minutes) and spend. On any
alarm it kills the batch processes writing there and exits with a report, so a broken run costs
minutes, not the whole budget. With --review-after it also exits (without pausing) after that many
minutes, as a checkpoint for reading transcripts.
"""
from __future__ import annotations
import glob
import json
import os
import signal
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path


def scan(roots):
    games = [d for r in roots for d in sorted(glob.glob(f'{r}*/game-*'))]
    s = {'games': len(games), 'done': 0, 'stopped': [], 'calls': Counter(), 'capped': Counter(),
         'lost': Counter(), 'refused': Counter(), 'cost': 0.0, 'last_call': 0.0, 'days': Counter()}
    for d in games:
        res = Path(d, 'result.json')
        if res.exists():
            r = json.loads(res.read_text())
            if r.get('winner'):
                s['done'] += 1
            elif r.get('stopped'):
                s['stopped'].append(f"{d}: {r['stopped'][:160]}")
        calls = Path(d, 'calls.jsonl')
        if not calls.exists():
            continue
        s['last_call'] = max(s['last_call'], calls.stat().st_mtime)
        for line in calls.read_text().splitlines():
            c = json.loads(line)
            s['cost'] += c.get('cost', 0)
            if c.get('kind') == 'probe':
                continue
            m = c['model']
            s['calls'][m] += 1
            if c['stop'] == 'max_tokens':
                s['capped'][m] += 1
                s['lost'][m] += c.get('attempt', 0) >= 1
            if c['stop'] == 'refusal':
                s['refused'][m] += 1
                s['lost'][m] += c.get('attempt', 0) >= 1
        events = Path(d, 'events.jsonl')
        if events.exists() and not res.exists():
            lines = events.read_text().splitlines()
            if lines:
                s['days'][json.loads(lines[-1])['day']] += 1
    return s


SYSTEMIC = ('credit balance', 'spend limit', 'insufficient_quota', 'authentication', 'permission', 'invalid_request')


def alarms(s, max_spend, cap_rate=0.01, lost_rate=0.005, refusal_rate=0.01, min_calls=100, max_stopped=3):
    """Reasons to pause. A single stopped game (a transient API error) is not one: it is rerun afterwards.
    Pause on a systemic stop reason (credit, quota, auth, a bad request) or several stopped games."""
    systemic = [x for x in s['stopped'] if any(k in x.lower() for k in SYSTEMIC)]
    out = [f'game stopped: {x}' for x in systemic]
    if len(s['stopped']) >= max_stopped:
        out.append(f'{len(s["stopped"])} games stopped: ' + '; '.join(x[:120] for x in s['stopped'][:3]))
    for m, n in s['calls'].items():
        if n < min_calls:
            continue
        if s['capped'][m] / n > cap_rate:
            out.append(f'{m}: {s["capped"][m]}/{n} game calls hit the output ceiling')
        if s['lost'][m] / n > lost_rate:
            out.append(f'{m}: {s["lost"][m]} turns lost (seat passed)')
        if s['refused'][m] / n > refusal_rate:
            out.append(f'{m}: {s["refused"][m]}/{n} refusals')
    if max_spend and s['cost'] > max_spend:
        out.append(f'spend ${s["cost"]:.0f} is over the planned ${max_spend:.0f}')
    return out


def report(s):
    lines = [f"{s['done']}/{s['games']} games done, {len(s['stopped'])} stopped, ${s['cost']:.0f} spent; "
             f"unfinished games by day: {dict(sorted(s['days'].items()))}"]
    for m in sorted(s['calls']):
        n = s['calls'][m]
        lines.append(f'  {m:<28} {n:6d} calls  capped {s["capped"][m]:3d}  lost {s["lost"][m]:3d}  refused {s["refused"][m]:3d}')
    return '\n'.join(lines)


def pause(roots):
    """Kill the batch processes writing under these directories."""
    out = subprocess.run(['pgrep', '-af', '^python -m clocktower run'], capture_output=True, text=True).stdout
    for line in out.splitlines():
        pid, cmd = line.split(' ', 1)
        if any(f'--out {r}' in cmd for r in roots):
            os.kill(int(pid), signal.SIGTERM)


def main(roots, max_spend=None, review_after=None, every=60, stall=600):
    start = time.time()
    while True:
        s = scan(roots)
        found = alarms(s, max_spend)
        running = subprocess.run(['pgrep', '-f', '^python -m clocktower run'], capture_output=True).returncode == 0
        if running and s['last_call'] and time.time() - s['last_call'] > stall:
            found.append(f'no new calls for {int(time.time() - s["last_call"])}s')
        if found:
            pause(roots)
            print('PAUSED\n' + '\n'.join(found) + '\n' + report(s))
            return 1
        if not running and s['games']:
            print('FINISHED\n' + report(s))
            return 0
        if review_after and time.time() - start > review_after * 60:
            print('CHECKPOINT (still running)\n' + report(s))
            return 0
        time.sleep(every)
