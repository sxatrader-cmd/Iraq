#!/usr/bin/env python3
"""YouTube Short of the Baghdad airport pickup, shown inside the airport-transfer section
(under the photo, just above the booking form) on the ENGLISH homepage only. Idempotent; re-run after add_airport.py."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
VID = "wJ_5nrtDy1s"
PAGES = [ROOT / "en" / "index.html"]
HTML = (f'<div class="vid vert xvid ap-vid"><iframe src="https://www.youtube-nocookie.com/embed/{VID}?rel=0&amp;modestbranding=1&amp;playsinline=1" '
        'title="Baghdad Airport pickup with Fable Tour" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>')

for f in PAGES:
    s = f.read_text()
    s = re.sub(r'\s*<div class="vid vert xvid ap-vid">.*?</div>', "", s, flags=re.S)
    # inside the card, under the photo and just above the booking form
    i = s.index('id="ap-body"')
    j = s.index('<div class="ap-form">', i)
    s = s[:j] + HTML + "\n          " + s[j:]
    if 'id="apvid-css"' not in s:
        s = s.replace("</head>", '<style id="apvid-css">.ap-in .ap-vid{margin:4px auto 20px!important;max-width:300px}</style>\n</head>', 1)
    f.write_text(s)
    print("ok", f.relative_to(ROOT))
