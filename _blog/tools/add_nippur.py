#!/usr/bin/env python3
"""Adds the Nippur day trip (key nippur, slug nippur) to every page that already
has the day-trips section, and builds /<lang>/day-trips/nippur/ (Arabic: /day-trips/nippur/)
plus sitemap, llms.txt and chatbot SL map.

Price: 150 + 25*(n-1) USD for the whole private group (1=$150, 2=$175, 3=$200, +$25 each extra).
Includes entrance tickets and a private car with driver/guide. Departure: Baghdad.
Idempotent."""
import re, json, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((pathlib.Path(__file__).parent / "nippur_i18n.json").read_text(encoding="utf-8"))
KEY, SLUG, TPL = "nippur", "nippur", "aqarquf"
TPL_SLUG = "aqar-quf"
PRICE = 150          # 1-person / JSON-LD starting price
DISPLAY_PRICE = 200  # default 3 travellers
PRICE_JS = f"{KEY}:function(n){{return 150+25*(n-1)}},"
IMGS = ["nippur-ziggurat.webp"]  # add nippur-ruins.webp here when the second photo is processed
SITE = "https://iraq.fabletour.com"
LANGMAP = {"zh-Hans": "zh", "zh-Hant-TW": "zh-tw"}
# Leave de/ja market landing pages alone if we ever need a tighter skip;
# day-trip cards already exist there in the same way, so language homes and
# day-trip pages in de/ja are updated like every other language.
SKIP_PARTS = {".git", "_blog"}
esc = lambda s: html.escape(s, quote=True)
ART = lambda k: rf'<article class="dt[^"]*"(?: data-max="\d+")? data-trip="{k}">.*?</article>'


def lang_of(s):
    m = re.search(r'<html lang="([^"]+)"', s)
    if not m:
        return "en"
    return LANGMAP.get(m.group(1), m.group(1))


def base_of(l):
    return ROOT if l == "ar" else ROOT / l


def art(s, key):
    return re.search(ART(key), s, re.S)


def img_pre(card):
    m = re.search(r"background-image:url\('([^']+)'\)", card)
    if not m:
        return "/img/"
    path = m.group(1)
    return path.rsplit("/", 1)[0] + "/" if "/" in path else ""


def tpl_href_home(tpl, slug):
    m = re.search(r'<a class="dt-tl" href="([^"]+)"', tpl)
    if not m:
        return None
    return re.sub(r"day-trips/[^/]+/", f"day-trips/{slug}/", m.group(1))


def build_card(tpl, l, solo=False, more_lbl=None):
    t = D.get(l) or D["en"]
    pre = img_pre(tpl)
    href = tpl_href_home(tpl, SLUG)
    a = re.sub(
        r'<article class="dt[^"]*"(?: data-max="\d+")? data-trip="[^"]+">',
        f'<article class="dt" data-trip="{KEY}">',
        tpl, 1,
    )
    a = re.sub(r"background-image:url\('[^']*'\)", f"background-image:url('{pre}{IMGS[0]}')", a, 1)
    if re.search(r'data-full="', a):
        a = re.sub(r'data-full="[^"]*"', 'data-full="' + "|".join(pre + i for i in IMGS) + '"', a, 1)
    else:
        a = re.sub(r"(class=\"dt-ph\")", r'\1 data-full="' + "|".join(pre + i for i in IMGS) + '"', a, 1)
    a = re.sub(
        r'(class="dt-ph"[^>]*aria-label=")[^"]*"',
        lambda m: m.group(1) + esc(t["n"]) + '"',
        a, 1,
    )
    if re.search(r'<span class="dt-cnt"', a):
        a = re.sub(
            r'<span class="dt-cnt"([^>]*)>1 / \d+</span>',
            rf'<span class="dt-cnt"\1>1 / {len(IMGS)}</span>',
            a, 1,
        )
    else:
        a = re.sub(
            r"(</div>\s*<div class=\"dt-bd\">)",
            f'<span class="dt-cnt" dir="ltr" aria-hidden="true">1 / {len(IMGS)}</span>\\1',
            a, 1,
        )
    if re.search(r'<a class="dt-tl"', a) and href:
        a = re.sub(
            r'<h3><a class="dt-tl" href="[^"]+"([^>]*)>.*?</a></h3>',
            lambda m: f'<h3><a class="dt-tl" href="{href}"{m.group(1)}>{esc(t["n"])}</a></h3>',
            a, 1, flags=re.S,
        )
    else:
        a = re.sub(r"<h3>(?:<a class=\"dt-tl\"[^>]*>)?(.*?)(?:</a>)?</h3>", f"<h3>{esc(t['n'])}</h3>", a, 1, flags=re.S)
    a = re.sub(r'(<p class="dt-s">).*?(</p>)', r"\1" + esc(t["s"]) + r"\2", a, 1, flags=re.S)
    # drop any extra dt-s lines (duration, discovery link, etc.) before pitch/inc
    a = re.sub(r'(</p>)\s*<p class="dt-s">.*?</p>', r"\1", a, 1, flags=re.S)
    if 'class="dt-pitch"' in a:
        a = re.sub(r'(<p class="dt-pitch">).*?(</p>)', r"\1" + esc(t["pitch"]) + r"\2", a, 1, flags=re.S)
    else:
        a = re.sub(
            r'(<p class="dt-s">.*?</p>)',
            r"\1<p class=\"dt-pitch\">" + esc(t["pitch"]) + "</p>",
            a, 1, flags=re.S,
        )
    incs = "".join(f"<li>{esc(x)}</li>" for x in t["inc"])
    if re.search(r'<ul class="dt-inc"', a):
        a = re.sub(r'(<ul class="dt-inc"[^>]*>).*?(</ul>)', lambda m: m.group(1) + incs + m.group(2), a, 1, flags=re.S)
    else:
        a = re.sub(r'(<div class="dt-calc">)', f'<ul class="dt-inc">{incs}</ul>\n    \\1', a, 1)
    more = f'<div class="dt-more" id="more-{KEY}" hidden>' + "".join(f"<p>{esc(p)}</p>" for p in t["p"]) + "</div>"
    if re.search(r'<div class="dt-more"', a):
        a = re.sub(r'<div class="dt-more" id="more-[^"]*"[^>]*>.*?</div>', more, a, 1, flags=re.S)
        a = re.sub(r'aria-controls="more-[^"]*"', f'aria-controls="more-{KEY}"', a, 1)
    a = re.sub(r'(<div class="dt-total">.*?<b dir="ltr">)[^<]*', lambda m: m.group(1) + f"${DISPLAY_PRICE}", a, 1, flags=re.S)
    if solo:
        a = a.replace(f'<article class="dt" data-trip="{KEY}">', f'<article class="dt is-solo" data-trip="{KEY}">', 1)
        a = re.sub(r"<h3>(?:<a class=\"dt-tl\"[^>]*>)?(.*?)(?:</a>)?</h3>", rf'<h1 class="dt-h">{esc(t["n"])}</h1>', a, 1, flags=re.S)
        a = a.replace(f'id="more-{KEY}" hidden>', f'id="more-{KEY}">', 1)
        if more_lbl:
            a = re.sub(r'(<button type="button" class="dt-rm"[^>]*>)[^<]*', lambda m: m.group(1) + more_lbl, a, 1)
            a = a.replace('class="dt-rm" aria-expanded="false"', 'class="dt-rm" aria-expanded="true"', 1)
    return a


def patch_js(s, l):
    tname = json.dumps((D.get(l) or D["en"])["n"], ensure_ascii=False)
    s = re.sub(KEY + r":function\(n\)\{[^}]*\},?", PRICE_JS, s)
    if f"{KEY}:function" not in s:
        if re.search(r"aqarquf:function\(n\)\{[^}]*\}", s):
            s = re.sub(r"(aqarquf:function\(n\)\{[^}]*\})", lambda m: m.group(1) + ",\n " + PRICE_JS.rstrip(","), s, 1)
        elif re.search(r"samarra:function\(n\)\{[^}]*\}", s):
            s = re.sub(r"(samarra:function\(n\)\{[^}]*\},)", lambda m: m.group(1) + "\n " + PRICE_JS, s, 1)
        else:
            s = re.sub(r"(var P=\{)", r"\1\n " + PRICE_JS, s, 1)
    # T map in the price script (T={...})
    if re.search(r"\bT=\{", s) and f'"{KEY}"' not in re.search(r"\bT=\{[^}]*\}", s).group(0) if re.search(r"\bT=\{[^}]*\}", s) else True:
        # only add if missing in that T object
        def add_t(m):
            body = m.group(0)
            if f'"{KEY}"' in body:
                return body
            return body.replace("T={", f"T={{\"{KEY}\": {tname}, ", 1)
        s = re.sub(r"\bT=\{[^}]*\}", add_t, s, count=1)
    # SL map in dtx
    def add_sl(m):
        body = m.group(0)
        if f'"{KEY}"' in body:
            return body
        return body.replace("SL={", f'SL={{"{KEY}": "{SLUG}", ', 1)
    s = re.sub(r"SL=\{[^}]*\}", add_sl, s)
    s = s.replace("n=Math.min(MAX,", "n=Math.min(+(c.dataset.max||MAX),")
    return s


def insert_card(s, card):
    s = re.sub(r"\n?" + ART(KEY), "", s, flags=re.S)
    for k in ("babylon4", "babylon", "south", "aqarquf"):
        m = art(s, k)
        if m:
            return s[: m.end()] + card + s[m.end() :]
    m = re.search(r'<div class="dt-grid">', s)
    if m:
        # after opening grid, skip first article if any — actually append before grid close
        g = s.find("</div>", s.find('class="dt-grid"'))
        return s[:g] + card + s[g:]
    return s


def trunc(t, n=157):
    if len(t) <= n:
        return t
    c = t[:n]
    return c[: c.rfind(" ")].rstrip(" ,;:—.،") + "…" if " " in c else c + "…"


def home_card(l):
    p = base_of(l) / "index.html"
    if not p.exists():
        p = ROOT / "en" / "index.html"
    return art(p.read_text(encoding="utf-8"), TPL).group(0)


def replace_seo(s, old, new):
    i = s.find("</head>")
    if i != -1:
        s = s[:i].replace(old, new) + s[i:]

    def ldrep(m):
        return m.group(0).replace(old, new)

    s = re.sub(r'<script type="application/ld\+json">.*?</script>', ldrep, s, flags=re.S)
    return s


def solo_page(l):
    base = base_of(l)
    src = base / "day-trips" / TPL_SLUG / "index.html"
    if not src.exists():
        print("skip solo, no template", l)
        return
    s = src.read_text(encoding="utf-8")
    t = D.get(l) or D["en"]
    old_m = re.search(r'T=\{.*?"' + TPL + r'": ("(?:\\.|[^"\\])*")', s, re.S)
    old_name = json.loads(old_m.group(1)) if old_m else "Aqar Quf"
    lbls_m = re.search(r"var L=(\[[^\]]*\])", s)
    lbls = json.loads(lbls_m.group(1)) if lbls_m else ["Read more", "Show less"]
    hc = home_card(l)
    m = art(s, TPL)
    if not m:
        print("skip solo, no tpl card", l)
        return
    norm = hc.replace(img_pre(hc), img_pre(m.group(0)))
    # Keep other-trip links working: put a normal TPL card back, then insert Nippur as solo
    s = s[: m.start()] + norm + s[m.end() :]
    s = re.sub(r"\n?" + ART(KEY), "", s, flags=re.S)
    m0 = re.search(r'<article class="dt[^"]*"', s)
    s = s[: m0.start()] + build_card(norm, l, solo=True, more_lbl=lbls[1] if len(lbls) > 1 else lbls[0]) + "\n" + s[m0.start() :]
    s = s.replace(f'<body class="dt-solo" data-trip="{TPL}"', f'<body class="dt-solo" data-trip="{KEY}"')
    s = replace_seo(s, f"day-trips/{TPL_SLUG}/", f"day-trips/{SLUG}/")
    s = replace_seo(s, f"img/og/{TPL_SLUG}.jpg", f"img/og/{SLUG}.jpg")
    old_desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    if old_desc_m:
        s = s.replace(f'content="{old_desc_m.group(1)}"', f'content="{esc(trunc(t["p"][0]))}"', 1)
    on, nn = esc(old_name), esc(t["n"])
    s = re.sub(r"<title>" + re.escape(on), lambda mm: "<title>" + nn, s, 1)
    for prop in ['property="og:title"', 'name="twitter:title"', 'property="og:image:alt"']:
        s = re.sub(rf'(<meta {prop} content=")%s' % re.escape(on), lambda mm: mm.group(1) + nn, s, 1)

    def ld(mm):
        d = json.loads(mm.group(1))

        def walk(x):
            if isinstance(x, dict):
                if x.get("@type") == "TouristTrip":
                    x["name"] = t["n"]
                    x["description"] = " ".join(t["p"])[:600]
                    x["image"] = [f"{SITE}/img/og/{SLUG}.jpg"] + [f"{SITE}/img/{i}" for i in IMGS]
                    stops = [p.strip() for p in t["s"].split("·")]
                    if "itinerary" in x:
                        x["itinerary"]["itemListElement"] = [
                            {"@type": "ListItem", "position": i + 1, "item": {"@type": "TouristAttraction", "name": n}}
                            for i, n in enumerate(stops)
                        ]
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
    out.write_text(s, encoding="utf-8")


def sitemap():
    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    if f"day-trips/{SLUG}/" in s:
        # refresh lastmod
        s = re.sub(
            rf"(<loc>https://iraq\.fabletour\.com(?:/[^<]*)?/day-trips/{SLUG}/</loc>\n    <lastmod>)[^<]+",
            r"\g<1>2026-11-11",
            s,
        )
        sm.write_text(s, encoding="utf-8")
        return
    blocks = re.findall(rf"  <url>\n    <loc>[^<]*day-trips/{TPL_SLUG}/</loc>.*?</url>\n", s, flags=re.S)
    if not blocks:
        print("sitemap: no template blocks")
        return
    add = "".join(
        b.replace(f"day-trips/{TPL_SLUG}/", f"day-trips/{SLUG}/")
        .replace(f"img/og/{TPL_SLUG}.jpg", f"img/og/{SLUG}.jpg")
        .replace("<lastmod>2026-10-28</lastmod>", "<lastmod>2026-11-11</lastmod>")
        for b in blocks
    )
    # also bump any other lastmod in copied blocks
    add = re.sub(r"<lastmod>[^<]+</lastmod>", "<lastmod>2026-11-11</lastmod>", add)
    s = s.replace(blocks[-1], blocks[-1] + add, 1)
    sm.write_text(s, encoding="utf-8")
    print("sitemap +", len(blocks))


def patch_llms():
    p = ROOT / "llms.txt"
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8")
    line = f"- [Nippur](https://iraq.fabletour.com/en/day-trips/{SLUG}/): from $150 for the group\n"
    if f"day-trips/{SLUG}/" in s:
        return
    # insert after Babylon (southern archaeological group) if present, else at end of day-trips list
    needle = "- [Babylon](https://iraq.fabletour.com/en/day-trips/babylon/): from $200 for the group\n"
    if needle in s:
        s = s.replace(needle, needle + line, 1)
    else:
        s = s.replace("## Day trips from Baghdad\n", "## Day trips from Baghdad\n\n" + line, 1)
    p.write_text(s, encoding="utf-8")
    print("llms.txt updated")


def patch_chatbot():
    p = ROOT / "chatbot.js"
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8")
    orig = s
    # add nippur (and assyria if the map is still missing it — same SL object)
    def add_sl(m):
        body = m.group(0)
        if f'"{KEY}"' not in body:
            body = body.replace("var SL = {", f'var SL = {{"{KEY}":"{SLUG}",', 1)
            body = body.replace("SL={", f'SL={{"{KEY}":"{SLUG}",', 1)
        if '"assyria"' not in body:
            body = body.replace("var SL = {", 'var SL = {"assyria":"assyria-hatra-nimrud",', 1)
            body = body.replace("SL={", 'SL={"assyria":"assyria-hatra-nimrud",', 1)
        return body
    s = re.sub(r"(?:var SL\s*=\s*)\{[^}]*\}", add_sl, s)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        print("chatbot.js SL updated")


def should_skip(path: pathlib.Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def run():
    homes = {}
    n = 0
    for p in sorted(ROOT.rglob("*.html")):
        if should_skip(p):
            continue
        if f"/day-trips/{SLUG}/" in str(p) or p.match("*/day-trips/nippur/index.html"):
            continue
        try:
            s = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        m = art(s, TPL)
        if not m:
            continue
        l = lang_of(s)
        if l not in D:
            # still patch if the page has day trips; fall back to English copy
            pass
        tpl = m.group(0)
        if "is-solo" in tpl or "<h1" in tpl:
            hc = homes.setdefault(l if l in D else "en", home_card(l if l in D else "en"))
            tpl = hc.replace(img_pre(hc), img_pre(tpl))
        s = insert_card(s, build_card(tpl, l if l in D else "en"))
        s = patch_js(s, l if l in D else "en")
        p.write_text(s, encoding="utf-8")
        n += 1
    print("pages patched:", n)
    for l in D:
        solo_page(l)
    sitemap()
    patch_llms()
    patch_chatbot()
    # links on language homepages + default pax 3, without sweeping add_us_phone
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import add_dt_links
    import add_dt_default_pax
    for f in sorted(ROOT.glob("day-trips/*/index.html")) + sorted(ROOT.glob("*/day-trips/*/index.html")):
        add_dt_links.fix_solo_h1(f)
    for l in ["ar"] + add_dt_links.LANGS:
        if l == "ar":
            for f in [ROOT / "index.html"] + sorted((ROOT / "day-trips").glob("*/index.html")):
                if f.exists():
                    add_dt_links.fix_home(f)
        else:
            for f in [ROOT / l / "index.html", ROOT / l / "airport-transfer" / "index.html"] + sorted((ROOT / l / "day-trips").glob("*/index.html")):
                if f.exists():
                    add_dt_links.fix_home(f)
    files = [ROOT / "index.html"] + [ROOT / l / "index.html" for l in add_dt_links.LANGS]
    total = 0
    for f in files:
        if f.exists():
            a, miss = add_dt_links.process(f)
            total += a
            if a or miss:
                print(f"{f.relative_to(ROOT)}: +{a} links" + (f"  MISSING: {miss}" if miss else ""))
    print("homepage links added:", total)
    add_dt_default_pax.run()


if __name__ == "__main__":
    run()
