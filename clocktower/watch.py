"""Spectator app: `python -m clocktower watch` then open http://127.0.0.1:8800

Serves the viewer in clocktower/viewer/ and read-only JSON about the games under
games/: an index of every game and each game's events, incrementally, so running
games can be followed live.
"""
from __future__ import annotations
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VIEWER = Path(__file__).with_name('viewer')
TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
         '.svg': 'image/svg+xml'}
EVIL = {'Imp', 'Poisoner', 'Spy', 'Scarlet Woman', 'Baron'}
LIVE_SECONDS = 180  # a game without a result that has written an event recently is live


def _json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def summary(root, d):
    events = d / 'events.jsonl'
    result, config = _json(d / 'result.json'), _json(d / 'config.json') or {}
    rel = d.relative_to(root)
    models = sorted(set((result or {}).get('models', {}).values())) or \
        sorted({m for m in (config.get('good_model'), config.get('evil_model'), config.get('model')) if m})
    return {
        'id': str(rel), 'name': rel.name, 'batch': str(rel.parent) if str(rel.parent) != '.' else '',
        'winner': (result or {}).get('winner'), 'reason': (result or {}).get('reason'),
        'days': (result or {}).get('days'), 'cost': (result or {}).get('cost'),
        'finished': result is not None,
        'live': result is None and time.time() - events.stat().st_mtime < LIVE_SECONDS,
        'updated': events.stat().st_mtime, 'models': models, 'human': config.get('human'),
        'storyteller': config.get('storyteller_model') or config.get('storyteller'),
    }


def index(root):
    games = [summary(root, p.parent) for p in root.rglob('events.jsonl') if 'logs' not in p.parts]
    return sorted(games, key=lambda g: (g['batch'], g['name']))


def game(root, gid, since):
    d = (root / gid).resolve()
    if root.resolve() not in d.parents or not (d / 'events.jsonl').exists():
        return None
    lines = (d / 'events.jsonl').read_text().splitlines()
    events = []
    for line in lines[since:]:
        try:
            events.append(json.loads(line))
        except ValueError:  # a line still being written
            break
    return {'summary': summary(root, d), 'events': events, 'next': since + len(events),
            'result': _json(d / 'result.json'), 'config': _json(d / 'config.json')}


def serve(root, port=8800):
    root = Path(root)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, body, ctype='application/json'):
            data = body if isinstance(body, bytes) else body.encode()
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            url = urlparse(self.path)
            q = parse_qs(url.query)
            if url.path == '/api/games':
                return self.send(200, json.dumps(index(root)))
            if url.path == '/api/game':
                data = game(root, q.get('id', [''])[0], int(q.get('since', ['0'])[0]))
                return self.send(200, json.dumps(data)) if data else self.send(404, '{}')
            name = 'index.html' if url.path in ('/', '') else url.path.lstrip('/')
            f = (VIEWER / name).resolve()
            if f.parent == VIEWER.resolve() and f.suffix in TYPES and f.exists():
                return self.send(200, f.read_bytes(), TYPES[f.suffix])
            self.send(404, 'not found', 'text/plain')

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'Watching {root} — open http://127.0.0.1:{port}')
    server.serve_forever()
