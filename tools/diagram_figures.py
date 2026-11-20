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
# The Concentric Ethics rings, lifted apart into layers and seen at an angle
# (the 2.5D style of the scales diagram): consequentialism the broadest layer at
# the base, deontology above it, virtue the smallest at the top. Seen from
# directly above, the three discs would close back into the concentric rings.
# Each disc in the rings' own translucent gold, its edge a little deeper;
# each rests partly over the top of the one beneath it, by the same amount.
def ethics_stack():
    cx, t = 300, 16
    layers = [   # from the base up, drawn in that order: radius, centre height
        ('Consequentialism', 'the civilisational &middot; the state', 250, 430, '#eaa528', 0.30, '#eab650'),
        ('Deontology', 'the collective &middot; the city', 147, 302, '#f7c85a', 0.42, '#efc04a'),
        ('Virtue', 'the individual &middot; the tribe', 70, 224, '#fad76e', 0.55, '#f2c64f'),
    ]
    s = ['<svg class="fig-svg dg-svg" viewBox="0 165 760 430" role="img" aria-labelledby="fig-stack-title">',
         '<title id="fig-stack-title">The ethics of civilisation as a hybrid stack: three gold discs, one above another, '
         'the concentric rings lifted apart. Consequentialism, the civilisational scale and the state, is the broadest, at the base; '
         'deontology, the collective and the city, above it; and virtue, the individual and the tribe, the smallest, at the top.</title>']
    for name, sub, rx, cy, fill, alpha, stroke in layers:
        ry = rx / 2
        side = ('M%g,%g L%g,%g A%g,%g 0 0 0 %g,%g L%g,%g A%g,%g 0 0 1 %g,%g Z'
                % (cx - rx, cy, cx - rx, cy + t, rx, ry, cx + rx, cy + t, cx + rx, cy, rx, ry, cx - rx, cy))
        # (each disc backed in the page's colour, so that it hides the
        # layers beneath it while keeping the rings' translucent gold)
        s.append('<path class="dg-backing" d="%s M%g,%g A%g,%g 0 1 0 %g,%g A%g,%g 0 1 0 %g,%g Z"/>'
                 % (side, cx - rx, cy, rx, ry, cx + rx, cy, rx, ry, cx - rx, cy))
        s.append('<path d="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>'
                 % (side, fill, min(1, alpha * 1.9), stroke))
        s.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="1.5"/>'
                 % (cx, cy, rx, ry, fill, alpha, stroke))
    lx = 600   # the labels in one column, each led out from its disc's edge
    for name, sub, rx, cy, fill, alpha, stroke in layers:
        y = cy + t / 2
        s.append('<polyline class="dg-leader" points="%g,%g %g,%g"/>' % (cx + rx + 10, y, lx - 14, y))
        s.append('<text class="dg-label" x="%g" y="%g">%s</text>' % (lx, y - 3, name))
        s.append('<text class="dg-sub" x="%g" y="%g">%s</text>' % (lx, y + 20, sub))
    s.append('</svg>')
    return figure('figure-ethics-stack', '\n'.join(s), 'the ethics of civilisation as a hybrid ethics stack')


# ---- A. theory &times; scale --------------------------------------------------------
def fit_matrix():
    native = lambda cls, text: '<td class="fit %s"><span class="fit-tag">Native</span>%s</td>' % (cls, text)
    misfit = lambda tag, text: '<td class="misfit"><span class="fit-tag">%s</span>%s</td>' % (tag, text)
    rows = [
        ('Consequentialism', 't-consequentialism', [
            misfit('Alienating', 'The impartial calculus estranges a person from their own attachments.'),
            misfit('Unpredictable', 'Case-by-case calculation erodes the predictability that lets strangers trust one another.'),
            native('t-consequentialism', 'System-wide optimisation: the ethics of the state.')]),
        ('Deontology', 't-deontology', [
            misfit('Rigid', 'Rules stand in for knowing someone, where character could be read first-hand.'),
            native('t-deontology', 'Shared rules let strangers trust one another: the ethics of the city.'),
            misfit('Complicated', 'Rules multiply but cannot keep pace with a complex, adaptive system.')]),
        ('Virtue Ethics', 't-virtue', [
            native('t-virtue', 'Character known first-hand: the ethics of the tribe.'),
            misfit('Vague', 'No character to track in a committee; judged by outcomes, it collapses into consequentialism.'),
            misfit('Negligible', 'One person&rsquo;s character barely registers among billions; it reaches civilisation only through the collectives it shapes.')]),
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
    .dg-svg .dg-label { font-size: 20px; font-weight: 500; }
    /* (the sublabels in the text colour, softened a little, rather than the faint grey) */
    .dg-svg .dg-sub { font-family: var(--serif); font-style: italic; font-size: 19px; fill: color-mix(in srgb, var(--canvas-ink) 72%, var(--canvas-bg)); }
    .dg-svg .dg-backing { fill: var(--canvas-bg); }
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
