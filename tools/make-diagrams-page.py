# Writes the Diagrams section of the site:
#   diagrams/index.html          the meta-page: a preview card for each figure,
#                                in two groups, Diagrams and Tables
#   diagrams/<slug>/index.html   each figure on a page of its own, with a line
#                                about it and a link to where it sits in the article
# The article's own figures, the footer and each page's head (fonts, colours,
# theme) are taken from index.html, so the pages stay in step with the article;
# the rest are drawn in tools/diagram_figures.py.
# Run from the repository root, after any change to the figures:
#   python3 -B tools/make-diagrams-page.py
import os, re, html

import diagram_figures

H = open('index.html').read()
# (the shared script, at the version the article loads: the find bar and the top menu)
TOOLS_V = re.search(r'assets/tools\.js\?v=([0-9a-f]+)', H).group(1)
SITE = 'https://maxramsahoye.github.io/multiscale.ethics/'


def head_for(depth, title, path, desc):
    """index.html's head, for a page `depth` folders down."""
    up = '../' * depth
    h = H[:H.index('</head>')]
    h = h.replace("url('fonts/", "url('" + up + "fonts/").replace('href="favicon/', 'href="' + up + 'favicon/').replace("'favicon/", "'" + up + "favicon/")
    h = h.replace('<title>Multi-Scale Ethics</title>', '<title>' + title + ' — Multi-Scale Ethics</title>')
    h = re.sub(r'\n  <link rel="canonical"[^>]*>', '', h)
    h = h.replace('content="' + SITE + '"', 'content="' + SITE + path + '"')
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + html.escape(desc, quote=True), h)
    return h


def block(start, end_tag):
    """The element in index.html that begins with `start`, through its closing tag."""
    i = H.index(start)
    j = H.index(end_tag, i) + len(end_tag)
    return H[i:j]


D = diagram_figures.figures()

# in each group, in the order they come in the article
FIGURES = [
    {
        'kind': 'diagram', 'slug': 'hybrid-ethics-stack', 'title': 'The Hybrid Ethics Stack',
        'where': 'Part I', 'anchor': 'ethics-stack',
        'desc': 'The concentric rings lifted apart into a stack: consequentialism the broadest layer, deontology within it and virtue at the core, each at the scale it was adapted to.',
        'html': D['stack'],
    },
    {
        'kind': 'diagram', 'slug': 'agency-across-scales', 'title': 'Agency across Scales',
        'where': 'Part II', 'anchor': 'figure-scales',
        'desc': 'The individual, the collective and the civilisational: each larger scale decomposes into the one below it, and emerges from it again.',
        'html': block('<figure class="article-figure" id="figure-scales">', '</figure>'),
    },
    {
        'kind': 'diagram', 'slug': 'concentric-ethics', 'title': 'Concentric Ethics',
        'where': 'Part III', 'anchor': 'figure-rings',
        'desc': 'Virtue ethics within deontology within consequentialism: the three theories as one nested system, each grown around the last.',
        'html': block('<figure class="article-figure" id="figure-rings">', '</figure>'),
    },
    {
        'kind': 'table', 'slug': 'three-theories', 'title': 'The Three Theories',
        'where': 'Ethical Theories', 'anchor': 'ethical-theories',
        'desc': 'Consequentialism, deontology and virtue ethics: the core idea of each, and the tradition it comes from.',
        'html': block('<figure class="article-figure figure-table">', '</figure>'),
    },
    {
        'kind': 'table', 'slug': 'scale-profiles', 'title': 'Scale Profiles',
        'where': 'Part I', 'anchor': 'human-societies',
        'desc': 'For each scale of society: how many people, how they come to trust one another, the ethic that suits it, and where that ethic strains.',
        'html': D['profiles'],
    },
    {
        'kind': 'table', 'slug': 'wrong-scales', 'title': 'Theories at the Wrong Scales',
        'where': 'Part II', 'anchor': 'wrong-scales',
        'desc': 'Each theory against each scale: native where it was adapted, and unfit elsewhere &ndash; alienating, rigid, unpredictable, vague, complicated or negligible.',
        'html': D['fit'],
    },
]
GROUPS = [('diagram', 'Diagrams'), ('table', 'Tables')]


def footer_for(depth):
    up = '../' * depth
    f = block('<footer class="site-footer">', '</footer>')
    return f.replace('href="./"', 'href="' + up + '"').replace('href="pdf/"', 'href="' + up + 'pdf/"').replace('href="diagrams/"', 'href="' + up + 'diagrams/"')


def indent(text, n):
    return '\n'.join((' ' * n + l.lstrip()) if l.strip() else l for l in text.split('\n'))


STYLE = '''
  <style>
    body { padding-top: 0; }

    .back-arrow {
      position: absolute; z-index: 10; top: 33px; left: 40px;
      display: flex; color: var(--canvas-ink);
    }
    .back-arrow:hover { color: var(--muted); }
    .back-arrow svg { width: 20px; height: 15px; }

    .site-title {
      position: fixed; z-index: 10; top: 24px; right: 40px; left: auto;
      margin: 0; text-align: right;
    }

    .dg-top { padding: 150px 0 24px; }

    .dg-kicker {
      margin: 0 0 12px;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 13px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .dg-kicker a { color: inherit; text-decoration: none; }
    .dg-kicker a:hover { color: var(--canvas-ink); }

    .dg-title {
      margin: 0 0 18px;
      font-family: 'Inter', sans-serif;
      font-weight: 700;
      letter-spacing: -0.02em;
      font-size: 52px;
      line-height: 1.08;
    }

    .dg-desc {
      margin: 0;
      font-family: var(--serif);
      font-size: 24px;
      line-height: 1.4;
    }

    .dg-meta {
      margin: 16px 0 0;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      color: var(--muted);
    }

    .dg-meta a { color: inherit; }

    /* ---- the meta-page: a group heading, then a grid of cards, three
       across: wider than the text column where there is room, centred on it ---- */
    .dg-wide {
      --dg-w: min(1060px, 100vw - 120px);
      width: var(--dg-w);
      margin-left: calc((100% - var(--dg-w)) / 2);
    }

    @media (max-width: 1180px) {
      .dg-wide { width: auto; margin-left: 0; }
    }

    .dg-wide .dg-card-desc { font-size: 17px; }

    .dg-group { margin: 72px 0 0; }

    .dg-group-title {
      margin: 0 0 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--rule);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .dg-cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 40px 28px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .dg-card a {
      display: block;
      color: inherit;
      text-decoration: none;
    }

    /* the figure itself, drawn small: the article's own width, scaled down to
       the card (by the script below), centred in it */
    .dg-thumb {
      position: relative;
      aspect-ratio: 4 / 3;
      overflow: hidden;
      border-radius: 6px;
      background: color-mix(in srgb, var(--inverse-bg) 7%, var(--canvas-bg));
      transition: background-color 0.25s ease;
    }

    .dg-card a:hover .dg-thumb {
      background: color-mix(in srgb, var(--inverse-bg) 16%, var(--canvas-bg));
    }

    .dg-thumb-inner {
      position: absolute;
      top: 0;
      left: 0;
      width: 760px;
      transform-origin: top left;
      pointer-events: none;
    }

    .dg-thumb .article-figure,
    .dg-thumb #figure-scales,
    .dg-thumb #figure-rings {
      margin: 0 !important;
    }

    .dg-thumb figcaption { display: none; }

    /* (in a card a drawing is always whole: none of the phone layout's
       sideways scrolling) */
    .dg-thumb .dg-figure { max-width: none !important; overflow: visible !important; }
    .dg-thumb .dg-figure .dg-svg { min-width: 0 !important; }

    .dg-card-title {
      display: block;
      margin: 16px 0 6px;
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      font-size: 19px;
      letter-spacing: -0.01em;
    }

    .dg-card a:hover .dg-card-title {
      text-decoration: underline;
      text-decoration-thickness: 1.5px;
      text-underline-offset: 4px;
    }

    .dg-card-desc {
      display: block;
      font-family: var(--serif);
      font-size: 18px;
      line-height: 1.4;
      color: color-mix(in srgb, var(--canvas-ink) 78%, var(--canvas-bg));
    }

    /* ---- a figure's own page ---- */
    .article-body .dg-single .article-figure,
    .article-body .dg-single #figure-scales,
    .article-body .dg-single #figure-rings {
      margin: 56px 0 0;
    }

    .dg-pager {
      display: flex;
      justify-content: space-between;
      gap: 24px;
      margin: 96px 0 0;
      padding-top: 20px;
      border-top: 1px solid var(--rule);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 15px;
    }

    .dg-pager a {
      color: var(--muted);
      text-decoration: none;
    }

    .dg-pager a:hover { color: var(--canvas-ink); }
    .dg-pager .next { margin-left: auto; text-align: right; }
    .dg-pager span { display: block; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }

    @media (max-width: 960px) {
      .back-arrow { top: 28px; left: 24px; }
      .site-title { position: absolute; top: 22px; right: 24px; }
      .dg-top { padding-top: 110px; }
      .dg-title { font-size: 38px; }
      .dg-desc { font-size: 20px; }
    }

    @media (max-width: 640px) {
      .dg-cards { grid-template-columns: minmax(0, 1fr); }
    }

    @media (min-width: 641px) and (max-width: 900px) {
      .dg-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
''' + diagram_figures.CSS + '''  </style>
'''

BACK = '''  <a class="back-arrow" href="{href}" aria-label="{label}">
    <svg viewBox="0 0 26 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="butt" stroke-linejoin="miter">
      <path d="M10,1.5 L5,6 L18,6 A4,4 0 0 1 18,14 L1,14"/>
      <path d="M10,10.5 L5,6"/>
    </svg>
  </a>
  <a class="site-title" href="{home}">Multi-<br>Scale<br>Ethics</a>
  <button class="scroll-top-btn" type="button" aria-label="Scroll to top">
    <svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1" stroke-linejoin="round">
      <polygon points="14,9.078 20.328,18.922 14,15.969 7.672,18.922"/>
    </svg>
  </button>
'''

UP_SCRIPT = '''  <script>
    // the up arrow, once the first screen has scrolled by
    (function () {
      var up = document.querySelector('.scroll-top-btn');
      function show() { up.classList.toggle('visible', window.scrollY > window.innerHeight * 0.6); }
      window.addEventListener('scroll', show, { passive: true });
      show();
      up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    })();
  </script>
'''

THUMB_SCRIPT = '''  <script>
    // each card's figure scaled from the article's width down to the card:
    // a diagram whole and centred, a table to the card's width from its top
    (function () {
      var thumbs = Array.prototype.slice.call(document.querySelectorAll('.dg-thumb'));
      function fit() {
        thumbs.forEach(function (t) {
          var inner = t.firstElementChild, ih = inner.offsetHeight;
          var s = t.clientWidth / 760, top;
          if (t.dataset.kind === 'diagram') {
            s = Math.min(s * 0.9, t.clientHeight * 0.86 / ih);
            top = (t.clientHeight - ih * s) / 2;
          } else {
            s = s * 0.9;
            top = Math.max(t.clientWidth * 0.05, (t.clientHeight - ih * s) / 2);
          }
          var left = (t.clientWidth - 760 * s) / 2;
          inner.style.transform = 'translate(' + left + 'px,' + top + 'px) scale(' + s + ')';
        });
      }
      fit();
      window.addEventListener('resize', fit);
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    })();
  </script>
'''


def page(depth, title, path, desc, back_href, back_label, content, scripts, footer=True):
    up = '../' * depth
    return (head_for(depth, title, path, desc) + STYLE + '</head>\n<body>\n'
            + BACK.format(href=back_href, label=back_label, home=up)
            + '''
  <div class="page">
    <div class="layout-grid">
      <main class="main-area">
        <article>
''' + content + '''        </article>
      </main>
    </div>

    ''' + (footer_for(depth) if footer else '') + '''
  </div>

''' + scripts + '  <script src="' + up + 'assets/tools.js?v=' + TOOLS_V + '"></script>\n' + UP_SCRIPT + '</body>\n</html>\n')


# ---- the meta-page ------------------------------------------------------------
def card(f):
    # (in a card, the figure keeps no ids of its own: the page it leads to has them)
    thumb = re.sub(r' (id|aria-labelledby)="[^"]*"', '', f['html'])
    thumb = re.sub(r'<title>[^<]*</title>', '', re.sub(r'<title id[^>]*>[^<]*</title>', '', thumb))
    return '''              <li class="dg-card">
                <a href="{slug}/">
                  <div class="dg-thumb" data-kind="{kind}" aria-hidden="true"><div class="dg-thumb-inner article-body">
{thumb}
                  </div></div>
                  <span class="dg-card-title">{title}</span>
                  <span class="dg-card-desc">{desc}</span>
                </a>
              </li>'''.format(thumb=indent(thumb, 20), **f)


groups = ''
for kind, name in GROUPS:
    groups += '''          <section class="dg-group" aria-labelledby="group-{kind}" id="group-{kind}">
            <h2 class="dg-group-title">{name}</h2>
            <ul class="dg-cards">
{cards}
            </ul>
          </section>
'''.format(kind=kind, name=name, cards='\n'.join(card(f) for f in FIGURES if f['kind'] == kind))

meta = '''          <div class="dg-wide">
          <div class="dg-top">
            <h1 class="dg-title">Diagrams</h1>
            <p class="dg-desc">The diagrams and tables of <em>Multi-Scale Ethics</em>, gathered in one place.</p>
          </div>
''' + groups + '          </div>\n'

os.makedirs('diagrams', exist_ok=True)
open('diagrams/index.html', 'w').write(page(
    1, 'Diagrams', 'diagrams/', 'The diagrams and tables of Multi-Scale Ethics, gathered in one place.',
    '../', 'Back to the article', meta, '', footer=False))
# (the cards' figures drawn still, as they first appear: no animation script on the meta-page)
s = open('diagrams/index.html').read()
s = s.replace('  <script src="../assets/tools.js', THUMB_SCRIPT + '  <script src="../assets/tools.js', 1)
open('diagrams/index.html', 'w').write(s)

# ---- each figure's own page ----------------------------------------------------------
for i, f in enumerate(FIGURES):
    prev_f = FIGURES[i - 1] if i > 0 else None
    next_f = FIGURES[i + 1] if i + 1 < len(FIGURES) else None
    pager = '          <nav class="dg-pager" aria-label="More diagrams and tables">\n'
    if prev_f:
        pager += '            <a class="prev" href="../{slug}/"><span>Previous</span>{title}</a>\n'.format(**prev_f)
    if next_f:
        pager += '            <a class="next" href="../{slug}/"><span>Next</span>{title}</a>\n'.format(**next_f)
    pager += '          </nav>\n'
    content = '''          <div class="dg-top">
            <p class="dg-kicker"><a href="../#group-{kind}">{group}</a></p>
            <h1 class="dg-title">{title}</h1>
            <p class="dg-desc">{desc}</p>
            <p class="dg-meta">In the article: <a href="../../#{anchor}">{where}</a></p>
          </div>
          <div class="article-body dg-single">
{figure}
          </div>
'''.format(group=dict(GROUPS)[f['kind']], figure=indent(f['html'], 12), **f) + pager
    os.makedirs('diagrams/' + f['slug'], exist_ok=True)
    open('diagrams/%s/index.html' % f['slug'], 'w').write(page(
        2, f['title'], 'diagrams/%s/' % f['slug'], html.unescape(f['desc']),
        '../', 'Back to all diagrams', content,
        '  <script src="../../assets/figures.js?v=2"></script>\n', footer=False))

print('Wrote diagrams/index.html and %d figure pages' % len(FIGURES))
