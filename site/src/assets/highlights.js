/* Highlights: a plain list. Only games that are in this build (with their transcript) are listed. */
(async function () {
  const { $, esc } = CT;
  const [R, hl, index] = await Promise.all([CT.ratings(), CT.json('data/highlights.json'), CT.json('data/index.json').catch(() => [])]);
  const have = new Set(index.map((g) => g.id));
  const list = hl.filter((h) => have.has(h.id));
  if (!list.length) { $('#hl').outerHTML = '<div class="empty"><b>No highlights in this build yet.</b>They appear once their games are in it. <a href="games.html">Browse the games instead.</a></div>'; return; }
  const moment = (h) => `game.html?g=${encodeURIComponent(h.id)}${h.day ? '&day=' + h.day : ''}${h.seq ? `&e=${h.seq}${h.think ? '&think=1' : ''}` : ''}`;
  const team = (t, side) => `<span class="m">${CT.token(R, t, 'xs')}<span class="${side}">${side === 'good' ? 'Good' : 'Evil'}</span> ${esc(CT.name(R, t))}</span>`;
  $('#hl').innerHTML = list.map((h, i) => `<li class="hl-item" id="h${i + 1}"><span class="n">${String(i + 1).padStart(2, '0')}</span><div>
      <h2><a href="${moment(h)}">${esc(h.title)}</a></h2>
      <p class="tg">${esc(h.tagline)}</p>
      <div class="meta">${team(h.good, 'good')}<span class="muted">vs</span>${team(h.evil, 'evil')}<span class="muted">· ${h.winner === 'good' ? 'Good' : 'Evil'} wins on day ${h.days} · ${esc(h.skill)}</span></div>
      <div class="links">${h.seq ? `<a href="${moment(h)}">Jump to the moment${h.day ? ` (day ${h.day})` : ''} →</a>` : ''}<a href="game.html?g=${encodeURIComponent(h.id)}">Read from the start</a></div>
      <details><summary>The story</summary><div class="story">${h.story.map((p) => `<p>${esc(p)}</p>`).join('')}${h.quote ? `<blockquote>“${esc(h.quote)}…”</blockquote>` : ''}<p><b>Why it's hard:</b> ${esc(h.why)}</p></div></details>
    </div></li>`).join('');
  CT.markTerms($('#hl'));
})();
