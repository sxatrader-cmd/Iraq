#!/usr/bin/env python3
"""Standalone page for each multi-day program, in every language that has day-trip pages:
  /tours/iraq-7-day-tour/  and  /tours/iraq-9-day-tour/   (Arabic, root)
  /<lang>/tours/iraq-7-day-tour/ ...                         (other languages)
Cloned from that language's homepage (same header, footer, form, contacts, scripts) and
reduced to the one program: day-by-day itinerary (open), price box, includes / not-included
and notes exactly as on the homepage, group dates, "what both tours include", program FAQ
(+ FAQPage JSON-LD) and the booking form with the program preselected.
Own title / description / canonical / hreflang cluster (+ x-default = en) / OG / JSON-LD
(TouristTrip + Offer copied from the homepage ItemList, BreadcrumbList, FAQPage).
link_homes(): the program titles on each language homepage link to these pages (crawlable
<a href>, like the day-trip cards). Only homepages are touched; never market/landing pages.
Idempotent:  python3 _blog/tools/add_program_pages.py"""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = "https://iraq.fabletour.com"
LANGS = ["ar", "en", "ru", "de", "fr", "es", "it", "el", "cs", "pl", "zh", "zh-tw", "ja", "tr", "fa", "ms", "id", "th",
         "hi", "ur", "ta", "fi", "sv", "da", "no", "sk", "hr", "ro", "nl", "ka", "ko", "pt", "vi", "ckb"]
HREFLANG = {"zh": "zh-Hans", "zh-tw": "zh-Hant"}
PROGS = {"7": {"pid": "tour-7-days", "slug": "iraq-7-day-tour", "img": "img/babylon-ishtar-gate.webp"},
         "9": {"pid": "tour-9-days", "slug": "iraq-9-day-tour", "img": "img/marshes-mashoof.webp"}}
LASTMOD = "2026-11-11"

# keyword title (without brand); " | Fable Tour" is appended when the total stays <= 60 chars
KW = {
 "ar": ("رحلة العراق 7 أيام: بغداد، بابل، أور والأهوار", "رحلة العراق 9 أيام من البصرة إلى أربيل"),
 "en": ("Iraq 7-Day Tour: Baghdad, Babylon, Ur & Marshes", "Iraq 9-Day Tour: Basra to Erbil, Ur & Mosul"),
 "ru": ("Тур в Ирак на 7 дней: Багдад, Вавилон, Ур", "Тур в Ирак на 9 дней: от Басры до Эрбиля"),
 "de": ("Irak Rundreise 7 Tage: Bagdad, Babylon & Ur", "Irak Rundreise 9 Tage: von Basra bis Erbil"),
 "fr": ("Circuit Irak 7 jours : Bagdad, Babylone, Ur", "Circuit Irak 9 jours : de Bassora à Erbil"),
 "es": ("Viaje a Irak 7 días: Bagdad, Babilonia y Ur", "Viaje a Irak 9 días: de Basora a Erbil"),
 "it": ("Tour Iraq 7 giorni: Baghdad, Babilonia e Ur", "Tour Iraq 9 giorni: da Bassora a Erbil"),
 "el": ("Ταξίδι στο Ιράκ 7 ημέρες: Βαγδάτη, Βαβυλώνα", "Ταξίδι στο Ιράκ 9 ημέρες: Βασόρα έως Ερμπίλ"),
 "cs": ("Zájezd do Iráku na 7 dní: Bagdád, Babylon, Ur", "Zájezd do Iráku na 9 dní: z Basry do Erbílu"),
 "pl": ("Wycieczka do Iraku 7 dni: Bagdad, Babilon, Ur", "Wycieczka do Iraku 9 dni: z Basry do Erbilu"),
 "zh": ("伊拉克7日游：巴格达、巴比伦、乌尔", "伊拉克9日游：巴士拉至埃尔比勒"),
 "zh-tw": ("伊拉克7日遊：巴格達、巴比倫、烏爾", "伊拉克9日遊：巴士拉至埃爾比勒"),
 "ja": ("イラク7日間ツアー：バグダッド・バビロン・ウル", "イラク9日間ツアー：バスラからエルビルへ"),
 "tr": ("Irak Turu 7 Gün: Bağdat, Babil ve Ur", "Irak Turu 9 Gün: Basra'dan Erbil'e"),
 "fa": ("تور عراق ۷ روزه: بغداد، بابل، اور و تالاب‌ها", "تور عراق ۹ روزه: از بصره تا اربیل"),
 "ms": ("Pakej Lawatan Iraq 7 Hari: Baghdad, Babylon, Ur", "Pakej Lawatan Iraq 9 Hari: Basra ke Erbil"),
 "id": ("Tur Irak 7 Hari: Baghdad, Babilonia, Ur", "Tur Irak 9 Hari: Basra ke Erbil"),
 "th": ("ทัวร์อิรัก 7 วัน: แบกแดด บาบิโลน อูร์", "ทัวร์อิรัก 9 วัน: บัสราถึงเออร์บิล"),
 "hi": ("इराक 7 दिन का टूर: बगदाद, बेबीलोन, उर", "इराक 9 दिन का टूर: बसरा से एरबिल"),
 "ur": ("عراق 7 دن کا ٹور: بغداد، بابل، اور", "عراق 9 دن کا ٹور: بصرہ سے اربیل"),
 "ta": ("ஈராக் 7 நாள் சுற்றுலா: பாக்தாத், பாபிலோன், ஊர்", "ஈராக் 9 நாள் சுற்றுலா: பஸ்ரா முதல் எர்பில் வரை"),
 "fi": ("Irakin kiertomatka 7 päivää: Bagdad, Babylon", "Irakin kiertomatka 9 päivää: Basrasta Erbiliin"),
 "sv": ("Irakresa 7 dagar: Bagdad, Babylon och Ur", "Irakresa 9 dagar: från Basra till Erbil"),
 "da": ("Irak-rejse 7 dage: Bagdad, Babylon og Ur", "Irak-rejse 9 dage: fra Basra til Erbil"),
 "no": ("Irak-reise 7 dager: Bagdad, Babylon og Ur", "Irak-reise 9 dager: fra Basra til Erbil"),
 "sk": ("Zájazd do Iraku na 7 dní: Bagdad, Babylon, Ur", "Zájazd do Iraku na 9 dní: z Basry do Erbilu"),
 "hr": ("Putovanje u Irak 7 dana: Bagdad, Babilon, Ur", "Putovanje u Irak 9 dana: od Basre do Erbila"),
 "ro": ("Excursie în Irak 7 zile: Bagdad, Babilon, Ur", "Excursie în Irak 9 zile: din Basra la Erbil"),
 "nl": ("Rondreis Irak 7 dagen: Bagdad, Babylon en Ur", "Rondreis Irak 9 dagen: van Basra naar Erbil"),
 "ka": ("ერაყის 7-დღიანი ტური: ბაღდადი, ბაბილონი, ური", "ერაყის 9-დღიანი ტური: ბასრიდან ერბილამდე"),
 "ko": ("이라크 7일 투어: 바그다드, 바빌론, 우르", "이라크 9일 투어: 바스라에서 에르빌까지"),
 "pt": ("Viagem ao Iraque 7 dias: Bagdade, Babilónia", "Viagem ao Iraque 9 dias: de Baçorá a Erbil"),
 "vi": ("Tour Iraq 7 ngày: Baghdad, Babylon, Ur", "Tour Iraq 9 ngày: từ Basra đến Erbil"),
 "ckb": ("گەشتی 7 ڕۆژە بۆ عێراق: بەغدا، بابل، ئور", "گەشتی 9 ڕۆژە بۆ عێراق: لە بەسرەوە بۆ هەولێر"),
}

# back link to the language homepage
ALL = {"ar": "كل رحلات العراق", "en": "All Iraq tours", "ru": "Все туры по Ираку", "de": "Alle Irak-Reisen",
       "fr": "Tous les circuits en Irak", "es": "Todos los tours por Irak", "it": "Tutti i tour in Iraq",
       "el": "Όλες οι περιηγήσεις στο Ιράκ", "cs": "Všechny zájezdy do Iráku", "pl": "Wszystkie wycieczki po Iraku",
       "zh": "全部伊拉克行程", "zh-tw": "全部伊拉克行程", "ja": "イラクのツアー一覧", "tr": "Tüm Irak turları",
       "fa": "همه تورهای عراق", "ms": "Semua lawatan Iraq", "id": "Semua tur Irak", "th": "ทัวร์อิรักทั้งหมด",
       "ta": "அனைத்து ஈராக் சுற்றுலாக்கள்", "hi": "इराक के सभी टूर", "ur": "عراق کے تمام ٹورز", "fi": "Kaikki Irakin matkat",
       "sv": "Alla Irakresor", "da": "Alle Irak-ture", "no": "Alle Irak-turer", "sk": "Všetky zájazdy do Iraku",
       "hr": "Sva putovanja po Iraku", "ro": "Toate tururile în Irak", "nl": "Alle Irak-reizen", "ka": "ერაყის ყველა ტური",
       "ko": "이라크 투어 전체 보기", "pt": "Todas as viagens ao Iraque", "vi": "Tất cả tour Iraq", "ckb": "هەموو گەشتەکانی عێراق"}

# program FAQ questions ({d} = number of days); answers are built from the page's own homepage text
FQ = {
 "ar": ("كم سعر رحلة العراق {d} أيام؟", "ماذا يشمل سعر رحلة الـ{d} أيام؟", "ماذا لا يشمل السعر؟", "من أين تبدأ رحلة الـ{d} أيام وأين تنتهي، وما الأماكن التي تزورها؟"),
 "en": ("How much does the {d}-day Iraq tour cost?", "What is included in the price of the {d}-day tour?", "What is not included in the price?", "Where does the {d}-day tour start and end, and which places does it visit?"),
 "ru": ("Сколько стоит тур в Ирак на {d} дней?", "Что входит в стоимость тура на {d} дней?", "Что не входит в стоимость?", "Где начинается и заканчивается тур на {d} дней и какие места он включает?"),
 "de": ("Was kostet die {d}-tägige Irak-Reise?", "Was ist im Preis der {d}-tägigen Reise enthalten?", "Was ist nicht im Preis enthalten?", "Wo beginnt und endet die {d}-tägige Reise und welche Orte besucht sie?"),
 "fr": ("Combien coûte le circuit de {d} jours en Irak ?", "Qu'est-ce qui est inclus dans le prix du circuit de {d} jours ?", "Qu'est-ce qui n'est pas inclus dans le prix ?", "Où commence et se termine le circuit de {d} jours, et quels lieux visite-t-il ?"),
 "es": ("¿Cuánto cuesta el viaje de {d} días a Irak?", "¿Qué incluye el precio del viaje de {d} días?", "¿Qué no incluye el precio?", "¿Dónde empieza y termina el viaje de {d} días y qué lugares visita?"),
 "it": ("Quanto costa il tour di {d} giorni in Iraq?", "Cosa include il prezzo del tour di {d} giorni?", "Cosa non è incluso nel prezzo?", "Dove inizia e finisce il tour di {d} giorni e quali luoghi visita?"),
 "el": ("Πόσο κοστίζει το ταξίδι {d} ημερών στο Ιράκ;", "Τι περιλαμβάνει η τιμή του ταξιδιού {d} ημερών;", "Τι δεν περιλαμβάνει η τιμή;", "Πού ξεκινά και πού τελειώνει το ταξίδι {d} ημερών και ποια μέρη επισκέπτεται;"),
 "cs": ("Kolik stojí {d}denní zájezd do Iráku?", "Co zahrnuje cena {d}denního zájezdu?", "Co cena nezahrnuje?", "Kde {d}denní zájezd začíná a končí a jaká místa navštíví?"),
 "pl": ("Ile kosztuje {d}-dniowa wycieczka do Iraku?", "Co obejmuje cena {d}-dniowej wycieczki?", "Czego nie obejmuje cena?", "Gdzie zaczyna się i kończy {d}-dniowa wycieczka i jakie miejsca odwiedza?"),
 "zh": ("伊拉克{d}日游多少钱？", "{d}日游的价格包含哪些内容？", "价格不包含哪些内容？", "{d}日游从哪里出发、在哪里结束？会游览哪些地方？"),
 "zh-tw": ("伊拉克{d}日遊多少錢？", "{d}日遊的價格包含哪些內容？", "價格不包含哪些內容？", "{d}日遊從哪裡出發、在哪裡結束？會遊覽哪些地方？"),
 "ja": ("イラク{d}日間ツアーの料金は？", "{d}日間ツアーの料金に含まれるものは？", "料金に含まれないものは？", "{d}日間ツアーの発着地と訪問地は？"),
 "tr": ("{d} günlük Irak turu ne kadar?", "{d} günlük turun fiyatına neler dahil?", "Fiyata neler dahil değil?", "{d} günlük tur nerede başlayıp nerede bitiyor, hangi yerleri ziyaret ediyor?"),
 "fa": ("قیمت تور {d} روزه عراق چقدر است؟", "قیمت تور {d} روزه شامل چه مواردی است؟", "چه مواردی در قیمت شامل نیست؟", "تور {d} روزه از کجا شروع و کجا تمام می‌شود و از چه مکان‌هایی بازدید می‌کند؟"),
 "ms": ("Berapakah harga lawatan Iraq {d} hari?", "Apakah yang termasuk dalam harga lawatan {d} hari?", "Apakah yang tidak termasuk dalam harga?", "Di manakah lawatan {d} hari bermula dan berakhir, dan tempat apa yang dilawati?"),
 "id": ("Berapa harga tur Irak {d} hari?", "Apa saja yang termasuk dalam harga tur {d} hari?", "Apa yang tidak termasuk dalam harga?", "Di mana tur {d} hari dimulai dan berakhir, dan tempat apa saja yang dikunjungi?"),
 "th": ("ทัวร์อิรัก {d} วัน ราคาเท่าไร?", "ราคาทัวร์ {d} วันรวมอะไรบ้าง?", "ราคาไม่รวมอะไรบ้าง?", "ทัวร์ {d} วันเริ่มและสิ้นสุดที่ไหน และเที่ยวสถานที่ใดบ้าง?"),
 "hi": ("इराक {d} दिन के टूर की कीमत कितनी है?", "{d} दिन के टूर की कीमत में क्या शामिल है?", "कीमत में क्या शामिल नहीं है?", "{d} दिन का टूर कहाँ से शुरू और कहाँ खत्म होता है, और किन जगहों पर जाता है?"),
 "ur": ("عراق {d} دن کے ٹور کی قیمت کتنی ہے؟", "{d} دن کے ٹور کی قیمت میں کیا شامل ہے؟", "قیمت میں کیا شامل نہیں ہے؟", "{d} دن کا ٹور کہاں سے شروع اور کہاں ختم ہوتا ہے، اور کن مقامات کی سیر کرتا ہے؟"),
 "ta": ("ஈராக் {d} நாள் சுற்றுலாவின் விலை என்ன?", "{d} நாள் சுற்றுலா விலையில் என்ன அடங்கும்?", "விலையில் என்ன அடங்காது?", "{d} நாள் சுற்றுலா எங்கே தொடங்கி எங்கே முடிகிறது, எந்த இடங்களுக்குச் செல்கிறது?"),
 "fi": ("Paljonko {d} päivän Irakin kiertomatka maksaa?", "Mitä {d} päivän matkan hintaan sisältyy?", "Mitä hintaan ei sisälly?", "Mistä {d} päivän matka alkaa ja mihin se päättyy, ja missä paikoissa se käy?"),
 "sv": ("Vad kostar Irakresan på {d} dagar?", "Vad ingår i priset för resan på {d} dagar?", "Vad ingår inte i priset?", "Var börjar och slutar resan på {d} dagar och vilka platser besöker den?"),
 "da": ("Hvad koster Irak-rejsen på {d} dage?", "Hvad er inkluderet i prisen for rejsen på {d} dage?", "Hvad er ikke inkluderet i prisen?", "Hvor starter og slutter rejsen på {d} dage, og hvilke steder besøger den?"),
 "no": ("Hva koster Irak-reisen på {d} dager?", "Hva er inkludert i prisen for reisen på {d} dager?", "Hva er ikke inkludert i prisen?", "Hvor starter og slutter reisen på {d} dager, og hvilke steder besøker den?"),
 "sk": ("Koľko stojí {d}-dňový zájazd do Iraku?", "Čo zahŕňa cena {d}-dňového zájazdu?", "Čo cena nezahŕňa?", "Kde sa {d}-dňový zájazd začína a končí a aké miesta navštívi?"),
 "hr": ("Koliko košta putovanje u Irak od {d} dana?", "Što je uključeno u cijenu putovanja od {d} dana?", "Što nije uključeno u cijenu?", "Gdje počinje i završava putovanje od {d} dana i koja mjesta posjećuje?"),
 "ro": ("Cât costă excursia de {d} zile în Irak?", "Ce include prețul excursiei de {d} zile?", "Ce nu include prețul?", "Unde începe și unde se termină excursia de {d} zile și ce locuri vizitează?"),
 "nl": ("Wat kost de rondreis van {d} dagen door Irak?", "Wat is inbegrepen in de prijs van de reis van {d} dagen?", "Wat is niet inbegrepen in de prijs?", "Waar begint en eindigt de reis van {d} dagen en welke plaatsen bezoekt hij?"),
 "ka": ("რა ღირს ერაყის {d}-დღიანი ტური?", "რას მოიცავს {d}-დღიანი ტურის ფასი?", "რას არ მოიცავს ფასი?", "სად იწყება და მთავრდება {d}-დღიანი ტური და რა ადგილებს მოიცავს?"),
 "ko": ("이라크 {d}일 투어 가격은 얼마인가요?", "{d}일 투어 가격에는 무엇이 포함되나요?", "가격에 포함되지 않는 것은 무엇인가요?", "{d}일 투어는 어디에서 시작하고 끝나며 어떤 곳을 방문하나요?"),
 "pt": ("Quanto custa a viagem de {d} dias ao Iraque?", "O que está incluído no preço da viagem de {d} dias?", "O que não está incluído no preço?", "Onde começa e termina a viagem de {d} dias e que locais visita?"),
 "vi": ("Tour Iraq {d} ngày giá bao nhiêu?", "Giá tour {d} ngày bao gồm những gì?", "Giá không bao gồm những gì?", "Tour {d} ngày bắt đầu và kết thúc ở đâu, đi qua những nơi nào?"),
 "ckb": ("نرخی گەشتی {d} ڕۆژەی عێراق چەندە؟", "نرخی گەشتی {d} ڕۆژە چی دەگرێتەوە؟", "نرخەکە چی ناگرێتەوە؟", "گەشتی {d} ڕۆژە لە کوێ دەست پێدەکات و لە کوێ کۆتایی دێت، و سەردانی چ شوێنێک دەکات؟"),
}
FADIG = {"7": "۷", "9": "۹"}

CSS = """
/* program page */
body.pg-solo .hero,body.pg-solo #video,body.pg-solo .pc-wrap,body.pg-solo .xvid{display:none!important}
body.pg-solo #itinerary{padding-top:8px}
.pg-top{padding-top:26px}
.pg-head{max-width:860px;margin:0 auto 22px}
.pg-all{display:inline-flex;align-items:center;gap:6px;color:var(--navy);font-size:14px;font-weight:600;text-decoration:none;border-bottom:1px solid var(--gold);padding-bottom:2px}
.pg-head .eyebrow{display:block;margin-top:16px}
.pg-h1{font-family:var(--serif-en);font-weight:400;font-size:clamp(28px,4.6vw,40px);line-height:1.25;color:var(--navy);margin:8px 0 10px}
html[lang="ar"] .pg-h1,html[lang="fa"] .pg-h1,html[lang="ur"] .pg-h1,html[lang="ckb"] .pg-h1{font-family:var(--serif-ar);font-weight:700}
.pg-head .route{margin:0;color:var(--ink,#2B3445);font-size:16px;line-height:1.6}
.pg-head .se{margin:6px 0 0;color:var(--gold);font-weight:600;font-size:14.5px}
.pg-img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:6px;margin-top:16px;filter:saturate(1.25) contrast(1.05)}
body.pg-solo .prog-body{display:block}
"""


def esc(s): return html.escape(s, quote=True)
def txt(s): return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
def home_of(l): return "/" if l == "ar" else f"/{l}/"
def src_of(l): return ROOT / ("index.html" if l == "ar" else f"{l}/index.html")
def url_of(l, k): return SITE + home_of(l) + "tours/" + PROGS[k]["slug"] + "/"
def dst_of(l, k): return ROOT / home_of(l).strip("/") / "tours" / PROGS[k]["slug"] / "index.html"


def meta_set(s, attr, key, val):
    pat = re.compile(rf'<meta {attr}="{re.escape(key)}" content="[^"]*">')
    tag = f'<meta {attr}="{key}" content="{esc(val)}">'
    return pat.sub(lambda m: tag, s, count=1) if pat.search(s) else s


def trunc(t, n=158):
    if len(t) <= n: return t
    t = t[:n]
    return (t.rsplit(" ", 1)[0] if " " in t[-40:] else t).rstrip(",.،、·:： ") + "…"


def title_of(l, k):
    kw = KW[l][0 if k == "7" else 1]
    full = f"{kw} | Fable Tour"
    return full if len(full) <= 60 else kw


def section_bounds(s, start_pat):
    a = s.find(start_pat)
    a = s.rfind("<section", 0, a)
    e = s.find("</section>", a) + len("</section>")
    return a, e


def find_sec(s, sid):
    return section_bounds(s, f'id="{sid}"')


def build(l, k):
    P = PROGS[k]; pid = P["pid"]; other = PROGS["9" if k == "7" else "7"]["pid"]
    s = src_of(l).read_text(encoding="utf-8")
    home = home_of(l); url = url_of(l, k)
    lang = re.search(r'<html[^>]*lang="([^"]+)"', s).group(1)
    rtl = 'dir="rtl"' in s[:300]

    # ---- data from the homepage itself (no new facts) ----
    card = re.search(rf'<article class="pc" data-prog="{pid}">.*?</article>', s, re.S).group(0)
    name = txt(re.search(r'<h3[^>]*>(.*?)</h3>', card, re.S).group(1))
    eyebrow = re.search(r'<span class="eyebrow">(.*?</span>)</span>', card, re.S).group(1)
    route = txt(re.search(r'<p class="route">(.*?)</p>', card, re.S).group(1))
    se = txt(re.search(r'<p class="se">(.*?)</p>', card, re.S).group(1))
    a, e = s.find(f'<section class="prog" id="{pid}"'), None
    e = s.find("</section>", a) + len("</section>")
    prog = s[a:e]
    amount = txt(re.search(r'<div class="amount"[^>]*>(.*?)<small>', prog, re.S).group(1))
    cur = txt(re.search(r'<div class="amount"[^>]*>.*?<small>(.*?)</small>', prog, re.S).group(1))
    per = txt(re.search(r'<div class="per">(.*?)</div>', prog, re.S).group(1))
    tag = txt(re.search(r'<div class="tag">(.*?)</div>', prog, re.S).group(1))
    cols = re.findall(r'<div class="pcol( no)?"><h3>.*?</h3><ul>(.*?)</ul>', prog, re.S)
    inc = [txt(x) for x in re.findall(r"<li>(.*?)</li>", cols[0][1], re.S)]
    noinc = [txt(x) for x in re.findall(r"<li>(.*?)</li>", cols[1][1], re.S)]
    assert "2,500" in amount if k == "7" else "3,400" in amount, (l, k, amount)

    # ---- asset paths absolute (page sits two folders deeper) ----
    s = re.sub(r'(?<=["\'(|=])\.\./', "/", s)
    s = re.sub(r'(?<=["\'(|])(img/|hero\.jpg|favicon\.png|apple-touch-icon\.png|logo\.png|og-image\.jpg)', r"/\1", s)

    # ---- head ----
    title = title_of(l, k)
    kw = KW[l][0 if k == "7" else 1]
    sep = "" if l in ("zh", "zh-tw", "ja") else " "
    dot = "。" if l in ("zh", "zh-tw", "ja") else ". "
    desc = trunc(f"{kw}{dot}{amount} {per}{dot}{route}{dot}{se}".replace(" .", "."), 158)
    og = f"{SITE}/img/og/{P['slug']}.jpg"
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, count=1, flags=re.S)
    s = meta_set(s, "name", "description", desc)
    s = re.sub(r'<meta name="keywords" content="[^"]*">\n?', "", s)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    # hreflang cluster: only languages that get the page (+ x-default = English)
    s = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", s)
    alts = "".join(f'<link rel="alternate" hreflang="{HREFLANG.get(x, x)}" href="{url_of(x, k)}">\n' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url_of("en", k)}">\n'
    i = s.find("<link rel=\"icon\"")
    s = s[:i] + alts + s[i:]
    s = meta_set(s, "property", "og:type", "article")
    for at, key, val in [("property", "og:title", title), ("property", "og:description", desc), ("property", "og:url", url),
                         ("property", "og:image", og), ("property", "og:image:alt", name),
                         ("name", "twitter:title", title), ("name", "twitter:description", desc), ("name", "twitter:image", og)]:
        s = meta_set(s, at, key, val)
    s = re.sub(r'<meta property="og:image:(width|height)" content="[^"]*">', lambda m: f'<meta property="og:image:{m.group(1)}" content="{1200 if m.group(1)=="width" else 630}">', s)

    # ---- FAQ (program questions + general homepage questions except the two that compare both programs) ----
    fa, fe = find_sec(s, "faq")
    hf = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", s[fa:fe], re.S)
    d = FADIG[k] if l == "fa" else k
    q = [x.replace("{d}", d) for x in FQ[l]]
    lst = "、" if l in ("zh", "zh-tw", "ja") else ("، " if l in ("ar", "fa", "ur", "ckb") else "; ")
    faq = [(q[0], f"{amount} {cur} {per}{dot}{tag}".strip()),
           (q[1], lst.join(inc)),
           (q[2], lst.join(noinc)),
           (q[3], f"{se}{dot}{route}")]
    faq_html = "".join(f"<details><summary>{esc(a_)}</summary><p>{esc(b_)}</p></details>" for a_, b_ in faq)
    faq_html += "".join(f"<details><summary>{a_}</summary><p>{b_}</p></details>" for j, (a_, b_) in enumerate(hf) if j not in (1, 2))
    faq_ld = [(a_, b_) for a_, b_ in faq] + [(txt(a_), txt(b_)) for j, (a_, b_) in enumerate(hf) if j not in (1, 2)]
    sec = s[fa:fe]
    sec = re.sub(r'(<div class="faq">).*?(</div>\s*</section>)', lambda m: m.group(1) + faq_html + m.group(2), sec, count=1, flags=re.S)
    s = s[:fa] + sec + s[fe:]

    # ---- JSON-LD ----
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    g = json.loads(m.group(1)); nodes = g.get("@graph", [g])
    org = next(n for n in nodes if n.get("@type") == "TravelAgency")
    website = next((n for n in nodes if n.get("@type") == "WebSite"), None)
    progs = next(n for n in nodes if n.get("@type") == "ItemList" and str(n.get("@id", "")).endswith("#programs"))
    trip = next(it["item"] for it in progs["itemListElement"] if it["item"]["@id"].endswith("#" + pid))
    trip = json.loads(json.dumps(trip))
    trip["@id"] = url + "#trip"; trip["url"] = url; trip["name"] = name
    trip["image"] = [og, SITE + "/" + P["img"]]
    trip["offers"]["url"] = url
    trip["provider"] = {"@id": org["@id"]}
    ld = {"@context": "https://schema.org", "@graph": [x for x in [
        org, website,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": lang,
         "primaryImageOfPage": og, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": url + "#trip"},
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        trip,
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Fable Tour", "item": SITE + home},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": a_, "acceptedAnswer": {"@type": "Answer", "text": b_}} for a_, b_ in faq_ld]},
    ] if x]}
    s = s[:m.start()] + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>" + s[m.end():]
    # any other JSON-LD blocks (e.g. a second FAQPage) are dropped to keep one clean graph
    first = s.find('<script type="application/ld+json">')
    s = s[:first + 10] + re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", s[first + 10:], flags=re.S)

    # ---- body ----
    s = re.sub(r'<h1 class="disp"([^>]*)>(.*?)</h1>', r'<div class="disp hero-h1"\1>\2</div>', s, count=1, flags=re.S)
    s = re.sub(r"<body([^>]*)>", lambda mm: mm.group(0) if "pg-solo" in mm.group(1) else
               (mm.group(0).replace('class="', 'class="pg-solo ', 1) if "class=" in mm.group(1) else f'<body class="pg-solo" data-prog="{pid}">'), s, count=1)
    # drop sections that belong to other products (the day-trip pages drop most of these too)
    for sid in ("video", "day-trips", "airport-transfer", "guide", "video-journeys", "gallery", "karbala-story", "usa-canada"):
        if f'id="{sid}"' in s:
            a_, e_ = find_sec(s, sid)
            s = s[:a_] + s[e_:]
    # the other program + the two-card chooser
    a_ = s.find(f'<section class="prog" id="{other}"'); e_ = s.find("</section>", a_) + len("</section>")
    s = s[:a_] + s[e_:]
    s = re.sub(r'<div class="pc-wrap">.*?<div class="pc-dots"></div></div>', "", s, count=1, flags=re.S)
    s = re.sub(r'<a class="pcard"[^>]*>.*?</a>', "", s, flags=re.S)  # "choose your programme" cards, if any
    s = s.replace(f'<div class="prog-body" id="pb-{pid}" hidden>', f'<div class="prog-body" id="pb-{pid}">', 1)
    # head block: back link, eyebrow (program no. + price), H1, route, start/end, photo
    arrow = "→" if rtl else "←"
    alt = f"{name} · {route.split(' · ')[0]}" if " · " in route else name
    w, h = (1284, 908) if k == "7" else (1600, 1200)
    head = (f'<div class="pg-head"><a class="pg-all" href="{home}">{arrow} {esc(ALL[l])}</a>'
            f'<span class="eyebrow">{eyebrow}</span><h1 class="pg-h1">{esc(name)}</h1>'
            f'<p class="route">{esc(route)}</p><p class="se">{esc(se)}</p>'
            f'<img class="pg-img" src="/{P["img"]}" alt="{esc(alt)}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div>')
    s = re.sub(r'<div class="letter">.*?</div>', "", s, count=1, flags=re.S)  # homepage intro (both programs)
    s = re.sub(r'(<main[^>]*>)', lambda mm: mm.group(1) + '\n  <div class="in pg-top">' + head + "</div>", s, count=1)
    # booking form: this program preselected
    def _sel(mm):
        opts = mm.group(1).replace(" selected", "")
        return re.sub(r'(<option value="[^"]*")>', lambda o: o.group(1) + (" selected>" if f"{k} days" in o.group(1) else ">"), opts)
    s = re.sub(r'(<select id="f-prog" name="program">.*?</select>)', _sel, s, count=1, flags=re.S)
    # in-page anchors that pointed at removed sections
    for sid in ("day-trips", "airport-transfer", "guide", "gallery", "video", "video-journeys", "karbala-story", "usa-canada"):
        s = s.replace(f'href="#{sid}"', f'href="{home}#{sid}"')
    s = s.replace(f'href="#{other}"', f'href="{home}#{other}"')
    # language menu goes to the same program page
    s = re.sub(r'location\.href="/"\+\(v==="ar"\?"":v\+"/"\)\+location\.hash;',
               f'location.href="/"+(v==="ar"?"":v+"/")+"tours/{P["slug"]}/";', s)
    # the homepage script would overwrite <title> with the homepage title
    s = s.replace("document.title=t.title;", "")
    # css
    if "/* program page */" not in s:
        i = s.find("</style>"); s = s[:i] + CSS + s[i:]
    dst = dst_of(l, k)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(s, encoding="utf-8")
    return title, desc, name


def link_homes():
    """program titles on the homepage cards link to the program pages; homepage TouristTrip url -> page"""
    n = 0
    for l in LANGS:
        f = src_of(l); s = f.read_text(encoding="utf-8"); t = s
        for k, P in PROGS.items():
            href = home_of(l) + "tours/" + P["slug"] + "/"
            if not dst_of(l, k).exists():
                continue
            pat = re.compile(rf'(<h3 class="disp" id="{P["pid"]}-h">)(?!<a )(.*?)(</h3>)', re.S)
            t = pat.sub(lambda m: f'{m.group(1)}<a class="pg-tl" href="{href}" style="color:inherit;text-decoration:none">{m.group(2)}</a>{m.group(3)}', t, count=1)
            t = t.replace(f'"url": "{SITE}{home_of(l)}#{P["pid"]}"', f'"url": "{SITE}{href}"')
        if t != s:
            f.write_text(t, encoding="utf-8"); n += 1
    return n


def sitemap():
    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    s = re.sub(r"  <url>\n    <loc>[^<]*/tours/iraq-[79]-day-tour/</loc>.*?</url>\n", "", s, flags=re.S)
    blocks = ""
    for k, P in PROGS.items():
        alts = "".join(f'    <xhtml:link rel="alternate" hreflang="{HREFLANG.get(x, x)}" href="{url_of(x, k)}"/>\n' for x in LANGS)
        alts += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_of("en", k)}"/>\n'
        for l in LANGS:
            blocks += (f"  <url>\n    <loc>{url_of(l, k)}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n{alts}"
                       f"    <image:image><image:loc>{SITE}/img/og/{P['slug']}.jpg</image:loc></image:image>\n  </url>\n")
    s = s.replace("</urlset>", blocks + "</urlset>")
    sm.write_text(s, encoding="utf-8")


def og_images():
    from PIL import Image
    for k, P in PROGS.items():
        out = ROOT / "img" / "og" / f"{P['slug']}.jpg"
        im = Image.open(ROOT / P["img"]).convert("RGB")
        W, H = im.size; th = int(W * 630 / 1200)
        if th > H:
            tw = int(H * 1200 / 630); x = (W - tw) // 2; im = im.crop((x, 0, x + tw, H))
        else:
            y = (H - th) // 2; im = im.crop((0, y, W, y + th))
        im.resize((1200, 630), Image.LANCZOS).save(out, "JPEG", quality=84, optimize=True, progressive=True)


def run():
    og_images()
    for l in LANGS:
        for k in PROGS:
            t, d, n = build(l, k)
            print(l, k, len(t), t, "|", len(d))
    print("homepages linked:", link_homes())
    sitemap()


if __name__ == "__main__":
    run()
    import add_us_phone; add_us_phone.run()
