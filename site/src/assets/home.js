(async function () {
  const { $, config: C } = CT;
  // The video essay: embedded once its YouTube id is set; until then the section stays hidden.
  if (C.youtubeVideoId) {
    $('#essay').innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(C.youtubeVideoId)}" title="Clocktower Bench: the video essay" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe>`;
    $('#essay-block').hidden = false;
  } else if (C.videoUrl) {
    document.querySelector('.hero .btns').insertAdjacentHTML('beforeend', `<a class="btn" href="${CT.esc(C.videoUrl)}" target="_blank" rel="noopener">Watch the video essay ↗</a>`);
  }
  const R = await CT.ratings();
  const t = R.trend_per_year.c;
  // Four numbers from the fit, in a row under the hero.
  const best = R.models.slice().sort((a, b) => b.combined - a.combined)[0];
  $('#stats').innerHTML = [
    [CT.esc(CT.name(R, best.id)), `best at the game, rated ${best.combined}; ${best.good_wins} of ${best.good_games} wins as good`],
    [`+${t[0]}`, 'Elo a year gained by models released in 2026'],
    [`${Math.round(R.evil_win_rate * 100)}%`, 'of games won by the evil team'],
    [`${R.games}`, 'rated games, each deal played from both sides'],
  ].map(([b, s]) => `<div class="stat"><b>${b}</b><span>${CT.esc(s)}</span></div>`).join('');
  CT.board($('#board'), R, true);
  $('#board-note').textContent = `Elo ratings from one fit over ${R.games} rated games between eleven models released in 2026; 1500 is their average. The whisker is the 90% interval. New models gained about ${t[0]} Elo a year.`;
})();
