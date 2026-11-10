#!/usr/bin/env python3
"""Vietnamese (vi) pages after add_lang_cs.py vi (Nov 2026):
- Vietnam is not in the EU: remove the euro prices copied from the Czech pages (USD only, like English).
- Libre Baskerville / PT Serif have no Vietnamese letters (ạ, ế, ổ…): headings use Noto Serif (has Vietnamese),
  body text stays Inter Tight (has Vietnamese).
Idempotent:  python3 _blog/tools/post_vi.py"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONT = "&family=Noto+Serif:wght@400;700"
CSS = ('<style id="vi-css">'
       'html[lang="vi"]{--serif-en:"Noto Serif",Georgia,"Times New Roman",serif}'
       'html[lang="vi"] body{line-height:1.7}'
       '</style>')


def run():
    files = [ROOT / "vi/index.html", ROOT / "vi/airport-transfer/index.html"] + sorted((ROOT / "vi/day-trips").glob("*/index.html"))
    n = 0
    for f in files:
        if not f.exists():
            continue
        s = f.read_text()
        s = re.sub(r'<style id="eur-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="eur-js">.*?</script>\n?', "", s, flags=re.S)
        s = re.sub(r'<div class="eur-pay" data-eur-note>[^<]*<span class="eur-rate"[^>]*></span></div>', "", s)
        if "Noto+Serif:" not in s:
            s = re.sub(r'(<link href="https://fonts\.googleapis\.com/css2\?[^"]*?)(&display=swap")', lambda m: m.group(1) + FONT + m.group(2), s, count=1)
        s = re.sub(r'<style id="vi-css">.*?</style>\n?', "", s, flags=re.S)
        s = s.replace("</head>", CSS + "\n</head>", 1)
        f.write_text(s); n += 1
    print("vi post-processed:", n, "pages")


if __name__ == "__main__":
    run()
    import add_us_phone; add_us_phone.run()  # US/Canada 24/7 line on every page (footer + JSON-LD)
