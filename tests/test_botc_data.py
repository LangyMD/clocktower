"""The Blood on the Clocktower reference data in docs/botc/data/ is internally consistent (no network)."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location('botc_data', ROOT / 'scripts' / 'botc_data.py')
botc_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(botc_data)


class BotcDataTest(unittest.TestCase):
    def test_consistent(self):
        self.assertEqual(botc_data.check(), [])

    def test_trouble_brewing_matches_engine(self):
        from clocktower import characters
        script = botc_data.load(botc_data.DATA / 'scripts' / 'trouble-brewing.json')
        data = {c['id']: c for c in botc_data.load(botc_data.DATA / 'characters.json')['characters']}
        names = {data[i]['name'] for i in script if isinstance(i, str) and data[i]['team'] != 'traveller'}
        self.assertEqual(names, set(characters.ALL))
        counts = botc_data.load(botc_data.DATA / 'setup-counts.json')['counts']
        for n, (t, o, m) in characters.SETUPS.items():
            self.assertEqual(counts[str(n)], {'townsfolk': t, 'outsider': o, 'minion': m, 'demon': 1})


if __name__ == '__main__':
    unittest.main()
