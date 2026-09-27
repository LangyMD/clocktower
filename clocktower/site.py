"""Build the spectator viewer as static files for publishing: `python -m clocktower site`.

Writes site/index.html (the page body; the host adds the document skeleton), the viewer's
style.css and app.js, data/index.json (every game's summary) and one bundle per batch,
data/<batch>.json, mapping each game id to what `watch` would serve for it.
"""
from __future__ import annotations
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

from .watch import VIEWER, game, index


def bundle_name(batch):
    return (batch or 'single').replace('/', '--') + '.json'


def build(root, out):
    root, out = Path(root), Path(out)
    if out.exists():
        shutil.rmtree(out)
    (out / 'data').mkdir(parents=True)
    games = [dict(g, live=False) for g in index(root)]
    batches = defaultdict(dict)
    for g in games:
        data = game(root, g['id'], 0)
        data['summary'] = dict(data['summary'], live=False)
        batches[g['batch']][g['id']] = data
    (out / 'data' / 'index.json').write_text(json.dumps(games))
    for batch, content in batches.items():
        (out / 'data' / bundle_name(batch)).write_text(json.dumps(content, separators=(',', ':')))
    for name in ('style.css', 'app.js'):
        shutil.copy(VIEWER / name, out / name)
    html = (VIEWER / 'index.html').read_text()
    head = re.search(r'<head>(.*)</head>', html, re.S).group(1)
    body = re.search(r'<body>(.*)</body>', html, re.S).group(1)
    head = re.sub(r'<meta[^>]*>\s*', '', head).replace('<title>Clocktower</title>', '<title>Clocktower Chronicles</title>')
    body = body.replace('<script src="app.js"></script>', '<script>window.CLOCKTOWER_STATIC = true;</script>\n<script src="app.js"></script>')
    (out / 'index.html').write_text(head.strip() + '\n' + body.strip() + '\n')
    files = sorted(str(p.relative_to(out)) for p in out.rglob('*') if p.is_file() and p.name != 'index.html')
    print(f'Built {out}: {len(games)} games in {len(batches)} batches, {len(files) + 1} files')
    return files
