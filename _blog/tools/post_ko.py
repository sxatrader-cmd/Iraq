#!/usr/bin/env python3
"""Korean (ko) pages after add_lang_cs.py ko (Oct 2026):
- Korea is not in the EU: remove the euro prices copied from the Czech pages (USD only, like English).
- Load Noto Sans/Serif KR, keep Korean words whole when lines wrap (word-break: keep-all)
  and turn off uppercase/letter-spacing on small labels.
No "travellers from Korea" content: South Korea bans its citizens from travelling to Iraq.
Idempotent:  python3 _blog/tools/post_ko.py"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONT = "&family=Noto+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600"
CSS = ('<style id="ko-css">'
       'html[lang="ko"] body{font-family:"Inter Tight","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;line-height:1.75;word-break:keep-all;overflow-wrap:anywhere}'
       'html[lang="ko"] .disp,html[lang="ko"] h1,html[lang="ko"] h2,html[lang="ko"] h3,html[lang="ko"] h4{font-family:"Noto Serif KR","Noto Sans KR",serif;line-height:1.4;word-break:keep-all}'
       'html[lang="ko"] .eyebrow,html[lang="ko"] .tagline,html[lang="ko"] .day-title .city,html[lang="ko"] .daynum small,'
       'html[lang="ko"] label,html[lang="ko"] th,html[lang="ko"] .btn,html[lang="ko"] button,html[lang="ko"] .kb-date{letter-spacing:0!important;text-transform:none!important}'
       '</style>')


def run():
    files = [ROOT / "ko/index.html", ROOT / "ko/airport-transfer/index.html"] + sorted((ROOT / "ko/day-trips").glob("*/index.html"))
    for f in files:
        if not f.exists():
            continue
        s = f.read_text()
        s = re.sub(r'<style id="eur-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="eur-js">.*?</script>\n?', "", s, flags=re.S)
        s = re.sub(r'<div class="eur-pay" data-eur-note>[^<]*<span class="eur-rate"[^>]*></span></div>', "", s)
        if "Noto+Sans+KR" not in s:
            s = re.sub(r'(<link href="https://fonts\.googleapis\.com/css2\?[^"]*?)(&display=swap")', lambda m: m.group(1) + FONT + m.group(2), s, count=1)
        s = s.replace('data-l="Kopírovat odkaz"', 'data-l="링크 복사"').replace('data-ok="Odkaz zkopírován ✓"', 'data-ok="링크가 복사되었습니다 ✓"')
        s = re.sub(r'<style id="ko-css">.*?</style>\n?', "", s, flags=re.S)
        s = s.replace("</head>", CSS + "\n</head>", 1)
        f.write_text(s)
    print("ko post-processed:", len(files), "pages")


if __name__ == "__main__":
    run()
