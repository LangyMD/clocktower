"""The multiplayer table (web.py): lobby rules, seat assignment, and a whole game played by two
people through the API against practice bots (no API calls)."""
import argparse
import random
import tempfile
import time
import unittest

from clocktower.web import Table, assign, evil_seats
from clocktower.state import Grimoire


def args(out):
    return argparse.Namespace(model='random', good_model=None, evil_model=None, seed=7, private_beats=6,
                              public_beats=3, waves=3, days=15, effort='high', good_effort=None, evil_effort=None,
                              max_output=8000, flex=False, concurrency=0, workspace='x', out=out, cap=None,
                              minions=None, players='10')


class LobbyTest(unittest.TestCase):
    def test_assign_respects_teams(self):
        chars = ['Imp', 'Poisoner', 'Chef', 'Empath', 'Monk', 'Saint', 'Soldier']
        g = Grimoire([f'P{i}' for i in range(7)], chars)
        import random
        for k in range(30):
            seats = assign([('a', 'evil'), ('b', 'good'), ('c', 'any'), ('d', 'evil')], g.players, random.Random(k))
            self.assertEqual(len(set(seats.values())), 4)
            self.assertTrue(g[seats['a']].evil and g[seats['d']].evil)
            self.assertFalse(g[seats['b']].evil)

    def test_problems_count_only(self):
        t = Table(args(None))
        host = t.join('Host', 'evil', t.host_key)
        t.set_config(host, {'players': 5})
        for i in range(evil_seats(5)):
            t.join(f'E{i}', 'evil')
        self.assertIn('Too many people chose evil', t.problem())
        with self.assertRaises(PermissionError):
            t.set_config(t.join('Guest', 'good'), {'players': 9})
        self.assertNotIn('team', str(t.lobby(None)['people']))


class GameTest(unittest.TestCase):
    def test_two_people_play_a_whole_game(self):
        with tempfile.TemporaryDirectory() as d:
            t = Table(args(d))
            a = t.join('Ann', 'good', t.host_key)
            b = t.join('Bo', 'evil')
            t.set_config(a, {'players': 7})
            t.start(a)
            seen = {a: 0, b: 0}
            turns = 0
            rng = random.Random(3)
            deadline = time.time() + 60
            while t.status == 'playing' and time.time() < deadline:
                for tok in (a, b):
                    s = t.state(tok, seen[tok])
                    if not s.get('seated'):
                        continue
                    seen[tok] = s['next']
                    for ev in s['events']:  # a seat never sees another's night info or a private whisper
                        self.assertTrue(not ev['private'] or ev['kind'] in ('intro', 'info', 'notice', 'whisper'))
                    p = s['pending']
                    if p:
                        act = ({'vote': False} if p['kind'] == 'vote' else  # random targets: an Imp stuck on one dead player never ends
                               {'targets': rng.sample(p['options'], min(p['n_targets'], len(p['options'])))})
                        if p['kind'] == 'beat' and p['mode'] == 'private':
                            other = next(x['name'] for x in s['players'] if x['name'] != s['me']['seat'])
                            act = {'whispers': [{'to': [other], 'text': 'hello there'}]}
                        t.act(tok, {'turn': p['turn'], 'action': act})
                        turns += 1
                time.sleep(0.01)
            self.assertEqual(t.status, 'over', t.error)
            final = t.state(a, 0)
            self.assertTrue(final['reveal']['winner'] in ('good', 'evil'))
            people = {s['player'] for s in final['reveal']['seats'] if s['player']}
            self.assertEqual(people, {'Ann', 'Bo'})
            by = {s['player']: s for s in final['reveal']['seats'] if s['player']}
            self.assertFalse(by['Ann']['evil'])
            self.assertTrue(by['Bo']['evil'])
            self.assertGreater(turns, 10)
            self.assertIn('Night 1', t.transcript(a))


if __name__ == '__main__':
    unittest.main()
