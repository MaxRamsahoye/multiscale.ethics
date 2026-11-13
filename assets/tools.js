// Find bar (Ctrl/Cmd+F and s) and a custom right-click menu (copy, copy link
// to highlight). Shared by the article, Lexicon and Pages.
//
// The find bar is on where the script tag has data-search-scope:
//   data-search-scope    what to search (selector)
//   data-search-exclude  parts of it to leave out (selector, optional)
//   data-hide-until      at the very top the bar sits top centre; once the
//                        page is scrolled it is hidden until this element
//                        (the Overview, the Lexicon's top band) has scrolled
//                        away, then it sits top left
(function () {
  var script = document.currentScript;
  var root = document.documentElement;

  /* ---------- styles ---------- */

  var css = [
    '.find-bar { position: fixed; z-index: 60; top: 22px; left: 50%; transform: translate(-50%, -8px);',
    '  display: flex; align-items: center; gap: 10px; width: 340px; max-width: calc(100vw - 32px); box-sizing: border-box;',
    '  padding: 8px 10px 8px 14px; background: var(--canvas-bg); color: var(--canvas-ink);',
    '  border: 1px solid var(--canvas-ink); border-radius: 999px; font-family: Inter, sans-serif; font-size: 15px;',
    '  opacity: 0; visibility: hidden; transition: opacity 0.25s ease, transform 0.25s ease, left 0.45s ease, visibility 0s 0.25s; }',
    '.find-bar.open { opacity: 1; visibility: visible; transform: translate(-50%, 0); transition: opacity 0.25s ease, transform 0.45s ease, left 0.45s ease; }',
    '.find-bar.at-left { left: 40px; transform: translate(0, -8px); }',
    '.find-bar.open.at-left { transform: translate(0, 0); }',
    '.find-bar.suppressed { opacity: 0; visibility: hidden; pointer-events: none; }',
    '.find-bar svg { flex: none; width: 15px; height: 15px; }',
    '.find-bar input { flex: 1; min-width: 0; border: none; outline: none; background: none; color: inherit; font: inherit; padding: 0; }',
    '.find-bar input::placeholder { color: var(--muted, #8c8c8c); }',
    '.find-count { flex: none; color: var(--muted, #8c8c8c); font-size: 13px; font-variant-numeric: tabular-nums; }',
    '.find-bar button { flex: none; display: flex; padding: 2px; border: none; background: none; color: inherit; }',
    '.find-bar button:hover { color: var(--muted, #8c8c8c); }',
    '::highlight(find-match) { background-color: rgba(255, 214, 0, 0.35); }',
    '::highlight(find-current) { background-color: rgba(255, 150, 0, 0.75); color: #000; }',
    '@media (max-width: 960px) { .find-bar.at-left { left: 24px; } }',
    '@media (max-width: 600px) { .find-bar, .find-bar.at-left { left: 16px; width: calc(100vw - 32px); transform: translate(0, -8px); }',
    '  .find-bar.open, .find-bar.open.at-left { transform: translate(0, 0); } }',
    '.context-menu { position: fixed; z-index: 70; min-width: 190px; padding: 6px 0; margin: 0; list-style: none;',
    '  background: var(--canvas-bg); color: var(--canvas-ink); border: 1px solid var(--canvas-ink);',
    '  font-family: Inter, sans-serif; font-size: 14px; opacity: 0; transform: scale(0.97); transform-origin: top left;',
    '  transition: opacity 0.12s ease, transform 0.12s ease; }',
    '.context-menu.open { opacity: 1; transform: none; }',
    '.context-menu button { display: block; width: 100%; padding: 7px 16px; border: none; background: none;',
    '  color: inherit; font: inherit; text-align: left; white-space: nowrap; }',
    '.context-menu button:hover:not(:disabled) { background: var(--canvas-ink); color: var(--canvas-bg); }',
    '.context-menu button:disabled { color: var(--muted, #8c8c8c); }',
    '.copy-toast { position: fixed; z-index: 70; padding: 5px 12px; background: var(--canvas-ink); color: var(--canvas-bg);',
    '  font-family: Inter, sans-serif; font-size: 13px; border-radius: 999px; pointer-events: none;',
    '  transform: translate(-50%, -100%); opacity: 0; transition: opacity 0.2s ease; }',
    '.copy-toast.show { opacity: 1; }',
    // the top menu: the site's pages across the top centre (hidden for now)
    '.top-nav { position: absolute; z-index: 30; top: 36px; left: 50%; transform: translateX(-50%);',
    '  display: flex; gap: 36px; margin: 0; padding: 0; list-style: none;',
    '  font-family: Inter, sans-serif; font-size: 15px; letter-spacing: -0.005em; white-space: nowrap; }',
    '.top-nav[hidden] { display: none; }',
    '.top-nav a { color: var(--muted, #8c8c8c); text-decoration: none; padding-bottom: 4px;',
    '  border-bottom: 1.5px solid transparent; transition: color 0.2s ease, border-color 0.2s ease; }',
    '.top-nav a:hover { color: var(--canvas-ink); }',
    '.top-nav a[aria-current="page"] { color: var(--canvas-ink); border-bottom-color: currentColor; }',
    '@media (max-width: 899px) { .top-nav { display: none; } }'
  ].join('\n');
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- top menu ---------- */

  (function () {
    var base = new URL('../', script.src);
    var pages = [['Article', '']];
    var nav = document.createElement('nav');
    nav.className = 'top-nav';
    nav.setAttribute('aria-label', 'Pages');
    // hidden: remove this line to show the menu again
    nav.hidden = true;
    pages.forEach(function (pg) {
      var a = document.createElement('a');
      var url = new URL(pg[1], base);
      a.href = url.pathname;
      a.textContent = pg[0];
      if (url.pathname === location.pathname) a.setAttribute('aria-current', 'page');
      nav.appendChild(a);
    });
    document.body.insertBefore(nav, document.body.firstChild);
  })();

  function typing() {
    var el = document.activeElement;
    var tag = el && el.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || (el && el.isContentEditable);
  }

  /* ---------- refresh: fade out, reload, fade in ---------- */

  // F5 and Ctrl/Cmd+R fade the page out before reloading (the browser's own
  // reload button can't be delayed, but still fades back in)
  document.addEventListener('keydown', function (e) {
    var reloadKey = e.key === 'F5' || ((e.key === 'r' || e.key === 'R') && (e.ctrlKey || e.metaKey) && !e.altKey);
    if (!reloadKey || document.body.classList.contains('page-leaving')) return;
    e.preventDefault();
    document.body.classList.add('page-leaving', 'reloading');
    setTimeout(function () { location.reload(); }, 210);
  });

  /* ---------- find bar ---------- */

  var scopeSel = script.getAttribute('data-search-scope');
  if (scopeSel) initFind();

  function initFind() {
    var excludeSel = script.getAttribute('data-search-exclude');
    var hideUntil = document.querySelector(script.getAttribute('data-hide-until') || 'none');
    var hasHighlights = window.CSS && CSS.highlights && window.Highlight;

    var bar = document.createElement('div');
    bar.className = 'find-bar';
    bar.setAttribute('role', 'search');
    bar.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.5" y1="15.5" x2="21" y2="21"/></svg>' +
      '<input type="text" placeholder="Search" aria-label="Search the page" spellcheck="false" autocomplete="off">' +
      '<span class="find-count" aria-live="polite"></span>' +
      '<button type="button" class="find-prev" aria-label="Previous match"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="6,15 12,9 18,15"/></svg></button>' +
      '<button type="button" class="find-next" aria-label="Next match"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polyline points="6,9 12,15 18,9"/></svg></button>' +
      '<button type="button" class="find-close" aria-label="Close search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg></button>';
    document.body.appendChild(bar);

    var input = bar.querySelector('input');
    var count = bar.querySelector('.find-count');
    var matches = [];
    var current = -1;
    var timer = null;
    var refocus = false;  // hidden while typing: take the cursor back on return
    var revealedAt = 0;   // a jump to a match can pass through the skip zone

    // which screen we are on: 'first', 'skip' (no bar) or 'main'
    function zone() {
      if (window.scrollY <= 10) return 'first';
      if (hideUntil && hideUntil.getBoundingClientRect().bottom > 80) return 'skip';
      return 'main';
    }

    function place() {
      var z = zone();
      bar.classList.toggle('at-left', z !== 'first');
      // while a search has matches the bar stays, wherever they lead
      var hide = z === 'skip' && !matches.length && Date.now() - revealedAt > 1500;
      var was = bar.classList.contains('suppressed');
      if (hide && !was && bar.contains(document.activeElement)) { input.blur(); refocus = true; }
      bar.classList.toggle('suppressed', hide);
      if (!hide && was && refocus) { refocus = false; input.focus({ preventScroll: true }); }
    }

    function textNodes() {
      var nodes = [];
      document.querySelectorAll(scopeSel).forEach(function (scope) {
        var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
          acceptNode: function (n) {
            var p = n.parentElement;
            if (!p || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
            if (p.closest('script, style, svg, button')) return NodeFilter.FILTER_REJECT;
            if (excludeSel && p.closest(excludeSel)) return NodeFilter.FILTER_REJECT;
            if (!p.getClientRects().length) return NodeFilter.FILTER_REJECT;
            return NodeFilter.FILTER_ACCEPT;
          }
        });
        while (walker.nextNode()) nodes.push(walker.currentNode);
      });
      return nodes;
    }

    function search() {
      var q = input.value.trim().toLowerCase();
      matches = [];
      current = -1;
      if (q) {
        textNodes().forEach(function (n) {
          var text = n.nodeValue.toLowerCase();
          var i = text.indexOf(q);
          while (i !== -1) {
            var r = document.createRange();
            r.setStart(n, i);
            r.setEnd(n, i + q.length);
            matches.push(r);
            i = text.indexOf(q, i + q.length);
          }
        });
      }
      // start from the first match on or below the top of the window
      if (matches.length) {
        current = 0;
        for (var k = 0; k < matches.length; k++) {
          if (matches[k].getBoundingClientRect().top >= 0) { current = k; break; }
        }
      }
      paint();
      if (current !== -1) reveal();
    }

    function paint() {
      if (hasHighlights) {
        CSS.highlights.set('find-match', new Highlight());
        CSS.highlights.set('find-current', new Highlight());
        matches.forEach(function (r, k) {
          CSS.highlights.get(k === current ? 'find-current' : 'find-match').add(r);
        });
      }
      count.textContent = !input.value.trim() ? '' : matches.length ? (current + 1) + ' of ' + matches.length : 'None';
    }

    function reveal() {
      var rect = matches[current].getBoundingClientRect();
      if (rect.top < 90 || rect.bottom > window.innerHeight - 60) {
        revealedAt = Date.now();
        window.scrollTo({ top: rect.top + window.scrollY - window.innerHeight * 0.35, behavior: 'smooth' });
      }
    }

    function step(dir) {
      if (!matches.length) return;
      current = (current + dir + matches.length) % matches.length;
      paint();
      reveal();
    }

    function open() {
      var sel = String(window.getSelection() || '').trim();
      if (sel && sel.length < 80 && sel.indexOf('\n') === -1) input.value = sel;
      place();
      bar.classList.add('open');
      input.focus();
      input.select();
      if (input.value) search();
    }

    function close() {
      bar.classList.remove('open');
      refocus = false;
      input.blur();
      if (hasHighlights) {
        CSS.highlights.delete('find-match');
        CSS.highlights.delete('find-current');
      }
      matches = [];
    }

    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(search, 120);
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (timer && matches.length === 0) { clearTimeout(timer); search(); }
        else step(e.shiftKey ? -1 : 1);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        close();
      }
      e.stopPropagation();
    });

    bar.querySelector('.find-prev').addEventListener('click', function () { step(-1); });
    bar.querySelector('.find-next').addEventListener('click', function () { step(1); });
    bar.querySelector('.find-close').addEventListener('click', close);

    document.addEventListener('keydown', function (e) {
      var findKey = (e.key === 'f' || e.key === 'F') && (e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey;
      var sKey = (e.key === 's' || e.key === 'S') && !e.ctrlKey && !e.metaKey && !e.altKey && !typing();
      if (!findKey && !sKey) {
        if (e.key === 'Escape' && bar.classList.contains('open')) close();
        return;
      }
      if (zone() === 'skip') return;   // the browser's own find still works here
      e.preventDefault();
      open();
    });

    window.addEventListener('scroll', function () {
      if (bar.classList.contains('open')) place();
    }, { passive: true });
    window.addEventListener('resize', function () {
      if (bar.classList.contains('open')) place();
    });
  }

  /* ---------- right-click menu ---------- */

  var menu = document.createElement('div');
  menu.className = 'context-menu';
  menu.setAttribute('role', 'menu');
  menu.innerHTML =
    '<button type="button" role="menuitem" data-act="copy">Copy</button>' +
    '<button type="button" role="menuitem" data-act="highlight">Copy link to highlight</button>' +
    '<button type="button" role="menuitem" data-act="address">Copy link address</button>';
  var copyBtn = menu.querySelector('[data-act="copy"]');
  var highlightBtn = menu.querySelector('[data-act="highlight"]');
  var addressBtn = menu.querySelector('[data-act="address"]');
  var menuState = null;
  var toast = null;

  // a link to this page that scrolls to and highlights the selected text
  function highlightLink(text) {
    var words = text.replace(/\s+/g, ' ').trim().split(' ');
    var enc = function (s) {
      return encodeURIComponent(s).replace(/-/g, '%2D').replace(/,/g, '%2C').replace(/&/g, '%26');
    };
    var frag = words.length > 10
      ? enc(words.slice(0, 5).join(' ')) + ',' + enc(words.slice(-5).join(' '))
      : enc(words.join(' '));
    return location.origin + location.pathname + location.search + '#:~:text=' + frag;
  }

  function writeClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(fallback);
    }
    fallback();
    return Promise.resolve();
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      ta.remove();
    }
  }

  function showToast(x, y, label) {
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'copy-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = label;
    toast.style.left = x + 'px';
    toast.style.top = (y - 8) + 'px';
    toast.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(function () { toast.classList.remove('show'); }, 1100);
  }

  function closeMenu() {
    if (!menuState) return;
    menu.classList.remove('open');
    menu.remove();
    menuState = null;
  }

  document.addEventListener('contextmenu', function (e) {
    // inside text boxes, and with Shift held, the browser's own menu
    if (e.shiftKey || e.target.closest('input, textarea, [contenteditable]')) return;
    e.preventDefault();
    var sel = String(window.getSelection() || '');
    var link = e.target.closest('a[href]');
    menuState = { text: sel.trim() ? sel : '', link: link ? link.href : '', x: e.clientX, y: e.clientY };
    copyBtn.disabled = !menuState.text;
    highlightBtn.disabled = !menuState.text;
    addressBtn.style.display = link ? '' : 'none';
    document.body.appendChild(menu);
    var w = menu.offsetWidth;
    var h = menu.offsetHeight;
    menu.style.left = Math.min(e.clientX, window.innerWidth - w - 8) + 'px';
    menu.style.top = Math.min(e.clientY, window.innerHeight - h - 8) + 'px';
    requestAnimationFrame(function () { menu.classList.add('open'); });
  });

  // keep the selection when the menu is pressed
  menu.addEventListener('mousedown', function (e) { e.preventDefault(); });

  menu.addEventListener('click', function (e) {
    var btn = e.target.closest('button');
    if (!btn || btn.disabled || !menuState) return;
    var act = btn.getAttribute('data-act');
    var s = menuState;
    var text = act === 'copy' ? s.text : act === 'highlight' ? highlightLink(s.text) : s.link;
    writeClipboard(text).then(function () {
      showToast(s.x, s.y, act === 'copy' ? 'Copied' : 'Link copied');
    });
    closeMenu();
  });

  document.addEventListener('mousedown', function (e) {
    if (menuState && !menu.contains(e.target)) closeMenu();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });
  window.addEventListener('scroll', closeMenu, { passive: true });
  window.addEventListener('resize', closeMenu);
  window.addEventListener('blur', closeMenu);
})();

// the screensaver: after twenty seconds with no movement, touch, key or
// scroll, three double pyramids (octahedra, drawn with flat shading)
// drift across a blank screen, each turning about two axes as it goes;
// they turn back from each edge and glance off each other, darkening to
// deep green and easing back to bright green; a click adds another (three times
// at most), and any other movement, key or scroll ends it. Not for those
// who prefer less motion. (On every page of the site.)
// Deactivated: set SCREENSAVER to true to turn it back on.
var SCREENSAVER = false;
(function () {
  if (!SCREENSAVER) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var css = [
    '.ce-saver { position: fixed; inset: 0; z-index: 1000; overflow: hidden; background: var(--canvas-bg, #fff);',
    '  opacity: 0; visibility: hidden; pointer-events: none; transition: opacity 0.8s ease, visibility 0s linear 0.8s; }',
    '.ce-saver.on { opacity: 1; visibility: visible; pointer-events: auto; cursor: none; transition: opacity 0.8s ease; }',
    '.ce-saver svg { position: absolute; top: 0; left: 0; width: 72px; height: auto; overflow: visible; will-change: transform; }',
    '.ce-saver polygon { stroke-linejoin: round; stroke-width: 0.6; }',
    '@media (max-width: 600px) { .ce-saver svg { width: 52px; } }'
  ].join('\n');
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);
  var box = document.createElement('div');
  box.className = 'ce-saver';
  box.setAttribute('aria-hidden', 'true');
  box.innerHTML = new Array(4).join('<svg viewBox="-60 -60 120 120"></svg>');
  document.body.appendChild(box);
  var NS = 'http://www.w3.org/2000/svg';
  // a regular octahedron: six corners, eight faces
  var V = [[0, -54, 0], [0, 54, 0], [54, 0, 0], [-54, 0, 0], [0, 0, 54], [0, 0, -54]];
  var F = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]];
  var DEEP = [20, 111, 68], BRIGHT = [24, 170, 107];
  var LIGHT = (function (l) { var n = Math.hypot(l[0], l[1], l[2]); return l.map(function (c) { return c / n; }); })([-0.5, -0.7, 0.9]);
  var SPEED = 150;
  function draw(o, flush) {
    var cy = Math.cos(o.ay), sy = Math.sin(o.ay), cx = Math.cos(o.ax), sx = Math.sin(o.ax);
    // turned about the upright axis, then about the crosswise one
    var P = V.map(function (v) {
      var x = v[0] * cy + v[2] * sy, z = -v[0] * sy + v[2] * cy, y = v[1];
      return [x, y * cx - z * sx, y * sx + z * cx];
    });
    var base = BRIGHT.map(function (c, k) { return c + (DEEP[k] - c) * flush; });
    F.map(function (f) {
      var a = P[f[0]], b = P[f[1]], c = P[f[2]];
      var u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], w = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
      var n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
      var len = Math.hypot(n[0], n[1], n[2]) || 1;
      n = n.map(function (q) { return q / len; });
      if (n[2] < 0) n = n.map(function (q) { return -q; });
      var lit = 0.32 + 0.8 * Math.max(0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2]);
      return { z: (a[2] + b[2] + c[2]) / 3, pts: [a, b, c], lit: lit };
    }).sort(function (p, q) { return p.z - q.z; }).forEach(function (f, i) {
      var col = 'rgb(' + base.map(function (c) { return Math.round(Math.min(255, c * f.lit * 1.15)); }).join(',') + ')';
      var p = o.polys[i];
      p.setAttribute('points', f.pts.map(function (q) { return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' '));
      p.setAttribute('fill', col);
      p.setAttribute('stroke', col);
    });
  }
  // each starts in its own part of the screen, heading its own way,
  // turning at its own pace
  var START = [[0.15, 0.62, 0.6, 0.35, 0.7, 0.45], [0.55, 0.12, 2.4, 0.9, -0.5, 0.6], [0.85, 0.72, 4.1, 2.0, 0.55, -0.4]];
  var W = window.innerWidth, H = window.innerHeight;
  function make(svg, x, y, heading, spin) {
    var d = svg.clientWidth;
    var o = {
      svg: svg, d: d, r: d / 2 * 0.92, x: x, y: y,
      vx: SPEED * Math.cos(heading), vy: SPEED * Math.sin(heading),
      ay: spin[0], ax: 0.4, sy: spin[1], sx: spin[2], hit: -1e9,
      polys: F.map(function () { var p = document.createElementNS(NS, 'polygon'); svg.appendChild(p); return p; })
    };
    svg.style.transform = 'translate(' + o.x + 'px,' + o.y + 'px)';
    draw(o, 0);
    return o;
  }
  var shapes = Array.prototype.map.call(box.querySelectorAll('svg'), function (svg, k) {
    var s = START[k], d = svg.clientWidth;
    return make(svg, (W - d) * s[0], (H - d) * s[1], s[2], [s[3], s[4], s[5]]);
  });
  var last = 0, frame = 0, onScreen = false, boost = 1, added = 0;
  // a click on the screensaver adds another where it lands, and quickens
  // them all by a fifth of their first pace - three times at most
  box.addEventListener('click', function (e) {
    if (added >= 3) return;
    var bx = box.getBoundingClientRect();
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '-60 -60 120 120');
    box.appendChild(svg);
    var d = svg.clientWidth;
    added += 1;
    boost = 1 + 0.2 * added;
    var o = make(svg,
      Math.max(0, Math.min(box.clientWidth - d, e.clientX - bx.left - d / 2)),
      Math.max(0, Math.min(box.clientHeight - d, e.clientY - bx.top - d / 2)),
      Math.random() * Math.PI * 2,
      [Math.random() * 6, (Math.random() < 0.5 ? -1 : 1) * (0.4 + Math.random() * 0.4), (Math.random() < 0.5 ? -1 : 1) * (0.3 + Math.random() * 0.4)]);
    o.hit = performance.now();
    shapes.push(o);
    shapes.forEach(function (q) { var v = Math.hypot(q.vx, q.vy) || 1; q.vx *= SPEED * boost / v; q.vy *= SPEED * boost / v; });
  });
  function step(t) {
    frame = 0;
    if (!onScreen) { last = 0; return; }
    var dt = last ? Math.min(0.05, (t - last) / 1000) : 0;
    last = t;
    var W = box.clientWidth, H = box.clientHeight;
    shapes.forEach(function (o) {
      o.x += o.vx * dt; o.y += o.vy * dt;
      var mw = W - o.d, mh = H - o.d;
      if (o.x <= 0) { o.x = 0; o.vx = Math.abs(o.vx); o.hit = t; } else if (o.x >= mw) { o.x = mw; o.vx = -Math.abs(o.vx); o.hit = t; }
      if (o.y <= 0) { o.y = 0; o.vy = Math.abs(o.vy); o.hit = t; } else if (o.y >= mh) { o.y = mh; o.vy = -Math.abs(o.vy); o.hit = t; }
      o.ay += o.sy * dt; o.ax += o.sx * dt;
    });
    // glancing off each other: as two equal balls would, exchanging
    // their motion along the line between their centres, then keeping
    // to their steady pace
    for (var i = 0; i < shapes.length; i++) {
      for (var j = i + 1; j < shapes.length; j++) {
        var a = shapes[i], b = shapes[j];
        var dx = (b.x + b.d / 2) - (a.x + a.d / 2), dy = (b.y + b.d / 2) - (a.y + a.d / 2);
        var dist = Math.hypot(dx, dy), min = a.r + b.r;
        if (!dist || dist >= min) continue;
        var nx = dx / dist, ny = dy / dist;
        var push = (min - dist) / 2;
        a.x -= nx * push; a.y -= ny * push; b.x += nx * push; b.y += ny * push;
        var rel = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny;
        if (rel > 0) {
          a.vx -= rel * nx; a.vy -= rel * ny; b.vx += rel * nx; b.vy += rel * ny;
          [a, b].forEach(function (o) { var v = Math.hypot(o.vx, o.vy) || 1; o.vx *= SPEED * boost / v; o.vy *= SPEED * boost / v; });
        }
        a.hit = b.hit = t;
      }
    }
    shapes.forEach(function (o) {
      // deep green at the moment it turns back, easing back to bright green
      // over two and a half seconds
      var since = (t - o.hit) / 2500;
      draw(o, since >= 1 ? 0 : 1 - since * since);
      o.svg.style.transform = 'translate(' + o.x + 'px,' + o.y + 'px)';
    });
    frame = requestAnimationFrame(step);
  }
  // showing and ending it
  var START_SHAPES = shapes.slice();
  function show() {
    if (onScreen) return;
    // afresh each time: the first three, at their first pace
    shapes.slice(START_SHAPES.length).forEach(function (o) { o.svg.remove(); });
    shapes = START_SHAPES.slice();
    added = 0; boost = 1;
    shapes.forEach(function (q) { var v = Math.hypot(q.vx, q.vy) || 1; q.vx *= SPEED / v; q.vy *= SPEED / v; });
    onScreen = true; last = 0;
    box.classList.add('on');
    if (!frame) frame = requestAnimationFrame(step);
  }
  function hide() {
    if (!onScreen) return;
    onScreen = false;
    box.classList.remove('on');
  }
  var IDLE = 20000, timer = 0, from = null;
  function wake() { hide(); clearTimeout(timer); timer = setTimeout(show, IDLE); }
  // (on the screensaver, the pointer may drift a little, as it does in a
  // click, without ending it)
  document.addEventListener('mousemove', function (e) {
    if (onScreen) {
      if (!from) { from = [e.clientX, e.clientY]; return; }
      if (Math.hypot(e.clientX - from[0], e.clientY - from[1]) < 40) return;
    }
    from = null;
    wake();
  }, { passive: true });
  ['keydown', 'wheel', 'scroll', 'touchmove'].forEach(function (ev) {
    window.addEventListener(ev, wake, { passive: true });
  });
  document.addEventListener('mousedown', function (e) { if (!box.contains(e.target)) wake(); });
  document.addEventListener('touchstart', function (e) { if (!box.contains(e.target)) wake(); }, { passive: true });
  timer = setTimeout(show, IDLE);
})();

// The footer's Contact: as the mail button at the top of the article, it
// copies the email address, and says so for a moment
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.footer-contact');
    if (!a) return;
    var email = a.getAttribute('data-email');
    if (!email || !navigator.clipboard || !navigator.clipboard.writeText) return;
    e.preventDefault();
    var label = a.getAttribute('data-label') || a.textContent;
    a.setAttribute('data-label', label);
    navigator.clipboard.writeText(email).then(function () {
      a.textContent = 'Email copied';
    }, function () {
      a.textContent = email;
    });
    clearTimeout(a.contactTimer);
    a.contactTimer = setTimeout(function () { a.textContent = label; }, 1800);
  });
})();
