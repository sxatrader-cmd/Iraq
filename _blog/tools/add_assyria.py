#!/usr/bin/env python3
"""Adds the 2-day trip 'Assyria: Ashur, Hatra, Mosul & Nimrud' (key assyria, slug assyria-hatra-nimrud)
to the day-trips section of every page that has it (all languages, country/city pages included),
and builds its own page /<lang>/day-trips/assyria-hatra-nimrud/ (Arabic: /day-trips/assyria-hatra-nimrud/)
+ sitemap entries.  Ramada Hotel International package only: 650,000 IQD -> $500 flat for 1-3 people
1 person $500, 2 people $600, 3+ people $250 per person.  Source: discovery.fabletour.com/assyria-tour/.  Idempotent."""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((pathlib.Path(__file__).parent / "assyria_i18n.json").read_text())
KEY, SLUG, TPL = "assyria", "assyria-hatra-nimrud", "samarra"
PRICE = 500  # 1-person / JSON-LD Offer starting price
DISPLAY_PRICE = 750  # 3 travellers ($250 each); do not use for JSON-LD
PRICE_JS = f"{KEY}:function(n){{return n<2?500:n<3?600:250*n}},"
IMGS = ["assyria-hatra-temple.webp", "assyria-hatra-iwan.webp", "assyria-hatra-gate.webp",
        "assyria-ashur-brick.webp", "assyria-mosul-nuri.webp", "assyria-nimrud-inscription.webp",
        "assyria-ramada-mosul.webp", "assyria-ramada-room.webp", "assyria-ramada-suite.webp"]
SITE = "https://iraq.fabletour.com"
LANGMAP = {"zh-Hans": "zh", "zh-Hant-TW": "zh-tw"}
esc = lambda s: html.escape(s, quote=True)
ART = lambda k: rf'<article class="dt[^"]*"(?: data-max="\d+")? data-trip="{k}">.*?</article>'


def lang_of(s):
    l = re.search(r'<html lang="([^"]+)"', s).group(1)
    return LANGMAP.get(l, l)


def base_of(l):
    return ROOT if l == "ar" else ROOT / l


def art(s, key):
    return re.search(ART(key), s, re.S)


def img_pre(card):
    return re.search(r"url\('([^']*)samarra-askari-gate\.webp'\)", card).group(1)


def build_card(tpl, l, solo=False, more_lbl=None):
    t = D[l]
    pre = img_pre(tpl)
    a = re.sub(r'<article class="dt[^"]*" data-trip="samarra">', f'<article class="dt" data-trip="{KEY}">', tpl, 1)
    a = re.sub(r"background-image:url\('[^']*'\)", f"background-image:url('{pre}{IMGS[0]}')", a, 1)
    a = re.sub(r'data-full="[^"]*"', 'data-full="' + "|".join(pre + i for i in IMGS) + '"', a, 1)
    a = re.sub(r'(class="dt-ph"[^>]*aria-label=")[^"]*"', lambda m: m.group(1) + esc(t["n"]) + '"', a, 1)
    a = re.sub(r'<span class="dt-cnt"([^>]*)>1 / \d+</span>', rf'<span class="dt-cnt"\1>1 / {len(IMGS)}</span>', a, 1)
    a = re.sub(r'<h[13][^>]*>.*?</h[13]>', f'<h3>{esc(t["n"])}</h3>', a, 1, flags=re.S)
    a = re.sub(r'<p class="dt-s">.*?</p>', f'<p class="dt-s">{esc(t["s"])}</p><p class="dt-s"><b>{esc(t["d"])}</b></p>', a, 1, flags=re.S)
    a = re.sub(r'(<ul class="dt-inc"[^>]*>).*?(</ul>)', lambda m: m.group(1) + "".join(f"<li>{esc(x)}</li>" for x in t["inc"]) + m.group(2), a, 1, flags=re.S)
    a = re.sub(r'<div class="dt-more" id="more-samarra"[^>]*>.*?</div>',
               f'<div class="dt-more" id="more-{KEY}" hidden>' + "".join(f"<p>{esc(p)}</p>" for p in t["p"]) + "</div>", a, 1, flags=re.S)
    a = a.replace('aria-controls="more-samarra"', f'aria-controls="more-{KEY}"')
    a = re.sub(r'(<div class="dt-total">.*?<b dir="ltr">)[^<]*', lambda m: m.group(1) + f"${DISPLAY_PRICE}", a, 1, flags=re.S)
    if solo:
        a = a.replace(f'<article class="dt" data-trip="{KEY}">', f'<article class="dt is-solo" data-trip="{KEY}">', 1)
        a = a.replace(f'<h3>{esc(t["n"])}</h3>', f'<h1 class="dt-h">{esc(t["n"])}</h1>', 1)
        a = a.replace(f'id="more-{KEY}" hidden>', f'id="more-{KEY}">', 1)
        if more_lbl:
            a = re.sub(r'(<button type="button" class="dt-rm"[^>]*>)[^<]*', lambda m: m.group(1) + more_lbl, a, 1)
            a = a.replace('class="dt-rm" aria-expanded="false"', 'class="dt-rm" aria-expanded="true"', 1)
    return a


def patch_js(s, l):
    s = re.sub(rf'{KEY}:function\(n\)\{{[^}}]*\}},', PRICE_JS, s)
    if f"{KEY}:function" not in s:
        s = re.sub(r'(samarra:function\(n\)\{[^}]*\},)', lambda m: m.group(1) + "\n " + PRICE_JS, s, 1)
    if f'T={{"{KEY}"' not in s:
        s = s.replace('},T={', f'}},T={{"{KEY}": {json.dumps(D[l]["n"], ensure_ascii=False)}, ', 1)
    if f'SL={{"{KEY}"' not in s:
        s = s.replace('SL={', f'SL={{"{KEY}": "{SLUG}", ', 1)
    s = s.replace("n=Math.min(MAX,", "n=Math.min(+(c.dataset.max||MAX),")
    return s


def insert_last(s, card):
    s = re.sub(r'\n?' + ART(KEY), "", s, flags=re.S)
    m = art(s, "south")
    return s[:m.end()] + card + s[m.end():]


def trunc(t, n=157):
    if len(t) <= n:
        return t
    c = t[:n]
    return c[:c.rfind(" ")].rstrip(" ,;:—.،") + "…" if " " in c else c + "…"


def home_card(l):
    return art((base_of(l) / "index.html").read_text(), TPL).group(0)


def solo_page(l):
    base = base_of(l)
    s = (base / "day-trips" / TPL / "index.html").read_text()
    t = D[l]
    old_name = json.loads(re.search(r'T=\{.*?"samarra": ("(?:\\.|[^"\\])*")', s, re.S).group(1))
    lbls = json.loads(re.search(r'var L=(\[[^\]]*\])', s).group(1))
    hc = home_card(l)
    m = art(s, TPL)
    norm = hc.replace(img_pre(hc), img_pre(m.group(0)))
    s = s[:m.start()] + norm + s[m.end():]
    s = re.sub(r'\n?' + ART(KEY), "", s, flags=re.S)
    m = re.search(r'<article class="dt[^"]*"', s)
    s = s[:m.start()] + build_card(norm, l, solo=True, more_lbl=lbls[1]) + "\n" + s[m.start():]
    s = s.replace('<body class="dt-solo" data-trip="samarra"', f'<body class="dt-solo" data-trip="{KEY}"')
    s = s.replace(f"day-trips/{TPL}/", f"day-trips/{SLUG}/").replace(f"img/og/{TPL}.jpg", f"img/og/{SLUG}.jpg")
    old_desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    s = s.replace(f'content="{old_desc}"', f'content="{esc(trunc(t["p"][0]))}"')
    on, nn = esc(old_name), esc(t["n"])
    s = re.sub(r'<title>' + re.escape(on), lambda mm: '<title>' + nn, s, 1)
    for prop in ['property="og:title"', 'name="twitter:title"', 'property="og:image:alt"']:
        s = re.sub(rf'(<meta {prop} content="){re.escape(on)}', lambda mm: mm.group(1) + nn, s, 1)

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
                        for k in ("price", "lowPrice", "highPrice"):
                            if k in x["offers"]:
                                x["offers"][k] = str(PRICE)
                for k, v in list(x.items()):
                    if isinstance(v, str):
                        if v == old_name:
                            x[k] = t["n"]
                    else:
                        walk(v)
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    if isinstance(v, str):
                        if v == old_name:
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
    blocks = re.findall(rf'  <url>\n    <loc>[^<]*day-trips/{TPL}/</loc>.*?</url>\n', s, flags=re.S)
    add = "".join(b.replace(f"day-trips/{TPL}/", f"day-trips/{SLUG}/").replace(f"img/og/{TPL}.jpg", f"img/og/{SLUG}.jpg") for b in blocks)
    s = s.replace(blocks[-1], blocks[-1] + add, 1)
    sm.write_text(s)
    print("sitemap +", len(blocks))


def run():
    homes = {}
    n = 0
    for p in sorted(ROOT.rglob("*.html")):
        if ".git" in p.parts or f"/day-trips/{SLUG}/" in str(p):
            continue
        s = p.read_text()
        m = art(s, TPL)
        if not m:
            continue
        l = lang_of(s)
        tpl = m.group(0)
        if "is-solo" in tpl or "<h1" in tpl:
            hc = homes.setdefault(l, home_card(l))
            tpl = hc.replace(img_pre(hc), img_pre(tpl))
        s = insert_last(s, build_card(tpl, l))
        s = patch_js(s, l)
        p.write_text(s)
        n += 1
    print("pages patched:", n)
    for l in D:
        solo_page(l)
    sitemap()
    import add_dt_default_pax; add_dt_default_pax.run()  # .dt day-trip cards default to 3 travellers, site-wide


if __name__ == "__main__":
    run()
    import add_dt_links; add_dt_links.run()  # keep homepage cards linked (crawlable <a href>) to their day-trip/airport pages
