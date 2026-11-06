"""Keep docs/botc/data/ in step with the official Blood on the Clocktower toolmaker resources.

The Pandemonium Institute publishes character data for toolmakers in the botc-release repository
(https://github.com/ThePandemoniumInstitute/botc-release, resources/data/), under its Community Created Content
Policy. This script downloads that data into docs/botc/data/official/ (git-ignored, so the official ability text
is never committed here) and refreshes the structural fields of docs/botc/data/characters.json from it: names,
types, editions, setup flags, reminder tokens, night order and jinx pairs. Our own fields (summary, tags, setup
notes) are kept as they are; a character that is new upstream gets a stub with an empty summary to fill in.

    python scripts/botc_data.py fetch     # download the official files (needs network)
    python scripts/botc_data.py build     # refresh characters.json, night-order.json, jinxes.json
    python scripts/botc_data.py check     # offline consistency checks (also run by tests/test_botc_data.py)
"""
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'docs' / 'botc' / 'data'
OFFICIAL = DATA / 'official'
SOURCE = 'https://raw.githubusercontent.com/ThePandemoniumInstitute/botc-release/main/resources/data/'
FILES = ['roles.json', 'nightsheet.json', 'jinxes.json']
TEAMS = ['townsfolk', 'outsider', 'minion', 'demon', 'traveller', 'fabled', 'loric']
EDITIONS = {'tb': 'Trouble Brewing', 'bmr': 'Bad Moon Rising', 'snv': 'Sects & Violets',
            'carousel': 'Experimental', 'fabled': 'Fabled', 'loric': 'Loric'}
OURS = ['summary', 'tags', 'setup_modifier']  # fields this repo writes; everything else comes from upstream


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def dump(path, obj):
    pathlib.Path(path).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')


def wiki_url(name):
    return 'https://wiki.bloodontheclocktower.com/' + name.replace(' ', '_')


def fetch():
    OFFICIAL.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        with urllib.request.urlopen(SOURCE + name, timeout=30) as response:
            (OFFICIAL / name).write_bytes(response.read())
        print('fetched', name)


def build():
    roles = load(OFFICIAL / 'roles.json')
    night = load(OFFICIAL / 'nightsheet.json')
    jinxes = load(OFFICIAL / 'jinxes.json')
    old = {c['id']: c for c in load(DATA / 'characters.json')['characters']} if (DATA / 'characters.json').exists() else {}
    out = []
    for role in sorted(roles, key=lambda r: (TEAMS.index(r['team']), list(EDITIONS).index(r['edition']), r['name'])):
        rid = role['id']
        mine = old.get(rid, {})
        entry = {
            'id': rid,
            'name': role['name'],
            'team': role['team'],
            'alignment': {'townsfolk': 'good', 'outsider': 'good', 'minion': 'evil', 'demon': 'evil'}.get(role['team']),
            'edition': role['edition'],
            'summary': mine.get('summary', ''),
            'tags': mine.get('tags', []),
            'setup': bool(role.get('setup')),
            'first_night': night['firstNight'].index(rid) if rid in night['firstNight'] else None,
            'other_nights': night['otherNight'].index(rid) if rid in night['otherNight'] else None,
            'reminders': role.get('reminders', []),
            'reminders_global': role.get('remindersGlobal', []),
            'app_special': sorted({s['name'] for s in role.get('special', [])}),
            'jinxed_with': [],
            'wiki': wiki_url(role['name']),
        }
        if mine.get('setup_modifier'):
            entry['setup_modifier'] = mine['setup_modifier']
        if not entry['summary']:
            print('new upstream character, write a summary:', rid, file=sys.stderr)
        out.append(entry)
    by_id = {c['id']: c for c in out}
    pairs = []
    for item in jinxes:
        for other in item['jinx']:
            pair = sorted([item['id'], other['id']])
            if pair not in pairs:
                pairs.append(pair)
    for a, b in pairs:
        for x, y in ((a, b), (b, a)):
            if x in by_id:
                by_id[x]['jinxed_with'].append(y)
    for c in out:
        c['jinxed_with'].sort()
    dump(DATA / 'characters.json', {
        'about': 'Blood on the Clocktower characters. Summaries and tags are this repo\'s own words; structural '
                 'fields mirror the official toolmaker data (see docs/botc/data/README.md). Night order values are '
                 'positions in night-order.json.',
        'editions': EDITIONS,
        'characters': out,
    })
    dump(DATA / 'night-order.json', {'first_night': night['firstNight'], 'other_nights': night['otherNight']})
    dump(DATA / 'jinxes.json', {'about': 'Pairs of characters with an official jinx. The ruling text is in '
                                         'official/jinxes.json after `python scripts/botc_data.py fetch`.',
                                'pairs': sorted(pairs)})
    print(f'{len(out)} characters, {len(pairs)} jinx pairs')


def check():
    """Return a list of problems with the committed data (empty when consistent)."""
    problems = []
    chars = load(DATA / 'characters.json')['characters']
    ids = [c['id'] for c in chars]
    known = set(ids)
    if len(ids) != len(known):
        problems.append('duplicate character ids')
    for c in chars:
        if c['team'] not in TEAMS:
            problems.append(f"{c['id']}: unknown team {c['team']}")
        if not c['summary']:
            problems.append(f"{c['id']}: empty summary")
        for other in c['jinxed_with']:
            if other not in known:
                problems.append(f"{c['id']}: jinx with unknown character {other}")
    night = load(DATA / 'night-order.json')
    markers = {'dusk', 'dawn', 'minioninfo', 'demoninfo'}
    for key in ('first_night', 'other_nights'):
        for rid in night[key]:
            if rid not in known and rid not in markers:
                problems.append(f'night order {key}: unknown id {rid}')
    for c in chars:
        for key in ('first_night', 'other_nights'):
            pos = c[key]
            if pos is not None and night[key][pos] != c['id']:
                problems.append(f"{c['id']}: {key} position {pos} does not match night-order.json")
    for path in sorted((DATA / 'scripts').glob('*.json')):
        script = load(path)
        meta = [x for x in script if isinstance(x, dict) and x.get('id') == '_meta']
        if not meta:
            problems.append(f'{path.name}: no _meta entry')
        for item in script:
            rid = item if isinstance(item, str) else item.get('id')
            if rid != '_meta' and rid not in known:
                problems.append(f'{path.name}: unknown character {rid}')
    counts = load(DATA / 'setup-counts.json')['counts']
    for players, row in counts.items():
        if sum(row.values()) != int(players):
            problems.append(f'setup-counts: {players} players adds up to {sum(row.values())}')
    return problems


def main(argv):
    command = argv[1] if len(argv) > 1 else 'check'
    if command == 'fetch':
        fetch()
    elif command == 'build':
        build()
    elif command == 'check':
        problems = check()
        print('\n'.join(problems) or 'ok')
        return 1 if problems else 0
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
