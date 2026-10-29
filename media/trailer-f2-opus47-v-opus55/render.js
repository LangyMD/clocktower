const { chromium } = require('playwright');
const fs = require('fs');
const D = __dirname;
(async () => {
  const S = JSON.parse(fs.readFileSync(D + '/schedule.json'));
  const html = fs.readFileSync(D + '/scene.html', 'utf8').replace('__SCHEDULE__', JSON.stringify(S));
  fs.writeFileSync(D + '/scene_built.html', html);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => console.log('console:', m.text()));
  page.on('pageerror', e => console.log('pageerror:', e.message));
  await page.goto('file://' + D + '/scene_built.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const mode = process.argv[2];
  if (mode === 'stills') {
    const times = process.argv.slice(3).map(Number);
    fs.mkdirSync(D + '/test', { recursive: true });
    for (const t of times) { await page.evaluate(t => window.render(t), t); await page.screenshot({ path: `${D}/test/t${t.toFixed(2)}.png` }); }
  } else {
    const fps = 30, total = S.total, N = Math.ceil(total * fps);
    fs.mkdirSync(D + '/frames', { recursive: true });
    for (let i = 0; i < N; i++) {
      await page.evaluate(t => window.render(t), i / fps);
      await page.screenshot({ path: `${D}/frames/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
      if (i % 300 === 0) console.log('frame', i, '/', N);
    }
  }
  await browser.close();
})();
