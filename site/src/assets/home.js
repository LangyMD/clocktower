(async function () {
  const { $, esc, config: C } = CT;

  // Live stream: a YouTube video id (a live event) or a channel id (its current live stream); else "coming soon".
  const stream = $('#stream');
  const yt = C.youtubeVideoId ? `https://www.youtube-nocookie.com/embed/${encodeURIComponent(C.youtubeVideoId)}`
    : C.youtubeChannelId ? `https://www.youtube.com/embed/live_stream?channel=${encodeURIComponent(C.youtubeChannelId)}` : '';
  if (yt) {
    stream.innerHTML = `<iframe src="${yt}" title="Clocktower Bench live stream" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
    $('#stream-kicker').innerHTML = '<span class="live-dot"></span>Live on YouTube';
  } else {
    stream.innerHTML = `<div class="soon"><div>
      <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="24" cy="24" r="19"/><circle cx="24" cy="24" r="15" opacity=".5"/><path d="M24 12v12l8 5" stroke-linecap="round" stroke-width="2"/></svg>
      <h3>The stream is coming soon</h3><p>A round-the-clock table of AI players, with the Grimoire open so you can see who is lying. Until then, <a href="games.html">watch any past game</a>.</p></div></div>`;
  }

  // Explainer video: local copy if published with the site, else the dataset's copy.
  const v = $('#explainer');
  if (v) {
    const srcs = [C.explainerVideo, C.explainerFallback].filter(Boolean);
    v.innerHTML = srcs.map((s) => `<source src="${esc(s)}" type="video/mp4">`).join('');
  }

  const R = await CT.ratings();
  CT.chartByDate($('#chart-date'), R, 'combined');
  const best = R.models.slice().sort((a, b) => b.combined - a.combined)[0];
  const t = R.trend_per_year.c;
  $('#chart-cap').textContent = `Elo ratings from one fit over ${R.games} rated games; 1500 is the average of the eleven models. Dashed: the trend, about +${t[0]} Elo a year (90%: ${t[1][0]} to ${t[1][1]}).`;
  $('#stats').innerHTML = [
    [CT.name(R, best.id), `rated ${best.combined}; won ${best.good_wins} of ${best.good_games} games as good`],
    [`+${t[0]}`, 'Elo gained per year by models released in 2026'],
    [Math.round(R.evil_win_rate * 100) + '%', 'of games won by the evil team'],
    [R.games, 'rated games, each deal played from both sides'],
  ].map(([b, s]) => `<div class="stat"><b>${esc(b)}</b><span>${esc(s)}</span></div>`).join('');
  try {
    const idx = await CT.json('data/index.json');
    $('#hero-count').textContent = idx.length;
  } catch (e) { /* keep the default */ }

  const hl = await CT.json('data/highlights.json');
  $('#hl-preview').innerHTML = hl.slice(0, 3).map((h) => `
    <a class="gcard" href="game.html?g=${encodeURIComponent(h.id)}${h.day ? '&day=' + h.day : ''}${h.seq ? '&e=' + h.seq + (h.think ? '&think=1' : '') : ''}" style="padding:18px">
      <div class="hl-num">${esc(h.skill)}</div>
      <h3 style="margin:8px 0 6px">${esc(h.title)}</h3>
      <div class="muted" style="font-family:var(--serif)">${esc(h.tagline)}</div>
      <div class="meta"><span class="chip ${h.side}">${h.side === 'evil' ? 'Evil' : 'Good'}: ${esc(CT.name(R, h.side === 'evil' ? h.evil : h.good))}</span><span class="chip">vs ${esc(CT.name(R, h.side === 'evil' ? h.good : h.evil))}</span></div>
    </a>`).join('');
})();
