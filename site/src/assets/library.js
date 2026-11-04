/* The games list: one row per game, filters and sort in the URL, 50 rows a page. Only games exported with their
   transcript are in data/index.json, so every row opens a full replay. */
(async function () {
  const { $, $$, esc } = CT;
  let R, games;
  try { [R, games] = await Promise.all([CT.ratings(), CT.json('data/index.json')]); }
  catch (e) { $('#count').textContent = ''; $('#glist').innerHTML = `<div class="empty"><b>The games didn't load.</b>${esc(e.message)}</div>`; return; }
  const PAGE = 50;
  const ids = new Set(games.map((g) => g.id));
  const teams = [...new Set(games.flatMap((g) => [g.good, g.evil]))];
  const order = (id) => { const m = R.models.find((x) => x.id === id); return m ? m.date : '9999' + id; };
  teams.sort((a, b) => order(a).localeCompare(order(b)));
  const opts = teams.map((t) => `<option value="${esc(t)}">${esc(CT.name(R, t))}</option>`).join('');
  $('#f-model').insertAdjacentHTML('beforeend', opts);
  $('#f-vs').insertAdjacentHTML('beforeend', opts);

  // Filters live in the URL so a view can be shared (old links with ?good= or ?evil= still work).
  const F = { model: '#f-model', side: '#f-side', winner: '#f-winner', sort: '#f-sort', vs: '#f-vs', minion: '#f-minion', players: '#f-players', days: '#f-days', group: '#f-group' };
  const MORE = ['vs', 'minion', 'players', 'days', 'group'];
  const params = new URLSearchParams(location.search);
  if (params.get('good')) { params.set('model', params.get('good')); params.set('side', 'good'); }
  if (params.get('evil') && !params.get('good')) { params.set('model', params.get('evil')); params.set('side', 'evil'); }
  if (params.get('sort') === 'long') params.set('sort', 'days-desc');
  if (params.get('sort') === 'short') params.set('sort', 'days-asc');
  if (params.get('sort') === 'hidden') params.set('sort', 'hidden-asc');
  for (const [k, s] of Object.entries(F)) if (params.get(k)) $(s).value = params.get(k);
  let page = Math.max(1, +params.get('page') || 1);
  const showMore = (open) => { $('#more-filters').hidden = !open; $('#more-btn').setAttribute('aria-expanded', open); $('#more-btn').textContent = open ? 'Fewer filters' : 'More filters'; };
  showMore(MORE.some((k) => params.get(k)));

  const side = (t, team, g) => `<span class="side ${team === 'good' ? 'g' : 'e'}${g.winner === team ? '' : ' lost'}"><span class="who ${team}">${team}</span>${CT.token(R, t, 'sm')}<span>${esc(CT.name(R, t))}</span></span>`;
  const tag = (g) => (g.group === 'mixed' ? '<span class="tag">Mixed teams</span>' : g.group === 'unrated' ? '<span class="tag" title="An early game that hit a retry bug and was replayed">Not rated</span>' : '');
  const row = (g) => {
    const twin = g.twin && ids.has(g.twin) ? `<a class="twin" href="game.html?g=${encodeURIComponent(g.twin)}" title="The same deal with the sides swapped">Twin</a>` : '<span class="twin"></span>';
    const label = `${CT.name(R, g.good)} (good) against ${CT.name(R, g.evil)} (evil): ${g.winner} won on day ${g.days}`;
    return `<div class="grow-g" role="row"><a class="rowlink" href="game.html?g=${encodeURIComponent(g.id)}" aria-label="${esc(label)}"></a>
      ${side(g.good, 'good', g)}${side(g.evil, 'evil', g)}
      <span class="res ${g.winner}">${g.winner === 'good' ? 'Good' : 'Evil'} wins</span>
      <span class="day num">Day ${g.days}</span><span class="players num">${g.players}</span>
      <span class="minions">${g.minions.map(esc).join(', ')}${tag(g)}</span>
      <span class="meta">Day ${g.days} · ${g.players} players</span>${twin}</div>`;
  };
  const SORTS = {
    'days-desc': (a, b) => b.days - a.days, 'days-asc': (a, b) => a.days - b.days,
    'players-desc': (a, b) => b.players - a.players, 'players-asc': (a, b) => a.players - b.players,
    'winner-good': (a, b) => (a.winner === 'good' ? 0 : 1) - (b.winner === 'good' ? 0 : 1),
    'winner-evil': (a, b) => (a.winner === 'evil' ? 0 : 1) - (b.winner === 'evil' ? 0 : 1),
    'hidden-asc': (a, b) => a.demonBelief - b.demonBelief,
  };
  const HEAD = [['good', 'Good team'], ['evil', 'Evil team'], ['winner', 'Winner', ['winner-good', 'winner-evil']], ['days', 'Ends', ['days-desc', 'days-asc']], ['players', 'Players', ['players-desc', 'players-asc']], ['minions', 'Minions'], ['twin', '']];
  const head = (sort) => `<div class="ghead" role="row">${HEAD.map(([k, label, cyc]) => {
    if (!cyc) return `<span role="columnheader">${label}</span>`;
    const on = cyc.includes(sort), dir = on ? (sort.endsWith('asc') || sort === 'winner-good' ? 'ascending' : 'descending') : 'none';
    return `<span role="columnheader"><button type="button" data-cyc="${cyc.join(' ')}" aria-sort="${dir}" title="Sort by ${label.toLowerCase()}">${label}</button></span>`;
  }).join('')}</div>`;

  function apply(keepPage) {
    const v = Object.fromEntries(Object.entries(F).map(([k, s]) => [k, $(s).value]));
    $('#f-side').disabled = !v.model;
    if (!v.model) v.side = '';
    if (!keepPage) page = 1;
    let list = games.filter((g) => {
      if (v.model && !(v.side === 'good' ? g.good === v.model : v.side === 'evil' ? g.evil === v.model : g.good === v.model || g.evil === v.model)) return false;
      if (v.vs && !(v.model ? (g.good === v.model ? g.evil === v.vs : g.good === v.vs) : g.good === v.vs || g.evil === v.vs)) return false;
      if (v.winner && g.winner !== v.winner) return false;
      if (v.minion && !g.minions.includes(v.minion)) return false;
      if (v.players && g.players !== +v.players) return false;
      if (v.group && g.group !== v.group) return false;
      if (v.days) { const [a, b] = v.days.split('-').map(Number); if (g.days < a || g.days > b) return false; }
      return true;
    });
    if (v.sort === 'hidden-asc') list = list.filter((g) => g.demonBelief != null);
    if (SORTS[v.sort]) list = list.slice().sort(SORTS[v.sort]);
    const pages = Math.max(1, Math.ceil(list.length / PAGE));
    page = Math.min(page, pages);
    const q = new URLSearchParams(Object.entries(v).filter(([, x]) => x));
    if (page > 1) q.set('page', page);
    history.replaceState(null, '', q.toString() ? '?' + q : location.pathname);
    const filtered = Object.entries(v).some(([k, x]) => x && k !== 'sort');
    $('#clear').hidden = !filtered;
    const good = list.filter((g) => g.winner === 'good').length;
    if (!games.length) {
      $('.fbar').hidden = true;
      $('#count').textContent = '';
      $('#glist').innerHTML = '<div class="empty"><b>No games here yet.</b>Games appear once their logs are in this build.</div>';
      $('#pager').innerHTML = ''; return;
    }
    if (!list.length) {
      $('#count').textContent = '';
      $('#glist').innerHTML = '<div class="empty"><b>No games match these filters.</b><button type="button" class="linkbtn" data-clear>Clear filters</button></div>';
      $('#pager').innerHTML = '';
      $('[data-clear]').addEventListener('click', clear); return;
    }
    $('#count').innerHTML = `<b>${list.length}</b> game${list.length === 1 ? '' : 's'} · good won ${good}, evil won ${list.length - good}`;
    const shown = list.slice((page - 1) * PAGE, page * PAGE);
    $('#glist').innerHTML = `<div class="glist" role="table" aria-label="Games">${head(v.sort)}${shown.map(row).join('')}</div>`;
    $$('#glist [data-cyc]').forEach((b) => b.addEventListener('click', () => {
      const cyc = b.dataset.cyc.split(' '), i = cyc.indexOf($('#f-sort').value);
      $('#f-sort').value = i === 0 ? cyc[1] : i === 1 ? '' : cyc[0];
      apply();
    }));
    $('#pager').innerHTML = pages < 2 ? '' : `${page > 1 ? '<button class="btn btn-sm" data-p="-1">← Previous</button>' : '<span></span>'}
      <span class="pos">Page ${page} of ${pages}</span>${page < pages ? '<button class="btn btn-sm" data-p="1">Next →</button>' : '<span></span>'}`;
    $$('#pager [data-p]').forEach((b) => b.addEventListener('click', () => { page += +b.dataset.p; apply(true); $('#count').scrollIntoView({ block: 'start' }); }));
  }
  function clear() { Object.entries(F).forEach(([k, s]) => { if (k !== 'sort') $(s).value = ''; }); apply(); }
  Object.values(F).forEach((s) => $(s).addEventListener('change', () => apply()));
  $('#more-btn').addEventListener('click', () => showMore($('#more-filters').hidden));
  $('#clear').addEventListener('click', clear);
  apply(true);
})();
