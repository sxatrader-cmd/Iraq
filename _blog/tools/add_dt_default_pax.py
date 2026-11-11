#!/usr/bin/env python3
"""Default every .dt day-trip card calculator to 3 travellers, site-wide.

Applies to language homepages, airport pages, market/landing pages, and
*/day-trips/* pages (plus standalone SEO day-trip pages). Does not change
airport-transfer calculators or the 7-/9-day package prices.

Sets: JS init n=3, the <output> stepper, the visible group total, and (via the
existing upd() on load) the WhatsApp prefill. JSON-LD Offer prices are left as
the starting/1-person totals. Idempotent.

Run after day-trip generators:  python3 _blog/tools/add_dt_default_pax.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = 3
SKIP_PARTS = {".git", "_blog", "node_modules"}
JS_INIT = re.compile(r'(var k=c\.dataset\.trip,n=)\d+(,out=c\.querySelector\("output"\))')
OUTPUT = re.compile(
    r'(<div class="dt-step"><button type="button" data-d="-1" aria-label="−">−</button><output>)\d+(</output><button type="button" data-d="1" aria-label="\+">\+</button></div>)'
)
ART = re.compile(r'(<article class="dt[^"]*" data-trip="([^"]+)">.*?<div class="dt-total">.*?<b dir="ltr">)\$[\d,]+(</b>)', re.S)


def price(k, n):
    if k == "oldtown":
        return 100 if n < 2 else 150 + 50 * (n - 2)
    if k == "ziyara":
        return 50 + 25 * (n - 1)
    if k == "babylon":
        return 200 if n < 2 else 240 + 50 * (n - 2)
    if k == "babylon4":
        return 220 if n < 2 else 260 + 40 * (n - 2)
    if k == "holy":
        return 239 + 30 * max(0, n - 3)
    if k == "south":
        return [300, 325, 350][n - 1] if 1 <= n <= 3 else 350 + 40 * (n - 3)
    if k == "samarra":
        return [150, 200, 225][n - 1] if 1 <= n <= 3 else 225 + 25 * (n - 3)
    if k == "assyria":
        return 500 if n < 2 else 600 if n < 3 else 250 * n
    if k == "madain":
        return 100 + 25 * (n - 1)
    if k == "aqarquf":
        return 50 + 25 * (n - 1)
    if k == "nippur":
        return 150 + 25 * (n - 1)
    raise KeyError(k)


def is_html(p):
    parts = p.relative_to(ROOT).parts
    return p.suffix == ".html" and not (SKIP_PARTS & set(parts))


def targets():
    for p in ROOT.rglob("*.html"):
        if is_html(p):
            yield p


def patch(s):
    s2, n_js = JS_INIT.subn(rf"\g<1>{DEFAULT}\2", s)
    s2, n_out = OUTPUT.subn(rf"\g<1>{DEFAULT}\2", s2)
    unknown = []

    def repl(m):
        k = m.group(2)
        try:
            return m.group(1) + f"${price(k, DEFAULT)}" + m.group(3)
        except KeyError:
            unknown.append(k)
            return m.group(0)

    s2, n_tot = ART.subn(repl, s2)
    return s2, n_js, n_out, n_tot, unknown


def run():
    n = 0
    unknown = []
    for p in targets():
        s = p.read_text()
        if 'class="dt"' not in s and "dataset.trip" not in s:
            continue
        s2, n_js, n_out, n_tot, unk = patch(s)
        unknown.extend((str(p.relative_to(ROOT)), k) for k in unk)
        if s2 != s:
            p.write_text(s2)
            n += 1
    print(f"add_dt_default_pax: {n} pages updated (default {DEFAULT}, site-wide .dt cards)")
    if unknown:
        print(" unknown trip keys:", unknown)
    return n


if __name__ == "__main__":
    run()
