// Clocktower spectator: library, Grimoire circle, chronicle and playback.
'use strict';

const EVIL = new Set(['Imp', 'Poisoner', 'Spy', 'Scarlet Woman', 'Baron']);
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const words = (s) => (s || '').split(/\s+/).filter(Boolean).length;

const S = {
  games: [], id: null, summary: null, result: null,
  events: [],        // every event of the open game, in order
  shown: [],         // indices into events visible in the current view
  pos: 0,            // how many of `shown` have been revealed
  playing: false, following: false, timer: null, poller: null,
  view: 'omniscient', thinking: false, speed: 2,
  seats: [], setup: null,
};

// ---------------------------------------------------------------- data
// Served by `clocktower watch` (live, /api/...) or published as static files by `clocktower site`
// (data/index.json plus one bundle per batch; no live games).
const STATIC = !!window.CLOCKTOWER_STATIC;
const bundles = new Map();
const bundleName = (batch) => `data/${(batch || 'single').replaceAll('/', '--')}.json`;

async function getGames() {
  return (await fetch(STATIC ? 'data/index.json' : '/api/games')).json();
}

async function getGame(id, since) {
  if (!STATIC) return (await fetch(`/api/game?id=${encodeURIComponent(id)}&since=${since}`)).json();
  const g = S.games.find((x) => x.id === id);
  if (!g) return null;
  if (!bundles.has(g.batch)) bundles.set(g.batch, (await fetch(bundleName(g.batch))).json());
  const game = (await bundles.get(g.batch))[id];
  return since ? { ...game, events: [] } : game;
}

// Links look like #v2~opus-20~game-01 (older #game=v2/opus-20/game-01 links still work).
function hashId() {
  const h = decodeURIComponent(location.hash.slice(1));
  return h.startsWith('game=') ? h.slice(5) : h.replaceAll('~', '/');
}

// ---------------------------------------------------------------- library
async function loadLibrary() {
  try {
    S.games = await getGames();
  } catch { return; }
  const groups = new Map();
  const recency = (g) => (g.live ? 1e12 : 0) + g.updated;
  const order = [...S.games].sort((a, b) => Math.max(...S.games.filter((x) => x.batch === b.batch).map(recency)) -
    Math.max(...S.games.filter((x) => x.batch === a.batch).map(recency)) || a.name.localeCompare(b.name));
  for (const g of order) {
    const key = g.batch || 'Single games';
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(g);
  }
  const box = $('games');
  const open = new Set([...box.querySelectorAll('.batch:not(.closed)')].map((b) => b.dataset.key));
  box.innerHTML = '';
  for (const [key, games] of groups) {
    const good = games.filter((g) => g.winner === 'good').length;
    const evil = games.filter((g) => g.winner === 'evil').length;
    const live = games.filter((g) => g.live).length;
    const div = document.createElement('div');
    div.className = 'batch';
    div.dataset.key = key;
    if (open.size && !open.has(key) && !games.some((g) => g.id === S.id)) div.classList.add('closed');
    div.innerHTML = `<div class="batch-head"><span>${esc(key)}</span><span class="tally">` +
      `<span class="g">${good}</span> · <span class="e">${evil}</span>${live ? ` · <span class="dot"></span>${live}` : ''}</span></div>`;
    div.querySelector('.batch-head').onclick = () => div.classList.toggle('closed');
    const list = document.createElement('div');
    list.className = 'list';
    for (const g of games) {
      const row = document.createElement('div');
      row.className = 'game' + (g.id === S.id ? ' active' : '');
      const n = g.batch ? (g.name.match(/(\d+)$/) || [])[1] : null;
      const pill = g.live ? '<span class="pill live"><span class="dot"></span>live</span>'
        : g.winner ? `<span class="pill ${g.winner}">${g.winner}</span>` : '<span class="pill none">—</span>';
      const meta = [g.days ? `day ${g.days}` : '', g.cost != null ? `$${g.cost.toFixed(2)}` : ''].filter(Boolean).join(' · ');
      row.innerHTML = n ? `<span class="num">${esc(n)}</span><span>${pill}</span><span class="meta">${esc(meta)}</span>`
        : `<span class="num">·</span><span class="single">${esc(g.name)} ${pill}</span><span class="meta">${esc(meta)}</span>`;
      row.title = `${g.id}\n${g.models.join(', ')}`;
      row.onclick = () => openGame(g.id);
      list.appendChild(row);
    }
    div.appendChild(list);
    box.appendChild(div);
  }
  const style = document.getElementById('closed-style') || Object.assign(document.createElement('style'), { id: 'closed-style' });
  style.textContent = '.batch.closed .list { display: none; }';
  document.head.appendChild(style);
}

// ---------------------------------------------------------------- loading a game
async function openGame(id) {
  stop();
  clearInterval(S.poller);
  Object.assign(S, { id, events: [], shown: [], pos: 0, setup: null, seats: [] });
  const data = await getGame(id, 0);
  if (!data) return;
  try { history.replaceState(null, '', '#' + id.replaceAll('/', '~')); } catch {}
  S.events = data.events;
  S.summary = data.summary;
  S.result = data.result;
  S.config = data.config;
  readSetup();
  buildViewMenu();
  buildSeats();
  recompute();
  S.following = !!S.summary.live;
  seek(S.following ? S.shown.length : 0);
  header();
  loadLibrary();
  if (S.summary.live) S.poller = setInterval(poll, 2500);
  $('live').hidden = !S.summary.live;
  if (S.following) play();
}

async function poll() {
  if (!S.id) return;
  const data = await getGame(S.id, S.events.length);
  if (!data || !data.events) return;
  const atEnd = S.pos >= S.shown.length;
  S.events.push(...data.events);
  S.summary = data.summary;
  S.result = data.result;
  if (!S.setup) { readSetup(); buildViewMenu(); buildSeats(); }
  recompute();
  updateScrubber();
  header();
  if (!S.summary.live && S.result) { clearInterval(S.poller); $('live').hidden = true; loadLibrary(); }
  if (S.following && atEnd && !S.playing) play();
}

function readSetup() {
  // New logs have a structured setup event; older ones a "Setup:" text block.
  const ev = S.events.find((e) => e.kind === 'setup');
  if (ev) {
    S.setup = { seats: ev.data.seats, redHerring: ev.data.red_herring, bluffs: ev.data.bluffs };
    return;
  }
  const text = S.events.find((e) => e.kind === 'text' && (e.data.text || '').startsWith('Setup:'));
  if (!text) return;
  const seats = [];
  let redHerring = null, bluffs = [];
  for (const line of text.data.text.split('\n')) {
    const m = line.match(/^\d+\. (\w+): ([A-Za-z ]+?) \((good|evil)\)(?: \[(.*)\])?$/);
    if (m) {
      const tags = m[4] || '';
      const drunk = tags.match(/thinks they are the ([A-Za-z ]+)/);
      seats.push({ name: m[1], character: m[2], shown: drunk ? drunk[1] : m[2] });
      if (tags.includes('red herring')) redHerring = m[1];
    }
    const b = line.match(/^Demon bluffs: (.*)$/);
    if (b) bluffs = b[1].split(', ');
  }
  if (seats.length) S.setup = { seats, redHerring, bluffs };
}

function buildViewMenu() {
  const sel = $('view');
  const names = S.setup ? S.setup.seats.map((s) => s.name) : [];
  const current = S.view;
  sel.innerHTML = '<option value="omniscient">Storyteller’s grimoire</option><option value="public">The town square</option>' +
    names.map((n) => `<option value="${esc(n)}">${esc(n)}’s eyes</option>`).join('');
  sel.value = [...sel.options].some((o) => o.value === current) ? current : 'omniscient';
  S.view = sel.value;
}

// ---------------------------------------------------------------- visibility
function visible(ev) {
  if (ev.kind === 'thinking') return S.thinking && (S.view === 'omniscient' || ev.data.player === S.view);
  if (ev.kind === 'intro') return S.view !== 'omniscient' && S.view !== 'public' && ev.to.includes(S.view);
  if (S.view === 'omniscient') return true;
  if (ev.to === 'public') return true;
  if (S.view === 'public') return false;
  return Array.isArray(ev.to) && ev.to.includes(S.view);
}

function recompute() {
  const keep = S.shown[S.pos - 1];
  S.shown = [];
  S.events.forEach((ev, i) => { if (visible(ev)) S.shown.push(i); });
  if (keep != null) {
    let p = S.shown.findIndex((i) => i > keep);
    S.pos = p === -1 ? S.shown.length : p;
  }
}

// ---------------------------------------------------------------- the circle
function buildSeats() {
  const box = $('tokens');
  box.innerHTML = '';
  const seats = S.setup ? S.setup.seats : [];
  const n = seats.length || 9;
  seats.forEach((seat, i) => {
    const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
    const el = document.createElement('div');
    el.className = 'seat';
    el.dataset.name = seat.name;
    el.style.left = `${50 + 41 * Math.cos(a)}%`;
    el.style.top = `${50 + 41 * Math.sin(a)}%`;
    el.innerHTML = `<div class="token"><div class="face"></div><div class="badges"></div></div><div class="name">${esc(seat.name)}</div>`;
    box.appendChild(el);
  });
}

function seatXY(name) {
  const seats = S.setup ? S.setup.seats : [];
  const i = seats.findIndex((s) => s.name === name);
  const a = -Math.PI / 2 + (2 * Math.PI * i) / seats.length;
  return [500 + 410 * Math.cos(a), 500 + 410 * Math.sin(a)];
}

// Everything the circle shows, derived from the events revealed so far.
function tableState() {
  const upto = S.pos ? S.shown[S.pos - 1] : -1;
  const st = {
    phase: 'Setup', sub: '', night: false, dead: [], characters: {}, poisoned: null, protected: null, master: null,
    speaker: null, whispers: [], nomination: null, spotlight: null, over: null, ghostUsed: new Set(),
  };
  if (S.setup) for (const s of S.setup.seats) st.characters[s.name] = s.character;
  const omni = S.view === 'omniscient';
  for (let i = 0; i <= upto; i++) {
    const ev = S.events[i];
    const d = ev.data;
    const seen = visible(ev) || (omni && ev.kind !== 'thinking');
    if (ev.kind === 'becomes' && omni) st.characters[d.player] = d.character;
    if (!seen) continue;
    st.dead = ev.dead || st.dead;
    switch (ev.kind) {
      case 'header': {
        const t = d.text;
        st.speaker = null; st.whispers = []; st.spotlight = null;
        if (t.startsWith('Night')) { st.phase = t; st.sub = ''; st.night = true; st.poisoned = null; st.protected = null; }
        else if (t.includes('beat')) { st.phase = t.split(' · ')[0]; st.sub = t.split(' · ')[1]; st.night = false; }
        else { st.phase = t; st.sub = 'Dawn'; st.night = false; }
        break;
      }
      case 'dawn': st.spotlight = { narration: d.narration, deaths: d.deaths }; break;
      case 'say': st.speaker = d.speaker; st.spotlight = { who: d.speaker, text: d.text }; break;
      case 'whisper': st.whispers.push({ from: d.from, to: d.to, fresh: i === upto }); break;
      case 'nominations_open': st.sub = 'Nominations'; st.speaker = null; st.whispers = []; break;
      case 'nomination': st.nomination = { nominee: d.nominee, nominator: d.nominator, yes: [], needed: null }; st.speaker = d.nominator; st.spotlight = { who: `${d.nominator} nominates ${d.nominee}`, text: d.text }; break;
      case 'defense': st.speaker = d.nominee; st.spotlight = { who: `${d.nominee}’s defense`, text: d.text }; break;
      case 'vote':
        if (st.nomination) { if (d.yes) st.nomination.yes.push(d.voter); st.speaker = d.voter; }
        if (d.ghost) st.ghostUsed.add(d.voter);
        break;
      case 'vote_result': if (st.nomination) { st.nomination.needed = d.needed; st.nomination.done = true; st.nomination.votes = d.votes; st.nomination.outcome = d.outcome; } break;
      case 'execution': case 'no_execution': st.nomination = null; st.spotlight = { event: ev }; break;
      case 'slayer': st.speaker = d.shooter; st.spotlight = { who: `${d.shooter} shoots ${d.target}`, text: d.died ? `${d.target} dies!` : 'Nothing happens.' }; break;
      case 'night_choice':
        if (d.role === 'Poisoner') st.poisoned = d.targets[0];
        if (d.role === 'Monk' && st.characters[d.player] === 'Monk') st.protected = d.targets[0];
        if (d.role === 'Butler') st.master = d.targets[0];
        break;
      case 'game_over': st.over = d; st.nomination = null; break;
    }
  }
  if (upto >= 0 && S.events[upto].kind === 'vote_result') { /* keep the tally visible until the next event */ }
  return st;
}

function renderCircle() {
  const st = tableState();
  const omni = S.view === 'omniscient';
  const reveal = omni || !!st.over;
  const me = S.view !== 'omniscient' && S.view !== 'public' ? S.view : null;
  $('circle').classList.toggle('night', st.night);
  $('phase').textContent = st.over ? 'The End' : st.phase;
  $('phase-sub').textContent = st.over ? '' : st.sub;

  for (const el of document.querySelectorAll('.seat')) {
    const name = el.dataset.name;
    const seat = S.setup.seats.find((s) => s.name === name);
    const character = st.characters[name] || seat.character;
    const evil = EVIL.has(character);
    const known = reveal || name === me;
    const token = el.querySelector('.token');
    const dead = st.dead.includes(name);
    el.classList.toggle('dead', dead);
    el.classList.toggle('me', name === me);
    token.className = 'token' + (known ? (evil ? ' evil' : ' good') : '') + (dead ? ' dead' : '');
    if (st.speaker === name) token.classList.add('speaking');
    if (st.nomination && st.nomination.nominee === name) token.classList.add('nominee');
    if (st.whispers.some((w) => w.fresh && (w.from === name || w.to.includes(name)))) token.classList.add('whispering');
    const shown = name === me && !reveal ? seat.shown : character;
    const drunkNote = known && seat.character === 'Drunk' && character === 'Drunk' ? `<small>thinks: ${esc(seat.shown)}</small>` : '';
    el.querySelector('.face').innerHTML = known ? `<div class="role">${esc(shown)}${drunkNote}</div>` : '<div class="unknown">?</div>';
    const badges = [];
    if (st.nomination && st.nomination.yes.includes(name)) badges.push('<span class="badge hand">✋</span>');
    if (omni && st.poisoned === name) badges.push('<span class="badge poison" title="Poisoned">poisoned</span>');
    if (omni && st.protected === name) badges.push('<span class="badge safe" title="Protected by the Monk">safe</span>');
    if (omni && S.setup.redHerring === name) badges.push('<span class="badge herring" title="Fortune Teller’s red herring">herring</span>');
    if (omni && st.master === name) badges.push('<span class="badge master" title="Butler’s master">master</span>');
    if (dead && !st.ghostUsed.has(name)) badges.push('<span class="badge ghost" title="Ghost vote unused"></span>');
    el.querySelector('.badges').innerHTML = badges.join('');
  }

  const threads = $('threads');
  threads.innerHTML = st.whispers.flatMap((w) => w.to.map((t) => {
    const [x1, y1] = seatXY(w.from), [x2, y2] = seatXY(t);
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
    const cx = mx + (500 - mx) * 0.55, cy = my + (500 - my) * 0.55;
    return `<path class="${w.fresh ? 'fresh' : ''}" d="M${x1},${y1} Q${cx},${cy} ${x2},${y2}"/>`;
  })).join('');

  const spot = $('spotlight');
  let html = '';
  if (st.over) {
    html = `<div class="banner ${st.over.winner}">${st.over.winner === 'good' ? 'Good' : 'Evil'} wins</div><div style="margin-top:8px">${esc(st.over.reason)}</div>`;
  } else if (st.nomination && (S.events[S.shown[S.pos - 1]] || {}).kind !== 'nomination' && (S.events[S.shown[S.pos - 1]] || {}).kind !== 'defense') {
    const nom = st.nomination;
    const needed = nom.needed || Math.ceil((S.setup.seats.length - st.dead.length) / 2);
    const count = nom.done ? nom.votes : nom.yes.length;
    const pips = Array.from({ length: Math.max(needed, count) }, (_, i) => `<i class="${i < count ? 'on' : ''} ${i === needed - 1 ? 'need' : ''}"></i>`).join('');
    html = `<span class="who">Vote on ${esc(nom.nominee)}</span><div class="tallyline">${count}<small> / ${needed}</small></div><div class="pips">${pips}</div>` +
      (nom.done ? `<div style="margin-top:8px">${nom.outcome === 'block' ? `${esc(nom.nominee)} is about to die` : nom.outcome === 'tie' ? 'A tie — nobody is about to die' : 'Not enough'}</div>` : '');
  } else if (st.spotlight) {
    const s = st.spotlight;
    if (s.narration !== undefined) html = `${esc(s.narration || '')}<span class="who" style="margin-top:8px">${s.deaths.length ? 'Died in the night: ' + esc(s.deaths.join(', ')) : 'Nobody died'}</span>`;
    else if (s.event) html = s.event.kind === 'execution' ? `<div class="banner evil" style="font-size:24px">${esc(s.event.data.player)} is executed</div>` : '<span class="who">Nobody is executed today</span>';
    else {
      const w = (s.text || '').split(/\s+/);
      html = `<span class="who">${esc(s.who)}</span>“${esc(w.length > 48 ? w.slice(0, 48).join(' ') + '…' : s.text)}”`;
    }
  }
  if (spot.dataset.html !== html) { spot.innerHTML = html; spot.dataset.html = html; spot.classList.remove('fade'); void spot.offsetWidth; spot.classList.add('fade'); }
}

// ---------------------------------------------------------------- the chronicle
function roleOf(name) {
  if (S.view !== 'omniscient' || !S.setup) return '';
  const s = S.setup.seats.find((x) => x.name === name);
  return s ? s.character : '';
}
function alignClass(name) {
  const r = roleOf(name);
  return r ? (EVIL.has(r) ? 'evil' : 'good') : '';
}
function avatar(name, dead) {
  return `<div class="avatar ${alignClass(name)} ${dead ? 'dead' : ''}">${esc(name[0])}</div>`;
}
function who(name, dead) {
  const r = roleOf(name);
  return `<div class="who ${dead ? 'dead' : ''}">${esc(name)}${dead ? ' · dead' : ''}${r ? `<span class="role">${esc(r)}</span>` : ''}</div>`;
}

let currentNomination = null;

function setupCard(seats, bluffs, redHerring) {
  const items = seats.map((s) => `<li><b>${esc(s.name)}</b> — <span class="${EVIL.has(s.character) ? 'evil' : 'good'}">${esc(s.character)}</span>` +
    `${s.shown !== s.character ? ` <i>(thinks ${esc(s.shown)})</i>` : ''}</li>`).join('');
  return `<div class="setup"><div class="head">The Grimoire</div><ol>${items}</ol><div class="extra">Demon bluffs: ${esc((bluffs || []).join(', '))}` +
    `${redHerring ? ` · Red herring: ${esc(redHerring)}` : ''}</div></div>`;
}

function entry(ev) {
  const d = ev.data;
  const dead = (ev.dead || []);
  const el = document.createElement('div');
  el.className = 'entry';
  const participant = S.view === 'omniscient' || (ev.kind === 'whisper' && (d.from === S.view || d.to.includes(S.view)));
  switch (ev.kind) {
    case 'header': {
      const minor = d.text.includes('beat');
      el.className = `entry divider ${d.text.startsWith('Night') ? 'night' : ''} ${minor ? 'minor' : ''}`;
      el.textContent = minor ? d.text.split(' · ')[1] : d.text;
      break;
    }
    case 'dawn':
      el.innerHTML = `<div class="dawn">${esc(d.narration || '')}<span class="deaths ${d.deaths.length ? '' : 'none'}">${d.deaths.length ? '☠ ' + esc(d.deaths.join(', ')) : 'Nobody died in the night'}</span></div>`;
      break;
    case 'say':
      el.innerHTML = `<div class="msg">${avatar(d.speaker, dead.includes(d.speaker))}<div>${who(d.speaker, dead.includes(d.speaker))}<div class="text">${esc(d.text)}</div></div></div>`;
      break;
    case 'whisper':
      el.innerHTML = participant
        ? `<div class="whisper"><span class="to">${esc(d.from)} → ${esc(d.to.join(', '))}</span>${esc(d.text)}</div>`
        : `<div class="whisper-meta">${esc(d.from)} whispered to ${esc(d.to.join(', '))}</div>`;
      break;
    case 'whisper_log':
      el.innerHTML = `<div class="whisper-meta">Private time ${d.beat}: ${Object.entries(d.sent).map(([p, to]) => esc(p) + ' → ' + (to.length ? esc(to.join(' and ')) : 'no one')).join(' · ')}</div>`;
      break;
    case 'nominations_open':
      el.className = 'entry divider minor';
      el.textContent = 'Nominations';
      break;
    case 'nomination':
      el.innerHTML = `<div class="card nomination"><div class="head">${esc(d.nominator)}<span class="vs">nominates</span>${esc(d.nominee)}</div>` +
        (d.text ? `<div class="quote">${esc(d.text)}</div>` : '') + '<div class="defense"></div><div class="votes"></div><div class="vote-remarks"></div><div class="result"></div></div>';
      currentNomination = el;
      break;
    case 'defense':
      if (currentNomination) {
        currentNomination.querySelector('.defense').innerHTML = `<div class="quote"><span class="by">Defense</span>${esc(d.text || '(silence)')}</div>`;
        return null;
      }
      el.innerHTML = `<div class="quote"><span class="by">${esc(d.nominee)}</span>${esc(d.text)}</div>`;
      break;
    case 'vote':
      if (currentNomination) {
        currentNomination.querySelector('.votes').insertAdjacentHTML('beforeend',
          `<span class="vote ${d.yes ? 'yes' : ''}" title="${esc(d.text || '')}">${d.yes ? '✋ ' : ''}${esc(d.voter)}${d.ghost ? ' 👻' : ''}</span>`);
        if (d.text) currentNomination.querySelector('.vote-remarks').insertAdjacentHTML('beforeend', `<div><b>${esc(d.voter)}:</b> ${esc(d.text)}</div>`);
        return null;
      }
      el.className = 'entry note';
      el.textContent = `${d.voter} votes ${d.yes ? 'yes' : 'no'}`;
      break;
    case 'vote_result':
      if (currentNomination) {
        const r = currentNomination.querySelector('.result');
        r.className = `result ${d.outcome === 'block' ? 'block' : ''}`;
        r.textContent = `${d.votes} of ${d.needed} needed — ` + (d.outcome === 'block' ? `${d.nominee} is about to die` : d.outcome === 'tie' ? 'tied: nobody is about to die' : 'not enough') +
          (d.voided && d.voided.length ? ` (${d.voided.join(', ')}’s vote did not count)` : '');
        currentNomination = null;
        return null;
      }
      el.className = 'entry note';
      el.textContent = `${d.nominee}: ${d.votes} votes`;
      break;
    case 'execution':
      el.innerHTML = `<div class="execution">✝ ${esc(d.player)} is executed${d.died ? '' : ' (already dead)'}</div>`;
      break;
    case 'virgin':
      el.innerHTML = `<div class="execution">⚡ The Virgin’s power: ${esc(d.nominator)} is executed on the spot</div>`;
      break;
    case 'no_execution':
      el.innerHTML = '<div class="execution none">Nobody is executed today</div>';
      break;
    case 'slayer':
      el.innerHTML = `<div class="slayer"><div class="head">⚔ ${esc(d.shooter)} fires the Slayer’s shot at ${esc(d.target)}</div><div class="${d.died ? 'hit' : ''}">${d.died ? `${esc(d.target)} falls dead!` : 'Nothing happens.'}</div></div>`;
      break;
    case 'game_over':
      el.innerHTML = `<div class="gameover"><div class="banner ${d.winner}">${d.winner === 'good' ? 'Good' : 'Evil'} wins</div><div class="why">${esc(d.reason)}</div></div>`;
      break;
    case 'setup':
      el.innerHTML = setupCard(d.seats, d.bluffs, d.red_herring);
      break;
    case 'night_choice':
      el.className = 'entry note night';
      el.innerHTML = `<span class="tag">night</span>${esc(d.player)} (${esc(d.role)}) chooses ${esc(d.targets.join(' & '))}`;
      break;
    case 'info':
      el.className = 'entry note info';
      el.innerHTML = `<span class="tag">${S.view === 'omniscient' ? esc(ev.to.join(', ')) : 'you learn'}</span>${esc(d.text.replace(/^Night \d+ — /, ''))}`;
      break;
    case 'st_choice':
      el.className = 'entry note st';
      el.innerHTML = `<span class="tag">storyteller</span>${esc(d.id)} → ${esc(JSON.stringify(d.value).replace(/[{}"]/g, '').replace(/,/g, ', '))}${d.valid ? '' : ' (illegal; default used)'}`;
      break;
    case 'text':
      if ((d.text || '').startsWith('Setup:') && S.setup) { el.innerHTML = setupCard(S.setup.seats, S.setup.bluffs, S.setup.redHerring); break; }
      if (ev.to === 'audit' && (d.text || '').startsWith('[error]')) { el.className = 'entry note'; el.textContent = d.text; break; }
      el.className = 'entry note st';
      el.innerHTML = `<span class="tag">storyteller</span>${esc(d.text).replace(/\n/g, '<br>')}`;
      break;
    case 'notice': case 'intro':
      el.className = 'entry note info';
      el.innerHTML = `<span class="tag">${ev.kind === 'intro' ? 'your character' : 'you'}</span>${esc(d.text).replace(/\n/g, '<br>')}`;
      break;
    case 'death':
      el.className = 'entry note night';
      el.innerHTML = `<span class="tag">death</span>${esc(d.player)} dies (${esc(d.cause)})`;
      break;
    case 'becomes':
      el.className = 'entry note st';
      el.innerHTML = `<span class="tag">grimoire</span>${esc(d.player)} becomes the ${esc(d.character)}`;
      break;
    case 'thinking':
      el.innerHTML = `<div class="thought"><span class="who">${esc(d.player)} thinks</span>${esc(d.text.trim())}</div>`;
      break;
    default:
      return null;
  }
  return el;
}

function renderChronicle(from) {
  const box = $('chronicle');
  if (from === 0) { box.innerHTML = ''; currentNomination = null; }
  for (let k = from; k < S.pos; k++) {
    const el = entry(S.events[S.shown[k]]);
    if (el) box.appendChild(el);
  }
  box.scrollTop = box.scrollHeight;
}

// ---------------------------------------------------------------- playback
function delay(ev) {
  const d = ev.data;
  const base = {
    header: 1100, dawn: 2600, say: 700 + 45 * Math.min(words(d.text), 70), whisper: 500 + 30 * Math.min(words(d.text), 60),
    nomination: 1600 + 30 * words(d.text), defense: 1200 + 35 * words(d.text), vote: 420, vote_result: 1400,
    execution: 2200, slayer: 2400, game_over: 3000, thinking: 350 + 8 * words(d.text), setup: 1500,
  }[ev.kind] ?? 260;
  return base / S.speed;
}

function step() {
  if (S.pos >= S.shown.length) {
    S.playing = false;
    playIcon();
    return;
  }
  S.pos += 1;
  renderChronicle(S.pos - 1);
  renderCircle();
  updateScrubber();
  if (S.playing) S.timer = setTimeout(step, delay(S.events[S.shown[S.pos - 1]]));
}
function play() { if (!S.id) return; S.playing = true; playIcon(); clearTimeout(S.timer); S.timer = setTimeout(step, 150); }
function stop() { S.playing = false; clearTimeout(S.timer); playIcon(); }
function playIcon() { $('play').innerHTML = S.playing ? '&#x275A;&#x275A;' : '&#x25B6;'; }
function seek(p) {
  S.pos = Math.max(0, Math.min(p, S.shown.length));
  renderChronicle(0);
  renderCircle();
  updateScrubber();
}

function updateScrubber() {
  const sc = $('scrubber');
  sc.max = S.shown.length;
  sc.value = S.pos;
  sc.style.setProperty('--p', `${S.shown.length ? (100 * S.pos) / S.shown.length : 0}%`);
  const ev = S.pos ? S.events[S.shown[S.pos - 1]] : null;
  $('position').textContent = ev ? `${ev.phase === 'night' ? 'Night' : 'Day'} ${ev.day || 1} · ${S.pos}/${S.shown.length}` : `0/${S.shown.length}`;
  const marks = $('marks');
  const heads = S.shown.map((i, k) => [S.events[i], k]).filter(([e]) => e.kind === 'header' && !e.data.text.includes('beat'));
  marks.innerHTML = heads.map(([e, k]) => {
    const night = e.data.text.startsWith('Night');
    const label = night ? `N${e.data.text.split(' ')[1]}` : `D${e.data.text.split(' ')[1]}`;
    return `<span class="${night ? 'night' : ''}" style="left:${(100 * k) / Math.max(1, S.shown.length)}%">${label}</span>`;
  }).join('');
  $('live').classList.toggle('following', S.following);
}

function header() {
  const s = S.summary;
  const r = S.result;
  const n = (s.name.match(/(\d+)$/) || [])[1];
  $('title').textContent = s.batch ? `${s.batch} · Game ${n || s.name}` : s.name;
  const models = [...new Set((r && r.models ? Object.values(r.models) : s.models))].join(', ');
  const outcome = r ? `<b>${r.winner ? (r.winner === 'good' ? 'Good' : 'Evil') + ' won' : 'Unfinished'}</b> after ${r.days} day${r.days === 1 ? '' : 's'} · $${(r.cost || 0).toFixed(2)}` : '<span class="dot"></span><b>in progress</b>';
  $('subtitle').innerHTML = `${esc(models)}${s.storyteller ? ` · Storyteller ${esc(s.storyteller)}` : ''} · ${outcome}`;
}

// ---------------------------------------------------------------- wiring
$('play').onclick = () => (S.playing ? stop() : play());
$('back').onclick = () => { stop(); S.following = false; seek(S.pos - 1); };
$('fwd').onclick = () => { stop(); if (S.pos < S.shown.length) { S.pos += 1; renderChronicle(S.pos - 1); renderCircle(); updateScrubber(); } };
$('scrubber').oninput = (e) => { stop(); S.following = false; seek(+e.target.value); };
$('speed').onchange = (e) => { S.speed = +e.target.value; };
$('live').onclick = () => { S.following = true; seek(S.shown.length); play(); };
$('view').onchange = (e) => { S.view = e.target.value; recompute(); seek(S.pos); };
$('thinking').onchange = (e) => { S.thinking = e.target.checked; recompute(); seek(S.pos); };
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'SELECT' || e.target.tagName === 'INPUT' && e.target.type !== 'range') return;
  if (e.key === ' ') { e.preventDefault(); S.playing ? stop() : play(); }
  if (e.key === 'ArrowRight') { e.preventDefault(); $('fwd').click(); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); $('back').click(); }
});

loadLibrary().then(() => {
  const wanted = hashId();
  const id = (S.games.find((g) => g.id === wanted) || S.games.find((g) => g.live) || S.games.find((g) => g.finished) || {}).id;
  if (id) openGame(id);
});
if (!STATIC) setInterval(loadLibrary, 15000);
window.addEventListener('hashchange', () => { const id = hashId(); if (id && id !== S.id) openGame(id); });
