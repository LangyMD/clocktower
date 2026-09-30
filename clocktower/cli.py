"""Command line: run AI games, play as a human, simulate, or summarise.

    python -m clocktower run                          # nine Claude players, scripted Storyteller
    python -m clocktower run --days 1                 # stop after the first day (smoke test)
    python -m clocktower run --games 6 --parallel 3   # a batch, three games at a time
    python -m clocktower play --seat Casey            # you play Casey in the browser
    python -m clocktower sim --games 20               # random players, no API calls
    python -m clocktower report games/*               # summarise finished games
    python -m clocktower analyze games/v5/*/game-*    # win rates and belief-probe scores by model pairing
    python -m clocktower replay games/X --view Casey  # re-read a game from one seat (or public/omniscient)
    python -m clocktower watch                        # spectator app at http://127.0.0.1:8800
    python -m clocktower site                         # the spectator app as static files in site/, to publish
"""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import os
import random
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from .agents import HumanSeat, ModelSeat, RandomSeat
from .characters import MINIONS
from .game import ALL_NAMES, Game
from .llm import MODEL, Ledger, conversation, limiter, make_client, spec
from .prompts import player_system
from .schema import player_schema

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / 'games'
PROTOCOL = 'v12'  # bump when a change affects how games play, and describe it in games/PROTOCOLS.md
RUNS = GAMES / PROTOCOL  # new games go here by default
DEFAULT_WORKSPACE = 'wrkspc_01PGEHMDFBurkms3UW2GryQb'


@dataclass
class Shared:
    """One client, spend ledger and request limit for every game in this process."""
    client: object
    ledger: Ledger
    semaphore: object  # an asyncio.Semaphore, or llm.NoLimit


def shared(args):
    os.environ.setdefault('ANTHROPIC_WORKSPACE_ID', args.workspace)
    return Shared(make_client(), Ledger(GAMES / 'ledger.jsonl', cap=args.budget), limiter(args.concurrency))


def table_size(players, seed):
    """'12' is always 12 players; a range '10-12' picks one by seed (10 + seed % 3), so a side-swapped
    pair, which shares its seed, shares its table size too."""
    lo, _, hi = str(players).partition('-')
    lo, hi = int(lo), int(hi or lo)
    if not 5 <= lo <= hi <= 15:
        raise ValueError(f'--players must be within 5-15, got {players}')
    return lo + (seed or 0) % (hi - lo + 1)


def build(args, seed, out, env: Shared | None = None, human=None, minion=None):
    characters = args.characters.split(',') if args.characters else None
    names = ALL_NAMES[:len(characters) if characters else table_size(args.players, seed)]
    game = Game({}, None, names=names, seed=seed, private_beats=args.private_beats,
                public_beats=args.public_beats, max_days=args.days, waves=args.waves, characters=characters,
                minion=minion, out=out, probes=getattr(args, 'probes', False))
    if env is None:  # sim: random players, no API
        rng = random.Random(seed + 1)
        game.seats = {n: RandomSeat(n, random.Random(rng.random()), names) for n in names}
        return game, []
    ttl = '1h' if human else '5m'  # a human can take longer than five minutes between turns
    convs = []
    game.meta['models'] = {}

    def seat(name, team):  # called once the characters are dealt
        if name == human:
            game.meta['models'][name] = 'human'
            return HumanSeat(name)
        model = {'good': args.good_model, 'evil': args.evil_model}[team] or args.model
        effort = {'good': args.good_effort, 'evil': args.evil_effort}[team] or args.effort
        game.meta['models'][name] = model
        system = player_system(len(names), spec(model)['memory'])
        c = conversation(env.client, system, player_schema(names), label=name, ledger=env.ledger,
                         semaphore=env.semaphore, on_call=game.record_call, model=model, effort=effort,
                         max_tokens=args.max_output, ttl=ttl, flex=args.flex)
        convs.append((name, c))
        return ModelSeat(c)

    game.seat_factory = seat
    config = {'protocol': PROTOCOL, 'model': args.model, 'good_model': args.good_model, 'evil_model': args.evil_model,
              'player_effort': args.effort, 'good_effort': args.good_effort or args.effort,
              'evil_effort': args.evil_effort or args.effort, 'max_output_tokens': args.max_output,
              'good_memory': spec(args.good_model or args.model)['memory'],
              'evil_memory': spec(args.evil_model or args.model)['memory'], 'storyteller': 'scripted',
              'seed': seed,
              'private_beats': args.private_beats, 'public_beats': args.public_beats,
              'whispers': 'private', 'waves': args.waves, 'minion': minion,
              'max_days': args.days, 'human': human, 'characters': characters, 'probes': args.probes,
              'openai_tier': 'flex' if args.flex else 'default',
              'players': len(names), 'players_arg': str(args.players),
              'player_prompt_sha': hashlib.sha256(player_system(len(names)).encode()).hexdigest()[:12]}
    (out / 'config.json').write_text(json.dumps(config, indent=2))
    return game, convs


def save_conversations(game, convs):
    if not game.out:
        return
    d = game.out / 'conversations'
    d.mkdir(exist_ok=True)
    for name, c in convs:
        (d / f'{name}.json').write_text(json.dumps({'system': c.system, 'messages': c.messages}, indent=1))


def summary(result, out):
    t = result['tokens']
    print(f"\n{(result['winner'] or 'no winner').upper()} — {result['reason']}  (days: {result['days']})")
    print(f"cost ${result['cost']:.2f} over {result['calls']} calls, {result['seconds'] / 60:.1f} min; tokens: "
          f"{t['cache_read'] / 1e6:.2f}M cached, {t['cache_write'] / 1e6:.2f}M written, {t['input'] / 1e3:.0f}K uncached, "
          f"{t['output'] / 1e3:.0f}K output")
    print(f'logs: {out}')


async def play_one(args, seed, out, env, human=None, serve=None, minion=None):
    game, convs = build(args, seed, out, env, human, minion)
    if serve:
        serve(game)
    try:
        result = await game.run()
    finally:
        save_conversations(game, convs)
    summary(result, game.out)
    return result


async def run_batch(args):
    env = shared(args)
    base = args.seed if args.seed is not None else random.randrange(2 ** 32)
    stamp = time.strftime('%Y%m%d-%H%M%S')
    if args.games == 1 and not args.swap:
        out = Path(args.out) if args.out else RUNS / f'{stamp}-{base}'
        return [await play_one(args, base, out, env)]
    root = Path(args.out) if args.out else RUNS / f'batch-{stamp}'
    limit = asyncio.Semaphore(args.parallel or 10 ** 6)  # 0 = every game of the batch at once (swaps included)
    numbers = parse_only(args.only) if args.only else range(1, args.games + 1)

    swapped = argparse.Namespace(**{**vars(args), 'good_model': args.evil_model or args.model,
                                    'evil_model': args.good_model or args.model,
                                    'good_effort': args.evil_effort, 'evil_effort': args.good_effort})

    async def one(k, a=args, suffix=''):  # game k gets seed base + k - 1; the seed picks the Minion in play
        minion = MINIONS[(base + k - 1) % len(MINIONS)] if not args.characters else None
        out = root / f'game-{k:02d}{suffix}'
        done = out / 'result.json'
        if done.exists() and json.loads(done.read_text()).get('winner'):
            return json.loads(done.read_text())  # finished earlier: keep it (so a batch can be resumed)
        if out.exists():
            shutil.rmtree(out)  # an unfinished game restarts from scratch
        async with limit:
            return await play_one(a, base + k - 1, out, env, minion=minion)

    jobs = [one(k) for k in numbers]
    if args.swap:  # the same seed again with the models' sides swapped, so setup luck cancels in the pair
        jobs += [one(k, swapped, '-swap') for k in numbers]
    results = await asyncio.gather(*jobs)
    from .report import main as report
    report(sorted(str(p) for p in root.iterdir() if p.is_dir()))
    return results


def parse_only(spec):
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += range(int(a), int(b or a) + 1)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog='clocktower')
    sub = ap.add_subparsers(dest='command', required=True)
    rp = sub.add_parser('report')
    rp.add_argument('paths', nargs='+')
    an = sub.add_parser('analyze')
    an.add_argument('paths', nargs='+')
    sv = sub.add_parser('supervise', help='watch running batches; pause them on errors, lost turns or overspend')
    sv.add_argument('roots', nargs='+', help='batch directory prefixes, e.g. games/v8/t2')
    sv.add_argument('--max-spend', type=float, help='pause if these games cost more than this (USD)')
    sv.add_argument('--review-after', type=float, help='exit (without pausing) after this many minutes')
    wp = sub.add_parser('watch')
    wp.add_argument('--port', type=int, default=8800)
    wp.add_argument('--games', default=str(GAMES))
    sp = sub.add_parser('site')
    sp.add_argument('--games', default=str(GAMES))
    sp.add_argument('--out', default=str(ROOT / 'site'))
    fp = sub.add_parser('fetch', help='download game logs from the Hugging Face dataset (e.g. v9/e1-*)')
    fp.add_argument('patterns', nargs='+')
    rv = sub.add_parser('replay')
    rv.add_argument('path')
    rv.add_argument('--view', default='omniscient', help='a player name, public, or omniscient')
    rv.add_argument('--thinking', action='store_true', help='include thinking (omniscient or that player)')
    for name in ('run', 'play', 'sim'):
        p = sub.add_parser(name)
        p.add_argument('--seed', type=int)
        p.add_argument('--private-beats', type=int, default=3, help='whisper-only beats each day')
        p.add_argument('--public-beats', type=int, default=3, help='town-square beats before nominations')
        p.add_argument('--waves', type=int, default=3, help='groups per beat; later groups see earlier ones')
        p.add_argument('--days', type=int, default=15, help='stop after this many days')
        p.add_argument('--players', default='9', metavar='N or A-B',
                       help='table size, 5-15 (official Trouble Brewing setup for that count); a range such as '
                            '10-12 picks each game\'s size from its seed')
        p.add_argument('--characters', help='comma-separated forced setup, in seating order (tests)')
        p.add_argument('--out')
        if name in ('run', 'sim'):
            p.add_argument('--games', type=int, default=1)
        if name != 'sim':
            p.add_argument('--model', default=MODEL, help='player model')
            p.add_argument('--good-model', help='model for the good team (default --model)')
            p.add_argument('--evil-model', help='model for the evil team (default --model)')
            p.add_argument('--effort', default='high', help='player reasoning effort (same for every model)')
            p.add_argument('--good-effort', help='reasoning effort for the good team (default --effort)')
            p.add_argument('--evil-effort', help='reasoning effort for the evil team (default --effort)')
            p.add_argument('--max-output', type=int, default=32000,
                           help='per-turn output ceiling, thinking included, identical for every model')
            p.add_argument('--budget', type=float, default=1000.0, help='cap on total spend in games/ledger.jsonl')
            p.add_argument('--concurrency', type=int, default=0,
                           help='cap on API requests in flight (0 = no cap: every game and seat runs at once; '
                                'rate limits are handled by retries)')
            p.add_argument('--flex', action='store_true',
                           help='OpenAI Flex tier (half price, but throttled under load: calls can take minutes)')
            p.add_argument('--no-probes', dest='probes', action='store_false',
                           help='skip the out-of-game belief probes (probes.jsonl)')
            p.add_argument('--workspace', default=os.environ.get('ANTHROPIC_WORKSPACE_ID', DEFAULT_WORKSPACE))
        if name == 'run':
            p.add_argument('--parallel', type=int, default=0, help='games at once in a batch (0 = all)')
            p.add_argument('--only', help='run just these game numbers of the batch, e.g. 13,14,16-20')
            p.add_argument('--swap', action='store_true',
                           help='also play every seed with the good and evil models swapped (game-NN-swap)')
        if name == 'play':
            p.add_argument('--seat', default='Casey', choices=ALL_NAMES)
            p.add_argument('--port', type=int, default=8765)
    args = ap.parse_args(argv)
    if args.command == 'report':
        from .report import main as report
        report(args.paths)
    elif args.command == 'supervise':
        from .supervise import main as supervise
        raise SystemExit(supervise(args.roots, args.max_spend, args.review_after))
    elif args.command == 'analyze':
        from .analyze import main as analyze
        analyze(args.paths)
    elif args.command == 'watch':
        from .watch import serve as watch
        watch(args.games, args.port)
    elif args.command == 'site':
        from .site import build as build_site
        build_site(args.games, args.out)
    elif args.command == 'fetch':
        from .store import fetch
        print(fetch(args.patterns))
    elif args.command == 'replay':
        from .report import replay
        replay(args.path, args.view, args.thinking)
    elif args.command == 'run':
        asyncio.run(run_batch(args))
    elif args.command == 'play':
        from .web import serve

        async def go():
            seed = args.seed if args.seed is not None else random.randrange(2 ** 32)
            out = Path(args.out) if args.out else RUNS / f'{time.strftime("%Y%m%d-%H%M%S")}-{seed}-human'
            return await play_one(args, seed, out, shared(args), human=args.seat,
                                  serve=lambda g: serve(g, args.seat, args.port))
        asyncio.run(go())
    else:
        base = args.seed if args.seed is not None else random.randrange(2 ** 32)
        results = []
        for i in range(args.games):
            game, _ = build(args, base + i, None)
            results.append(asyncio.run(game.run()))
        wins = {w: sum(r['winner'] == w for r in results) for w in ('good', 'evil', None)}
        print(f'{args.games} random games: {wins}')
