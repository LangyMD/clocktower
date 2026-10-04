// Clocktower table: lobby, the town circle, the chronicle and the action dock for one human seat.
// Everything a seat sees comes from /api/state (the same events and prompts a model in that seat gets).
'use strict';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch { /* private mode */ } },
};
const svg = (body, cls = 'i') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true">${body}</svg>`;
const ICON = {
  moon: svg('<path d="M20.5 14.2A8.5 8.5 0 1 1 9.8 3.5a6.8 6.8 0 0 0 10.7 10.7z"/>'),
  sun: svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
  bell: svg('<path d="M18 9a6 6 0 0 0-12 0c0 7-3 8.5-3 8.5h18S18 16 18 9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>'),
  quill: svg('<path d="M20 4c-6 0-11 4-13 11l-1.5 5"/><path d="M20 4c0 6-4 10-10 11"/><path d="M9 12h5"/>'),
  town: svg('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="3.5" r="1.6"/><circle cx="20.5" cy="12" r="1.6"/><circle cx="12" cy="20.5" r="1.6"/><circle cx="3.5" cy="12" r="1.6"/>'),
  book: svg('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>'),
  scroll: svg('<path d="M7 3h11a2 2 0 0 1 2 2v1H9"/><path d="M7 3a2 2 0 0 0-2 2v14a2 2 0 0 1-2 2h12a2 2 0 0 0 2-2V6"/><path d="M9 9h5M9 13h5"/>'),
  pen: svg('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
  sound: svg('<path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/>'),
  mute: svg('<path d="M11 5 6 9H3v6h3l5 4z"/><path d="M22 9l-6 6M16 9l6 6"/>'),
  glass: svg('<path d="M6 2h12M6 22h12"/><path d="M7 2c0 5 10 5 10 10S7 17 7 22"/><path d="M17 2c0 5-10 5-10 10s10 5 10 10"/>'),
  whisper: svg('<path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
  eye: svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
  skull: svg('<path d="M12 3a8 8 0 0 0-5 14.2V20h10v-2.8A8 8 0 0 0 12 3z"/><circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/>'),
  arrow: svg('<path d="M12 2 4 22l8-5 8 5z"/>'),
  good: '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="7" fill="currentColor"/><g stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M20 4v5M20 31v5M4 20h5M31 20h5M8.7 8.7l3.5 3.5M27.8 27.8l3.5 3.5M8.7 31.3l3.5-3.5M27.8 12.2l3.5-3.5"/></g></svg>',
  evil: '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M9 6c1 6 3 9 6 10M31 6c-1 6-3 9-6 10" stroke="currentColor" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M20 13c-6 0-10 4.5-10 10.5S14.5 35 20 35s10-5.5 10-11.5S26 13 20 13z" fill="currentColor"/><path d="M15 23l3.5 1.5M25 23l-3.5 1.5" stroke="#160c0a" stroke-width="2.2" stroke-linecap="round"/></svg>',
  any: '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 7a13 13 0 0 1 0 26z" fill="currentColor"/><circle cx="20" cy="20" r="3" fill="currentColor"/></svg>',
};
const SETUPS = { 5: [3, 0, 1], 6: [3, 1, 1], 7: [5, 0, 1], 8: [5, 1, 1], 9: [5, 2, 1], 10: [7, 0, 2], 11: [7, 1, 2], 12: [7, 2, 2], 13: [9, 0, 3], 14: [9, 1, 3], 15: [9, 2, 3] };
const TEAM_TEXT = {
  good: ['Good', 'Find the Demon'], evil: ['Evil', 'Deceive the town'], any: ['Either', 'Let fate decide'],
};

let token = store.get('ct.token');
let hostKey = null;
let sound = store.get('ct.sound') !== 'off';
let models = {};          // id -> display name (from the lobby)

async function api(path, body) {
  const opts = body === undefined ? {} : { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } };
  opts.headers = { ...(opts.headers || {}), 'X-Token': token || '' };
  const r = await fetch(path, opts);
  const ct = r.headers.get('Content-Type') || '';
  const data = ct.includes('json') ? await r.json() : await r.text();
  if (!r.ok) throw new Error((data && data.error) || `HTTP ${r.status}`);
  return data;
}

function show(screen) {
  $('lobby').hidden = screen !== 'lobby';
  $('table').hidden = screen !== 'table';
}

// ================================================================== lobby
let lobbyTimer = null, lobbyState = null, joinTeam = 'good';

function allegiance(box, current, onPick) {
  box.innerHTML = ['good', 'evil', 'any'].map((t) => `<button type="button" class="team-tile ${t}${t === current ? ' on' : ''}" data-team="${t}">
    ${ICON[t]}<b>${TEAM_TEXT[t][0]}</b><small>${TEAM_TEXT[t][1]}</small></button>`).join('');
  box.querySelectorAll('button').forEach((b) => b.onclick = () => {
    box.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b));
    onPick(b.dataset.team);
  });
}

async function pollLobby() {
  clearTimeout(lobbyTimer);
  try {
    const L = await api('/api/lobby');
    lobbyState = L;
    L.models.forEach((m) => { models[m.id] = m.name; });
    if (token && !L.me) { token = null; store.set('ct.token', null); }
    if (L.me && hostKey && !L.me.host) {
      try { await api('/api/host', { key: hostKey }); } catch { /* not valid */ }
      hostKey = null; history.replaceState(null, '', location.pathname);
      return pollLobby();
    }
    if (L.status !== 'lobby' && L.me && L.me.seated) return enterTable();
    renderLobby(L);
  } catch (e) { /* server restarting: keep trying */ }
  lobbyTimer = setTimeout(pollLobby, 1500);
}

function renderLobby(L) {
  show('lobby');
  const joined = !!L.me;
  $('join').hidden = joined;
  $('gather').hidden = !joined || (L.status === 'playing' && !L.me.in_game);
  $('busy').hidden = !(joined && L.status === 'playing' && !L.me.in_game);
  if (!joined) {
    if (!$('join-team').childElementCount) allegiance($('join-team'), joinTeam, (t) => { joinTeam = t; });
    return;
  }
  $('people').innerHTML = L.people.map((p) => `<li><span class="mini-token">${esc(p.name[0] || '?')}</span>
    <span>${esc(p.name)}${p.you ? ' <em>(you)</em>' : ''}</span>${p.host ? '<small>host</small>' : ''}
    ${L.me.host && !p.you && p.token ? `<button class="kick" data-t="${esc(p.token)}" title="Remove">&times;</button>` : ''}</li>`).join('');
  $('people').querySelectorAll('.kick').forEach((b) => b.onclick = () => api('/api/kick', { target: b.dataset.t }).then(pollLobby));
  const box = $('my-team');
  if (box.dataset.team !== L.me.team) {
    box.dataset.team = L.me.team;
    allegiance(box, L.me.team, (t) => { box.dataset.team = t; api('/api/me', { team: t }).then(pollLobby).catch(() => {}); });
  }

  const c = L.config, n = c.players, [tf, os, mn] = SETUPS[n];
  $('settings').classList.toggle('readonly', !L.me.host);
  $('size-n').textContent = n;
  $('composition').innerHTML = '<i class="tf"></i>'.repeat(tf) + '<i class="os"></i>'.repeat(os) + '<i class="mn"></i>'.repeat(mn) + '<i class="dm"></i>';
  const humans = L.people.length;
  $('comp-text').innerHTML = `${tf} Townsfolk &middot; ${os} Outsider${os === 1 ? '' : 's'} &middot; ${mn} Minion${mn === 1 ? '' : 's'} &middot; 1 Demon<br>
    <em>${humans} ${humans === 1 ? 'human' : 'humans'}, ${Math.max(0, n - humans)} AI players</em>`;
  for (const [id, key] of [['good-model', 'good_model'], ['evil-model', 'evil_model']]) {
    const sel = $(id);
    if (sel.dataset.v !== c[key] || !sel.options.length) {
      sel.innerHTML = L.models.map((m) => `<option value="${esc(m.id)}">${esc(m.name)}${m.elo ? ` · ${m.elo}` : ''}</option>`).join('');
      if (!L.models.some((m) => m.id === c[key])) sel.insertAdjacentHTML('beforeend', `<option value="${esc(c[key])}">${esc(c[key])}</option>`);
      sel.value = c[key]; sel.dataset.v = c[key];
    }
  }
  const tm = $('timer');
  if (tm.dataset.v !== String(c.timer) || !tm.options.length) {
    tm.innerHTML = L.timers.map((t) => `<option value="${t}">${t ? (t < 120 ? `${t} seconds` : `${t / 60} minutes`) : 'No limit'}</option>`).join('');
    tm.value = c.timer; tm.dataset.v = String(c.timer);
  }
  const cost = (id) => (L.models.find((m) => m.id === id) || {}).seat_cost;
  const evilSeats = mn + 1, goodSeats = n - evilSeats, ai = Math.max(0, n - humans) / n;
  const cg = cost(c.good_model), ce = cost(c.evil_model);
  $('estimate').innerHTML = cg == null || ce == null ? '' :
    `Roughly <b>$${Math.max(0, (goodSeats * cg + evilSeats * ce) * ai).toFixed(2)}</b> of API calls per game, from past games. Ratings are the 2026 study's Elo.`;
  $('share').hidden = !(L.me.host && L.links && L.links.friends);
  if (L.links && L.links.friends) $('share-url').textContent = L.links.friends;
  $('start').hidden = !L.me.host;
  $('start').disabled = !!L.problem;
  $('start-err').textContent = L.me.host ? (L.problem || L.error || '') : '';
  $('host-note').textContent = L.me.host ? '' : 'The host sets the table and rings the bell.';
  if (L.status === 'playing' && L.me.in_game) {
    $('start').hidden = false; $('start').disabled = true; $('start').textContent = 'Dealing the characters…';
  } else $('start').textContent = 'Ring the bell';
}

function wireLobby() {
  $('join-go').onclick = async () => {
    $('join-err').textContent = '';
    try {
      const r = await api('/api/join', { name: $('join-name').value, team: joinTeam, host: hostKey });
      token = r.token; store.set('ct.token', token);
      if (hostKey) { hostKey = null; history.replaceState(null, '', location.pathname); }
      pollLobby();
    } catch (e) { $('join-err').textContent = e.message; }
  };
  $('join-name').addEventListener('keydown', (e) => { if (e.key === 'Enter') $('join-go').click(); });
  const set = (cfg) => api('/api/config', cfg).then(pollLobby).catch((e) => { $('start-err').textContent = e.message; });
  $('size-minus').onclick = () => set({ players: Math.max(5, lobbyState.config.players - 1) });
  $('size-plus').onclick = () => set({ players: Math.min(15, lobbyState.config.players + 1) });
  $('good-model').onchange = (e) => set({ good_model: e.target.value });
  $('evil-model').onchange = (e) => set({ evil_model: e.target.value });
  $('timer').onchange = (e) => set({ timer: +e.target.value });
  $('share-copy').onclick = () => { navigator.clipboard?.writeText($('share-url').textContent); $('share-copy').textContent = 'Copied'; setTimeout(() => { $('share-copy').textContent = 'Copy'; }, 1500); };
  $('start').onclick = async () => {
    unlockAudio();
    try { await api('/api/start', {}); pollLobby(); } catch (e) { $('start-err').textContent = e.message; }
  };
}

// ================================================================== the table
const T = {};
function resetTable(game) {
  Object.assign(T, {
    game, since: 0, players: [], me: null, pending: null, sent: null, over: false, reveal: null, revealShown: false,
    filter: 'all', who: null, head: '', day: 0, stage: '', nominee: null, yes: new Set(), block: null, tie: false,
    speaking: null, wh: {}, ballot: null, form: null, deadline: null, alertedTurn: null,
  });
  $('feed').innerHTML = '';
  $('reveal').hidden = true;
}

let tableTimer = null;
function enterTable() {
  clearTimeout(lobbyTimer);
  show('table');
  pollState();
}

async function pollState() {
  clearTimeout(tableTimer);
  let S;
  try {
    S = await api('/api/state?since=' + (T.since || 0));
  } catch (e) {
    if (/Unknown player/.test(e.message)) { token = null; store.set('ct.token', null); return pollLobby(); }
    tableTimer = setTimeout(pollState, 2000);
    return;
  }
  if (!S.seated) {
    if (S.status === 'playing') { tableTimer = setTimeout(pollState, 1000); return; }
    return pollLobby();
  }
  if (S.game !== T.game) resetTable(S.game);
  T.since = S.next;
  T.players = S.players; T.me = S.me; T.over = S.over; T.reveal = S.reveal; T.spent = S.spent;
  const feed = $('feed'), stick = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 160;
  S.events.forEach(addEvent);
  const prevTurn = T.pending && T.pending.turn;
  T.pending = S.pending;
  const myTurn = S.pending && S.pending.turn !== prevTurn;
  if (S.events.length || myTurn) {
    if (stick || myTurn) { feed.scrollTop = feed.scrollHeight; $('jump').hidden = true; }
    else if (S.events.length) $('jump').hidden = false;
  }
  if ((S.pending && S.pending.turn) !== prevTurn) { T.form = null; renderDock(); }
  else tickDock();
  if (S.pending && T.sent !== S.pending.turn && T.alertedTurn !== S.pending.turn) { T.alertedTurn = S.pending.turn; alertTurn(); }
  if (!S.pending || T.sent === S.pending.turn) document.title = 'Clocktower';
  renderBar(); renderTown();
  if (S.over && S.reveal && !T.revealShown) { T.revealShown = true; renderReveal(); }
  tableTimer = setTimeout(pollState, S.over ? 3000 : 900);
}

// ---------------------------------------------------------------- derived table state
function processEvent(ev) {
  const d = ev.data;
  switch (ev.kind) {
    case 'header':
      T.head = d.text;
      if (/^Night/.test(d.text)) { T.stage = 'night'; T.nominee = null; T.yes = new Set(); T.block = null; T.tie = false; }
      else if (/^Day \d+$/.test(d.text)) { T.stage = 'dawn'; T.wh = {}; }
      else if (/private time/.test(d.text)) T.stage = 'private';
      else if (/town square/.test(d.text)) T.stage = 'public';
      T.day = ev.day; break;
    case 'nominations_open': T.stage = 'nominations'; T.head = `Day ${ev.day} · nominations`; break;
    case 'nomination': T.nominee = d.nominee; T.yes = new Set(); break;
    case 'vote': if (d.yes) T.yes.add(d.voter); break;
    case 'vote_result':
      if (d.outcome === 'block') { T.block = { name: d.nominee, votes: d.votes }; T.tie = false; }
      else if (d.outcome === 'tie') { T.block = null; T.tie = true; }
      T.nominee = null; T.yes = new Set(); break;
    case 'execution': case 'no_execution': T.block = null; break;
    case 'say': case 'defense': T.speaking = { name: d.speaker || d.nominee, at: Date.now() }; break;
    case 'whisper': {
      const me = T.me && T.me.seat;
      const others = [d.from, ...d.to].filter((x) => x !== me);
      others.forEach((x) => { T.wh[x] = (T.wh[x] || 0) + 1; });
      break;
    }
  }
}

// ---------------------------------------------------------------- the circle and the strip
function seatEl(p, opts = {}) {
  const me = T.me, isMe = me && p.name === me.seat;
  const known = me && me.known[p.name];
  const el = document.createElement('button');
  el.type = 'button';
  el.className = 'seat' + (isMe ? ' me' : '') + (p.alive ? '' : ' dead');
  el.dataset.name = p.name;
  let face = `<span class="initial">${esc(p.name[0])}</span>`, ring = '';
  if (isMe) { face = `<span class="role">${esc(me.character)}<small>you</small></span>`; ring = me.evil ? ' evil' : ' good'; }
  else if (known) { face = `<span class="role">${known}<small>${esc(p.name)}</small></span>`; ring = ' evil'; }
  let badges = '';
  if (T.nominee && T.yes.has(p.name)) badges += '<span class="badge hand">✋</span>';
  if (!p.alive && p.ghost) badges += '<span class="badge ghost" title="Ghost vote unused">&#9675;</span>';
  if (T.wh[p.name]) badges += `<span class="badge wh" title="Whispers with you today">${T.wh[p.name]}</span>`;
  if (T.block && T.block.name === p.name) badges += `<span class="badge blk">block ${T.block.votes}</span>`;
  el.innerHTML = `<span class="token${ring}">${face}${badges}</span><span class="name">${esc(p.name)}</span>`;
  if (T.speaking && T.speaking.name === p.name && Date.now() - T.speaking.at < 4000) el.classList.add('speaking');
  if (T.nominee === p.name) el.classList.add('nominee');
  if (T.who === p.name) el.classList.add('filtered');
  const f = T.pending && T.sent !== T.pending.turn ? T.form : null;
  if (f && f.picks.includes(p.name)) el.classList.add('picked', ...(f.mode === 'whisper' ? [] : ['target']));
  if (f && f.pickable && !f.pickable.includes(p.name)) el.classList.add('dim');
  el.onclick = () => seatClicked(p.name);
  return el;
}

function seatClicked(name) {
  const f = T.pending && T.sent !== T.pending.turn ? T.form : null;
  if (f && f.pickable && f.pickable.includes(name)) { togglePick(name); return; }
  T.who = T.who === name ? null : name;
  renderFilters(); applyFilter(); renderTown();
}

function dial() {
  // 12 ticks: six private beats, three town-square beats, nominations, and two for the night.
  let pos = 0;
  const m = T.head.match(/private time (\d+)/), q = T.head.match(/town square (\d+)/);
  if (T.stage === 'night') pos = 10.5;
  else if (m) pos = +m[1] - 1;
  else if (q) pos = 5 + +q[1];
  else if (T.stage === 'nominations') pos = 9;
  else pos = -0.5;
  let ticks = '';
  for (let i = 0; i < 12; i++) {
    const a = (i * 30 - 90) * Math.PI / 180, r1 = 38, r2 = i % 3 === 0 ? 31 : 34;
    ticks += `<line class="tick${i <= pos && T.stage !== 'night' ? ' done' : ''}" x1="${50 + r1 * Math.cos(a)}" y1="${50 + r1 * Math.sin(a)}" x2="${50 + r2 * Math.cos(a)}" y2="${50 + r2 * Math.sin(a)}"/>`;
  }
  return `<svg class="dial" viewBox="0 0 100 100" aria-hidden="true"><circle class="face" cx="50" cy="50" r="44"/>
    <path class="night-arc" d="M ${50 + 44 * Math.cos(-150 * Math.PI / 180)} ${50 + 44 * Math.sin(-150 * Math.PI / 180)} A 44 44 0 0 1 50 6"/>
    ${ticks}<line class="hand" x1="50" y1="50" x2="50" y2="20" style="transform: rotate(${pos * 30}deg)"/><circle class="hub" cx="50" cy="50" r="3"/></svg>`;
}

function phaseText() {
  const h = T.head || '';
  if (T.stage === 'night') return [h, 'the town sleeps'];
  const m = h.match(/^Day (\d+)(?: · (.*))?$/);
  if (!m) return [h, ''];
  let sub = m[2] || 'dawn';
  sub = sub.replace(/private time (\d+)/, 'private time $1 of 6').replace(/town square (\d+)/, 'town square $1 of 3');
  return [`Day ${m[1]}`, sub];
}

function renderCircle(box) {
  const ps = T.players, n = ps.length || 1;
  box.innerHTML = '<div class="ring"></div>';
  const size = box.clientWidth || 600;
  // the token size follows the space between neighbours, so names never collide
  const r0 = size * 0.40, t = Math.max(30, Math.min(86, (2 * Math.PI * r0 / n) * 0.56, size * 0.15));
  box.style.setProperty('--t', t + 'px');
  const R = 50 - (t * 0.75 / size) * 100 - 2;
  ps.forEach((p, i) => {
    const a = (i / n) * 2 * Math.PI - Math.PI / 2;
    const el = seatEl(p);
    el.style.left = `${50 + R * Math.cos(a)}%`;
    el.style.top = `${50 + R * Math.sin(a)}%`;
    box.appendChild(el);
  });
  const [ph, sub] = phaseText();
  const centre = document.createElement('div');
  centre.className = 'centre';
  const blk = T.nominee ? `${esc(T.nominee)} is nominated` : T.block ? `${esc(T.block.name)} is on the block (${T.block.votes})` : T.tie ? 'A tie: nobody on the block' : '';
  centre.innerHTML = `${dial()}<div class="ph">${esc(ph)}</div><div class="ph-sub">${esc(sub)}</div><div class="block">${blk}</div>`;
  box.appendChild(centre);
}

function renderTown() {
  if (getComputedStyle($('town')).display !== 'none') renderCircle($('circle'));
  const strip = $('strip');
  if (getComputedStyle(strip).display !== 'none') { strip.innerHTML = ''; T.players.forEach((p) => strip.appendChild(seatEl(p))); }
  if (!$('sheet').hidden && $('sheet').dataset.kind === 'town') renderCircle($('sheet-body').querySelector('.circle'));
}

function renderBar() {
  const me = T.me;
  if (!me) return;
  $('me-token').textContent = me.seat[0];
  $('me-token').className = 'mini-token ' + (me.evil ? 'evil' : 'good') + (me.alive ? '' : ' dead');
  $('me-name').textContent = me.seat;
  $('me-char').textContent = me.character + (me.alive ? '' : ' · dead');
  $('me-char').className = me.evil ? 'evil' : 'good';
  const [ph, sub] = phaseText();
  const short = innerWidth < 900 ? sub.replace(/private time (\d+) of (\d+)/, 'whisper $1/$2').replace(/town square (\d+) of (\d+)/, 'square $1/$2').replace('the town sleeps', '') : sub;
  $('phase-mini').innerHTML = `<b>${esc(ph)}</b>${short ? ' · ' + esc(short) : ''}`;
  document.body.classList.toggle('night', T.stage === 'night');
}

// ---------------------------------------------------------------- the chronicle
const CATS = [['all', 'All'], ['town', 'Town square'], ['whisper', 'Whispers'], ['st', 'Storyteller']];

function renderFilters() {
  const f = $('filters');
  f.innerHTML = CATS.map(([k, label]) => `<button class="chip${T.filter === k ? ' on' : ''}" data-f="${k}">${label}</button>`).join('') +
    (T.who ? `<button class="chip who" data-who="1">${esc(T.who)} &times;</button>` : '');
  f.querySelectorAll('[data-f]').forEach((b) => b.onclick = () => { T.filter = b.dataset.f; renderFilters(); applyFilter(); });
  const w = f.querySelector('[data-who]');
  if (w) w.onclick = () => { T.who = null; renderFilters(); applyFilter(); renderTown(); };
}

function matches(el) {
  const cat = el.dataset.cat;
  if (cat === 'divider') return !T.who;
  if (T.filter !== 'all' && cat !== T.filter) return false;
  if (T.who && !(el.dataset.who || '').split(' ').includes(T.who)) return false;
  return true;
}
function applyFilter() { for (const el of $('feed').children) el.hidden = !matches(el); }

function tokenHTML(name, extra = '') {
  const me = T.me, known = me && me.known[name];
  const cls = me && name === me.seat ? (me.evil ? ' evil' : ' good') : known ? ' evil' : '';
  const dead = T.players.find((p) => p.name === name && !p.alive) ? ' dead' : '';
  return `<span class="mini-token${cls}${dead}${extra}">${esc(name[0])}</span>`;
}

function stripPrompt(p) {
  return String(p || '')
    .replace(/ Put your choice in `targets`\./, '').replace(/ \(`targets`\)/, '')
    .replace(/Set `vote` to true or false; `say` may hold a very short remark \(optional; don't just restate your vote\)\./, 'You may add a very short remark.')
    .replace(/Set `vote` to true \(yes\) or false \(no\)/, 'Vote yes or no')
    .replace(/ \(set `nominate`; your `say` is the accusation\)/, ' (your words are the accusation)')
    .replace(/ in `say`/, '').replace(/`/g, '');
}

function addEvent(ev) {
  processEvent(ev);
  const d = ev.data, me = T.me ? T.me.seat : '';
  const feed = $('feed');
  let el = document.createElement('div'), cat = 'town', who = [];
  el.className = 'ev';
  const nameTag = (n) => esc(n) + (n === me ? ' <span class="tag">you</span>' : '');
  switch (ev.kind) {
    case 'header': {
      cat = 'divider';
      const big = /^(Night|Day) \d+$/.test(d.text), night = /^Night/.test(d.text);
      const icon = night ? ICON.moon : /private/.test(d.text) ? ICON.quill : /town square/.test(d.text) ? ICON.bell : ICON.sun;
      el.className += ' divider' + (big ? ' big' : '') + (night ? ' night' : '');
      el.innerHTML = `${icon}<span>${esc(d.text)}</span>`;
      break;
    }
    case 'intro': {
      cat = 'st';
      const m = T.me || {};
      el.innerHTML = `<div class="card-ev intro${m.evil ? ' evil' : ''}"><span class="token${m.evil ? ' evil' : ' good'}"><span class="role">${esc(m.character || '')}</span></span>
        <div><div class="h">${ICON.eye} The Storyteller shows you your character</div><p>${esc(d.text)}</p></div></div>`;
      break;
    }
    case 'info': {
      cat = 'st';
      const night = /^Night/.test(d.text);
      el.innerHTML = `<div class="card-ev st${night ? ' night' : ''}"><div class="h">${night ? ICON.moon : ICON.eye} The Storyteller, to you alone</div><p>${esc(d.text)}</p></div>`;
      break;
    }
    case 'notice': case 'text':
      cat = 'st'; el.innerHTML = `<div class="notice">${esc(d.text)}</div>`; break;
    case 'dawn':
      who = d.deaths;
      el.innerHTML = `<div class="card-ev dawn"><div class="narr">${esc(d.narration || '')}</div>
        <div class="deaths${d.deaths.length ? '' : ' none'}">${d.deaths.length ? `${ICON.skull} Died in the night: ${d.deaths.map(esc).join(', ')}` : 'Nobody died in the night'}</div></div>`;
      break;
    case 'say': {
      who = [d.speaker];
      const dead = T.players.find((p) => p.name === d.speaker && !p.alive);
      el.innerHTML = `<div class="say${d.speaker === me ? ' mine' : ''}${dead ? ' dead' : ''}">${tokenHTML(d.speaker)}
        <div class="body"><div class="who">${nameTag(d.speaker)}${dead ? ' <span class="tag">dead</span>' : ''}</div><div class="bubble">${esc(d.text)}</div></div></div>`;
      break;
    }
    case 'whisper': {
      cat = 'whisper'; who = [d.from, ...d.to];
      const to = d.to.map((x) => (x === me ? 'you' : esc(x))).join(' & ');
      el.innerHTML = `<div class="say whisper${d.from === me ? ' mine' : ''}">${tokenHTML(d.from)}
        <div class="body"><div class="who">${d.from === me ? 'You' : esc(d.from)} &rarr; ${to}</div><div class="bubble">${esc(d.text)}</div></div></div>`;
      break;
    }
    case 'nominations_open':
      cat = 'divider'; el.className += ' divider'; el.innerHTML = `${ICON.bell}<span>The Storyteller opens nominations</span>`; break;
    case 'nomination':
      who = [d.nominator, d.nominee]; T.ballot = null;
      el.innerHTML = `<div class="card-ev nom"><div class="h">${ICON.arrow} ${esc(d.nominator === me ? 'You' : d.nominator)} nominate${d.nominator === me ? '' : 's'} ${esc(d.nominee === me ? 'you' : d.nominee)}</div>${d.text ? `<p>${esc(d.text)}</p>` : ''}</div>`;
      break;
    case 'defense':
      who = [d.nominee];
      el.innerHTML = `<div class="say${d.nominee === me ? ' mine' : ''}">${tokenHTML(d.nominee)}<div class="body"><div class="who">${nameTag(d.nominee)} <span class="tag">defense</span></div>
        <div class="bubble">${d.text ? esc(d.text) : '<em>says nothing in their defense</em>'}</div></div></div>`;
      break;
    case 'vote': {
      if (!T.ballot) {
        T.ballot = document.createElement('div');
        T.ballot.className = 'ev'; T.ballot.dataset.cat = 'town'; T.ballot.dataset.who = d.nominee;
        T.ballot.innerHTML = `<div class="card-ev ballot"><div class="h">${ICON.bell} The vote on ${esc(d.nominee)}</div><div class="votes"></div><div class="remarks"></div></div>`;
        feed.appendChild(T.ballot); T.ballot.hidden = !matches(T.ballot);
      }
      const b = T.ballot;
      b.dataset.who += ' ' + d.voter;
      b.querySelector('.votes').insertAdjacentHTML('beforeend', `<span class="v${d.yes ? ' yes' : ''}${d.ghost ? ' ghost' : ''}" title="${d.ghost ? 'ghost vote' : ''}">${d.yes ? '✋' : '·'} ${esc(d.voter === me ? 'you' : d.voter)}</span>`);
      if (d.text) b.querySelector('.remarks').insertAdjacentHTML('beforeend', `<div><b>${esc(d.voter)}</b> ${esc(d.text)}</div>`);
      b.hidden = !matches(b);
      return;
    }
    case 'vote_result': {
      const line = `<div class="res${d.outcome === 'block' ? ' block' : ''}">${d.votes} of ${d.needed} needed${d.outcome === 'block' ? ` · ${esc(d.nominee)} is about to be executed` : d.outcome === 'tie' ? ' · a tie: nobody is about to die' : ''}</div>`;
      if (T.ballot) { T.ballot.querySelector('.ballot').insertAdjacentHTML('beforeend', line); T.ballot = null; return; }
      who = [d.nominee]; el.innerHTML = `<div class="card-ev ballot">${line}</div>`;
      break;
    }
    case 'execution':
      who = [d.player]; el.innerHTML = `<div class="doom">${ICON.skull} ${esc(d.player)} is executed${d.died ? '' : ' (they were already dead)'}</div>`; break;
    case 'no_execution':
      el.innerHTML = '<div class="doom quiet">Nobody is executed today</div>'; break;
    case 'virgin':
      who = [d.nominator, d.nominee]; el.innerHTML = `<div class="doom">${esc(d.nominator)} is executed immediately! The day ends.</div>`; break;
    case 'slayer':
      who = [d.shooter, d.target];
      el.innerHTML = `<div class="card-ev slay"><div class="h">${ICON.arrow} The Slayer's shot</div><p>${esc(d.shooter)} claims the Slayer's power and shoots at ${esc(d.target)}. ${d.died ? `<b>${esc(d.target)} dies!</b>` : 'Nothing happens.'}</p></div>`;
      break;
    case 'game_over':
      el.innerHTML = `<div class="over-ev">Game over · ${esc(d.winner)} wins<br><em>${esc(d.reason)}</em></div>`; break;
    default:
      cat = 'st'; el.innerHTML = `<div class="notice">${esc(ev.text)}</div>`;
  }
  el.dataset.cat = cat;
  el.dataset.who = who.join(' ');
  el.hidden = !matches(el);
  feed.appendChild(el);
}

// ---------------------------------------------------------------- the dock
const words = (s) => (s.trim().match(/\S+/g) || []).length;

function newForm(p) {
  const others = T.players.map((x) => x.name).filter((x) => x !== T.me.seat);
  const f = { picks: [], text: '', shot: null, showShot: false, remark: false, err: '' };
  if (p.kind === 'night' || p.kind === 'ravenkeeper') Object.assign(f, { mode: 'night', pickable: p.options, max: p.n_targets });
  else if (p.kind === 'beat' && p.mode === 'private') Object.assign(f, { mode: 'whisper', pickable: others, max: 2 });
  else if (p.kind === 'nominate') Object.assign(f, { mode: 'nominate', pickable: p.options, max: 1 });
  else if (p.kind === 'vote') Object.assign(f, { mode: 'vote', pickable: null });
  else if (p.kind === 'defense') Object.assign(f, { mode: 'defense', pickable: null });
  else Object.assign(f, { mode: 'speak', pickable: null });
  return f;
}

function togglePick(name) {
  const f = T.form;
  if (!f) return;
  if (f.shotPicking) { f.shot = f.shot === name ? null : name; renderDock(); renderTown(); return; }
  const i = f.picks.indexOf(name);
  if (i >= 0) f.picks.splice(i, 1);
  else { f.picks.push(name); if (f.picks.length > f.max) f.picks.shift(); }
  renderDock(); renderTown();
}

function timerHTML() {
  const p = T.pending;
  if (!p || !p.deadline) return '';
  const left = Math.max(0, Math.round(p.deadline - Date.now() / 1000));
  return `<span class="timer${left < 20 ? ' low' : ''}" id="turn-timer">${Math.floor(left / 60)}:${String(left % 60).padStart(2, '0')}</span>`;
}
function tickDock() { const t = $('turn-timer'); if (t) t.outerHTML = timerHTML(); }
setInterval(tickDock, 1000);

const KIND = {
  night: 'Night · your ability', ravenkeeper: 'Ravenkeeper', whisper: 'Private time · whisper', speak: 'Town square',
  comment: 'Comments on the nomination', nominate: 'Nominations', defense: 'You stand accused', vote: 'The vote',
};

function waitingText() {
  const dead = T.me && !T.me.alive;
  const base = { night: 'Night has fallen. The town sleeps…', private: 'Whispers pass between the others…', public: 'The town square is talking…',
    nominations: 'The town deliberates…', dawn: 'Dawn breaks…' }[T.stage] || 'The town deliberates…';
  return base + (dead ? ' <em>You are dead: you can still talk and whisper, and you have one ghost vote.</em>' : '');
}

function renderDock() {
  const dock = $('dock'), p = T.pending;
  dock.className = '';
  if (T.over) {
    dock.innerHTML = `<div class="wait">${ICON.bell} The game is over. <button class="linkish" id="see-reveal">See the Grimoire</button></div>`;
    $('see-reveal').onclick = renderReveal;
    return setDockHeight();
  }
  if (!p) { dock.innerHTML = `<div class="wait">${ICON.glass}<span>${waitingText()}</span></div>`; return setDockHeight(); }
  if (T.sent === p.turn) { dock.innerHTML = `<div class="sealed">Sealed · waiting for the others</div>`; return setDockHeight(); }
  const f = T.form || (T.form = newForm(p));
  const kindLabel = p.kind === 'comment' ? KIND.comment : KIND[f.mode];
  dock.className = 'turn' + (f.mode === 'whisper' ? ' private' : f.mode === 'night' ? ' night' : '');
  let h = `<div class="ask"><div class="what"><div class="kind">${kindLabel}</div><div class="prompt">${esc(stripPrompt(p.prompt))}</div></div>${timerHTML()}</div>`;
  const picks = (list, cls = '') => `<div class="picks">${list.map((n) => {
    const dead = !T.players.find((x) => x.name === n)?.alive;
    return `<button type="button" class="pick${f.picks.includes(n) ? ' on' : ''}${dead ? ' dead' : ''}${cls}" data-pick="${esc(n)}">${esc(n === T.me.seat ? 'yourself' : n)}</button>`;
  }).join('')}</div>`;
  const textarea = (ph, limit, rows = 3) => `<div class="compose"><textarea id="say" rows="${rows}" placeholder="${ph}">${esc(f.text)}</textarea><span class="count" id="count">${words(f.text)}/${limit}</span></div>`;
  const slayer = () => {
    if (!f.showShot) return `<div class="slayer-row"><button class="linkish" id="shot-open">Claim the Slayer's shot…</button></div>`;
    const others = T.players.map((x) => x.name).filter((x) => x !== T.me.seat);
    return `<div class="slayer-box"><div class="fine">Shoot publicly at a player. If you are the real Slayer and hit the Demon, they die; otherwise nothing happens (anyone may claim).</div>
      <div class="picks">${others.map((n) => `<button type="button" class="pick${f.shot === n ? ' on' : ''}" data-shot="${esc(n)}">${esc(n)}</button>`).join('')}</div>
      <button class="linkish" id="shot-close">Never mind</button></div>`;
  };
  if (f.mode === 'night') {
    h += picks(p.options);
    h += `<div class="actions"><button class="primary" id="go" ${f.picks.length === f.max ? '' : 'disabled'}>Choose ${f.max === 2 ? 'these two' : f.picks[0] ? esc(f.picks[0] === T.me.seat ? 'yourself' : f.picks[0]) : ''}</button></div>`;
  } else if (f.mode === 'whisper') {
    h += picks(f.pickable);
    h += textarea(f.picks.length ? `Only ${f.picks.join(' and ')} will see this` : 'Pick one or two players, then whisper…', p.whisper_words, 2);
    h += `<div class="actions"><button class="primary violet" id="go" ${f.picks.length && words(f.text) ? '' : 'disabled'}>Whisper</button><button class="ghost" id="pass">Stay silent</button></div>`;
  } else if (f.mode === 'nominate') {
    h += picks(p.options);
    h += textarea(f.picks[0] ? `Why ${f.picks[0]}? (your accusation)` : 'Pick a player to nominate, or pass', p.words, 2);
    h += `<div class="actions"><button class="primary blood" id="go" ${f.picks.length ? '' : 'disabled'}>${f.picks[0] ? 'Nominate ' + esc(f.picks[0] === T.me.seat ? 'yourself' : f.picks[0]) : 'Nominate'}</button><button class="ghost" id="pass">Pass</button></div>`;
    h += slayer();
  } else if (f.mode === 'vote') {
    h += f.remark ? textarea('A short remark (optional)', p.words, 1) : '<div class="slayer-row"><button class="linkish" id="remark">Add a remark…</button></div>';
    h += `<div class="vote-btns"><button class="primary blood" id="yes">✋ Raise hand</button><button class="ghost" id="no">Keep it down</button></div>`;
  } else if (f.mode === 'defense') {
    h += textarea('Your defense, to the whole town', p.words, 3);
    h += `<div class="actions"><button class="primary" id="go">Defend</button><button class="ghost" id="pass">Say nothing</button></div>`;
  } else {
    h += textarea(p.kind === 'comment' ? 'Speak before the vote (or stay quiet)' : 'Speak to the whole town…', p.words, 2);
    h += `<div class="actions"><button class="primary" id="go" ${words(f.text) || f.shot ? '' : 'disabled'}>${f.shot && !words(f.text) ? 'Shoot' : 'Speak'}</button><button class="ghost" id="pass">Stay quiet</button></div>`;
    h += slayer();
  }
  if (f.err) h += `<p class="err">${esc(f.err)}</p>`;
  dock.innerHTML = h;

  dock.querySelectorAll('[data-pick]').forEach((b) => b.onclick = () => togglePick(b.dataset.pick));
  dock.querySelectorAll('[data-shot]').forEach((b) => b.onclick = () => { f.shot = f.shot === b.dataset.shot ? null : b.dataset.shot; renderDock(); });
  const ta = $('say');
  if (ta) {
    const limit = f.mode === 'whisper' ? p.whisper_words : p.words;
    ta.oninput = () => {
      f.text = ta.value;
      const c = $('count'), n = words(f.text);
      c.textContent = n > limit ? `${n}/${limit} · cut at ${limit}` : `${n}/${limit}`;
      c.classList.toggle('over', n > limit);
      const go = $('go');
      if (go && f.mode === 'whisper') go.disabled = !(f.picks.length && n);
      if (go && f.mode === 'speak') { go.disabled = !(n || f.shot); go.textContent = f.shot && !n ? 'Shoot' : 'Speak'; }
    };
    ta.onkeydown = (e) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); ($('go') || $('yes'))?.click(); } };
  }
  const on = (id, fn) => { const b = $(id); if (b) b.onclick = fn; };
  on('shot-open', () => { f.showShot = true; renderDock(); });
  on('shot-close', () => { f.showShot = false; f.shot = null; renderDock(); });
  on('remark', () => { f.remark = true; renderDock(); $('say')?.focus(); });
  on('go', () => submit(false));
  on('pass', () => submit(true));
  on('yes', () => submit(false, true));
  on('no', () => submit(false, false));
  setDockHeight();
}

function setDockHeight() { document.documentElement.style.setProperty('--dock-h', $('dock').offsetHeight + 'px'); }

async function submit(pass, vote) {
  const p = T.pending, f = T.form;
  const a = { say: '', whispers: [], nominate: null, vote: null, targets: [], slayer_shot: null };
  if (!pass) {
    if (f.mode === 'night') a.targets = f.picks.slice();
    else if (f.mode === 'whisper') a.whispers = [{ to: f.picks.slice(), text: f.text.trim() }];
    else if (f.mode === 'nominate') { a.nominate = f.picks[0]; a.say = f.text.trim(); }
    else if (f.mode === 'vote') { a.vote = vote; a.say = f.text.trim(); }
    else a.say = f.text.trim();
    if (f.shot && (f.mode === 'speak' || f.mode === 'nominate')) a.slayer_shot = f.shot;
  } else if (f.shot && (f.mode === 'speak' || f.mode === 'nominate')) a.slayer_shot = f.shot;
  try {
    await api('/api/act', { turn: p.turn, action: a });
    T.sent = p.turn;
    document.title = 'Clocktower';
    renderDock(); renderTown();
  } catch (e) { f.err = e.message; renderDock(); }
}

// ---------------------------------------------------------------- turn alerts
let audio = null;
function unlockAudio() { try { audio = audio || new (window.AudioContext || window.webkitAudioContext)(); audio.resume(); } catch { /* no audio */ } }
function chime() {
  if (!sound || !audio) return;
  const t = audio.currentTime;
  [[523.25, 0], [783.99, 0.14], [1046.5, 0.28]].forEach(([fq, dt]) => {
    const o = audio.createOscillator(), g = audio.createGain();
    o.type = 'sine'; o.frequency.value = fq;
    g.gain.setValueAtTime(0.0001, t + dt);
    g.gain.exponentialRampToValueAtTime(0.12, t + dt + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dt + 1.6);
    o.connect(g).connect(audio.destination); o.start(t + dt); o.stop(t + dt + 1.7);
  });
}
function alertTurn() {
  chime();
  try { navigator.vibrate && navigator.vibrate([60, 40, 60]); } catch { /* ignore */ }
  document.title = '● Your turn · Clocktower';
}
document.addEventListener('pointerdown', unlockAudio, { once: true });

// ---------------------------------------------------------------- sheets
let rules = null;
async function openSheet(kind) {
  const body = $('sheet-body'), me = T.me;
  $('sheet').dataset.kind = kind;
  $('sheet').hidden = false; $('scrim').hidden = false;
  document.querySelectorAll('.tools .icon').forEach((b) => b.classList.toggle('on', b.dataset.sheet === kind));
  if (kind === 'town') {
    $('sheet-title').textContent = 'The town';
    body.innerHTML = '<div class="circle"></div><p class="fine center">Clockwise from the top. Tap a player to see only what involves them.</p>';
    renderCircle(body.querySelector('.circle'));
  } else if (kind === 'me') {
    $('sheet-title').textContent = 'Your character';
    const names = T.players.map((p) => p.name), i = names.indexOf(me.seat), n = names.length;
    const known = Object.entries(me.known);
    body.innerHTML = `<div class="mecard${me.evil ? ' evil' : ''}"><span class="token ${me.evil ? 'evil' : 'good'}"><span class="role">${esc(me.character)}</span></span>
      <div><h4 style="margin-top:0">${esc(me.seat)} · ${esc(me.kind)}</h4><p>${esc(me.ability)}</p></div></div>
      <p class="fine">You are on the <b>${me.evil ? 'evil' : 'good'}</b> team${me.alive ? '' : ', and dead: you still talk and whisper, and have one ghost vote'}.</p>
      <h4>Your neighbours</h4><div class="kv"><span>${esc(names[(i - 1 + n) % n])}</span><span>${esc(names[(i + 1) % n])}</span></div>
      ${known.length ? `<h4>Your evil team</h4><div class="kv">${known.map(([nm, r]) => `<span class="evil">${esc(nm)} · ${r}</span>`).join('')}</div>` : ''}
      ${me.bluffs.length ? `<h4>Not in play (safe bluffs)</h4><div class="kv">${me.bluffs.map((b) => `<span>${esc(b)}</span>`).join('')}</div>` : ''}
      <h4>What the Storyteller has told you</h4>${[...$('feed').querySelectorAll('[data-cat="st"] .card-ev.st p')].map((p) => `<p>${esc(p.textContent)}</p>`).join('') || '<p class="fine">Nothing yet.</p>'}`;
  } else if (kind === 'script') {
    $('sheet-title').textContent = 'Trouble Brewing';
    rules = rules || await api('/api/rules');
    const n = T.players.length || 10, [tf, os, mn] = SETUPS[n] || SETUPS[10];
    const group = (k, title) => `<h4>${title}</h4>` + rules.characters.filter((c) => c.kind === k).map((c) => `<div class="char ${c.kind}${me && c.name === me.character ? ' mine' : ''}">
      <span class="mini-token ${c.kind === 'Minion' || c.kind === 'Demon' ? 'evil' : 'good'}">${esc(c.name[0])}</span><div><b>${esc(c.name)}</b><span>${esc(c.ability)}</span></div></div>`).join('');
    body.innerHTML = `<p class="fine">This table of ${n}: ${tf} Townsfolk, ${os} Outsider${os === 1 ? '' : 's'}, ${mn} Minion${mn === 1 ? '' : 's'} and the Imp (a Baron adds two Outsiders in place of two Townsfolk). * = not on the first night.</p>`
      + group('Townsfolk', 'Townsfolk · good') + group('Outsider', 'Outsiders · good') + group('Minion', 'Minions · evil') + group('Demon', 'Demon · evil');
  } else if (kind === 'rules') {
    $('sheet-title').textContent = 'How this table works';
    rules = rules || await api('/api/rules');
    const parts = rules.text.split(/\n(?=[A-Z][A-Z ]+\n)/);
    const keep = parts.filter((s) => !/^(CHARACTERS|YOUR RESPONSE)\n/.test(s));
    body.innerHTML = `<div class="rules"><p class="note">This is, word for word, what every AI player at this table was told (its system prompt), minus the characters (see the book) and the reply format. You have the same moves: one whisper per private-time turn, speech in the town square, nominations, votes and night choices, under the same word limits. Like the AIs, you can't see who is waiting on whom.</p>`
      + keep.map((s) => { const [hd, ...rest] = s.split('\n'); return /^[A-Z ]+$/.test(hd) ? `<h4>${esc(hd.toLowerCase())}</h4><p>${esc(rest.join('\n'))}</p>` : `<p>${esc(s)}</p>`; }).join('') + '</div>';
  } else if (kind === 'notes') {
    $('sheet-title').textContent = 'Your notes';
    const key = `ct.notes.${T.game}.${me.seat}`;
    body.innerHTML = `<p class="fine">Private to this device. The AI players keep their own private reasoning from turn to turn; this is yours.</p><textarea id="notes-pad" placeholder="Claims, alibis, who whispered what…">${esc(store.get(key) || '')}</textarea>`;
    $('notes-pad').oninput = (e) => store.set(key, e.target.value);
  }
}
function closeSheet() { $('sheet').hidden = true; $('scrim').hidden = true; document.querySelectorAll('.tools .icon').forEach((b) => b.classList.remove('on')); }

// ---------------------------------------------------------------- reveal
function renderReveal() {
  const R = T.reveal, me = T.me;
  if (!R) return;
  const box = $('reveal');
  box.className = R.winner === 'evil' ? 'evil' : '';
  const title = R.winner ? `${R.winner === 'good' ? 'Good' : 'Evil'} wins` : 'The game stopped';
  box.innerHTML = `<div class="rv"><div class="crest">The Grimoire is opened</div><h2>${title}</h2><p class="why">${esc(R.reason || '')}</p>
    <div class="rv-grid">${R.seats.map((s, i) => {
      const was = s.started && s.started !== s.character ? `<small>was the ${esc(s.started)}</small>` : '';
      const thought = s.shown ? `<small>thought they were the ${esc(s.shown)}</small>` : '';
      const model = (models[(s.model || '').split('@')[0]] || s.model || '').replace(/ \(.*\)$/, '');
      const by = s.player ? `<small class="human">${esc(s.player)}</small>` : `<small>${esc(model)}</small>`;
      return `<div class="rv-seat${s.evil ? ' evil' : ''}${s.alive ? '' : ' dead'}${s.name === me.seat ? ' you' : ''}" style="animation-delay:${i * 60}ms">
        <span class="token ${s.evil ? 'evil' : 'good'}"><span class="role">${esc(s.character)}</span></span><b>${esc(s.name)}${s.name === me.seat ? ' (you)' : ''}</b>${was}${thought}${by}</div>`;
    }).join('')}</div>
    <p class="fine">Demon bluffs: ${(R.bluffs || []).map(esc).join(', ')}${R.red_herring ? ` · Fortune Teller's red herring: ${esc(R.red_herring)}` : ''}</p>
    <div class="rv-actions"><button class="primary" id="rv-read">Read every AI's reasoning</button><button class="ghost" id="rv-close">Back to the table</button>
    <button class="ghost" id="rv-lobby">Back to the lobby</button></div></div>`;
  box.hidden = false;
  $('rv-read').onclick = () => window.open('/api/transcript?token=' + encodeURIComponent(token), '_blank');
  $('rv-close').onclick = () => { box.hidden = true; };
  $('rv-lobby').onclick = async () => {
    try { await api('/api/reset', {}); } catch { /* not the host: just go back */ }
    box.hidden = true; clearTimeout(tableTimer); T.game = null; pollLobby();
  };
}

// ---------------------------------------------------------------- boot
function boot() {
  const m = location.hash.match(/host=([\w-]+)/);
  if (m) hostKey = m[1];
  wireLobby();
  $('town-btn').innerHTML = ICON.town;
  document.querySelector('[data-sheet="script"]').innerHTML = ICON.book;
  document.querySelector('[data-sheet="rules"]').innerHTML = ICON.scroll;
  document.querySelector('[data-sheet="notes"]').innerHTML = ICON.pen;
  const sb = $('sound-btn');
  const paintSound = () => { sb.innerHTML = sound ? ICON.sound : ICON.mute; sb.title = sound ? 'Turn chime on' : 'Turn chime off'; };
  paintSound();
  sb.onclick = () => { sound = !sound; store.set('ct.sound', sound ? 'on' : 'off'); unlockAudio(); paintSound(); };
  document.querySelectorAll('[data-sheet]').forEach((b) => b.onclick = () => openSheet(b.dataset.sheet));
  $('me-chip').onclick = () => openSheet('me');
  $('sheet-close').onclick = closeSheet;
  $('scrim').onclick = closeSheet;
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSheet(); });
  $('jump').onclick = () => { const f = $('feed'); f.scrollTop = f.scrollHeight; $('jump').hidden = true; };
  $('feed').addEventListener('scroll', () => { const f = $('feed'); if (f.scrollHeight - f.scrollTop - f.clientHeight < 60) $('jump').hidden = true; });
  window.addEventListener('resize', () => { if (!$('table').hidden) renderTown(); setDockHeight(); });
  resetTable(null);
  renderFilters();
  pollLobby();
}
boot();
