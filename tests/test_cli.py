"""End-to-end smoke tests of the command line with random bots (no API calls, no keys needed)."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from clocktower import cli


def quiet(fn, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        result = fn(*args)
    return result, out.getvalue()


class CommandLineTests(unittest.TestCase):
    def test_a_random_bot_game_runs_end_to_end_and_writes_its_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'game'
            quiet(cli.main, ['run', '--model', 'random', '--seed', '7', '--out', str(out), '--no-probes'])
            result = json.loads((out / 'result.json').read_text())
            config = json.loads((out / 'config.json').read_text())
            self.assertIn(result['winner'], ('good', 'evil'))
            self.assertEqual(result['cost'], 0)
            self.assertEqual(config['protocol'], cli.PROTOCOL)
            self.assertEqual(config['players'], 10 + 7 % 3)  # --players 10-12 picks by seed
            self.assertTrue((out / 'events.jsonl').read_text().strip())
            self.assertIn('Night', (out / 'transcript.md').read_text())
            _, text = quiet(cli.main, ['replay', str(out), '--view', 'public'])
            self.assertTrue(text.strip())

    def test_a_side_swapped_batch_plays_both_games_on_one_seed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'batch'
            quiet(cli.main, ['run', '--good-model', 'random', '--evil-model', 'random', '--games', '1', '--swap',
                             '--seed', '11', '--out', str(root), '--no-probes', '--minions', 'Spy'])
            games = sorted(p.name for p in root.iterdir())
            self.assertEqual(games, ['game-01', 'game-01-swap'])
            seeds = {json.loads((root / g / 'config.json').read_text())['seed'] for g in games}
            self.assertEqual(seeds, {11})
            for g in games:
                self.assertEqual(json.loads((root / g / 'config.json').read_text())['minion'], 'Spy')
                self.assertTrue(json.loads((root / g / 'result.json').read_text())['winner'])

    def test_sim_and_help(self):
        _, text = quiet(cli.main, ['sim', '--games', '3', '--seed', '1'])
        self.assertIn('3 random games', text)
        with self.assertRaises(SystemExit) as done:
            quiet(cli.main, ['--help'])
        self.assertEqual(done.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
