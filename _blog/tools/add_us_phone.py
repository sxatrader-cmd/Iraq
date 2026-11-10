"""US/Canada 24/7 customer-service line (+1 (212) 433-8608) on every page.

- footer contact line: same markup as the Arabic pages
  (<a href="tel:+12124338608" ...>أمريكا وكندا 24/7: <span dir="ltr">+1 (212) 433-8608</span></a>),
  label translated per language; added to every page that has no tel:+12124338608 link yet
  and to every language homepage footer (blog pages copy that footer)
- JSON-LD: contactPoint (US 24/7 line + WhatsApp) on the Fable Tour TravelAgency node,
  or on the provider of day-trip TouristTrip pages
Idempotent; run after any generator:   python3 _blog/tools/add_us_phone.py"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://iraq.fabletour.com"
TEL = "tel:+12124338608"
NUM = "+1 (212) 433-8608"
LABEL = {
    "ar": "أمريكا وكندا 24/7", "en": "USA & Canada 24/7", "ru": "США и Канада 24/7", "de": "USA & Kanada 24/7",
    "fr": "États-Unis et Canada 24/7", "es": "EE. UU. y Canadá 24/7", "it": "USA e Canada 24/7",
    "el": "ΗΠΑ & Καναδάς 24/7", "cs": "USA a Kanada 24/7", "pl": "USA i Kanada 24/7",
    "zh-Hans": "美国和加拿大 24 小时", "zh-Hant-TW": "美國和加拿大 24 小時", "zh-Hant": "美國和加拿大 24 小時",
    "ja": "米国・カナダ 24時間", "ko": "미국·캐나다 24시간", "tr": "ABD ve Kanada 7/24", "fa": "آمریکا و کانادا ۲۴/۷",
    "ms": "AS & Kanada 24/7", "id": "AS & Kanada 24/7", "th": "สหรัฐฯ และแคนาดา 24/7", "hi": "अमेरिका और कनाडा 24/7",
    "ur": "امریکہ اور کینیڈا 24/7", "ta": "அமெரிக்கா & கனடா 24/7", "fi": "Yhdysvallat ja Kanada 24/7",
    "sv": "USA & Kanada 24/7", "da": "USA & Canada 24/7", "no": "USA & Canada 24/7", "sk": "USA a Kanada 24/7",
    "hr": "SAD i Kanada 24/7", "ro": "SUA și Canada 24/7", "nl": "VS & Canada 24/7", "ka": "აშშ და კანადა 24/7",
    "pt": "EUA e Canadá 24/7", "ckb": "ئەمریکا و کەنەدا 24/7", "vi": "Mỹ và Canada 24/7",
}
COLON = {"fr": " : ", "zh-Hans": "：", "zh-Hant-TW": "：", "zh-Hant": "：", "ja": "："}
CP = [{"@type": "ContactPoint", "telephone": "+1-212-433-8608", "contactType": "customer service",
       "areaServed": ["US", "CA"], "availableLanguage": ["en", "ar"],
       "hoursAvailable": {"@type": "OpeningHoursSpecification",
                          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                          "opens": "00:00", "closes": "23:59"}},
      {"@type": "ContactPoint", "name": "WhatsApp", "telephone": "+964-771-174-5353", "contactType": "customer service",
       "url": "https://wa.me/9647711745353"}]
CPJ = json.dumps(CP, ensure_ascii=False)
WA_SPAN = '<span dir="ltr" style="white-space:nowrap">+964 771 174 5353</span>'


def link(lang):
    lab = html.escape(LABEL.get(lang, LABEL["en"]), quote=False)
    return (f'<a href="{TEL}" style="white-space:nowrap;color:inherit">{lab}{COLON.get(lang, ": ")}'
            f'<span dir="ltr">{NUM}</span></a>')


def footer(s, lang):
    a = s.rfind("<footer"); e = s.find("</footer>", a)
    if a < 0 or e < 0: return s
    ft = s[a:e]
    if TEL in ft: return s
    m = re.search(r'(<span><a href="https://fabletour\.com"[^\n]*?)(</span>\n)', ft)
    if not m: return s
    nf = ft[:m.end(1)] + " · " + link(lang) + ft[m.end(1):]
    return s[:a] + nf + s[e:]


def jsonld(s):
    def fix(m):
        j = m.group(2)
        if "contactPoint" in j: return m.group(0)
        if '"telephone": "+9647711745353"' in j:
            j2 = j.replace('"telephone": "+9647711745353"', '"telephone": "+9647711745353", "contactPoint": ' + CPJ, 1)
        elif '"provider": {"@id": "https://fabletour.com/#org"}' in j:
            j2 = j.replace('"provider": {"@id": "https://fabletour.com/#org"}',
                           '"provider": {"@id": "https://fabletour.com/#org", "contactPoint": ' + CPJ + '}', 1)
        else:
            return m.group(0)
        json.loads(j2)
        return m.group(1) + j2 + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, s, flags=re.S)


def pages():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for u in re.findall(r"<loc>([^<]+)</loc>", sm):
        p = u[len(SITE):].strip("/")
        f = ROOT / (p + "/index.html" if p else "index.html")
        if f.exists(): yield f, False
    for f in ROOT.glob("*/index.html"):
        s = f.read_text(encoding="utf-8")
        if re.search(r'<html lang="[^"]+"', s) and f.parent.name in LANG_DIRS: yield f, True
    yield ROOT / "index.html", True


LANG_DIRS = {"en", "ru", "de", "fr", "es", "it", "el", "cs", "pl", "zh", "zh-tw", "ja", "ko", "tr", "fa", "ms", "id",
             "th", "hi", "ur", "ta", "fi", "sv", "da", "no", "sk", "hr", "ro", "nl", "ka", "pt", "ckb", "vi"}


def run():
    seen = {}
    for f, home in pages():
        seen[f] = seen.get(f, False) or home
    n = 0
    for f, home in seen.items():
        s = f.read_text(encoding="utf-8")
        lang = re.search(r'<html lang="([^"]+)"', s).group(1)
        out = s
        if home or TEL not in out:
            out = footer(out, lang)
        out = jsonld(out)
        if out != s:
            f.write_text(out, encoding="utf-8"); n += 1
    print(f"add_us_phone: {n} pages updated")


if __name__ == "__main__":
    run()
