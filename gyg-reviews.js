/* Fable Tour – verified GetYourGuide reviews slider.
   Reviews are copied word for word from the Fable Tour supplier account on
   GetYourGuide (only reviews with text). To add a new one, add an object to R. */
(function () {
  "use strict";
  var GYG = "https://www.getyourguide.com/fable-tour-in-iraq-s471675/";
  var R = [
    /* Chinese-page only (only: ["zh"]), pinned first there (pin: 1) */
    { n: "Ting", c: "United States", d: "2026-11-05", s: 5, t: "From Baghdad: Babylon Walking Tour", u: "https://gyg.me/BHeinxB8", lang: "zh", only: ["zh"], pin: 1,
      x: "非常愉快且难忘的巴比伦之旅！司机非常专业、知识丰富，对当地历史文化十分了解，而且行程安排灵活，能够根据实际情况及时调整，让整个旅程轻松又充实。虽然今天巴比伦部分景点没有开放，但司机非常热情周到，主动请我享用当地特色午餐，还特意安排了我一直想尝试的伊拉克传统烤鱼 Masgouf，非常美味！ 由于下午还有空余时间，司机又贴心地提议增加卡尔巴拉（Karbala）的参观行程，只收取了非常合理的少量额外费用，让我有机会进一步体验伊拉克独特的历史与文化。 非常感谢司机的热情、专业和灵活安排，让原本可能留下遗憾的一天变成了丰富而难忘的旅行体验。强烈推荐！" },
    { n: "Pavel", c: "Romania", d: "2026-10-05", s: 5, t: "Baghdad: Kadhimiya Sunrise Tour & Airport Pickup & Breakfast", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-kadhimiya-sunrise-tour-airport-pickup-breakfast-t1471096/", lang: "ru",
      x: "Супер профессиональный гид. Все было на высоте . Рекомендую",
      en: "A super professional guide. Everything was top-notch. I recommend it." },
    { n: "Harry", c: "United Kingdom", d: "2026-10-04", s: 4, t: "Baghdad: Old Town Guided Walking Tour with Drinks", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-old-town-guided-walking-tour-with-drinks-t1477870/",
      x: "Very good! Highly recommend this tour to old town in the evening and enjoy some drinks! Tour guide great English, knowledgeable and friendly!" },
    { n: "Erik", c: "Netherlands", d: "2026-09-30", s: 5, t: "From Baghdad to the Shrines of Ezekiel & Prophet Job", u: "https://gyg.me/0Ag0lnve", lang: "nl",
      x: "Dankzij Saif een fantastische maar vooral ook heel indrukwekkende tour gehad. Die begon al met een mooie reis zuidwaarts door Irak. Na een hartelijke ontvangst bij de heiligdommen van Ezekiel en Ayyub werd de indrukwekkende en heel bijzondere achtergrond en historie verteld. Deze tour is beslist een aanrader.",
      en: "Thanks to Saif we had a fantastic and above all very impressive tour. It began with a beautiful drive south through Iraq. After a warm welcome at the shrines of Ezekiel and Ayyub (Job), the impressive and very special background and history were explained. This tour is definitely recommended." },
    { n: "Joe", c: "Estonia", d: "2026-09-03", s: 5, t: "From Baghdad: Karbala Holy Shrines Guided Day Trip", u: "https://www.getyourguide.com/baghdad-l152664/from-baghdad-karbala-holy-shrines-guided-day-trip-t1448656/",
      x: "Awesome trip to Karbala, best trip during my time in Iraq. Comfortable car, flexible itinerary and a very knowledgable and dedicated guide. Karbala itself is mindblowing and a must see" },
    { n: "Zach", c: "United Kingdom", d: "2026-08-25", s: 5, t: "From Baghdad: 4-Day Kurdistan Highlands Private Tour", u: "https://www.getyourguide.com/dohuk-l1108/from-baghdad-4-day-kurdistan-highlands-private-tour-t1417341/",
      x: "beautiful city and nice people and highly recommended to visit Dohuk. tour guide knows a lot about places history" },
    { n: "GetYourGuide traveler", c: "United Kingdom", d: "2026-08-23", s: 5, t: "From Baghdad: Babylon Walking Tour", u: "https://gyg.me/BHeinxB8",
      x: "highly recommended. the tour guide have deep knowledge about Babylonian history and i will book another tours with him for another historical sites in iraq ." },
    { n: "GetYourGuide traveler", c: "United Kingdom", d: "2026-08-19", s: 5, t: "Two-day tour: Kufa, Najaf & Karbala", u: "https://gyg.me/eAIpconO",
      x: "Fluent in English, Russian and Arabic. Excellent service always flexible to meet the customers needs. Highly recommend" },
    { n: "Robert", c: "Germany", d: "2026-02-02", s: 5, t: "Baghdad: Full-Day Cultural Tour with Lunch", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-full-day-cultural-tour-with-lunch-t861019/", lang: "de",
      x: "Das ist eine wundervolle Tour! Sie ist umfangreich, informativ und kurzweilig. Unser Guid Saif bringt viel Detailwissen mit und ist ein angenehmer Gastgeber. Alls verlief reibungslos, ohne Komplikationen und einfach, da er fließend Englisch und Russisch spricht. Wir können diese Tour sehr empfehlen und würden sie wieder buchen.",
      en: "This is a wonderful tour! It is comprehensive, informative and entertaining. Our guide Saif brings a lot of detailed knowledge and is a pleasant host. Everything went smoothly, without complications and easily, as he speaks fluent English and Russian. We highly recommend this tour and would book it again." },
    { n: "Michael", c: "Switzerland", d: "2026-01-19", s: 5, t: "Baghdad: Baghdadi Museum Guided Tour", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-baghdadi-museum-guided-tour-t986948/",
      x: "As a Swiss couple visiting Iraq for the first time, our visit to the Baghdadi Museum was one of the most memorable cultural experiences of our journey. The museum offers a vivid and authentic portrayal of traditional Baghdadi life, with lifelike scenes showing daily customs, crafts, music, family life, and social traditions that once defined the city." },
    { n: "Alessandro", c: "Italy", d: "2026-01-07", s: 5, t: "Baghdad: National Museum of Iraq Guided Tour", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-national-museum-of-iraq-guided-tour-t860924/",
      x: "Saif is attentive, well-organized, and genuinely passionate about sharing Iraq’s rich heritage. I highly recommend him to anyone looking for an authentic and enriching experience in Iraq. Although my first trip to Iraq lasted only a few days, it left a strong impression on me. On my next visit, I plan to stay for 15 days—and without hesitation, I will book the entire tour with Saif again." },
    { n: "Rana", c: "United States", d: "2025-12-24", s: 5, t: "Baghdad: Mustansiriyah Madrasah & Al-Baghdadi Museum Tour", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-mustansiriyah-madrasah-al-baghdadi-museum-tour-t1110000/",
      x: "My recent private tour through Old Town Baghdad, Al-Mutanabbi Street, the Baghdadi Museum, and Al-Mustansiriya School was nothing short of exceptional. This was not a standard sightseeing tour—it was a refined cultural journey designed with precision, depth, and elegance. From walking through the historic alleys of Old Baghdad to feeling the intellectual soul of Mutanabbi Street, every moment was curated with insight and respect for history. The Iraq Museum was presented with remarkable storytelling, transforming ancient artifacts into a living narrative of Mesopotamian civilization. Visiting the Mustansiriya School was a powerful reminder that Baghdad once stood at the heart of global knowledge and scholarship. The level of professionalism, discretion, and personalized attention reflected true luxury service. I felt completely safe, deeply informed, and genuinely welcomed." },
    { n: "Haroon", c: "United Kingdom", d: "2025-06-27", s: 5, t: "Baghdad: Full-Day Cultural Tour with Lunch", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-full-day-cultural-tour-with-lunch-t861019/",
      x: "I thought I was just visiting a city — I didn’t expect to fall in love. Al-Mutanabbi Street was alive with poetry, books, and an energy I can’t describe. With every step, I felt Baghdad whispering her secrets. At the Mustansiriya School, I stood in awe — centuries of beauty and knowledge carved into every detail. But it was the Baghdadi Museum that surprised me most. It wasn’t about ancient ruins — it was about people. Weddings, traditions, laughter in the public baths… It felt like walking through Baghdad’s memory. And in Souk Al-Safarin, time slowed. I found myself touching handmade treasures I didn’t know I needed. It wasn’t a tour. It was an experience I didn’t know my soul was craving." },
    { n: "Ewa", c: "Poland", d: "2025-04-22", s: 5, t: "7-Day Iraq Heritage Tour includes Babylon, Uruk & Hatra", u: "https://www.getyourguide.com/baghdad-l152664/iraq-10-day-guided-tour-with-accommodation-and-meals-t860866/",
      x: "I came to Iraq looking for history. What I found was so much more: soul, beauty, kindness, and a sense of connection I didn`t know I was missing. Every single day of this 10-day journey was filled with moments I`ll never forget. And all of it - every smile, every sacred site, every incredible meal - was made possible thanks to our amazing guide, whose warmth and deep knowledge made us feel like we weren`t just tourists - we were family. We visited sacred shrines in Baghdad, Karbala and Najaf. In Samarra we saw architectural marvels: iconic spiral minaret, the Grand Mosque and the Abu Dulaf Mosque. On our way there were also: legendary city of Uruk, ancient ruins of Babylon and Borsippa, magnificent Zigurrat of Ur, the must-see Iraqi National Museum in Baghdad. We explored the Al-Chibayish Marshes and colourful markets. The food was absolutely delicious. This fantastic tour was perfectly organised (very good hotels, meals, comfortable transport, entrance tickets) by our local guide." },
    { n: "David", c: "United Arab Emirates", d: "2024-12-26", s: 5, t: "Baghdad: National Museum of Iraq Guided Tour", u: "https://www.getyourguide.com/baghdad-l152664/baghdad-national-museum-of-iraq-guided-tour-t860924/",
      x: "The museum has a broad and rich collection of archaeological treasures and it’s definitely a must. I would have loved to receive more history information about the museums but there were no audio guides available. The 1.5h tour is recommended for those interested in knowing more about Iraqi culture and history." }
  ];

  R.sort(function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : 0; }); /* oldest first */
  var LANGS = ["zh-tw","cs","da","de","el","en","es","fa","fi","fr","hi","hr","id","it","ja","ka","ko","ms","nl","no","pl","pt","ro","ru","sk","sv","ta","th","tr","ur","zh","ckb","vi"];
  var PH = document.getElementById("gyg-reviews-here");
  var seg = (location.pathname.split("/")[1] || "").toLowerCase();
  var LG = PH ? ((PH.getAttribute("data-lang") || document.documentElement.lang || "en").toLowerCase().replace(/^(zh-tw|ckb|[a-z]{2}).*$/, "$1")) : (LANGS.indexOf(seg) >= 0 ? seg : "ar");
  /* page-only reviews; on the Chinese page: pinned first, then newest to oldest */
  R = R.filter(function (r) { return !r.only || r.only.indexOf(LG) >= 0; });
  if (LG === "zh") R.sort(function (a, b) { return ((b.pin || 0) - (a.pin || 0)) || (a.d < b.d ? 1 : a.d > b.d ? -1 : 0); });
  var UI = {
    ar: ["آراء المسافرين", "تقييمات موثّقة على GetYourGuide", "حجز موثّق على GetYourGuide", "عرض الترجمة", "النص الأصلي", "كل التقييمات على GetYourGuide", "السابق", "التالي", "مرّر للأسفل لقراءة المزيد"],
    ckb: ["ڕای گەشتیاران", "هەڵسەنگاندنی پشتڕاستکراوە لە GetYourGuide", "حیجزی پشتڕاستکراوە لە GetYourGuide", "وەرگێڕان پیشان بدە", "دەقی ڕەسەن", "هەموو هەڵسەنگاندنەکان لە GetYourGuide", "پێشوو", "دواتر", "بۆ خوێندنەوەی زیاتر بەرەو خوارەوە بڕۆ"],
    en: ["Traveller reviews", "Verified reviews on GetYourGuide", "Verified booking on GetYourGuide", "Show translation", "Show original", "All reviews on GetYourGuide", "Previous", "Next", "Scroll to read more"],
    ru: ["Отзывы путешественников", "Проверенные отзывы на GetYourGuide", "Подтверждённое бронирование на GetYourGuide", "Показать перевод", "Оригинал", "Все отзывы на GetYourGuide", "Назад", "Вперёд", "Прокрутите, чтобы читать дальше"],
    de: ["Bewertungen von Reisenden", "Verifizierte Bewertungen auf GetYourGuide", "Verifizierte Buchung auf GetYourGuide", "Übersetzung anzeigen", "Original anzeigen", "Alle Bewertungen auf GetYourGuide", "Zurück", "Weiter", "Scrollen zum Weiterlesen"],
    fr: ["Avis des voyageurs", "Avis vérifiés sur GetYourGuide", "Réservation vérifiée sur GetYourGuide", "Voir la traduction", "Voir l'original", "Tous les avis sur GetYourGuide", "Précédent", "Suivant", "Faites défiler pour lire la suite"],
    es: ["Opiniones de viajeros", "Opiniones verificadas en GetYourGuide", "Reserva verificada en GetYourGuide", "Ver traducción", "Ver original", "Todas las opiniones en GetYourGuide", "Anterior", "Siguiente", "Desliza para leer más"],
    it: ["Recensioni dei viaggiatori", "Recensioni verificate su GetYourGuide", "Prenotazione verificata su GetYourGuide", "Mostra traduzione", "Mostra originale", "Tutte le recensioni su GetYourGuide", "Precedente", "Successivo", "Scorri per leggere tutto"],
    tr: ["Gezgin yorumları", "GetYourGuide'da doğrulanmış yorumlar", "GetYourGuide'da doğrulanmış rezervasyon", "Çeviriyi göster", "Orijinali göster", "GetYourGuide'daki tüm yorumlar", "Önceki", "Sonraki", "Devamı için kaydırın"],
    fa: ["نظرات مسافران", "نظرات تأییدشده در GetYourGuide", "رزرو تأییدشده در GetYourGuide", "نمایش ترجمه", "متن اصلی", "همه نظرات در GetYourGuide", "قبلی", "بعدی", "برای خواندن ادامه اسکرول کنید"],
    pl: ["Opinie podróżnych", "Zweryfikowane opinie na GetYourGuide", "Zweryfikowana rezerwacja na GetYourGuide", "Pokaż tłumaczenie", "Pokaż oryginał", "Wszystkie opinie na GetYourGuide", "Poprzednia", "Następna", "Przewiń, aby czytać dalej"],
    nl: ["Reviews van reizigers", "Geverifieerde reviews op GetYourGuide", "Geverifieerde boeking op GetYourGuide", "Vertaling tonen", "Origineel tonen", "Alle reviews op GetYourGuide", "Vorige", "Volgende", "Scroll om verder te lezen"],
    pt: ["Avaliações de viajantes", "Avaliações verificadas no GetYourGuide", "Reserva verificada no GetYourGuide", "Ver tradução", "Ver original", "Todas as avaliações no GetYourGuide", "Anterior", "Seguinte", "Deslize para ler mais"],
    cs: ["Recenze cestovatelů", "Ověřené recenze na GetYourGuide", "Ověřená rezervace na GetYourGuide", "Zobrazit překlad", "Zobrazit originál", "Všechny recenze na GetYourGuide", "Předchozí", "Další", "Posuňte pro další text"],
    sk: ["Recenzie cestovateľov", "Overené recenzie na GetYourGuide", "Overená rezervácia na GetYourGuide", "Zobraziť preklad", "Zobraziť originál", "Všetky recenzie na GetYourGuide", "Predchádzajúca", "Ďalšia", "Posuňte pre ďalší text"],
    hr: ["Recenzije putnika", "Provjerene recenzije na GetYourGuide", "Provjerena rezervacija na GetYourGuide", "Prikaži prijevod", "Prikaži izvornik", "Sve recenzije na GetYourGuide", "Prethodna", "Sljedeća", "Pomaknite za nastavak"],
    ro: ["Recenziile călătorilor", "Recenzii verificate pe GetYourGuide", "Rezervare verificată pe GetYourGuide", "Vezi traducerea", "Vezi originalul", "Toate recenziile pe GetYourGuide", "Anterior", "Următor", "Derulați pentru a citi mai mult"],
    el: ["Κριτικές ταξιδιωτών", "Επαληθευμένες κριτικές στο GetYourGuide", "Επαληθευμένη κράτηση στο GetYourGuide", "Εμφάνιση μετάφρασης", "Εμφάνιση πρωτοτύπου", "Όλες οι κριτικές στο GetYourGuide", "Προηγούμενη", "Επόμενη", "Κάντε κύλιση για περισσότερα"],
    sv: ["Resenärers omdömen", "Verifierade omdömen på GetYourGuide", "Verifierad bokning på GetYourGuide", "Visa översättning", "Visa original", "Alla omdömen på GetYourGuide", "Föregående", "Nästa", "Scrolla för att läsa mer"],
    da: ["Rejsendes anmeldelser", "Verificerede anmeldelser på GetYourGuide", "Verificeret booking på GetYourGuide", "Vis oversættelse", "Vis original", "Alle anmeldelser på GetYourGuide", "Forrige", "Næste", "Rul for at læse mere"],
    no: ["Reisendes omtaler", "Verifiserte omtaler på GetYourGuide", "Verifisert bestilling på GetYourGuide", "Vis oversettelse", "Vis original", "Alle omtaler på GetYourGuide", "Forrige", "Neste", "Rull for å lese mer"],
    fi: ["Matkailijoiden arviot", "Vahvistetut arviot GetYourGuidessa", "Vahvistettu varaus GetYourGuidessa", "Näytä käännös", "Näytä alkuperäinen", "Kaikki arviot GetYourGuidessa", "Edellinen", "Seuraava", "Vieritä lukeaksesi lisää"],
    ka: ["მოგზაურების შეფასებები", "დადასტურებული შეფასებები GetYourGuide-ზე", "დადასტურებული ჯავშანი GetYourGuide-ზე", "თარგმანის ჩვენება", "ორიგინალის ჩვენება", "ყველა შეფასება GetYourGuide-ზე", "წინა", "შემდეგი", "გადაახვიეთ მეტის წასაკითხად"],
    ko: ["여행자 후기", "GetYourGuide 인증 후기", "GetYourGuide 인증 예약", "번역 보기", "원문 보기", "GetYourGuide의 모든 후기", "이전", "다음", "스크롤하여 더 읽기"],
    ja: ["旅行者の口コミ", "GetYourGuideの認証済み口コミ", "GetYourGuideで認証済みの予約", "翻訳を表示", "原文を表示", "GetYourGuideのすべての口コミ", "前へ", "次へ", "スクロールして続きを読む"],
    zh: ["旅行者评价", "GetYourGuide 认证评价", "GetYourGuide 认证预订", "显示翻译", "显示原文", "GetYourGuide 上的全部评价", "上一个", "下一个", "向下滚动阅读更多"],
    "zh-tw": ["旅客評價", "GetYourGuide 認證評價", "GetYourGuide 認證預訂", "顯示翻譯", "顯示原文", "GetYourGuide 上的所有評價", "上一則", "下一則", "向下捲動閱讀更多"],
    hi: ["यात्रियों की समीक्षाएँ", "GetYourGuide पर सत्यापित समीक्षाएँ", "GetYourGuide पर सत्यापित बुकिंग", "अनुवाद दिखाएँ", "मूल दिखाएँ", "GetYourGuide पर सभी समीक्षाएँ", "पिछला", "अगला", "और पढ़ने के लिए स्क्रॉल करें"],
    ta: ["பயணிகளின் மதிப்புரைகள்", "GetYourGuide சரிபார்க்கப்பட்ட மதிப்புரைகள்", "GetYourGuide சரிபார்க்கப்பட்ட முன்பதிவு", "மொழிபெயர்ப்பைக் காட்டு", "மூலத்தைக் காட்டு", "GetYourGuide இல் அனைத்து மதிப்புரைகளும்", "முந்தையது", "அடுத்தது", "மேலும் படிக்க உருட்டவும்"],
    th: ["รีวิวจากนักเดินทาง", "รีวิวที่ยืนยันแล้วบน GetYourGuide", "การจองที่ยืนยันแล้วบน GetYourGuide", "แสดงคำแปล", "แสดงต้นฉบับ", "รีวิวทั้งหมดบน GetYourGuide", "ก่อนหน้า", "ถัดไป", "เลื่อนเพื่ออ่านต่อ"],
    ms: ["Ulasan pengembara", "Ulasan disahkan di GetYourGuide", "Tempahan disahkan di GetYourGuide", "Tunjuk terjemahan", "Tunjuk asal", "Semua ulasan di GetYourGuide", "Sebelumnya", "Seterusnya", "Tatal untuk membaca lagi"],
    vi: ["Đánh giá của du khách", "Đánh giá đã xác minh trên GetYourGuide", "Đặt tour đã xác minh trên GetYourGuide", "Xem bản dịch", "Xem bản gốc", "Tất cả đánh giá trên GetYourGuide", "Trước", "Tiếp", "Cuộn xuống để đọc tiếp"],
    id: ["Ulasan wisatawan", "Ulasan terverifikasi di GetYourGuide", "Pemesanan terverifikasi di GetYourGuide", "Tampilkan terjemahan", "Tampilkan asli", "Semua ulasan di GetYourGuide", "Sebelumnya", "Berikutnya", "Gulir untuk membaca lagi"],
    ur: ["مسافروں کے تبصرے", "GetYourGuide پر تصدیق شدہ تبصرے", "GetYourGuide پر تصدیق شدہ بکنگ", "ترجمہ دیکھیں", "اصل متن", "GetYourGuide پر تمام تبصرے", "پچھلا", "اگلا", "مزید پڑھنے کے لیے اسکرول کریں"]
  };
  var U = UI[LG] || UI.en;
  var RTL = document.documentElement.dir === "rtl";
  var LOC = LG === "zh-tw" ? "zh-TW" : LG === "ar" ? "ar-IQ-u-nu-latn" : LG;

  function el(tag, cls, t) { var e = document.createElement(tag); if (cls) e.className = cls; if (t != null) e.textContent = t; return e; }
  function date(s) { try { return new Intl.DateTimeFormat(LOC, { year: "numeric", month: "long" }).format(new Date(s + "T12:00:00")); } catch (e) { return s; } }
  var AV = ["#2A3D63", "#B8955A", "#4F7CAC", "#7A9E7E", "#C26B5A", "#1B2A47"];

  var css = ".gr{padding-top:0}" +
    ".gr-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}" +
    ".gr-head h2{margin:4px 0 0}.gr-head p{margin:6px 0 0;color:var(--muted,#5b6475);font-size:15px}" +
    ".gr-nav{display:flex;gap:8px}.gr-nav button{width:44px;height:44px;border-radius:50%;border:1px solid var(--gold,#B8955A);background:#fff;color:var(--navy,#1B2A47);cursor:pointer;display:grid;place-items:center}" +
    ".gr-nav button:hover{background:var(--gold,#B8955A)}[dir=rtl] .gr-nav svg{transform:scaleX(-1)}" +
    ".gr-track{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding:4px 2px 14px;scrollbar-width:none;overscroll-behavior-x:contain}" +
    ".gr-track::-webkit-scrollbar{display:none}" +
    ".gr-c{flex:0 0 calc((100% - 36px)/3);scroll-snap-align:start;background:#fff;border:1px solid var(--line,rgba(27,42,71,.12));border-top:4px solid var(--gold,#B8955A);border-radius:8px;padding:20px 20px 16px;display:flex;flex-direction:column;gap:12px;box-shadow:0 8px 24px -18px rgba(27,42,71,.5);min-width:0}" +
    ".gr-top{display:flex;align-items:center;justify-content:space-between;gap:10px}" +
    ".gr-st{color:#E3A92B;font-size:19px;letter-spacing:2px;line-height:1}.gr-st i{color:#D5D9E0;font-style:normal}" +
    ".gr-dt{font-size:12.5px;color:var(--muted,#5b6475);white-space:nowrap}" +
    ".gr-who{display:flex;align-items:center;gap:10px}.gr-av{width:38px;height:38px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:700;font-size:16px;flex:none}" +
    ".gr-who b{display:block;color:var(--navy,#1B2A47);font-size:15px;line-height:1.3}.gr-who small{color:var(--muted,#5b6475);font-size:13px}" +
    ".gr-tx{margin:0;font-size:15px;line-height:1.65;color:var(--ink,#1F2733);max-height:11.6em;overflow:auto;padding-inline-end:4px;unicode-bidi:plaintext;text-align:start}" +
    ".gr-tx::before{content:'\\201C';font-family:Georgia,serif;color:var(--gold,#B8955A);font-size:30px;line-height:0;vertical-align:-10px;margin-inline-end:3px}" +
    ".gr-tx{scrollbar-width:thin;scrollbar-color:var(--gold,#B8955A) #EEE7DA;padding-inline-end:10px}" +
    ".gr-tx::-webkit-scrollbar{width:6px;-webkit-appearance:none}.gr-tx::-webkit-scrollbar-track{background:#EEE7DA;border-radius:3px}.gr-tx::-webkit-scrollbar-thumb{background:var(--gold,#B8955A);border-radius:3px}" +
    ".gr-txw{position:relative}.gr-txw.more::after{content:\"\";position:absolute;left:0;right:12px;bottom:0;height:46px;background:linear-gradient(rgba(255,255,255,0),#fff);pointer-events:none}" +
    ".gr-more{display:none;align-self:center;font-size:12.5px;font-weight:700;color:var(--gold,#B8955A);gap:4px;align-items:center;margin-top:-4px}.gr-more.on{display:inline-flex;animation:grb 1.6s ease-in-out infinite}@keyframes grb{0%,100%{transform:translateY(0)}50%{transform:translateY(3px)}}" +
    ".gr-tr{align-self:flex-start;background:none;border:0;padding:0;color:var(--navy-2,#2A3D63);font:inherit;font-size:13px;font-weight:700;cursor:pointer;text-decoration:underline}" +
    ".gr-ft{margin-top:auto;padding-top:10px;border-top:1px solid var(--line,rgba(27,42,71,.1));display:flex;flex-direction:column;gap:3px}" +
    ".gr-tour{font-size:13px;font-weight:700;color:var(--navy,#1B2A47);text-decoration:underline;text-decoration-color:var(--gold,#B8955A);text-underline-offset:3px}.gr-tour:hover{color:var(--gold,#B8955A)}" +
    ".gr-ver{font-size:12px;color:#2E7D4F;display:flex;align-items:center;gap:5px}" +
    ".gr-dots{display:flex;justify-content:center;gap:7px;margin-top:4px}.gr-dots button{width:9px;height:9px;border-radius:50%;border:0;padding:0;background:#D5D9E0;cursor:pointer}.gr-dots button.on{background:var(--gold,#B8955A);width:22px;border-radius:5px}" +
    ".gr-all{display:inline-block;margin-top:14px;color:var(--navy,#1B2A47);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:2px solid var(--gold,#B8955A);padding-bottom:2px}" +
    ".gr-ext{padding:36px 0 28px}.gr-ext .eyebrow{display:block;font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold,#B8955A);font-weight:600}.gr-ext h2{margin:4px 0 0;font-size:clamp(24px,3vw,32px);line-height:1.25;color:var(--navy,#1B2A47);font-weight:500}" +
    "@media (max-width:900px){.gr-c{flex-basis:calc((100% - 18px)/2)}}" +
    "@media (max-width:600px){.gr-c{flex-basis:88%}.gr-nav{display:none}}";

  var CHK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var ARR = function (d) { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + (d < 0 ? "M15 5l-7 7 7 7" : "M9 5l7 7-7 7") + '"/></svg>'; };

  function build() {
    var anchor = PH || document.getElementById("video-journeys") || document.getElementById("gallery") || document.getElementById("faq");
    if (!anchor || document.getElementById("gyg-reviews")) return;
    var st = el("style"); st.textContent = css; document.head.appendChild(st);
    var sec = el("section", "block in gr" + (PH ? " gr-ext" : "")); sec.id = "gyg-reviews"; sec.setAttribute("aria-label", U[0]);
    var head = el("div", "gr-head"), hl = el("div");
    hl.appendChild(el("span", "eyebrow", "GetYourGuide"));
    hl.appendChild(el("h2", "disp", U[0]));
    hl.appendChild(el("p", null, U[1]));
    var nav = el("div", "gr-nav");
    var prev = el("button"); prev.type = "button"; prev.innerHTML = ARR(-1); prev.setAttribute("aria-label", U[6]);
    var next = el("button"); next.type = "button"; next.innerHTML = ARR(1); next.setAttribute("aria-label", U[7]);
    nav.appendChild(prev); nav.appendChild(next);
    head.appendChild(hl); head.appendChild(nav); sec.appendChild(head);

    var track = el("div", "gr-track"); track.setAttribute("tabindex", "0");
    R.forEach(function (r, i) {
      var c = el("article", "gr-c");
      var top = el("div", "gr-top");
      var stars = el("span", "gr-st"); stars.setAttribute("aria-label", r.s + "/5");
      stars.innerHTML = "★★★★★".slice(0, r.s) + "<i>" + "★★★★★".slice(0, 5 - r.s) + "</i>";
      top.appendChild(stars); top.appendChild(el("span", "gr-dt", date(r.d))); c.appendChild(top);
      var who = el("div", "gr-who"), av = el("span", "gr-av", r.n.charAt(0)); av.style.background = AV[i % AV.length];
      var wd = el("div"); wd.appendChild(el("b", null, r.n)); if (r.c) wd.appendChild(el("small", null, r.c));
      who.appendChild(av); who.appendChild(wd); c.appendChild(who);
      var p = el("p", "gr-tx", r.x); if (r.lang) p.lang = r.lang; else p.lang = "en";
      var w = el("div", "gr-txw"); w.appendChild(p); c.appendChild(w);
      var mh = el("span", "gr-more", "↓ " + U[8]); c.appendChild(mh);
      (function (p, w, mh) {
        function chk() { var over = p.scrollHeight - p.clientHeight > 4, end = p.scrollTop + p.clientHeight >= p.scrollHeight - 4;
          w.classList.toggle("more", over && !end); mh.classList.toggle("on", over && p.scrollTop < 8); }
        p.addEventListener("scroll", chk, { passive: true }); setTimeout(chk, 50); window.addEventListener("resize", chk); p._chk = chk;
      })(p, w, mh);
      var ol = r.lang || "en", tr = LG === ol ? null : (LG === "en" ? r.en : (T[r.d] || null)), tl2 = tr ? LG : "en";
      if (!tr && LG !== ol && r.en && ol !== "en") tr = r.en; /* no page-language text yet: offer English */
      if (tr) {
        var dflt = tl2 === LG; /* translation in page language is shown by default */
        var b = el("button", "gr-tr"); b.type = "button"; var shown = dflt;
        var paint = function () { p.textContent = shown ? tr : r.x; p.lang = shown ? tl2 : ol; b.textContent = shown ? U[4] : U[3]; p.scrollTop = 0; p._chk && p._chk(); };
        b.addEventListener("click", function () { shown = !shown; paint(); });
        paint(); c.appendChild(b);
      }
      var ft = el("div", "gr-ft"), tl = el("a", "gr-tour", r.t + " ↗"); tl.href = r.u || GYG; tl.target = "_blank"; tl.rel = "noopener"; ft.appendChild(tl);
      var v = el("span", "gr-ver"); v.innerHTML = CHK; v.appendChild(document.createTextNode(U[2])); ft.appendChild(v);
      c.appendChild(ft); track.appendChild(c);
    });
    sec.appendChild(track);
    var dots = el("div", "gr-dots"); sec.appendChild(dots);
    if (PH) PH.parentNode.replaceChild(sec, PH); else anchor.parentNode.insertBefore(sec, anchor);

    /* slider logic */
    var cards = track.children;
    function per() { var c = cards[0]; return c ? Math.max(1, Math.round(track.clientWidth / (c.getBoundingClientRect().width + 18))) : 1; }
    function pages() { return Math.max(1, Math.ceil(cards.length / per())); }
    function cur() { var w = cards[0].getBoundingClientRect().width + 18; return Math.round(Math.abs(track.scrollLeft) / (w * per())); }
    function go(pg) {
      var n = pages(); pg = (pg + n) % n;
      var c = cards[Math.min(cards.length - 1, pg * per())];
      var f = cards[0];
      var x = RTL ? -((f.offsetLeft + f.offsetWidth) - (c.offsetLeft + c.offsetWidth)) : c.offsetLeft - f.offsetLeft;
      track.scrollTo({ left: x });
    }
    function drawDots() {
      dots.innerHTML = ""; var n = pages(), k = cur();
      for (var i = 0; i < n; i++) { (function (i) { var d = el("button"); d.type = "button"; d.setAttribute("aria-label", (i + 1) + "/" + n); if (i === k) d.className = "on"; d.addEventListener("click", function () { go(i); hold(); }); dots.appendChild(d); })(i); }
    }
    prev.addEventListener("click", function () { go(cur() - 1); hold(); });
    next.addEventListener("click", function () { go(cur() + 1); hold(); });
    var t; track.addEventListener("scroll", function () { clearTimeout(t); t = setTimeout(drawDots, 120); });
    window.addEventListener("resize", drawDots); drawDots();
    /* auto-advance, paused on hover/touch and when off-screen */
    var paused = false, visible = false, timer;
    function hold() { paused = true; clearTimeout(timer); timer = setTimeout(function () { paused = false; }, 12000); }
    sec.addEventListener("mouseenter", function () { paused = true; }); sec.addEventListener("mouseleave", function () { paused = false; });
    track.addEventListener("touchstart", hold, { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(sec); else visible = true;
    if (!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches))
      setInterval(function () { if (visible && !paused && !document.hidden) go(cur() + 1); }, 6500);
  }
  var T = {};
  var HAS_T = ["ar","ckb","ru","de","fr","es","it","tr","pl","nl","pt","cs","sk","hr","ro","el","sv","da","no","fi","ka","ko","ja","zh","zh-tw","hi","ta","th","ms","id","fa","ur","vi"];
  function start() {
    if (HAS_T.indexOf(LG) < 0 || !window.fetch) return build();
    var base = /fabletour\.com$|^localhost|^127\./.test(location.hostname) && !PH ? "" : "https://iraq.fabletour.com";
    var done = false, to = setTimeout(function () { if (!done) { done = true; build(); } }, 4000);
    fetch(base + "/reviews-i18n/" + LG + ".json").then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; })
      .then(function (j) { if (done) return; done = true; clearTimeout(to); T = j || {}; build(); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
