"""Local web UI for a human seat: http://localhost:8765

Shows exactly what that seat can see (the same text the models get) and a form
for whatever is currently being asked. Runs a stdlib HTTP server in a thread.
"""
from __future__ import annotations
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .render import render, visible


def state(game, seat, since):
    events = []
    for ev in game.events[since:]:
        if ev['kind'] == 'thinking' or not visible(ev, seat):
            continue
        text = render(ev, seat, set(ev['dead']))
        if text is not None:
            events.append({'seq': ev['seq'], 'kind': ev['kind'], 'text': text.strip(),
                           'private': ev['to'] != 'public' or (ev['kind'] == 'whisper' and
                                                             (ev['data']['from'] == seat or seat in ev['data']['to']))})
    human = game.seats[seat]
    req = human.pending
    g = game.g
    return {
        'next': len(game.events),
        'events': events,
        'pending': None if req is None else {'kind': req.kind, 'prompt': req.prompt, 'n_targets': req.n_targets,
                                             'options': req.options, 'alive': req.alive, 'mode': req.mode},
        'players': [{'name': p.name, 'alive': p.alive, 'ghost': p.ghost_vote} for p in g.players] if g else [],
        'me': seat,
        'over': bool(g and g.winner),
    }


def serve(game, seat, port=8765):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, body, ctype='application/json'):
            data = body.encode() if isinstance(body, str) else body
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == '/':
                return self.send(200, PAGE, 'text/html; charset=utf-8')
            if url.path == '/state':
                since = int(parse_qs(url.query).get('since', ['0'])[0])
                return self.send(200, json.dumps(state(game, seat, since)))
            self.send(404, '{}')

        def do_POST(self):
            if urlparse(self.path).path != '/act':
                return self.send(404, '{}')
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
            game.seats[seat].submit(body)
            self.send(200, '{"ok": true}')

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'You are {seat}. Open http://127.0.0.1:{port}')
    return server


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clocktower</title>
<style>
:root { --bg:#faf8f5; --panel:#fff; --ink:#1d1b19; --muted:#6f6a64; --line:#e4dfd8; --accent:#7a2e2e;
        --whisper:#f3eefa; --whisper-ink:#4b3a73; --private:#eef6f0; --private-ink:#2f5d3a; }
@media (prefers-color-scheme: dark) { :root { --bg:#171513; --panel:#211e1b; --ink:#ece7e1; --muted:#9d958c;
        --line:#35302b; --accent:#e08a7a; --whisper:#2a2438; --whisper-ink:#c9b8f0; --private:#1f2e23; --private-ink:#9fd3aa; } }
* { box-sizing:border-box; }
[hidden] { display:none !important; }
body { margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system, system-ui, sans-serif; }
main { max-width:860px; margin:0 auto; padding:16px; display:flex; flex-direction:column; height:100vh; }
header { display:flex; justify-content:space-between; align-items:baseline; gap:12px; flex-wrap:wrap; }
h1 { font-size:18px; margin:0; }
#players { color:var(--muted); font-size:13px; }
#players .dead { text-decoration:line-through; }
#feed { flex:1; min-height:200px; overflow-y:auto; background:var(--panel); border:1px solid var(--line); border-radius:10px;
        padding:12px 14px; margin:12px 0; }
.ev { margin:3px 0; white-space:pre-wrap; }
.ev.header { color:var(--accent); font-weight:600; margin-top:14px; }
.ev.whisper { background:var(--whisper); color:var(--whisper-ink); border-radius:6px; padding:2px 8px; }
.ev.meta { color:var(--muted); font-size:13px; }
.ev.private { background:var(--private); color:var(--private-ink); border-radius:6px; padding:4px 8px; }
#panel { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }
#prompt { font-weight:600; margin-bottom:8px; }
textarea, select, input[type=text] { font:inherit; color:var(--ink); background:var(--bg);
        border:1px solid var(--line); border-radius:6px; padding:5px 8px; }
textarea { width:100%; min-height:44px; height:44px; resize:vertical; }
.row { margin:6px 0; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.row select { flex:0 0 auto; min-width:96px; }
.row input[type=text] { flex:1 1 200px; min-width:0; }
.link { background:none; border:none; color:var(--accent); padding:0; cursor:pointer; font-size:13px; }
.row label { display:inline-flex; gap:4px; align-items:center; }
button { font:inherit; padding:7px 16px; border-radius:6px; border:1px solid var(--accent); background:var(--accent);
         color:#fff; cursor:pointer; }
button.secondary { background:transparent; color:var(--accent); }
.hint { color:var(--muted); font-size:13px; }
</style></head>
<body><main>
<header><h1 id="title">Clocktower</h1><div id="players"></div></header>
<div id="feed"></div>
<div id="panel"><div id="prompt" class="hint">Waiting for the game…</div><div id="form"></div></div>
</main>
<script>
let since = 0, pending = null, players = [], me = '', submitted = false;
const feed = document.getElementById('feed');
const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

function addEvent(ev) {
  const div = document.createElement('div');
  let cls = 'ev';
  if (ev.kind === 'header') cls += ' header';
  else if (ev.kind === 'whisper') cls += ev.private ? ' whisper' : ' meta';
  else if (ev.private) cls += ' private';
  else if (['nominations_open','vote','vote_result'].includes(ev.kind)) cls += ' meta';
  div.className = cls;
  div.textContent = ev.text;
  const atBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 60;
  feed.appendChild(div);
  if (atBottom) feed.scrollTop = feed.scrollHeight;
}

function others() { return players.map(p => p.name).filter(n => n !== me); }
function options(list, blank) { return (blank ? '<option value="">—</option>' : '') + list.map(n => `<option>${esc(n)}</option>`).join(''); }

function renderForm() {
  const prompt = document.getElementById('prompt'), form = document.getElementById('form');
  if (!pending || submitted) {
    prompt.textContent = submitted ? 'Waiting for the other players…' : 'Waiting…';
    prompt.className = 'hint'; form.innerHTML = ''; return;
  }
  prompt.className = ''; prompt.textContent = pending.prompt.replace(/`/g, '');
  const k = pending.kind; let h = '';
  if ((k === 'beat' && pending.mode !== 'private') || k === 'comment') {
    h += `<textarea id="say" placeholder="Say something to the town (or leave blank)"></textarea>
      <div class="row"><span class="hint">Slayer shot</span><select id="shot">${options(others(), true)}</select></div>`;
  }
  if (k === 'beat' && pending.mode !== 'public') {
    for (const i of [0, 1, 2]) h += `<div class="row" id="wrow${i}" ${i ? 'hidden' : ''}><span class="hint">Whisper</span>
      <select id="wto${i}a">${options(others(), true)}</select><select id="wto${i}b">${options(others(), true)}</select>
      <input type="text" id="wtext${i}" placeholder="words only they see"></div>`;
    h += `<div class="row"><button class="link" onclick="const r=[...document.querySelectorAll('[id^=wrow]')].find(x=>x.hidden); if(r) r.hidden=false; if(!document.querySelector('[id^=wrow][hidden]')) this.remove()">+ another whisper</button></div>`;
  } else if (k === 'nominate') {
    h += `<div class="row"><span class="hint">Nominate</span><select id="nom">${options(pending.options, true)}</select></div>
      <textarea id="say" placeholder="Accusation (if nominating)"></textarea>
      <div class="row"><span class="hint">Slayer shot</span><select id="shot">${options(others(), true)}</select></div>`;
  } else if (k === 'defense') {
    h += `<textarea id="say" placeholder="Your defense"></textarea>`;
  } else if (k === 'vote') {
    h += `<input type="text" id="say" placeholder="Optional short remark">
      <div class="row"><button onclick="send({vote:true})">Vote YES</button>
      <button class="secondary" onclick="send({vote:false})">Vote no</button></div>`;
  } else if (k === 'night' || k === 'ravenkeeper') {
    h += `<div class="row">` + pending.options.map(n => `<label><input type="checkbox" name="t" value="${esc(n)}"> ${esc(n)}</label>`).join('') +
      `</div><div class="hint">Choose ${pending.n_targets}.</div>`;
  }
  if (k !== 'vote') h += `<div class="row"><button onclick="send({})">Submit</button></div>`;
  form.innerHTML = h;
}

function val(id) { const e = document.getElementById(id); return e ? e.value.trim() : ''; }
async function send(extra) {
  const a = {say: val('say'), whispers: [], nominate: null, vote: null, targets: [], slayer_shot: null};
  if (pending.kind === 'beat') {
    for (const i of [0, 1, 2]) {
      const to = [val(`wto${i}a`), val(`wto${i}b`)].filter(Boolean), text = val(`wtext${i}`);
      if (to.length && text) a.whispers.push({to: [...new Set(to)], text});
    }
  }
  a.slayer_shot = val('shot') || null;
  if (pending.kind === 'nominate') a.nominate = val('nom') || null;
  if (pending.kind === 'night' || pending.kind === 'ravenkeeper') {
    a.targets = [...document.querySelectorAll('input[name=t]:checked')].map(x => x.value);
    if (a.targets.length !== pending.n_targets) { alert(`Choose exactly ${pending.n_targets}.`); return; }
  }
  Object.assign(a, extra);
  submitted = true; renderForm();
  await fetch('/act', {method: 'POST', body: JSON.stringify(a)});
}

async function poll() {
  try {
    const s = await (await fetch('/state?since=' + since)).json();
    me = s.me; players = s.players; since = s.next;
    document.getElementById('title').textContent = 'Clocktower — you are ' + me;
    document.getElementById('players').innerHTML = players.map(p =>
      `<span class="${p.alive ? '' : 'dead'}">${esc(p.name)}</span>`).join(' · ');
    s.events.forEach(addEvent);
    const key = s.pending ? s.pending.kind + '|' + s.pending.prompt : null;
    const old = pending ? pending.kind + '|' + pending.prompt : null;
    if (key !== old) { pending = s.pending; submitted = false; renderForm(); }
    if (!s.pending && !submitted && pending) { pending = null; renderForm(); }
  } catch (e) {}
  setTimeout(poll, 1000);
}
poll();
</script></body></html>
"""
