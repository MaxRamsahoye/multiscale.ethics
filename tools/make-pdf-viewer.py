# Writes pdf/index.html: the article's PDF read within the site - each page
# drawn with PDF.js (assets/pdfjs, Apache-2.0), with a bar for the page count,
# zoom and download, as on complexemergencemodel.systems. The page takes its
# head (fonts, colours, theme) from index.html.
# Run from the repository root, after tools/make-pdf.js:
#   python3 tools/make-pdf-viewer.py
import os, re
H = open('index.html').read()
head = H[:H.index('</head>')]
# one folder down: the fonts, icons and preview card one level up
head = head.replace("url('fonts/", "url('../fonts/").replace('href="favicon/', 'href="../favicon/').replace("'favicon/", "'../favicon/")
head = head.replace('<title>Multi-Scale Ethics</title>', '<title>PDF \u2014 Multi-Scale Ethics</title>')
head = re.sub(r'\n  <link rel="canonical"[^>]*>', '', head)
PDF = '../Multi-Scale%20Ethics.pdf'
style = '''
  <style>
    body { margin: 0; background: var(--canvas-bg); color: var(--canvas-ink); }

    /* back to the article at the top left; the site's name at the top right */
    .back-arrow {
      position: absolute; z-index: 10; top: 33px; left: 40px;
      display: flex; color: var(--canvas-ink);
    }
    .back-arrow:hover { color: var(--muted); }
    .back-arrow svg { width: 20px; height: 15px; }

    .site-title {
      position: absolute; z-index: 10; top: 24px; right: 40px; left: auto;
      margin: 0; text-align: right;
    }

    @media (max-width: 960px) {
      .back-arrow { top: 28px; left: 24px; }
      .site-title { top: 22px; right: 24px; }
    }

    /* the bar: the title, the page count, zoom, and the file itself */
    .pv-bar {
      position: relative;
      top: 0;
      z-index: 20;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
      width: min(100% - 48px, 900px);
      margin: 84px auto 0;
      padding: 16px 0;
      background: var(--canvas-bg);
      border-bottom: 1px solid color-mix(in srgb, currentColor 16%, transparent);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
    }

    /* (once scrolled past, the bar moves to the left of the pages, upright,
       out of their way; its place above them kept, so nothing jumps) */
    .pv-barwrap {
      min-height: var(--pv-bar-h, 77px);
    }

    @media (min-width: 901px) {
      body.pv-docked .pv-bar {
        position: fixed;
        top: 50%;
        left: 24px;
        width: auto;
        margin: 0;
        padding: 0;
        border: 0;
        background: none;
        flex-direction: column;
        align-items: flex-start;
        transform: translateY(-50%);
        animation: pv-dock 0.3s ease;
      }

      body.pv-docked .pv-title {
        display: none;
      }

      body.pv-docked .pv-tools {
        flex-direction: column;
        align-items: flex-start;
        gap: 14px;
      }

      body.pv-docked .pv-pct,
      body.pv-docked .pv-count {
        margin: 0;
        min-width: 0;
        text-align: left;
        padding-left: 4px;
      }

      body.pv-docked .pv-tools a span {
        display: none;
      }
    }

    @keyframes pv-dock {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    .pv-title {
      margin: 0;
      font-family: var(--serif);
      font-size: 20px;
      font-weight: 400;
      font-style: italic;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .pv-tools {
      display: flex;
      align-items: center;
      gap: 18px;
      flex: none;
      color: var(--muted);
    }

    .pv-tools button,
    .pv-tools a {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 4px;
      border: none;
      background: none;
      font: inherit;
      color: inherit;
      text-decoration: none;
      cursor: pointer;
      transition: color 0.2s ease;
    }

    .pv-tools button:hover,
    .pv-tools a:hover {
      color: var(--canvas-ink);
    }

    .pv-tools svg {
      width: 20px;
      height: 20px;
    }

    .pv-pct {
      min-width: 3.2em;
      text-align: center;
      font-variant-numeric: tabular-nums;
      margin: 0 -10px;
    }

    .pv-count {
      font-variant-numeric: tabular-nums;
      min-width: 4.5em;
      text-align: center;
    }

    /* the pages, one beneath another, on a faintly tinted ground */
    .pv-pages {
      display: flex;
      flex-direction: column;
      align-items: safe center;
      overflow-x: auto;
      gap: 28px;
      padding: 40px 24px 120px;
    }

    /* (at the zoom's own width, wider than the window if need be, scrolling
       sideways; on phones, the width of the screen) */
    .pv-page {
      position: relative;
      flex: none;
      width: var(--pv-w, 794px);
      aspect-ratio: 210 / 297;
      background: #fff;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 8px 28px rgba(0, 0, 0, 0.08);
    }

    .pv-page canvas {
      display: block;
      width: 100%;
      height: 100%;
    }

    .pv-note {
      margin: 80px auto;
      max-width: 560px;
      text-align: center;
      font-size: 20px;
      color: var(--muted);
    }

    .pv-note a {
      color: var(--link-blue);
    }

    @media (max-width: 600px) {
      .pv-bar { margin-top: 84px; width: calc(100% - 32px); }
    }

    @media (max-width: 900px) {
      .pv-bar { position: sticky; top: 0; }
      .pv-barwrap { min-height: 0; display: contents; }
      .pv-title { font-size: 17px; }
      .pv-zoom { display: none !important; }
      .pv-pages { padding: 24px 12px 80px; gap: 16px; }
      .pv-page { width: 100%; }
    }
  </style>
</head>
'''

body_top = '''<body>
  <a class="back-arrow" href="../" aria-label="Back to the article">
    <svg viewBox="0 0 26 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="butt" stroke-linejoin="miter">
      <path d="M10,1.5 L5,6 L18,6 A4,4 0 0 1 18,14 L1,14"/>
      <path d="M10,10.5 L5,6"/>
    </svg>
  </a>
  <a class="site-title" href="../">Multi-<br>Scale<br>Ethics</a>

  '''
I = lambda d: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>'
main = '''<main class="pv-main">
    <div class="pv-barwrap"><div class="pv-bar">
      <h1 class="pv-title">Multi-Scale Ethics: The Cultural Evolution of Major Ethical Theories</h1>
      <div class="pv-tools">
        <span class="pv-count" aria-live="polite">&ndash;</span>
        <button class="pv-zoom" type="button" data-zoom="-1" aria-label="Zoom out">''' + I('<circle cx="11" cy="11" r="6.5"/><path d="M8 11h6M16 16l4.5 4.5"/>') + '''</button>
        <span class="pv-zoom pv-pct" aria-live="polite">100%</span>
        <button class="pv-zoom" type="button" data-zoom="1" aria-label="Zoom in">''' + I('<circle cx="11" cy="11" r="6.5"/><path d="M8 11h6M11 8v6M16 16l4.5 4.5"/>') + '''</button>
        <a href="''' + PDF + '''" download="Multi-Scale Ethics.pdf" aria-label="Download the PDF">''' + I('<path d="M4 15v3.5A1.5 1.5 0 0 0 5.5 20h13a1.5 1.5 0 0 0 1.5-1.5V15"/><path d="M12 4v11"/><path d="M8 11l4 4 4-4"/>') + '''<span>Download</span></a>
      </div>
    </div></div>
    <div class="pv-pages" aria-label="The pages of the PDF"></div>
  </main>

  <script src="../assets/pdfjs/pdf.min.js"></script>
  <script>
    // each page drawn as it comes near the screen, at the screen's own
    // resolution, and drawn again when the zoom changes
    (function () {
      var URL_ = ''' + "'" + PDF + "'" + ''';
      var list = document.querySelector('.pv-pages'), count = document.querySelector('.pv-count');
      if (!window.pdfjsLib) { list.innerHTML = '<p class="pv-note">The viewer could not load. <a href="' + URL_ + '">Open the PDF directly.</a></p>'; return; }
      pdfjsLib.GlobalWorkerOptions.workerSrc = '../assets/pdfjs/pdf.worker.min.js';
      // (the browser's own PDF viewer's steps, as percentages of the page at
      // its actual size: A4, 794px wide)
      var ZOOMS = [25, 33, 50, 67, 75, 80, 90, 100, 110, 125, 150, 175, 200, 250, 300, 400, 500], z = 7, pdf, pages = [], drawn = new Map();
      // (the zoom as a percentage of the page at its actual size: A4, 794px wide)
      var pct = document.querySelector('.pv-pct');
      function setWidth() {
        document.documentElement.style.setProperty('--pv-w', Math.round(794 * ZOOMS[z] / 100) + 'px');
        pct.textContent = ZOOMS[z] + '%';
      }
      setWidth();
      function draw(i) {
        var box = pages[i]; if (!box || box._busy) return;
        var w = box.clientWidth; if (!w || drawn.get(i) === w) return;
        box._busy = true;
        pdf.getPage(i + 1).then(function (page) {
          var v1 = page.getViewport({ scale: 1 }), dpr = Math.min(window.devicePixelRatio || 1, 3);
          // (very large zooms drawn at no more than 6000px across, which
          // browsers can hold as a canvas)
          dpr = Math.min(dpr, 6000 / w);
          var vp = page.getViewport({ scale: w / v1.width * dpr });
          var c = document.createElement('canvas');
          c.width = Math.round(vp.width); c.height = Math.round(vp.height);
          return page.render({ canvasContext: c.getContext('2d'), viewport: vp }).promise.then(function () {
            box.replaceChildren(c); drawn.set(i, w);
          });
        }).finally(function () { box._busy = false; });
      }
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) draw(+e.target.dataset.i); });
      }, { rootMargin: '1200px 0px' });
      function visible() {
        var mid = window.innerHeight / 2, best = 0;
        pages.forEach(function (p, i) { var r = p.getBoundingClientRect(); if (r.top < mid) best = i; });
        count.textContent = (best + 1) + ' / ' + pages.length;
      }
      pdfjsLib.getDocument(URL_).promise.then(function (doc) {
        pdf = doc;
        return doc.getPage(1).then(function (p1) {
          var v = p1.getViewport({ scale: 1 });
          for (var i = 0; i < doc.numPages; i++) {
            var d = document.createElement('div');
            d.className = 'pv-page'; d.dataset.i = i;
            d.style.aspectRatio = v.width + ' / ' + v.height;
            d.setAttribute('aria-label', 'Page ' + (i + 1));
            list.appendChild(d); pages.push(d); io.observe(d);
          }
          visible();
        });
      }).catch(function () {
        list.innerHTML = '<p class="pv-note">The PDF could not be shown here. <a href="' + URL_ + '">Open it directly.</a></p>';
      });
      window.addEventListener('scroll', function () { if (pages.length) visible(); }, { passive: true });
      // the bar: at the top, then docked at the left once scrolled past
      var wrap = document.querySelector('.pv-barwrap'), bar = document.querySelector('.pv-bar');
      document.documentElement.style.setProperty('--pv-bar-h', bar.offsetHeight + 'px');
      function dock() { document.body.classList.toggle('pv-docked', wrap.getBoundingClientRect().top < 0); }
      window.addEventListener('scroll', dock, { passive: true });
      dock();
      var redraw = 0;
      function again() { clearTimeout(redraw); redraw = setTimeout(function () { pages.forEach(function (p, i) { var r = p.getBoundingClientRect(); if (r.bottom > -1200 && r.top < window.innerHeight + 1200) draw(i); }); }, 150); }
      window.addEventListener('resize', again);
      document.querySelectorAll('[data-zoom]').forEach(function (b) {
        b.addEventListener('click', function () {
          var at = pages.length ? (window.scrollY + window.innerHeight / 2) / document.documentElement.scrollHeight : 0;
          z = Math.max(0, Math.min(ZOOMS.length - 1, z + +b.dataset.zoom));
          setWidth();
          window.scrollTo(0, at * document.documentElement.scrollHeight - window.innerHeight / 2);
          // (sideways, kept centred on the page)
          list.scrollLeft = (list.scrollWidth - list.clientWidth) / 2;
          again();
        });
      });
    })();
  </script>

  '''
tail = '''
</body>
</html>
'''
os.makedirs('pdf', exist_ok=True)
open('pdf/index.html', 'w').write(head + style + body_top + main + tail)
print('Wrote pdf/index.html')
