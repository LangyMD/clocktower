// node render.js stills t1 t2 ...   |   node render.js frames [workers]
const { chromium } = require('playwright');
const fs = require('fs');
const D = __dirname;
(async () => {
  const TL = JSON.parse(fs.readFileSync(D + '/timeline.json'));
  const html = fs.readFileSync(D + '/scene.html', 'utf8').replace('__TIMELINE__', JSON.stringify(TL));
  fs.writeFileSync(D + '/scene_built.html', html);
  const browser = await chromium.launch();
  async function page() {
    const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('pageerror:', e.message));
    p.on('console', m => console.log('console:', m.text()));
    await p.goto('file://' + D + '/scene_built.html');
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    return p;
  }
  const mode = process.argv[2];
  if (mode === 'stills') {
    const p = await page(); fs.mkdirSync(D + '/test', { recursive: true });
    for (const t of process.argv.slice(3).map(Number)) { await p.evaluate(t => window.render(t), t); await p.screenshot({ path: `${D}/test/t${t.toFixed(1)}.png` }); }
  } else {
    const fps = 30, N = Math.ceil(TL.total * fps), W = +(process.argv[3] || 4);
    fs.mkdirSync(D + '/frames', { recursive: true });
    let next = 0, done = 0;
    await Promise.all([...Array(W)].map(async () => {
      const p = await page();
      while (true) {
        const i = next++; if (i >= N) break;
        const f = `${D}/frames/f${String(i).padStart(5, '0')}.jpg`;
        if (!fs.existsSync(f)) { await p.evaluate(t => window.render(t), i / fps); await p.screenshot({ path: f, type: 'jpeg', quality: 92 }); }
        if (++done % 300 === 0) console.log('frame', done, '/', N);
      }
    }));
  }
  await browser.close();
})();
