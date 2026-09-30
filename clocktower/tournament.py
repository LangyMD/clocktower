"""Experiments as plan files: `python -m clocktower plan ...` writes one, `tournament PLAN` runs it.

A plan lists matchups (a good model and an evil model, optional efforts and per-seat overrides) and how
many side-swapped pairs each plays. `tournament` launches every matchup at once as its own `run`
process (one process per matchup, so one failure never stops the others), each with its own block of
seeds, and resumes: finished games are kept, unfinished ones restart. Logs go to `<out>/logs/`.

    python -m clocktower plan plans/models.json --within 10 --pairs 1 --seed 80000 --out games/v12/f1 > plans/f1.json
    python -m clocktower tournament plans/f1.json
"""
from __future__ import annotations
import itertools
import json
import subprocess
import sys
from pathlib import Path

SEEDS_PER_MATCHUP = 100  # matchup i uses seeds seed + 100*i onwards


def make_plan(models, within=None, pairs=1, seed=80000, out='games/v12/f1', players='10-12'):
    """Every pair of models at most `within` places apart in the list (all pairs if None)."""
    ms = [m if isinstance(m, dict) else {'id': m, 'short': m} for m in models]
    matchups = []
    for (i, a), (j, b) in itertools.combinations(enumerate(ms), 2):
        if within is None or j - i <= within:
            matchups.append({'name': f"{a['short']}-v-{b['short']}", 'good': a['id'], 'evil': b['id'], 'pairs': pairs})
    return {'out': out, 'seed': seed, 'players': players, 'matchups': matchups}


def commands(plan):
    for i, m in enumerate(plan['matchups']):
        cmd = [sys.executable, '-m', 'clocktower', 'run', '--games', str(m.get('pairs', 1)), '--swap',
               '--seed', str(plan['seed'] + SEEDS_PER_MATCHUP * i), '--players', str(plan.get('players', '10-12')),
               '--good-model', m['good'], '--evil-model', m['evil'], '--out', f"{plan['out']}-{m['name']}",
               '--budget', str(plan.get('budget', 100000))]
        for flag in ('good_effort', 'evil_effort'):
            if m.get(flag):
                cmd += [f"--{flag.replace('_', '-')}", m[flag]]
        for s in m.get('seat_models', []):
            cmd += ['--seat-model', s]
        cmd += m.get('args', [])  # any other run flags, e.g. ["--private-beats", "6"] for a protocol variant
        yield m['name'], cmd


def run(path, dry=False, only=None):
    """Launch the plan's matchups (or just those named in `only`, with the seeds and output folders
    they have in the full plan, so a pilot's games count toward the full run)."""
    plan = json.loads(Path(path).read_text())
    logs = Path(plan['out'] + '-logs')
    if not dry:
        logs.mkdir(parents=True, exist_ok=True)
    procs = []
    for name, cmd in commands(plan):
        if only and name not in only:
            continue
        if dry:
            print(' '.join(cmd))
            continue
        procs.append((name, subprocess.Popen(cmd, stdout=open(logs / f'{name}.log', 'w'), stderr=subprocess.STDOUT)))
    if dry:
        return 0
    print(f'launched {len(procs)} matchups; logs in {logs}/')
    failed = [name for name, p in procs if p.wait() != 0]
    print('all matchups finished' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if failed else 0
