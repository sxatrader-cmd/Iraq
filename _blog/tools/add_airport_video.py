#!/usr/bin/env python3
"""YouTube Short of the Baghdad airport pickup, shown inside the airport-transfer section
(under the booking card) on the ENGLISH homepage only. Idempotent; re-run after add_airport.py."""
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
    i = s.index('id="ap-body"')
    j = s.index('<div class="ap-card">', i)
    # end of the ap-card block = the </div> that closes #ap-body, minus one level
    end = s.index("\n    </div>\n  </section>", j)
    s = s[:end] + "\n      " + HTML + s[end:]
    f.write_text(s)
    print("ok", f.relative_to(ROOT))
