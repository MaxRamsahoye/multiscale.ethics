# The Diagrams page's own figures (those not taken from the article): drawn
# here as SVG and HTML in the site's golden palette, and placed by
# tools/make-diagrams-page.py.

LIGHT = ('#fce278', '#eac859', '#c89a28')   # top, left side, right side
MID = ('#f5be28', '#d69e18', '#a5750e')
DARK = ('#d6920a', '#b27406', '#855404')


def pts(*p):
    return ' '.join('%g,%g' % (round(x, 1), round(y, 1)) for x, y in p)


def slab(cx, cy, w, h, t, c):
    top, left, right = c
    return ('<polygon fill="%s" points="%s"/>' % (left, pts((cx - w, cy), (cx, cy + h), (cx, cy + h + t), (cx - w, cy + t))) +
            '<polygon fill="%s" points="%s"/>' % (right, pts((cx, cy + h), (cx + w, cy), (cx + w, cy + t), (cx, cy + h + t))) +
            '<polygon fill="%s" points="%s"/>' % (top, pts((cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy))))


def figure(fid, svg, caption, extra=''):
    return ('<figure class="article-figure dg-figure%s" id="%s">\n%s\n  <figcaption>%s</figcaption>\n</figure>'
            % (extra, fid, svg, caption))


# ---- 4. the hybrid ethics stack -------------------------------------------------
def ethics_stack():
    cx, w, h, t = 250, 170, 85, 22
    layers = [   # from the base up, drawn in that order
        ('Virtue', 'the individual &middot; the tribe', 330, LIGHT),
        ('Deontology', 'the collective &middot; the city', 220, MID),
        ('Consequentialism', 'the civilisational &middot; the state', 110, DARK),
    ]
    s = ['<svg class="fig-svg dg-svg" viewBox="0 0 760 470" role="img" aria-labelledby="fig-stack-title">',
         '<title id="fig-stack-title">The ethics of civilisation as a hybrid stack of three layers: virtue at the base, '
         'for the individual and the tribe; deontology above it, for the collective and the city; and consequentialism at the top, '
         'for the civilisational scale and the state.</title>']
    for name, sub, cy, c in layers:
        s.append(slab(cx, cy, w, h, t, c))
    for name, sub, cy, c in layers:
        lx = cx + w + 70
        s.append('<polyline class="dg-leader" points="%g,%g %g,%g"/>' % (cx + w + 10, cy + t / 2, lx - 12, cy + t / 2))
        s.append('<text class="dg-label" x="%g" y="%g">%s</text>' % (lx, cy + t / 2 - 2, name))
        s.append('<text class="dg-sub" x="%g" y="%g">%s</text>' % (lx, cy + t / 2 + 18, sub))
    s.append('</svg>')
    return figure('figure-ethics-stack', '\n'.join(s), 'the ethics of civilisation as a hybrid ethics stack')


# ---- A. theory &times; scale --------------------------------------------------------
def fit_matrix():
    native = lambda cls, text: '<td class="fit %s"><span class="fit-tag">Native</span>%s</td>' % (cls, text)
    misfit = lambda tag, text: '<td class="misfit"><span class="fit-tag">%s</span>%s</td>' % (tag, text)
    none = '<td class="unset" aria-label="Not discussed">&ndash;</td>'
    rows = [
        ('Consequentialism', 't-consequentialism', [
            misfit('Alienating', 'The impartial calculus estranges a person from their own attachments.'),
            none,
            native('t-consequentialism', 'System-wide optimisation: the ethics of the state.')]),
        ('Deontology', 't-deontology', [
            none,
            native('t-deontology', 'Shared rules let strangers trust one another: the ethics of the city.'),
            misfit('Complicated', 'Rules multiply but cannot keep pace with a complex, adaptive system.')]),
        ('Virtue Ethics', 't-virtue', [
            native('t-virtue', 'Character known first-hand: the ethics of the tribe.'),
            misfit('Vague', 'No character to track in a committee; judged by outcomes, it collapses into consequentialism.'),
            none]),
    ]
    body = '\n'.join('      <tr class="%s"><th scope="row"><span class="t-name">%s</span></th>%s</tr>' % (cls, name, ''.join(cells)) for name, cls, cells in rows)
    return ('<figure class="article-figure figure-table dg-matrix" id="figure-fit">\n'
            '  <table class="theories-table fit-table">\n'
            '    <thead><tr><th scope="col">Theory</th><th scope="col">Individual</th><th scope="col">Collective</th><th scope="col">Civilisational</th></tr></thead>\n'
            '    <tbody>\n' + body + '\n    </tbody>\n  </table>\n'
            '  <figcaption>each theory at its native scale, and the problems of applying it at the wrong one</figcaption>\n</figure>')


# ---- B. the scales of human society --------------------------------------------------
def scale_profiles():
    rows = [
        ('Tribe', 's-tribe', 'Up to ~150 (Dunbar&rsquo;s number)', 'Reputation and gossip: a shared ledger of character', 'Virtue',
         'Beyond 150 no one can track everyone, and vice goes unseen'),
        ('City', 's-city', 'Hundreds to thousands, and beyond', 'Shared conventions &ndash; manners, commandments &ndash; among strangers', 'Deontology',
         'Absolute rules are inflexible as complexity grows'),
        ('State', 's-state', 'Networks of cities: nations and empires', 'System-wide optimisation of aggregate welfare', 'Consequentialism',
         'The tyranny of the majority, overriding principles and virtues'),
        ('Civilisation', 's-civilisation', 'Global', 'Each theory at its own scale, in a hybrid ethics stack', 'All three, as a stack',
         'Conflicts between classes of agent; the multipolar trap'),
    ]
    body = '\n'.join(
        '      <tr class="%s"><th scope="row"><span class="t-name">%s</span></th><td>%s</td><td>%s</td><td><strong>%s</strong></td><td>%s</td></tr>' % (cls, name, pop, trust, ethic, strain)
        for name, cls, pop, trust, ethic, strain in rows)
    return ('<figure class="article-figure figure-table dg-matrix" id="figure-profiles">\n'
            '  <table class="theories-table profiles-table">\n'
            '    <thead><tr><th scope="col">Scale</th><th scope="col">Population</th><th scope="col">How trust works</th><th scope="col">Ethic</th><th scope="col">Where it strains</th></tr></thead>\n'
            '    <tbody>\n' + body + '\n    </tbody>\n  </table>\n'
            '  <figcaption>the scales of human society: how each coordinates, and where it gives way</figcaption>\n</figure>')


CSS = '''
    /* the Diagrams page's own figures */
    .article-body .dg-figure .dg-svg { max-width: 680px; margin: 0 auto; }
    .dg-svg text { font-family: 'IBM Plex Sans', sans-serif; fill: var(--canvas-ink); }
    .dg-svg .dg-label { font-size: 18px; font-weight: 500; }
    .dg-svg .dg-sub { font-family: var(--serif); font-style: italic; font-size: 16px; fill: var(--muted); }
    .dg-svg .dg-leader { fill: none; stroke: var(--muted); stroke-width: 1; }

    /* the matrices: shaded where a theory is native, plain where it strains */
    .fit-table td { width: 24.6%; }
    .fit-table .fit-tag {
      display: block;
      margin-bottom: 6px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .fit-table td.fit { color: #3a2a00; }
    .fit-table td.t-consequentialism { background: #fde27a; }
    .fit-table td.t-deontology { background: #f5be2c; }
    .fit-table td.t-virtue { background: #d6920a; }
    .fit-table td.misfit .fit-tag { color: var(--inverse-bg); }
    .fit-table td.unset { color: var(--muted); text-align: center; vertical-align: middle; }
    .profiles-table tbody tr.s-tribe th { background: #fde27a; }
    .profiles-table tbody tr.s-city th { background: #f5be2c; }
    .profiles-table tbody tr.s-state th { background: #d6920a; }
    .profiles-table tbody tr.s-civilisation th {
      background: linear-gradient(to bottom, #fde27a 0 33.4%, #f5be2c 33.4% 66.7%, #d6920a 66.7%);
    }

    @media (max-width: 640px) {
      /* the drawings kept legible on phones: at a readable size, scrolling
         sideways within their own frame */
      .article-body .dg-figure { overflow-x: auto; max-width: calc(100vw - 48px); }
      .article-body .dg-figure .dg-svg { min-width: 580px; }
      .fit-table td { width: auto; }
      .fit-table td.fit::before { color: inherit; opacity: 0.7; }
      .fit-table td.unset { display: none; }
      .fit-table td::before,
      .profiles-table td::before {
        content: attr(data-col);
        display: block;
        margin-bottom: 4px;
        font-size: 11px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--muted);
      }
    }
'''


def label_cells(table_html, columns):
    """Give each cell its column's name (shown above it on phones)."""
    import re
    out = []
    for row in table_html.split('\n'):
        if '<tbody>' in row or not row.strip().startswith('<tr class'):
            out.append(row)
            continue
        cells = iter(columns)
        out.append(re.sub(r'<td( |>)', lambda m: '<td data-col="%s"%s' % (next(cells), m.group(1)), row))
    return '\n'.join(out)


def figures():
    return {
        'stack': ethics_stack(),
        'fit': label_cells(fit_matrix(), ['Individual', 'Collective', 'Civilisational']),
        'profiles': label_cells(scale_profiles(), ['Population', 'How trust works', 'Ethic', 'Where it strains']),
    }
