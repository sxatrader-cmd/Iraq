#!/usr/bin/env python3
"""Country landing pages "Iraq tours from <country>" (Oct 2026): Thailand, Pakistan, Kuwait,
Bahrain, Oman, UAE, Lebanon, Jordan, Iran, Turkey.
Each market gets two pages: the local language (copy of that language's homepage) and English
(copy of the English homepage), with their own title/description/H1, a "travellers from X" panel
(visa, getting there, what to see), hreflang pair, JSON-LD WebPage and sitemap entries.
The local homepages get a small banner linking to their market page(s). Idempotent.
Visa rules are NOT stated per nationality (they change); the text points to the official
e-visa portal and to Fable Tour's visa service, as on the rest of the site."""
import re, json, html, posixpath, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://iraq.fabletour.com"
TODAY = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)).date().isoformat()
esc = lambda s: html.escape(s, quote=True)

# ---------------------------------------------------------------- shared text blocks
VISA = {
 "en": ("Iraq visa", "Iraq visas are issued through the official e-visa portal (evisa.iq), which also covers the Kurdistan Region. Rules differ by nationality and change from time to time, so check your eligibility on the portal or with the Iraqi embassy before you book. If your nationality cannot apply online, we obtain the visa for you (US$300) when you book a full tour — half is paid in advance, the rest on arrival."),
 "ar": ("تأشيرة العراق", "تصدر تأشيرات العراق عبر بوابة التأشيرة الإلكترونية الرسمية (evisa.iq)، وتشمل إقليم كردستان أيضاً. تختلف الشروط حسب الجنسية وتتغير من وقت لآخر، لذا تأكد من أهليتك عبر البوابة أو من السفارة العراقية قبل الحجز. إذا لم تتمكن جنسيتك من التقديم إلكترونياً، نستخرج لك التأشيرة (300 دولار) عند حجز برنامج كامل، ويُدفع نصف المبلغ مقدماً والباقي عند الوصول."),
 "th": ("วีซ่าอิรัก", "วีซ่าอิรักออกผ่านพอร์ทัลวีซ่าอิเล็กทรอนิกส์อย่างเป็นทางการ (evisa.iq) ซึ่งครอบคลุมเขตปกครองตนเองเคอร์ดิสถานด้วย เงื่อนไขแตกต่างกันตามสัญชาติและอาจเปลี่ยนแปลงได้ โปรดตรวจสอบสิทธิ์ของคุณผ่านพอร์ทัลหรือสถานทูตอิรักก่อนจอง หากสัญชาติของคุณไม่สามารถยื่นออนไลน์ได้ เราจะดำเนินการขอวีซ่าให้ (300 ดอลลาร์สหรัฐ) เมื่อจองทริปเต็มโปรแกรม โดยชำระครึ่งหนึ่งล่วงหน้าและส่วนที่เหลือเมื่อเดินทางถึง"),
 "ur": ("عراق کا ویزا", "عراق کے ویزے سرکاری ای ویزا پورٹل (evisa.iq) کے ذریعے جاری ہوتے ہیں، جو کردستان ریجن کا بھی احاطہ کرتا ہے۔ شرائط ہر قومیت کے لیے مختلف ہیں اور وقتاً فوقتاً بدلتی رہتی ہیں، اس لیے بکنگ سے پہلے پورٹل یا عراقی سفارت خانے سے اپنی اہلیت ضرور چیک کریں۔ اگر آپ کی قومیت آن لائن درخواست نہیں دے سکتی تو مکمل ٹور بک کرنے پر ہم آپ کا ویزا (300 امریکی ڈالر) خود لگواتے ہیں — آدھی رقم پیشگی اور باقی پہنچنے پر۔"),
 "fa": ("ویزای عراق", "ویزای عراق از طریق درگاه رسمی ویزای الکترونیکی (evisa.iq) صادر می‌شود که اقلیم کردستان را هم در بر می‌گیرد. شرایط برای هر ملیت متفاوت است و گاهی تغییر می‌کند؛ پس پیش از رزرو، شرایط خود را در درگاه یا از سفارت عراق بررسی کنید. اگر ملیت شما امکان درخواست آنلاین ندارد، با رزرو یک برنامهٔ کامل، ویزا را خودمان برایتان می‌گیریم (۳۰۰ دلار)؛ نیمی پیش‌پرداخت و باقی هنگام ورود."),
 "tr": ("Irak vizesi", "Irak vizeleri, Kürdistan Bölgesi'ni de kapsayan resmi e-vize portalı (evisa.iq) üzerinden verilir. Koşullar uyruğa göre değişir ve zaman zaman güncellenir; rezervasyondan önce uygunluğunuzu portaldan veya Irak büyükelçiliğinden kontrol edin. Uyruğunuz çevrimiçi başvuru yapamıyorsa, tam bir tur rezervasyonunda vizenizi biz alırız (300 ABD doları); yarısı önceden, kalanı varışta ödenir."),
}
# label for: eyebrow / panel heading / "getting there" / "what to see" / "Book now" / banner button
UI = {
 "en": ("Travellers from {c}", "Iraq tours from {c}", "Getting to Iraq from {c}", "What to see", "See the programmes ↓"),
 "ar": ("للمسافرين من {c}", "رحلات إلى العراق من {c}", "السفر من {c} إلى العراق", "ماذا ستزور", "اطّلع على البرامج ↓"),
 "th": ("สำหรับนักเดินทางจาก{c}", "ทัวร์อิรักจาก{c}", "เดินทางจาก{c}ไปอิรัก", "ไฮไลต์ที่จะได้ชม", "ดูโปรแกรมทัวร์ ↓"),
 "ur": ("{c} سے آنے والے مسافروں کے لیے", "{c} سے عراق کے ٹور", "{c} سے عراق کا سفر", "کیا دیکھیں گے", "پروگرام دیکھیں ↓"),
 "fa": ("برای مسافران {c}", "تور عراق از {c}", "سفر از {c} به عراق", "چه می‌بینید", "دیدن برنامه‌ها ↓"),
 "tr": ("{c}'den gelen gezginler için", "{c}'den Irak turları", "{c}'den Irak'a ulaşım", "Neler göreceksiniz", "Programları görün ↓"),
}
IMG = {"shrines": "wadi-al-salam", "babylon": "babylon-ishtar-gate", "marshes": "marshes-mashoof",
       "kadhimiya": "kadhimiya-shrine-night", "samarra": "samarra-malwiya", "ctesiphon": "taq-kasra",
       "qishla": "qishla-clock-tower-view", "mosul": "mosul-al-hadba-nuri", "gilani": "junayd-baghdadi-shrine",
       "basra": "basra-shatt-al-arab-sunset", "ur": "ur-ziggurat", "hatra": "hatra"}

# ---------------------------------------------------------------- markets
# slug, local language, country name per language, page texts per language
M = {}

def market(key, slug, local, names, texts):
    M[key] = {"slug": slug, "local": local, "names": names, "texts": texts}

# Gulf / Levant (Arabic + English) -----------------------------------------
GULF_HL_AR = [("shrines", "زيارة كربلاء والنجف", "مرقد الإمام الحسين وأخيه العباس (ع) في كربلاء، ومرقد الإمام علي (ع) في النجف، ومسجد الكوفة ووادي السلام."),
              ("kadhimiya", "بغداد والكاظمية وسامراء", "مرقد الكاظمية، وجامع الإمام أبي حنيفة، والشيخ عبد القادر الكيلاني، ومرقد العسكريين والملوية في سامراء."),
              ("babylon", "بابل وأور والأهوار", "بوابة عشتار وأسد بابل، وزقورة أور، وجولة بالمشحوف في الأهوار مع غداء المسكوف.")]
GULF_HL_EN = [("shrines", "Karbala & Najaf ziyarah", "The shrines of Imam Hussein and al-Abbas in Karbala, Imam Ali in Najaf, the Great Mosque of Kufa and Wadi al-Salam."),
              ("kadhimiya", "Baghdad, Kadhimiya & Samarra", "Al-Kadhimiya shrine, Abu Hanifa Mosque, Sheikh Abdul Qadir al-Gilani, the Askari shrine and the Malwiya in Samarra."),
              ("babylon", "Babylon, Ur & the Marshes", "The Ishtar Gate and the Lion of Babylon, the ziggurat of Ur and a mashoof boat ride in the Marshes with a masgouf lunch.")]

market("kuwait", "iraq-tours-from-kuwait", "ar", {"ar": "الكويت", "en": "Kuwait"}, {
 "ar": dict(title="رحلات إلى العراق من الكويت: زيارة كربلاء والنجف وبابل | Fable Tour",
   desc="رحلات سياحية وزيارات إلى العراق من الكويت مع مرشد من بغداد: كربلاء والنجف والكاظمية وبابل والأهوار. برنامج 7 أيام أو 9 أيام من البصرة إلى أربيل.",
   kw="رحلات العراق من الكويت, زيارة كربلاء من الكويت, حملات زيارة العراق, سفر الكويت العراق, زيارة النجف, رحلة بابل, سياحة العراق, Fable Tour",
   h1="رحلات إلى العراق من الكويت", lead="زيارة كربلاء والنجف والكاظمية وسامراء، مع بابل وأور والأهوار — برنامجان بفنادق 4 و5 نجوم ومرشد خاص، من 2,500 دولار.",
   intro="العراق على بُعد ساعة طيران من الكويت، والبصرة على بُعد ساعتين تقريباً بالسيارة. نرتب لك ولعائلتك برنامجاً خاصاً بمرشد من بغداد يتحدث العربية، بالتاريخ الذي تختاره.",
   travel="رحلات جوية قصيرة من مطار الكويت الدولي إلى بغداد والنجف والبصرة تستغرق قرابة الساعة (تحقق من الجداول الحالية لدى شركات الطيران). ويمكن الوصول براً عبر منفذ العبدلي–سفوان إلى البصرة، وهي نقطة بداية برنامج الأيام التسعة. نستقبلك في المطار أو عند وصولك إلى البصرة.",
   hl=GULF_HL_AR),
 "en": dict(title="Iraq Tours from Kuwait: Karbala, Najaf & Babylon | Fable Tour",
   desc="Iraq tours from Kuwait with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, Babylon and the Marshes. 7 days from Baghdad or 9 days from Basra to Erbil.",
   kw="Iraq tours from Kuwait, Kuwait to Iraq trip, Karbala ziyarah from Kuwait, Najaf tour, Babylon tour, Basra tour, Fable Tour",
   h1="Iraq tours from Kuwait", lead="Ziyarah to Karbala, Najaf, Kadhimiya and Samarra, plus Babylon, Ur and the Marshes — two programmes with 4★–5★ hotels and a private guide, from US$2,500.",
   intro="Iraq is about an hour's flight from Kuwait, and Basra roughly two hours by road. We arrange a private programme for you and your family with an Arabic-speaking guide from Baghdad, on the date you choose.",
   travel="Short flights from Kuwait International Airport to Baghdad, Najaf and Basra take about an hour (check current airline schedules). You can also cross by land at Abdali–Safwan to Basra, where our 9-day programme begins. We meet you at the airport or on arrival in Basra.",
   hl=GULF_HL_EN)})

market("bahrain", "iraq-tours-from-bahrain", "ar", {"ar": "البحرين", "en": "Bahrain"}, {
 "ar": dict(title="رحلات إلى العراق من البحرين: كربلاء والنجف وبغداد | Fable Tour",
   desc="رحلات وزيارات إلى العراق من البحرين مع مرشد من بغداد: كربلاء والنجف والكاظمية وسامراء وبابل. برنامج 7 أو 9 أيام بفنادق 4–5 نجوم وتاريخ تختاره.",
   kw="رحلات العراق من البحرين, زيارة كربلاء من البحرين, حملات الزيارة البحرين, زيارة النجف, زيارة الكاظمية, سياحة العراق, Fable Tour",
   h1="رحلات إلى العراق من البحرين", lead="زيارة كربلاء والنجف والكاظمية وسامراء، مع بابل والأهوار وأور — برنامجان خاصان بمرشد عربي وفنادق 4 و5 نجوم، من 2,500 دولار.",
   intro="سواء كانت زيارة للعتبات المقدسة أو رحلة لاكتشاف بلاد الرافدين، نرتب لك برنامجاً خاصاً بالتاريخ الذي يناسبك، مع مرشد من بغداد وسيارة خاصة طوال الرحلة.",
   travel="تتوفر رحلات من مطار البحرين الدولي إلى بغداد والنجف تستغرق نحو ساعتين (تحقق من الجداول الحالية لدى شركات الطيران)، أو عبر دبي والدوحة. نستقبلك في المطار ونتولى كل التنقلات.",
   hl=GULF_HL_AR),
 "en": dict(title="Iraq Tours from Bahrain: Karbala, Najaf & Baghdad | Fable Tour",
   desc="Iraq tours from Bahrain with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, Samarra and Babylon. 7 or 9 days with 4★–5★ hotels, on the date you choose.",
   kw="Iraq tours from Bahrain, Bahrain to Iraq trip, Karbala ziyarah from Bahrain, Najaf tour, Kadhimiya, Babylon tour, Fable Tour",
   h1="Iraq tours from Bahrain", lead="Ziyarah to Karbala, Najaf, Kadhimiya and Samarra, plus Babylon, the Marshes and Ur — two private programmes with an Arabic-speaking guide and 4★–5★ hotels, from US$2,500.",
   intro="Whether you come for the holy shrines or to discover Mesopotamia, we arrange a private programme on the date that suits you, with a guide from Baghdad and a private car throughout.",
   travel="Flights from Bahrain International Airport to Baghdad and Najaf take around two hours (check current airline schedules), or connect via Dubai or Doha. We meet you at the airport and handle every transfer.",
   hl=GULF_HL_EN)})

market("oman", "iraq-tours-from-oman", "ar", {"ar": "سلطنة عُمان", "en": "Oman"}, {
 "ar": dict(title="رحلات إلى العراق من سلطنة عُمان: بابل وكربلاء والنجف | Fable Tour",
   desc="رحلات سياحية إلى العراق من سلطنة عُمان مع مرشد من بغداد: بابل وأور والأهوار وكربلاء والنجف وسامراء. برنامج 7 أو 9 أيام بفنادق 4–5 نجوم.",
   kw="رحلات العراق من عمان, سياحة العراق من مسقط, رحلة بابل, زيارة كربلاء والنجف, الأهوار, سفر مسقط بغداد, Fable Tour",
   h1="رحلات إلى العراق من سلطنة عُمان", lead="من بابل وأور والأهوار في الجنوب إلى سامراء والحضر وأربيل في الشمال، مع كربلاء والنجف — برنامجان بمرشد خاص وفنادق 4 و5 نجوم، من 2,500 دولار.",
   intro="العراق وجهة قريبة من مسقط، تجمع أقدم حضارات العالم مع المراقد المقدسة والأسواق التراثية. نرتب لك رحلة خاصة لك ولعائلتك بالتاريخ الذي تختاره.",
   travel="تتوفر رحلات من مطار مسقط الدولي إلى بغداد في بعض الأيام، أو عبر دبي والدوحة (تحقق من الجداول الحالية لدى شركات الطيران). مدة الطيران المباشر نحو ثلاث ساعات. نستقبلك في المطار ونتولى كل التنقلات.",
   hl=[("babylon", "بابل وأور", "بوابة عشتار وأسد بابل وقصر نبوخذنصر، وزقورة أور السومرية التي يزيد عمرها على أربعة آلاف عام."),
       ("marshes", "الأهوار والبصرة", "جولة بالمشحوف بين القصب والجاموس، وغروب الشمس على شط العرب في البصرة."),
       ("shrines", "كربلاء والنجف وسامراء", "مرقد الإمام الحسين والعباس (ع)، ومرقد الإمام علي (ع)، ومنارة الملوية في سامراء.")]),
 "en": dict(title="Iraq Tours from Oman: Babylon, Karbala & Najaf | Fable Tour",
   desc="Iraq tours from Oman with a Baghdad-based guide: Babylon, Ur, the Marshes, Karbala, Najaf and Samarra. 7 or 9 days with 4★–5★ hotels and a private guide.",
   kw="Iraq tours from Oman, Muscat to Baghdad trip, Iraq holiday from Oman, Babylon tour, Karbala Najaf ziyarah, Iraq Marshes, Fable Tour",
   h1="Iraq tours from Oman", lead="From Babylon, Ur and the Marshes in the south to Samarra, Hatra and Erbil in the north, with Karbala and Najaf — two programmes with a private guide and 4★–5★ hotels, from US$2,500.",
   intro="Iraq is a short trip from Muscat, combining the world's oldest civilisations with holy shrines and heritage markets. We arrange a private trip for you and your family on the date you choose.",
   travel="Flights from Muscat International Airport to Baghdad operate on some days, or connect via Dubai or Doha (check current airline schedules). A direct flight takes about three hours. We meet you at the airport and handle every transfer.",
   hl=[("babylon", "Babylon & Ur", "The Ishtar Gate, the Lion of Babylon and Nebuchadnezzar's palace, and the Sumerian ziggurat of Ur, over four thousand years old."),
       ("marshes", "The Marshes & Basra", "A mashoof boat ride among reeds and water buffalo, and sunset over the Shatt al-Arab in Basra."),
       ("shrines", "Karbala, Najaf & Samarra", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali, and the Malwiya minaret in Samarra.")])})

market("uae", "iraq-tours-from-uae", "ar", {"ar": "الإمارات", "en": "the UAE"}, {
 "ar": dict(title="رحلات إلى العراق من الإمارات: دبي إلى بغداد وبابل وكربلاء | Fable Tour",
   desc="رحلات إلى العراق من دبي وأبوظبي والشارقة مع مرشد من بغداد: بابل وأور والأهوار وكربلاء والنجف. للمواطنين والمقيمين، برنامج 7 أو 9 أيام.",
   kw="رحلات العراق من الإمارات, رحلة من دبي إلى بغداد, سياحة العراق من دبي, زيارة كربلاء من الإمارات, رحلة بابل, Fable Tour",
   h1="رحلات إلى العراق من الإمارات", lead="للمواطنين والمقيمين في الإمارات: بابل وأور والأهوار، وكربلاء والنجف والكاظمية، وسامراء والحضر وأربيل — برنامجان بمرشد خاص وفنادق 4 و5 نجوم، من 2,500 دولار.",
   intro="من دبي إلى بغداد أقل من ثلاث ساعات طيران. سواء كنت مواطناً أو مقيماً في الإمارات من أي جنسية، نرتب لك رحلة خاصة أو تنضم إلى مجموعة صغيرة بالتاريخ الذي يناسبك.",
   travel="رحلات يومية كثيرة من دبي والشارقة وأبوظبي إلى بغداد والبصرة والنجف وأربيل، ومدة الطيران نحو ساعتين ونصف (تحقق من الجداول الحالية لدى شركات الطيران). برنامج الأيام السبعة يبدأ وينتهي في بغداد، وبرنامج الأيام التسعة يبدأ في البصرة وينتهي في أربيل.",
   hl=[("babylon", "بابل وأور والأهوار", "بوابة عشتار وأسد بابل، وزقورة أور، والمشحوف في الأهوار مع غداء المسكوف."),
       ("shrines", "كربلاء والنجف والكوفة", "مرقد الإمام الحسين والعباس (ع)، ومرقد الإمام علي (ع)، ومسجد الكوفة الكبير."),
       ("qishla", "بغداد القديمة", "شارع المتنبي والقشلة ومقهى الشابندر والمدرسة المستنصرية — قلب بغداد العباسية.")]),
 "en": dict(title="Iraq Tours from the UAE: Dubai to Baghdad, Babylon & Karbala | Fable Tour",
   desc="Iraq tours from Dubai, Abu Dhabi and Sharjah with a Baghdad-based guide: Babylon, Ur, the Marshes, Karbala and Najaf. For UAE citizens and residents, 7 or 9 days.",
   kw="Iraq tours from UAE, Dubai to Baghdad tour, Iraq trip from Dubai, Iraq holiday UAE residents, Babylon tour, Karbala Najaf ziyarah, Fable Tour",
   h1="Iraq tours from the UAE", lead="For UAE citizens and residents: Babylon, Ur and the Marshes, Karbala, Najaf and Kadhimiya, Samarra, Hatra and Erbil — two programmes with a private guide and 4★–5★ hotels, from US$2,500.",
   intro="Baghdad is less than three hours' flight from Dubai. Whether you are an Emirati citizen or a UAE resident of any nationality, we arrange a private trip or a place in a small group on the date that suits you.",
   travel="Many daily flights connect Dubai, Sharjah and Abu Dhabi with Baghdad, Basra, Najaf and Erbil, about two and a half hours (check current airline schedules). The 7-day programme starts and ends in Baghdad; the 9-day programme starts in Basra and ends in Erbil.",
   hl=[("babylon", "Babylon, Ur & the Marshes", "The Ishtar Gate and the Lion of Babylon, the ziggurat of Ur and a mashoof boat in the Marshes with a masgouf lunch."),
       ("shrines", "Karbala, Najaf & Kufa", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali and the Great Mosque of Kufa."),
       ("qishla", "Old Baghdad", "Mutanabbi Street, the Qishla, Shabandar Café and the Mustansiriya — the heart of Abbasid Baghdad.")])})

market("lebanon", "iraq-tours-from-lebanon", "ar", {"ar": "لبنان", "en": "Lebanon"}, {
 "ar": dict(title="رحلات إلى العراق من لبنان: زيارة كربلاء والنجف وبابل | Fable Tour",
   desc="رحلات وزيارات إلى العراق من بيروت مع مرشد من بغداد: كربلاء والنجف والكاظمية وسامراء وبابل والأهوار. برنامج 7 أو 9 أيام بفنادق 4–5 نجوم.",
   kw="رحلات العراق من لبنان, زيارة كربلاء من بيروت, زيارة العتبات المقدسة, سفر بيروت بغداد, زيارة النجف, رحلة بابل, Fable Tour",
   h1="رحلات إلى العراق من لبنان", lead="زيارة العتبات المقدسة في كربلاء والنجف والكاظمية وسامراء، مع بابل وأور والأهوار — برنامجان بمرشد خاص وفنادق 4 و5 نجوم، من 2,500 دولار.",
   intro="من بيروت إلى بغداد أو النجف رحلة قصيرة. نرتب لك زيارة مريحة ومنظمة لك ولعائلتك، مع مرشد يتحدث العربية وسيارة خاصة، وتمر في الطريق على أعظم آثار بلاد الرافدين.",
   travel="تتوفر رحلات من مطار رفيق الحريري الدولي في بيروت إلى بغداد والنجف تستغرق نحو ساعتين (تحقق من الجداول الحالية لدى شركات الطيران). نستقبلك في المطار ونتولى كل التنقلات.",
   hl=GULF_HL_AR),
 "en": dict(title="Iraq Tours from Lebanon: Karbala, Najaf & Babylon | Fable Tour",
   desc="Iraq tours from Beirut with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, Samarra, Babylon and the Marshes. 7 or 9 days with 4★–5★ hotels.",
   kw="Iraq tours from Lebanon, Beirut to Baghdad trip, Karbala ziyarah from Lebanon, Najaf tour, Babylon tour, Fable Tour",
   h1="Iraq tours from Lebanon", lead="Ziyarah to the holy shrines of Karbala, Najaf, Kadhimiya and Samarra, plus Babylon, Ur and the Marshes — two programmes with a private guide and 4★–5★ hotels, from US$2,500.",
   intro="Baghdad and Najaf are a short flight from Beirut. We arrange a comfortable, well-organised visit for you and your family, with an Arabic-speaking guide and a private car, taking in Mesopotamia's greatest sites on the way.",
   travel="Flights from Beirut–Rafic Hariri International Airport to Baghdad and Najaf take about two hours (check current airline schedules). We meet you at the airport and handle every transfer.",
   hl=GULF_HL_EN)})

market("jordan", "iraq-tours-from-jordan", "ar", {"ar": "الأردن", "en": "Jordan"}, {
 "ar": dict(title="رحلات إلى العراق من الأردن: بغداد وبابل وكربلاء | Fable Tour",
   desc="رحلات سياحية إلى العراق من عمّان مع مرشد من بغداد: بغداد القديمة وبابل وأور والأهوار وكربلاء والنجف. برنامج 7 أو 9 أيام بفنادق 4–5 نجوم.",
   kw="رحلات العراق من الأردن, سفر عمان بغداد, سياحة العراق من الأردن, رحلة بابل, زيارة كربلاء والنجف, بغداد القديمة, Fable Tour",
   h1="رحلات إلى العراق من الأردن", lead="بغداد القديمة وبابل وأور والأهوار، وكربلاء والنجف وسامراء والحضر — برنامجان بمرشد خاص وفنادق 4 و5 نجوم، من 2,500 دولار.",
   intro="الأردن والعراق جاران يجمعهما تاريخ طويل، ورحلة الطيران من عمّان إلى بغداد قصيرة. نرتب لك برنامجاً خاصاً بالتاريخ الذي تختاره، أو تنضم إلى مجموعة صغيرة.",
   travel="تتوفر رحلات من مطار الملكة علياء الدولي في عمّان إلى بغداد والبصرة وأربيل والنجف، ومدة الطيران إلى بغداد نحو ساعة ونصف (تحقق من الجداول الحالية لدى شركات الطيران). نستقبلك في المطار ونتولى كل التنقلات.",
   hl=[("qishla", "بغداد العباسية", "شارع المتنبي والقشلة والمدرسة المستنصرية ومقهى الشابندر، ومرقد الكاظمية وجامع أبي حنيفة."),
       ("babylon", "بابل وأور والأهوار", "بوابة عشتار وأسد بابل، وزقورة أور، والمشحوف في الأهوار."),
       ("hatra", "سامراء والحضر والموصل", "منارة الملوية، ومدينة الحضر الأثرية وسط الصحراء، والموصل القديمة وجامع النوري.")]),
 "en": dict(title="Iraq Tours from Jordan: Baghdad, Babylon & Karbala | Fable Tour",
   desc="Iraq tours from Amman with a Baghdad-based guide: old Baghdad, Babylon, Ur, the Marshes, Karbala and Najaf. 7 or 9 days with 4★–5★ hotels and a private guide.",
   kw="Iraq tours from Jordan, Amman to Baghdad trip, Iraq holiday from Jordan, Babylon tour, Karbala Najaf, old Baghdad, Fable Tour",
   h1="Iraq tours from Jordan", lead="Old Baghdad, Babylon, Ur and the Marshes, plus Karbala, Najaf, Samarra and Hatra — two programmes with a private guide and 4★–5★ hotels, from US$2,500.",
   intro="Jordan and Iraq are neighbours with a long shared history, and the flight from Amman to Baghdad is short. We arrange a private programme on the date you choose, or a place in a small group.",
   travel="Flights from Queen Alia International Airport in Amman serve Baghdad, Basra, Erbil and Najaf; Amman–Baghdad takes about an hour and a half (check current airline schedules). We meet you at the airport and handle every transfer.",
   hl=[("qishla", "Abbasid Baghdad", "Mutanabbi Street, the Qishla, the Mustansiriya and Shabandar Café, plus Kadhimiya and the Abu Hanifa Mosque."),
       ("babylon", "Babylon, Ur & the Marshes", "The Ishtar Gate and the Lion of Babylon, the ziggurat of Ur and a mashoof boat in the Marshes."),
       ("hatra", "Samarra, Hatra & Mosul", "The Malwiya minaret, the desert city of Hatra and Old Mosul with the al-Nuri Mosque.")])})

# Thailand ------------------------------------------------------------------
market("thailand", "iraq-tours-from-thailand", "th", {"th": "ไทย", "en": "Thailand"}, {
 "th": dict(title="ทัวร์อิรักจากไทย: บาบิโลน เมโสโปเตเมีย 7–9 วัน | Fable Tour",
   desc="ทัวร์อิรักจากประเทศไทยกับไกด์ท้องถิ่นจากแบกแดด: บาบิโลน ซิกกูรัตแห่งเมืองอูร์ บึงเมโสโปเตเมีย และซามาร์รา 7 หรือ 9 วัน โรงแรม 4–5 ดาว",
   kw="ทัวร์อิรัก, เที่ยวอิรัก, ทัวร์อิรักจากไทย, บาบิโลน, เมโสโปเตเมีย, แบกแดด, ทัวร์ตะวันออกกลาง, Fable Tour",
   h1="ทัวร์อิรักจากประเทศไทย", lead="ดินแดนเมโสโปเตเมีย อู่อารยธรรมแห่งแรกของโลก: บาบิโลน อูร์ บึงน้ำทางใต้ ซามาร์รา ฮัตรา และเออร์บิล — 2 โปรแกรม โรงแรม 4–5 ดาว พร้อมไกด์ส่วนตัว เริ่มต้น 2,500 ดอลลาร์สหรัฐ",
   intro="อิรักคือดินแดนของเมืองแรก อักษรแรก และกฎหมายฉบับแรกของมนุษยชาติ เราจัดทริปส่วนตัวสำหรับคุณและกลุ่มของคุณในวันที่คุณเลือก โดยมีไกด์จากแบกแดดดูแลตลอดการเดินทาง",
   travel="ยังไม่มีเที่ยวบินตรงจากไทยไปอิรัก เส้นทางที่สะดวกคือบินจากสุวรรณภูมิ แวะต่อเครื่องหนึ่งครั้งที่ดูไบ โดฮา หรืออิสตันบูล ไปยังแบกแดด บาสรา หรือเออร์บิล (โปรดตรวจสอบตารางบินล่าสุดกับสายการบิน) อิรักใช้เวลา UTC+3 ช้ากว่าไทย 4 ชั่วโมง เราไปรับที่สนามบินและดูแลการเดินทางทั้งหมด",
   hl=[("babylon", "บาบิโลน", "ประตูอิชทาร์ สิงโตแห่งบาบิโลน และพระราชวังของพระเจ้าเนบูคัดเนซซาร์"),
       ("marshes", "บึงเมโสโปเตเมีย", "ล่องเรือมาชูฟท่ามกลางต้นกกและควายน้ำ มรดกโลกของยูเนสโก"),
       ("samarra", "ซามาร์รา", "หออะซานมัลวียารูปเกลียว สัญลักษณ์ของราชวงศ์อับบาซียะฮ์")]),
 "en": dict(title="Iraq Tours from Thailand: Babylon & Mesopotamia | Fable Tour",
   desc="Iraq tours from Thailand with a local guide from Baghdad: Babylon, the ziggurat of Ur, the Mesopotamian Marshes and Samarra. 7 or 9 days with 4★–5★ hotels.",
   kw="Iraq tours from Thailand, Bangkok to Baghdad trip, Iraq holiday from Thailand, Babylon tour, Mesopotamia tour, Fable Tour",
   h1="Iraq tours from Thailand", lead="Mesopotamia, the cradle of civilisation: Babylon, Ur, the southern Marshes, Samarra, Hatra and Erbil — two programmes with 4★–5★ hotels and a private guide, from US$2,500.",
   intro="Iraq is the land of the first cities, the first writing and the first laws. We arrange a private trip for you and your group on the date you choose, with a guide from Baghdad throughout.",
   travel="There are no direct flights from Thailand to Iraq. The easiest route is from Bangkok Suvarnabhumi with one stop in Dubai, Doha or Istanbul to Baghdad, Basra or Erbil (check current airline schedules). Iraq is on UTC+3, four hours behind Thailand. We meet you at the airport and handle every transfer.",
   hl=[("babylon", "Babylon", "The Ishtar Gate, the Lion of Babylon and the palace of Nebuchadnezzar."),
       ("marshes", "The Mesopotamian Marshes", "A mashoof boat among reeds and water buffalo — a UNESCO World Heritage site."),
       ("samarra", "Samarra", "The spiral Malwiya minaret, symbol of the Abbasid caliphate.")])})

# Pakistan ------------------------------------------------------------------
market("pakistan", "iraq-tours-from-pakistan", "ur", {"ur": "پاکستان", "en": "Pakistan"}, {
 "ur": dict(title="پاکستان سے عراق زیارت ٹور: کربلا، نجف، بغداد | Fable Tour",
   desc="پاکستان سے عراق کی زیارت اور سیاحت بغداد کے مقامی گائیڈ کے ساتھ: کربلا، نجف، کاظمین، سامرا، غوث اعظمؒ کا مزار اور بابل۔ 7 یا 9 دن، 4–5 اسٹار ہوٹل۔",
   kw="عراق زیارت پاکستان, کربلا زیارت, نجف اشرف, زیارت ٹور عراق, غوث اعظم بغداد, عراق ٹور پیکج, Fable Tour",
   h1="پاکستان سے عراق زیارت اور ٹور", lead="کربلا، نجف اشرف، کاظمین اور سامرا کی زیارت، بغداد میں حضرت غوث اعظم شیخ عبدالقادر جیلانیؒ اور امام ابو حنیفہؒ کے مزارات، اور بابل و اُر کی سیر — 4–5 اسٹار ہوٹل اور ذاتی گائیڈ، 2,500 امریکی ڈالر سے۔",
   intro="ہم آپ اور آپ کے خاندان کے لیے آپ کی منتخب کردہ تاریخ پر نجی زیارت کا انتظام کرتے ہیں، بغداد کے گائیڈ اور پورے سفر میں نجی گاڑی کے ساتھ، تاکہ آپ آرام اور سکون سے زیارت کر سکیں۔",
   travel="کراچی، لاہور اور اسلام آباد سے دبئی، شارجہ یا دوحہ کے راستے بغداد اور نجف کی پروازیں دستیاب ہیں، اور بعض موسموں میں براہِ راست پروازیں بھی چلتی ہیں (ایئر لائن سے تازہ شیڈول ضرور چیک کریں)۔ ہم ایئرپورٹ پر آپ کا استقبال کرتے ہیں اور تمام سفری انتظامات سنبھالتے ہیں۔",
   hl=[("shrines", "کربلا اور نجف اشرف", "امام حسینؑ اور حضرت عباسؑ کے روضے، امام علیؑ کا روضہ، مسجد کوفہ اور وادی السلام۔"),
       ("gilani", "بغداد کے مزارات", "حضرت غوث اعظم شیخ عبدالقادر جیلانیؒ، امام ابو حنیفہؒ، کاظمین اور حضرت جنید بغدادیؒ کے مزارات۔"),
       ("babylon", "بابل اور اُر", "عشتار دروازہ، بابل کا شیر اور اُر کا قدیم زِگورات۔")]),
 "en": dict(title="Iraq Ziyarat Tours from Pakistan: Karbala, Najaf & Baghdad | Fable Tour",
   desc="Iraq ziyarat and tours from Pakistan with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, Samarra, the shrine of Ghaus-e-Azam and Babylon. 7 or 9 days.",
   kw="Iraq ziyarat from Pakistan, Karbala ziyarat package, Najaf ziyarat, Ghaus-e-Azam Baghdad, Iraq tour package Pakistan, Fable Tour",
   h1="Iraq ziyarat & tours from Pakistan", lead="Ziyarat to Karbala, Najaf, Kadhimiya and Samarra, the shrines of Ghaus-e-Azam Sheikh Abdul Qadir Gilani and Imam Abu Hanifa in Baghdad, plus Babylon and Ur — 4★–5★ hotels and a private guide, from US$2,500.",
   intro="We arrange a private ziyarat for you and your family on the date you choose, with a guide from Baghdad and a private car throughout, so you can visit in comfort and peace.",
   travel="Flights from Karachi, Lahore and Islamabad reach Baghdad and Najaf via Dubai, Sharjah or Doha, and direct flights operate in some seasons (always check current airline schedules). We meet you at the airport and handle every transfer.",
   hl=[("shrines", "Karbala & Najaf", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali, the Great Mosque of Kufa and Wadi al-Salam."),
       ("gilani", "The shrines of Baghdad", "Ghaus-e-Azam Sheikh Abdul Qadir Gilani, Imam Abu Hanifa, Kadhimiya and Junayd al-Baghdadi."),
       ("babylon", "Babylon & Ur", "The Ishtar Gate, the Lion of Babylon and the ancient ziggurat of Ur.")])})

# Iran ----------------------------------------------------------------------
market("iran", "iraq-tours-from-iran", "fa", {"fa": "ایران", "en": "Iran"}, {
 "fa": dict(title="تور عراق از ایران: زیارت عتبات عالیات و بابل | Fable Tour",
   desc="تور زیارتی و گردشگری عراق از ایران با راهنمای بغدادی: کربلا، نجف، کاظمین، سامرا، طاق کسری و بابل. ۷ یا ۹ روز با هتل ۴ و ۵ ستاره.",
   kw="تور عراق, تور کربلا, زیارت عتبات عالیات, تور نجف, تور کاظمین و سامرا, طاق کسری, تور بابل, Fable Tour",
   h1="تور عراق از ایران", lead="زیارت عتبات عالیات در کربلا، نجف، کاظمین و سامرا، همراه با طاق کسری در مدائن، بابل، اور و تالاب‌های جنوب — دو برنامه با هتل ۴ و ۵ ستاره و راهنمای خصوصی، از ۲٬۵۰۰ دلار.",
   intro="برای شما و خانواده‌تان، در تاریخی که انتخاب می‌کنید، سفری خصوصی و آرام ترتیب می‌دهیم؛ با راهنمایی از بغداد و خودروی اختصاصی در تمام مسیر، فراتر از کاروان‌های شلوغ.",
   travel="پروازهایی از تهران، مشهد، شیراز و اصفهان به بغداد و نجف برقرار است (برنامهٔ به‌روز را از شرکت هواپیمایی بپرسید) و مرزهای زمینی مانند مهران و شلمچه هم مسیرهای رایج زائران‌اند. ایران و عراق در سال ۲۰۲۱ لغو روادید برای سفر هوایی را اعلام کردند؛ پیش از سفر بررسی کنید که اکنون شامل حال شما می‌شود یا نه. در فرودگاه به استقبالتان می‌آییم.",
   hl=[("shrines", "کربلا و نجف", "حرم امام حسین و حضرت ابوالفضل (ع)، حرم امام علی (ع)، مسجد کوفه و وادی‌السلام."),
       ("ctesiphon", "طاق کسری و سلمان پاک", "ایوان شکوهمند ساسانی در مدائن و آرامگاه سلمان فارسی، یار ایرانی پیامبر."),
       ("samarra", "کاظمین و سامرا", "حرم کاظمین در بغداد، حرم عسکریین و منارهٔ ملویه در سامرا.")]),
 "en": dict(title="Iraq Tours from Iran: Karbala, Najaf & Ctesiphon | Fable Tour",
   desc="Iraq tours and ziyarat from Iran with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, Samarra, Ctesiphon (Taq Kasra) and Babylon. 7 or 9 days, 4★–5★ hotels.",
   kw="Iraq tours from Iran, Karbala ziyarat from Iran, Atabat tour, Najaf, Kadhimiya Samarra, Taq Kasra Ctesiphon, Babylon tour, Fable Tour",
   h1="Iraq tours from Iran", lead="Ziyarat to Karbala, Najaf, Kadhimiya and Samarra, with the Sasanian arch of Ctesiphon, Babylon, Ur and the southern Marshes — two programmes with 4★–5★ hotels and a private guide, from US$2,500.",
   intro="We arrange a calm, private trip for you and your family on the date you choose, with a guide from Baghdad and a private car throughout — an alternative to crowded group caravans.",
   travel="Flights connect Tehran, Mashhad, Shiraz and Isfahan with Baghdad and Najaf (check current airline schedules), and land crossings such as Mehran and Shalamcheh are common pilgrim routes. Iran and Iraq announced a visa waiver for air travel in 2021; check whether it currently applies to you before travelling. We meet you at the airport.",
   hl=[("shrines", "Karbala & Najaf", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali, the Great Mosque of Kufa and Wadi al-Salam."),
       ("ctesiphon", "Taq Kasra & Salman Pak", "The great Sasanian arch at Ctesiphon and the shrine of Salman al-Farsi, the Persian companion of the Prophet."),
       ("samarra", "Kadhimiya & Samarra", "The Kadhimiya shrine in Baghdad, the Askari shrine and the Malwiya minaret in Samarra.")])})

# Turkey --------------------------------------------------------------------
market("turkey", "iraq-tours-from-turkey", "tr", {"tr": "Türkiye", "en": "Turkey"}, {
 "tr": dict(title="Türkiye'den Irak Turu: Bağdat, Babil, Kerbela | Fable Tour",
   desc="Bağdatlı rehberle Türkiye'den Irak turu: Bağdat, Abdülkadir Geylani ve İmam-ı Azam türbeleri, Babil, Kerbela, Necef ve Musul. 7 veya 9 gün, 4–5 yıldızlı oteller.",
   kw="Irak turu, Bağdat turu, Türkiye'den Irak turu, Abdülkadir Geylani ziyareti, İmam-ı Azam türbesi, Kerbela Necef turu, Babil, Fable Tour",
   h1="Türkiye'den Irak turları", lead="Bağdat'ta Abdülkadir Geylani ve İmam-ı Azam Ebu Hanife türbeleri, Kerbela, Necef ve Samarra, Babil, Ur ve bataklıklar, Musul ve Erbil — 4–5 yıldızlı oteller ve özel rehberle iki program, 2.500 dolardan başlayan fiyatlarla.",
   intro="Seçtiğiniz tarihte size ve ailenize özel bir gezi düzenliyoruz; Bağdatlı rehber ve tüm yol boyunca özel araçla. İsterseniz küçük bir gruba da katılabilirsiniz.",
   travel="İstanbul'dan Bağdat, Basra, Erbil ve Necef'e doğrudan uçuşlar var; Bağdat'a uçuş yaklaşık üç saat sürüyor (güncel tarifeleri havayolundan kontrol edin). Irak, Türkiye ile aynı saat dilimindedir (UTC+3). Havalimanında sizi karşılıyor, tüm transferleri biz ayarlıyoruz.",
   hl=[("gilani", "Bağdat'ın türbeleri", "Gavs-ı Azam Abdülkadir Geylani, İmam-ı Azam Ebu Hanife, Kazımiye ve Cüneyd-i Bağdadi."),
       ("qishla", "Osmanlı izleri", "Bağdat'ta Kışla saat kulesi ve Mutanabbi Caddesi, Musul'un eski şehri ve Hadba minaresi."),
       ("babylon", "Babil ve Ur", "İştar Kapısı, Babil Aslanı ve Sümerlerin Ur zigguratı.")]),
 "en": dict(title="Iraq Tours from Turkey: Baghdad, Babylon & Karbala | Fable Tour",
   desc="Iraq tours from Turkey with a Baghdad-based guide: Baghdad, the shrines of Abdul Qadir Gilani and Abu Hanifa, Babylon, Karbala, Najaf and Mosul. 7 or 9 days.",
   kw="Iraq tours from Turkey, Istanbul to Baghdad trip, Baghdad tour, Abdul Qadir Gilani shrine, Abu Hanifa mosque, Babylon tour, Fable Tour",
   h1="Iraq tours from Turkey", lead="The shrines of Abdul Qadir Gilani and Imam Abu Hanifa in Baghdad, Karbala, Najaf and Samarra, Babylon, Ur and the Marshes, Mosul and Erbil — two programmes with 4★–5★ hotels and a private guide, from US$2,500.",
   intro="We arrange a private trip for you and your family on the date you choose, with a guide from Baghdad and a private car throughout — or join a small group.",
   travel="There are direct flights from Istanbul to Baghdad, Basra, Erbil and Najaf; Istanbul–Baghdad takes about three hours (check current airline schedules). Iraq is in the same time zone as Turkey (UTC+3). We meet you at the airport and handle every transfer.",
   hl=[("gilani", "The shrines of Baghdad", "Sheikh Abdul Qadir Gilani, Imam Abu Hanifa, Kadhimiya and Junayd al-Baghdadi."),
       ("qishla", "Ottoman Iraq", "The Qishla clock tower and Mutanabbi Street in Baghdad, Old Mosul and the al-Hadba minaret."),
       ("babylon", "Babylon & Ur", "The Ishtar Gate, the Lion of Babylon and the Sumerian ziggurat of Ur.")])})

# ---------------------------------------------------------------- page building
CSS = """<style id="market-css">
.market-panel{margin:28px 0 8px;padding:0}
.market-panel .sec-head{margin-bottom:18px}
.market-grid{display:grid;gap:16px;grid-template-columns:1fr}
@media(min-width:820px){.market-grid{grid-template-columns:1fr 1fr}}
.market-card{background:var(--paper,#fff);border:1px solid rgba(27,42,71,.12);border-radius:8px;padding:18px 20px}
.market-card h3{margin:0 0 8px;font-size:1.15rem;color:var(--navy,#1B2A47)}
.market-card p,.market-card li{font-size:15px;line-height:1.55;color:rgba(27,42,71,.88)}
.market-hl{display:grid;gap:14px;grid-template-columns:1fr;margin-top:14px}
@media(min-width:720px){.market-hl{grid-template-columns:1fr 1fr 1fr}}
.market-hl .hl{border-radius:8px;overflow:hidden;border:1px solid rgba(27,42,71,.1);background:#fff}
.market-hl .ph{height:140px;background-size:cover;background-position:center}
.market-hl .bd{padding:12px 14px}
.market-hl .bd h3{margin:0 0 6px;font-size:1.05rem}
.market-hl .bd p{margin:0;font-size:14px;line-height:1.45}
</style>"""
BANNER_CSS = """<style id="mkt-banner-css">
.mkt-banner{margin:18px 0 8px;padding:14px 18px;background:linear-gradient(135deg,var(--navy),var(--navy-2,#243a5e));border-radius:8px;color:#fff;display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px}
.mkt-banner p{margin:0;font-size:15px;line-height:1.45}
.mkt-banner a{display:inline-block;background:var(--gold);color:var(--navy);font-weight:600;padding:8px 13px;border-radius:4px;text-decoration:none;white-space:nowrap;font-size:14px}
</style>"""


def home(lang):
    return ROOT / "index.html" if lang == "ar" else ROOT / lang / "index.html"


def page_dir(lang):
    return "/" if lang == "ar" else f"/{lang}/"


def absolutize(s, lang):
    d = page_dir(lang)

    def fix(u):
        if re.match(r"(?:[a-z][a-z0-9+.-]*:|/|#|\$\{|data:)", u) or not u:
            return u
        r = posixpath.normpath(posixpath.join(d, u))
        return r if r.endswith("/") or not u.endswith("/") else r + "/"

    def attr(m):
        return m.group(1) + "|".join(fix(p) for p in m.group(2).split("|")) + '"'
    s = re.sub(r'(\s(?:href|src|data-src|data-full|poster)=")([^"]*)"', attr, s)
    s = re.sub(r"url\('([^']*)'\)", lambda m: "url('" + fix(m.group(1)) + "')", s)
    s = re.sub(r'(HERO_IMG = ")([^"]*)"', lambda m: m.group(1) + fix(m.group(2)) + '"', s)
    s = re.sub(r'location\.href="(?:\.\./)?"\+\(v==="ar"', 'location.href="/"+(v==="ar"', s)  # language menu
    return s


def url(key, lang):
    return f"{BASE}/{'' if lang == 'ar' else lang + '/'}{M[key]['slug']}/"


def panel(key, lang):
    mk, t = M[key], M[key]["texts"][lang]
    c = mk["names"][lang]
    eye, h2, trv, see, _ = [x.format(c=c) for x in UI[lang]]
    vh, vt = VISA[lang]
    hl = "".join(f'<div class="hl"><div class="ph" style="background-image:url(\'/img/{IMG[i]}.webp\')" role="img" aria-label="{esc(h)}"></div>'
                 f'<div class="bd"><h3>{esc(h)}</h3><p>{esc(p)}</p></div></div>' for i, h, p in t["hl"])
    return (f'\n  <section class="block in market-panel" id="for-{key}" aria-labelledby="mkt-h">\n'
            f'    <div class="sec-head"><span class="eyebrow">{esc(eye)}</span><h2 class="disp" id="mkt-h">{esc(h2)}</h2><p>{esc(t["intro"])}</p></div>\n'
            f'    <div class="market-grid">\n'
            f'      <div class="market-card" id="getting-there"><h3>{esc(trv)}</h3><p>{esc(t["travel"])}</p></div>\n'
            f'      <div class="market-card" id="visa"><h3>{esc(vh)}</h3><p>{esc(vt)}</p></div>\n'
            f'    </div>\n'
            f'    <div class="market-card" style="margin-top:16px" id="highlights"><h3>{esc(see)}</h3><div class="market-hl">{hl}</div></div>\n'
            f'  </section>\n')


def build(key, lang):
    mk, t = M[key], M[key]["texts"][lang]
    s = home(lang).read_text()
    s = absolutize(s, lang)
    u = url(key, lang)
    pair = [(mk["local"], url(key, mk["local"])), ("en", url(key, "en"))]
    hl = lambda l: "zh-Hans" if l == "zh" else l
    alts = "".join(f'<link rel="alternate" hreflang="{hl(l)}" href="{x}">\n' for l, x in pair) + f'<link rel="alternate" hreflang="x-default" href="{url(key, "en")}">\n'
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", s)
    s = re.sub(r'<link rel="canonical" href="[^"]*">\n?', f'<link rel="canonical" href="{u}">\n' + alts, s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(t['title'])}</title>", s, count=1, flags=re.S)
    for p in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {p} content=")[^"]*"', lambda m: m.group(1) + esc(t["desc"]) + '"', s)
    for p in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {p} content=")[^"]*"', lambda m: m.group(1) + esc(t["title"]) + '"', s)
    s = re.sub(r'(<meta name="keywords" content=")[^"]*"', lambda m: m.group(1) + esc(t["kw"]) + '"', s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*"', lambda m: m.group(1) + u + '"', s)
    # hero
    eye = UI[lang][0].format(c=mk["names"][lang])
    s = re.sub(r'(<span class="eyebrow" data-i="eyebrow">).*?(</span>)', lambda m: m.group(1) + esc(eye) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<h1 class="disp" data-i="h1">).*?(</h1>)', lambda m: m.group(1) + esc(t["h1"]) + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p data-i="lead">).*?(</p>)', lambda m: m.group(1) + esc(t["lead"]) + m.group(2), s, count=1, flags=re.S)
    # the page's JS re-renders the title and data-i texts from its table T: put the landing texts there
    k = s.index("const T = ")
    head, tail = s[:k], s[k:]
    for key_, val in (("title", t["title"]), ("eyebrow", eye), ("h1", t["h1"]), ("lead", t["lead"])):
        tail = re.sub(r'("%s": )"(?:\\.|[^"\\])*"' % key_, lambda m: m.group(1) + json.dumps(val, ensure_ascii=False), tail, count=1)
    s = head + tail
    # remove other market banners / panels copied from the homepage
    s = re.sub(r'\s*<div class="(?:mkt|[a-z]+)-banner">.*?</div>', "", s, flags=re.S)
    s = re.sub(r'\s*<section class="block in market-panel".*?</section>\n?', "\n", s, flags=re.S)
    # market panel right after the hero section
    hero_end = s.index("</section>", s.index('data-i="h1"')) + len("</section>")
    s = s[:hero_end] + panel(key, lang) + s[hero_end:]
    if 'id="market-css"' not in s:
        s = s.replace("</head>", CSS + "\n</head>", 1)
    # JSON-LD: WebPage node + breadcrumb
    def ld(m):
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        for n in data.get("@graph", [data]):
            if n.get("@type") == "WebPage":
                n.update({"@id": u + "#webpage", "url": u, "name": t["title"], "description": t["desc"], "inLanguage": lang})
                n.pop("breadcrumb", None)
            if n.get("@type") == "BreadcrumbList":
                n["@id"] = u + "#breadcrumb"
                items = n.get("itemListElement", [])[:1]
                items.append({"@type": "ListItem", "position": len(items) + 1, "name": t["h1"], "item": u})
                n["itemListElement"] = items
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)
    out = ROOT / ("" if lang == "ar" else lang) / mk["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    return u


BANNER = {
 "ar": ("من الخليج والعالم العربي؟ صفحات خاصة لبلدك:", ["kuwait", "bahrain", "oman", "uae", "lebanon", "jordan"]),
 "th": ("เดินทางจากประเทศไทย? ข้อมูลเที่ยวบินและวีซ่า", ["thailand"]),
 "ur": ("پاکستان سے زیارت؟ پروازیں، ویزا اور زیارات", ["pakistan"]),
 "fa": ("از ایران سفر می‌کنید؟ پرواز، ویزا و زیارت", ["iran"]),
 "tr": ("Türkiye'den mi geliyorsunuz? Uçuşlar, vize ve ziyaretler", ["turkey"]),
}


def banners():
    for lang, (txt, keys) in BANNER.items():
        f = home(lang)
        s = f.read_text()
        s = re.sub(r'\s*<div class="mkt-banner">.*?</div>', "", s, flags=re.S)
        links = "".join(f'<a href="{page_dir(lang)}{M[k]["slug"]}/">{esc(M[k]["names"][lang])} →</a>' for k in keys)
        b = f'\n        <div class="mkt-banner"><p>{esc(txt)}</p>{links}</div>'
        i = s.index('<p data-i="intro2">')
        j = s.index("</div>", i) + len("</div>")
        s = s[:j] + b + s[j:]
        if 'id="mkt-banner-css"' not in s:
            s = s.replace("</head>", BANNER_CSS + "\n</head>", 1)
        f.write_text(s)


def sitemap(urls):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text()
    add = ""
    for u, pair in urls:
        s = re.sub(r"  <url>\n    <loc>" + re.escape(u) + r"</loc>.*?</url>\n", "", s, flags=re.S)
        links = "".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{x}"/>\n' for l, x in pair)
        add += (f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n"
                f"    <priority>0.8</priority>\n{links}  </url>\n")
    s = s.replace("</urlset>", add + "</urlset>")
    sm.write_text(s)


def run():
    urls = []
    for key, mk in M.items():
        pair = [(mk["local"], url(key, mk["local"])), ("en", url(key, "en")), ("x-default", url(key, "en"))]
        for lang in (mk["local"], "en"):
            urls.append((build(key, lang), pair))
    banners()
    sitemap(urls)
    print("built", len(urls), "pages")


if __name__ == "__main__":
    run()
