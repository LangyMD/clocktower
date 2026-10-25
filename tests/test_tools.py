"""Experiment tooling: plans' Minion balancing and the ratings fit (no API, no game logs needed)."""
import collections
import json
import random
import tempfile
import unittest
from pathlib import Path

from clocktower.characters import MINIONS
from clocktower.ratings import fit, load, ratings
from clocktower.tournament import assign_minions, commands, make_plan


def minion_flags(plan):
    out = {}
    for name, cmd in commands(plan):
        out[name] = cmd[cmd.index('--minions') + 1].split(',') if '--minions' in cmd else None
    return out


class MinionTests(unittest.TestCase):
    def test_a_round_robin_with_one_pair_each_deals_every_minion_evenly(self):
        models = [f'm{i}' for i in range(8)]
        plan = make_plan(models, pairs=1, seed=80000, out='x')  # seeds step by 100: by seed alone, all Poisoner
        got = assign_minions(plan)
        total = collections.Counter(m for ms in got.values() for m in ms)
        self.assertEqual(sum(total.values()), 28)
        self.assertEqual(set(total.values()), {7})
        per = collections.defaultdict(collections.Counter)
        for m in plan['matchups']:
            for x in got[m['name']]:
                per[m['good']][x] += 1; per[m['evil']][x] += 1
        for model in models:  # 7 opponents each: every Minion 1-2 times
            self.assertLessEqual(max(per[model].values()) - min(per[model][x] for x in MINIONS), 1, model)

    def test_a_matchup_with_several_pairs_cycles(self):
        plan = make_plan(['a', 'b'], pairs=4, out='x')
        self.assertEqual(sorted(assign_minions(plan)['a-v-b']), sorted(MINIONS))

    def test_forced_minions_are_kept_and_counted(self):
        plan = make_plan(['a', 'b', 'c'], pairs=1, out='x')
        plan['matchups'][0]['args'] = ['--minions', 'Spy']
        plan['matchups'][1]['minions'] = ['Baron']
        flags = minion_flags(plan)
        self.assertEqual(flags['a-v-b'], ['Spy'])
        self.assertEqual(flags['a-v-c'], ['Baron'])
        self.assertNotIn(flags['b-v-c'][0], ('Spy', 'Baron'))  # b already had Spy, c already had Baron
        cmd = dict(commands(plan))['a-v-b']
        self.assertEqual(cmd.count('--minions'), 1)  # an explicit flag is passed once, as written

    def test_choices_depend_on_the_whole_plan_so_a_single_game_rerun_matches(self):
        plan = make_plan([f'm{i}' for i in range(5)], pairs=2, out='x')
        full = minion_flags(plan)
        for name, cmd in commands(plan, per_game=True):
            self.assertEqual(cmd[cmd.index('--minions') + 1].split(','), full[name.split('/')[0]])

    def test_forced_setups_get_no_minion(self):
        plan = make_plan(['a', 'b'], out='x')
        plan['matchups'][0]['args'] = ['--characters', 'Imp,Spy,Chef,Saint,Monk']
        self.assertIsNone(minion_flags(plan)['a-v-b'])


def synthetic(strength, n_pairs=60, h=0.4, seed=3):
    """Side-swapped pairs between random models, won by the true model + h (logits)."""
    rng = random.Random(seed); names = list(strength); games = []
    for i in range(n_pairs):
        a, b = rng.sample(names, 2)
        minions = [rng.random() < 0.25 for _ in range(3)]; players = rng.choice((10, 11, 12))
        for good, evil in ((a, b), (b, a)):
            p = 1 / (1 + 2.718281828 ** -(strength[good] - strength[evil] + h))
            games.append({'pair': f'x/game-{i}', 'good': good, 'evil': evil, 'won': rng.random() < p,
                          'minions': minions, 'players': players})
    return games


class FitTests(unittest.TestCase):
    def test_fit_recovers_the_order_and_centres_on_1500(self):
        strength = {'weak': -1.5, 'mid': 0.0, 'strong': 1.5}
        games = synthetic(strength, n_pairs=300)
        comb, none, extra = fit(games, list(strength))
        self.assertIsNone(none)
        self.assertAlmostEqual(sum(comb.values()) / 3, 1500, places=6)
        self.assertLess(comb['weak'], comb['mid']); self.assertLess(comb['mid'], comb['strong'])
        self.assertGreater(extra[-1], 0)  # good-side advantage
        det, dec, _ = fit(games, list(strength), split=True)
        self.assertLess(det['weak'], det['strong']); self.assertLess(dec['weak'], dec['strong'])

    def test_ratings_json_shape_and_records(self):
        strength = {'a': -0.5, 'b': 0.5}
        models = [{'id': 'a', 'released': '2026-02-01', 'lab': 'X'}, {'id': 'b', 'released': '2026-06-01', 'lab': 'Y'}]
        games = synthetic(strength, n_pairs=20)
        out = ratings(games, models, boot=5)
        self.assertEqual(out['games'], 40)
        a = out['models'][0]
        self.assertEqual(a['good_games'] + a['evil_games'], 40)
        self.assertEqual(sum(m['good_wins'] for m in out['models']) / 40, 1 - out['evil_win_rate'])
        self.assertEqual(set(out['setup_effects']), {'Spy', 'Scarlet Woman', 'Baron', '11 players', '12 players'})
        self.assertEqual(out, ratings(games, models, boot=5))  # deterministic

    def test_load_reads_finished_games_and_drops_opus48_v16(self):
        with tempfile.TemporaryDirectory() as root:
            def game(path, good, evil, winner, chars):
                d = Path(root, path); d.mkdir(parents=True)
                (d / 'config.json').write_text(json.dumps({'good_model': good, 'evil_model': evil, 'players': len(chars)}))
                (d / 'result.json').write_text(json.dumps({'winner': winner}))
                seats = [{'character': c} for c in chars]
                (d / 'events.jsonl').write_text(json.dumps({'kind': 'setup', 'data': {'seats': seats}}) + '\n')
            chars = ['Imp', 'Spy', 'Baron'] + ['Chef'] * 8
            game('v17/f3-a-v-b/game-01', 'a', 'b', 'good', chars)
            game('v17/f3-a-v-b/game-01-swap', 'b', 'a', 'evil', chars)
            game('v17/f3-a-v-b/game-02', 'a', 'b', None, chars)  # stopped
            game('v16/f2-a-v-o/game-01', 'a', 'claude-opus-4-8', 'good', chars)  # dropped
            game('v16/f2-a-v-b/game-01', 'a', 'b', 'evil', chars[:10])
            gs = sorted(load(root), key=lambda g: (g['pair'], g['good']))
            self.assertEqual(len(gs), 3)
            self.assertEqual([g['pair'] for g in gs], ['f2-a-v-b/game-01', 'f3-a-v-b/game-01', 'f3-a-v-b/game-01'])
            self.assertEqual(gs[1]['minions'], [True, False, True])
            self.assertEqual((gs[1]['players'], gs[0]['players']), (11, 10))


if __name__ == '__main__':
    unittest.main()
