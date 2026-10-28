#!/usr/bin/env python3
"""Builds a new language version of the Iraq site (homepage + every day-trip page) from the
CZECH pages, which already carry every section (day trips, airport transfer, holy shrines,
gallery, FAQ, euro prices…), using a Czech→language dictionary, then links the new language
from every page (hreflang, language menu, footer links, og:locale) and the sitemap.

Used for Slovak, Croatian and Romanian (Oct 2026):  python3 _blog/tools/add_lang_cs.py sk hr ro
Translations: _blog/tools/pages_i18n/<lang>.from-cs.json  ({"<Czech text>": "<translation>"})
Idempotent: re-running rebuilds the pages of the given languages from Czech.
The Karbala story section is not on the Czech pages, so new languages don't get it."""
import re, json, html, sys, pathlib
import add_lang as A

ROOT, BASE, I18N = A.ROOT, A.BASE, A.I18N
SRC = "cs"
NEW = {
    "sk": ("Slovenčina", "Sk", "sk_SK", "sk"),
    "hr": ("Hrvatski", "Hr", "hr_HR", "hr"),
    "ro": ("Română", "Ro", "ro_RO", "ro"),
}
A.META.update(NEW)
for l in NEW:
    if l not in A.ORDER:
        A.ORDER.append(l)


def cs_trips():
    s = (ROOT / SRC / "index.html").read_text()
    return [[html.unescape(p).strip() for p in re.findall(r'<p>(.*?)</p>', m.group(1), flags=re.S)]
            for m in re.finditer(r'<div class="dt-more"[^>]*>(.*?)</div>', s, flags=re.S)]


def tr_plain(p, M, lang, trips):
    core = p.strip()
    if core in M:
        return p.replace(core, M[core])
    parts = re.findall(r'<p>(.*?)</p>', core, flags=re.S)
    if parts and all(x in M for x in parts) and core == "".join(f"<p>{x}</p>" for x in parts):
        return "".join(f"<p>{M[x]}</p>" for x in parts)
    if f"/{SRC}/" in core and " " not in core:          # URLs and paths
        return p.replace(f"/{SRC}/", f"/{lang}/")
    gal = M.get("Z našich cest po Iráku")
    m = re.match(r'^Z našich cest po Iráku – (\d+)$', core)
    if m and gal:
        return f"{gal} – {m.group(1)}"
    for paras in trips:                                  # truncated descriptions (meta 157 chars, JSON-LD 600)
        if not all(x in M for x in paras):
            continue
        full = " ".join(paras)
        t = " ".join(M[x] for x in paras)
        if core.endswith("…") and full.startswith(core[:-1].rstrip()):
            cut = t[:157]
            cut = cut[:cut.rfind(" ")] if len(t) > 157 else t
            return cut.rstrip(" ,;:—") + "…"
        if len(core) >= 300 and full.startswith(core):
            return t[:len(core)]
    return None


def build_page(lang, rel, M, trips, unknown):
    s = (ROOT / SRC / rel).read_text()
    toks = A.tokenize(s)
    for t in toks:
        k, v = t
        if k == "C" or not re.search(r'[^\W\d_]', v):
            continue
        if k == "Q":
            tr = M.get(v.strip())
            if tr:
                t[1] = v.replace(v.strip(), tr)
            continue
        try:
            p = A.norm(k, v)
        except Exception:
            continue
        tr = tr_plain(p, M, lang, trips)
        if tr is None:
            if re.search(r'[À-ž]', p):
                unknown.add(p[:90])
            continue
        t[1] = A.enc(k, tr, v)
    out = "".join(v for _, v in toks)
    name, short, loc, hl = NEW[lang]
    # keep the links that point to the Czech version itself
    keep = []
    def mask(m):
        keep.append(m.group(0)); return f"\x00{len(keep)-1}\x00"
    out = re.sub(rf'<link rel="alternate" hreflang="{SRC}" href="[^"]*">', mask, out)
    out = re.sub(rf'<a href="[^"]*" hreflang="{SRC}" lang="{SRC}"[^>]*>[^<]*</a>', mask, out)
    out = re.sub(rf'<option value="{SRC}"[^>]*>[^<]*</option>', mask, out)
    out = out.replace(f'<html lang="{SRC}"', f'<html lang="{lang}"', 1)
    out = out.replace(f'/{SRC}/', f'/{lang}/')
    out = out.replace(f'"{SRC}": ', f'"{lang}": ')
    out = out.replace(f'let lang = "{SRC}"', f'let lang = "{lang}"')
    out = out.replace(f'"inLanguage": "{SRC}"', f'"inLanguage": "{lang}"')
    out = out.replace('<meta property="og:locale" content="cs_CZ">',
                      f'<meta property="og:locale" content="{loc}">\n<meta property="og:locale:alternate" content="cs_CZ">', 1)
    out = out.replace(f'<meta property="og:locale:alternate" content="{loc}">\n', "")
    out = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], out)
    out = re.sub(rf'(<option value="{SRC}") selected', r'\1', out)
    out = re.sub(rf'(<a href="[^"]*" hreflang="{SRC}" lang="{SRC}") aria-current="page"', r'\1', out)
    return out


def run(langs):
    trips = cs_trips()
    for lang in langs:
        M = json.loads((I18N / f"{lang}.from-cs.json").read_text())
        unknown = set()
        for rel in A.pages():
            f = ROOT / lang / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(build_page(lang, rel, M, trips, unknown))
        if unknown:
            print(f"[{lang}] untranslated:", *sorted(unknown)[:60], sep="\n  ")
        print("built", lang)
    for d in A.all_dirs():
        for rel in A.pages():
            f = ROOT / d / rel
            if f.exists():
                cur = d.strip("/") or "ar"
                f.write_text(A.add_links(f.read_text(), rel, cur))
    A.sitemap()


if __name__ == "__main__":
    run(sys.argv[1:] or list(NEW))
