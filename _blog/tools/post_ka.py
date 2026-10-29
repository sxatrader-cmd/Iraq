#!/usr/bin/env python3
"""Georgian (ka) pages after add_lang_cs.py ka (Oct 2026):
- Georgia is not in the EU: remove the euro prices copied from the Czech pages (USD only, like English).
- Load Noto Sans/Serif Georgian and turn off uppercase/letter-spacing (Georgian has no case in body text).
Idempotent:  python3 _blog/tools/post_ka.py"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONT = "&family=Noto+Sans+Georgian:wght@400;500;600&family=Noto+Serif+Georgian:wght@600"
CSS = ('<style id="ka-css">'
       'html[lang="ka"] body{font-family:"Inter Tight","Noto Sans Georgian","Sylfaen",sans-serif;line-height:1.8}'
       'html[lang="ka"] .disp,html[lang="ka"] h1,html[lang="ka"] h2,html[lang="ka"] h3,html[lang="ka"] h4{font-family:"Noto Serif Georgian","Noto Sans Georgian","Sylfaen",serif;line-height:1.45}'
       'html[lang="ka"] .eyebrow,html[lang="ka"] .tagline,html[lang="ka"] .day-title .city,html[lang="ka"] .daynum small,'
       'html[lang="ka"] label,html[lang="ka"] th,html[lang="ka"] .btn,html[lang="ka"] button,html[lang="ka"] .kb-date{letter-spacing:0!important;text-transform:none!important}'
       '</style>')


def run():
    files = [ROOT / "ka/index.html"] + sorted((ROOT / "ka/day-trips").glob("*/index.html"))
    for f in files:
        s = f.read_text()
        s = re.sub(r'<style id="eur-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="eur-js">.*?</script>\n?', "", s, flags=re.S)
        s = re.sub(r'<div class="eur-pay" data-eur-note>[^<]*<span class="eur-rate"[^>]*></span></div>', "", s)
        if "Noto+Sans+Georgian" not in s:
            s = re.sub(r'(<link href="https://fonts\.googleapis\.com/css2\?[^"]*?)(&display=swap")', lambda m: m.group(1) + FONT + m.group(2), s, count=1)
        s = re.sub(r'<style id="ka-css">.*?</style>\n?', "", s, flags=re.S)
        s = s.replace("</head>", CSS + "\n</head>", 1)
        f.write_text(s)
    print("ka post-processed:", len(files), "pages")


if __name__ == "__main__":
    run()
