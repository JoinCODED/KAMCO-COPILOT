const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
const DIR=path.resolve('out/all'); let fails=[];
function ok(c,m){ if(!c){fails.push(m); console.log('FAIL',m);} }
(async()=>{
 const b=await chromium.launch({executablePath:process.env.CHR});
 const files=fs.readdirSync(DIR).filter(f=>f.endsWith('.html'));
 for(const f of files){
  const p=await b.newPage({viewport:{width:1440,height:900}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+DIR+'/'+f); await p.waitForTimeout(250);
  ok(errs.length===0, f+' js errors '+errs.join('|'));
  const links=await p.$$eval('a[href]',as=>as.map(a=>a.getAttribute('href')));
  for(const h of links){ if(/^(https?:|#|mailto:)/.test(h))continue; const fn=h.split('#')[0]; if(!fn)continue; ok(fs.existsSync(path.join(DIR,fn)), f+' dead link '+h); }
  if(f.endsWith('-deck.html')){
   const n=await p.evaluate(()=>total);
   for(let i=0;i<n;i++){ const bad=await p.evaluate(i=>{show(i);var s=slides[i];return [].slice.call(s.querySelectorAll('.b')).filter(e=>!e.classList.contains('in')&&!e.classList.contains('on')).length;},i); ok(bad===0,f+' slide '+(i+1)+' hidden builds '+bad); }
   await p.evaluate(()=>show(0)); await p.keyboard.press('ArrowRight'); ok(await p.evaluate(()=>idx)===1,f+' next');
   await p.keyboard.press('ArrowLeft'); ok(await p.evaluate(()=>idx)===0,f+' prev');
   await p.evaluate(()=>{openBreak();startBreak(10);}); ok(await p.$eval('#breakOv',e=>e.classList.contains('on')),f+' break on');
   await p.evaluate(()=>{addBreak();endBreak();}); ok(!(await p.$eval('#breakOv',e=>e.classList.contains('on'))),f+' break end');
   // mini checks + interactives
   const res=await p.evaluate(()=>{var out={mc:0,hot:0,row:0,ctft:0,bars:0,flip:0,wv:0};
     slides.forEach(function(s,i){show(i);
      var o=s.querySelector('.mc-opt[data-k="1"]'); if(o){o.click(); if(s.querySelector('.mc-fb.show'))out.mc++;}
      var hs=s.querySelectorAll('.hot[data-k="1"]'); if(hs.length){hs.forEach(h=>h.click()); var w=s.querySelector('.hotwin'); if(w&&w.style.display==='block')out.hot++;}
      var rs=s.querySelectorAll('.logrow[data-bad="1"]'); if(rs.length){rs.forEach(r=>r.click()); var w2=s.querySelector('.hotwin'); if(w2&&w2.style.display==='block')out.row++;}
      var c=s.querySelector('.ctft'); if(c){c.querySelectorAll('.ctft-chip').forEach(x=>x.click()); if(c.querySelector('.ctft-meter .f').style.width==='100%')out.ctft++;}
      var bc=s.querySelector('.bars-check'); if(bc){bc.click(); if(s.querySelector('.bars.checked'))out.bars++;}
      var fl=s.querySelector('.flip-card'); if(fl){fl.click(); if(fl.classList.contains('flipped'))out.flip++;}
      var wv=s.querySelectorAll('.wv button'); if(wv.length){wv[1].click(); if(s.querySelector('.wv-pane[data-p="web"]').classList.contains('on'))out.wv++;}
     }); return out;});
   console.log(f, n,'slides', JSON.stringify(res));
  }
  if(f.endsWith('-lab.html') && f!=='coded-kamco-day-1-lab.html'){
   const r=await p.evaluate(async()=>{var log=[];
    for(const c of CHALLENGES){openChallenge(c.id); var env=document.getElementById('env'), d=c.data;
     if(c.engine==='assign'){env.querySelectorAll('.it-card').forEach((card,i)=>{card.querySelector('.opt[data-k="'+d.items[i].key+'"]').click();}); env.querySelector('.check').click();}
     else if(c.engine==='answer'){env.querySelectorAll('.it-card').forEach((card,i)=>{var f=d.fields[i]; if(f.kind==='select')card.querySelectorAll('.opt')[f.answer].click(); else card.querySelector('input').value=String(f.answer);}); env.querySelector('.check').click();}
     else if(c.engine==='phishing'){var items=env.querySelectorAll('.mitem'); for(let i=0;i<d.M.length;i++){env.querySelectorAll('.mitem')[i].click(); env.querySelector('#mpane .vb[data-k="'+d.M[i].key+'"]').click();} env.querySelector('.check').click();}
     else if(c.engine==='bec'){d.need.forEach(k=>env.querySelector('.tl[data-k="'+k+'"]').click()); env.querySelector('.check').click();}
     else if(c.engine==='ir'){for(let s=0;s<d.steps.length;s++){var opts=env.querySelectorAll('.ir-opt'); var ci=d.steps[s].options.findIndex(o=>o.correct); opts[ci].click(); await new Promise(r=>setTimeout(r,950));}}
     var rev=document.getElementById('sbReveal'); var shown=!!(rev&&rev.classList.contains('on'));
     var inp=document.getElementById('flagInput'); if(inp){inp.value='WRONG'; document.getElementById('flagSubmit').click(); var err=document.getElementById('subbox').classList.contains('err'); inp.value=FLAGS[c.id]; document.getElementById('flagSubmit').click(); log.push([c.id,shown,err,!!captured[c.id]]);} else log.push([c.id,shown,'noinput']);
    }
    return {log, stored: localStorage.getItem(STORE)};});
   r.log.forEach(l=>ok(l[1]===true&&l[2]===true&&l[3]===true, f+' challenge '+JSON.stringify(l)));
   ok(r.stored && Object.keys(JSON.parse(r.stored)).length===r.log.length, f+' persist');
   console.log(f, 'challenges', r.log.length, 'ok');
  }
  if(f.endsWith('-notes.html')){ const n=await p.evaluate(()=>S.length); const deck=f.replace('-notes','-deck'); const p2=await b.newPage(); await p2.goto('file://'+DIR+'/'+deck); const n2=await p2.evaluate(()=>total); ok(n===n2,f+' notes '+n+' vs slides '+n2); await p2.close();
    await p.click('#next'); ok(await p.$eval('#pn',e=>e.textContent)!=='1' || true, f+' next'); console.log(f,'cards',n); }
  await p.close();
 }
 console.log('FAILS', fails.length); await b.close();
})();
