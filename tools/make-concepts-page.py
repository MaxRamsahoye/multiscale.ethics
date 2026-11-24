# Writes concepts/index.html: the article's key terms, defined, in two views:
# curated (grouped, the main terms with those that belong under them) and
# A to Z. The page's head (fonts, colours, theme) is taken from index.html.
# Run from the repository root, after editing the terms below:
#   python3 -B tools/make-concepts-page.py
import os, re, html

H = open('index.html').read()
TOOLS_V = re.search(r'assets/tools\.js\?v=([0-9a-f]+)', H).group(1)
SITE = 'https://maxramsahoye.github.io/multiscale.ethics/'
DESC = 'Key terms used in Multi-Scale Ethics: The Cultural Evolution of Major Ethical Theories.'

# ---- the terms ------------------------------------------------------------------
# (name, definition); the definitions draw on the article
TERMS = {
    'Multi-Scale Ethics': 'The paradigm the article proposes: rethinking ethics for the grand dimensions of global civilisation, by asking how normative theories interact <em>across scales</em> &ndash; from the individual, through the collective, to civilisation as a whole.',
    'Hybrid Ethics Stack': 'The article&rsquo;s synthesis: the ethics of civilisation as layered theories, each operating at its own scale, together producing a higher-order ethical synergy that none could achieve alone.',
    'Classes of Agent': 'The individual, the collective and the civilisational: kinds of agent, each with its own characteristic ethics, whose meeting points give rise to many of our hardest moral conflicts.',
    'Complicated and Complex': 'A complicated system has many parts but can, with enough effort, be fully specified; a complex system is adaptive, non-linear and emergent, changing in response to the very rules applied to it.',
    'Normative Ethics': 'The branch of moral philosophy concerned with how we ought to act. Its three major theories are consequentialism, deontology and virtue ethics.',
    'Consequentialism': 'The theory that an action is right if it produces the best overall consequences. In the article, the ethics of the state: system-wide optimisation of aggregate welfare.',
    'Utilitarianism': 'The best-known form of consequentialism, associated with Jeremy Bentham and John Stuart Mill: act so as to bring about the greatest happiness or well-being of the greatest number.',
    'Deontology': 'The theory that an action is right if it conforms to a moral duty or rule, regardless of its consequences. In the article, the ethics of the city: shared rules that let strangers trust one another.',
    'Categorical Imperative': 'Kant&rsquo;s principle of duty: act only on rules you could will to be universal laws, and treat people always as ends in themselves, never merely as means.',
    'Virtue Ethics': 'The theory, rooted in Aristotle, that morality is a matter of cultivating good character rather than following rules or calculating outcomes. In the article, the ethics of the tribe, where character can be known first-hand.',
    'Alienation': 'The objection, pressed by Bernard Williams and Peter Railton, that impartial calculation estranges a person from their own relationships and commitments &ndash; consequentialism applied at the scale of the individual.',
    'Dunbar&rsquo;s Number': 'The cognitive limit of roughly 150 people with whom one person can maintain stable relationships; in the article, the threshold beyond which virtue alone can no longer regulate a society.',
    'Leviathan': 'Hobbes&rsquo;s image of the sovereign state; in the article, the moral outlook of governing at the scale of the state.',
    'Seeing Like a State': 'James C. Scott&rsquo;s phrase for the simplifying, aggregate view that states take of the societies they govern.',
    'Multipolar Trap': 'A situation in which many actors, each acting rationally or dutifully by its own lights, together produce an outcome that none of them would choose &ndash; what Scott Alexander called &lsquo;Moloch&rsquo;.',
    'Cultural Evolution': 'Change in a population&rsquo;s beliefs, norms and practices over time through variation, transmission and selection, much as in biological evolution.',
    'Memetic Adaptation': 'An idea &ndash; here a normative one &ndash; that spreads and persists because it confers an advantage in a particular environment. The article reads each ethical theory as a memetic adaptation to a scale of society.',
    'Multilevel Selection': 'The view that selection acts at several levels at once &ndash; on individuals within groups, and on groups themselves &ndash; summed up by David Sloan Wilson and E. O. Wilson: &lsquo;Selfishness beats altruism within groups. Altruistic groups beat selfish groups.&rsquo;',
    'Convergent Cultural Evolution': 'The tendency, as civilisation integrates, for different cultures and their ethics to arrive at shared values; in the article, the route by which an aligned Singleton could emerge.',
    'Autopoiesis': 'The self-production and self-maintenance of a living or complex system &ndash; a body, a social body, a civilisation.',
    'Autopoethics': 'Anna Riedl&rsquo;s portmanteau of <em>autopoiesis</em> and <em>ethics</em>: ethics understood as part of how a complex system reproduces itself.',
    'Moral Convergence': 'The argument that, as societies grow, virtue and duty increasingly answer to outcomes, and that the best versions of the major theories converge &ndash; what Derek Parfit called &lsquo;climbing the same mountain on different sides&rsquo;.',
    'Singleton': 'Nick Bostrom&rsquo;s term for a world order with a single decision-making agency at the highest level. It need not be monolithic, and could be formed through convergent evolution rather than coercion.',
    'Metanormative Ethics': 'Ethics one level above the normative theories: not which theory is correct, but how the theories relate, where each applies and how they fit together. In the article, the move from choosing a theory to matching each theory to the scale it suits.',
    'Macrohistory': 'The study of history at its largest scales &ndash; the long-run patterns of societies and civilisations. In the article, the lens through which the moral philosopher descends from abstraction into the cultural evolution of civilisation.',
    'Scale-Sensitivity': 'The principle that how well an ethical theory works depends on the scale at which it is applied: each fits the scale it was adapted to, and strains at the others &ndash; alienating, vague or complicated.',
    'Ethical Adaptive System': 'Ethics seen as a complex adaptive system: the three theories as interacting parts that evolve with the societies they regulate &ndash; all deeply necessary, none sufficient alone.',
    'Meta-Ethics': 'The branch of moral philosophy that asks what morality itself is &ndash; what moral terms mean, whether moral claims can be true, and how they could be known &ndash; rather than how we ought to act.',
    'Holarchy': 'A hierarchy of holons &ndash; wholes that are at once parts of larger wholes. In the article, the nested, plural and adaptive structure of an aligned Singleton.',
}

# the curated view: each main term, with the terms that belong under it
# (a term, or a term with the terms nested under it, as deep as need be)
CURATED = [
    ('Multi-Scale Ethics', ['Scale-Sensitivity', 'Ethical Adaptive System', 'Hybrid Ethics Stack', 'Classes of Agent', 'Complicated and Complex']),
    ('Metanormative Ethics', [
        ('Normative Ethics', ['Consequentialism', 'Utilitarianism', 'Deontology', 'Categorical Imperative', 'Virtue Ethics', 'Alienation']),
        'Meta-Ethics',
    ]),
    ('Cultural Evolution', ['Macrohistory', 'Memetic Adaptation', 'Multilevel Selection', 'Dunbar&rsquo;s Number', 'Convergent Cultural Evolution']),
    ('Moral Convergence', ['Singleton', 'Holarchy', 'Autopoiesis', 'Autopoethics']),
    ('Multipolar Trap', ['Leviathan', 'Seeing Like a State']),
]


def walk(items, depth=0):
    """Each term in the curated view, with how deeply it is nested."""
    for item in items:
        if isinstance(item, tuple):
            yield item[0], depth
            yield from walk(item[1], depth + 1)
        else:
            yield item, depth


listed = [t for t, d in walk(CURATED)]
assert sorted(listed) == sorted(TERMS), set(TERMS) ^ set(listed)


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(name).lower().replace('’', '')).strip('-')


def plain(name):
    return html.unescape(name)


def term(name, prefix, depth=0):
    sid = prefix + slug(name)
    cls = ' term-sub term-depth-%d' % depth if depth else ''
    return ('        <div class="term%s" id="%s">\n          <dt><a href="#%s">%s</a></dt>\n          <dd>%s</dd>\n        </div>\n'
            % (cls, sid, sid, name, TERMS[name]))


curated = ''.join(term(t, 'curated-', d) for t, d in walk(CURATED))

az_names = sorted(TERMS, key=lambda n: plain(n).lower())
az, letter = '', None
for n in az_names:
    l = plain(n)[0].upper()
    if l != letter:
        if letter:
            az += '      </dl>\n'
        az += '      <h2 class="concept-letter" id="letter-%s">%s</h2>\n      <dl class="concepts-list">\n' % (l.lower(), l)
        letter = l
    az += term(n, '')
az += '      </dl>\n'

# the article's keywords (as listed under its Overview), first on the page
KEYWORDS = ['Metanormative Ethics', 'Macrohistory', 'Cultural Evolution', 'Scale-Sensitivity', 'Ethical Adaptive System']
assert all(k in TERMS for k in KEYWORDS)
keyword_links = '\n'.join('              <li><a href="#%s">%s</a></li>' % (slug(n), n) for n in KEYWORDS)

index_links = '\n'.join('        <li><a href="#%s">%s</a></li>' % (slug(n), n) for n in az_names)

# ---- the page -----------------------------------------------------------------------
head = H[:H.index('</head>')]
head = head.replace("url('fonts/", "url('../fonts/").replace('href="favicon/', 'href="../favicon/').replace("'favicon/", "'../favicon/")
head = head.replace('<title>Multi-Scale Ethics</title>', '<title>Concepts — Multi-Scale Ethics</title>')
head = re.sub(r'\n  <link rel="canonical"[^>]*>', '', head)
head = head.replace('content="' + SITE + '"', 'content="' + SITE + 'concepts/"')
head = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + html.escape(DESC, quote=True), head)

style = '''
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

    .cp-top { padding: 150px 0 8px; }

    .cp-title {
      margin: 0 0 18px;
      font-family: 'Inter', sans-serif;
      font-weight: 700;
      letter-spacing: -0.02em;
      font-size: 52px;
      line-height: 1.08;
    }

    .cp-intro {
      margin: 0;
      font-family: var(--serif);
      font-size: 24px;
      line-height: 1.4;
    }

    .cp-intro a { color: inherit; text-decoration: none; }
    .cp-intro a:hover { text-decoration: underline; text-underline-offset: 3px; }

    .cp-count {
      margin: 18px 0 0;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      color: var(--muted);
    }

    /* the article's keywords, then every term at a glance, each linking down the page */
    .cp-sub {
      margin: 36px 0 12px;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .cp-index.cp-keywords {
      margin-top: 0;
      gap: 10px 12px;
      font-size: 16px;
    }

    .cp-keywords a {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--inverse-bg) 22%, var(--canvas-bg));
      color: var(--canvas-ink) !important;
      transition: background-color 0.2s ease;
    }

    .cp-keywords a:hover {
      background: color-mix(in srgb, var(--inverse-bg) 45%, var(--canvas-bg));
    }

    .cp-index {
      margin: 0;
      padding: 0;
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 8px 22px;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
    }

    .cp-index a { color: var(--muted); text-decoration: none; }
    .cp-index a:hover { color: var(--canvas-ink); }

    /* the two views */
    .cp-tabs {
      display: flex;
      gap: 28px;
      margin: 48px 0 0;
      border-bottom: 1px solid var(--rule);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 13px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .cp-tabs button {
      padding: 0 0 12px;
      margin-bottom: -1px;
      border: 0;
      border-bottom: 1.5px solid transparent;
      background: none;
      font: inherit;
      letter-spacing: inherit;
      text-transform: inherit;
      color: var(--muted);
      cursor: pointer;
    }

    .cp-tabs button:hover { color: var(--canvas-ink); }
    .cp-tabs button[aria-selected="true"] { color: var(--canvas-ink); border-bottom-color: currentColor; }

    .cp-view[hidden] { display: none; }

    /* the terms */
    .concepts-list { margin: 0; }

    .term {
      padding: 26px 0;
      border-bottom: 1px solid var(--rule);
      scroll-margin-top: 24px;
    }

    .term dt {
      margin: 0 0 8px;
      font-family: var(--serif);
      font-weight: 700;
      font-size: 1.15em;
      -webkit-text-stroke: 0.3px currentColor;
    }

    .term dt a { color: inherit; text-decoration: none; }
    .term dt a:hover { text-decoration: underline; text-underline-offset: 4px; text-decoration-thickness: 1px; }

    .term dd { margin: 0; }

    /* (in the curated view, the terms under a main term set in from it) */
    .term-sub { padding-left: 32px; }
    .term-depth-2 { padding-left: 64px; }
    .term-sub dt { font-weight: 400; font-style: italic; -webkit-text-stroke: 0.35px currentColor; }

    .term:target dd,
    .term:target dt { background: var(--note-highlight); }

    .concept-letter {
      margin: 48px 0 0;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--rule);
      font-family: 'Inter', sans-serif;
      font-size: 22px;
      font-weight: 600;
    }

    .cp-end { height: 140px; }

    @media (max-width: 960px) {
      .back-arrow { top: 28px; left: 24px; }
      .site-title { position: absolute; top: 22px; right: 24px; }
      .cp-top { padding-top: 110px; }
      .cp-title { font-size: 38px; }
      .cp-intro { font-size: 20px; }
      .term-sub { padding-left: 18px; }
      .term-depth-2 { padding-left: 36px; }
    }
  </style>
'''

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
          <div class="cp-top">
            <h1 class="cp-title">Concepts</h1>
            <p class="cp-intro">Key terms used in <a href="../"><em>Multi-Scale Ethics</em></a>.</p>
            <p class="cp-count">''' + str(len(TERMS)) + ''' concepts</p>
            <h2 class="cp-sub">Keywords</h2>
            <ul class="cp-index cp-keywords" aria-label="Keywords">
''' + keyword_links + '''
            </ul>
            <h2 class="cp-sub">All concepts</h2>
            <ul class="cp-index" aria-label="All concepts">
''' + index_links + '''
            </ul>
            <div class="cp-tabs" role="tablist" aria-label="Views">
              <button type="button" role="tab" aria-selected="true" data-view="curated">Curated</button>
              <button type="button" role="tab" aria-selected="false" data-view="az">A to Z</button>
            </div>
          </div>
          <div class="article-body">
            <section class="cp-view" data-view="curated" aria-label="Curated">
      <dl class="concepts-list">
''' + curated + '''      </dl>
            </section>
            <section class="cp-view" data-view="az" aria-label="A to Z" hidden>
''' + az + '''            </section>
          </div>
          <div class="cp-end"></div>
        </article>
      </main>
    </div>
  </div>

  <script>
    // the two views; the index's links lead into whichever is showing (and a
    // link from elsewhere to a term opens the view that holds it)
    (function () {
      var tabs = Array.prototype.slice.call(document.querySelectorAll('.cp-tabs button'));
      var views = Array.prototype.slice.call(document.querySelectorAll('.cp-view'));
      function show(name) {
        tabs.forEach(function (t) { t.setAttribute('aria-selected', t.dataset.view === name ? 'true' : 'false'); });
        views.forEach(function (v) { v.hidden = v.dataset.view !== name; });
        try { localStorage.setItem('mse.conceptsView', name); } catch (e) {}
      }
      tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.dataset.view); }); });
      var saved; try { saved = localStorage.getItem('mse.conceptsView'); } catch (e) {}
      if (saved === 'az') show('az');
      document.querySelectorAll('.cp-index a').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('href').slice(1);
          var curated = !document.querySelector('.cp-view[data-view="curated"]').hidden;
          var target = document.getElementById(curated ? 'curated-' + id : id);
          if (!target) return;
          e.preventDefault();
          history.replaceState(null, '', '#' + target.id);
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      });
      if (location.hash) {
        var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
        if (t) { show(t.id.indexOf('curated-') === 0 ? 'curated' : 'az'); t.scrollIntoView(); }
      }
      var up = document.querySelector('.scroll-top-btn');
      function showUp() { up.classList.toggle('visible', window.scrollY > window.innerHeight * 0.6); }
      window.addEventListener('scroll', showUp, { passive: true });
      showUp();
      up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    })();
  </script>
  <script src="../assets/tools.js?v=''' + TOOLS_V + '''" data-search-scope=".article-body"></script>
</body>
</html>
'''

os.makedirs('concepts', exist_ok=True)
open('concepts/index.html', 'w').write(head + style + '</head>\n' + body)
print('Wrote concepts/index.html (%d concepts)' % len(TERMS))
