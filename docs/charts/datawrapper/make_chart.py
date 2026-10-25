"""Create (or update) the Datawrapper chart of the final 2026 ratings from ratings.csv.
Needs DATAWRAPPER_API_TOKEN (scopes: chart:read, chart:write). Prints the chart's public URL for Substack.
Usage: python docs/charts/datawrapper/make_chart.py [CHART_ID]   (an id updates that chart in place)"""
import csv, json, os, sys, urllib.request

API, TOKEN = 'https://api.datawrapper.de/v3', os.environ['DATAWRAPPER_API_TOKEN']
HERE = os.path.dirname(os.path.abspath(__file__))

def call(method, path, body=None, ctype='application/json'):
    data = body if isinstance(body, bytes) else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(API + path, data=data, method=method,
                                 headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': ctype})
    with urllib.request.urlopen(req) as r:
        out = r.read()
    return json.loads(out) if out else None

# Dot plot: one row per model, dots at the interval ends and the rating, joined by a line.
rows = list(csv.DictReader(open(os.path.join(HERE, 'ratings.csv'))))
table = 'Model,Low (90%),Elo,High (90%)\n' + ''.join(
    f"{r['Model']} ({r['Lab']}),{r['Low (90%)']},{r['Elo']},{r['High (90%)']}\n" for r in rows)

meta = {
    'title': 'GPT-6 Astra leads at Blood on the Clocktower',
    'describe': {
        'intro': 'Elo rating from 386 games of Blood on the Clocktower between the 11 models released in 2026. '
                 'The average model is 1,500; a 400-point gap means the stronger model wins about 91% of games. '
                 'Lines show 90% intervals.',
        'source-name': 'Clocktower eval', 'byline': 'Dwarkesh Patel',
    },
    'visualize': {
        'custom-range': [1000, 2000], 'sort-range': {'by': 'Elo', 'enabled': True, 'reverse': False},
        'value-labels': {'enabled': True, 'column': 'Elo'},
        'color-by-column': True,
        'custom-colors': {'Low (90%)': '#c9ced6', 'High (90%)': '#c9ced6', 'Elo': '#18202b'},
        'range-extent': 'nice',
    },
}

cid = sys.argv[1] if len(sys.argv) > 1 else call('POST', '/charts', {'title': meta['title'], 'type': 'd3-dot-plot'})['id']
call('PUT', f'/charts/{cid}/data', table.encode(), 'text/csv')
call('PATCH', f'/charts/{cid}', {'title': meta['title'], 'metadata': meta})
call('POST', f'/charts/{cid}/publish')
print(f'chart {cid}: https://datawrapper.dwcdn.net/{cid}/  (edit: https://app.datawrapper.de/chart/{cid}/visualize)')
