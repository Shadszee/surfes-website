"""SURFES static site generator.
Run: python3 build/site.py   (from the project root)
Products live in build/products.json. Edit that file, re-run, upload /site.
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
DATA = json.load(open(os.path.join(ROOT, 'build', 'products.json'), encoding='utf-8'))
SURF = [s for s in DATA['surfaces'] if not s['discontinued']]
DOORS = [d for d in DATA['doors'] if d['page']]

# ---- Placeholder business details: replace before launch ----
PHONE = '(02) 4587 9261'
PHONE_LINK = '+61245879261'
EMAIL = 'email@placeholder.com.au'        # PLACEHOLDER
ADDRESS = 'Street address, Suburb NSW 0000'  # PLACEHOLDER
FACEBOOK = '#'   # PLACEHOLDER
INSTAGRAM = '#'  # PLACEHOLDER

e = html.escape


def rel(depth):
    return '../' * depth


def surf_url(s, r):
    return f'{r}solid-surfaces/{s["slug"]}/index.html'


def door_url(d, r):
    return f'{r}mdf-routed-doors/{d["slug"]}/index.html'


def img(r, name, alt='', cls='', lazy=True, sizes=''):
    if not name:
        return f'<div class="img-missing {cls}"><span>Image needed</span></div>'
    return (f'<img src="{r}images/{name}" alt="{e(alt)}"'
            f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}'
            f'{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async">')


def head(title, desc, r, og=None):
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{f'<meta property="og:image" content="{r}images/{og}">' if og else ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/site.css">
</head>
<body>
'''


def header(r, active=''):
    def nav(key, label, href):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{r}index.html" aria-label="SURFES home">{img(r, "surfes-logo.png", "SURFES", lazy=False)}</a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav" onclick="var o=this.getAttribute('aria-expanded')==='true';this.setAttribute('aria-expanded',!o);document.body.classList.toggle('nav-open',!o)"><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="nav" class="main-nav" aria-label="Main">
      {nav('surf', 'Surfaces', f'{r}solid-surfaces/index.html')}
      {nav('doors', 'Doors', f'{r}mdf-routed-doors/index.html')}
      {nav('trade', 'Trade', f'{r}trade-partners/index.html')}
      {nav('about', 'About', f'{r}about/index.html')}
      {nav('news', 'News', f'{r}news/index.html')}
      <a class="btn btn-sm btn-clay" href="{r}contact/index.html">Order a sample</a>
    </nav>
  </div>
</header>
<main id="main">
'''


def cta(r, title='See it where it will live.',
        body='Order a sample and look at it in your own light, morning and evening, beside your cabinetry. Then decide.'):
    return f'''<section class="cta-band" style="background-image:url('{r}images/surfes-stone-block.webp')">
  <div class="wrap cta-inner">
    <div>
      <h2>{e(title)}</h2>
      <p>{e(body)}</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
      <a class="btn btn-ghost" href="tel:{PHONE_LINK}">Call {PHONE}</a>
    </div>
  </div>
</section>
'''


def footer(r):
    return f'''</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      {img(r, "surfes-logo-light.png", "SURFES")}
      <p class="rule-line">Surfaces worth choosing once.</p>
      <p>Silica-free decorative surfaces for kitchens, cabinetry and interiors. Made in Australia by Craftmark.</p>
    </div>
    <div>
      <h3>Products</h3>
      <ul>
        <li><a href="{r}solid-surfaces/index.html">Solid surfaces</a></li>
        <li><a href="{r}solid-surfaces/index.html">Outdoor surfaces</a></li>
        <li><a href="{r}mdf-routed-doors/index.html">MDF routed doors</a></li>
        <li><a href="{r}contact/index.html">Order a sample</a></li>
      </ul>
    </div>
    <div>
      <h3>Company</h3>
      <ul>
        <li><a href="{r}trade-partners/index.html">Trade partners</a></li>
        <li><a href="{r}about/index.html">About</a></li>
        <li><a href="{r}news/index.html">News</a></li>
        <li><a href="{r}contact/index.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <h3>Contact</h3>
      <ul class="contact-list">
        <li><a href="tel:{PHONE_LINK}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{ADDRESS}</li>
      </ul>
      <div class="social">
        <a href="{FACEBOOK}" aria-label="Facebook">{img(r, "facebook.svg", "")}</a>
        <a href="{INSTAGRAM}" aria-label="Instagram">{img(r, "instagram.svg", "")}</a>
      </div>
    </div>
  </div>
  <div class="wrap footer-brands">
    <span>Made by</span>
    <a href="https://www.craftmark.com.au/">{img(r, "craftmark-logo.png", "Craftmark")}</a>
    <a href="https://trade.craftmark.com.au/">{img(r, "craftmark-trade-logo.png", "Craftmark Trade")}</a>
  </div>
  <div class="wrap footer-legal">
    <span>&copy; 2026 Craftmark Pty Ltd. All rights reserved.</span>
    <span><a href="https://www.craftmark.com.au/privacy-policy">Privacy policy</a> <a href="https://www.craftmark.com.au/terms-and-conditions">Terms and conditions</a></span>
  </div>
</footer>
</body>
</html>
'''


def swatch_card(s, r):
    tag = '<span class="tag">Outdoor</span>' if s['outdoor'] else ''
    return f'''<a class="swatch-card" href="{surf_url(s, r)}">
  <div class="swatch-img">{img(r, s["swatch"], s["name"] + " solid surface")}{tag}</div>
  <h3>{e(s["name"])}</h3>
  <p>{e(s.get("tone", ""))}</p>
</a>'''


def door_card(d, r):
    return f'''<a class="door-card" href="{door_url(d, r)}">
  <div class="door-img">{img(r, d["thumb"], d["name"] + " MDF routed door")}</div>
  <h3>{e(d["name"])}</h3>
  <p>{e(d["spec"])}</p>
</a>'''


ICON = {
    'silica': '<svg viewBox="0 0 24 24"><path d="M12 3l7 4v5c0 4.5-3 8-7 9-4-1-7-4.5-7-9V7z"/><path d="M9 12l2 2 4-4"/></svg>',
    'warranty': '<svg viewBox="0 0 24 24"><circle cx="12" cy="10" r="6"/><path d="M9 15.5L8 21l4-2 4 2-1-5.5"/></svg>',
    'repair': '<svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
    'sun': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    'local': '<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    'seam': '<svg viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="8" rx="1"/><path d="M12 8v8" stroke-dasharray="2 2"/></svg>',
}


def home():
    r = rel(0)
    featured = [s for s in SURF if s['slug'] in ('taj-sogno', 'calacatta-oro', 'luna-bianco', 'aurora-cloud', 'artesian-concrete', 'ombra-concrete', 'sabbia-dune', 'glacier-white')]
    fdoors = [d for d in DOORS if d['slug'] in ('richmond', 'mulgrave', 'bilpin-20', 'katoomba')]
    proof = [('silica', 'Zero silica', 'Safe to cut on site'),
             ('warranty', '10 year warranty', 'On every surface'),
             ('repair', 'Repairable', 'Restored, not replaced'),
             ('sun', 'UV-stable outdoor range', 'Holds its colour outside'),
             ('local', 'Made in Australia', 'By Craftmark')]
    out = head('SURFES | Surfaces worth choosing once',
               'Silica-free decorative surfaces for kitchens, cabinetry and interiors. Chosen for colour, texture and the way they actually live in a home. Made in Australia.',
               r, 'craftmark-surfaces-kitchen-bathroom.webp')
    out += header(r)
    out += f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Surfaces worth<br>choosing once.</h1>
      <span class="clay-rule"></span>
      <p class="lede">Decorative surfaces for kitchens, cabinetry and interiors. Chosen for colour, texture and the way they actually live in a home.</p>
      <div class="hero-actions">
        <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
        <a class="btn btn-ghost" href="{r}solid-surfaces/index.html">Explore surfaces</a>
      </div>
    </div>
    <div class="hero-media">
      {img(r, "surfes-taj-sogno-island.webp", "Taj Sogno waterfall island edge against dark timber cabinetry", "hero-main", lazy=False)}
      <a class="hero-chip" href="{r}solid-surfaces/taj-sogno/index.html">{img(r, "craftmark-surfaces-kitchen-bathroom-taj-sogno.webp", "", lazy=False)}<span><small>Pictured</small>Taj Sogno<em>Warm off-white / taupe / gold / soft grey</em></span></a>
    </div>
  </div>
</section>

<section class="proof" aria-label="What every SURFES surface gives you">
  <div class="wrap proof-row">
    {''.join(f'<div class="proof-item"><span class="icon">{ICON[i]}</span><div><strong>{t}</strong><span>{s}</span></div></div>' for i, t, s in proof)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split">
      <div>
        <p class="eyebrow">Solid surfaces</p>
        <h2>Start with the colour.</h2>
      </div>
      <a class="link" href="{r}solid-surfaces/index.html">All {len(SURF)} colours</a>
    </div>
    <div class="swatch-grid">
      {''.join(swatch_card(s, r) for s in featured)}
    </div>
  </div>
</section>

<section class="wide-band">
  {img(r, "surfes-kitchen-wide.webp", "Kitchen with a pale speckled surface on the island and splashback, oak cabinetry and brass tapware")}
  <div class="wrap"><p class="wide-caption">A surface rarely gets chosen alone. Show it on its own, then show what belongs beside it.</p></div>
</section>

<section class="section section-stone">
  <div class="wrap feature-split">
    <figure class="feature-media">{img(r, "surfes-sabbia-dune-kitchen.webp", "Sabbia Dune benchtop with oak cabinetry and a vertical tile splashback")}<figcaption><a href="{r}solid-surfaces/sabbia-dune/index.html">Sabbia Dune</a> with pale timber</figcaption></figure>
    <div class="feature-copy">
      <p class="eyebrow">What you are buying</p>
      <h2>The look of stone. None of the silica.</h2>
      <p class="lede">Made from natural minerals with zero silica content. It can be cut safely on site, joined without visible seams and repaired if it is ever damaged.</p>
      <ul class="benefits">
        <li><span class="icon">{ICON['silica']}</span><div><h3>Zero silica</h3><p>Safer for your installer to cut, and for the people who make it.</p></div></li>
        <li><span class="icon">{ICON['repair']}</span><div><h3>Repairable</h3><p>Chips and scratches can be restored to original condition. No replacing the whole benchtop.</p></div></li>
        <li><span class="icon">{ICON['seam']}</span><div><h3>Seamless</h3><p>Pieces join into one unbroken island. Colour and texture run through the full thickness.</p></div></li>
        <li><span class="icon">{ICON['sun']}</span><div><h3>Outdoor range</h3><p>UV resistant, so outdoor colours do not fade or chalk in the sun.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split">
      <div>
        <p class="eyebrow">MDF routed doors</p>
        <h2>The door beside the benchtop.</h2>
      </div>
      <a class="link" href="{r}mdf-routed-doors/index.html">All {len(DOORS)} profiles</a>
    </div>
    <div class="door-grid">
      {''.join(door_card(d, r) for d in fdoors)}
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap trade-split">
    <div class="trade-copy">
      <p class="eyebrow">Trade</p>
      <h2>No pitch. Just what you need.</h2>
      <p>Fast samples, spec sheets and trade pricing for designers, cabinetmakers, builders and showrooms. Custom sheet sizes to cut waste, and custom colours for developments of 100+ units.</p>
      <a class="btn btn-ghost-light" href="{r}trade-partners/index.html">Trade enquiries</a>
    </div>
    <div class="maker">
      <p class="eyebrow">The maker</p>
      <p class="maker-line">SURFES surfaces and doors are manufactured in Australia by Craftmark, a cabinetry and joinery manufacturer with over 20 years in the industry.</p>
      {img(r, "craftmark-logo.png", "Craftmark", "maker-logo")}
    </div>
  </div>
</section>
'''
    out += cta(r)
    out += footer(r)
    return out


def surface_page(s):
    r = rel(2)
    gallery = [x for x in [s['swatch'], s['room']] + s['installer'] if x]
    related = [x for x in SURF if x['slug'] != s['slug'] and x['outdoor'] == s['outdoor']][:4]
    feats = ''.join(f'<li>{e(f)}</li>' for f in s['features'])
    intro = ''.join(f'<p>{e(p)}</p>' for p in s['intro'])
    use = 'Indoor and outdoor' if s['outdoor'] else 'Kitchens, bathrooms, laundries'
    thumbs = ''.join(
        f'<button class="thumb{" is-active" if i == 0 else ""}" data-src="{r}images/{g}" aria-label="Show image {i + 1}">{img(r, g, "")}</button>'
        for i, g in enumerate(gallery)) if len(gallery) > 1 else ''
    out = head(f'{s["name"]} | Solid surfaces | SURFES', s['desc'], r, s['swatch'])
    out += header(r, 'surf')
    out += f'''<div class="wrap crumbs"><a href="{r}index.html">Home</a><span>/</span><a href="{r}solid-surfaces/index.html">Solid surfaces</a><span>/</span><span aria-current="page">{e(s["name"])}</span></div>
<section class="product">
  <div class="wrap product-grid">
    <div class="gallery">
      <div class="gallery-main">{img(r, gallery[0] if gallery else None, s["name"] + " solid surface", "gallery-img", lazy=False)}</div>
      <div class="gallery-thumbs">{thumbs}</div>
    </div>
    <div class="product-info">
      <p class="eyebrow">{'Outdoor surface' if s['outdoor'] else 'Solid surface'}</p>
      <h1>{e(s["name"])}</h1>
      <p class="tone">{e(s.get("tone", ""))}</p>
      <div class="product-intro">{intro}</div>
      <dl class="specs">
        <div><dt>Use</dt><dd>{use}</dd></div>
        <div><dt>Material</dt><dd>Silica-free solid surface</dd></div>
        <div><dt>Warranty</dt><dd>10 year product warranty</dd></div>
      </dl>
      <div class="product-actions">
        <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
        <a class="btn btn-ghost" href="{r}contact/index.html">Ask a question</a>
      </div>
      <h2 class="h-small">Colour, movement, texture</h2>
      <ul class="ticks">{feats}</ul>
      <p class="note">The colour shown is a representation only and may vary from the actual product. Please see a physical sample before making your final selection.</p>
    </div>
  </div>
</section>

<section class="section section-stone">
  <div class="wrap three-up">
    <div><span class="icon">{ICON['warranty']}</span><h3>10 year product warranty</h3><p>If anything goes wrong with your surface, we will replace it.</p></div>
    <div><span class="icon">{ICON['repair']}</span><h3>Seamless repairs</h3><p>Restored to original condition if accidentally damaged, without replacing the whole benchtop.</p></div>
    <div><span class="icon">{ICON['seam']}</span><h3>Solid material</h3><p>Colour and texture run through the entire thickness, so it cannot delaminate or wear away.</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">Keep exploring</p><h2>You might also like</h2></div>
      <a class="link" href="{r}solid-surfaces/index.html">View all colours</a>
    </div>
    <div class="swatch-grid">{''.join(swatch_card(x, r) for x in related)}</div>
  </div>
</section>
<script>
document.querySelectorAll('.thumb').forEach(function(b){{b.addEventListener('click',function(){{
  document.querySelector('.gallery-img').src=b.dataset.src;
  document.querySelectorAll('.thumb').forEach(function(t){{t.classList.toggle('is-active',t===b)}});
}})}});
</script>
'''
    out += cta(r, 'Same surface. Different light.', 'Order a sample and see it where it is actually going to live.')
    out += footer(r)
    return out


STYLES = [('shaker', 'Shaker and framed'), ('grooved', 'Grooved'), ('detailed', 'Detailed profiles'), ('flat', 'Flat and handleless')]
STYLE_NAME = dict(STYLES)
PAIR = ['taj-sogno', 'sabbia-dune', 'calacatta-oro', 'ombra-concrete']


def door_card_f(d, r):
    return f'''<a class="door-card" data-style="{d["style"]}" href="{door_url(d, r)}">
  <div class="door-img">{img(r, d["thumb"], d["name"] + " MDF routed door")}</div>
  <h3>{e(d["name"])}</h3>
  <p>{e(d["spec"])}</p>
</a>'''


def doors_page():
    r = rel(1)
    photos = [d for d in DOORS if d.get('photo')][:8]
    out = head('MDF routed doors | SURFES',
               'Painted MDF routed doors from classic Shaker to V-groove. Routed with diamond tooling on high-density moisture-resistant MDF and finished in repairable polyurethane.',
               r, 'craftmark-mdf-doors-kitchen-bathroom.webp')
    out += header(r, 'doors')
    out += f'''<section class="hero hero-tight">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">MDF routed doors</p>
      <h1>The door beside the benchtop.</h1>
      <span class="clay-rule"></span>
      <p class="lede">{len(DOORS)} painted MDF profiles, from classic Shaker to tight V-grooves. Routed with diamond tooling on a dense, moisture-resistant core and finished in polyurethane you can repair.</p>
      <div class="hero-actions">
        <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
        <a class="btn btn-ghost" href="#range">See the profiles</a>
      </div>
    </div>
    <div class="hero-media">
      {img(r, "craftmark-mdf-doors-kitchen-bathroom.webp", "White kitchen with V-groove MDF routed doors and brass handles", "hero-main", lazy=False)}
    </div>
  </div>
</section>

<section class="section section-stone" id="range">
  <div class="wrap">
    <div class="section-head range-head">
      <div>
        <p class="eyebrow">The range</p>
        <h2>Choose a profile.</h2>
      </div>
      <div class="filters" role="group" aria-label="Filter by style">
        <button class="filter is-active" data-filter="all">All <span>{len(DOORS)}</span></button>
        {''.join(f'<button class="filter" data-filter="{k}">{v} <span>{sum(1 for d in DOORS if d["style"] == k)}</span></button>' for k, v in STYLES)}
      </div>
    </div>
    <div class="door-grid" id="door-grid">
      {''.join(door_card_f(d, r) for d in DOORS)}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap feature-split">
    <figure class="feature-media">{img(r, "mdf-routed-door-benefits-craftmark.webp", "Blue painted Shaker doors above a glass display cabinet")}</figure>
    <div class="feature-copy">
      <p class="eyebrow">How they are made</p>
      <h2>Made to stay straight. Made to be fixed.</h2>
      <ul class="benefits">
        <li><span class="icon">{ICON['seam']}</span><div><h3>Stable core</h3><p>Every face-routed door is cut from superdense, high-density moisture-resistant MDF. It limits bowing, so doors stay aligned for years.</p></div></li>
        <li><span class="icon">{ICON['silica']}</span><div><h3>Clean lines</h3><p>Diamond and carbide tooling leaves no machine marks. Edges come out crisp and the face is ready for a high-end paint finish.</p></div></li>
        <li><span class="icon">{ICON['repair']}</span><div><h3>Repairable</h3><p>Unlike melamine or veneer, polyurethane paint can be colour-matched and touched up years after install, or repainted for a new look.</p></div></li>
        <li><span class="icon">{ICON['local']}</span><div><h3>Any profile</h3><p>CNC routing gives you Shaker, V-groove, cove or a bespoke pattern, without the knots and grain of solid timber.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-stone">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Installed</p>
      <h2>In real rooms.</h2>
    </div>
    <div class="photo-grid">
      {''.join(f'<a href="{door_url(d, r)}">{img(r, d["photo"], d["name"] + " doors installed")}<span>{e(d["name"])}</span></a>' for d in photos)}
    </div>
  </div>
</section>
<script>
(function(){{var b=document.querySelectorAll('.filter'),c=document.querySelectorAll('#door-grid .door-card');
b.forEach(function(x){{x.addEventListener('click',function(){{var f=x.dataset.filter;
b.forEach(function(y){{y.classList.toggle('is-active',y===x)}});
c.forEach(function(k){{k.hidden=!(f==='all'||k.dataset.style===f)}});}})}});}})();
</script>
'''
    out += cta(r, 'See the profile up close.', 'Order a door sample and hold it against your benchtop and handles before you commit.')
    out += footer(r)
    return out


def door_page(d):
    r = rel(2)
    gallery = [x for x in d['images'] if x] or [d['thumb']]
    related = [x for x in DOORS if x['style'] == d['style'] and x['slug'] != d['slug']][:4]
    if len(related) < 4:
        related += [x for x in DOORS if x not in related and x['slug'] != d['slug']][:4 - len(related)]
    pairs = [s for s in SURF if s['slug'] in PAIR]
    thumbs = ''.join(
        f'<button class="thumb{" is-active" if i == 0 else ""}" data-src="{r}images/{g}" aria-label="Show image {i + 1}">{img(r, g, "")}</button>'
        for i, g in enumerate(gallery)) if len(gallery) > 1 else ''
    note = '<p class="note">Profile detail to be confirmed.</p>' if d.get('spec_unconfirmed') else ''
    out = head(f'{d["name"]} | MDF routed doors | SURFES',
               f'The {d["name"]} MDF routed door: {d["spec"]}. Routed on high-density moisture-resistant MDF and finished in repairable polyurethane paint.',
               r, gallery[0])
    out += header(r, 'doors')
    out += f'''<div class="wrap crumbs"><a href="{r}index.html">Home</a><span>/</span><a href="{r}mdf-routed-doors/index.html">MDF routed doors</a><span>/</span><span aria-current="page">{e(d["name"])}</span></div>
<section class="product">
  <div class="wrap product-grid">
    <div class="gallery">
      <div class="gallery-main">{img(r, gallery[0], d["name"] + " MDF routed door", "gallery-img", lazy=False)}</div>
      <div class="gallery-thumbs">{thumbs}</div>
    </div>
    <div class="product-info">
      <p class="eyebrow">MDF routed door &middot; {STYLE_NAME[d["style"]]}</p>
      <h1>{e(d["name"])}</h1>
      <p class="tone">{e(d["spec"])}</p>
      <div class="product-intro"><p>A painted MDF door routed to the {e(d["name"])} profile. Cut on a CNC with diamond tooling from high-density moisture-resistant MDF, then finished in polyurethane paint.</p></div>
      {note}
      <dl class="specs">
        <div><dt>Profile</dt><dd>{e(d["spec"])}</dd></div>
        <div><dt>Style</dt><dd>{STYLE_NAME[d["style"]]}</dd></div>
        <div><dt>Substrate</dt><dd>Superdense high-density MDF, moisture resistant</dd></div>
        <div><dt>Finish</dt><dd>Polyurethane paint, colour-matchable for repairs</dd></div>
      </dl>
      <div class="product-actions">
        <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
        <a class="btn btn-ghost" href="{r}contact/index.html">Ask a question</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-stone">
  <div class="wrap three-up">
    <div><span class="icon">{ICON['silica']}</span><h3>Smooth finish</h3><p>No grain, knots or voids. Painted, your cabinetry has an even, high-end finish.</p></div>
    <div><span class="icon">{ICON['seam']}</span><h3>Stays aligned</h3><p>The superdense core limits bowing, so doors stay straight for years.</p></div>
    <div><span class="icon">{ICON['repair']}</span><h3>Fully repairable</h3><p>The paint can be colour-matched to fix a blemish, or changed completely for a new look.</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">A surface rarely gets chosen alone</p><h2>Pair it with a benchtop</h2></div>
      <a class="link" href="{r}solid-surfaces/index.html">All colours</a>
    </div>
    <div class="swatch-grid">{''.join(swatch_card(x, r) for x in pairs)}</div>
  </div>
</section>

<section class="section section-stone">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">Similar profiles</p><h2>You might also like</h2></div>
      <a class="link" href="{r}mdf-routed-doors/index.html">All profiles</a>
    </div>
    <div class="door-grid">{''.join(door_card(x, r) for x in related)}</div>
  </div>
</section>
<script>
document.querySelectorAll('.thumb').forEach(function(b){{b.addEventListener('click',function(){{
  document.querySelector('.gallery-img').src=b.dataset.src;
  document.querySelectorAll('.thumb').forEach(function(t){{t.classList.toggle('is-active',t===b)}});
}})}});
</script>
'''
    out += cta(r, 'Same door. Different light.', 'Order a sample and see it beside your benchtop, where it is actually going to live.')
    out += footer(r)
    return out




FAMILY = {
    'whites': ['lumina', 'luna-bianco', 'glacier-white'],
    'marble': ['calacatta-oro', 'calacatta-grigio', 'carrara-pietra', 'aurora-cloud', 'bruma-vagli', 'taj-sogno', 'altus-classico'],
    'concrete': ['artesian-concrete', 'ombra-concrete', 'weathered-concrete', 'pietra-urbana', 'obsidian-nuvo', 'grigio-pallazzo'],
    'warm': ['sabbia-dune', 'dune-prima', 'whisper'],
}
FAMILY_NAME = [('whites', 'Whites'), ('marble', 'Marble look'), ('concrete', 'Concrete and stone'), ('warm', 'Warm and sandy'), ('outdoor', 'Outdoor')]


def tags(s):
    t = [k for k, v in FAMILY.items() if s['slug'] in v]
    if s['outdoor']:
        t.append('outdoor')
    return ' '.join(t)


def surfaces_page():
    r = rel(1)
    outdoor = [s for s in SURF if s['outdoor']]
    counts = {k: sum(1 for s in SURF if k in tags(s).split()) for k, _ in FAMILY_NAME}
    cards = ''.join(f'<div class="fcard" data-tags="{tags(s)}">{swatch_card(s, r)}</div>' for s in SURF)
    out = head('Solid surfaces | SURFES',
               'Silica-free solid surfaces for kitchens, bathrooms, laundries and outdoors. Stain resistant, repairable and seamless, with a 10 year product warranty. Made in Australia.',
               r, 'surfes-kitchen-wide.webp')
    out += header(r, 'surf')
    out += f'''<section class="page-head">
  <div class="wrap page-head-grid">
    <div>
      <p class="eyebrow">Solid surfaces</p>
      <h1>{len(SURF)} colours.<br>Zero silica.</h1>
    </div>
    <div>
      <p class="lede">Benchtops, vanities and splashbacks made from natural minerals with no silica. Stain resistant, repairable and seamless, with a 10 year product warranty. Four colours are UV-stable for outdoor kitchens.</p>
      <div class="hero-actions">
        <a class="btn btn-clay" href="{r}contact/index.html">Order a sample</a>
        <a class="btn btn-ghost" href="#why">Why solid surface</a>
      </div>
    </div>
  </div>
</section>

<section class="range-section" id="range">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter colours">
      <button class="filter is-active" data-filter="all">All <span>{len(SURF)}</span></button>
      {''.join(f'<button class="filter" data-filter="{k}">{v} <span>{counts[k]}</span></button>' for k, v in FAMILY_NAME)}
    </div>
    <div class="swatch-grid range-grid-s" id="swatch-grid">{cards}</div>
    <p class="note range-note">Colours shown are a representation only and may vary from the actual product. Please see a physical sample before making your final selection.</p>
  </div>
</section>

<section class="wide-band">
  {img(r, "surfes-kitchen-wide.webp", "Kitchen with a pale speckled surface on the island and splashback, oak cabinetry and brass tapware")}
</section>

<section class="section" id="why">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Why solid surface</p>
      <h2>What you are actually getting.</h2>
    </div>
    <div class="why-grid">
      <div><span class="icon">{ICON['silica']}</span><h3>Zero silica</h3><p>Made from natural minerals with no silica content. A safer material for the people who cut, install and live with it.</p></div>
      <div><span class="icon">{ICON['seam']}</span><h3>Stain resistant</h3><p>A non-porous, hygienic surface that resists dirt and stains. Simple cleaning keeps it looking new, without harsh chemicals.</p></div>
      <div><span class="icon">{ICON['repair']}</span><h3>Repairable</h3><p>Accidental damage can be restored to original condition. You fix the spot, not the whole benchtop.</p></div>
      <div><span class="icon">{ICON['seam']}</span><h3>Seamless</h3><p>Pieces join into one unbroken surface for large islands. Colour and texture run through the entire thickness.</p></div>
      <div><span class="icon">{ICON['warranty']}</span><h3>10 year warranty</h3><p>Every colour carries a 10 year product warranty. Full details are in the product documentation.</p></div>
      <div><span class="icon">{ICON['local']}</span><h3>Made in Australia</h3><p>Manufactured locally by Craftmark, which means faster supply and someone to call when you need help.</p></div>
    </div>
  </div>
</section>

<section class="section section-stone" id="outdoor">
  <div class="wrap feature-split">
    <div class="feature-copy">
      <p class="eyebrow">Outdoor range</p>
      <h2>Holds its colour in the sun.</h2>
      <p class="lede">Most surfaces fade and chalk outdoors. These {len(outdoor)} colours are UV resistant, so an outdoor kitchen or alfresco bar keeps its colour for years.</p>
      <a class="btn btn-ghost" href="#range" data-jump="outdoor">Show outdoor colours</a>
    </div>
    <div class="swatch-grid two">{''.join(swatch_card(s, r) for s in outdoor)}</div>
  </div>
</section>
<script>
(function(){{var b=document.querySelectorAll('.filter'),c=document.querySelectorAll('#swatch-grid .fcard');
function go(f){{b.forEach(function(y){{y.classList.toggle('is-active',y.dataset.filter===f)}});
c.forEach(function(k){{k.hidden=!(f==='all'||k.dataset.tags.split(' ').indexOf(f)>-1)}});}}
b.forEach(function(x){{x.addEventListener('click',function(){{go(x.dataset.filter)}})}});
document.querySelectorAll('[data-jump]').forEach(function(a){{a.addEventListener('click',function(){{go(a.dataset.jump)}})}});}})();
</script>
'''
    out += cta(r)
    out += footer(r)
    return out




STUBS = {
    'trade-partners': ('Trade partners', 'trade'),
    'about': ('About', 'about'),
    'news': ('News', 'news'),
    'contact': ('Contact', ''),
}


def stub_page(path, title, active, depth):
    r = rel(depth)
    out = head(f'{title} | SURFES', 'Page in progress.', r)
    out += header(r, active)
    out += f'''<section class="section stub">
  <div class="wrap">
    <p class="eyebrow">Preview</p>
    <h1>{e(title)}</h1>
    <p class="lede">This page is being rebuilt and will be added in the next round.</p>
    <a class="btn" href="{r}index.html">Back to the homepage</a>
  </div>
</section>
'''
    out += footer(r)
    return out


PRETTY = os.environ.get('PRETTY', '1') == '1'   # clean URLs for hosting; PRETTY=0 for local file previews


def write(path, content):
    if PRETTY:
        import re
        content = re.sub(r'href="((?:\.\./)*)([^"]*?)index\.html', lambda m: 'href="' + (m.group(1) + m.group(2) or './'), content)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)


if __name__ == '__main__':
    write('index.html', home())
    for s in SURF:
        write(f'solid-surfaces/{s["slug"]}/index.html', surface_page(s))
    for k, (t, a) in STUBS.items():
        write(f'{k}/index.html', stub_page(k, t, a, 1))
    write('mdf-routed-doors/index.html', doors_page())
    write('solid-surfaces/index.html', surfaces_page())
    for d in DOORS:
        write(f'mdf-routed-doors/{d["slug"]}/index.html', door_page(d))
    print('built', 1 + len(SURF), 'pages')
