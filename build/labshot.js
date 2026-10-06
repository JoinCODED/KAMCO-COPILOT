const { chromium } = require('playwright');
(async () => {
  const [, , file, prefix, ids] = process.argv;
  const b = await chromium.launch({ executablePath: process.env.CHR });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + require('path').resolve(file)); await p.waitForTimeout(300);
  await p.screenshot({ path: prefix + '-home.png' });
  for (const id of (ids||'').split(',').filter(Boolean)) { await p.evaluate(i => openChallenge(i), id); await p.waitForTimeout(300); await p.screenshot({ path: `${prefix}-${id}.png`, fullPage: true }); }
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
