#!/usr/bin/env python3
"""Fable Tour — multilingual blog builder (20 languages).

Sources (per language code L):
  _blog/L/posts.json          article metadata (list)
  _blog/L/posts/<slug>.html   article body fragment (<p>, <h2>, <h3>, <ul>, <blockquote>…)
  _blog/i18n.json             interface strings per language
  _blog/style.css, gyg.css    shared styles
Output:
  ar  -> /blog/ ;  other L -> /L/blog/
  <blog>/index.html, <blog>/<slug>/index.html, <blog>/feed.xml
  sitemap.xml (blog block between <!-- blog:start --> and <!-- blog:end -->)

Articles about the same place share the same "topic" key in every language,
which links them together with hreflang.

Run:  python3 _blog/build.py
"""
import json, re, html, math, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "_blog"
SITE = "https://iraq.fabletour.com"
WA = "https://wa.me/9647711745353"
LANGS = ["ar", "en", "tr", "ru", "de", "fr", "es", "it", "el", "cs", "pl", "zh", "ja", "fa", "ms", "id", "th", "hi", "ur", "ta", "fi", "sv", "da", "no", "sk", "hr", "ro", "nl"]
HREFLANG = {"zh": "zh-Hans"}
OGLOC = {"ar": "ar_AR", "en": "en_US", "ru": "ru_RU", "de": "de_DE", "fr": "fr_FR", "es": "es_ES", "it": "it_IT",
         "el": "el_GR", "cs": "cs_CZ", "pl": "pl_PL", "zh": "zh_CN", "ja": "ja_JP", "tr": "tr_TR", "fa": "fa_IR",
         "ms": "ms_MY", "id": "id_ID", "th": "th_TH", "hi": "hi_IN", "ur": "ur_PK", "ta": "ta_IN",
         "fi": "fi_FI", "sv": "sv_SE", "da": "da_DK", "no": "nb_NO", "sk": "sk_SK", "hr": "hr_HR", "ro": "ro_RO", "nl": "nl_NL"}
RTL = {"ar", "fa", "ur"}
BLOGWORD = {"ar": "المدونة", "fa": "وبلاگ", "ru": "Блог", "zh": "博客", "ja": "ブログ", "th": "บล็อก", "hi": "ब्लॉग", "ur": "بلاگ", "ta": "வலைப்பதிவு", "fi": "Blogi", "sv": "Blogg", "no": "Blogg"}
AUTHOR = {"ar": "سيف التميمي", "fa": "سیف التمیمی", "ur": "سیف التمیمی", "hi": "सैफ़ अल-तमीमी", "ta": "சைஃப் அல்-தமீமி"}
AUTHOR_EN = "Saif Al-Tamimi"
T = json.loads((B / "i18n.json").read_text())
CSS = (B / "style.css").read_text() + (B / "gyg.css").read_text()

def esc(s): return html.escape(str(s), quote=True)
def hl(l): return HREFLANG.get(l, l)
def home(l): return "/" if l == "ar" else f"/{l}/"
def blog_path(l): return "/blog/" if l == "ar" else f"/{l}/blog/"
def blog_url(l): return SITE + blog_path(l)
def out_dir(l): return ROOT / blog_path(l).strip("/")
def author(l): return AUTHOR.get(l, AUTHOR_EN)
def blogword(l): return BLOGWORD.get(l, "Blog")

def fdate(l, d):
    y, m, dd = map(int, d.split("-"))
    return T[l]["date"].format(d=dd, M=T[l]["months"][m - 1], y=y)

def slugify(s):
    s = s.lower()
    for a, b in {"à":"a","á":"a","â":"a","ä":"a","è":"e","é":"e","ê":"e","ì":"i","í":"i","ò":"o","ó":"o","ô":"o","ö":"o","ù":"u","ú":"u","ü":"u","ç":"c","ñ":"n","ş":"s","ğ":"g","ı":"i","ł":"l","ś":"s","ź":"z","ż":"z","ą":"a","ę":"e","ć":"c","ń":"n","ř":"r","š":"s","č":"c","ž":"z","ý":"y","ů":"u","ě":"e","ď":"d","ť":"t","ň":"n","å":"a","æ":"ae","ø":"o","’":"","'":""}.items():
        s = s.replace(a, b)
    s = re.sub(r"[^\w]+", "-", s, flags=re.U).strip("-")
    return s or "s"

def words(l, t):
    t = re.sub(r"<[^>]+>", " ", t)
    if l in ("zh", "ja"): return len(re.sub(r"\s", "", t)) // 2      # ~2 chars per "word"
    if l == "th": return len(re.sub(r"\s", "", t)) // 5
    return len(t.split())

def src(p): return p if p.startswith("http") else "/" + p.lstrip("/")
def img_url(p): return (SITE + "/og-image.jpg") if not p else (p if p.startswith("http") else SITE + "/" + p.lstrip("/"))

def tours(l):
    f = ROOT / ("index.html" if l == "ar" else f"{l}/index.html")
    s = f.read_text()
    t = re.findall(r'<a class="pcard".*?<b class="disp">(.*?)</b>.*?<span class="ppk">(.*?)</span>', s, re.S)
    if len(t) < 2:  # programme cards were removed from the homepages: use the booking form and price box
        names = re.findall(r'<select id="f-prog"[^>]*><option value="([^"]*)">.*?<option value="([^"]*)">', s, re.S)[0]
        per = re.search(r'<div class="per">([^<]*)</div>', s).group(1)
        t = [(names[0], per), (names[1], per)]
    (n7, k7), (n9, k9) = [(html.unescape(a), html.unescape(b)) for a, b in t[:2]]
    return {"7": (n7, home(l) + "#tour-7-days", f"$2,500 {k7}"), "9": (n9, home(l) + "#tour-9-days", f"$3,400 {k9}")}

def footer(l):
    f = ROOT / ("index.html" if l == "ar" else f"{l}/index.html")
    s = f.read_text()
    a = s.rfind("<footer"); e = s.find("</footer>", a) + 9
    ft = s[a:e].replace(' aria-current="page"', "")
    def absol(m):
        h = m.group(1)
        if re.match(r"(https?:|mailto:|tel:|#|/)", h): return m.group(0)
        h = h[3:] if h.startswith("../") else h
        h = h[2:] if h.startswith("./") else h
        return f'href="/{h}"'
    ft = re.sub(r'href="([^"]*)"', absol, ft)
    # language links in the footer point to that language's blog
    def langnav(m):
        x = re.sub(r'href="/([a-z]{2})/"', lambda n: f'href="/{n.group(1)}/blog/"', m.group(0))
        return x.replace('href="/"', 'href="/blog/"')
    return re.sub(r'<nav class="langs".*?</nav>', langnav, ft, flags=re.S)

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=PT+Serif:wght@400;700&family=Inter+Tight:wght@400;500;600{extra}&display=swap" rel="stylesheet">')
FONT_EXTRA = {"ar": "&family=Amiri:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600",
              "fa": "&family=Amiri:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600",
              "zh": "&family=Noto+Serif+SC:wght@600", "ja": "&family=Noto+Serif+JP:wght@600",
              "hi": "&family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Serif+Devanagari:wght@600",
              "ta": "&family=Noto+Sans+Tamil:wght@400;500;600&family=Noto+Serif+Tamil:wght@600",
              "ur": "&family=Noto+Nastaliq+Urdu:wght@400;700&family=Noto+Naskh+Arabic:wght@400;600"}

ORG = {"@type": "TravelAgency", "@id": "https://fabletour.com/#org", "name": "Fable Tour", "url": "https://fabletour.com",
       "logo": SITE + "/logo.png", "email": "support@fabletour.com", "telephone": "+9647711745353"}

def head(l, title, desc, canonical, alts, og_type, image, image_alt, extra_meta="", jsonld=None, keywords=""):
    t = T[l]
    ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>" if jsonld else ""
    kw = f'<meta name="keywords" content="{esc(keywords)}">\n' if keywords else ""
    alt_links = "".join(f'<link rel="alternate" hreflang="{hl(a)}" href="{u}">\n' for a, u in alts)
    if alts:
        xd = dict(alts).get("en") or dict(alts).get(l)
        alt_links += f'<link rel="alternate" hreflang="x-default" href="{xd}">\n'
    ogalt = "".join(f'<meta property="og:locale:alternate" content="{OGLOC[a]}">\n' for a, _ in alts if a != l)
    d = "rtl" if l in RTL else "ltr"
    return f"""<!DOCTYPE html>
<html lang="{hl(l)}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{kw}<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="{esc(author(l))} — Fable Tour">
<meta name="theme-color" content="#1B2A47">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{canonical}">
{alt_links}<link rel="alternate" type="application/rss+xml" title="Fable Tour — {esc(blogword(l))}" href="{blog_url(l)}feed.xml">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Fable Tour">
<meta property="og:locale" content="{OGLOC[l]}">
{ogalt}<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{esc(image)}">
<meta property="og:image:alt" content="{esc(image_alt)}">
{extra_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(image)}">
{FONTS.format(extra=FONT_EXTRA.get(l, ""))}
{ld}
<style>{CSS}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="ftmark" viewBox="0 0 48 48"><image href="/logo.png" width="48" height="48"/></symbol></svg>
<div class="card">
<header class="topbar"><div class="wrap">
  <a class="logo" href="{home(l)}"><svg><use href="#ftmark"/></svg><b>Fable Tour</b></a>
  <nav class="nav" aria-label="Menu"><a href="{home(l)}">{esc(t["tours"])}</a><a href="{blog_path(l)}" aria-current="page">{esc(blogword(l))}</a><a class="hide-s" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></nav>
</div></header>
"""

def tail(l):
    return footer(l) + f"""
</div>
<a class="wa-fab" href="{WA}?text={esc(T[l]['wa_hello'])}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_ICON}</a>
</body>
</html>
"""

def card(l, p, cls="pc"):
    style = f' style="background-image:url(\'{esc(src(p["image"]))}\')"' if p.get("image") else ""
    noimg = "" if p.get("image") else " ph-none"
    return (f'<a class="{cls}" href="{blog_path(l)}{p["slug"]}/" data-cat="{esc(p["category"])}">'
            f'<div class="ph{noimg}"{style}><span>{esc(p["category"])}</span></div>'
            f'<div class="bd"><h3>{esc(p["h1"])}</h3><p>{esc(p["excerpt"])}</p>'
            f'<small>{fdate(l, p["date"])} · {T[l]["min"].format(n=p["_min"])}</small></div></a>')

def article_alts(p, ALL):
    """[(lang, url)] for every language that has an article with the same topic."""
    out = []
    for l2 in LANGS:
        for q in ALL.get(l2, []):
            if q.get("topic") and q.get("topic") == p.get("topic"):
                out.append((l2, blog_url(l2) + q["slug"] + "/")); break
    return out

def build_article(l, p, posts, ALL, TOURS):
    t = T[l]
    body = (B / l / "posts" / f'{p["slug"]}.html').read_text()
    toc = []
    def add_id(m):
        attrs, text = m.group(1), m.group(2)
        if "id=" in attrs:
            i = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            i = "s" + str(len(toc) + 1) + "-" + slugify(re.sub(r"<[^>]+>", "", text))[:50]
            attrs += f' id="{i}"'
        toc.append((i, re.sub(r"<[^>]+>", "", text)))
        return f"<h2{attrs}>{text}</h2>"
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, body, flags=re.S)
    url = blog_url(l) + p["slug"] + "/"
    image = img_url(p.get("image"))
    alt = p.get("image_alt", p["h1"])
    place = p.get("place", p["h1"])
    facts = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in p.get("facts", []))
    faq = p.get("faq", [])
    tour = TOURS[p.get("tour", "7")]
    related = [x for x in reversed(posts) if x["slug"] != p["slug"]]
    same = [x for x in related if x["category"] == p["category"]]
    rel = (same + [x for x in related if x not in same])[:3]
    alts = article_alts(p, ALL)
    graph = [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": p["h1"][:110], "name": p["title"],
         "description": p["description"], "inLanguage": hl(l),
         "datePublished": p["date"] + "T08:00:00+03:00", "dateModified": p.get("updated", p["date"]) + "T08:00:00+03:00",
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
         "image": {"@type": "ImageObject", "url": image}, "wordCount": p["_words"], "articleSection": p["category"],
         "keywords": p.get("keywords", ""),
         "author": {"@type": "Person", "name": author(l), "alternateName": AUTHOR_EN, "jobTitle": t["guide_job"], "image": "https://iraq.fabletour.com/img/saif-avatar.webp",
                    "worksFor": {"@id": "https://fabletour.com/#org"}, "knowsLanguage": ["ar", "en", "ru"]},
         "publisher": ORG, "isPartOf": {"@id": blog_url(l) + "#blog"},
         "about": {"@type": "TouristAttraction", "name": place,
                   **({"geo": {"@type": "GeoCoordinates", "latitude": p["geo"][0], "longitude": p["geo"][1]}} if p.get("geo") else {}),
                   "address": {"@type": "PostalAddress", "addressCountry": "IQ", "addressRegion": p.get("region", "")}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home_crumb"], "item": SITE + home(l)},
            {"@type": "ListItem", "position": 2, "name": blogword(l), "item": blog_url(l)},
            {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url}]},
    ]
    if faq:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    extra = (f'<meta property="article:published_time" content="{p["date"]}T08:00:00+03:00">\n'
             f'<meta property="article:modified_time" content="{p.get("updated", p["date"])}T08:00:00+03:00">\n'
             f'<meta property="article:author" content="{esc(author(l))}">\n'
             f'<meta property="article:section" content="{esc(p["category"])}">\n')
    for kw in [k.strip() for k in re.split(r"[,،、，]", p.get("keywords", "")) if k.strip()][:6]:
        extra += f'<meta property="article:tag" content="{esc(kw)}">\n'
    h = head(l, p["title"], p["description"], url, alts, "article", image, alt, extra,
             {"@context": "https://schema.org", "@graph": graph}, p.get("keywords", ""))
    hero_img = ""
    if p.get("image"):
        hero_img = (f'<img class="hero-img" src="{esc(src(p["image"]))}" alt="{esc(alt)}" width="1600" height="800" fetchpriority="high" decoding="async">'
)
    toc_html = ""
    if len(toc) >= 3:
        toc_html = f'<nav class="toc" aria-label="{esc(t["toc"])}"><b>{esc(t["toc"])}</b><ol>' + "".join(
            f'<li><a href="#{i}">{esc(x)}</a></li>' for i, x in toc) + "</ol></nav>"
    faq_html = ""
    if faq:
        faq_html = f'<section class="faq" id="faq"><h2>{esc(t["faq"])}</h2>' + "".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</section>"
    rel_html = ""
    if rel:
        rel_html = (f'<section class="block in" style="padding-top:8px"><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">{esc(t["more_eye"])}</span><h2>{esc(t["more_h"])}</h2></div>'
                    '<div class="grid">' + "".join(card(l, x) for x in rel) + "</div></section>")
    wa_msg = esc(t["wa_art"].format(t=p["h1"]))
    cta_p = esc(t["cta_p"]).replace("{tour}", f'<a href="{tour[1]}" style="color:var(--gold-2)">{esc(tour[0])}</a>').replace("{price}", esc(tour[2]))
    brief = f'<section class="facts" aria-label="{esc(t["brief"])}"><h2>{esc(t["brief"])}</h2><dl>{facts}</dl></section>' if facts else ""
    out = h + f"""
<div class="in crumbs"><ol><li><a href="{home(l)}">{esc(t["home_crumb"])}</a></li><li><a href="{blog_path(l)}">{esc(blogword(l))}</a></li><li aria-current="page">{esc(place)}</li></ol></div>
<main>
<section class="hero">
  <div class="hero-band in" style="margin-top:14px">
    <span class="eyebrow">{esc(p["category"])} · {esc(p.get("region", "Iraq"))}</span>
    <h1>{esc(p["h1"])}</h1>
    <p>{esc(p["excerpt"])}</p>
    <div class="meta"><span>{esc(t["by"])} <b>{esc(author(l))}</b>, {esc(t["role"])}</span><span><time datetime="{p["date"]}">{fdate(l, p["date"])}</time></span><span>{t["min"].format(n=p["_min"])}</span></div>
  </div>
  {hero_img}
</section>
<article class="post in">
  <div class="prose">
    {brief}
    {toc_html}
    {body}
    <aside class="cta">
      <span class="eyebrow">{esc(t["cta_eye"])}</span>
      <h2>{esc(t["cta_h"].format(place=place))}</h2>
      <p>{cta_p}</p>
      <div class="btns"><a class="btn" href="{WA}?text={wa_msg}" target="_blank" rel="noopener">{WA_ICON.replace('<svg ', '<svg width="18" height="18" ')} {esc(t["wa_btn"])}</a><a class="btn ghost" href="{tour[1]}">{esc(t["see_prog"])}</a></div>
    </aside>
    {faq_html}
    <div class="author"><img src="/img/saif-avatar.webp" alt="{esc(author(l))} — Fable Tour Iraq" width="88" height="88" loading="lazy"><p><b>{esc(author(l))}</b> {esc(t["bio"])}</p></div>
  </div>
</article>
{rel_html}
</main>
""" + tail(l)
    d = out_dir(l) / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out)

def build_index(l, posts):
    t = T[l]
    ordered = list(reversed(posts))
    cats = sorted({p["category"] for p in posts})
    url = blog_url(l)
    alts = [(x, blog_url(x)) for x in LANGS]
    graph = [
        {"@type": "Blog", "@id": url + "#blog", "url": url, "name": t["b_title"].split(" | ")[0],
         "description": t["b_desc"], "inLanguage": hl(l), "publisher": ORG,
         "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": url + p["slug"] + "/",
                       "datePublished": p["date"], "image": img_url(p.get("image"))} for p in ordered[:30]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home_crumb"], "item": SITE + home(l)},
            {"@type": "ListItem", "position": 2, "name": blogword(l), "item": url}]},
    ]
    h = head(l, t["b_title"], t["b_desc"], url, alts, "website", SITE + "/og-image.jpg", "Fable Tour", "",
             {"@context": "https://schema.org", "@graph": graph}, t["b_kw"])
    feat, rest = "", ordered
    if ordered:
        p = ordered[0]; rest = ordered[1:]
        style = f' style="background-image:url(\'{esc(src(p["image"]))}\')"' if p.get("image") else ""
        noimg = "" if p.get("image") else " ph-none"
        feat = (f'<a class="featured" href="{blog_path(l)}{p["slug"]}/"><div class="ph{noimg}"{style}></div><div class="bd">'
                f'<span class="eyebrow">{esc(t["latest"])} · {esc(p["category"])}</span><h2>{esc(p["h1"])}</h2><p>{esc(p["excerpt"])}</p>'
                f'<small style="color:var(--muted);font-size:13px">{fdate(l, p["date"])} · {t["min"].format(n=p["_min"])}</small></div></a>')
    else:
        feat = f'<p style="color:var(--muted)">{esc(t["empty"])}</p>'
    chips = ""
    if len(cats) > 1 and len(rest) > 2:
        chips = (f'<div class="chips" role="group" aria-label="{esc(t["filter"])}"><button aria-pressed="true" data-f="*">{esc(t["all"])}</button>'
                 + "".join(f'<button aria-pressed="false" data-f="{esc(c)}">{esc(c)}</button>' for c in cats) + "</div>")
    grid = '<div class="grid" id="posts">' + "".join(card(l, p) for p in rest) + "</div>" if rest else ""
    script = """<script>(function(){var b=document.querySelectorAll('.chips button'),c=document.querySelectorAll('#posts .pc');b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.setAttribute('aria-pressed',y===x)});var f=x.dataset.f;c.forEach(function(k){k.hidden=!(f==='*'||k.dataset.cat===f)})})})})();</script>"""
    out = h + f"""
<main>
<section class="hero"><div class="hero-band in">
  <span class="eyebrow">{esc(t["b_eye"])}</span>
  <h1>{esc(t["b_h1"])}</h1>
  <p>{esc(t["b_lead"])}</p>
</div></section>
<section class="block in">
  {feat}
  {chips}
  {grid}
</section>
<section class="in"><aside class="cta" style="margin-top:0">
  <span class="eyebrow">{esc(t["c2_eye"])}</span>
  <h2>{esc(t["c2_h"])}</h2>
  <p>{esc(t["c2_p"])}</p>
  <div class="btns"><a class="btn" href="{home(l)}">{esc(t["c2_btn"])}</a><a class="btn ghost" href="{WA}?text={esc(t['wa_hello'])}" target="_blank" rel="noopener">WhatsApp</a></div>
</aside></section>
</main>
{script if chips else ""}
""" + tail(l)
    out_dir(l).mkdir(parents=True, exist_ok=True)
    (out_dir(l) / "index.html").write_text(out)

def build_feed(l, posts):
    items = ""
    for p in list(reversed(posts))[:30]:
        dt = datetime.datetime.strptime(p["date"], "%Y-%m-%d").replace(hour=8, tzinfo=datetime.timezone(datetime.timedelta(hours=3)))
        u = blog_url(l) + p["slug"] + "/"
        items += (f"<item><title>{esc(p['h1'])}</title><link>{u}</link><guid>{u}</guid>"
                  f"<pubDate>{dt.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate><category>{esc(p['category'])}</category>"
                  f"<description>{esc(p['description'])}</description></item>")
    (out_dir(l) / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Fable Tour — {esc(T[l]['b_h1'])}</title><link>{blog_url(l)}</link>
<description>{esc(T[l]['b_desc'])}</description><language>{hl(l).lower()}</language>{items}</channel></rss>
""")

def build_sitemap(ALL):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    s = re.sub(r"\s*<!-- blog(-it)?:start -->.*?<!-- blog(-it)?:end -->", "", s, flags=re.S)
    today = datetime.date.today().isoformat()
    e = "\n  <!-- blog:start -->"
    idx_alts = "".join(f'<xhtml:link rel="alternate" hreflang="{hl(x)}" href="{blog_url(x)}"/>' for x in LANGS)
    for l in LANGS:
        posts = ALL.get(l, [])
        last = max([p.get("updated", p["date"]) for p in posts] or [today])
        e += f"\n  <url><loc>{blog_url(l)}</loc><lastmod>{last}</lastmod><changefreq>daily</changefreq><priority>0.7</priority>{idx_alts}</url>"
        for p in posts:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{hl(a)}" href="{u}"/>' for a, u in article_alts(p, ALL))
            img = f"<image:image><image:loc>{esc(img_url(p['image']))}</image:loc></image:image>" if p.get("image") else ""
            e += f"\n  <url><loc>{blog_url(l)}{p['slug']}/</loc><lastmod>{p.get('updated', p['date'])}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>{alts}{img}</url>"
    e += "\n  <!-- blog:end -->"
    if "xmlns:image=" not in s:
        s = s.replace("<urlset ", '<urlset xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" ', 1)
    s = s.replace("</urlset>", e + "\n</urlset>")
    sm.write_text(s)

def load(l):
    f = B / l / "posts.json"
    if not f.exists(): return []
    posts = json.loads(f.read_text())
    posts.sort(key=lambda p: p["date"])
    seen = set()
    for p in posts:
        assert p["slug"] not in seen, f"duplicate slug {l}/{p['slug']}"; seen.add(p["slug"])
        assert re.fullmatch(r"[a-z0-9-]+", p["slug"]), f"slug must be ascii a-z0-9-: {l}/{p['slug']}"
        body = (B / l / "posts" / f'{p["slug"]}.html').read_text()
        p["_words"] = words(l, body) + sum(words(l, q + " " + a) for q, a in p.get("faq", []))
        p["_min"] = max(1, math.ceil(p["_words"] / 220))
        if len(p["title"]) > 70: print(f"WARN {l}/{p['slug']}: title {len(p['title'])} chars (keep ≤ 65)")
        dl = len(p["description"])
        if not ((60 if l in ('zh', 'ja', 'th') else 110) <= dl <= 165): print(f"WARN {l}/{p['slug']}: description {dl} chars")
    return posts

def main():
    ALL = {l: load(l) for l in LANGS}
    for l in LANGS:
        TOURS = tours(l)
        for p in ALL[l]:
            build_article(l, p, ALL[l], ALL, TOURS)
        build_index(l, ALL[l])
        build_feed(l, ALL[l])
    build_sitemap(ALL)
    print("Built:", ", ".join(f"{l}={len(ALL[l])}" for l in LANGS))

if __name__ == "__main__":
    main()
    # footer links to the other Fable Tour sites (+ their CSS) on the freshly built blog pages
    import sys; sys.path.insert(0, str(pathlib.Path(__file__).parent / "tools"))
    import footer_sites; footer_sites.run()
