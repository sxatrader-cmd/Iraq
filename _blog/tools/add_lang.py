#!/usr/bin/env python3
"""Builds a new language version of the Iraq site (homepage + every day-trip page)
from the English pages and a translation file, then links it from every page
(hreflang, language menu, footer language links, og:locale) and the sitemap.

Usage:  python3 _blog/tools/add_lang.py fi sv da no
Translations: _blog/tools/pages_i18n/<lang>.json  ({"<id>": "text"}, ids from src.json)
Idempotent: re-running rebuilds the pages of the given languages from English.
After rebuilding run add_airport.py, then add_euro.py."""
import re, json, html, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = pathlib.Path(__file__).parent
I18N = TOOLS / "pages_i18n"
BASE = "https://iraq.fabletour.com"

# native name, short label, og:locale, hreflang
META = {
    "fi": ("Suomi", "Fi", "fi_FI", "fi"),
    "sv": ("Svenska", "Sv", "sv_SE", "sv"),
    "da": ("Dansk", "Da", "da_DK", "da"),
    "no": ("Norsk", "No", "nb_NO", "no"),
}
ORDER = ["ar", "en", "tr", "ru", "de", "fr", "es", "it", "el", "cs", "pl", "zh", "ja", "fa",
         "ms", "id", "th", "hi", "ur", "ta", "fi", "sv", "da", "no"]
# extra strings that are built, not translated one by one
DT = {"fi": "Päiväretket Bagdadista", "sv": "Dagsutflykter från Bagdad",
      "da": "Dagsture fra Bagdad", "no": "Dagsturer fra Bagdad"}

ATTR = r'(?:alt|title|aria-label|content|placeholder|data-alt|data-cap|data-show|data-hide|data-l|data-ok|label)'


def tokenize(s):
    out, pos = [], 0
    for m in re.finditer(r'(<script\b[^>]*>)(.*?)(</script>)|(<style\b[^>]*>.*?</style>)|(<[^>]+>)', s, flags=re.S):
        if m.start() > pos:
            out.append(["T", s[pos:m.start()]])
        if m.group(1):
            out.append(["C", m.group(1)])
            js, p2 = m.group(2), 0
            for sm in re.finditer(r'"(?:\\.|[^"\\\n])*"|`(?:\\.|[^`\\])*`', js):
                if sm.start() > p2:
                    out.append(["C", js[p2:sm.start()]])
                lit = sm.group(0)
                if lit[0] == '`':
                    for part in re.split(r'(\$\{[^}]*\})', lit):
                        out.append(["C" if part.startswith('${') or not re.search(r'[^\W\d_]', part) else "Q", part])
                else:
                    out.append(["S", lit])
                p2 = sm.end()
            out += [["C", js[p2:]], ["C", m.group(3)]]
        elif m.group(4):
            out.append(["C", m.group(4)])
        else:
            tag, p2 = m.group(5), 0
            for am in re.finditer(r'(\b' + ATTR + r'=")([^"]*)(")', tag):
                out.append(["C", tag[p2:am.end(1)]])
                out.append(["A", am.group(2)])
                p2 = am.start(3)
            out.append(["C", tag[p2:]])
        pos = m.end()
    out.append(["T", s[pos:]])
    return [t for t in out if t[1] != ""]


def norm(kind, v):
    if kind == "S":
        return json.loads('"' + v[1:-1].replace("\\'", "'") + '"')
    return html.unescape(v)


def enc(kind, plain, orig):
    if kind == "S":
        return json.dumps(plain, ensure_ascii=False)
    esc = plain.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if kind == "A":
        return esc.replace('"', "&quot;")
    lead = re.match(r'^\s*', orig).group(0)
    trail = re.search(r'\s*$', orig).group(0)
    return lead + esc.strip() + trail


def load_map(lang):
    src = json.loads((I18N / "src.json").read_text())
    tr = json.loads((I18N / f"{lang}.json").read_text())
    missing = [i for i in range(len(src)) if str(i) not in tr]
    if missing:
        sys.exit(f"{lang}: missing translations {missing[:10]}")
    return {src[i]: tr[str(i)] for i in range(len(src))}


def paragraphs(en_html):
    """the long trip descriptions: list of (english paragraphs) per trip, from the English homepage"""
    s = (ROOT / "en/index.html").read_text()
    out = []
    for m in re.finditer(r'<div class="dt-more"[^>]*>(.*?)</div>', s, flags=re.S):
        out.append([html.unescape(p).strip() for p in re.findall(r'<p>(.*?)</p>', m.group(1), flags=re.S)])
    lead = [html.unescape(p).strip() for p in re.findall(r'<p class="dt-lead">(.*?)</p>', s, flags=re.S)]
    return out, lead


def translate_plain(p, M, lang, trips):
    """returns the translation of an English plain string, or None if it is not text"""
    if p.strip() in M:
        core = p.strip()
        return p.replace(core, M[core])
    if p.startswith("<p>"):
        parts = re.findall(r'<p>(.*?)</p>', p, flags=re.S)
        if parts and all(x in M for x in parts):
            return "".join(f"<p>{M[x]}</p>" for x in parts)
    if p == "en":
        return lang
    if p == "/en/":
        return f"/{lang}/"
    if p.startswith(BASE + "/en/"):
        return p.replace(BASE + "/en/", f"{BASE}/{lang}/", 1)
    if p == "en_US":
        return META[lang][2]
    m = re.match(r'^(.*) \| Day trips from Baghdad \| Fable Tour$', p)
    if m and m.group(1) in M:
        return f"{M[m.group(1)]} | {DT[lang]} | Fable Tour"
    m = re.match(r'^(.*) — Day trips from Baghdad$', p)
    if m and m.group(1) in M:
        return f"{M[m.group(1)]} — {DT[lang]}"
    # truncated trip descriptions (meta description "…", JSON-LD 600 chars)
    for paras in trips:
        if not all(x in M for x in paras):
            continue  # section added later by its own tool (add_ziyara.py etc.)
        full = " ".join(paras)
        if p.endswith("…") and full.startswith(p[:-1].rstrip()):
            t = " ".join(M[x] for x in paras)
            cut = t[:157]
            cut = cut[:cut.rfind(" ")] if len(t) > 157 else t
            return cut.rstrip(" ,;:—") + "…"
        if len(p) >= 300 and full.startswith(p):
            return " ".join(M[x] for x in paras)[:len(p)]
    return None


def build_page(lang, rel, M, trips, unknown):
    s = (ROOT / "en" / rel).read_text()
    toks = tokenize(s)
    for t in toks:
        k, v = t
        if k == "C" or not re.search(r'[A-Za-z]', v):
            continue
        if k == "Q":
            p = v
            tr = M.get(p.strip())
            if tr:
                t[1] = v.replace(p.strip(), tr)
            continue
        try:
            p = norm(k, v)
        except Exception:
            continue
        tr = translate_plain(p, M, lang, trips)
        if tr is None:
            if re.search(r'[a-z]{3}', p) and k != "S" or (k == "S" and " " in p):
                unknown.add(p[:90])
            continue
        t[1] = enc(k, tr, v)
    out = "".join(v for _, v in toks)
    # markup that is not text
    out = out.replace('<html lang="en"', f'<html lang="{lang}"', 1)
    out = out.replace('<base href="/en/">', f'<base href="/{lang}/">')
    out = out.replace(f'<link rel="canonical" href="{BASE}/en/', f'<link rel="canonical" href="{BASE}/{lang}/')
    out = re.sub(r'(<option value="en") selected', r'\1', out)
    out = re.sub(r'(<a href="[^"]*" hreflang="en" lang="en") aria-current="page"', r'\1', out)
    out = re.sub(r'(<a href="[^"]*/en/[^"]*day-trips/[^"]*")', lambda m: m.group(1).replace("/en/", f"/{lang}/"), out)
    out = out.replace('HOME="/en/"', f'HOME="/{lang}/"')
    out = out.replace('href="/en/blog/"', f'href="/{lang}/blog/"')
    return out


def add_links(s, rel, cur):
    """adds the new languages to hreflang links, language menu, footer links and og:locale of one page"""
    sub = rel.replace("index.html", "")
    for lang in [l for l in ORDER if l in META]:
        name, short, loc, hl = META[lang]
        if f'hreflang="{hl}" href="{BASE}/' in s:
            continue
        prev = ORDER[ORDER.index(lang) - 1]
        prev_hl = "zh-Hans" if prev == "zh" else prev
        # <link rel="alternate">
        s = re.sub(rf'(<link rel="alternate" hreflang="{prev_hl}" href="{BASE}/{prev}/{re.escape(sub)}">\n?)',
                   lambda m: m.group(1) + (m.group(1).replace(f'hreflang="{prev_hl}"', f'hreflang="{hl}"')
                                           .replace(f"{BASE}/{prev}/", f"{BASE}/{lang}/")), s, count=1)
        # language select
        s = re.sub(rf'(<option value="{prev}"[^>]*>[^<]*</option>\n?)',
                   lambda m: m.group(1) + f'<option value="{lang}"' + (" selected" if lang == cur else "") +
                   f' title="{name}">{short}</option>' + ("\n" if m.group(1).endswith("\n") else ""), s, count=1)
        # footer language links
        def foot(m):
            a = m.group(0)
            href = re.search(r'href="([^"]*)"', a).group(1).replace(f"/{prev}/", f"/{lang}/")
            cur_attr = ' aria-current="page"' if lang == cur else ""
            return a + f'<a href="{href}" hreflang="{hl}" lang="{hl}"{cur_attr} title="{name}">{short}</a>'
        s = re.sub(rf'<a href="[^"]*" hreflang="{prev}" lang="{prev}"[^>]*>[^<]*</a>', foot, s, count=1)
        # og:locale:alternate
        if cur != lang and f'content="{loc}"' not in s:
            s = re.sub(r'(<meta property="og:locale:alternate" content="ta_IN">)',
                       lambda m: m.group(1) + f'\n<meta property="og:locale:alternate" content="{loc}">', s, count=1)
    if cur in META:
        s = s.replace('<meta property="og:locale:alternate" content="en_US">', "")
        if 'og:locale:alternate" content="en_US"' not in s:
            s = s.replace('<meta property="og:locale:alternate" content="ar_AR">',
                          '<meta property="og:locale:alternate" content="en_US">\n<meta property="og:locale:alternate" content="ar_AR">', 1)
    # schema.org inLanguage of the website
    s = re.sub(r'("inLanguage": \[)([^\]]*)\]', lambda m: m.group(1) + ", ".join(f'"{x}"' for x in ORDER) + "]", s)
    return s


def pages():
    return ["index.html"] + [f"day-trips/{d.name}/index.html" for d in sorted((ROOT / "en/day-trips").iterdir())]


def all_dirs():
    return [""] + [l + "/" for l in ORDER if l != "ar"]


def sitemap():
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    blocks = re.findall(r'  <url>\n    <loc>[^<]*</loc>.*?</url>\n', s, flags=re.S)
    for b in blocks:
        loc = re.search(r'<loc>([^<]*)</loc>', b).group(1)
        if "/blog" in loc or 'hreflang="ta"' not in b:
            continue
        nb = b
        for lang in META:
            hl = META[lang][3]
            if f'hreflang="{hl}"' in nb:
                continue
            nb = re.sub(r'(    <xhtml:link rel="alternate" hreflang="(\w+)" href="([^"]*)"/>\n)(    <xhtml:link rel="alternate" hreflang="x-default")',
                        lambda m: m.group(1) + f'    <xhtml:link rel="alternate" hreflang="{hl}" href="'
                        + re.sub(r'\.com/[a-z]{2}/', f'.com/{lang}/', m.group(3)) + '"/>\n' + m.group(4), nb, count=1)
        s = s.replace(b, nb)
    # new <url> entries: copy the Tamil ones
    for b in re.findall(r'  <url>\n    <loc>https://iraq\.fabletour\.com/ta/[^<]*</loc>.*?</url>\n', s, flags=re.S):
        if "/blog" in b:
            continue
        add = ""
        for lang in META:
            loc = b.split("<loc>")[1].split("</loc>")[0].replace("/ta/", f"/{lang}/")
            if f"<loc>{loc}</loc>" in s:
                continue
            add += b.replace(b.split("<loc>")[1].split("</loc>")[0], loc, 1)
        s = s.replace(b, b + add, 1)
    sm.write_text(s)


def run(langs):
    trips, _ = paragraphs(None)
    for lang in langs:
        M = load_map(lang)
        unknown = set()
        for rel in pages():
            out = build_page(lang, rel, M, trips, unknown)
            f = ROOT / lang / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(out)
        if unknown:
            print(f"[{lang}] untranslated:", *sorted(unknown)[:40], sep="\n  ")
        print("built", lang)
    for d in all_dirs():
        for rel in pages():
            f = ROOT / d / rel
            if f.exists():
                cur = d.strip("/") or "ar"
                f.write_text(add_links(f.read_text(), rel, cur))
    sitemap()


if __name__ == "__main__":
    run(sys.argv[1:] or list(META))
