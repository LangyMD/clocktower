/* About: the repository URL in the quick start, and the two-minute explainer once a source actually loads. */
(function () {
  const C = CT.config;
  if (C.githubUrl) document.getElementById('repo-url').textContent = C.githubUrl.replace(/\/$/, '') + '.git';
  const v = document.getElementById('explainer');
  const srcs = [C.explainerVideo, C.explainerFallback].filter(Boolean);
  if (v && srcs.length) {
    v.addEventListener('loadedmetadata', () => { document.getElementById('explainer-box').hidden = false; }, { once: true });
    v.innerHTML = srcs.map((s) => `<source src="${CT.esc(s)}" type="video/mp4">`).join('');
    v.load();
  }
})();
