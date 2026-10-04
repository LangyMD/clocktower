"""Play with friends against the AI players: `python -m clocktower play`, then open the link it prints.

One server holds a lobby and one game at a time. Everyone opens the same address on their own phone or
computer; joining gives that browser a private token for its seat. A person's seat sees exactly what a
model in that seat would see (the same rendered events, the same prompts) and answers the same requests
(whispers, speech, nominations, votes, night choices, Slayer shots) under the same word limits. Each
person's allegiance choice, and which seat they were dealt, stays secret from everyone else.

The page lives in clocktower/table/; this module is its JSON API and the game runner (a thread with its
own event loop, so the HTTP server stays responsive while the game waits on people and models).
"""
from __future__ import annotations
import argparse
import asyncio
import json
import os
import random
import secrets
import socket
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .agents import HumanSeat
from .characters import ABILITY, DEMONS, MINIONS, OUTSIDERS, SETUPS, TOWNSFOLK, kind
from .game import WORDS
from .llm import Ledger, limiter, make_client
from .prompts import player_system
from .render import render, visible

PAGE = Path(__file__).with_name('table')
TYPES = {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
         '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml'}

# What the lobby offers, strongest first: the 2026 rating (docs/plans/f2-ratings.json) and the fitted
# cost of one AI seat for one game (v16-v17 results), so a host can see roughly what a game costs.
MODELS = [
    ('gpt-6-astra', 'GPT-6 Astra', 1858, 1.85),
    ('gpt-6.1-sol', 'GPT-6.1 Sol', 1729, 0.11),
    ('claude-fable-5-1', 'Claude Fable 5.1', 1595, 2.66),
    ('gpt-5.6-sol', 'GPT-5.6 Sol', 1593, 0.74),
    ('claude-fable-5', 'Claude Fable 5', 1561, 10.43),
    ('claude-opus-5-5', 'Claude Opus 5.5', 1538, 0.85),
    ('gpt-5.5', 'GPT-5.5', 1472, 1.91),
    ('claude-opus-4-6', 'Claude Opus 4.6', 1427, 3.30),
    ('gpt-5.4', 'GPT-5.4', 1268, 3.87),
    ('claude-opus-4-7', 'Claude Opus 4.7', 1265, 2.77),
    ('claude-opus-4-8', 'Claude Opus 4.8', 1194, 8.44),
    ('random', 'Practice bots (random moves, free)', None, 0.0),
]
TEAMS = ('good', 'evil', 'any')


def available(model):
    """Whether this server holds the API key the model needs (so the lobby offers only playable models)."""
    if model == 'random':
        return True
    if model.startswith('openrouter:'):
        return bool(os.environ.get('OPENROUTER_API_KEY'))
    if model.startswith('claude'):
        return bool(os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('MY_ANTHROPIC_API_KEY'))
    return bool(os.environ.get('OPENAI_API_KEY'))
TIMERS = (0, 60, 120, 300, 600)  # seconds per turn; 0 = wait as long as it takes


def evil_seats(n):
    return SETUPS[n][2] + 1


def assign(people, players, rng):
    """Seats for people, given the dealt players: those who asked for evil get evil seats, good get
    good, the rest fill what is left. `people` is [(token, team)]; returns {token: seat name}."""
    evil = [p.name for p in players if p.evil]
    good = [p.name for p in players if not p.evil]
    rng.shuffle(evil)
    rng.shuffle(good)
    out = {}
    for want in ('evil', 'good', 'any'):
        for token, team in people:
            if team != want:
                continue
            pool = {'evil': evil, 'good': good}.get(team) or rng.choice([x for x in (evil, good) if x])
            out[token] = pool.pop()
    return out


def lan_address():
    """This machine's address on the local network (for friends' phones), or None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('10.255.255.255', 1))
            return s.getsockname()[0]
    except OSError:
        return None


class Table:
    """The lobby, the people at it, and the current game."""

    def __init__(self, args, runner=None):
        self.args = args
        self.lock = threading.RLock()
        self.people = {}       # token -> {name, team, host, seat}
        self.host_key = os.environ.get('CLOCKTOWER_HOST_KEY') or secrets.token_urlsafe(9)  # a fixed one for hosted servers
        fallback = next((m[0] for m in MODELS if available(m[0])), 'random')
        pick = lambda m: m if available(m) else fallback
        self.config = {'players': 10, 'good_model': pick(args.good_model or args.model),
                       'evil_model': pick(args.evil_model or args.model), 'timer': 0}
        self.status, self.error, self.game, self.result = 'lobby', None, None, None
        self.seats = {}        # seat name -> HumanSeat (current game)
        self.game_id = None
        self.runner = runner or run_game
        self.links = {}
        self.dealt = set()     # tokens of the people in the current game

    # ---- lobby ---------------------------------------------------------------------------------
    def join(self, name, team, host_key=None):
        name = ' '.join(str(name or '').split())[:24]
        if not name:
            raise ValueError('Enter a name.')
        if team not in TEAMS:
            raise ValueError('Choose good, evil or either.')
        with self.lock:
            if len(self.people) >= 15:
                raise ValueError('The table is full.')
            token = secrets.token_urlsafe(12)
            self.people[token] = {'name': name, 'team': team, 'host': host_key == self.host_key, 'seat': None}
            return token

    def person(self, token):
        p = self.people.get(token or '')
        if not p:
            raise PermissionError('Unknown player: join the table first.')
        return p

    def update_me(self, token, name=None, team=None):
        with self.lock:
            p = self.person(token)
            if name is not None:
                name = ' '.join(str(name).split())[:24]
                if name:
                    p['name'] = name
            if team is not None and self.status != 'playing':
                if team not in TEAMS:
                    raise ValueError('Choose good, evil or either.')
                p['team'] = team

    def claim_host(self, token, key):
        with self.lock:
            if key != self.host_key:
                raise PermissionError('That is not the host password.')
            self.person(token)['host'] = True

    def set_config(self, token, cfg):
        with self.lock:
            if not self.person(token)['host']:
                raise PermissionError('Only the host can change the table.')
            if self.status == 'playing':
                raise ValueError('A game is under way.')
            ids = {m[0] for m in MODELS} | {self.config['good_model'], self.config['evil_model']}
            if 'players' in cfg:
                n = int(cfg['players'])
                if not 5 <= n <= 15:
                    raise ValueError('Tables seat 5 to 15 players.')
                self.config['players'] = n
            for k in ('good_model', 'evil_model'):
                if k in cfg:
                    if cfg[k] not in ids:
                        raise ValueError(f'Unknown model {cfg[k]}.')
                    if not available(cfg[k]):
                        raise ValueError(f'This server has no API key for {cfg[k]}.')
                    self.config[k] = cfg[k]
            if 'timer' in cfg:
                t = int(cfg['timer'])
                if t not in TIMERS:
                    raise ValueError('Unknown timer.')
                self.config['timer'] = t

    def kick(self, token, target):
        with self.lock:
            if not self.person(token)['host']:
                raise PermissionError('Only the host can do that.')
            if self.status == 'playing':
                raise ValueError('A game is under way.')
            if target in self.people and target != token:
                del self.people[target]

    def problem(self):
        """Why the game can't start yet, or None. Counts only: never who chose what."""
        n, people = self.config['players'], list(self.people.values())
        if not people:
            return 'Nobody has joined.'
        if len(people) > n:
            return f'{len(people)} people have joined a {n}-player table: add seats.'
        evil = sum(p['team'] == 'evil' for p in people)
        good = sum(p['team'] == 'good' for p in people)
        if evil > evil_seats(n):
            return f'Too many people chose evil: a {n}-player table has {evil_seats(n)} evil seats.'
        if good > n - evil_seats(n):
            return f'Too many people chose good: a {n}-player table has {n - evil_seats(n)} good seats.'
        return None

    def start(self, token):
        with self.lock:
            if not self.person(token)['host']:
                raise PermissionError('Only the host can begin.')
            if self.status == 'playing':
                raise ValueError('A game is already under way.')
            why = self.problem()
            if why:
                raise ValueError(why)
            for p in self.people.values():
                p['seat'] = None
            self.status, self.error, self.result, self.game, self.seats = 'playing', None, None, None, {}
            self.game_id = secrets.token_hex(4)
            self.dealt = set(self.people)
            cfg = dict(self.config)
        threading.Thread(target=self._run, args=(cfg,), daemon=True).start()

    def humans(self, g):
        """Called by the engine once the characters are dealt: seats for the people at the table."""
        with self.lock:
            tokens = [(t, p['team']) for t, p in self.people.items() if t in self.dealt]
            seats = assign(tokens, g.players, random.Random())
            timeout = self.config['timer'] or None
            self.seats = {}
            for token, seat in seats.items():
                self.people[token]['seat'] = seat
                self.seats[seat] = HumanSeat(seat, timeout)
            return dict(self.seats)

    def _run(self, cfg):
        try:
            result = self.runner(self, cfg)
            with self.lock:
                self.result = result
                self.status = 'over'
        except Exception as e:
            traceback.print_exc()
            with self.lock:
                self.status, self.error = 'over', f'{type(e).__name__}: {e}'

    def reset(self, token):
        with self.lock:
            if not self.person(token)['host']:
                raise PermissionError('Only the host can do that.')
            if self.status == 'playing':
                raise ValueError('A game is under way.')
            self.status, self.game, self.result, self.error, self.seats = 'lobby', None, None, None, {}
            for p in self.people.values():
                p['seat'] = None

    # ---- views -----------------------------------------------------------------------------------
    def lobby(self, token, base=None):
        with self.lock:
            me = self.people.get(token or '')
            n = self.config['players']
            tf, os_, mn = SETUPS[n]
            return {
                'status': self.status, 'error': self.error, 'game': self.game_id,
                'me': None if not me else {'name': me['name'], 'team': me['team'], 'host': me['host'],
                                           'seated': bool(me['seat']), 'in_game': token in self.dealt},
                'people': [{'name': p['name'], 'host': p['host'], 'you': t == token,
                            **({'token': t} if me and me['host'] else {})} for t, p in self.people.items()],
                'config': self.config, 'setup': {'townsfolk': tf, 'outsiders': os_, 'minions': mn, 'demons': 1},
                'evil_seats': evil_seats(n), 'problem': self.problem(),
                'models': [{'id': i, 'name': nm, 'elo': elo, 'seat_cost': c} for i, nm, elo, c in MODELS
                           if available(i)],
                'timers': TIMERS, 'links': ({'friends': base, 'host': f'{base}/#host={self.host_key}'} if base else
                                            self.links) if me and me['host'] else {},
            }

    def state(self, token, since):
        with self.lock:
            p = self.person(token)
            seat, game = p['seat'], self.game
        if not game or not seat or not game.g:
            return {'status': self.status, 'seated': False, 'error': self.error}
        g = game.g
        events = []
        public_dead, ghosts_used = set(), set()
        evs = list(game.events)
        for ev in evs:  # deaths as the town knows them (the engine's own record runs ahead at night)
            k, d = ev['kind'], ev['data']
            if ev['to'] != 'public':
                continue
            if k == 'dawn':
                public_dead.update(d['deaths'])
            elif k in ('execution',) and d.get('died'):
                public_dead.add(d['player'])
            elif k == 'slayer' and d.get('died'):
                public_dead.add(d['target'])
            elif k == 'vote' and d.get('ghost'):
                ghosts_used.add(d['voter'])
        for ev in evs[since:]:
            if ev['kind'] == 'thinking' or not visible(ev, seat):
                continue
            text = render(ev, seat, set(ev['dead']))
            if text is None:
                continue
            events.append({'seq': ev['seq'], 'kind': ev['kind'], 'day': ev['day'], 'phase': ev['phase'],
                           'text': text.strip(), 'data': ev['data'], 'private': ev['to'] != 'public'})
        human = self.seats.get(seat)
        req = human.pending if human else None
        me = g[seat]
        start = game.starting or {}
        known = {}
        if start.get(seat) in MINIONS + DEMONS:  # what the evil team was told at the start
            for name, c in start.items():
                if name != seat and c in DEMONS:
                    known[name] = 'Demon'
                elif name != seat and c in MINIONS:
                    known[name] = 'Minion'
        over = bool(g.winner) or self.status == 'over'
        out = {
            'status': self.status, 'seated': True, 'game': self.game_id, 'next': len(evs), 'events': events,
            'me': {'seat': seat, 'character': me.shown, 'kind': kind(me.shown),
                   'evil': me.shown in MINIONS + DEMONS, 'ability': ABILITY[me.shown], 'known': known,
                   'bluffs': g.bluffs if start.get(seat) == 'Imp' else [], 'alive': seat not in public_dead},
            'players': [{'name': q.name, 'alive': q.name not in public_dead, 'ghost': q.name not in ghosts_used}
                        for q in g.players],
            'day': game.day, 'phase': game.phase,
            'pending': None if req is None else {
                'turn': human.turn, 'kind': req.kind, 'prompt': req.prompt, 'n_targets': req.n_targets,
                'options': req.options, 'alive': req.alive, 'mode': req.mode, 'beat': req.beat,
                'deadline': human.deadline, 'words': WORDS['vote' if req.kind == 'vote' else
                                                           'defense' if req.kind == 'defense' else 'beat'],
                'whisper_words': WORDS['whisper']},
            'waiting': req is None and not over,
            'spent': round(sum(c.get('cost', 0) for c in game.calls), 2),
            'over': over, 'error': self.error,
        }
        if over:
            models = game.meta.get('models', {})
            seat_of = {q['seat']: q['name'] for q in self.people.values() if q['seat']}
            out['reveal'] = {
                'winner': g.winner, 'reason': g.reason or (self.result or {}).get('stopped') or self.error,
                'seats': [{'name': q.name, 'character': q.character, 'started': start.get(q.name),
                           'shown': q.shown if q.shown != q.character else None, 'evil': q.evil,
                           'alive': q.alive, 'player': seat_of.get(q.name), 'model': models.get(q.name)}
                          for q in g.players],
                'bluffs': g.bluffs, 'red_herring': g.red_herring,
            }
        return out

    def act(self, token, body):
        with self.lock:
            seat = self.person(token)['seat']
            human = self.seats.get(seat)
        if not human or not human.pending:
            raise ValueError('It is not your turn.')
        if not human.submit(clean(body.get('action') or {}), body.get('turn')):
            raise ValueError('That turn has passed.')

    def rules(self):
        return {'text': player_system(self.config['players']),
                'characters': [{'name': c, 'kind': kind(c), 'ability': ABILITY[c]}
                               for c in TOWNSFOLK + OUTSIDERS + MINIONS + DEMONS]}

    def transcript(self, token):
        """The whole game with every seat's reasoning, once it is over."""
        self.person(token)
        game = self.game
        if not game or self.status != 'over' or not game.out or not (game.out / 'transcript.md').exists():
            raise ValueError('The chronicle opens when the game is over.')
        return (game.out / 'transcript.md').read_text()


def clean(a):
    """An action from the page, coerced to the schema's shape (the engine validates names and limits)."""
    s = lambda v: v if isinstance(v, str) else ''
    names = lambda v: [x for x in v if isinstance(x, str)][:3] if isinstance(v, list) else []
    whispers = [{'to': names(w.get('to')), 'text': s(w.get('text'))}
                for w in (a.get('whispers') or [])[:1] if isinstance(w, dict)]
    return {'say': s(a.get('say')), 'whispers': whispers,
            'nominate': a.get('nominate') if isinstance(a.get('nominate'), str) else None,
            'vote': a.get('vote') if isinstance(a.get('vote'), bool) else None,
            'targets': names(a.get('targets')),
            'slayer_shot': a.get('slayer_shot') if isinstance(a.get('slayer_shot'), str) else None}


def run_game(table, cfg):
    """Play one game for the table (in the server's game thread)."""
    from .cli import GAMES, Shared, play_one
    args = argparse.Namespace(**{**vars(table.args), 'players': str(cfg['players']), 'model': cfg['good_model'],
                                 'good_model': cfg['good_model'], 'evil_model': cfg['evil_model'],
                                 'characters': None, 'probes': False, 'seat_model': None})
    seed = args.seed if args.seed is not None else random.randrange(2 ** 32)
    out = Path(args.out or GAMES / 'play') / f'{time.strftime("%Y%m%d-%H%M%S")}-{seed}'

    def serve(game):
        with table.lock:
            table.game = game

    async def go():
        os.environ.setdefault('ANTHROPIC_WORKSPACE_ID', args.workspace)
        env = Shared(make_client(), Ledger(getattr(table.args, 'ledger', None) or GAMES / 'play' / 'ledger.jsonl', cap=table.args.cap), limiter(args.concurrency))
        return await play_one(args, seed, out, env, humans=table.humans, serve=serve)
    return asyncio.run(go())


def serve(table: Table, host='0.0.0.0', port=8765):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, ctype='application/json'):
            data = body.encode() if isinstance(body, str) else body
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def reply(self, fn):
            try:
                out = fn()
            except PermissionError as e:
                return self.send(403, json.dumps({'error': str(e)}))
            except (ValueError, KeyError, TypeError) as e:
                return self.send(400, json.dumps({'error': str(e)}))
            if isinstance(out, str):
                return self.send(200, out, 'text/plain; charset=utf-8')
            self.send(200, json.dumps(out if out is not None else {'ok': True}))

        def do_GET(self):
            url = urlparse(self.path)
            q = {k: v[0] for k, v in parse_qs(url.query).items()}
            token = self.headers.get('X-Token') or q.get('token')
            if url.path == '/api/lobby':
                host = self.headers.get('X-Forwarded-Host') or self.headers.get('Host') or ''
                proto = self.headers.get('X-Forwarded-Proto') or 'http'
                public = host and not host.split(':')[0] in ('localhost', '127.0.0.1')
                return self.reply(lambda: table.lobby(token, f'{proto}://{host}' if public else None))
            if url.path == '/api/state':
                return self.reply(lambda: table.state(token, int(q.get('since', 0))))
            if url.path == '/api/rules':
                return self.reply(table.rules)
            if url.path == '/api/transcript':
                return self.reply(lambda: table.transcript(token))
            name = 'index.html' if url.path in ('/', '/index.html') else url.path.lstrip('/')
            f = (PAGE / name).resolve()
            if PAGE.resolve() in f.parents and f.is_file() and f.suffix in TYPES:
                return self.send(200, f.read_bytes(), TYPES[f.suffix])
            self.send(404, '{}')

        def do_POST(self):
            url = urlparse(self.path)
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            except ValueError:
                return self.send(400, '{"error": "bad JSON"}')
            token = self.headers.get('X-Token') or body.get('token')
            routes = {
                '/api/join': lambda: {'token': table.join(body.get('name'), body.get('team'), body.get('host'))},
                '/api/me': lambda: table.update_me(token, body.get('name'), body.get('team')),
                '/api/host': lambda: table.claim_host(token, body.get('key')),
                '/api/config': lambda: table.set_config(token, body),
                '/api/kick': lambda: table.kick(token, body.get('target')),
                '/api/start': lambda: table.start(token),
                '/api/reset': lambda: table.reset(token),
                '/api/act': lambda: table.act(token, body),
            }
            if url.path not in routes:
                return self.send(404, '{}')
            self.reply(routes[url.path])

    server = ThreadingHTTPServer((host, port), Handler)
    lan = lan_address()
    local = f'http://localhost:{port}'
    table.links = {'host': f'{local}/#host={table.host_key}',
                   'friends': f'http://{lan}:{port}' if lan and host in ('0.0.0.0', '') else local}
    print(f'\n  Clocktower table is open.\n'
          f'  You (the host):  {table.links["host"]}\n'
          f'  Friends:         {table.links["friends"]}   (same Wi-Fi; or share a tunnel URL, see README)\n')
    return server
