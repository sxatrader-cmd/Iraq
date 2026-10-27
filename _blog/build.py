#!/usr/bin/env python3
"""Fable Tour — Italian blog builder.

Sources:   _blog/it/posts.json            (article metadata, newest last)
           _blog/it/posts/<slug>.html     (article body fragment: <p>, <h2>, <h3>, <ul>, <figure>…)
Output:    it/blog/index.html             (blog home, static, SEO)
           it/blog/<slug>/index.html      (one page per article)
           it/blog/feed.xml               (RSS)
           sitemap.xml                    (blog URLs refreshed inside the existing sitemap)

Run:  python3 _blog/build.py
"""
import json, re, html, math, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_blog" / "it"
OUT = ROOT / "it" / "blog"
SITE = "https://iraq.fabletour.com"
BASE = SITE + "/it/blog/"
WA = "https://wa.me/9647711745353"
AUTHOR = "Saif Al-Tamimi"

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]

def it_date(d):
    y, m, dd = map(int, d.split("-"))
    return f"{dd} {MESI[m-1]} {y}"

def esc(s):
    return html.escape(s, quote=True)

def slugify(s):
    s = s.lower()
    for a, b in {"à":"a","á":"a","è":"e","é":"e","ì":"i","í":"i","ò":"o","ó":"o","ù":"u","ú":"u","’":"","'":""}.items():
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def words(t):
    return len(re.sub(r"<[^>]+>", " ", t).split())

GYG = (SRC / "gyg.css").read_text()
FOOTER = (SRC / "footer.html").read_text()

CSS = """
:root{--navy:#1B2A47;--navy-2:#2A3C5F;--gold:#B8955A;--gold-2:#D9C08E;--ground:#EEE6D8;--paper:#FCFAF6;--panel:#F4EEE3;--ink:#22262E;--muted:#5F6672;--line:#E6DDCC;
--serif:"Libre Baskerville","PT Serif",Georgia,"Times New Roman",serif;--sans:"Inter Tight","Helvetica Neue",Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.75;-webkit-font-smoothing:antialiased;padding:24px max(12px,env(safe-area-inset-right,0px)) 24px max(12px,env(safe-area-inset-left,0px))}
img{max-width:100%;height:auto;display:block}
a{color:var(--navy-2)}
:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
h1,h2,h3{text-wrap:balance;margin:0;font-family:var(--serif);font-weight:400;color:var(--navy)}
.card{max-width:880px;margin:0 auto;background:var(--paper);border-radius:6px;overflow:hidden;box-shadow:0 2px 24px -12px rgba(27,42,71,.35)}
.wrap,.in{padding-left:clamp(18px,5vw,44px);padding-right:clamp(18px,5vw,44px)}
.eyebrow{display:block;font:500 12.5px var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.topbar{background:var(--navy);color:#fff;position:sticky;top:0;z-index:20}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-block:16px}
.logo{display:flex;align-items:center;gap:14px;color:#fff;text-decoration:none}
.logo svg{width:52px;height:52px;flex:none;border-radius:50%;background:#fff;box-shadow:0 0 0 3px var(--gold)}
.logo b{font-family:var(--serif);font-size:21px;letter-spacing:.16em;font-weight:700;color:#EFE3C8;text-transform:uppercase;white-space:nowrap}
.nav{display:flex;gap:6px;align-items:center}
.nav a{color:#EFE3C8;text-decoration:none;font:600 13px var(--sans);letter-spacing:.06em;padding:8px 12px;border:1px solid rgba(217,192,142,.45);border-radius:4px;white-space:nowrap}
.nav a:hover,.nav a[aria-current]{background:var(--gold);color:var(--navy);border-color:var(--gold)}
.crumbs{font-size:13px;color:var(--muted);padding-top:18px}
.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.crumbs li+li::before{content:"›";margin-inline-end:6px;color:var(--gold)}
.crumbs a{color:var(--muted)}
.hero-band{background:var(--navy);color:#fff;border-bottom:5px solid var(--gold);padding-block:34px 32px;position:relative;overflow:hidden}
.hero-band::after{content:"";position:absolute;inset:0;opacity:.09;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'%3E%3Cg fill='none' stroke='%23D9C08E' stroke-width='1.4'%3E%3Cpath d='M28 4 52 28 28 52 4 28z'/%3E%3Ccircle cx='28' cy='28' r='7'/%3E%3C/g%3E%3C/svg%3E")}
.hero-band>*{position:relative;z-index:1}
.hero-band h1{color:#fff;font-size:clamp(28px,5vw,42px);line-height:1.22;margin:10px 0 14px}
.hero-band p{margin:0;color:#D9DEE6;max-width:62ch;font-size:16.5px}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:18px;font-size:13.5px;color:#C9CFD9}
.meta b{color:var(--gold-2);font-weight:600}
.hero-img{width:100%;aspect-ratio:16/8;object-fit:cover;background:var(--navy-2)}
.figcap{font-size:12.5px;color:var(--muted);padding:6px clamp(18px,5vw,44px) 0}
article.post{padding-block:28px 8px}
.prose{max-width:68ch}
.prose p{margin:0 0 16px}
.prose h2{font-size:clamp(23px,3.6vw,29px);line-height:1.3;margin:38px 0 12px;scroll-margin-top:100px}
.prose h3{font-size:20px;margin:26px 0 8px}
.prose ul,.prose ol{padding-inline-start:22px;margin:0 0 16px}
.prose li{margin-bottom:6px}
.prose blockquote{margin:22px 0;padding:14px 20px;border-inline-start:4px solid var(--gold);background:var(--panel);font-family:var(--serif);color:var(--navy);font-size:17px}
.prose figure{margin:22px 0}.prose figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.lead{font-size:19px;line-height:1.65;color:#343a45}
.facts{background:var(--panel);border-radius:6px;padding:18px 22px;margin:6px 0 26px;border-top:4px solid var(--gold)}
.facts h2{font-size:18px!important;margin:0 0 10px!important}
.facts dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0;font-size:15px}
.facts dt{color:var(--muted);font-weight:500}.facts dd{margin:0}
.toc{border:1px solid var(--line);border-radius:6px;padding:14px 20px;margin:0 0 26px;font-size:15px}
.toc b{font-family:var(--serif);font-weight:400;color:var(--navy)}
.toc ol{margin:8px 0 0;padding-inline-start:20px}.toc li{margin:3px 0}
.cta{background:var(--navy);color:#fff;border-radius:6px;padding:24px;margin:34px 0;border-bottom:5px solid var(--gold)}
.cta h2{color:#fff!important;font-size:24px!important;margin:6px 0 8px!important}
.cta p{color:#D9DEE6;margin:0 0 16px}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font:600 14.5px var(--sans);padding:12px 18px;border-radius:4px;background:var(--gold);color:var(--navy)}
.btn.ghost{background:transparent;color:#EFE3C8;border:1px solid rgba(217,192,142,.6)}
.faq details{border-bottom:1px solid var(--line);padding:12px 0}
.faq summary{cursor:pointer;font-weight:600;color:var(--navy);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq summary::-webkit-details-marker{display:none}
.faq p{margin:10px 0 0;color:#3a404b}
.author{display:flex;gap:16px;align-items:center;background:var(--panel);border-radius:6px;padding:18px;margin:30px 0 8px;font-size:15px}
.author svg{width:56px;height:56px;flex:none;border-radius:50%;background:#fff;box-shadow:0 0 0 2px var(--gold)}
.author p{margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.pc{display:flex;flex-direction:column;background:var(--paper);border:1px solid var(--line);border-radius:6px;overflow:hidden;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s}
.pc:hover{box-shadow:0 10px 26px -14px rgba(27,42,71,.45);transform:translateY(-2px)}
.pc .ph{aspect-ratio:16/9;background:var(--navy) center/cover no-repeat;position:relative}
.ph.ph-none{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'%3E%3Cg fill='none' stroke='%23B8955A' stroke-width='1.2' opacity='.35'%3E%3Cpath d='M28 4 52 28 28 52 4 28z'/%3E%3Ccircle cx='28' cy='28' r='7'/%3E%3C/g%3E%3C/svg%3E")}
.pc .ph span{position:absolute;inset-inline-start:12px;bottom:10px;background:var(--gold);color:var(--navy);font:600 11px var(--sans);letter-spacing:.12em;text-transform:uppercase;padding:4px 8px;border-radius:3px}
.pc .bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.pc h3{font-size:18.5px;line-height:1.35}
.pc p{margin:0;font-size:14.5px;color:var(--muted);line-height:1.55}
.pc small{margin-top:auto;font-size:12.5px;color:var(--muted)}
.featured{display:grid;grid-template-columns:1.15fr 1fr;border:1px solid var(--line);border-radius:6px;overflow:hidden;text-decoration:none;color:inherit;margin-bottom:22px;background:var(--paper)}
.featured .ph{min-height:240px;background:var(--navy) center/cover no-repeat}
.featured .bd{padding:22px;display:flex;flex-direction:column;gap:10px;justify-content:center}
.featured h2{font-size:clamp(22px,3.4vw,28px);line-height:1.3}
.featured p{margin:0;color:var(--muted);font-size:15.5px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}
.chips button{font:600 13px var(--sans);border:1px solid var(--line);background:var(--paper);color:var(--navy);padding:7px 12px;border-radius:999px;cursor:pointer}
.chips button[aria-pressed="true"]{background:var(--navy);color:#EFE3C8;border-color:var(--navy)}
section.block{padding-block:30px}
.sec-head h2{font-size:clamp(23px,3.6vw,29px)}
footer{background:var(--navy);color:#C9CFD9;font-size:14px;border-top:5px solid var(--gold);margin-top:34px}
footer .wrap{padding-block:22px;display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:center}
footer a{color:var(--gold-2);text-decoration:none}
footer .logo svg{width:30px;height:30px}
.social{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.social span{font-size:13px;color:#C9CFD9;margin-inline-end:4px}
.social a{width:40px;height:40px;border-radius:50%;border:1px solid rgba(217,192,142,.55);display:grid;place-items:center;color:var(--gold-2)}
.social a:hover{background:var(--gold);color:var(--navy)}
.social svg{width:19px;height:19px}
.social a .gyg-ic{color:inherit;margin:0;font-size:0}
.langs{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px}
.addr{display:inline-flex;align-items:center;gap:8px;color:#C9CFD9!important;font-size:14px}
.addr svg{color:var(--gold-2);flex:none}
.wa-fab{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));z-index:30;width:56px;height:56px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 8px 22px -6px rgba(0,0,0,.4)}
.wa-fab svg{width:30px;height:30px;color:#fff}
@media (max-width:760px){body{padding:0}.card{border-radius:0}.logo svg{width:42px;height:42px}.logo b{font-size:15px;letter-spacing:.12em}.nav a{padding:7px 9px;font-size:12px}.nav .hide-s{display:none}.featured{grid-template-columns:1fr}.featured .ph{min-height:190px}.facts dl{grid-template-columns:1fr;gap:0}.facts dd{margin-bottom:8px}}
@media print{.topbar,.wa-fab,.cta,footer{display:none}body{background:#fff;padding:0}.card{box-shadow:none}}
""" + GYG

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">')

WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'

def head(title, desc, canonical, og_type, image, image_alt, extra_meta="", jsonld=None, keywords=""):
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    kw = f'<meta name="keywords" content="{esc(keywords)}">\n' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{kw}<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="{AUTHOR} — Fable Tour">
<meta name="theme-color" content="#1B2A47">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="it" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="Blog Fable Tour — Iraq" href="{BASE}feed.xml">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Fable Tour">
<meta property="og:locale" content="it_IT">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{esc(image_alt)}">
{extra_meta}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
{FONTS}
{ld}
<style>{CSS}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="ftmark" viewBox="0 0 48 48"><image href="/logo.png" width="48" height="48"/></symbol></svg>
<div class="card">
<header class="topbar"><div class="wrap">
  <a class="logo" href="/it/"><svg><use href="#ftmark"/></svg><b>Fable Tour</b></a>
  <nav class="nav" aria-label="Menu"><a href="/it/">Tour</a><a href="/it/blog/" {{BLOGCUR}}>Blog</a><a class="hide-s" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></nav>
</div></header>
"""

def tail():
    return FOOTER + f"""
</div>
<a class="wa-fab" href="{WA}?text={esc('Ciao! Vorrei informazioni sui tour in Iraq.')}" target="_blank" rel="noopener" aria-label="Scrivici su WhatsApp">{WA_ICON}</a>
</body>
</html>
"""

ORG = {"@type": "TravelAgency", "@id": "https://fabletour.com/#org", "name": "Fable Tour",
       "url": "https://fabletour.com", "logo": SITE + "/logo.png", "email": "support@fabletour.com",
       "telephone": "+9647711745353"}

def src(p):
    return p if p.startswith("http") else "/" + p.lstrip("/")

def img_url(p):
    if not p: return SITE + "/og-image.jpg"
    return p if p.startswith("http") else SITE + "/" + p.lstrip("/")

def card(p, cls="pc"):
    style = f' style="background-image:url(\'{src(p["image"])}\')"' if p.get("image") else ""
    noimg = "" if p.get("image") else " ph-none"
    return (f'<a class="{cls}" href="/it/blog/{p["slug"]}/" data-cat="{esc(p["category"])}">'
            f'<div class="ph{noimg}"{style}><span>{esc(p["category"])}</span></div>'
            f'<div class="bd"><h3>{esc(p["h1"])}</h3><p>{esc(p["excerpt"])}</p>'
            f'<small>{it_date(p["date"])} · {p["_min"]} min di lettura</small></div></a>')

def build_article(p, posts):
    body = (SRC / "posts" / f'{p["slug"]}.html').read_text()
    # ids for h2 + table of contents
    toc = []
    def add_id(m):
        attrs, text = m.group(1), m.group(2)
        if "id=" in attrs:
            i = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            i = slugify(re.sub(r"<[^>]+>", "", text))[:60]
            attrs += f' id="{i}"'
        toc.append((i, re.sub(r"<[^>]+>", "", text)))
        return f"<h2{attrs}>{text}</h2>"
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, body, flags=re.S)
    url = BASE + p["slug"] + "/"
    image = img_url(p.get("image"))
    alt = p.get("image_alt", p["h1"])
    facts = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in p.get("facts", []))
    faq = p.get("faq", [])
    tour = p.get("tour", "7")
    tour_txt = {"7": ("Tour del patrimonio dell'Iraq — 7 giorni", "/it/#tour-7-days", "da $2,500 a persona"),
                "9": ("Tutto l'Iraq, da Bassora a Erbil — 9 giorni", "/it/#tour-9-days", "$3,400 a persona")}[tour]
    related = [x for x in reversed(posts) if x["slug"] != p["slug"]]
    same = [x for x in related if x["category"] == p["category"]]
    rel = (same + [x for x in related if x not in same])[:3]

    graph = [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": p["h1"][:110],
         "name": p["title"], "description": p["description"], "inLanguage": "it-IT",
         "datePublished": p["date"] + "T08:00:00+03:00",
         "dateModified": p.get("updated", p["date"]) + "T08:00:00+03:00",
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
         "image": {"@type": "ImageObject", "url": image},
         "wordCount": p["_words"], "articleSection": p["category"],
         "keywords": p.get("keywords", ""),
         "author": {"@type": "Person", "name": AUTHOR, "jobTitle": "Guida turistica in Iraq",
                    "worksFor": {"@id": "https://fabletour.com/#org"}, "knowsLanguage": ["ar", "en", "ru"]},
         "publisher": ORG, "isPartOf": {"@id": BASE + "#blog"},
         "about": {"@type": "TouristAttraction", "name": p.get("place", p["h1"]),
                   **({"geo": {"@type": "GeoCoordinates", "latitude": p["geo"][0], "longitude": p["geo"][1]}} if p.get("geo") else {}),
                   "address": {"@type": "PostalAddress", "addressCountry": "IQ", "addressRegion": p.get("region", "")}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Fable Tour Iraq", "item": SITE + "/it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE},
            {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url}]},
    ]
    if faq:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    extra = (f'<meta property="article:published_time" content="{p["date"]}T08:00:00+03:00">\n'
             f'<meta property="article:modified_time" content="{p.get("updated", p["date"])}T08:00:00+03:00">\n'
             f'<meta property="article:author" content="{AUTHOR}">\n'
             f'<meta property="article:section" content="{esc(p["category"])}">\n')
    for t in [k.strip() for k in p.get("keywords", "").split(",") if k.strip()][:6]:
        extra += f'<meta property="article:tag" content="{esc(t)}">\n'

    h = head(p["title"], p["description"], url, "article", image, alt, extra,
             {"@context": "https://schema.org", "@graph": graph}, p.get("keywords", "")).replace("{BLOGCUR}", 'aria-current="page"')
    hero_img = ""
    if p.get("image"):
        hero_img = (f'<img class="hero-img" src="{esc(src(p["image"]))}" alt="{esc(alt)}" width="1600" height="800" fetchpriority="high" decoding="async">'
                    + (f'<div class="figcap">{esc(p["image_credit"])}</div>' if p.get("image_credit") else ""))
    toc_html = ""
    if len(toc) >= 3:
        toc_html = '<nav class="toc" aria-label="Indice"><b>In questo articolo</b><ol>' + "".join(
            f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ol></nav>"
    faq_html = ""
    if faq:
        faq_html = '<section class="faq" id="faq"><h2>Domande frequenti</h2>' + "".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq) + "</section>"
    rel_html = ""
    if rel:
        rel_html = ('<section class="block in" style="padding-top:8px"><div class="sec-head" style="margin-bottom:16px"><span class="eyebrow">Continua a leggere</span><h2>Altri luoghi dell\'Iraq</h2></div>'
                    '<div class="grid">' + "".join(card(x) for x in rel) + "</div></section>")
    wa_msg = esc(f"Ciao! Ho letto l'articolo «{p['h1']}» e vorrei informazioni sul tour.")
    out = h + f"""
<div class="in crumbs"><ol><li><a href="/it/">Tour in Iraq</a></li><li><a href="/it/blog/">Blog</a></li><li aria-current="page">{esc(p.get("place", p["h1"]))}</li></ol></div>
<main>
<section class="hero">
  <div class="hero-band in" style="margin-top:14px">
    <span class="eyebrow">{esc(p["category"])} · {esc(p.get("region", "Iraq"))}</span>
    <h1>{esc(p["h1"])}</h1>
    <p>{esc(p["excerpt"])}</p>
    <div class="meta"><span>Di <b>{AUTHOR}</b>, guida Fable Tour</span><span><time datetime="{p["date"]}">{it_date(p["date"])}</time></span><span>{p["_min"]} min di lettura</span></div>
  </div>
  {hero_img}
</section>
<article class="post in">
  <div class="prose">
    {'<section class="facts" aria-label="In breve"><h2>In breve</h2><dl>' + facts + '</dl></section>' if facts else ''}
    {toc_html}
    {body}
    <aside class="cta">
      <span class="eyebrow">Viaggia con noi</span>
      <h2>Visita {esc(p.get("place", "questo luogo"))} con una guida locale</h2>
      <p>Questo luogo fa parte del nostro <a href="{tour_txt[1]}" style="color:var(--gold-2)">{esc(tour_txt[0])}</a> ({tour_txt[2]}, camera doppia). Tour privati, nella data che scegli tu, con hotel 4★–5★.</p>
      <div class="btns"><a class="btn" href="{WA}?text={wa_msg}" target="_blank" rel="noopener">{WA_ICON.replace('<svg ', '<svg width="18" height="18" ')} Scrivici su WhatsApp</a><a class="btn ghost" href="{tour_txt[1]}">Vedi il programma →</a></div>
    </aside>
    {faq_html}
    <div class="author"><svg><use href="#ftmark"/></svg><p><b>{AUTHOR}</b> è una guida turistica di Baghdad e fondatore di Fable Tour. Accompagna viaggiatori da tutto il mondo tra i siti archeologici e le città dell'Iraq, in inglese, russo e arabo.</p></div>
  </div>
</article>
{rel_html}
</main>
""" + tail()
    d = OUT / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out)

def build_index(posts):
    ordered = list(reversed(posts))
    cats = sorted({p["category"] for p in posts})
    url = BASE
    desc = ("Il blog di Fable Tour sull'Iraq: guide in italiano ai siti archeologici, alle città e ai luoghi della Mesopotamia — "
            "Babilonia, Ur, Hatra, le Paludi e molto altro, con consigli pratici di una guida locale.")
    graph = [
        {"@type": "Blog", "@id": url + "#blog", "url": url, "name": "Blog Fable Tour — Viaggio in Iraq",
         "description": desc, "inLanguage": "it-IT", "publisher": ORG,
         "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": BASE + p["slug"] + "/",
                       "datePublished": p["date"], "image": img_url(p.get("image"))} for p in ordered[:30]]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Fable Tour Iraq", "item": SITE + "/it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": url}]},
    ]
    h = head("Blog sull'Iraq: guide ai luoghi della Mesopotamia | Fable Tour", desc, url, "website",
             SITE + "/og-image.jpg", "Fable Tour — blog di viaggio sull'Iraq", "",
             {"@context": "https://schema.org", "@graph": graph},
             "blog Iraq, viaggio in Iraq, cosa vedere in Iraq, siti archeologici Iraq, Mesopotamia, guida Iraq").replace("{BLOGCUR}", 'aria-current="page"')
    feat = ""
    rest = ordered
    if ordered:
        p = ordered[0]; rest = ordered[1:]
        style = f' style="background-image:url(\'{src(p["image"])}\')"' if p.get("image") else ""
        noimg = "" if p.get("image") else " ph-none"
        feat = (f'<a class="featured" href="/it/blog/{p["slug"]}/"><div class="ph{noimg}"{style}></div><div class="bd">'
                f'<span class="eyebrow">Ultimo articolo · {esc(p["category"])}</span><h2>{esc(p["h1"])}</h2><p>{esc(p["excerpt"])}</p>'
                f'<small style="color:var(--muted);font-size:13px">{it_date(p["date"])} · {p["_min"]} min di lettura</small></div></a>')
    chips = ""
    if len(cats) > 1:
        chips = ('<div class="chips" role="group" aria-label="Filtra per categoria"><button aria-pressed="true" data-f="*">Tutti</button>'
                 + "".join(f'<button aria-pressed="false" data-f="{esc(c)}">{esc(c)}</button>' for c in cats) + "</div>")
    grid = '<div class="grid" id="posts">' + "".join(card(p) for p in rest) + "</div>" if rest else ""
    script = """<script>(function(){var b=document.querySelectorAll('.chips button'),c=document.querySelectorAll('#posts .pc');b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.setAttribute('aria-pressed',y===x)});var f=x.dataset.f;c.forEach(function(k){k.hidden=!(f==='*'||k.dataset.cat===f)})})})})();</script>"""
    out = h + f"""
<main>
<section class="hero"><div class="hero-band in">
  <span class="eyebrow">Blog · Un luogo dell'Iraq al giorno</span>
  <h1>Viaggio in Iraq: storie e guide dalla Mesopotamia</h1>
  <p>Ogni giorno un nuovo articolo su un luogo dell'Iraq — siti archeologici, città antiche, santuari, paesaggi — scritto con l'esperienza di una guida che ci lavora ogni settimana.</p>
</div></section>
<section class="block in">
  {feat}
  {chips}
  {grid}
</section>
<section class="in"><aside class="cta" style="margin-top:0">
  <span class="eyebrow">Dal blog al viaggio</span>
  <h2>Vuoi vedere questi luoghi dal vivo?</h2>
  <p>Due programmi privati con guida e hotel 4★–5★: 7 giorni da Baghdad o 9 giorni da Bassora a Erbil, nella data che scegli tu.</p>
  <div class="btns"><a class="btn" href="/it/">Scopri i tour in Iraq →</a><a class="btn ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
</aside></section>
</main>
{script if chips else ""}
""" + tail()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(out)

def build_feed(posts):
    items = ""
    for p in list(reversed(posts))[:30]:
        dt = datetime.datetime.strptime(p["date"], "%Y-%m-%d").replace(hour=8, tzinfo=datetime.timezone(datetime.timedelta(hours=3)))
        items += (f"<item><title>{esc(p['h1'])}</title><link>{BASE}{p['slug']}/</link><guid>{BASE}{p['slug']}/</guid>"
                  f"<pubDate>{dt.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate><category>{esc(p['category'])}</category>"
                  f"<description>{esc(p['description'])}</description></item>")
    (OUT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Blog Fable Tour — Viaggio in Iraq</title><link>{BASE}</link>
<description>Guide in italiano ai luoghi dell'Iraq</description><language>it-it</language>{items}</channel></rss>
""")

def build_sitemap(posts):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    s = re.sub(r"\s*<!-- blog-it:start -->.*?<!-- blog-it:end -->", "", s, flags=re.S)
    last = max([p.get("updated", p["date"]) for p in posts] or [datetime.date.today().isoformat()])
    entries = f"\n  <!-- blog-it:start -->\n  <url><loc>{BASE}</loc><lastmod>{last}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>"
    for p in posts:
        img = ""
        if p.get("image"):
            img = f"<image:image><image:loc>{esc(img_url(p['image']))}</image:loc></image:image>"
        entries += f"\n  <url><loc>{BASE}{p['slug']}/</loc><lastmod>{p.get('updated', p['date'])}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>{img}</url>"
    entries += "\n  <!-- blog-it:end -->"
    if 'xmlns:image=' not in s:
        s = s.replace('<urlset ', '<urlset xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" ', 1)
    s = s.replace("</urlset>", entries + "\n</urlset>")
    sm.write_text(s)

def main():
    posts = json.loads((SRC / "posts.json").read_text())
    posts.sort(key=lambda p: p["date"])
    slugs = set()
    for p in posts:
        assert p["slug"] not in slugs, "duplicate slug " + p["slug"]; slugs.add(p["slug"])
        body = (SRC / "posts" / f'{p["slug"]}.html').read_text()
        p["_words"] = words(body) + sum(words(q + " " + a) for q, a in p.get("faq", []))
        p["_min"] = max(1, math.ceil(p["_words"] / 220))
        if len(p["title"]) > 65: print("WARN title >65 chars:", p["slug"], len(p["title"]))
        if not (110 <= len(p["description"]) <= 160): print("WARN description length:", p["slug"], len(p["description"]))
    for p in posts:
        build_article(p, posts)
    build_index(posts)
    build_feed(posts)
    build_sitemap(posts)
    print(f"Built {len(posts)} article(s) + blog index, feed, sitemap.")

if __name__ == "__main__":
    main()
