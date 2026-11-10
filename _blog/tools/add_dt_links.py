#!/usr/bin/env python3
"""Makes the day-trip cards and the airport-transfer card on every language homepage
link to their own product pages with real <a href> tags (crawlable internal links).

- Day-trip card: <h3>Title</h3>  ->  <h3><a class="dt-tl" href="<HOME>day-trips/<slug>/">Title</a></h3>
  (slug read from the page's own <script id="dtx"> SL map; HOME = the page's language folder)
- Airport card: adds <a class="ap-pg" href="<HOME>airport-transfer/">title</a> next to "Copy link".
Copy-link buttons and the look of the cards are unchanged (links inherit the heading colour).
Only product pages (day-trips, airport-transfer) are linked; never market/landing pages.
Also keeps day-trip pages at one H1 (fix_solo_h1) and the copy-link HOME per language (fix_home).
Idempotent. Run after add_lang.py / add_airport.py / add_ziyara.py / add_assyria.py whenever
homepages are rebuilt:   python3 _blog/tools/add_dt_links.py"""
import re, json, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LANGS = ["ckb", "cs", "da", "de", "el", "en", "es", "fa", "fi", "fr", "hi", "hr", "id", "it", "ja", "ka", "ko",
         "ms", "nl", "no", "pl", "pt", "ro", "ru", "sk", "sv", "ta", "th", "tr", "ur", "vi", "zh", "zh-tw"]
DT_STYLE = "color:inherit;text-decoration:none"
AP_STYLE = "margin-inline-start:14px;color:var(--navy);font-weight:600;font-size:14px"

def target_exists(href):
    return (ROOT / href.strip("/") / "index.html").exists()

def process(path):
    s = path.read_text(encoding="utf-8")
    m = re.search(r'<script id="dtx">.*?HOME="([^"]+)",SL=(\{[^}]*\})', s, flags=re.S)
    if not m:
        return 0, []
    sl = json.loads(m.group(2))
    # HOME from the file location (language folder)
    rel = path.relative_to(ROOT).parent.as_posix()
    home = "/" if rel in ("", ".") else f"/{rel}/"
    added, missing = 0, []

    def dt_card(mm):
        nonlocal added
        art = mm.group(0)
        k = mm.group(1)
        if k not in sl or 'class="dt-tl"' in art:
            return art
        href = f"{home}day-trips/{sl[k]}/"
        if not target_exists(href):
            missing.append(href); return art
        new, n = re.subn(r'<h3>(.*?)</h3>',
                         lambda h: f'<h3><a class="dt-tl" href="{href}" style="{DT_STYLE}">{h.group(1)}</a></h3>',
                         art, count=1, flags=re.S)
        added += n
        return new

    sec_start = s.find('id="day-trips"')
    if sec_start != -1:
        sec_end = s.find('</section>', sec_start)
        sec = re.sub(r'<article class="dt" data-trip="([a-z0-9]+)">.*?</article>', dt_card, s[sec_start:sec_end], flags=re.S)
        s = s[:sec_start] + sec + s[sec_end:]

    ap = re.search(r'(<p class="ap-cpw"><button type="button" class="dt-cp ap-cp" data-url="([^"]+)".*?</button>)(</p>)', s, flags=re.S)
    if ap and 'class="ap-pg"' not in s:
        href = f"{home}airport-transfer/"
        tm = re.search(r'id="airport-transfer">.*?<button class="ap-toggle".*?<b>(.*?)</b>', s, flags=re.S)
        title = tm.group(1) if tm else html.escape("Airport transfer")
        if target_exists(href):
            s = s[:ap.end(1)] + f'<a class="ap-pg" href="{href}" style="{AP_STYLE}">{title}</a>' + s[ap.end(1):]
            added += 1
        else:
            missing.append(href)
    path.write_text(s, encoding="utf-8")
    return added, missing

def fix_home(path):
    """the copy-link script (<script id="dtx">) must use the page's own language home,
    e.g. /ckb/ pages were built from the Arabic root and kept HOME="/" (copied Arabic URLs)"""
    parts = path.relative_to(ROOT).parts
    lang = parts[0] if parts[0] in LANGS else ""
    home = f"/{lang}/" if lang else "/"
    s = path.read_text(encoding="utf-8")
    t = re.sub(r'(<script id="dtx">.*?HOME=")[^"]*(",SL=)', lambda m: m.group(1) + home + m.group(2), s, count=1, flags=re.S)
    if t != s:
        path.write_text(t, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: HOME -> {home}")

HERO_CSS_OLD = ".hero-band h1{font-size:clamp(30px,5.2vw,44px);line-height:1.25;margin:10px 0 12px;color:#fff}"
HERO_CSS_NEW = (".hero-band h1,.hero-band .hero-h1{font-size:clamp(30px,5.2vw,44px);line-height:1.25;margin:10px 0 12px;color:#fff}"
                ".hero-band .hero-h1{text-wrap:balance}")

def fix_solo_h1(path):
    """day-trip pages: the generic hero title ("Iraq: a journey through Mesopotamia") is a <div class="hero-h1">
    with the same look, so the trip name (<h1 class="dt-h">) is the page's only H1"""
    s = path.read_text(encoding="utf-8")
    if '<h1 class="dt-h">' not in s:
        return
    t = re.sub(r'<h1 class="disp" data-i="h1">(.*?)</h1>', r'<div class="disp hero-h1" data-i="h1">\1</div>', s, count=1, flags=re.S)
    if HERO_CSS_NEW not in t:
        t = t.replace(HERO_CSS_OLD, HERO_CSS_NEW, 1)
    if t != s:
        path.write_text(t, encoding="utf-8")

def run():
    for f in sorted(ROOT.glob("day-trips/*/index.html")) + sorted(ROOT.glob("*/day-trips/*/index.html")):
        fix_solo_h1(f)
    for l in LANGS:
        for f in [ROOT / l / "index.html", ROOT / l / "airport-transfer" / "index.html"] + sorted((ROOT / l / "day-trips").glob("*/index.html")):
            if f.exists():
                fix_home(f)
    files = [ROOT / "index.html"] + [ROOT / l / "index.html" for l in LANGS]
    total = 0
    for f in files:
        if not f.exists():
            continue
        a, miss = process(f)
        total += a
        print(f"{f.relative_to(ROOT)}: +{a} links" + (f"  MISSING TARGETS: {miss}" if miss else ""))
    print("total links added:", total)

if __name__ == "__main__":
    run()
