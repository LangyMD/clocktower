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
  CT.board($('#board'), R, true);
  const t = R.trend_per_year.c;
  $('#board-note').textContent = `Elo ratings from one fit over ${R.games} rated games between eleven models released in 2026; 1500 is their average. The whisker is the 90% interval.`;
  // The same ratings against each model's release date: the year's trend at a glance.
  CT.chartByDate($('#chart-date'), R, 'combined');
  $('#trend-cap').textContent = `Each model on the day it was released. Dashed line: the trend, +${t[0]} Elo a year (90%: ${t[1][0]} to ${t[1][1]}). A model from the end of 2026 beats one from the start of the year almost every time.`;
})();
