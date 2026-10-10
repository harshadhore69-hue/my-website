/* Before / after for ONE page (run separately -- these files are 15-31 MB).
 *   node _before_after.js MBG_index.html
 *
 * Both versions get the same layout model. The original's real
 * IntersectionObserver callback is driven by a spec-faithful shim, because
 * jsdom ships none.
 *
 * Metrics are deliberately definition-free: they do not depend on where the
 * new rule draws its reference line.
 *   offScreen  -- the pill the page marked active is outside the visible strip
 *   backwards  -- the active index decreased while scrolling down
 *   unreachable-- a slide no scroll position ever marks active
 *   maxTrail   -- how many slides the indicator trails the slide at the top
 */
const { execSync } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { loadPage, PAGES } = require('./harness.js');

const file = process.argv[2];
const cfg = PAGES[file];
const origPath = path.join(os.tmpdir(), 'orig_' + file);
if (!fs.existsSync(origPath)) {
  fs.writeFileSync(origPath, execSync('git show HEAD:' + file, { cwd: __dirname, maxBuffer: 1 << 28 }));
}

const topOfViewportSlide = (h) => {
  const y = h.window.__test.scrollY;
  const top = cfg.headerH + cfg.railH;
  for (let i = 0; i < h.slides.length; i++) {
    if (h.window.__test.offsets[i] + h.window.__test.heights[i] - y > top) return i;
  }
  return h.slides.length - 1;
};

function sweep(h, label, note, checkVisibility) {
  const steps = 2000;
  const step = Math.max(1, Math.floor(h.window.__test.maxScroll / steps));
  let offScreen = 0, backwards = 0, maxTrail = 0, total = 0, prev = -1, none = 0;
  const seen = new Set();
  for (let y = 0; y <= h.window.__test.maxScroll; y += step) {
    h.scrollTo(y);
    const a = h.activeIndex();
    total++;
    if (a < 0) { none++; continue; }
    seen.add(a);
    if (checkVisibility && !h.pillVisible(a)) offScreen++;
    if (a < prev) backwards++;
    prev = a;
    const t = topOfViewportSlide(h);
    if (t - a > maxTrail) maxTrail = t - a;
  }
  const unreachable = h.slides.length - seen.size;
  console.log('  ' + label.padEnd(7) +
    ' off-screen:' + (checkVisibility ? String(offScreen).padStart(5) + '/' + total : '  n/a') +
    '   backwards:' + String(backwards).padStart(4) +
    '   never-active slides:' + String(unreachable).padStart(3) +
    '   max trail:' + String(maxTrail).padStart(3) + ' slide(s)' +
    (none ? '   no-active:' + none : ''));
  if (note) console.log('         ' + note);
  return { offScreen, backwards, unreachable, maxTrail, total };
}

const beforeSel = file === 'MBG_index.html' ? null : (file === 'StrategicUX_index.html' ? '.slide-nav' : '.pnav-grid-list');
const beforeCfg = beforeSel ? Object.assign({}, cfg, { railIn: beforeSel, stripW: 100000 }) : cfg;

const before = loadPage(file, beforeCfg, { src: origPath, io: 'faithful' });
console.log('\n=== ' + file + '  (' + before.slides.length + ' slides) ===');
const b = sweep(before, 'BEFORE',
  file === 'MBG_index.html'
    ? 'the strip holds 2948px of pills in a 1064px window and the old code never scrolls it'
    : (file === 'StrategicUX_index.html'
        ? 'numbers live in a slide-out drawer: ' + (before.doc.querySelector('.drawer').classList.contains('is-open') ? 'open' : 'CLOSED while scrolling')
        : 'header shows only a "01 / 30" counter, no slide list'),
  file === 'MBG_index.html');
before.window.close();

const after = loadPage(file, cfg, { io: 'noop' });
const a = sweep(after, 'AFTER', null, true);
after.window.close();

// "max trail" is measured against the slide touching the sticky bar; the new
// rule deliberately reads a line a third of the way down, so +/-1 is expected.
console.log('\n  verdict: off-screen ' + b.offScreen + ' -> ' + a.offScreen +
            ', backwards ' + b.backwards + ' -> ' + a.backwards +
            ', never-active ' + b.unreachable + ' -> ' + a.unreachable +
            ', max trail ' + b.maxTrail + ' -> ' + a.maxTrail);
const good = a.offScreen === 0 && a.backwards === 0 && a.unreachable === 0 && a.maxTrail <= 1;
console.log('  ' + (good ? 'PASS' : 'FAIL'));
process.exit(good ? 0 : 1);
