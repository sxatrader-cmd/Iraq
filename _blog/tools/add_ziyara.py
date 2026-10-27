#!/usr/bin/env python3
"""Adds the day trip 'Baghdad's Holy Shrines' (key ziyara, slug baghdad-holy-shrines) to the
day-trips section of every page in all 24 languages, and builds its own page
/<lang>/day-trips/baghdad-holy-shrines/ (Arabic: /day-trips/baghdad-holy-shrines/) + sitemap entries.
Price: 1 person $50, 2 people $75, +$25 per extra person.  Idempotent."""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((pathlib.Path(__file__).parent / "ziyara_i18n.json").read_text())
KEY, SLUG, OLD = "ziyara", "baghdad-holy-shrines", "baghdad-old-town"
PRICE_JS = "ziyara:function(n){return 50+25*(n-1)},"
IMGS = ["kadhimiya-shrine-night.webp", "junayd-baghdadi-shrine.webp", "junayd-baghdadi-front.webp",
        "bahlul-shrine-dome.webp", "bahlul-shrine-tomb.webp"]
SITE = "https://iraq.fabletour.com"
esc = lambda s: html.escape(s, quote=True)


def lang_dirs():
    for l in D:
        yield l, (ROOT if l == "ar" else ROOT / l)


def art(s, key):
    m = re.search(rf'<article class="dt[^"]*" data-trip="{key}">.*?</article>', s, re.S)
    return m


def build_card(tpl, l, solo=False, more_lbl=None):
    """tpl = this page's (non-solo) oldtown article; returns the ziyara article"""
    t = D[l]
    pre = re.search(r"url\('([^']*)shabandar-cafe-tea\.webp'\)", tpl).group(1)
    full = "|".join(pre + i for i in IMGS)
    a = re.sub(r'data-trip="oldtown"', f'data-trip="{KEY}"', tpl, 1)
    a = re.sub(r"background-image:url\('[^']*'\)", f"background-image:url('{pre}{IMGS[0]}')", a, 1)
    a = re.sub(r'data-full="[^"]*"', f'data-full="{full}"', a, 1)
    a = re.sub(r'(class="dt-ph"[^>]*aria-label=")[^"]*"', lambda m: m.group(1) + esc(t["n"]) + '"', a, 1)
    a = re.sub(r'<span class="dt-cnt"([^>]*)>1 / \d+</span>', rf'<span class="dt-cnt"\1>1 / {len(IMGS)}</span>', a, 1)
    a = re.sub(r'<h[13][^>]*>.*?</h[13]>', f'<h3>{esc(t["n"])}</h3>', a, 1, flags=re.S)
    a = re.sub(r'<p class="dt-s">.*?</p>', f'<p class="dt-s">{esc(t["s"])}</p>', a, 1, flags=re.S)
    a = re.sub(r'(<ul class="dt-inc"[^>]*>).*?(</ul>)', lambda m: m.group(1) + "".join(f"<li>{esc(x)}</li>" for x in t["inc"]) + m.group(2), a, 1, flags=re.S)
    a = re.sub(r'<div class="dt-more" id="more-oldtown"[^>]*>.*?</div>',
               f'<div class="dt-more" id="more-{KEY}" hidden>' + "".join(f"<p>{esc(p)}</p>" for p in t["p"]) + "</div>", a, 1, flags=re.S)
    a = a.replace('aria-controls="more-oldtown"', f'aria-controls="more-{KEY}"')
    if solo:
        a = a.replace(f'<article class="dt" data-trip="{KEY}">', f'<article class="dt is-solo" data-trip="{KEY}">', 1)
        a = a.replace(f'<h3>{esc(t["n"])}</h3>', f'<h1 class="dt-h">{esc(t["n"])}</h1>', 1)
        a = a.replace(f'id="more-{KEY}" hidden>', f'id="more-{KEY}">', 1)
        if more_lbl:
            a = re.sub(rf'(<button type="button" class="dt-rm"[^>]*>)[^<]*', lambda m: m.group(1) + more_lbl, a, 1)
    return a


def patch_js(s, l):
    if "ziyara:function" not in s:
        s = re.sub(r'(oldtown:function\(n\)\{[^}]*\},)', lambda m: m.group(1) + "\n " + PRICE_JS, s, 1)
    if f'T={{"{KEY}"' not in s:
        s = s.replace('T={"oldtown"', f'T={{"{KEY}": {json.dumps(D[l]["n"], ensure_ascii=False)}, "oldtown"', 1)
    if f'SL={{"{KEY}"' not in s:
        s = s.replace('SL={"oldtown"', f'SL={{"{KEY}": "{SLUG}", "oldtown"', 1)
    return s


def insert(s, card):
    s = re.sub(rf'\n?<article class="dt[^"]*" data-trip="{KEY}">.*?</article>', "", s, flags=re.S)
    m = re.search(r'<article class="dt[^"]*" data-trip=', s)
    return s[:m.start()] + card + "\n" + s[m.start():]


def trunc(t, n=157):
    if len(t) <= n:
        return t
    c = t[:n]
    return c[:c.rfind(" ")].rstrip(" ,;:—.") + "…" if " " in c else c + "…"


def solo_page(l, base, home_old):
    src = base / "day-trips" / OLD / "index.html"
    s = src.read_text()
    t = D[l]
    old_name = json.loads(re.search(r'T=\{.*?"oldtown": ("(?:\\.|[^"\\])*")', s, re.S).group(1))
    lbls = json.loads(re.search(r'var L=(\[[^\]]*\])', s).group(1))
    # put the oldtown card back to its normal (non-solo) form, then add the solo shrines card
    m = art(s, "oldtown")
    pre_here = re.search(r"url\('([^']*)shabandar-cafe-tea\.webp'\)", m.group(0)).group(1)
    pre_home = re.search(r"url\('([^']*)shabandar-cafe-tea\.webp'\)", home_old).group(1)
    norm_old = home_old.replace(pre_home, pre_here)
    s = s[:m.start()] + norm_old + s[m.end():]
    s = re.sub(rf'\n?<article class="dt[^"]*" data-trip="{KEY}">.*?</article>', "", s, flags=re.S)
    m = re.search(r'<article class="dt[^"]*" data-trip=', s)
    s = s[:m.start()] + build_card(norm_old, l, solo=True, more_lbl=lbls[1]) + "\n" + s[m.start():]
    s = s.replace('data-trip="oldtown"', f'data-trip="{KEY}"', 1) if s.find('<body class="dt-solo" data-trip="oldtown"') >= 0 else s
    s = s.replace('<body class="dt-solo" data-trip="oldtown"', f'<body class="dt-solo" data-trip="{KEY}"')
    s = s.replace(f"day-trips/{OLD}/", f"day-trips/{SLUG}/").replace(f"img/og/{OLD}.jpg", f"img/og/{SLUG}.jpg")
    # head texts
    old_desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    new_desc = esc(trunc(t["p"][0]))
    s = s.replace(f'content="{old_desc}"', f'content="{new_desc}"')
    on, nn = esc(old_name), esc(t["n"])
    s = re.sub(r'<title>' + re.escape(on), '<title>' + nn.replace("\\", "\\\\"), s, 1)
    for prop in ['property="og:title"', 'name="twitter:title"', 'property="og:image:alt"']:
        s = re.sub(rf'(<meta {prop} content="){re.escape(on)}', lambda mm: mm.group(1) + nn, s, 1)
    # JSON-LD
    def ld(mm):
        d = json.loads(mm.group(1))
        def walk(x):
            if isinstance(x, dict):
                if x.get("@type") == "TouristTrip":
                    x["name"] = t["n"]
                    x["description"] = " ".join(t["p"])[:600]
                    x["image"] = [f"{SITE}/img/og/{SLUG}.jpg"] + [f"{SITE}/img/{i}" for i in IMGS[:4]]
                    stops = [p.strip() for p in t["s"].split("·")]
                    if "itinerary" in x:
                        x["itinerary"]["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "item": {"@type": "TouristAttraction", "name": n}} for i, n in enumerate(stops)]
                        if "numberOfItems" in x["itinerary"]:
                            x["itinerary"]["numberOfItems"] = len(stops)
                    if isinstance(x.get("offers"), dict):
                        x["offers"]["price"] = "50"
                        if "lowPrice" in x["offers"]: x["offers"]["lowPrice"] = "50"
                for k, v in list(x.items()):
                    if isinstance(v, str) and v == old_name:
                        x[k] = t["n"]
                    else:
                        walk(v)
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    if isinstance(v, str) and v == old_name:
                        x[i] = t["n"]
                    else:
                        walk(v)
        walk(d)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)
    out = base / "day-trips" / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)


def sitemap():
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    if f"day-trips/{SLUG}/" in s:
        return
    blocks = re.findall(rf'  <url>\n    <loc>[^<]*day-trips/{OLD}/</loc>.*?</url>\n', s, flags=re.S)
    add = "".join(b.replace(f"day-trips/{OLD}/", f"day-trips/{SLUG}/").replace(f"img/og/{OLD}.jpg", f"img/og/{SLUG}.jpg") for b in blocks)
    s = s.replace(blocks[-1], blocks[-1] + add, 1)
    sm.write_text(s)


def run():
    for l, base in lang_dirs():
        home = base / "index.html"
        hs = home.read_text()
        old_home = art(hs, "oldtown").group(0)
        pages = [home] + sorted(p for p in (base / "day-trips").glob("*/index.html") if p.parent.name != SLUG)
        for p in pages:
            s = p.read_text()
            m = art(s, "oldtown")
            tpl = m.group(0)
            if 'is-solo' in tpl or '<h1' in tpl:  # old-town page: use the homepage card as template
                pre_here = re.search(r"url\('([^']*)shabandar-cafe-tea\.webp'\)", tpl).group(1)
                pre_home = re.search(r"url\('([^']*)shabandar-cafe-tea\.webp'\)", old_home).group(1)
                tpl = old_home.replace(pre_home, pre_here)
            s = insert(s, build_card(tpl, l))
            s = patch_js(s, l)
            p.write_text(s)
        solo_page(l, base, old_home)
        print("ziyara:", l)
    sitemap()


if __name__ == "__main__":
    run()
