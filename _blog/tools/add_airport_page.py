"""Build a standalone, shareable airport-pickup page for every language:
/airport-transfer/ (Arabic) and /<lang>/airport-transfer/, cloned from that
language's homepage with only the airport section shown (body.ap-solo),
own title/description/canonical/hreflang, OG + Twitter share image
(img/og/airport-transfer.jpg) and JSON-LD. Also points every airport
copy-link button to the page and adds the pages to sitemap.xml. Idempotent."""
import re, json, html, pathlib, glob

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://iraq.fabletour.com"
SLUG = "airport-transfer"
OG = f"{SITE}/img/og/{SLUG}.jpg"

ALL = {"ar": "كل رحلات العراق", "en": "All Iraq tours", "ru": "Все туры по Ираку", "de": "Alle Irak-Reisen",
       "fr": "Tous les circuits en Irak", "es": "Todos los tours por Irak", "it": "Tutti i tour in Iraq",
       "el": "Όλες οι περιηγήσεις στο Ιράκ", "cs": "Všechny zájezdy do Iráku", "pl": "Wszystkie wycieczki po Iraku",
       "zh-Hans": "全部伊拉克行程", "zh-Hant-TW": "全部伊拉克行程", "ja": "イラクのツアー一覧", "tr": "Tüm Irak turları",
       "fa": "همه تورهای عراق", "ms": "Semua lawatan Iraq", "id": "Semua tur Irak", "th": "ทัวร์อิรักทั้งหมด",
       "ta": "அனைத்து ஈராக் சுற்றுலாக்கள்", "hi": "इराक के सभी टूर", "ur": "عراق کے تمام ٹورز", "fi": "Kaikki Irakin matkat",
       "sv": "Alla Irakresor", "da": "Alle Irak-ture", "no": "Alle Irak-turer", "sk": "Všetky zájazdy do Iraku",
       "hr": "Sva putovanja po Iraku", "ro": "Toate tururile în Irak", "nl": "Alle Irak-reizen", "ka": "ერაყის ყველა ტური"}

CSS = ("body.ap-solo .hero,body.ap-solo .hero-band,body.ap-solo main>*:not(#airport-transfer){display:none!important}"
       "body.ap-solo #airport-transfer{padding-top:26px!important;max-width:820px;margin-inline:auto}"
       "body.ap-solo .ap-toggle{display:none}"
       ".ap-solo-head{margin-bottom:16px}"
       ".ap-all{display:inline-flex;align-items:center;gap:6px;color:var(--navy);font-size:14px;font-weight:600;text-decoration:none;border-bottom:1px solid var(--gold);padding-bottom:2px}"
       ".ap-h1{font-family:var(--serif-en);font-weight:400;font-size:clamp(26px,4.4vw,36px);line-height:1.25;color:var(--navy);margin:14px 0 0}"
       'html[lang="ar"] .ap-h1,html[lang="fa"] .ap-h1,html[lang="ur"] .ap-h1{font-family:var(--serif-ar);font-weight:700}\n')


def homes():
    out = [ROOT / "index.html"]
    for p in sorted(glob.glob(str(ROOT / "*/index.html"))):
        p = pathlib.Path(p)
        if p.parent.name in ("blog", "_blog", "day-trips", SLUG) or p.parent.name.startswith("iraq-tours-from"):
            continue
        if 'id="airport-transfer"' in p.read_text(encoding="utf-8"):
            out.append(p)
    return out


def meta_set(s, attr, key, val):
    pat = re.compile(rf'<meta {attr}="{re.escape(key)}" content="[^"]*">')
    tag = f'<meta {attr}="{key}" content="{html.escape(val, quote=True)}">'
    return pat.sub(lambda m: tag, s, count=1) if pat.search(s) else s


def trunc(t, n=158):
    if len(t) <= n: return t
    t = t[:n]
    return (t.rsplit(" ", 1)[0] if " " in t[-40:] else t).rstrip(",.،、 ") + "…"

def _old_trunc(t, n=158):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",.،") + "…"


def build(src):
    s = src.read_text(encoding="utf-8")
    lang = re.search(r'<html[^>]*lang="([^"]+)"', s).group(1)
    home = re.search(r'HOME="([^"]*)"', s).group(1)
    url = SITE + home + SLUG + "/"
    sec = re.search(r'<section[^>]*id="airport-transfer">.*?</section>', s, re.S).group(0)
    title = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<button class="ap-toggle".*?<b>(.*?)</b>', sec, re.S).group(1))).strip()
    intro = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<div class="ap-in">\s*<p>(.*?)</p>', sec, re.S).group(1))).strip()
    alt = html.unescape(re.search(r'<div class="ap-ph"><img[^>]*alt="([^"]*)"', sec).group(1))
    inc = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<li>(.*?)</li>", re.search(r'<ul class="ap-inc">(.*?)</ul>', sec, re.S).group(1))]
    sep = "، " if lang in ("ar", "fa", "ur") else ("、" if lang.startswith(("zh", "ja")) else ", ")
    desc = trunc(intro + " " + sep.join(inc) + ("." if lang not in ("zh-Hans", "zh-Hant-TW", "ja") else "。"), 200)

    # absolute asset paths (page sits one folder deeper)
    s = re.sub(r'(?<=["\'(|=])\.\./', "/", s)
    s = re.sub(r'(?<=["\'(|])(img/|hero\.jpg|favicon\.png|apple-touch-icon\.png|logo\.png|og-image\.jpg)', r"/\1", s)

    # head
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | Fable Tour</title>", s, count=1, flags=re.S)
    s = meta_set(s, "name", "description", desc)
    s = re.sub(r'<meta name="keywords" content="[^"]*">\n?', "", s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', rf"\g<1>{url}", s, count=1)
    s = re.sub(rf'(<link rel="alternate" hreflang="[^"]+" href="{re.escape(SITE)}/(?:[a-z-]+/)?)"', rf'\1{SLUG}/"', s)
    s = meta_set(s, "property", "og:type", "article")
    for a, k, v in [("property", "og:title", title), ("property", "og:description", desc), ("property", "og:url", url),
                    ("property", "og:image", OG), ("property", "og:image:alt", alt),
                    ("name", "twitter:title", title), ("name", "twitter:description", desc), ("name", "twitter:image", OG)]:
        s = meta_set(s, a, k, v)
    if 'og:image:type' not in s:
        s = s.replace(f'<meta property="og:image" content="{OG}">',
                      f'<meta property="og:image" content="{OG}">\n<meta property="og:image:secure_url" content="{OG}">\n<meta property="og:image:type" content="image/jpeg">', 1)

    # JSON-LD
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    org = None
    try:
        g = json.loads(m.group(1))
        nodes = g.get("@graph", [g])
        org = next((n for n in nodes if n.get("@type") == "TravelAgency"), None)
    except Exception:
        pass
    org = org or {"@type": "TravelAgency", "@id": "https://fabletour.com/#org", "name": "Fable Tour", "url": "https://fabletour.com"}
    ld = {"@context": "https://schema.org", "@graph": [
        org,
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": lang,
         "primaryImageOfPage": OG, "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "Service", "@id": url + "#service", "name": title, "description": intro, "url": url, "image": OG,
         "serviceType": "Airport transfer", "provider": {"@id": org.get("@id", "https://fabletour.com/#org")},
         "areaServed": {"@type": "City", "name": "Baghdad"},
         "availableChannel": {"@type": "ServiceChannel", "serviceUrl": url, "servicePhone": "+9647711745353"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Fable Tour", "item": SITE + home},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}]}]}
    s = s[:m.start()] + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>" + s[m.end():]

    # body: only the airport section, open, with its own h1
    s = re.sub(r'<h1 class="disp"([^>]*)>(.*?)</h1>', r'<p class="disp"\1>\2</p>', s, count=1, flags=re.S)
    s = re.sub(r"<body([^>]*)>", lambda mm: (f'<body{mm.group(1)}>' if "ap-solo" in mm.group(1) else
               (re.sub(r'class="', 'class="ap-solo ', mm.group(0), 1) if "class=" in mm.group(1) else '<body class="ap-solo">')), s, count=1)
    arrow = "→" if re.search(r'dir="rtl"', s[:300]) else "←"
    headblk = f'<div class="ap-solo-head"><a class="ap-all" href="{home}">{arrow} {ALL[lang]}</a><h1 class="ap-h1">{html.escape(title)}</h1></div>'
    s = re.sub(r'(<section[^>]*id="airport-transfer">)', lambda mm: mm.group(1) + "\n    " + headblk, s, count=1)
    s = s.replace('<div id="ap-body" hidden>', '<div id="ap-body">', 1)
    s = s.replace('.dt-cp.ok{', CSS + ".dt-cp.ok{", 1)
    s = s.replace('href="#interest"', 'href="#airport-transfer"').replace('href="#itinerary"', f'href="{home}#itinerary"')
    s = s.replace('href="#day-trips"', f'href="{home}#day-trips"')

    dst = ROOT / home.strip("/") / SLUG / "index.html" if home != "/" else ROOT / SLUG / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(s, encoding="utf-8")
    return lang, home, dst


def point_buttons():
    n = 0
    for p in glob.glob(str(ROOT / "**/index.html"), recursive=True):
        p = pathlib.Path(p)
        s = p.read_text(encoding="utf-8")
        t = re.sub(r'(class="dt-cp ap-cp" data-url="[^"#]*)#airport-transfer"', rf'\1{SLUG}/"', s)
        if t != s:
            p.write_text(t, encoding="utf-8"); n += 1
    return n


def sitemap(pairs):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    s = re.sub(rf"  <url>\n    <loc>[^<]*/{SLUG}/</loc>.*?</url>\n", "", s, flags=re.S)
    hreflang = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', (ROOT / SLUG / "index.html").read_text(encoding="utf-8"))
    alts = "".join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>\n' for h, u in hreflang)
    blocks = "".join(f"  <url>\n    <loc>{SITE}{home}{SLUG}/</loc>\n    <lastmod>2026-10-29</lastmod>\n{alts}"
                     f"    <image:image><image:loc>{OG}</image:loc></image:image>\n  </url>\n" if "xmlns:image" in s else
                     f"  <url>\n    <loc>{SITE}{home}{SLUG}/</loc>\n    <lastmod>2026-10-29</lastmod>\n{alts}  </url>\n"
                     for _, home in pairs)
    s = s.replace("</urlset>", blocks + "</urlset>")
    sm.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    pairs = []
    for h in homes():
        lang, home, dst = build(h)
        pairs.append((lang, home))
        print(lang, home, dst.relative_to(ROOT))
    print("buttons:", point_buttons())
    sitemap(pairs)
    print("pages:", len(pairs))
