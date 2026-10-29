(async function () {
  const { $, $$, esc } = CT;
  const [R, charts] = await Promise.all([CT.ratings(), CT.json('data/charts.json')]);
  const ms = R.models.slice().sort((a, b) => b.combined - a.combined);
  $('#lb-lede').textContent = `Eleven models released in 2026, ${R.games} rated games. Every model plays both sides: its rating combines how well it hunts the Demon as the town and how well it hides as the Demon's team.`;

  // Ranked table with interval bars on a shared scale.
  const lo = Math.min(...ms.map((m) => m.c90[0])) - 20, hi = Math.max(...ms.map((m) => m.c90[1])) + 20;
  const pos = (v) => ((v - lo) / (hi - lo) * 100).toFixed(2) + '%';
  $('#table').innerHTML = `<thead><tr><th class="num">#</th><th>Model</th><th class="num">Rating</th><th class="hide-sm" style="min-width:150px">90% interval</th>
    <th class="num">Detection</th><th class="num">Deception</th><th class="num hide-sm">As good</th><th class="num hide-sm">As evil</th><th class="hide-sm">Released</th></tr></thead><tbody>` +
    ms.map((m, i) => {
      const lab = CT.lab(R, m.id), c = lab === 'Anthropic' ? 'var(--anth)' : 'var(--oai)';
      return `<tr><td class="num rank">${i + 1}</td>
      <td style="white-space:nowrap">${CT.labMark(R, m.id)}<a href="games.html?model=${encodeURIComponent(m.id)}" style="color:var(--ink);text-decoration:none;font-weight:600">${esc(CT.name(R, m.id))}</a><div class="small muted" style="padding-left:18px">${lab}</div></td>
      <td class="num" style="font-weight:700;font-size:1.05rem">${m.combined}</td>
      <td class="hide-sm"><div class="ci" title="${m.c90[0]}–${m.c90[1]}"><span class="bar" style="left:${pos(m.c90[0])};right:calc(100% - ${pos(m.c90[1])});background:${c}"></span><span class="dot" style="left:${pos(m.combined)};background:${c};border-radius:${lab === 'Anthropic' ? '50%' : '2px'}"></span></div></td>
      <td class="num">${m.detection}</td><td class="num">${m.deception}</td>
      <td class="num hide-sm">${m.good_wins}/${m.good_games}</td><td class="num hide-sm">${m.evil_wins}/${m.evil_games}</td>
      <td class="hide-sm small muted">${CT.fmtDate(m.date)}</td></tr>`;
    }).join('') + '</tbody>';

  // Rating by date, with a metric switch.
  const host = $('#chart-date');
  const trendCap = (m) => {
    const t = R.trend_per_year[{ combined: 'c', detection: 'd', deception: 'v' }[m]];
    $('#trend-cap').textContent = `Dashed line: the trend across the year, +${t[0]} Elo per year (90%: ${t[1][0]} to ${t[1][1]}). A model from the end of 2026 beats one from the start of the year almost every time.`;
  };
  CT.chartByDate(host, R, 'combined'); trendCap('combined');
  $$('#metric button').forEach((b) => b.addEventListener('click', () => {
    $$('#metric button').forEach((x) => x.setAttribute('aria-pressed', x === b));
    const fresh = host.cloneNode(false); $('#chart-date').replaceWith(fresh);  // a fresh node drops the old resize hook
    CT.chartByDate(fresh, R, b.dataset.m); trendCap(b.dataset.m);
  }));

  CT.chartSplit($('#chart-split'), R);

  CT.h2h($('#h2h'), R, 'both');
  $$('#h2h-mode button').forEach((b) => b.addEventListener('click', () => {
    $$('#h2h-mode button').forEach((x) => x.setAttribute('aria-pressed', x === b));
    CT.h2h($('#h2h'), R, b.dataset.m);
  }));
  window.addEventListener('ct-theme', () => CT.h2h($('#h2h'), R, ($$('#h2h-mode button').find((b) => b.getAttribute('aria-pressed') === 'true') || {}).dataset?.m || 'both'));

  CT.chartBelief($('#chart-belief'), charts.demon_belief);
  if (charts.evil_tilt) {
    CT.chartTilt($('#chart-tilt'), charts.evil_tilt);
    $('#tilt-cap').textContent = `In ${Math.round(charts.evil_tilt.p_good_gains * 100)}% of bootstrap resamples the good side gains with skill: catching a liar gets easier faster than lying does.`;
  }
  if (charts.mixed) {
    const drawMixed = (k) => {
      const fresh = $('#chart-mixed').cloneNode(false); $('#chart-mixed').replaceWith(fresh);
      CT.chartMixed(fresh, charts.mixed, R, k);
      const d = charts.mixed[k], label = { combined: 'Overall', detection: 'As good', deception: 'As evil' }[k];
      $('#mixed-cap').textContent = `${label}: mixed team ${d.mixed[0]} vs members' average ${d.members_mean[0]}. ${k === 'deception' ? 'Mixed evil teams won 4 of 66 games; this is the one split whose interval excludes zero.' : 'The interval includes zero: a small effect at most.'}`;
    };
    drawMixed('deception');
    $$('#mixed-mode button').forEach((b) => b.addEventListener('click', () => {
      $$('#mixed-mode button').forEach((x) => x.setAttribute('aria-pressed', x === b)); drawMixed(b.dataset.m);
    }));
  }
  const se = R.setup_effects;
  $('#setup').innerHTML = '<tbody>' + [['Good-side advantage', R.good_advantage], ['Spy in play', se['Spy']], ['Baron in play', se['Baron']], ['Scarlet Woman in play', se['Scarlet Woman']], ['11 players', se['11 players']], ['12 players', se['12 players']], ['Evil wins overall', Math.round(R.evil_win_rate * 100) + '%']]
    .map(([k, v]) => `<tr><td>${k}</td><td class="num" style="font-weight:600">${typeof v === 'number' && v > 0 ? '+' + v : v}</td></tr>`).join('') + '</tbody>';
})();
