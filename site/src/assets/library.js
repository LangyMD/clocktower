(async function () {
  const { $, $$, esc } = CT;
  const [R, games] = await Promise.all([CT.ratings(), CT.json('data/index.json')]);
  const teams = [...new Set(games.flatMap((g) => [g.good, g.evil]))];
  const order = (id) => { const m = R.models.find((x) => x.id === id); return m ? m.date : '9999' + id; };
  teams.sort((a, b) => order(a).localeCompare(order(b)));
  const opts = teams.map((t) => `<option value="${esc(t)}">${esc(CT.name(R, t))}</option>`).join('');
  ['#f-model', '#f-good', '#f-evil'].forEach((s) => $(s).insertAdjacentHTML('beforeend', opts));

  // Filters live in the URL so a filtered view can be shared.
  const params = new URLSearchParams(location.search);
  const F = { model: '#f-model', good: '#f-good', evil: '#f-evil', winner: '#f-winner', minion: '#f-minion', days: '#f-days', group: '#f-group', sort: '#f-sort' };
  for (const [k, s] of Object.entries(F)) if (params.get(k)) $(s).value = params.get(k);

  // On phones the filters fold away unless the link already carries some.
  if (matchMedia('(max-width: 700px)').matches && ![...params.keys()].length) $('#filters-box').open = false;
  const PAGE = 48;
  let shown = PAGE;
  const minionChip = (m) => `<span class="chip">${esc(m)}</span>`;
  const card = (g) => {
    const belief = g.demonBelief == null ? '' : `<span class="chip" title="The town's final average belief that the real Demon was the Demon">Demon suspected ${g.demonBelief}%</span>`;
    return `<a class="gcard" href="game.html?g=${encodeURIComponent(g.id)}">
      ${CT.vsTeams(R, g, 'md')}
      <div class="meta"><span class="chip ${g.winner}">${g.winner === 'good' ? 'Good' : 'Evil'} wins, day ${g.days}</span><span class="chip">${g.players} players</span>${g.minions.map(minionChip).join('')}${belief}${g.group === 'mixed' ? '<span class="chip gold">Mixed teams</span>' : g.group === 'unrated' ? '<span class="chip">Unrated</span>' : ''}</div>
      <div class="gid">${esc(g.id.replace(/^v1[67]\//, ''))}</div>
    </a>`;
  };
  function apply() {
    const v = Object.fromEntries(Object.entries(F).map(([k, s]) => [k, $(s).value]));
    const q = new URLSearchParams(Object.entries(v).filter(([k, x]) => x && !(k === 'sort' && x === 'batch')));
    history.replaceState(null, '', q.toString() ? '?' + q : location.pathname);
    let list = games.filter((g) => (!v.model || g.good === v.model || g.evil === v.model) && (!v.good || g.good === v.good) && (!v.evil || g.evil === v.evil) &&
      (!v.winner || g.winner === v.winner) && (!v.minion || g.minions.includes(v.minion)) && (!v.group || g.group === v.group) &&
      (!v.days || (() => { const [a, b] = v.days.split('-').map(Number); return g.days >= a && g.days <= b; })()));
    if (v.sort === 'long') list.sort((a, b) => b.days - a.days);
    if (v.sort === 'short') list.sort((a, b) => a.days - b.days);
    if (v.sort === 'hidden') list = list.filter((g) => g.demonBelief != null).sort((a, b) => a.demonBelief - b.demonBelief);
    const good = list.filter((g) => g.winner === 'good').length;
    $('#count').textContent = list.length ? `${list.length} game${list.length === 1 ? '' : 's'} · good won ${good}, evil won ${list.length - good}` : 'No games match these filters.';
    $('#games').innerHTML = list.slice(0, shown).map(card).join('');
    $('#more').hidden = list.length <= shown;
  }
  Object.values(F).forEach((s) => $(s).addEventListener('change', () => { shown = PAGE; apply(); }));
  $('#more').addEventListener('click', () => { shown += PAGE * 2; apply(); });
  apply();
})();
