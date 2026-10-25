"""Mixed-team analysis (pilot B, games/v17/b1-*): does a team of two models play at the average of its
members' ratings, and do seats favour their own model (whispers, votes)?

Prediction: team strength = mean of its seats' combined ratings (docs/plans/f2-ratings.json), plus the
good-side edge and setup terms, as in the rating fit. In-group: among whispers from one mixed-team seat
to others on the mixed team, the share going to the same model vs the share expected if recipients were
picked without regard to model; vote agreement of same-model vs cross-model pairs on the mixed team.
Intervals: bootstrap over side-swapped pairs.

    python -m clocktower mixed [GAMES_PREFIX]   # default games/v17/b1-; results in docs/analysis/b1-mixed-pilot.json
"""
import json, glob, sys, random, collections
from pathlib import Path
from .characters import MINIONS

REPO = Path(__file__).resolve().parent.parent
ROOT = 'games/v17/b1-'
R = json.loads((REPO / 'docs/plans/f2-ratings.json').read_text())
RATING = {m['id']: m['combined'] for m in R['models']}
H, SETUP = R['good_advantage'], R['setup_effects']
SOLO = 'gpt-6.1-sol'


def p_good(good, evil, inplay, n):
    d = sum(RATING[m] for m in good) / len(good) - sum(RATING[m] for m in evil) / len(evil) + H
    d += sum(SETUP[m] for m in ('Spy', 'Scarlet Woman', 'Baron') if m in inplay)
    d += SETUP.get(f'{n} players', 0)
    return 1 / (1 + 10 ** (-d / 400))


def games(root=ROOT):
    out = []
    for d in sorted(glob.glob(root + '*/game-*')):
        try:
            r = json.load(open(d + '/result.json'))
        except FileNotFoundError:
            continue
        if r.get('winner') not in ('good', 'evil'):
            continue
        evil = {s for s, c in r['starting'].items() if c in MINIONS or c == 'Imp'}
        models = r['models']
        mixed_side = 'evil' if any(models[s] != SOLO for s in evil) else 'good'
        team = {s for s in models if (s in evil) == (mixed_side == 'evil')}
        ev = [json.loads(l) for l in open(d + '/events.jsonl')]
        out.append({'dir': d, 'r': r, 'evil': evil, 'models': models,
                    'side': mixed_side, 'team': team, 'events': ev})
    return out


def summarise(gs):
    res = {'games': len(gs), 'by_side': {}}
    for side in ('good', 'evil'):
        sub = [g for g in gs if g['side'] == side]
        won = sum(g['r']['winner'] == side for g in sub)
        pred = {}
        for label, sub_model in (('mixed (average)', None), ('all Opus 5.5', 'claude-opus-5-5'), ('all GPT-5.6 Sol', 'gpt-5.6-sol')):
            tot = 0
            for g in sub:
                inplay = set(g['r']['starting'].values())
                good = [g['models'][s] for s in g['models'] if s not in g['evil']]
                evil = [g['models'][s] for s in g['evil']]
                if sub_model:
                    good = [sub_model if m != SOLO else m for m in good]
                    evil = [sub_model if m != SOLO else m for m in evil]
                p = p_good(good, evil, inplay, len(g['models']))
                tot += p if side == 'good' else 1 - p
            pred[label] = round(tot, 2)
        res['by_side'][side] = {'games': len(sub), 'mixed_won': won, 'expected_wins': pred}
    # in-group whispers
    same = exp = n = 0
    for g in gs:
        for e in g['events']:
            if e['kind'] != 'whisper':
                continue
            s = e['data']['from']
            if s not in g['team']:
                continue
            pool = [q for q in g['team'] if q != s]
            chance = sum(g['models'][q] == g['models'][s] for q in pool) / len(pool)
            for t in e['data']['to']:
                if t in g['team']:
                    n += 1; same += g['models'][t] == g['models'][s]; exp += chance
    res['whispers'] = {'to_teammates': n, 'same_model': same, 'expected_same': round(exp, 1)}
    # vote agreement
    agree = collections.Counter(); pairs = collections.Counter()
    for g in gs:
        votes = collections.defaultdict(dict)
        for e in g['events']:
            if e['kind'] == 'vote' and e['data']['voter'] in g['team']:
                votes[(e['day'], e['data']['nominee'])][e['data']['voter']] = e['data']['yes']
        for vs in votes.values():
            ss = sorted(vs)
            for i in range(len(ss)):
                for j in range(i + 1, len(ss)):
                    k = 'same' if g['models'][ss[i]] == g['models'][ss[j]] else 'cross'
                    pairs[k] += 1; agree[k] += vs[ss[i]] == vs[ss[j]]
    res['votes'] = {k: {'pairs': pairs[k], 'agree': round(agree[k] / pairs[k], 3) if pairs[k] else None} for k in ('same', 'cross')}
    return res


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    gs = games(argv[0] if argv else ROOT)
    res = summarise(gs)
    # bootstrap over side-swapped pairs: whisper excess and vote gap
    by = collections.defaultdict(list)
    for g in gs:
        by[g['dir'].replace('-swap', '')].append(g)
    keys = list(by); rng = random.Random(0); W, V = [], []
    for _ in range(1000):
        s = summarise([g for k in (rng.choice(keys) for _ in keys) for g in by[k]])
        w = s['whispers']
        if w['to_teammates']:
            W.append((w['same_model'] - w['expected_same']) / w['to_teammates'])
        v = s['votes']
        if v['same']['agree'] is not None and v['cross']['agree'] is not None:
            V.append(v['same']['agree'] - v['cross']['agree'])
    q = lambda xs: [round(sorted(xs)[int(.05 * len(xs))], 3), round(sorted(xs)[int(.95 * len(xs))], 3)]
    res['whispers']['excess_share_90'] = q(W); res['votes']['gap_90'] = q(V)
    print(json.dumps(res, indent=1))
    return res


if __name__ == '__main__':
    main()
