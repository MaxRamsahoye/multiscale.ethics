// The article's two animated figures, drawn as SVG and played on a loop while
// they are on screen (still, at their most telling moment, for anyone who
// prefers reduced motion, and in the PDF).
//
//   Scales: the individual, collective and civilisational tiles; each larger
//   tile splits into a three-by-three grid of the scale below it, spreads
//   apart, then closes up again (decomposition and emergence).
//
//   Ethics rings: virtue ethics, then deontology around it, then
//   consequentialism around both, growing out and drawing back in.
//
// Coordinates are those of the original 1200-pixel-wide animations.
(function () {
  'use strict';

  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function ease(x) { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function easeOut(x) { x = clamp(x); return 1 - Math.pow(1 - x, 3); }
  // 0 before a, rising to 1 by b
  function ramp(t, a, b, fn) { return (fn || ease)((t - a) / (b - a)); }
  function hex(c) { return '#' + c.map(function (v) { return ('0' + Math.round(v).toString(16)).slice(-2); }).join(''); }
  function rgb(h) { return [1, 3, 5].map(function (i) { return parseInt(h.slice(i, i + 2), 16); }); }
  function mix(a, b, k) { a = rgb(a); b = rgb(b); return hex(a.map(function (v, i) { return v + (b[i] - v) * k; })); }
  function pts(list) { return list.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' '); }

  // ---- Scales -------------------------------------------------------------
  var SCALES_LOOP = 6150;
  var CX = 510, THICK = 10;
  var PALETTE = {
    ind: { top: '#fce278', left: '#eac859', right: '#c89a28' },
    col: { top: '#f5be28', left: '#d69e18', right: '#a5750e' },
    civ: { top: '#d6920a', left: '#b27406', right: '#855404' }
  };
  var TILES = [
    { key: 'ind', w: 32, cy: 134, label: 'Individual', lx: 632 },
    { key: 'col', w: 96, cy: 274, label: 'Collective', lx: 712, sub: 'ind', gap: 8 },
    { key: 'civ', w: 231, cy: 495.5, label: 'Civilisational', lx: 851, sub: 'col', gap: 10 }
  ];

  function tile(cx, cy, w, c, seam) {
    var h = w / 2, t = THICK;
    var s = '<polygon fill="' + c.left + '" points="' + pts([[cx - w, cy], [cx, cy + h], [cx, cy + h + t], [cx - w, cy + t]]) + '"/>' +
      '<polygon fill="' + c.right + '" points="' + pts([[cx, cy + h], [cx + w, cy], [cx + w, cy + t], [cx, cy + h + t]]) + '"/>' +
      '<polygon fill="' + c.top + '" points="' + pts([[cx, cy - h], [cx + w, cy], [cx, cy + h], [cx - w, cy]]) + '"';
    if (seam > 0) s += ' stroke="' + c.left + '" stroke-opacity="' + seam.toFixed(2) + '" stroke-width="1.2" stroke-linejoin="round"';
    return s + '/>';
  }

  // how far each of the two larger tiles has split (seams and colour) and spread
  function scalesState(t) {
    t = ((t % SCALES_LOOP) + SCALES_LOOP) % SCALES_LOOP;
    return {
      col: { split: ramp(t, 1100, 1460) * (1 - ramp(t, 5410, 5590)), spread: ramp(t, 1460, 1820) * (1 - ramp(t, 5230, 5410)) },
      civ: { split: ramp(t, 2530, 2890) * (1 - ramp(t, 5770, 5950)), spread: ramp(t, 2890, 3210) * (1 - ramp(t, 5590, 5770)) }
    };
  }

  function drawScales(t) {
    var st = scalesState(t), out = '';
    TILES.forEach(function (T) {
      var s = st[T.key];
      if (!s || s.split <= 0) {
        out += tile(CX, T.cy, T.w, PALETTE[T.key], 0);
      } else {
        var from = PALETTE[T.key], to = PALETTE[T.sub];
        var c = { top: mix(from.top, to.top, s.split), left: mix(from.left, to.left, s.split), right: mix(from.right, to.right, s.split) };
        var sw = T.w / 3, step = sw + T.gap * s.spread;
        var cells = [];
        for (var i = -1; i <= 1; i++) for (var j = -1; j <= 1; j++) cells.push([i, j]);
        // back to front, so the nearer tiles cover the sides of those behind
        cells.sort(function (a, b) { return (a[0] + a[1]) - (b[0] + b[1]); });
        cells.forEach(function (ij) {
          out += tile(CX + (ij[0] - ij[1]) * step, T.cy + (ij[0] + ij[1]) * step / 2, sw, c, s.split * (1 - s.spread));
        });
      }
      out += '<text class="fig-label" x="' + T.lx + '" y="' + (T.cy + 9) + '">' + T.label + '</text>';
    });
    return out;
  }

  // ---- Ethics rings -------------------------------------------------------
  // each ring a translucent gold, so that where they overlap they deepen (on
  // white they come out as the original's three shades)
  var RINGS_LOOP = 9960;
  var RCX = 600, RCY = 540;
  var RINGS = [
    // grows, label shows, deepens; then label goes, shrinks back
    { label: 'Virtue Ethics', ly: 0, r0: 0, r1: 122, grow: [500, 1060], text: [1180, 1500], deepen: [1600, 1990], unText: [8720, 9080], shrink: [9080, 9440], stroke: '#f2c64f', fill: '#fad76e', alpha: 0.30 },
    { label: 'Deontology', ly: -184, r0: 122, r1: 256, grow: [2110, 2590], text: [2350, 2950], deepen: [3000, 3520], unText: [7880, 8240], shrink: [8240, 8600], stroke: '#efc04a', fill: '#f7c85a', alpha: 0.30 },
    { label: 'Consequentialism', ly: -342, r0: 256, r1: 436, grow: [3640, 4120], text: [3880, 4480], deepen: [4300, 4800], unText: [6920, 7280], shrink: [7280, 7760], stroke: '#eab650', fill: '#eaa528', alpha: 0.232 }
  ];

  function drawRings(t) {
    t = ((t % RINGS_LOOP) + RINGS_LOOP) % RINGS_LOOP;
    var discs = '', labels = '';
    RINGS.forEach(function (R) {
      var g = ramp(t, R.grow[0], R.grow[1], easeOut) * (1 - ramp(t, R.shrink[0], R.shrink[1]));
      if (g <= 0) return;
      var r = R.r0 + (R.r1 - R.r0) * g;
      // a ring that has shrunk back in fades as it meets the one inside it
      var fade = R.r0 > 0 ? clamp((r - R.r0) / 12) : 1;
      var depth = 0.5 + 0.5 * ramp(t, R.deepen[0], R.deepen[1]);
      discs = '<circle class="ring-disc" cx="' + RCX + '" cy="' + RCY + '" r="' + r.toFixed(1) + '" fill="' + R.fill + '" fill-opacity="' + (R.alpha * depth * fade).toFixed(3) + '" stroke="' + R.stroke + '" stroke-opacity="' + (depth * fade).toFixed(2) + '"/>' + discs;
      var a = ramp(t, R.text[0], R.text[1]) * (1 - ramp(t, R.unText[0], R.unText[1]));
      if (a > 0) labels += '<text class="fig-label fig-label-ring" x="' + RCX + '" y="' + (RCY + R.ly + 9) + '" opacity="' + a.toFixed(2) + '">' + R.label + '</text>';
    });
    return discs + labels;
  }

  var FIGURES = {
    scales: { draw: drawScales, loop: SCALES_LOOP, still: 3600 },  // split and spread
    rings: { draw: drawRings, loop: RINGS_LOOP, still: 5500 }      // all three rings
  };

  if (typeof module !== 'undefined') { module.exports = FIGURES; return; }

  // ---- playing them -------------------------------------------------------
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var playing = [];
  var raf = null;

  function frame(now) {
    playing.forEach(function (p) {
      if (p.start == null) p.start = now - p.offset;
      p.stage.innerHTML = p.fig.draw(now - p.start);
    });
    raf = playing.length ? requestAnimationFrame(frame) : null;
  }

  document.querySelectorAll('svg[data-figure]').forEach(function (svg) {
    var fig = FIGURES[svg.getAttribute('data-figure')];
    var stage = svg.querySelector('.fig-stage');
    if (!fig || !stage || reduce || !window.IntersectionObserver) return;
    // each figure starts from the top of its loop the first time it is seen
    var entry = { fig: fig, stage: stage, start: null, offset: 0 };
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var i = playing.indexOf(entry);
        if (e.isIntersecting && i < 0) {
          // pick up where it was left off
          entry.start = null;
          playing.push(entry);
          if (!raf) raf = requestAnimationFrame(frame);
        } else if (!e.isIntersecting && i >= 0) {
          entry.offset = (performance.now() - entry.start) % fig.loop;
          playing.splice(i, 1);
        }
      });
    }, { threshold: 0.2 }).observe(svg);
  });
})();
