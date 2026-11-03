/* Fable Tour – verified GetYourGuide reviews slider.
   Reviews are copied word for word from the Fable Tour supplier account on
   GetYourGuide (only reviews with text). To add a new one, add an object to R. */
(function () {
  "use strict";
  var GYG = "https://www.getyourguide.com/fable-tour-in-iraq-s471675/";
  var R = [
    { n: "Pavel", c: "Romania", d: "2026-10-05", s: 5, t: "Kadhimiya Sunrise Tour, Baghdad", lang: "ru",
      x: "Супер профессиональный гид. Все было на высоте . Рекомендую",
      en: "A super professional guide. Everything was top-notch. I recommend it." },
    { n: "Harry", c: "United Kingdom", d: "2026-10-04", s: 4, t: "Baghdad Old Town Guided Tour",
      x: "Very good! Highly recommend this tour to old town in the evening and enjoy some drinks! Tour guide great English, knowledgeable and friendly!" },
    { n: "Erik", c: "Netherlands", d: "2026-09-30", s: 5, t: "From Baghdad to the Shrines of Ezekiel & Prophet Job", lang: "nl",
      x: "Dankzij Saif een fantastische maar vooral ook heel indrukwekkende tour gehad. Die begon al met een mooie reis zuidwaarts door Irak. Na een hartelijke ontvangst bij de heiligdommen van Ezekiel en Ayyub werd de indrukwekkende en heel bijzondere achtergrond en historie verteld. Deze tour is beslist een aanrader.",
      en: "Thanks to Saif we had a fantastic and above all very impressive tour. It began with a beautiful drive south through Iraq. After a warm welcome at the shrines of Ezekiel and Ayyub (Job), the impressive and very special background and history were explained. This tour is definitely recommended." },
    { n: "Joe", c: "Estonia", d: "2026-09-03", s: 5, t: "From Baghdad: Karbala Holy Sites",
      x: "Awesome trip to Karbala, best trip during my time in Iraq. Comfortable car, flexible itinerary and a very knowledgable and dedicated guide. Karbala itself is mindblowing and a must see" },
    { n: "Zach", c: "United Kingdom", d: "2026-08-25", s: 5, t: "Duhok tour",
      x: "beautiful city and nice people and highly recommended to visit Dohuk. tour guide knows a lot about places history" },
    { n: "GetYourGuide traveler", c: "United Kingdom", d: "2026-08-23", s: 5, t: "From Baghdad: Babylon Walking Tour",
      x: "highly recommended. the tour guide have deep knowledge about Babylonian history and i will book another tours with him for another historical sites in iraq ." },
    { n: "GetYourGuide traveler", c: "United Kingdom", d: "2026-08-19", s: 5, t: "Two-day tour: Kufa, Najaf & Karbala",
      x: "Fluent in English, Russian and Arabic. Excellent service always flexible to meet the customers needs. Highly recommend" },
    { n: "Robert", c: "Germany", d: "2026-02-02", s: 5, t: "Baghdad: Full-Day Cultural Tour", lang: "de",
      x: "Das ist eine wundervolle Tour! Sie ist umfangreich, informativ und kurzweilig. Unser Guid Saif bringt viel Detailwissen mit und ist ein angenehmer Gastgeber. Alls verlief reibungslos, ohne Komplikationen und einfach, da er fließend Englisch und Russisch spricht. Wir können diese Tour sehr empfehlen und würden sie wieder buchen.",
      en: "This is a wonderful tour! It is comprehensive, informative and entertaining. Our guide Saif brings a lot of detailed knowledge and is a pleasant host. Everything went smoothly, without complications and easily, as he speaks fluent English and Russian. We highly recommend this tour and would book it again." },
    { n: "Michael", c: "Switzerland", d: "2026-01-19", s: 5, t: "Baghdad: Baghdadi Museum",
      x: "As a Swiss couple visiting Iraq for the first time, our visit to the Baghdadi Museum was one of the most memorable cultural experiences of our journey. The museum offers a vivid and authentic portrayal of traditional Baghdadi life, with lifelike scenes showing daily customs, crafts, music, family life, and social traditions that once defined the city." },
    { n: "Alessandro", c: "Italy", d: "2026-01-07", s: 5, t: "Baghdad: National Museum of Iraq",
      x: "Saif is attentive, well-organized, and genuinely passionate about sharing Iraq’s rich heritage. I highly recommend him to anyone looking for an authentic and enriching experience in Iraq. Although my first trip to Iraq lasted only a few days, it left a strong impression on me. On my next visit, I plan to stay for 15 days—and without hesitation, I will book the entire tour with Saif again." },
    { n: "Rana", c: "United States", d: "2025-12-24", s: 5, t: "Baghdad: Mustansiriyah Madrasah & Old Town",
      x: "My recent private tour through Old Town Baghdad, Al-Mutanabbi Street, the Baghdadi Museum, and Al-Mustansiriya School was nothing short of exceptional. This was not a standard sightseeing tour—it was a refined cultural journey designed with precision, depth, and elegance. From walking through the historic alleys of Old Baghdad to feeling the intellectual soul of Mutanabbi Street, every moment was curated with insight and respect for history. The Iraq Museum was presented with remarkable storytelling, transforming ancient artifacts into a living narrative of Mesopotamian civilization. Visiting the Mustansiriya School was a powerful reminder that Baghdad once stood at the heart of global knowledge and scholarship. The level of professionalism, discretion, and personalized attention reflected true luxury service. I felt completely safe, deeply informed, and genuinely welcomed. This experience reshaped my perception of Baghdad—not only as a historic city, but as a destination capable of" },
    { n: "Haroon", c: "United Kingdom", d: "2025-06-27", s: 5, t: "Baghdad: Full-Day Cultural Tour",
      x: "I thought I was just visiting a city — I didn’t expect to fall in love. Al-Mutanabbi Street was alive with poetry, books, and an energy I can’t describe. With every step, I felt Baghdad whispering her secrets. At the Mustansiriya School, I stood in awe — centuries of beauty and knowledge carved into every detail. But it was the Baghdadi Museum that surprised me most. It wasn’t about ancient ruins — it was about people. Weddings, traditions, laughter in the public baths… It felt like walking through Baghdad’s memory. And in Souk Al-Safarin, time slowed. I found myself touching handmade treasures I didn’t know I needed. It wasn’t a tour. It was an experience I didn’t know my soul was craving." },
    { n: "Ewa", c: "Poland", d: "2025-04-22", s: 5, t: "7-Day Iraq Heritage Tour",
      x: "I came to Iraq looking for history. What I found was so much more: soul, beauty, kindness, and a sense of connection I didn`t know I was missing. Every single day of this 10-day journey was filled with moments I`ll never forget. And all of it - every smile, every sacred site, every incredible meal - was made possible thanks to our amazing guide, whose warmth and deep knowledge made us feel like we weren`t just tourists - we were family. We visited sacred shrines in Baghdad, Karbala and Najaf. In Samarra we saw architectural marvels: iconic spiral minaret, the Grand Mosque and the Abu Dulaf Mosque. On our way there were also: legendary city of Uruk, ancient ruins of Babylon and Borsippa, magnificent Zigurrat of Ur, the must-see Iraqi National Museum in Baghdad. We explored the Al-Chibayish Marshes and colourful markets. The food was absolutely delicious. This fantastic tour was perfectly organised (very good hotels, meals, comfortable transport, entrance tickets) by our local guide." },
    { n: "David", c: "United Arab Emirates", d: "2024-12-26", s: 5, t: "Baghdad: National Museum of Iraq",
      x: "The museum has a broad and rich collection of archaeological treasures and it’s definitely a must. I would have loved to receive more history information about the museums but there were no audio guides available. The 1.5h tour is recommended for those interested in knowing more about Iraqi culture and history." }
  ];

  var LANGS = ["zh-tw","cs","da","de","el","en","es","fa","fi","fr","hi","hr","id","it","ja","ka","ko","ms","nl","no","pl","pt","ro","ru","sk","sv","ta","th","tr","ur","zh"];
  var seg = (location.pathname.split("/")[1] || "").toLowerCase();
  var LG = LANGS.indexOf(seg) >= 0 ? seg : "ar";
  var UI = {
    ar: ["آراء المسافرين", "تقييمات موثّقة على GetYourGuide", "حجز موثّق على GetYourGuide", "عرض الترجمة", "النص الأصلي", "كل التقييمات على GetYourGuide", "السابق", "التالي"],
    en: ["Traveller reviews", "Verified reviews on GetYourGuide", "Verified booking on GetYourGuide", "Show translation", "Show original", "All reviews on GetYourGuide", "Previous", "Next"],
    ru: ["Отзывы путешественников", "Проверенные отзывы на GetYourGuide", "Подтверждённое бронирование на GetYourGuide", "Показать перевод", "Оригинал", "Все отзывы на GetYourGuide", "Назад", "Вперёд"],
    de: ["Bewertungen von Reisenden", "Verifizierte Bewertungen auf GetYourGuide", "Verifizierte Buchung auf GetYourGuide", "Übersetzung anzeigen", "Original anzeigen", "Alle Bewertungen auf GetYourGuide", "Zurück", "Weiter"],
    fr: ["Avis des voyageurs", "Avis vérifiés sur GetYourGuide", "Réservation vérifiée sur GetYourGuide", "Voir la traduction", "Voir l'original", "Tous les avis sur GetYourGuide", "Précédent", "Suivant"],
    es: ["Opiniones de viajeros", "Opiniones verificadas en GetYourGuide", "Reserva verificada en GetYourGuide", "Ver traducción", "Ver original", "Todas las opiniones en GetYourGuide", "Anterior", "Siguiente"],
    it: ["Recensioni dei viaggiatori", "Recensioni verificate su GetYourGuide", "Prenotazione verificata su GetYourGuide", "Mostra traduzione", "Mostra originale", "Tutte le recensioni su GetYourGuide", "Precedente", "Successivo"],
    tr: ["Gezgin yorumları", "GetYourGuide'da doğrulanmış yorumlar", "GetYourGuide'da doğrulanmış rezervasyon", "Çeviriyi göster", "Orijinali göster", "GetYourGuide'daki tüm yorumlar", "Önceki", "Sonraki"],
    fa: ["نظرات مسافران", "نظرات تأییدشده در GetYourGuide", "رزرو تأییدشده در GetYourGuide", "نمایش ترجمه", "متن اصلی", "همه نظرات در GetYourGuide", "قبلی", "بعدی"],
    ur: ["مسافروں کے تبصرے", "GetYourGuide پر تصدیق شدہ تبصرے", "GetYourGuide پر تصدیق شدہ بکنگ", "ترجمہ دیکھیں", "اصل متن", "GetYourGuide پر تمام تبصرے", "پچھلا", "اگلا"]
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
    ".gr-tr{align-self:flex-start;background:none;border:0;padding:0;color:var(--navy-2,#2A3D63);font:inherit;font-size:13px;font-weight:700;cursor:pointer;text-decoration:underline}" +
    ".gr-ft{margin-top:auto;padding-top:10px;border-top:1px solid var(--line,rgba(27,42,71,.1));display:flex;flex-direction:column;gap:3px}" +
    ".gr-tour{font-size:13px;font-weight:700;color:var(--navy,#1B2A47)}" +
    ".gr-ver{font-size:12px;color:#2E7D4F;display:flex;align-items:center;gap:5px}" +
    ".gr-dots{display:flex;justify-content:center;gap:7px;margin-top:4px}.gr-dots button{width:9px;height:9px;border-radius:50%;border:0;padding:0;background:#D5D9E0;cursor:pointer}.gr-dots button.on{background:var(--gold,#B8955A);width:22px;border-radius:5px}" +
    ".gr-all{display:inline-block;margin-top:14px;color:var(--navy,#1B2A47);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:2px solid var(--gold,#B8955A);padding-bottom:2px}" +
    "@media (max-width:900px){.gr-c{flex-basis:calc((100% - 18px)/2)}}" +
    "@media (max-width:600px){.gr-c{flex-basis:88%}.gr-nav{display:none}}";

  var CHK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var ARR = function (d) { return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + (d < 0 ? "M15 5l-7 7 7 7" : "M9 5l7 7-7 7") + '"/></svg>'; };

  function build() {
    var anchor = document.getElementById("video-journeys") || document.getElementById("gallery") || document.getElementById("faq");
    if (!anchor || document.getElementById("gyg-reviews")) return;
    var st = el("style"); st.textContent = css; document.head.appendChild(st);
    var sec = el("section", "block in gr"); sec.id = "gyg-reviews"; sec.setAttribute("aria-label", U[0]);
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
      var wd = el("div"); wd.appendChild(el("b", null, r.n)); wd.appendChild(el("small", null, r.c));
      who.appendChild(av); who.appendChild(wd); c.appendChild(who);
      var p = el("p", "gr-tx", r.x); if (r.lang) p.lang = r.lang; else p.lang = "en";
      c.appendChild(p);
      if (r.en && LG !== r.lang) {
        var b = el("button", "gr-tr", U[3]); b.type = "button"; var shown = false;
        b.addEventListener("click", function () { shown = !shown; p.textContent = shown ? r.en : r.x; p.lang = shown ? "en" : r.lang; b.textContent = shown ? U[4] : U[3]; });
        c.appendChild(b);
      }
      var ft = el("div", "gr-ft"); ft.appendChild(el("span", "gr-tour", r.t));
      var v = el("span", "gr-ver"); v.innerHTML = CHK; v.appendChild(document.createTextNode(U[2])); ft.appendChild(v);
      c.appendChild(ft); track.appendChild(c);
    });
    sec.appendChild(track);
    var dots = el("div", "gr-dots"); sec.appendChild(dots);
    var all = el("a", "gr-all", U[5] + (RTL ? " ←" : " →")); all.href = GYG; all.target = "_blank"; all.rel = "noopener"; sec.appendChild(all);
    anchor.parentNode.insertBefore(sec, anchor);

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
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build); else build();
})();
