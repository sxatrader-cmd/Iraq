#!/usr/bin/env python3
"""Pakistan city landing pages (Oct 2026): /ur/iraq-tours-from-<city>/ (copy of the Urdu homepage)
and /en/iraq-tours-from-<city>/ (copy of the English homepage) for Karachi, Lahore, Islamabad,
Peshawar, Multan, Quetta and Faisalabad, built with add_markets.build().
Every Pakistan page (cities + the existing /iraq-tours-from-pakistan/ pair) also gets:
- a card on Pakistan's Ziyarat Management Policy: since 1 Jan 2026 pilgrims from Pakistan travel
  only with government-registered Ziyarat Group Organisers (ZGOs); Fable Tour works as the ground
  partner in Iraq for registered organisers;
- a card linking all the city pages.
Not linked from the homepages. Idempotent:  python3 _blog/tools/add_markets_pk.py
Re-run after add_markets.py (which rebuilds the Pakistan pair without these cards)."""
import re, pathlib, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import add_markets as A

esc = lambda s: html.escape(s, quote=True)
HL_UR = [("shrines", "کربلا اور نجف اشرف", "امام حسینؑ اور حضرت عباسؑ کے روضے، امام علیؑ کا روضہ، مسجد کوفہ اور وادی السلام۔"),
         ("gilani", "بغداد کے مزارات", "حضرت غوث اعظم شیخ عبدالقادر جیلانیؒ، امام ابو حنیفہؒ، کاظمین اور حضرت جنید بغدادیؒ کے مزارات۔"),
         ("samarra", "سامرا", "امام علی نقیؑ اور امام حسن عسکریؑ کا روضہ اور مشہور مینار ملویہ۔")]
HL_EN = [("shrines", "Karbala & Najaf", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali, the Great Mosque of Kufa and Wadi al-Salam."),
         ("gilani", "The shrines of Baghdad", "Ghaus-e-Azam Sheikh Abdul Qadir Gilani, Imam Abu Hanifa, Kadhimiya and Junayd al-Baghdadi."),
         ("samarra", "Samarra", "The shrine of Imam Ali al-Hadi and Imam Hasan al-Askari and the spiral Malwiya minaret.")]
HL_BAB_UR = ("babylon", "بابل اور اُر", "عشتار دروازہ، بابل کا شیر اور اُر کا قدیم زِگورات۔")
HL_BAB_EN = ("babylon", "Babylon & Ur", "The Ishtar Gate, the Lion of Babylon and the ancient ziggurat of Ur.")

# key: (name ur, name en, airport ur, airport en, intro ur, intro en, highlights index swap)
C = {
 "karachi": ("کراچی", "Karachi",
   "کراچی کے جناح انٹرنیشنل ایئرپورٹ سے دبئی، شارجہ، دوحہ، بحرین یا مسقط کے راستے ایک اسٹاپ کے ساتھ نجف اور بغداد پہنچا جا سکتا ہے، اور بعض موسموں میں نجف کے لیے براہِ راست پروازیں بھی چلتی ہیں (ایئر لائن سے تازہ شیڈول ضرور چیک کریں)۔ ہم نجف یا بغداد ایئرپورٹ پر آپ کا استقبال کرتے ہیں۔",
   "From Jinnah International Airport (KHI), one-stop flights via Dubai, Sharjah, Doha, Bahrain or Muscat reach Najaf and Baghdad, and direct flights to Najaf operate in some seasons (always check current schedules). We meet you at Najaf or Baghdad airport.",
   "کراچی سے ہر سال ہزاروں زائرین کربلا اور نجف اشرف کی زیارت کے لیے جاتے ہیں۔ آپ کا قافلہ رجسٹرڈ زیارت گروپ آرگنائزر کے ساتھ ہو یا آپ عراق کی تاریخ دیکھنا چاہتے ہوں، بغداد سے ہمارا گائیڈ اور نجی گاڑی آپ کے ساتھ رہتے ہیں۔",
   "Every year thousands of zaireen travel from Karachi to Karbala and Najaf. Whether your group travels with a registered Ziyarat Group Organiser or you want to see Iraq's history, our Baghdad guide and private car stay with you throughout.", False),
 "lahore": ("لاہور", "Lahore",
   "لاہور کے علامہ اقبال انٹرنیشنل ایئرپورٹ سے دبئی، شارجہ، دوحہ یا بحرین کے راستے بغداد اور نجف کی پروازیں دستیاب ہیں، اور بعض موسموں میں براہِ راست پروازیں بھی چلتی ہیں (تازہ شیڈول ضرور چیک کریں)۔",
   "From Allama Iqbal International Airport (LHE), flights via Dubai, Sharjah, Doha or Bahrain reach Baghdad and Najaf, and direct flights operate in some seasons (check current schedules).",
   "داتا کی نگری لاہور سے بغداد کا رشتہ پرانا ہے: حضرت غوث اعظم شیخ عبدالقادر جیلانیؒ اور حضرت جنید بغدادیؒ کے مزارات ہوں یا کربلا اور نجف اشرف، ہم آپ کے لیے آرام دہ زیارت کا انتظام کرتے ہیں، اور ساتھ بابل اور اُر کی سیر بھی۔",
   "Lahore's bond with Baghdad runs deep — from the shrines of Ghaus-e-Azam Sheikh Abdul Qadir Gilani and Junayd al-Baghdadi to Karbala and Najaf. We arrange a comfortable ziyarat, and add Babylon and Ur if you wish.", True),
 "islamabad": ("اسلام آباد اور راولپنڈی", "Islamabad & Rawalpindi",
   "اسلام آباد انٹرنیشنل ایئرپورٹ سے دبئی، شارجہ، دوحہ یا مسقط کے راستے بغداد، نجف اور اربیل کی پروازیں دستیاب ہیں (تازہ شیڈول ضرور چیک کریں)۔ عراق کا سفارت خانہ اسلام آباد میں ہے۔",
   "From Islamabad International Airport (ISB), flights via Dubai, Sharjah, Doha or Muscat reach Baghdad, Najaf and Erbil (check current schedules). The Embassy of Iraq is in Islamabad.",
   "جڑواں شہروں سے زیارت اور سیاحت دونوں کے لیے: کربلا، نجف اشرف، کاظمین اور سامرا کی زیارت، اور بابل، اُر، ہترا اور اربیل کی تاریخی سیر — نجی گاڑی، بغداد کے گائیڈ اور 4–5 اسٹار ہوٹلوں کے ساتھ۔",
   "From the twin cities, for both ziyarat and history: Karbala, Najaf, Kadhimiya and Samarra, plus Babylon, Ur, Hatra and Erbil — with a private car, a Baghdad guide and 4★–5★ hotels.", True),
 "peshawar": ("پشاور", "Peshawar",
   "پشاور کے باچا خان انٹرنیشنل ایئرپورٹ سے دبئی، شارجہ یا دوحہ کے راستے بغداد اور نجف کی پروازیں دستیاب ہیں، یا اسلام آباد سے سفر کیا جا سکتا ہے (تازہ شیڈول ضرور چیک کریں)۔",
   "From Bacha Khan International Airport (PEW), flights via Dubai, Sharjah or Doha reach Baghdad and Najaf, or you can fly from Islamabad (check current schedules).",
   "خیبر پختونخوا سے آنے والے زائرین کے لیے: بغداد میں امام ابو حنیفہؒ اور حضرت غوث اعظمؒ کے مزارات، کاظمین، اور کربلا و نجف اشرف کی زیارت۔ ہمارا گائیڈ عربی اور انگریزی میں رہنمائی کرتا ہے۔",
   "For travellers from Khyber Pakhtunkhwa: the shrines of Imam Abu Hanifa and Ghaus-e-Azam in Baghdad, Kadhimiya, and ziyarat to Karbala and Najaf. Our guide works in Arabic and English.", True),
 "multan": ("ملتان", "Multan",
   "ملتان انٹرنیشنل ایئرپورٹ سے دبئی یا شارجہ کے راستے بغداد اور نجف کی پروازیں دستیاب ہیں، یا لاہور اور کراچی سے سفر کیا جا سکتا ہے (تازہ شیڈول ضرور چیک کریں)۔",
   "From Multan International Airport (MUX), flights via Dubai or Sharjah reach Baghdad and Najaf, or you can fly from Lahore or Karachi (check current schedules).",
   "اولیا کے شہر ملتان کا بغداد سے روحانی رشتہ ہے: حضرت بہاء الدین زکریا ملتانیؒ نے بغداد میں شیخ شہاب الدین عمر سہروردیؒ سے فیض پایا۔ درخواست پر ہم بغداد میں شیخ سہروردیؒ کے مزار کی زیارت بھی شامل کرتے ہیں، ساتھ غوث اعظمؒ، کاظمین، کربلا اور نجف اشرف۔",
   "Multan, the city of saints, has a spiritual bond with Baghdad: Hazrat Bahauddin Zakariya studied under Sheikh Shihab al-Din Umar Suhrawardi in Baghdad. On request we add the shrine of Sheikh Suhrawardi in Baghdad, alongside Ghaus-e-Azam, Kadhimiya, Karbala and Najaf.", True),
 "quetta": ("کوئٹہ", "Quetta",
   "کوئٹہ ایئرپورٹ سے کراچی، لاہور یا اسلام آباد کے راستے، پھر دبئی، شارجہ یا دوحہ سے نجف اور بغداد پہنچا جا سکتا ہے (تازہ شیڈول ضرور چیک کریں)۔ زمینی راستے سے سفر سے متعلق حکومتِ پاکستان کی تازہ ہدایات ضرور دیکھیں۔",
   "From Quetta (UET), connect via Karachi, Lahore or Islamabad, then Dubai, Sharjah or Doha to Najaf and Baghdad (check current schedules). Check the Government of Pakistan's latest instructions on overland travel.",
   "بلوچستان سے آنے والے زائرین کے لیے کربلا، نجف اشرف، کاظمین اور سامرا کی پُرسکون زیارت: نجف یا بغداد ایئرپورٹ پر استقبال، نجی گاڑی، اور ہر روضے پر کافی وقت۔",
   "For zaireen from Balochistan, a calm ziyarat to Karbala, Najaf, Kadhimiya and Samarra: an airport welcome in Najaf or Baghdad, a private car and unhurried time at every shrine.", False),
 "faisalabad": ("فیصل آباد", "Faisalabad",
   "فیصل آباد ایئرپورٹ سے دبئی یا شارجہ کے راستے سفر کیا جا سکتا ہے، یا لاہور سے بغداد اور نجف کی پروازیں لی جا سکتی ہیں (تازہ شیڈول ضرور چیک کریں)۔",
   "From Faisalabad (LYP), fly via Dubai or Sharjah, or take flights from Lahore to Baghdad and Najaf (check current schedules).",
   "فیصل آباد اور وسطی پنجاب کے خاندانوں کے لیے: بغداد میں حضرت غوث اعظمؒ اور امام ابو حنیفہؒ کے مزارات، کاظمین، کربلا اور نجف اشرف کی زیارت — اپنی تاریخ پر، اپنے خاندان کے ساتھ۔",
   "For families from Faisalabad and central Punjab: the shrines of Ghaus-e-Azam and Imam Abu Hanifa in Baghdad, Kadhimiya, Karbala and Najaf — on your dates, with your family.", True),
}

ZGO = {
 "ur": ("زیارت مینجمنٹ پالیسی", "حکومتِ پاکستان کی زیارت مینجمنٹ پالیسی کے تحت یکم جنوری 2026 سے عراق جانے والے زائرین صرف حکومت سے رجسٹرڈ زیارت گروپ آرگنائزرز (ZGO) کے ذریعے سفر کرتے ہیں۔ اپنی بکنگ رجسٹرڈ آرگنائزر سے کریں اور اس کا نام وزارتِ مذہبی امور کی سرکاری فہرست میں ضرور دیکھیں۔ Fable Tour عراق میں رجسٹرڈ آرگنائزرز کا زمینی پارٹنر ہے: ایئرپورٹ استقبال، ہوٹل، نجی گاڑیاں اور گائیڈ۔ آرگنائزرز ہم سے واٹس ایپ پر رابطہ کریں۔ قوانین بدل سکتے ہیں، سفر سے پہلے تازہ ہدایات ضرور چیک کریں۔"),
 "en": ("Pakistan's Ziyarat Management Policy", "Under the Government of Pakistan's Ziyarat Management Policy, since 1 January 2026 pilgrims travel to Iraq only with government-registered Ziyarat Group Organisers (ZGOs). Book through a registered organiser and check its name on the Ministry of Religious Affairs' official list. Fable Tour is the ground partner in Iraq for registered organisers — airport welcome, hotels, private vehicles and guides. Organisers can contact us on WhatsApp. Rules can change, so always check the latest instructions before you travel."),
}
LINKS_T = {"ur": "پاکستان کے شہروں سے عراق کے ٹور", "en": "Iraq tours by city in Pakistan"}

A.M.clear()
for k, (nu, ne, tu, te, iu, ie, bab) in C.items():
    hu = list(HL_UR); he = list(HL_EN)
    if bab:
        hu[2] = HL_BAB_UR; he[2] = HL_BAB_EN
    A.market(k, f"iraq-tours-from-{k}", "ur", {"ur": nu, "en": ne}, {
     "ur": dict(title=f"{nu} سے عراق زیارت ٹور: کربلا، نجف، بغداد | Fable Tour",
       desc=f"{nu} سے عراق کی زیارت اور سیاحت: کربلا، نجف اشرف، کاظمین، سامرا، حضرت غوث اعظمؒ کا مزار اور بابل — بغداد کے مقامی گائیڈ، نجی گاڑی اور 4–5 اسٹار ہوٹل کے ساتھ۔",
       kw=f"{nu} سے عراق زیارت, {nu} سے کربلا, نجف زیارت {nu}, عراق زیارت پیکج, غوث اعظم بغداد, زیارت گروپ آرگنائزر, Fable Tour",
       h1=f"{nu} سے عراق زیارت اور ٹور", lead=f"{nu} سے کربلا، نجف اشرف، کاظمین اور سامرا کی زیارت، بغداد کے مزارات اور بابل کی سیر — 4–5 اسٹار ہوٹل اور ذاتی گائیڈ، 2,500 امریکی ڈالر سے۔",
       intro=iu, travel=tu, hl=hu),
     "en": dict(title=f"Iraq Ziyarat & Tours from {ne}: Karbala, Najaf, Baghdad | Fable Tour",
       desc=f"Iraq ziyarat and tours from {ne}: Karbala, Najaf, Kadhimiya, Samarra, the shrine of Ghaus-e-Azam and Babylon, with a Baghdad guide, private car and 4★–5★ hotels.",
       kw=f"Iraq ziyarat from {ne}, {ne} to Karbala, {ne} to Najaf, Iraq ziyarat package {ne}, Ghaus-e-Azam Baghdad, Ziyarat Group Organiser, Fable Tour",
       h1=f"Iraq ziyarat & tours from {ne}", lead=f"Ziyarat to Karbala, Najaf, Kadhimiya and Samarra, the shrines of Baghdad and a visit to Babylon — 4★–5★ hotels and a private guide, from US$2,500.",
       intro=ie, travel=te, hl=he)})


def cards(lang, cur):
    h, t = ZGO[lang]
    pre = "/ur/" if lang == "ur" else "/en/"
    items = "".join((f'<li><strong>{esc(v[0 if lang == "ur" else 1])}</strong></li>' if k == cur else
                     f'<li><a href="{pre}iraq-tours-from-{k}/">{esc(v[0 if lang == "ur" else 1])}</a></li>') for k, v in C.items())
    allp = (f'<li><strong>{"پاکستان" if lang == "ur" else "Pakistan"}</strong></li>' if cur == "pakistan" else
            f'<li><a href="{pre}iraq-tours-from-pakistan/">{"پاکستان" if lang == "ur" else "Pakistan"}</a></li>')
    return (f'    <div class="market-card" id="zgo" style="margin-top:16px"><h3>{esc(h)}</h3><p>{esc(t)}</p></div>\n'
            f'    <div class="market-card market-links" id="by-city" style="margin-top:16px"><h3>{esc(LINKS_T[lang])}</h3><ul class="mkt-links">{allp}{items}</ul></div>\n')


LINKS_CSS = '<style id="mkt-links-css">.mkt-links{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.mkt-links li a,.mkt-links li strong{display:inline-block;padding:6px 12px;border:1px solid rgba(27,42,71,.18);border-radius:20px;font-size:14px;text-decoration:none;color:var(--navy,#1B2A47);background:#fff}.mkt-links li strong{background:var(--gold,#C9A96A);border-color:var(--gold,#C9A96A)}</style>'


def inject(f, lang, cur):
    s = f.read_text()
    s = re.sub(r'\s*<div class="market-card" id="zgo".*?</div>\n?', "\n", s, flags=re.S)
    s = re.sub(r'\s*<div class="market-card market-links" id="by-city".*?</ul></div>\n?', "\n", s, flags=re.S)
    i = s.index("</section>", s.index('class="block in market-panel"'))
    s = s[:i].rstrip() + "\n" + cards(lang, cur) + "  " + s[i:]
    if 'id="mkt-links-css"' not in s:
        s = s.replace("</head>", LINKS_CSS + "\n</head>", 1)
    f.write_text(s)


def run():
    urls = []
    for key, mk in A.M.items():
        pair = [("ur", A.url(key, "ur")), ("en", A.url(key, "en")), ("x-default", A.url(key, "en"))]
        for lang in ("ur", "en"):
            urls.append((A.build(key, lang), pair))
            inject(A.ROOT / lang / mk["slug"] / "index.html", lang, key)
    for lang in ("ur", "en"):
        inject(A.ROOT / lang / "iraq-tours-from-pakistan" / "index.html", lang, "pakistan")
    A.sitemap(urls)
    print("built", len(urls), "pages")


if __name__ == "__main__":
    run()
