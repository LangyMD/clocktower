(async function () {
  const { $, esc } = CT;
  const [R, hl] = await Promise.all([CT.ratings(), CT.json('data/highlights.json')]);
  const link = (h) => `game.html?g=${encodeURIComponent(h.id)}${h.seq ? `&e=${h.seq}${h.think ? '&think=1' : ''}` : ''}`;
  $('#hl').innerHTML = hl.map((h, i) => {
    const hero = h.side === 'evil' ? h.evil : h.good, foe = h.side === 'evil' ? h.good : h.evil;
    return `<article class="hl-card sheet ${h.side}" id="h${i + 1}">
      <div class="hl-num">${String(i + 1).padStart(2, '0')} · ${esc(h.skill)}</div>
      <h3>${esc(h.title)}</h3>
      <p class="tagline">${esc(h.tagline)}</p>
      <div class="meta" style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px">
        <span class="chip ${h.side}">${CT.token(R, hero, 'xs')}${h.side === 'evil' ? 'Evil' : 'Good'}: ${esc(CT.name(R, hero))}</span>
        <span class="chip">vs ${esc(CT.name(R, foe))}</span>
        <span class="chip gold">${h.winner === 'good' ? 'Good' : 'Evil'} wins, day ${h.days}</span>
      </div>
      ${h.story.map((p) => `<p>${esc(p)}</p>`).join('')}
      ${h.quote ? `<blockquote>"${esc(h.quote)}…"</blockquote>` : ''}
      <p class="why"><b>Why it's hard:</b> ${esc(h.why)}</p>
      <div class="btns" style="margin-top:14px">
        ${h.seq ? `<a class="btn primary" href="${link(h)}">Jump to the moment${h.day ? ` (day ${h.day})` : ''}</a>` : ''}
        <a class="btn" href="game.html?g=${encodeURIComponent(h.id)}">Read from the start</a>
      </div>
    </article>`;
  }).join('');
})();
