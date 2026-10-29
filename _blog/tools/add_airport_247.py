"""Add '24/7' and 'English-speaking staff' to the airport pickup list on every page. Idempotent."""
import re, glob, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
X = {"ar": ("الخدمة متاحة على مدار الساعة 24/7", "موظف الاستقبال يتحدث اللغة الإنجليزية"),
 "en": ("Available 24/7", "English-speaking meet & greet staff"),
 "ru": ("Работаем круглосуточно, 24/7", "Встречающий сотрудник говорит по-английски"),
 "de": ("Rund um die Uhr verfügbar (24/7)", "Englischsprachiges Empfangspersonal"),
 "fr": ("Disponible 24h/24, 7j/7", "Personnel d'accueil anglophone"),
 "es": ("Disponible 24/7", "Personal de recepción que habla inglés"),
 "it": ("Disponibile 24/7", "Personale di accoglienza che parla inglese"),
 "el": ("Διαθέσιμο 24/7", "Προσωπικό υποδοχής που μιλά αγγλικά"),
 "cs": ("K dispozici nonstop 24/7", "Anglicky mluvící personál na letišti"),
 "pl": ("Dostępne 24/7", "Anglojęzyczny personel powitalny"),
 "zh-Hans": ("全天候 24/7 服务", "接机人员会说英语"),
 "zh-Hant-TW": ("全天候 24/7 服務", "接機人員會說英語"),
 "ja": ("24時間年中無休", "英語を話すスタッフがお出迎え"),
 "tr": ("7/24 hizmet", "İngilizce konuşan karşılama personeli"),
 "fa": ("خدمات شبانه‌روزی 24/7", "کارمند استقبال انگلیسی صحبت می‌کند"),
 "ms": ("Tersedia 24/7", "Kakitangan sambutan berbahasa Inggeris"),
 "id": ("Tersedia 24/7", "Staf penjemput berbahasa Inggris"),
 "th": ("บริการตลอด 24 ชั่วโมง ทุกวัน", "เจ้าหน้าที่รับรองพูดภาษาอังกฤษ"),
 "ta": ("24/7 சேவை கிடைக்கும்", "ஆங்கிலம் பேசும் வரவேற்பு பணியாளர்"),
 "hi": ("24/7 उपलब्ध", "अंग्रेज़ी बोलने वाला स्वागत कर्मचारी"),
 "ur": ("24/7 دستیاب", "انگریزی بولنے والا استقبالیہ عملہ"),
 "fi": ("Saatavilla 24/7", "Englantia puhuva vastaanottaja"),
 "sv": ("Tillgängligt dygnet runt, 24/7", "Engelsktalande mottagningspersonal"),
 "da": ("Tilgængelig døgnet rundt, 24/7", "Engelsktalende modtagepersonale"),
 "no": ("Tilgjengelig døgnet rundt, 24/7", "Engelsktalende mottakspersonale"),
 "sk": ("K dispozícii nonstop 24/7", "Anglicky hovoriaci personál na letisku"),
 "hr": ("Dostupno 24/7", "Osoblje za doček koje govori engleski"),
 "ro": ("Disponibil 24/7", "Personal de întâmpinare vorbitor de engleză"),
 "nl": ("24/7 beschikbaar", "Engelstalig ontvangstpersoneel"),
 "ka": ("ხელმისაწვდომია 24/7", "ინგლისურენოვანი შემხვედრი თანამშრომელი")}
n = 0
for p in glob.glob(str(ROOT / "**/index.html"), recursive=True):
    s = open(p, encoding="utf-8").read()
    if 'class="ap-inc"' not in s or 'class="ap-x"' in s: continue
    lang = re.search(r'<html[^>]*lang="([^"]+)"', s).group(1)
    a, b = X[lang]
    s = re.sub(r'(<ul class="ap-inc">.*?)(</ul>)', lambda m: m.group(1) + f'<li class="ap-x">{a}</li><li class="ap-x">{b}</li>' + m.group(2), s, count=1, flags=re.S)
    open(p, "w", encoding="utf-8").write(s); n += 1
print(n)
