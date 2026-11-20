# Writes sources/index.html: the works the article draws on, by category,
# with a bibliography at the top and, for each, how the article uses it.
# The page's head (fonts, colours, theme) is taken from index.html.
# Run from the repository root, after editing the sources below:
#   python3 -B tools/make-sources-page.py
import os, re, html

H = open('index.html').read()
TOOLS_V = re.search(r'assets/tools\.js\?v=([0-9a-f]+)', H).group(1)
SITE = 'https://maxramsahoye.github.io/multiscale.ethics/'
DESC = 'Works drawn on in Multi-Scale Ethics: The Cultural Evolution of Major Ethical Theories.'
WIKI = 'https://en.wikipedia.org/wiki/'

# ---- the sources -----------------------------------------------------------------
# id, author, title, kind ('book' set in italics; 'essay' in quotation marks,
# with `venue` in italics), venue, year, link, where in the article, note
CATEGORIES = [
    ('Scale and Society', [
        dict(id='west', author='Geoffrey West', title='Scale: The Universal Laws of Life, Growth, and Death in Organisms, Cities, and Companies', kind='book', year='2017',
             where=('Overview', 'overview'),
             note='West argues that complex systems &ndash; from cells to cities to civilisations &ndash; are governed by universal scaling laws. The article begins from his question and turns it from the biophysical to the ethical: how do ethics change <em>across scales</em>?'),
        dict(id='dunbar', author='Robin Dunbar', title='Neocortex size as a constraint on group size in primates', kind='essay', venue='Journal of Human Evolution', year='1992', link=WIKI + 'Dunbar%27s_number',
             where=('Virtue is the Ethics of the Tribe', 'virtue-tribe'),
             note='The source of Dunbar&rsquo;s number: roughly 150 people with whom one person can maintain stable relationships. In the article, the threshold at which virtue alone stops being enough to regulate a society.'),
        dict(id='hobbes', author='Thomas Hobbes', title='Leviathan', kind='book', year='1651', link=WIKI + 'Leviathan_(Hobbes_book)',
             where=('Consequentialism is the Ethics of the State', 'consequentialism-state'),
             note='Hobbes&rsquo;s image of the sovereign state. The article invokes &lsquo;the moral phenomenology of the Leviathan&rsquo; for the view from the scale of the state.'),
        dict(id='scott', author='James C. Scott', title='Seeing Like a State: How Certain Schemes to Improve the Human Condition Have Failed', kind='book', year='1998', link=WIKI + 'Seeing_Like_a_State',
             where=('Consequentialism is the Ethics of the State', 'consequentialism-state'),
             note='Scott&rsquo;s account of the simplifying, aggregate view of states. In the article, <em>seeing like a state</em> is what governing at scale requires: system-wide optimisation.'),
    ]),
    ('The Three Theories', [
        dict(id='aristotle', author='Aristotle', title='Nicomachean Ethics', kind='book', year='c. 340 BCE', link=WIKI + 'Nicomachean_Ethics',
             where=('Ethical Theories', 'ethical-theories'),
             note='The founding text of virtue ethics: morality as the cultivation of good character, asking not only &lsquo;What should I do?&rsquo; but &lsquo;What kind of person should I be?&rsquo;'),
        dict(id='kant', author='Immanuel Kant', title='Groundwork of the Metaphysics of Morals', kind='book', year='1785', link=WIKI + 'Groundwork_of_the_Metaphysics_of_Morals',
             where=('Ethical Theories', 'ethical-theories'),
             note='The classic statement of deontology and the Categorical Imperative: act only on rules you could will to be universal, and treat people as ends in themselves, never merely as means.'),
        dict(id='bentham', author='Jeremy Bentham', title='An Introduction to the Principles of Morals and Legislation', kind='book', year='1789', link=WIKI + 'An_Introduction_to_the_Principles_of_Morals_and_Legislation',
             where=('Ethical Theories', 'ethical-theories'),
             note='The founding work of utilitarianism and its principle of &lsquo;the greatest happiness of the greatest number&rsquo;, which the article quotes for the ethics of the state.'),
        dict(id='mill', author='John Stuart Mill', title='Utilitarianism', kind='book', year='1861', link=WIKI + 'Utilitarianism_(book)',
             where=('Ethical Theories', 'ethical-theories'),
             note='Mill&rsquo;s defence and refinement of Bentham&rsquo;s utilitarianism, cited with Bentham in the article&rsquo;s table of the three theories.'),
        dict(id='sidgwick', author='Henry Sidgwick', title='The Methods of Ethics', kind='book', year='1874', link=WIKI + 'The_Methods_of_Ethics',
             where=('Consequentialism is Alienating at the Individual Scale', 'consequentialism-individual'),
             note='Sidgwick&rsquo;s systematic utilitarianism, and the source of &lsquo;the point of view of the universe&rsquo;: the impartial standpoint the article finds estranging at the scale of a single life.'),
    ]),
    ('Wrong Scales and Agent Classes', [
        dict(id='williams', author='Bernard Williams', title='Persons, Character and Morality', kind='essay', venue='Moral Luck', year='1981',
             where=('Consequentialism is Alienating at the Individual Scale', 'consequentialism-individual'),
             note='The source of &lsquo;one thought too many&rsquo;: the person who saves their drowning spouse only after checking that impartial morality permits it. The article&rsquo;s first example of a theory applied at the wrong scale.'),
        dict(id='railton', author='Peter Railton', title='Alienation, Consequentialism, and the Demands of Morality', kind='essay', venue='Philosophy &amp; Public Affairs', year='1984',
             where=('Consequentialism is Alienating at the Individual Scale', 'consequentialism-individual'),
             note='Railton names the problem of <em>alienation</em>: a consequentialist agent estranged from their own attachments and commitments.'),
        dict(id='arendt', author='Hannah Arendt', title='Eichmann in Jerusalem: A Report on the Banality of Evil', kind='book', year='1963', link=WIKI + 'Eichmann_in_Jerusalem',
             where=('Individual <> Collective', 'individual-collective'),
             note='Arendt&rsquo;s account of the functionary who was &lsquo;just following orders&rsquo;: the extreme case of the collective&rsquo;s rules overriding the individual&rsquo;s conscience.'),
        dict(id='wilson', author='David Sloan Wilson and E. O. Wilson', title='Rethinking the Theoretical Foundation of Sociobiology', kind='essay', venue='The Quarterly Review of Biology', year='2007',
             where=('Individual <> Collective', 'individual-collective'),
             note='Their summary of multilevel selection &ndash; &lsquo;Selfishness beats altruism within groups. Altruistic groups beat selfish groups.&rsquo; &ndash; frames the tension between individual and collective.'),
        dict(id='alexander', author='Scott Alexander', title='Meditations on Moloch', kind='essay', venue='Slate Star Codex', year='2014', link='https://slatestarcodex.com/2014/07/30/meditations-on-moloch/',
             where=('Collective <> Civilisational', 'collective-civilisational'),
             note='Alexander&rsquo;s essay on multipolar traps, personified as &lsquo;Moloch&rsquo;: many actors, each following its own rules, together producing outcomes none would choose.'),
    ]),
    ('Convergence', [
        dict(id='riedl', author='Anna Riedl', title='Autopoethics', kind='concept',
             where=('A Hybrid Ethics Stack is the Ethics of Civilisation', 'ethics-stack'),
             note='Riedl&rsquo;s portmanteau of <em>autopoiesis</em> and <em>ethics</em>: ethics as part of how a complex system reproduces itself. The article finds it overlapping with its hybrid ethics stack.'),
        dict(id='parfit', author='Derek Parfit', title='On What Matters', kind='book', year='2011', link=WIKI + 'On_What_Matters',
             where=('Moral Convergence', 'moral-convergence'),
             note='Parfit argues that the best versions of Kantian, contractualist and consequentialist ethics are &lsquo;climbing the same mountain on different sides&rsquo; &ndash; the article&rsquo;s precedent for moral convergence.'),
        dict(id='bostrom', author='Nick Bostrom', title='What is a Singleton?', kind='essay', venue='Future of Humanity Institute', year='2005', link='https://nickbostrom.com/fut/singleton',
             where=('Moral Convergence', 'moral-convergence'),
             note='Bostrom&rsquo;s singleton &ndash; a world order with a single decision-making agency at the highest level &ndash; which, he notes, could form through convergent evolution and need not be monolithic. The article quotes him at length.'),
        dict(id='dennett', author='Daniel Dennett', title='From Bacteria to Bach and Back: The Evolution of Minds', kind='book', year='2017', link=WIKI + 'From_Bacteria_to_Bach_and_Back',
             where=None,
             note='The source of the quotation in the site&rsquo;s footer: &lsquo;Homo sapiens are the only species (so far) with richly cumulative culture.&rsquo;'),
    ]),
]


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', html.unescape(text).lower()).strip('-')


def work(s, linked=True):
    """The work, set as a book (italics) or an essay (quotation marks, its venue in italics)."""
    title = s['title']
    if linked and s.get('link'):
        title = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (s['link'], title)
    if s['kind'] == 'book':
        out = '<em>%s</em>' % title
    elif s['kind'] == 'essay':
        out = '&lsquo;%s&rsquo;, <em>%s</em>' % (title, s['venue'])
    else:
        out = '&lsquo;%s&rsquo;' % title
    if s.get('year'):
        out += ' (%s)' % s['year']
    return out


count = sum(len(items) for _, items in CATEGORIES)

biblio = ''
for name, items in CATEGORIES:
    biblio += '            <h2 class="sr-bib-heading">%s</h2>\n            <ol class="sr-bib">\n' % name
    for s in items:
        biblio += '              <li><a class="sr-jump" href="#%s">%s</a> %s</li>\n' % (s['id'], s['author'], work(s, linked=False))
    biblio += '            </ol>\n'

entries = ''
for name, items in CATEGORIES:
    entries += '            <h2 class="sr-section" id="%s">%s</h2>\n' % (slug(name), name)
    for s in items:
        where = ''
        if s['where']:
            label, anchor = s['where']
            where = '\n                <p class="sr-where">In the article: <a href="../#%s">%s</a></p>' % (anchor, html.escape(label))
        entries += '''            <section class="sr-entry" id="{id}">
                <p class="sr-author">{author}</p>
                <p class="sr-work">{work}</p>
                <p class="sr-note">{note}</p>{where}
            </section>
'''.format(id=s['id'], author=s['author'], work=work(s), note=s['note'], where=where)

# ---- the page -----------------------------------------------------------------------
head = H[:H.index('</head>')]
head = head.replace("url('fonts/", "url('../fonts/").replace('href="favicon/', 'href="../favicon/').replace("'favicon/", "'../favicon/")
head = head.replace('<title>Multi-Scale Ethics</title>', '<title>Sources — Multi-Scale Ethics</title>')
head = re.sub(r'\n  <link rel="canonical"[^>]*>', '', head)
head = head.replace('content="' + SITE + '"', 'content="' + SITE + 'sources/"')
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

    .sr-top { padding: 150px 0 8px; }

    .sr-title {
      margin: 0 0 18px;
      font-family: 'Inter', sans-serif;
      font-weight: 700;
      letter-spacing: -0.02em;
      font-size: 52px;
      line-height: 1.08;
    }

    .sr-intro {
      margin: 0;
      font-family: var(--serif);
      font-size: 24px;
      line-height: 1.4;
    }

    .sr-intro a { color: inherit; text-decoration: none; }
    .sr-intro a:hover { text-decoration: underline; text-underline-offset: 3px; }

    .sr-count {
      margin: 18px 0 0;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      color: var(--muted);
    }

    /* the bibliography: every work in brief, each leading to its entry */
    .sr-bib-heading,
    html .article-body h2.sr-section {
      margin: 44px 0 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--rule);
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 16px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }

    .sr-bib {
      margin: 0;
      padding: 0;
      list-style: none;
      font-family: var(--serif);
      font-size: 18px;
      line-height: 1.45;
    }

    .sr-bib li {
      margin: 0 0 8px;
      padding-left: 1.2em;
      text-indent: -1.2em;
    }

    .sr-jump {
      color: inherit;
      text-decoration: none;
      font-weight: 600;
    }

    .sr-jump:hover { text-decoration: underline; text-underline-offset: 3px; }

    .sr-entries { margin-top: 96px; }

    html .article-body h2.sr-section { margin-top: 72px; -webkit-text-stroke: 0; }
    html .article-body.sr-entries > h2.sr-section:first-child { margin-top: 0; }

    .sr-entry {
      padding: 26px 0;
      border-bottom: 1px solid var(--rule);
      scroll-margin-top: 24px;
    }

    .article-body .sr-entry p { margin: 0; }

    .article-body .sr-entry .sr-author {
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      letter-spacing: 0.02em;
      color: var(--muted);
      margin-bottom: 4px;
    }

    .article-body .sr-entry .sr-work {
      font-size: 1.1em;
      margin-bottom: 10px;
    }

    .article-body .sr-entry .sr-work em a,
    .article-body .sr-entry .sr-work a em {
      -webkit-text-stroke: 0;
    }

    .article-body .sr-entry .sr-work a {
      color: inherit;
      font-weight: 400;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }

    .article-body .sr-entry .sr-where {
      margin-top: 10px;
      font-family: 'IBM Plex Sans', sans-serif;
      font-size: 14px;
      color: var(--muted);
    }

    .article-body .sr-entry .sr-where a { color: inherit; font-weight: 400; }

    .sr-entry:target { background: var(--note-highlight); }

    /* (entries run on one after another, without the article's gap between sections) */
    .article-body .sr-entry + .sr-entry { margin-top: 0; }

    .sr-end { height: 140px; }

    @media (max-width: 960px) {
      .back-arrow { top: 28px; left: 24px; }
      .site-title { position: absolute; top: 22px; right: 24px; }
      .sr-top { padding-top: 110px; }
      .sr-title { font-size: 38px; }
      .sr-intro { font-size: 20px; }
      .sr-bib { font-size: 17px; }
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
          <div class="sr-top">
            <h1 class="sr-title">Sources</h1>
            <p class="sr-intro">Works drawn on in <a href="../"><em>Multi-Scale Ethics</em></a>.</p>
            <p class="sr-count">''' + '%d sources in %d categories' % (count, len(CATEGORIES)) + '''</p>
''' + biblio + '''          </div>
          <div class="article-body sr-entries">
''' + entries + '''          </div>
          <div class="sr-end"></div>
        </article>
      </main>
    </div>
  </div>

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
  <script src="../assets/tools.js?v=''' + TOOLS_V + '''" data-search-scope=".sr-top, .sr-entries"></script>
</body>
</html>
'''

os.makedirs('sources', exist_ok=True)
open('sources/index.html', 'w').write(head + style + '</head>\n' + body)
print('Wrote sources/index.html (%d sources)' % count)
