"""Fill docs/plans/f2-ratings.template.html with scripts/ratings2026.py output."""
import json, sys
data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'docs/plans/f2-ratings.json'))
t = open('docs/plans/f2-ratings.template.html').read()
open('docs/plans/f2-ratings.html', 'w').write(t.replace('__DATA__', json.dumps(data)).replace('__GAMES__', str(data['games'])))
