// usage: node shot.js file.html outprefix [slideIndexes comma] [width height]
const { chromium } = require('playwright');
(async () => {
  const [, , file, prefix, idxs, w, h] = process.argv;
  const b = await chromium.launch({ executablePath: process.env.CHR });
  const p = await b.newPage({ viewport: { width: +(w || 1440), height: +(h || 900) } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(file));
  await p.waitForTimeout(400);
  if (idxs) {
    for (const i of idxs.split(',')) {
      await p.evaluate(n => show(+n), i);
      await p.waitForTimeout(700);
      await p.screenshot({ path: `${prefix}-${i}.png` });
    }
  } else {
    await p.screenshot({ path: `${prefix}.png`, fullPage: true });
  }
  console.log('errors:', JSON.stringify(errs));
  await b.close();
})();
