(async function () {
  const { $, esc, config: C } = CT;
  if (C.youtubeVideoId && !C.videoUrl) C.videoUrl = 'https://www.youtube.com/watch?v=' + encodeURIComponent(C.youtubeVideoId);

  // The video essay: embedded when its YouTube id is set; else the animatic still, linked when videoUrl is set.
  const essay = $('#essay');
  if (C.youtubeVideoId) {
    essay.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(C.youtubeVideoId)}" title="Clocktower Bench: the video essay" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
  } else if (C.videoUrl) {
    const a = document.createElement('a');
    a.className = 'video'; a.id = 'essay'; a.href = C.videoUrl; a.target = '_blank'; a.rel = 'noopener';
    a.innerHTML = essay.innerHTML; essay.replaceWith(a);
    $('#essay-soon').textContent = '▶ Watch the video essay';
  }

  // The two-minute explainer: shown only once a source actually loads.
  const v = $('#explainer');
  const srcs = [C.explainerVideo, C.explainerFallback].filter(Boolean);
  if (v && srcs.length) {
    v.addEventListener('loadedmetadata', () => { $('#video-block').hidden = false; }, { once: true });
    v.innerHTML = srcs.map((s) => `<source src="${esc(s)}" type="video/mp4">`).join('');
    v.load();
  }

  const R = await CT.ratings();
  CT.board($('#board'), R, true);
  const best = R.models.slice().sort((a, b) => b.combined - a.combined)[0];
  const t = R.trend_per_year.c;
  $('#board-note').textContent = `Elo ratings from one fit over ${R.games} rated games; 1500 is the average of the eleven models. Bars run to each rating; the whisker is its 90% interval. Across 2026, new models gained about ${t[0]} Elo a year.`;
  $('#stats').innerHTML = [
    [CT.name(R, best.id), `rated ${best.combined.toLocaleString('en-US')}; won ${best.good_wins} of ${best.good_games} games as good`],
    [`+${t[0]}`, 'Elo gained per year by models released in 2026'],
    [Math.round(R.evil_win_rate * 100) + '%', 'of games won by the evil team'],
    [R.games, 'rated games, each deal played from both sides'],
  ].map(([b, s]) => `<div class="stat"><b>${esc(b)}</b><span>${esc(s)}</span></div>`).join('');
  try { $('#hero-count').textContent = (await CT.json('data/index.json')).length; } catch (e) { /* keep the default */ }

  const hl = await CT.json('data/highlights.json');
  $('#hl-preview').innerHTML = hl.slice(0, 3).map((h) => {
    const hero = h.side === 'evil' ? h.evil : h.good, foe = h.side === 'evil' ? h.good : h.evil;
    const href = `game.html?g=${encodeURIComponent(h.id)}${h.day ? '&day=' + h.day : ''}${h.seq ? '&e=' + h.seq + (h.think ? '&think=1' : '') : ''}`;
    return `<a class="hlp" href="${href}"><div class="rc">
      <div class="hl-num" style="color:var(--faint)">${esc(h.skill)}</div>
      <h3>${esc(h.title)}</h3>
      <p class="tg">${esc(h.tagline)}</p>
      <div class="meta"><span class="chip ${h.side}">${CT.token(R, hero, 'xs')}${h.side === 'evil' ? 'Evil' : 'Good'}: ${esc(CT.name(R, hero))}</span><span class="chip">vs ${esc(CT.name(R, foe))}</span></div>
    </div></a>`;
  }).join('');
})();
