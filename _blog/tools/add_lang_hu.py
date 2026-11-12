#!/usr/bin/env python3
"""Hungarian (hu) version of the Iraq site (Nov 2026), built from the Czech pages with
pages_i18n/hu.from-cs.json (Czech text -> Hungarian), like add_lang_cs.py, but for every page
of a language: homepage, airport transfer, all day trips and the three programme pages.

Hungarian-only changes:
- the Karbala story section (Czech-subtitled video) and the Czech-market banner are removed;
- the top video (#video) is Saif's own video of his first group from Budapest, hosted in this repo
  (/video/budapest-guests-hungary.mp4), in the same place as the French short on the French page;
- the videos of the English homepage that the Czech page lacks are added (9-day programme video,
  airport pickup video, "Travel Iraq with Fable Tour").
Then hu is linked from every page (hreflang, language menu, og:locale, inLanguage) and the sitemap.

Run:  python3 _blog/tools/add_lang_hu.py      (idempotent: rebuilds /hu/ from Czech)"""
import re, json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import add_lang as A
import add_lang_cs as C

ROOT, BASE = A.ROOT, A.BASE
LANG = "hu"
C.NEW[LANG] = ("Magyar", "Hu", "hu_HU", "hu")
A.META[LANG] = C.NEW[LANG]
if LANG not in A.ORDER:
    A.ORDER.append(LANG)

VIDEO = "/video/budapest-guests-hungary.mp4"
POSTER = "/video/budapest-guests-hungary.jpg"


def pages():
    src = ROOT / C.SRC
    return (["index.html", "airport-transfer/index.html"]
            + sorted(str(p.relative_to(src)) for p in src.glob("day-trips/*/index.html"))
            + sorted(str(p.relative_to(src)) for p in src.glob("tours/*/index.html")))


def strip_cs(s):
    s = re.sub(r'\s*<!-- =+ START: KARBALA SECTION =+ -->.*?<!-- =+ END: KARBALA SECTION =+ -->', '', s, flags=re.S)
    s = re.sub(r'\s*<div class="czechia-banner">.*?</div>', '', s, flags=re.S)
    s = re.sub(r'<style id="czechia-banner-css">.*?</style>\s*', '', s, flags=re.S)
    return s


def yt(vid, title, cls, style=""):
    st = f' style="{style}"' if style else ""
    return (f'<div class="{cls}"{st}><iframe src="https://www.youtube-nocookie.com/embed/{vid}?rel=0&amp;modestbranding=1&amp;playsinline=1" '
            f'title="{title}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>')


def videos(s):
    """homepage only: Budapest video on top + the English homepage's extra videos"""
    top = ('<section class="block in" style="padding-bottom:0" id="video">\n'
           '    <div class="sec-head"><span class="eyebrow">Videó</span><h2 class="disp">Első csoportunk Budapestről</h2>'
           '<p>Gábor és útitársai mesélnek iraki utazásukról a Fable Tourral.</p></div>\n'
           '    <div class="vid" style="max-width:860px;margin:0 auto"><video controls playsinline preload="metadata" poster="' + POSTER + '" '
           'title="Első csoportunk Budapestről – Fable Tour Irak"><source src="' + VIDEO + '" type="video/mp4"></video></div>\n'
           '  </section>')
    s, n = re.subn(r'<section class="block in" style="padding-bottom:0" id="video">.*?</section>', lambda m: top, s, count=1, flags=re.S)
    assert n == 1, "no #video section"
    css = ('<style id="hu-video-css">.vid video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;border:0}</style>\n')
    if 'id="hu-video-css"' not in s:
        s = s.replace("</head>", css + "</head>", 1)
    # VideoObject for search engines
    ld = {"@context": "https://schema.org", "@type": "VideoObject",
          "name": "Első csoportunk Budapestről – Fable Tour Irak",
          "description": "Magyar utazók Budapestről mesélnek iraki körútjukról a Fable Tourral.",
          "thumbnailUrl": BASE + POSTER, "contentUrl": BASE + VIDEO, "uploadDate": "2026-11-12",
          "duration": "PT47S", "inLanguage": "en",
          "publisher": {"@type": "Organization", "name": "Fable Tour", "logo": {"@type": "ImageObject", "url": BASE + "/logo.png"}}}
    if '"VideoObject"' not in s:
        s = s.replace("</head>", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n</head>", 1)
    # 9-day programme video: first item in the 2nd programme block (as on the English page)
    if "MSFPSNenMOY" not in s:
        i = s.index('id="tour-9-days"')
        j = s.index('<div class="pblock">', i) + len('<div class="pblock">')
        s = s[:j] + "\n    " + yt("MSFPSNenMOY", "9 napos iraki körút a Fable Tourral", "vid vert",
                                   "aspect-ratio:9/16;max-width:360px;margin:0 auto 22px") + s[j:]
    # airport pickup video
    if "wJ_5nrtDy1s" not in s:
        m = re.search(r'<ul class="ap-inc">[^\n]*\n', s)
        s = s[:m.end()] + "          " + yt("wJ_5nrtDy1s", "Felvétel a bagdadi repülőtéren a Fable Tourral", "vid vert xvid ap-vid") + "\n" + s[m.end():]
    # "Travel Iraq with Fable Tour", before the gallery
    if "nWEGqKHTc8M" not in s:
        k = s.index('<section class="block in gal-wrap" style="padding-top:0" id="gallery">')
        sec = ('<section class="block in" style="padding-top:0" id="video-journeys"><div class="sec-head"><span class="eyebrow">Videó</span>'
               '<h2 class="disp">Utazzon Irakba a Fable Tourral</h2></div>'
               + yt("nWEGqKHTc8M", "Utazzon Irakba a Fable Tourral", "vid", "max-width:860px;margin:0 auto") + '</section>\n      ')
        s = s[:k] + sec + s[k:]
    return s


def build(rel, M, trips, unknown):
    src = ROOT / C.SRC / rel
    orig = src.read_text()
    tmp = strip_cs(orig)
    src.write_text(tmp)                       # build_page reads the Czech file itself
    try:
        out = C.build_page(LANG, rel, M, trips, unknown)
    finally:
        src.write_text(orig)
    out = out.replace('<meta property="og:locale" content="hu_HU">\n<meta property="og:locale:alternate" content="cs_CZ">',
                      '<meta property="og:locale" content="hu_HU">', 1)
    if rel == "index.html":
        out = videos(out)
    return out


def add_links_all():
    """adds hu next to vi on every page of the language sets"""
    rels = pages()
    for d in A.all_dirs() + ["ckb/", "zh-tw/"]:
        for rel in rels:
            f = ROOT / d / rel
            if f.exists():
                cur = d.strip("/") or "ar"
                s = f.read_text()
                n = A.add_links(s, rel, cur if cur in A.ORDER else "x")
                f.write_text(n)


def sitemap():
    """hu next to vi in every (non-blog) <url> block whose page exists in Hungarian, plus the hu <url> entries"""
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    def blk(b):
        if "/blog" in b or 'hreflang="hu"' in b:
            return b
        m = re.search(r'(    <xhtml:link rel="alternate" hreflang="vi" href="https://iraq\.fabletour\.com/vi/([^"]*)"/>\n)', b)
        if not m or not (ROOT / LANG / m.group(2) / "index.html").exists():
            return b
        return b.replace(m.group(1), m.group(1) + m.group(1).replace('hreflang="vi"', f'hreflang="{LANG}"').replace("/vi/", f"/{LANG}/"), 1)
    s = re.sub(r'  <url>\n.*?</url>\n', lambda m: blk(m.group(0)), s, flags=re.S)
    add = ""
    for b in re.findall(r'  <url>\n    <loc>https://iraq\.fabletour\.com/vi/[^<]*</loc>.*?</url>\n', s, flags=re.S):
        if "/blog" in b:
            continue
        loc = re.search(r"<loc>([^<]*)</loc>", b).group(1).replace("/vi/", f"/{LANG}/")
        if f"<loc>{loc}</loc>" not in s and (ROOT / loc.split(".com/", 1)[1] / "index.html").exists():
            add += b.replace(b[b.index("<loc>"):b.index("</loc>")], "<loc>" + loc, 1)
    if add:
        i = s.index("<!-- blog:start -->") if "<!-- blog:start -->" in s else s.rindex("</urlset>")
        s = s[:i] + add + s[i:]
    sm.write_text(s)


def main():
    M = json.loads((A.I18N / f"{LANG}.from-cs.json").read_text())
    trips = C.cs_trips()
    unknown = set()
    for rel in pages():
        f = ROOT / LANG / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(build(rel, M, trips, unknown))
    if unknown:
        print("untranslated:", *sorted(unknown)[:80], sep="\n  ")
    add_links_all()
    sitemap()
    import seo_local
    seo_local.apply(LANG, seo_local.L[LANG])
    import footer_sites; footer_sites.run()
    import add_us_phone; add_us_phone.run()
    import add_dt_default_pax; add_dt_default_pax.run()
    print("built", LANG)


if __name__ == "__main__":
    main()
