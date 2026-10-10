#!/usr/bin/env python3
"""Inject the shared slide rail into the three case-study pages."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
RAIL_JS = io.open(os.path.join(HERE, 'slide-rail.js'), encoding='utf-8').read()

MBG_CSS = """
/* ===== slide rail: keep the active pill scrolled into view ===== */
.toc .wrap{scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth;overscroll-behavior-x:contain}
.toc .wrap::-webkit-scrollbar{display:none}
.toc a{flex:none}
.toc a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.slide-sec{scroll-margin-top:calc(var(--nav-h) + 74px)}
@media print{.toc{display:none}}
"""

MED_CSS = """
  /* ================= SLIDE RAIL (scroll-driven slide strip) ================= */
  :root { --sld-rail-h:46px; }
  .sld-rail {
    position:sticky; top:var(--pnav-h); z-index:29; height:var(--sld-rail-h);
    display:flex; align-items:center;
    background:rgba(239,255,221,.93);
    backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
    border-bottom:1px solid var(--pn-line);
  }
  .sld-rail-in {
    display:flex; align-items:center; gap:6px; width:100%; height:100%;
    padding:0 clamp(14px, 3vw, 40px);
    overflow-x:auto; overflow-y:hidden;
    scrollbar-width:none; -ms-overflow-style:none;
    overscroll-behavior-x:contain; scroll-behavior:smooth;
  }
  .sld-rail-in::-webkit-scrollbar { display:none; }
  .sld-rail a {
    flex:none; display:inline-flex; align-items:center; gap:6px;
    padding:7px 13px; border:1px solid var(--pn-line); border-radius:999px;
    background:#fff; color:rgba(27,57,20,.62); text-decoration:none; white-space:nowrap;
    font:600 12px/1 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    transition:background .2s ease, color .2s ease, border-color .2s ease;
  }
  .sld-rail a b { font-weight:800; color:var(--pn-ink); }
  .sld-rail a:hover, .sld-rail a:focus-visible { color:var(--pn-ink); border-color:var(--pn-ink); }
  .sld-rail a.is-active, .sld-rail a.active { background:var(--pn-ink); border-color:var(--pn-ink); color:rgba(239,255,221,.85); }
  .sld-rail a.is-active b, .sld-rail a.active b { color:var(--pn-lime); }
  .sld-rail a:focus-visible { outline:2px solid var(--pn-green); outline-offset:2px; }
  .slide { scroll-margin-top:calc(var(--pnav-h) + var(--sld-rail-h) + 8px); }
  @media (max-width:1024px) {
    /* the rail shares the screen with the full-height deck viewer */
    .deck { height:calc(100vh - var(--pnav-h) - var(--sld-rail-h)); height:calc(100svh - var(--pnav-h) - var(--sld-rail-h)); }
    .slide { height:calc(100vh - var(--pnav-h) - var(--sld-rail-h)); height:calc(100svh - var(--pnav-h) - var(--sld-rail-h));
             contain-intrinsic-size:auto calc(100vh - var(--pnav-h) - var(--sld-rail-h)); scroll-margin-top:0; }
  }
  @media (max-width:760px) {
    .sld-rail-in { padding:0 12px; gap:5px; }
    .sld-rail a { padding:6px 10px; font-size:11.5px; }
  }
  @media print { .sld-rail { display:none; } }
"""

SUX_CSS = """
    /* ===== slide rail (scroll-driven slide strip) ===== */
    :root { --sld-rail-h: 46px; }
    .sld-rail {
      position: sticky; top: 75px; z-index: 13; height: var(--sld-rail-h);
      display: flex; align-items: center;
      background: rgba(244, 240, 233, .94);
      backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--line);
    }
    .sld-rail-in {
      display: flex; align-items: center; gap: 6px; width: 100%; height: 100%;
      padding: 0 clamp(12px, 3.5vw, 54px);
      overflow-x: auto; overflow-y: hidden;
      scrollbar-width: none; -ms-overflow-style: none;
      overscroll-behavior-x: contain; scroll-behavior: smooth;
    }
    .sld-rail-in::-webkit-scrollbar { display: none; }
    .sld-rail a {
      flex: none; display: inline-flex; align-items: center; gap: 6px;
      min-height: 0; padding: 7px 13px;
      border: 1px solid var(--line); border-radius: 999px;
      background: var(--paper-strong); color: var(--muted); text-decoration: none;
      font-size: .75rem; font-weight: 700; white-space: nowrap;
      transition: color .2s ease, background .2s ease, border-color .2s ease;
    }
    .sld-rail a b { font-weight: 800; color: var(--ink); }
    .sld-rail a:hover, .sld-rail a:focus-visible { color: var(--ink); border-color: var(--accent); }
    .sld-rail a.is-active, .sld-rail a.active { background: var(--accent); border-color: var(--accent); color: rgba(248, 246, 241, .9); }
    .sld-rail a.is-active b, .sld-rail a.active b { color: #fff; }
    .slide { scroll-margin-top: calc(72px + var(--sld-rail-h) + 14px); }
    @media (max-width: 680px) {
      .sld-rail { top: 65px; }
      .sld-rail-in { padding: 0 14px; gap: 5px; }
      .sld-rail a span { display: none; }
      .slide { scroll-margin-top: calc(62px + var(--sld-rail-h) + 12px); }
    }
    @media print { .sld-rail { display: none; } }
"""

# ---- old active-slide observers, replaced by the shared rail -------------
MBG_OLD = """const secs=[...document.querySelectorAll('.slide-sec')];const links=[...document.querySelectorAll('.toc a')];
const tio=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){const id=en.target.id;links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+id))}})},{threshold:.5});
secs.forEach(s=>tio.observe(s));"""
MBG_NEW = "/* active-slide tracking now lives in the shared slide rail script below */"

MED_OLD = """  // slide crossing the middle of the screen = current slide (works for page scroll and the mobile deck)
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) setCurrent(slides.indexOf(en.target)); });
  }, { rootMargin: '-50% 0px -50% 0px', threshold: 0 });
  slides.forEach((sl) => io.observe(sl));"""
MED_NEW = """  // the shared slide rail reports which slide is on screen
  // (works for the desktop page scroll and the mobile deck scroller alike)
  window.addEventListener('slide-rail:change', (e) => {
    if (slides[e.detail.index]) setCurrent(e.detail.index);
  });"""

SUX_OLD = """      const observer = new IntersectionObserver((entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setActive(visible.target);
      }, { rootMargin: '-20% 0px -55% 0px', threshold: [0, .25, .5, .75, 1] });
      slides.forEach((slide) => observer.observe(slide));"""
SUX_NEW = """      // the shared slide rail reports which slide is on screen
      window.addEventListener('slide-rail:change', (e) => {
        if (slides[e.detail.index]) setActive(slides[e.detail.index]);
      });"""

JOBS = [
    ('MBG_index.html',         MBG_CSS, MBG_OLD, MBG_NEW),
    ('MedicalAdher_index.html', MED_CSS, MED_OLD, MED_NEW),
    ('StrategicUX_index.html',  SUX_CSS, SUX_OLD, SUX_NEW),
]

for fname, css, old, new in JOBS:
    with io.open(os.path.join(ROOT, fname), encoding='utf-8') as fh:
        doc = fh.read()

    if 'slide-rail:change' in doc:
        print('%-26s SKIP (already injected)' % fname)
        continue

    # 1. swap the observer for the rail's event
    if doc.count(old) != 1:
        sys.exit('%s: expected exactly 1 occurrence of the old observer, found %d' % (fname, doc.count(old)))
    doc = doc.replace(old, new)

    # 2. CSS at the end of the existing stylesheet so it wins the cascade
    if doc.count('</style>') != 1:
        sys.exit('%s: expected exactly 1 </style>, found %d' % (fname, doc.count('</style>')))
    doc = doc.replace('</style>', css + '</style>')

    # 3. the rail script, last so every page's own listeners are wired first
    if doc.count('</body>') != 1:
        sys.exit('%s: expected exactly 1 </body>, found %d' % (fname, doc.count('</body>')))
    block = '<script>\n' + RAIL_JS + '\n</script>\n</body>'
    doc = doc.replace('</body>', block)

    with io.open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as fh:
        fh.write(doc)
    print('%-26s injected  (+%d bytes)' % (fname, len(doc) - (len(doc) - len(css) - len(RAIL_JS))))
