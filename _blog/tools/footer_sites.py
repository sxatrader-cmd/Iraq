#!/usr/bin/env python3
"""Footer: replaces the long language list (<nav class="langs">) with links to the other
Fable Tour destination sites (Sri Lanka, Turkey, Yemen, UAE). The language menu at the top stays.
Runs on every page of the site (homepages, day trips, country pages, blog). Idempotent.
Re-run after add_lang*.py or _blog/build.py."""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITES = [("srilanka", "https://srilanka.fabletour.com/"), ("turkey", "https://turkey.fabletour.com/"),
         ("yemen", "https://yemen.fabletour.com/"), ("uae", "https://uae.fabletour.com/")]
# label, Sri Lanka, Turkey, Yemen, UAE
T = {
 "ar": ("رحلاتنا الأخرى", "سريلانكا", "تركيا", "اليمن", "الإمارات"),
 "en": ("More Fable Tour trips", "Sri Lanka", "Turkey", "Yemen", "UAE"),
 "tr": ("Diğer turlarımız", "Sri Lanka", "Türkiye", "Yemen", "BAE"),
 "ru": ("Другие наши туры", "Шри-Ланка", "Турция", "Йемен", "ОАЭ"),
 "de": ("Weitere Reisen", "Sri Lanka", "Türkei", "Jemen", "VAE"),
 "fr": ("Nos autres voyages", "Sri Lanka", "Turquie", "Yémen", "Émirats"),
 "es": ("Otros viajes", "Sri Lanka", "Turquía", "Yemen", "EAU"),
 "it": ("Altri viaggi", "Sri Lanka", "Turchia", "Yemen", "Emirati Arabi"),
 "el": ("Άλλα ταξίδια μας", "Σρι Λάνκα", "Τουρκία", "Υεμένη", "ΗΑΕ"),
 "cs": ("Další zájezdy", "Srí Lanka", "Turecko", "Jemen", "SAE"),
 "sk": ("Ďalšie zájazdy", "Srí Lanka", "Turecko", "Jemen", "SAE"),
 "pl": ("Inne wycieczki", "Sri Lanka", "Turcja", "Jemen", "ZEA"),
 "hr": ("Ostala putovanja", "Šri Lanka", "Turska", "Jemen", "UAE"),
 "ro": ("Alte circuite", "Sri Lanka", "Turcia", "Yemen", "EAU"),
 "zh": ("更多旅程", "斯里兰卡", "土耳其", "也门", "阿联酋"),
 "zh-Hans": ("更多旅程", "斯里兰卡", "土耳其", "也门", "阿联酋"),
 "zh-tw": ("更多旅程", "斯里蘭卡", "土耳其", "葉門", "阿聯酋"),
 "zh-Hant": ("更多旅程", "斯里蘭卡", "土耳其", "葉門", "阿聯酋"),
 "zh-TW": ("更多旅程", "斯里蘭卡", "土耳其", "葉門", "阿聯酋"),
 "ja": ("その他のツアー", "スリランカ", "トルコ", "イエメン", "UAE"),
 "fa": ("سفرهای دیگر ما", "سریلانکا", "ترکیه", "یمن", "امارات"),
 "ms": ("Lawatan lain kami", "Sri Lanka", "Turki", "Yaman", "UAE"),
 "id": ("Tur lain kami", "Sri Lanka", "Turki", "Yaman", "UEA"),
 "th": ("ทริปอื่นของเรา", "ศรีลังกา", "ตุรกี", "เยเมน", "ยูเออี"),
 "hi": ("हमारी अन्य यात्राएँ", "श्रीलंका", "तुर्किये", "यमन", "यूएई"),
 "ur": ("ہمارے دیگر ٹور", "سری لنکا", "ترکی", "یمن", "متحدہ عرب امارات"),
 "ta": ("எங்கள் பிற பயணங்கள்", "இலங்கை", "துருக்கி", "யேமன்", "ஐக்கிய அரபு அமீரகம்"),
 "fi": ("Muut matkamme", "Sri Lanka", "Turkki", "Jemen", "Arabiemiirikunnat"),
 "sv": ("Fler resor", "Sri Lanka", "Turkiet", "Jemen", "Förenade Arabemiraten"),
 "da": ("Flere rejser", "Sri Lanka", "Tyrkiet", "Yemen", "UAE"),
 "no": ("Flere reiser", "Sri Lanka", "Tyrkia", "Jemen", "De forente arabiske emirater"),
 "nb": ("Flere reiser", "Sri Lanka", "Tyrkia", "Jemen", "De forente arabiske emirater"),
}
CSS = ('<style id="sites-css">.sites{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;font-size:14px}'
       '.sites b{font-weight:500;opacity:.75}.sites a{color:var(--gold,#c9a14a);text-decoration:none}'
       '.sites a:hover{text-decoration:underline}</style>')
esc = lambda s: html.escape(s, quote=True)


def nav(lang):
    t = T.get(lang) or ("Hant" in lang and T["zh-Hant"]) or T.get(lang.split("-")[0]) or T["en"]
    links = "".join(f'<a href="{u}" rel="noopener">{esc(n)}</a>' for (k, u), n in zip(SITES, t[1:]))
    return f'<nav class="sites" aria-label="{esc(t[0])}"><b>{esc(t[0])}:</b>{links}</nav>'


def run():
    n = 0
    for f in ROOT.rglob("*.html"):
        if "_blog" in f.parts or ".git" in f.parts:
            continue
        s = f.read_text()
        if '<nav class="langs"' not in s and '<nav class="sites"' not in s:
            continue
        m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
        lang = m.group(1) if m else "en"
        new = re.sub(r'<nav class="(?:langs|sites)".*?</nav>', lambda _: nav(lang), s, count=1, flags=re.S)
        if 'id="sites-css"' not in new:
            new = new.replace("</head>", CSS + "\n</head>", 1)
        if new != s:
            f.write_text(new); n += 1
    print("updated", n, "pages")


if __name__ == "__main__":
    run()
