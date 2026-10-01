"""Relaunch, one process per game, every game of a plan that stopped (seat failed / halted) and isn't
running: each resumes from its last checkpoint. Usage: python scripts/resume_stopped.py PLAN.json [--dry-run]"""
import json, subprocess, sys
from pathlib import Path
plan_path = sys.argv[1]; plan = json.load(open(plan_path))
running = subprocess.run(['pgrep', '-af', 'clocktower run'], capture_output=True, text=True).stdout
names = []
for m in plan['matchups']:
    root = Path(f"{plan['out']}-{m['name']}")
    for d in sorted(root.glob('game-*')):
        r = d / 'result.json'
        if not r.exists() or json.loads(r.read_text()).get('winner') or (d / 'STOP').exists():
            continue
        k = int(d.name.split('-')[1]); swap = d.name.endswith('-swap')
        if f"--out {root} " in running and f"--only {k} --side {'swap' if swap else 'normal'}" in running:
            continue
        names.append(f"{m['name']}/g{k:02d}{'-swap' if swap else ''}")
print(len(names), 'stopped games:', ' '.join(names))
if names and '--dry-run' not in sys.argv:
    subprocess.Popen([sys.executable, '-m', 'clocktower', 'tournament', plan_path, '--only', ','.join(names)],
                     stdout=open(f"{plan['out']}-resume.log", 'a'), stderr=subprocess.STDOUT, start_new_session=True)
