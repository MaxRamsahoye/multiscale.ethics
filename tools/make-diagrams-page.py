# Writes diagrams/index.html: the article's diagrams and tables gathered on one
# page, each with a link back to where it sits in the article. The figures,
# the footer and the page's head (fonts, colours, theme) are taken from
# index.html, so the page stays in step with the article.
# Run from the repository root, after any change to the article's figures:
#   python3 tools/make-diagrams-page.py
import os, re

H = open('index.html').read()
# (the shared script, at the version the article loads: the find bar and the top menu)
TOOLS_V = re.search(r'assets/tools\.js\?v=([0-9a-f]+)', H).group(1)

# ---- the head, one folder down ----------------------------------------------
head = H[:H.index('</head>')]
head = head.replace("url('fonts/", "url('../fonts/").replace('href="favicon/', 'href="../favicon/').replace("'favicon/", "'../favicon/")
head = head.replace('<title>Multi-Scale Ethics</title>', '<title>Diagrams — Multi-Scale Ethics</title>')
head = re.sub(r'\n  <link rel="canonical"[^>]*>', '', head)
head = head.replace('content="https://maxramsahoye.github.io/multiscale.ethics/"', 'content="https://maxramsahoye.github.io/multiscale.ethics/diagrams/"')


def block(start, end_tag):
    """The element that begins with `start`, through its closing tag."""
    i = H.index(start)
    j = H.index(end_tag, i) + len(end_tag)
    return H[i:j]


# the page's own figures, drawn in tools/diagram_figures.py
import diagram_figures
D = diagram_figures.figures()

FIGURES = [
    {
        'id': 'three-theories',
        'title': 'The Three Theories',
        'where': 'Ethical Theories',
        'anchor': 'ethical-theories',
        'desc': 'Consequentialism, deontology and virtue ethics: the core idea of each, and the tradition it comes from.',
        'html': block('<figure class="article-figure figure-table">', '</figure>'),
    },
    {
        'id': 'scale-profiles',
        'title': 'Scale Profiles',
        'where': 'Part I',
        'anchor': 'human-societies',
        'desc': 'For each scale of society: how many people, how they come to trust one another, the ethic that suits it, and where that ethic strains.',
        'html': D['profiles'],
    },
    {
        'id': 'hybrid-ethics-stack',
        'title': 'The Hybrid Ethics Stack',
        'where': 'Part I',
        'anchor': 'ethics-stack',
        'desc': 'The concentric rings lifted apart into a stack: consequentialism the broadest layer, deontology within it and virtue at the core, each at the scale it was adapted to.',
        'html': D['stack'],
    },
    {
        'id': 'agency-across-scales',
        'title': 'Agency across Scales',
        'where': 'Part II',
        'anchor': 'figure-scales',
        'desc': 'The individual, the collective and the civilisational: each larger scale decomposes into the one below it, and emerges from it again.',
        'html': block('<figure class="article-figure" id="figure-scales">', '</figure>'),
    },
    {
        'id': 'theory-scale-fit',
        'title': 'Theories at the Wrong Scales',
        'where': 'Part II',
        'anchor': 'wrong-scales',
        'desc': 'Each theory against each scale: native where it was adapted, and alienating, vague or complicated where it was not.',
        'html': D['fit'],
    },
    {
        'id': 'concentric-ethics',
        'title': 'Concentric Ethics',
        'where': 'Part III',
        'anchor': 'figure-rings',
        'desc': 'Virtue ethics within deontology within consequentialism: the three theories as one nested system, each grown around the last.',
        'html': block('<figure class="article-figure" id="figure-rings">', '</figure>'),
    },
]

footer = block('<footer class="site-footer">', '</footer>')
# (the footer's links, one folder down)
footer = footer.replace('href="./"', 'href="../"').replace('href="pdf/"', 'href="../pdf/"').replace('href="diagrams/"', 'href="./"')

style = '''
  <style>
    /* the Diagrams page: a title and a line about it, then each diagram in
       turn, with where it sits in the article */
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

    .dg-top {
      padding: 150px 0 40px;
    }

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

    /* the list of diagrams, linking down the page */
    .dg-index {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 28px;
      margin: 28px 0 0;
      padding: 0;
      list-style: none;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 15px;
    }

    .dg-index a {
      color: var(--muted);
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }

    .dg-index a:hover {
      color: var(--canvas-ink);
      border-bottom-color: currentColor;
    }

    .article-body .dg-item {
      margin: 0;
      padding: 72px 0 24px;
      border-top: 1px solid var(--rule);
      scroll-margin-top: 24px;
    }

    .article-body .dg-item + .dg-item {
      margin-top: 72px;
    }

    .article-body .dg-item > h2 {
      margin-bottom: 8px;
    }

    .dg-meta {
      margin: 0 0 6px !important;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      color: var(--muted);
    }

    .dg-meta a {
      color: inherit !important;
      font-weight: 400 !important;
    }

    .article-body .dg-item .article-figure,
    .article-body .dg-item #figure-scales,
    .article-body .dg-item #figure-rings {
      margin: 56px 0 0;
    }

    @media (max-width: 960px) {
      .back-arrow { top: 28px; left: 24px; }
      .site-title { position: absolute; top: 22px; right: 24px; }
      .dg-top { padding-top: 110px; }
      .dg-title { font-size: 38px; }
      .dg-desc { font-size: 20px; }
    }
''' + diagram_figures.CSS + '''  </style>
'''

items = '\n'.join(
    '''            <section class="dg-item" id="{id}">
              <h2><a class="heading-link" href="#{id}">{title}</a></h2>
              <p class="dg-meta">In the article: <a href="../#{anchor}">{where}</a></p>
              <p>{desc}</p>

{figure}
            </section>
'''.format(figure='\n'.join('              ' + l.lstrip() if l.strip() else l for l in f['html'].split('\n')).replace('              <figure', '              <figure', 1), **f)
    for f in FIGURES)

index = '\n'.join('                <li><a href="#{id}">{title}</a></li>'.format(**f) for f in FIGURES)

body = '''<body>
  <a class="back-arrow" href="../" aria-label="Back to the article">
    <svg viewBox="0 0 26 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="butt" stroke-linejoin="miter">
      <path d="M10,1.5 L5,6 L18,6 A4,4 0 0 1 18,14 L1,14"/>
      <path d="M10,10.5 L5,6"/>
    </svg>
  </a>
  <a class="site-title" href="../">Multi-<br>Scale<br>Ethics</a>
  <button class="scroll-top-btn" type="button" aria-label="Scroll to top">
    <svg viewBox="0 0 28 28" fill="none" stroke="currentColor" stroke-width="1" stroke-linejoin="round">
      <polygon points="14,9.078 20.328,18.922 14,15.969 7.672,18.922"/>
    </svg>
  </button>

  <div class="page">
    <div class="layout-grid">
      <main class="main-area">
        <article>
          <div class="dg-top">
            <h1 class="dg-title">Diagrams</h1>
            <p class="dg-desc">The diagrams and tables of <em>Multi-Scale Ethics</em>, gathered in one place.</p>
            <ol class="dg-index">
''' + index + '''
            </ol>
          </div>
          <div class="article-body">
''' + items + '''          </div>
        </article>
      </main>
    </div>

    ''' + footer + '''
  </div>

  <script src="../assets/figures.js?v=2"></script>
  <script src="../assets/tools.js?v=''' + TOOLS_V + '''"></script>
  <script>
    // the up arrow, once the first screen has scrolled by
    (function () {
      var up = document.querySelector('.scroll-top-btn');
      function show() { up.classList.toggle('visible', window.scrollY > window.innerHeight * 0.6); }
      window.addEventListener('scroll', show, { passive: true });
      show();
      up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    })();
  </script>
</body>
</html>
'''

os.makedirs('diagrams', exist_ok=True)
open('diagrams/index.html', 'w').write(head + style + '</head>\n' + body)
print('Wrote diagrams/index.html')
