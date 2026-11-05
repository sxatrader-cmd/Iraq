/* Fable Tour – Iraq site Q&A assistant (no server, no API, free).
   Knowledge is read from the visitor's language home page (FAQ, programs,
   day trips, airport transfer, booking), so answers always match the site. */
(function () {
  "use strict";
  if (window.__ftBot) return; window.__ftBot = 1;

  var WA = "9647711745353";

  /* usage stats -> Supabase table chatbot_events (insert-only for the public key) */
  var SB = "https://zrbbnveaqockoptftqst.supabase.co/rest/v1/chatbot_events", SBK = "sb_publishable_YscqakXUfq9ngPjaAhe2KA__sFDoMcl", SID;
  try { SID = sessionStorage.getItem("ftb_sid"); if (!SID) { SID = Date.now().toString(36) + Math.random().toString(36).slice(2, 10); sessionStorage.setItem("ftb_sid", SID); } } catch (e) { SID = Date.now().toString(36) + Math.random().toString(36).slice(2, 10); }
  function logBot(ev, detail) {
    try {
      fetch(SB, { method: "POST", keepalive: true, headers: { apikey: SBK, Authorization: "Bearer " + SBK, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify({ session_id: SID, page: location.pathname, lang: typeof LG === "string" ? LG : "", event: ev, detail: String(detail || "").slice(0, 300) }) }).catch(function () {});
    } catch (e) {}
  }
  var LANGS = ["zh-tw","cs","da","de","el","en","es","fa","fi","fr","hi","hr","id","it","ja","ka","ko","ms","nl","no","pl","pt","ro","ru","sk","sv","ta","th","tr","ur","zh","ckb","vi"];
  var SL = {"ziyara":"baghdad-holy-shrines","oldtown":"baghdad-old-town","aqarquf":"aqar-quf","madain":"al-madain-ctesiphon","samarra":"samarra","babylon":"babylon","babylon4":"babylon-borsippa-kifl","holy":"kufa-najaf-karbala","south":"ur-marshes"};

  var seg = (location.pathname.split("/")[1] || "").toLowerCase();
  var LG = LANGS.indexOf(seg) >= 0 ? seg : "ar", PG = LG;
  var HOME = LG === "ar" ? "/" : "/" + LG + "/";

  /* ---------- interface text (32 languages) ---------- */
  var K = ["t","hi","ph","nf","wa","more","prog","dt","ap","faq","bk","one","open","q","thx","send","close","form"];
  var S = {
    ar:["مساعد Fable Tour","أهلاً بك! أجيبك عن أسئلتك حول رحلاتنا في العراق. اختر موضوعاً أو اكتب سؤالك.","اكتب سؤالك…","لم أجد إجابة لهذا السؤال. راسلنا على واتساب وسنرد عليك بسرعة.","تواصل عبر واتساب","مواضيع أخرى","البرامج والأسعار","رحلات اليوم الواحد","الاستقبال من المطار","أسئلة شائعة","احجز رحلتك","لشخص واحد","التفاصيل","عندك سؤال؟","العفو! هل تريد شيئاً آخر؟","إرسال","إغلاق","افتح نموذج الحجز"],
    ckb:["یاریدەدەری Fable Tour","سڵاو! وەڵامی پرسیارەکانت دەدەمەوە دەربارەی گەشتەکانمان لە عێراق. بابەتێک هەڵبژێرە یان پرسیارەکەت بنووسە.","پرسیارەکەت بنووسە…","وەڵامی ئەم پرسیارەم نەدۆزییەوە. لە واتسئاپ نامەمان بۆ بنێرە و بە خێرایی وەڵامت دەدەینەوە.","پەیوەندی لە واتسئاپ","بابەتی تر","بەرنامە و نرخەکان","گەشتی یەک ڕۆژە","پێشوازی لە فڕۆکەخانە","پرسیارە باوەکان","گەشتەکەت حیجز بکە","بۆ 1 کەس","وردەکاری","پرسیارێکت هەیە؟","سوپاس! شتێکی ترت دەوێت؟","ناردن","داخستن","فۆرمی حیجز بکەرەوە"],
    en:["Fable Tour assistant","Hello! I can answer your questions about our tours in Iraq. Pick a topic or type your question.","Type your question…","I couldn't find an answer to that. Message us on WhatsApp and we'll reply quickly.","Chat on WhatsApp","Other topics","Programs & prices","Day trips","Airport pickup","FAQ","Book your trip","for 1 person","Details","Have a question?","You're welcome! Anything else?","Send","Close","Open the booking form"],
    tr:["Fable Tour asistanı","Merhaba! Irak turlarımızla ilgili sorularınızı yanıtlayabilirim. Bir konu seçin veya sorunuzu yazın.","Sorunuzu yazın…","Bu sorunun cevabını bulamadım. Bize WhatsApp'tan yazın, hemen yanıt verelim.","WhatsApp'tan yazın","Diğer konular","Programlar ve fiyatlar","Günübirlik turlar","Havalimanı karşılama","Sık sorulan sorular","Turunuzu ayırtın","1 kişi için","Detaylar","Sorunuz mu var?","Rica ederim! Başka bir şey var mı?","Gönder","Kapat","Rezervasyon formunu aç"],
    ru:["Помощник Fable Tour","Здравствуйте! Я отвечу на ваши вопросы о наших турах по Ираку. Выберите тему или напишите вопрос.","Напишите ваш вопрос…","Не нашёл ответа на этот вопрос. Напишите нам в WhatsApp — мы быстро ответим.","Написать в WhatsApp","Другие темы","Программы и цены","Однодневные экскурсии","Встреча в аэропорту","Частые вопросы","Забронировать тур","за 1 человека","Подробнее","Есть вопрос?","Пожалуйста! Чем ещё помочь?","Отправить","Закрыть","Открыть форму бронирования"],
    de:["Fable Tour Assistent","Hallo! Ich beantworte Ihre Fragen zu unseren Reisen im Irak. Wählen Sie ein Thema oder schreiben Sie Ihre Frage.","Ihre Frage…","Dazu habe ich keine Antwort gefunden. Schreiben Sie uns auf WhatsApp, wir antworten schnell.","Auf WhatsApp schreiben","Andere Themen","Programme & Preise","Tagesausflüge","Flughafenabholung","Häufige Fragen","Reise buchen","für 1 Person","Details","Haben Sie eine Frage?","Gern geschehen! Noch etwas?","Senden","Schließen","Buchungsformular öffnen"],
    fr:["Assistant Fable Tour","Bonjour ! Je réponds à vos questions sur nos circuits en Irak. Choisissez un sujet ou écrivez votre question.","Votre question…","Je n'ai pas trouvé de réponse. Écrivez-nous sur WhatsApp, nous répondons rapidement.","Écrire sur WhatsApp","Autres sujets","Programmes et prix","Excursions d'une journée","Accueil à l'aéroport","Questions fréquentes","Réserver votre voyage","pour 1 personne","Détails","Une question ?","Avec plaisir ! Autre chose ?","Envoyer","Fermer","Ouvrir le formulaire de réservation"],
    es:["Asistente de Fable Tour","¡Hola! Respondo tus preguntas sobre nuestros viajes por Irak. Elige un tema o escribe tu pregunta.","Escribe tu pregunta…","No encontré respuesta a esa pregunta. Escríbenos por WhatsApp y te respondemos enseguida.","Escribir por WhatsApp","Otros temas","Programas y precios","Excursiones de un día","Recogida en el aeropuerto","Preguntas frecuentes","Reserva tu viaje","para 1 persona","Detalles","¿Tienes una pregunta?","¡De nada! ¿Algo más?","Enviar","Cerrar","Abrir el formulario de reserva"],
    it:["Assistente Fable Tour","Ciao! Rispondo alle tue domande sui nostri tour in Iraq. Scegli un argomento o scrivi la tua domanda.","Scrivi la tua domanda…","Non ho trovato una risposta. Scrivici su WhatsApp, rispondiamo subito.","Scrivi su WhatsApp","Altri argomenti","Programmi e prezzi","Escursioni giornaliere","Accoglienza in aeroporto","Domande frequenti","Prenota il viaggio","per 1 persona","Dettagli","Hai una domanda?","Prego! Altro?","Invia","Chiudi","Apri il modulo di prenotazione"],
    el:["Βοηθός Fable Tour","Γεια σας! Απαντώ στις ερωτήσεις σας για τις περιηγήσεις μας στο Ιράκ. Διαλέξτε θέμα ή γράψτε την ερώτησή σας.","Γράψτε την ερώτησή σας…","Δεν βρήκα απάντηση. Γράψτε μας στο WhatsApp και θα απαντήσουμε γρήγορα.","Μήνυμα στο WhatsApp","Άλλα θέματα","Προγράμματα και τιμές","Ημερήσιες εκδρομές","Παραλαβή από το αεροδρόμιο","Συχνές ερωτήσεις","Κράτηση ταξιδιού","για 1 άτομο","Λεπτομέρειες","Έχετε ερώτηση;","Παρακαλώ! Κάτι άλλο;","Αποστολή","Κλείσιμο","Άνοιγμα φόρμας κράτησης"],
    cs:["Asistent Fable Tour","Dobrý den! Odpovím na vaše otázky o našich zájezdech do Iráku. Vyberte téma nebo napište otázku.","Napište svou otázku…","Na tuto otázku jsem odpověď nenašel. Napište nám na WhatsApp, odpovíme rychle.","Napsat na WhatsApp","Další témata","Programy a ceny","Jednodenní výlety","Vyzvednutí na letišti","Časté otázky","Rezervovat cestu","za 1 osobu","Podrobnosti","Máte otázku?","Rádo se stalo! Ještě něco?","Odeslat","Zavřít","Otevřít rezervační formulář"],
    pl:["Asystent Fable Tour","Dzień dobry! Odpowiem na pytania o nasze wycieczki po Iraku. Wybierz temat lub wpisz pytanie.","Wpisz pytanie…","Nie znalazłem odpowiedzi na to pytanie. Napisz do nas na WhatsApp, odpowiemy szybko.","Napisz na WhatsApp","Inne tematy","Programy i ceny","Wycieczki jednodniowe","Odbiór z lotniska","Częste pytania","Zarezerwuj podróż","za 1 osobę","Szczegóły","Masz pytanie?","Proszę bardzo! Coś jeszcze?","Wyślij","Zamknij","Otwórz formularz rezerwacji"],
    zh:["Fable Tour 助手","您好！我可以回答关于我们伊拉克旅游的问题。请选择一个主题或输入您的问题。","输入您的问题…","没有找到这个问题的答案。请通过 WhatsApp 联系我们，我们会尽快回复。","WhatsApp 联系","其他主题","行程与价格","一日游","机场接机","常见问题","预订行程","1人","详情","有问题吗？","不客气！还有其他问题吗？","发送","关闭","打开预订表单"],
    "zh-tw":["Fable Tour 助理","您好！我可以回答關於我們伊拉克旅遊的問題。請選擇主題或輸入您的問題。","輸入您的問題…","找不到這個問題的答案。請透過 WhatsApp 聯絡我們，我們會盡快回覆。","WhatsApp 聯絡","其他主題","行程與價格","一日遊","機場接機","常見問題","預訂行程","1人","詳情","有問題嗎？","不客氣！還有其他問題嗎？","傳送","關閉","開啟預訂表單"],
    ja:["Fable Tour アシスタント","こんにちは！イラクツアーについてのご質問にお答えします。トピックを選ぶか、質問を入力してください。","ご質問を入力…","その質問への回答が見つかりませんでした。WhatsAppでお問い合わせください。すぐに返信します。","WhatsAppで問い合わせ","その他のトピック","プランと料金","日帰りツアー","空港送迎","よくある質問","予約する","1名","詳細","ご質問はありますか？","どういたしまして！他にご質問は？","送信","閉じる","予約フォームを開く"],
    fa:["دستیار Fable Tour","سلام! به سؤالات شما درباره تورهای ما در عراق پاسخ می‌دهم. یک موضوع را انتخاب کنید یا سؤالتان را بنویسید.","سؤال خود را بنویسید…","پاسخی برای این سؤال پیدا نکردم. در واتس‌اپ به ما پیام دهید، سریع پاسخ می‌دهیم.","پیام در واتس‌اپ","موضوعات دیگر","برنامه‌ها و قیمت‌ها","تورهای یک‌روزه","استقبال از فرودگاه","سؤالات متداول","رزرو سفر","برای ۱ نفر","جزئیات","سؤالی دارید؟","خواهش می‌کنم! سؤال دیگری دارید؟","ارسال","بستن","باز کردن فرم رزرو"],
    ms:["Pembantu Fable Tour","Hai! Saya boleh menjawab soalan anda tentang lawatan kami di Iraq. Pilih topik atau taip soalan anda.","Taip soalan anda…","Saya tidak menemui jawapan untuk soalan itu. Hubungi kami di WhatsApp, kami akan membalas dengan cepat.","Hubungi di WhatsApp","Topik lain","Program & harga","Lawatan sehari","Sambutan di lapangan terbang","Soalan lazim","Tempah perjalanan","untuk 1 orang","Butiran","Ada soalan?","Sama-sama! Ada lagi?","Hantar","Tutup","Buka borang tempahan"],
    id:["Asisten Fable Tour","Halo! Saya bisa menjawab pertanyaan Anda tentang tur kami di Irak. Pilih topik atau ketik pertanyaan Anda.","Ketik pertanyaan Anda…","Saya tidak menemukan jawaban untuk pertanyaan itu. Hubungi kami di WhatsApp, kami akan membalas dengan cepat.","Chat di WhatsApp","Topik lain","Program & harga","Tur sehari","Penjemputan bandara","Pertanyaan umum","Pesan perjalanan","untuk 1 orang","Detail","Ada pertanyaan?","Sama-sama! Ada lagi?","Kirim","Tutup","Buka formulir pemesanan"],
    th:["ผู้ช่วย Fable Tour","สวัสดีครับ! ผมตอบคำถามเกี่ยวกับทัวร์อิรักของเราได้ เลือกหัวข้อหรือพิมพ์คำถามของคุณ","พิมพ์คำถามของคุณ…","ไม่พบคำตอบสำหรับคำถามนี้ ติดต่อเราทาง WhatsApp แล้วเราจะตอบกลับโดยเร็ว","แชทผ่าน WhatsApp","หัวข้ออื่น","โปรแกรมและราคา","ทริปหนึ่งวัน","รับที่สนามบิน","คำถามที่พบบ่อย","จองทริป","สำหรับ 1 ท่าน","รายละเอียด","มีคำถามไหม?","ยินดีครับ! มีอะไรอีกไหม?","ส่ง","ปิด","เปิดแบบฟอร์มการจอง"],
    ta:["Fable Tour உதவியாளர்","வணக்கம்! ஈராக்கில் எங்கள் சுற்றுலாக்கள் பற்றிய உங்கள் கேள்விகளுக்கு பதிலளிக்கிறேன். ஒரு தலைப்பைத் தேர்ந்தெடுக்கவும் அல்லது உங்கள் கேள்வியை எழுதவும்.","உங்கள் கேள்வியை எழுதுங்கள்…","இந்தக் கேள்விக்கு பதில் கிடைக்கவில்லை. WhatsApp-இல் எங்களுக்கு எழுதுங்கள், விரைவில் பதிலளிப்போம்.","WhatsApp-இல் பேசுங்கள்","மற்ற தலைப்புகள்","திட்டங்கள் & விலைகள்","ஒரு நாள் பயணங்கள்","விமான நிலைய வரவேற்பு","அடிக்கடி கேட்கப்படும் கேள்விகள்","பயணத்தை முன்பதிவு செய்யுங்கள்","1 நபருக்கு","விவரங்கள்","கேள்வி உள்ளதா?","பரவாயில்லை! வேறு ஏதாவது வேண்டுமா?","அனுப்பு","மூடு","முன்பதிவு படிவத்தைத் திறக்கவும்"],
    hi:["Fable Tour सहायक","नमस्ते! मैं इराक में हमारे टूर के बारे में आपके सवालों के जवाब देता हूँ। कोई विषय चुनें या अपना सवाल लिखें।","अपना सवाल लिखें…","इस सवाल का जवाब नहीं मिला। हमें WhatsApp पर लिखें, हम जल्दी जवाब देंगे।","WhatsApp पर बात करें","अन्य विषय","प्रोग्राम और कीमतें","एक दिन की यात्राएँ","एयरपोर्ट पिकअप","अक्सर पूछे जाने वाले सवाल","यात्रा बुक करें","1 व्यक्ति के लिए","विवरण","कोई सवाल है?","आपका स्वागत है! और कुछ?","भेजें","बंद करें","बुकिंग फ़ॉर्म खोलें"],
    ur:["Fable Tour معاون","السلام علیکم! میں عراق میں ہمارے ٹورز کے بارے میں آپ کے سوالات کے جواب دیتا ہوں۔ کوئی موضوع منتخب کریں یا اپنا سوال لکھیں۔","اپنا سوال لکھیں…","اس سوال کا جواب نہیں ملا۔ ہمیں واٹس ایپ پر لکھیں، ہم جلد جواب دیں گے۔","واٹس ایپ پر بات کریں","دیگر موضوعات","پروگرام اور قیمتیں","ایک دن کے دورے","ایئرپورٹ پک اپ","عام سوالات","سفر بک کریں","1 فرد کے لیے","تفصیلات","کوئی سوال؟","خوش آمدید! کچھ اور؟","بھیجیں","بند کریں","بکنگ فارم کھولیں"],
    fi:["Fable Tour -avustaja","Hei! Vastaan kysymyksiisi Irakin matkoistamme. Valitse aihe tai kirjoita kysymyksesi.","Kirjoita kysymyksesi…","En löytänyt vastausta tähän kysymykseen. Kirjoita meille WhatsAppissa, vastaamme nopeasti.","Kirjoita WhatsAppissa","Muut aiheet","Ohjelmat ja hinnat","Päiväretket","Lentokenttänouto","Usein kysytyt","Varaa matka","1 hengelle","Lisätiedot","Onko sinulla kysyttävää?","Ole hyvä! Jotain muuta?","Lähetä","Sulje","Avaa varauslomake"],
    sv:["Fable Tour-assistent","Hej! Jag svarar på dina frågor om våra resor i Irak. Välj ett ämne eller skriv din fråga.","Skriv din fråga…","Jag hittade inget svar på den frågan. Skriv till oss på WhatsApp så svarar vi snabbt.","Skriv på WhatsApp","Andra ämnen","Program och priser","Dagsutflykter","Hämtning på flygplatsen","Vanliga frågor","Boka resan","för 1 person","Detaljer","Har du en fråga?","Varsågod! Något mer?","Skicka","Stäng","Öppna bokningsformuläret"],
    da:["Fable Tour-assistent","Hej! Jeg svarer på dine spørgsmål om vores ture i Irak. Vælg et emne eller skriv dit spørgsmål.","Skriv dit spørgsmål…","Jeg fandt ikke et svar på det spørgsmål. Skriv til os på WhatsApp, så svarer vi hurtigt.","Skriv på WhatsApp","Andre emner","Programmer og priser","Dagsture","Afhentning i lufthavnen","Ofte stillede spørgsmål","Book rejsen","for 1 person","Detaljer","Har du et spørgsmål?","Selv tak! Andet?","Send","Luk","Åbn bookingformularen"],
    no:["Fable Tour-assistent","Hei! Jeg svarer på spørsmålene dine om turene våre i Irak. Velg et emne eller skriv spørsmålet ditt.","Skriv spørsmålet ditt…","Jeg fant ikke svar på det spørsmålet. Skriv til oss på WhatsApp, så svarer vi raskt.","Skriv på WhatsApp","Andre emner","Programmer og priser","Dagsturer","Henting på flyplassen","Vanlige spørsmål","Bestill reisen","for 1 person","Detaljer","Har du et spørsmål?","Bare hyggelig! Noe mer?","Send","Lukk","Åpne bestillingsskjemaet"],
    sk:["Asistent Fable Tour","Dobrý deň! Odpoviem na vaše otázky o našich zájazdoch do Iraku. Vyberte tému alebo napíšte otázku.","Napíšte svoju otázku…","Na túto otázku som nenašiel odpoveď. Napíšte nám na WhatsApp, odpovieme rýchlo.","Napísať na WhatsApp","Ďalšie témy","Programy a ceny","Jednodňové výlety","Vyzdvihnutie na letisku","Časté otázky","Rezervovať cestu","za 1 osobu","Podrobnosti","Máte otázku?","Nie je za čo! Ešte niečo?","Odoslať","Zavrieť","Otvoriť rezervačný formulár"],
    hr:["Fable Tour asistent","Pozdrav! Odgovaram na vaša pitanja o našim putovanjima u Irak. Odaberite temu ili napišite pitanje.","Napišite svoje pitanje…","Nisam pronašao odgovor na to pitanje. Pišite nam na WhatsApp, brzo odgovaramo.","Pišite na WhatsApp","Druge teme","Programi i cijene","Jednodnevni izleti","Doček u zračnoj luci","Česta pitanja","Rezervirajte putovanje","za 1 osobu","Detalji","Imate pitanje?","Nema na čemu! Još nešto?","Pošalji","Zatvori","Otvori obrazac za rezervaciju"],
    ro:["Asistent Fable Tour","Bună ziua! Răspund la întrebările dumneavoastră despre circuitele noastre în Irak. Alegeți un subiect sau scrieți întrebarea.","Scrieți întrebarea…","Nu am găsit un răspuns la această întrebare. Scrieți-ne pe WhatsApp, răspundem rapid.","Scrieți pe WhatsApp","Alte subiecte","Programe și prețuri","Excursii de o zi","Preluare de la aeroport","Întrebări frecvente","Rezervați călătoria","pentru 1 persoană","Detalii","Aveți o întrebare?","Cu plăcere! Altceva?","Trimite","Închide","Deschide formularul de rezervare"],
    nl:["Fable Tour-assistent","Hallo! Ik beantwoord je vragen over onze reizen in Irak. Kies een onderwerp of typ je vraag.","Typ je vraag…","Ik heb geen antwoord op die vraag gevonden. Stuur ons een bericht via WhatsApp, we reageren snel.","Chat via WhatsApp","Andere onderwerpen","Programma's en prijzen","Dagtochten","Ophalen op de luchthaven","Veelgestelde vragen","Boek je reis","voor 1 persoon","Details","Heb je een vraag?","Graag gedaan! Nog iets?","Verstuur","Sluiten","Open het boekingsformulier"],
    ka:["Fable Tour-ის ასისტენტი","გამარჯობა! გიპასუხებთ კითხვებზე ერაყში ჩვენი ტურების შესახებ. აირჩიეთ თემა ან დაწერეთ კითხვა.","დაწერეთ თქვენი კითხვა…","ამ კითხვაზე პასუხი ვერ ვიპოვე. მოგვწერეთ WhatsApp-ზე, სწრაფად გიპასუხებთ.","მოგვწერეთ WhatsApp-ზე","სხვა თემები","პროგრამები და ფასები","ერთდღიანი ექსკურსიები","აეროპორტში დახვედრა","ხშირი კითხვები","დაჯავშნეთ მოგზაურობა","1 ადამიანზე","დეტალები","გაქვთ კითხვა?","არაფრის! კიდევ რამე?","გაგზავნა","დახურვა","დაჯავშნის ფორმის გახსნა"],
    ko:["Fable Tour 도우미","안녕하세요! 이라크 투어에 관한 질문에 답해 드립니다. 주제를 선택하거나 질문을 입력하세요.","질문을 입력하세요…","해당 질문에 대한 답을 찾지 못했습니다. WhatsApp으로 문의해 주시면 빠르게 답변드리겠습니다.","WhatsApp으로 문의","다른 주제","프로그램 및 가격","당일 투어","공항 픽업","자주 묻는 질문","여행 예약","1인 기준","자세히","궁금한 점이 있으신가요?","천만에요! 더 궁금한 점이 있으신가요?","보내기","닫기","예약 양식 열기"],
    pt:["Assistente Fable Tour","Olá! Respondo às suas perguntas sobre os nossos circuitos no Iraque. Escolha um tema ou escreva a sua pergunta.","Escreva a sua pergunta…","Não encontrei resposta para essa pergunta. Escreva-nos pelo WhatsApp e respondemos rapidamente.","Falar pelo WhatsApp","Outros temas","Programas e preços","Passeios de um dia","Recolha no aeroporto","Perguntas frequentes","Reservar a viagem","para 1 pessoa","Detalhes","Tem uma pergunta?","De nada! Mais alguma coisa?","Enviar","Fechar","Abrir o formulário de reserva"],
    vi:["Trợ lý Fable Tour","Xin chào! Tôi trả lời các câu hỏi của bạn về tour Iraq của chúng tôi. Hãy chọn một chủ đề hoặc gõ câu hỏi.","Nhập câu hỏi của bạn…","Tôi chưa tìm thấy câu trả lời cho câu hỏi này. Hãy nhắn cho chúng tôi qua WhatsApp, chúng tôi sẽ trả lời nhanh.","Nhắn qua WhatsApp","Chủ đề khác","Chương trình và giá","Tour trong ngày","Đón tại sân bay","Câu hỏi thường gặp","Đặt chuyến đi","cho 1 người","Chi tiết","Bạn có câu hỏi?","Không có gì! Bạn cần gì thêm không?","Gửi","Đóng","Mở biểu mẫu đặt tour"]
  };
  var T = {}; function setT() { var a = S[LG] || S.en; for (var i = 0; i < K.length; i++) T[K[i]] = a[i]; } setT();

  /* answer to flight questions and any extra service the visitor asks for (Saif: always "yes, on request") */
  var SV = {
    ar:"نعم، هذا ممكن عند الطلب. راسلنا على واتساب بما تحتاجه وسيرتّبه لك فريق Fable Tour.",
    en:"Yes, that's possible on request. Message us on WhatsApp with what you need and the Fable Tour team will arrange it for you.",
    ru:"Да, это возможно по запросу. Напишите нам в WhatsApp, что вам нужно, и команда Fable Tour всё организует.",
    de:"Ja, das ist auf Anfrage möglich. Schreiben Sie uns auf WhatsApp, was Sie brauchen, und das Fable-Tour-Team organisiert es für Sie.",
    fr:"Oui, c'est possible sur demande. Écrivez-nous sur WhatsApp ce dont vous avez besoin et l'équipe Fable Tour s'en occupe.",
    es:"Sí, es posible bajo petición. Escríbanos por WhatsApp lo que necesita y el equipo de Fable Tour lo organizará.",
    it:"Sì, è possibile su richiesta. Scriveteci su WhatsApp di cosa avete bisogno e il team Fable Tour se ne occuperà.",
    tr:"Evet, talep üzerine mümkün. İhtiyacınızı WhatsApp'tan yazın, Fable Tour ekibi sizin için ayarlasın.",
    el:"Ναι, είναι δυνατό κατόπιν αιτήματος. Γράψτε μας στο WhatsApp τι χρειάζεστε και η ομάδα της Fable Tour θα το κανονίσει.",
    cs:"Ano, na vyžádání je to možné. Napište nám na WhatsApp, co potřebujete, a tým Fable Tour to zařídí.",
    pl:"Tak, jest to możliwe na życzenie. Napisz nam na WhatsAppie, czego potrzebujesz, a zespół Fable Tour wszystko zorganizuje.",
    zh:"可以，按需安排。请通过 WhatsApp 告诉我们您的需求，Fable Tour 团队会为您安排。",
    "zh-tw":"可以，依需求安排。請透過 WhatsApp 告訴我們您的需求，Fable Tour 團隊會為您安排。",
    ja:"はい、ご希望に応じて手配可能です。WhatsAppでご要望をお送りいただければ、Fable Tourチームが手配いたします。",
    ko:"네, 요청하시면 가능합니다. 필요하신 내용을 WhatsApp으로 보내 주시면 Fable Tour 팀이 준비해 드립니다.",
    fa:"بله، در صورت درخواست امکان‌پذیر است. نیاز خود را در واتساپ برای ما بفرستید تا تیم Fable Tour آن را ترتیب دهد.",
    ms:"Ya, boleh atas permintaan. Hantarkan keperluan anda melalui WhatsApp dan pasukan Fable Tour akan menguruskannya.",
    id:"Ya, bisa sesuai permintaan. Kirimkan kebutuhan Anda lewat WhatsApp dan tim Fable Tour akan mengaturnya untuk Anda.",
    th:"ได้ครับ จัดให้ได้ตามคำขอ ส่งรายละเอียดที่ต้องการมาทาง WhatsApp แล้วทีม Fable Tour จะจัดการให้",
    hi:"हाँ, अनुरोध पर यह संभव है। अपनी ज़रूरत WhatsApp पर भेजें, Fable Tour टीम आपके लिए इसकी व्यवस्था करेगी।,xin chào,chào bạn",
    ur:"جی ہاں، درخواست پر یہ ممکن ہے۔ اپنی ضرورت واٹس ایپ پر بھیجیں، Fable Tour کی ٹیم آپ کے لیے انتظام کر دے گی۔",
    ta:"ஆம், கோரிக்கையின் பேரில் இது சாத்தியம். உங்களுக்குத் தேவையானதை WhatsApp-இல் அனுப்புங்கள், Fable Tour குழு ஏற்பாடு செய்யும்.",
    fi:"Kyllä, se onnistuu pyynnöstä. Kerro tarpeesi meille WhatsAppissa, niin Fable Tourin tiimi järjestää sen.",
    sv:"Ja, det går att ordna på begäran. Skriv till oss på WhatsApp vad du behöver så ordnar Fable Tour-teamet det.",
    da:"Ja, det kan lade sig gøre på forespørgsel. Skriv til os på WhatsApp, hvad du har brug for, så arrangerer Fable Tour-teamet det.",
    no:"Ja, det er mulig på forespørsel. Skriv til oss på WhatsApp hva du trenger, så ordner Fable Tour-teamet det.",
    sk:"Áno, na požiadanie je to možné. Napíšte nám na WhatsApp, čo potrebujete, a tím Fable Tour to zariadi.",
    hr:"Da, to je moguće na zahtjev. Napišite nam na WhatsApp što vam treba i tim Fable Toura će to organizirati.",
    ro:"Da, este posibil la cerere. Scrieți-ne pe WhatsApp de ce aveți nevoie și echipa Fable Tour se va ocupa.",
    nl:"Ja, dat is op aanvraag mogelijk. Laat ons via WhatsApp weten wat je nodig hebt en het Fable Tour-team regelt het.",
    ka:"დიახ, მოთხოვნისამებრ შესაძლებელია. მოგვწერეთ WhatsApp-ზე რა გჭირდებათ და Fable Tour-ის გუნდი მოაგვარებს.",
    pt:"Sim, é possível mediante pedido. Escreva-nos pelo WhatsApp o que precisa e a equipa Fable Tour trata de tudo.",
    vi:"Có, chúng tôi có thể sắp xếp theo yêu cầu. Hãy nhắn cho chúng tôi qua WhatsApp điều bạn cần và đội ngũ Fable Tour sẽ lo liệu."
  };
  T.svc = SV[LG] || SV.en; var T0 = {}; for (var k0 in T) T0[k0] = T[k0];

  /* ---------- text matching ---------- */
  function norm(s) {
    s = String(s || "").toLowerCase();
    try { s = s.normalize("NFKD"); } catch (e) {}
    s = s.replace(/[̀-ًͯ-ٰٟـ]/g, "")
         .replace(/[آأإٱ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه")
         .replace(/ک/g, "ك").replace(/ی/g, "ي");
    try { s = s.replace(/[^\p{L}\p{M}\p{N}$€\s]/gu, " "); } catch (e) { s = s.replace(/[.,!?;:"'()\[\]{}«»“”،؟؛\-]/g, " "); }
    return s.replace(/\s+/g, " ").trim();
  }
  var DENSE = /[぀-ヿ㐀-鿿가-힯ᄀ-ᇿ฀-๿]/;
  function grams(s) {
    var a = Array.from(" " + s + " "), n = DENSE.test(s) ? 2 : 3, g = {}, c = 0;
    for (var i = 0; i + n <= a.length; i++) { var k = a.slice(i, i + n).join(""); if (k.trim().length && !g[k]) { g[k] = 1; c++; } }
    g.__n = c; return g;
  }
  function contain(gq, gt) { var h = 0; for (var k in gq) if (k !== "__n" && gt[k]) h++; return gq.__n ? h / gq.__n : 0; }

  /* intent keywords in all site languages (normalised on load) */
  var IN = {
    who:"who is,who are you,who will,about the guide,about your guide,tell me about,من هو,من انت,منو,مين,عن المرشد,кто,о гиде,wer ist,qui est,quien es,chi e,kimdir,kim,kto,kdo,ko je,cine este,wie is,kuka,vem ar,hvem er,ποιος,谁,誰,누구,siapa,ใคร,யார்,कौन,کون,کیست,ვინ,là ai,ai là",
    spk:"language,languages,speak,speaks,لغه,لغات,يتكلم,يتحدث,язык,говор,sprach,sprich,langue,parle,idioma,habla,lingu,parla,dil,konus,jezyk,jazyk,limb,taal,kieli,sprak,sprog,γλωσσ,语言,語言,言語,언어,bahasa,ภาษา,மொழி,भाषा,زبان,nói tiếng,ngôn ngữ",
    time:"what time,time now,local time,time in baghdad,time zone,timezone,كم الساعه,الساعه كم,الساعه الان,الوقت,التوقيت,توقيت,сколько времени,который час,время,часовой пояс,uhrzeit,wie spat,zeitzone,quelle heure,heure,fuseau,que hora,hora,zona horaria,che ore,ora locale,fuso orario,saat kac,saat dilimi,yerel saat,ktora godzina,godzina,strefa czasowa,kolik je hodin,casove pasmo,koliko je sati,vrijeme,ce ora,fus orar,hoe laat,tijdzone,paljonko kello,kello,aikavyohyke,vad ar klockan,klockan,tidszon,hvad er klokken,klokken,tidszone,hva er klokka,klokka,ωρα,ζωνη ωρας,几点,时间,時間,幾點,何時,時差,몇 시,시간,jam berapa,zona waktu,waktu,กี่โมง,เวลา,நேரம்,समय,कितने बजे,وقت,ساعت چند,کتنے بجے,საათი,დრო,mấy giờ,bây giờ là,giờ ở baghdad,múi giờ",
    dist:"how far,distance,km,км,kilomet,miles,how long does it take,driving time,كم تبعد,تبعد,المسافه,مسافه,كيلو,كم ساعه,كم تستغرق,расстоян,далеко,километр,сколько ехать,entfernung,wie weit,distance,a quelle distance,distancia,a que distancia,distanza,quanto dista,mesafe,ne kadar uzak,odleglosc,jak daleko,vzdalenost,udaljenost,distanta,afstand,hoe ver,etaisyys,avstand,hur langt,hvor langt,αποστασ,距离,多远,距離,多遠,どのくらい,距離,거리,얼마나 멀,jarak,berapa jauh,ระยะทาง,ไกล,தூரம்,दूरी,कितनी दूर,فاصله,چقدر دور,فاصلہ,کتنا دور,მანძილ,bao xa,khoảng cách,cách bao nhiêu,mất bao lâu",
    price:"price,prices,cost,how much,usd,dollar,euro,$,€,سعر,اسعار,الاسعار,كلفه,تكلفه,بكم,كم السعر,قيمه,цен,стоим,сколько,preis,kost,prix,cout,combien,tarif,precio,cuesta,cuanto,prezz,costo,quanto,fiyat,ucret,ne kadar,cena,ceny,koszt,kosztuj,stoji,cijen,koliko,pret,prijs,hinta,maksaa,pris,koster,kostar,preco,τιμ,κοστ,价格,价钱,多少钱,费用,價格,費用,料金,値段,いくら,가격,얼마,비용,harga,berapa,ราคา,เท่าไ,விலை,कीमत,कितन,قیمت,کتنا,هزینه,چند,ფას,ღირ,giá tour,giá bao nhiêu,bao nhiêu tiền,chi phí,giá cả,bảng giá,giá là",
    visa:"visa,viza,visum,vize,виз,فيز,تاشير,ویزا,ويزا,ویزہ,ვიზ,签证,簽證,ビザ,비자,วีซ,விசா,वीज़ा,वीजा,βιζα,θεωρησ,thị thực",
    cancel:"cancel,annul,отмен,الغاء,الغي,storn,zrus,odwol,anul,iptal,cancela,annull,otkaz,peruu,avbok,afbestil,ακυρ,取消,キャンセル,취소,batal,ยกเลิก,ரத்து,रद्द,منسوخ,لغو,გაუქმ,refund,استرجاع,возврат,hủy,hoàn tiền",
    pay:"pay,paying,ادفع,payment,deposit,دفع,عربون,مقدم,оплат,предоплат,депозит,zahl,anzahl,paiement,payer,acompte,pago,pagar,deposito,pagament,acconto,odeme,depozit,platb,zaloh,plat,zaliczk,placan,avans,betal,aanbetal,maksu,ennakko,depositum,πληρω,προκαταβολ,付款,定金,支付,訂金,支払,前金,결제,보증금,bayar,ชำระ,มัดจำ,கட்டண,भुगतान,ادائیگی,پرداخت,بیعانه,گادا,გადახდ,thanh toán,đặt cọc,trả tiền",
    safe:"safe,safety,secur,danger,امان,امن,خطر,безопас,опасн,sicher,gefahr,securi,segur,sicur,pericol,guven,tehlike,bezpieczn,niebezpie,bezpecn,sigur,veilig,turvall,saker,sikker,ασφαλ,κινδυν,安全,危险,危險,안전,위험,aman,bahaya,ปลอดภัย,อันตราย,பாதுகாப்,सुरक्षित,محفوظ,امنیت,ایمن,უსაფრთხ,an toàn,nguy hiểm",
    lang:"language,speak,guide,english,russian,لغه,لغات,مرشد,دليل,يتكلم,язык,гид,говор,sprach,sprich,reiseleiter,langue,parle,idioma,habla,guia,lingu,parla,dil,rehber,konus,jezyk,przewodnik,jazyk,pruvodc,sprievodc,vodic,limb,ghid,taal,gids,kieli,opas,sprak,sprog,γλωσσ,ξεναγ,语言,導遊,导游,語言,言語,ガイド,언어,가이드,bahasa,pemandu,ภาษา,ไกด์,மொழி,வழிகாட்ட,भाषा,गाइड,زبان,گائیڈ,راهنما,ენა,გიდ,ngôn ngữ,hướng dẫn viên,nói tiếng",
    group:"private,group,join,departure,خاص,جماعي,مجموعه,انطلاق,индивидуал,групп,privat,gruppe,abfahrt,prive,groupe,depart,privad,grupo,salida,gruppo,partenz,ozel,grup,kalkis,prywat,grupow,soukrom,skupin,sukrom,groep,vertrek,yksityi,ryhma,grupp,ιδιωτ,ομαδ,私人,团队,團體,プライベート,グループ,개인,단체,pribadi,rombongan,persendirian,kumpulan,ส่วนตัว,กลุ่ม,தனிப்பட்ட,குழு,निजी,समूह,پرائیویٹ,گروپ,خصوصی,گروه,კერძო,ჯგუფ,tour riêng,đi riêng,theo đoàn,tour đoàn,ghép đoàn,khởi hành",
    incl:"includ,flight,flights,meals,طيران,تذاكر,يشمل,شامل,وجبات,включ,перел,авиабил,inklusiv,flug,inclu,vol,vuelo,volo,compres,dahil,ucak,wliczon,zahrn,ukljuc,inbegrepen,vlucht,sisalt,lento,ingar,flyg,inkluder,περιλαμβ,πτησ,包含,包括,机票,機票,含まれ,航空券,포함,항공,termasuk,penerbangan,รวม,เที่ยวบิน,அடங்கும,விமானம்,शामिल,उड़ान,پرواز,ჩათვლ,ფრენ,bao gồm,vé máy bay,bữa ăn",
    fly:"flight,flights,airline,air ticket,plane ticket,airfare,طيران,طياره,الطياره,تذكره طيران,تذاكر طيران,حجز طيران,رحله جويه,خطوط جويه,перелет,перелёт,авиабилет,билет на самолет,рейс,авиакомпан,flug,fluge,flugticket,vol,vols,billet d avion,billets d avion,vuelo,vuelos,billete de avion,pasaje,volo,voli,biglietto aereo,ucak,ucus,ucak bileti,przelot,bilet lotniczy,loty,letenk,letenka,letadl,let letadlem,zrakoplov,avionsk,karta za avion,zbor,zboruri,bilet de avion,vlucht,vluchten,vliegticket,lento,lennot,lentolippu,flyg,flygbiljett,flybillet,flyreise,flyrejse,voo,voos,passagem aerea,bilhete de aviao,πτηση,πτησεις,αεροπορικ,机票,航班,機票,飛機,航空券,フライト,飛行機,항공권,항공편,비행기,tiket pesawat,penerbangan,pesawat,kapal terbang,tiket penerbangan,ตั๋วเครื่องบิน,เที่ยวบิน,เครื่องบิน,விமானம்,விமான டிக்கெட்,உடான்,उड़ान,फ्लाइट,हवाई टिकट,ہوائی ٹکٹ,فلائٹ,پرواز,بلیط هواپیما,بلیط,ფრენ,ავიაბილეთ,თვითმფრინავ,vé máy bay,chuyến bay,hãng bay,máy bay",
    inc2:"includ,inclu,يشمل,شامل,مشمول,ضمن السعر,включ,inklusiv,inbegriffen,enthalten,compres,inclus,dahil,wliczon,zahrn,ukljuc,inbegrepen,sisalt,ingar,inkluder,περιλαμβ,包含,包括,含まれ,포함,termasuk,รวม,அடங்கும,शामिल,شامل,ჩათვლ,bao gồm,đã gồm",
    svc:"do you offer,do you provide,do you arrange,can you arrange,can you book,can you get,can you provide,could you arrange,could you book,arrange,rent a car,car rental,hotel booking,book a hotel,sim card,insurance,translator,photographer,خدمه,خدمات,توفرون,توفير,توفر,تقدرون,تكدرون,ممكن تحجز,ممكن تحجزون,ممكن توفر,هل بالامكان,تأمين,تامين,شريحه,سياره خاصه,ايجار سياره,مترجم,مصور,حجز فندق,услуг,можете ли,организ,забронир,аренд,страхов,сим карт,переводчик,dienstleist,konnen sie,konnt ihr,organisier,mietwagen,versicher,pouvez vous,organiser,location de voiture,assurance,servicio,puede organizar,alquiler,seguro,servizi,noleggio,assicurazion,hizmet,ayarlay,kiralik,sigorta,uslug,czy mozecie,wynajem,ubezpiecz,sluzb,pronajem,pojisten,najam,osiguranj,servici,puteti,inchiri,asigur,dienst,kunnen jullie,huurauto,verzeker,palvelu,voitteko,vuokra,vakuutu,tjanst,hyrbil,forsakring,tjeneste,leiebil,lejebil,forsikring,servico,aluguer,υπηρεσ,μπορειτε,ενοικιασ,ασφαλισ,服务,服務,租车,保险,保險,サービス,手配,レンタカー,保険,서비스,렌터카,보험,bisa bantu,boleh bantu,boleh atur,bisa atur,sewa kereta,sewa mobil,asuransi,insurans,บริการ,จัดให้,เช่ารถ,ประกัน,சேவை,ஏற்பாடு,सेवा,व्यवस्था,बीमा,سروس,انتظام,بیمہ,خدمات,ترتیب,اجاره,بیمه,მომსახურ,შეგიძლიათ,დაზღვევ,thuê xe,đặt khách sạn,sim điện thoại,bảo hiểm,phiên dịch,nhiếp ảnh",
    book:"book,booking,reserv,حجز,احجز,брон,buch,prenot,rezerv,boek,varaa,varaus,bestil,boka,κρατ,预订,預訂,予約,예약,tempah,pesan,จอง,முன்பதிவு,बुक,بک,رزرو,დაჯავშ,đặt tour,đặt chỗ,muốn đặt",
    prog:"program,programs,itinerar,difference,7 day,9 day,برنامج,برامج,البرنامجين,الفرق,مسار,программ,маршрут,отлича,unterschied,rundreise,circuit,programa,itinerario,diferencia,programm,differenz,fark,rozni,rozdil,razlik,diferent,verschil,skillnad,forskel,διαφορ,行程,区别,區別,違い,차이,perbezaan,perbedaan,ความต่าง,வித்தியாச,अंतर,فرق,განსხვ,chương trình,lịch trình,7 ngày,9 ngày,khác nhau",
    dt:"day trip,day trips,one day,same day,excursion,يوم واحد,اليوم الواحد,يوميه,однодн,экскурси,tagesaus,ausflug,journee,excursi,escursion,giornat,gunubirlik,jednodnio,jednoden,jednodnov,jednodnevn,izlet,o zi,dagtocht,dagstur,dagsutfl,dagstur,paivaret,ημερησι,εκδρομ,一日游,一日遊,日帰り,당일,sehari,satu hari,วันเดียว,หนึ่งวัน,ஒரு நாள்,एक दिन,ایک دن,یکروزه,یک روزه,ერთდღ,ექსკურს,tour trong ngày,trong ngày,một ngày",
    ap:"airport,pickup,pick up,transfer,مطار,استقبال,توصيل,аэропорт,трансфер,flughafen,abholung,aeroport,aeropuerto,aeroporto,havaliman,lotnisk,letist,letisk,zracn,luchthaven,lentoken,flygplats,lufthavn,flyplass,αεροδρομ,机场,機場,空港,공항,lapangan terbang,bandara,สนามบิน,விமான நிலைய,हवाई अड्डा,एयरपोर्ट,ایئرپورٹ,فرودگاه,აეროპორტ,sân bay,đón tại",
    wa:"whatsapp,واتس,واتساب,contact,phone,call,تواصل,اتصل,هاتف,رقم,связ,телефон,kontakt,telefon,contatt,iletisim,kontakti,επικοινων,联系,聯絡,連絡,연락,hubungi,ติดต่อ,தொடர்பு,संपर्क,رابطہ,تماس,კონტაქტ,liên hệ,điện thoại,số điện thoại,gọi",
    hi:"hello,hi,hey,مرحبا,السلام,اهلا,هلا,привет,здравств,hallo,bonjour,salut,hola,ciao,merhaba,selam,czesc,dzien dobry,dobry den,ahoj,zdravo,buna,hoi,hei,hej,γεια,你好,您好,こんにちは,안녕,halo,hai,สวัสดี,வணக்கம்,नमस्ते,سلام,გამარჯობ,ola",
    thx:"thank,thanks,thx,شكرا,مشكور,спасибо,danke,merci,gracias,grazie,tesekkur,sagol,dzieku,dekuj,dakuj,hvala,multum,bedankt,dank,kiitos,tack,takk,ευχαριστ,谢谢,謝謝,ありがとう,감사,고마,terima kasih,ขอบคุณ,நன்றி,धन्यवाद,شکریہ,ممنون,مرسی,მადლობ,obrigad,cảm ơn,cám ơn"
  };
  var INK = {}; for (var ik in IN) INK[ik] = IN[ik].split(",").map(norm).filter(Boolean);
  function intents(text) {
    var n = norm(text), toks = n.split(" "), out = {};
    for (var k in INK) {
      var L = INK[k];
      for (var i = 0; i < L.length; i++) {
        var w = L[i], hit = false;
        if (w.length >= 4 || DENSE.test(w) || w.indexOf(" ") >= 0) hit = n.indexOf(w) >= 0;
        else for (var j = 0; j < toks.length && !hit; j++) { var t0 = toks[j], t1 = t0.replace(/^(\u0648?[\u0628\u0641\u0643]?\u0627\u0644|\u0644\u0644|\u0648)/, ""); hit = (w.length <= 2 ? (t0 === w || t1 === w) : (t0.indexOf(w) === 0 || t1.indexOf(w) === 0)); }
        if (hit) { out[k] = 1; break; }
      }
    }
    return out;
  }

  /* ---------- Iraqi cities: road distances (approx., shortest route over main roads) ---------- */
  var CITY = {
    bgd:["بغداد","Baghdad","Багдад","Bagdad","Bağdat","Bagdá","Βαγδάτη","巴格达","バグダッド","바그다드","बगदाद","แบกแดด","பாக்தாத்","بغداد","ბაღდადი","Bagdád"],
    bsr:["البصرة","Basra","Басра","Basra","Basra","Bassorá","Βασόρα","巴士拉","バスラ","바스라","बसरा","บัสรา","பஸ்ரா","بصرہ","ბასრა","Bassora","Bassorah","بصره"],
    msl:["الموصل","Mosul","Мосул","Mossul","Musul","Mosul","Μοσούλη","摩苏尔","モースル","모술","मोसुल","โมซูล","மொசூல்","موصل","მოსული","Mossoul","Mosoul"],
    erb:["أربيل","Erbil","Эрбиль","Erbil","Erbil","Erbil","Ερμπίλ","埃尔比勒","アルビール","아르빌","एरबिल","เออร์บิล","எர்பில்","اربیل","ერბილი","Arbil","Irbil","Hewler","Hawler","اربيل","هولير"],
    kik:["كركوك","Kirkuk","Киркук","Kirkuk","Kerkük","Kirkuk","Κιρκούκ","基尔库克","キルクーク","키르쿠크","किरकुक","คีร์คูก","கிர்குக்","کرکوک","ქირქუქი"],
    sul:["السليمانية","Sulaymaniyah","Сулеймания","Sulaimaniyya","Süleymaniye","Sulaymaniyah","Σουλεϊμανίγια","苏莱曼尼亚","スレイマニヤ","술라이마니야","सुलेमानिया","สุไลมานียะห์","சுலைமானியா","سلیمانیہ","სულეიმანია","Slemani","Sulaimani","Souleimaniye","سلیمانیه","سليمانية"],
    dhk:["دهوك","Duhok","Дохук","Dohuk","Duhok","Duhok","Ντουχόκ","杜胡克","ドホーク","두후크","दुहोक","ดูฮอก","துஹோக்","دہوک","დუჰოკი","Dohuk","Dahuk","Dihok","دهوک"],
    zak:["زاخو","Zakho","Захо","Zakho","Zaho","Zakho","Ζάχο","扎胡","ザーホー","자코","ज़ाखो","ซาโค","சாக்கோ","زاخو","ზახო"],
    nja:["النجف","Najaf","Наджаф","Nadschaf","Necef","Najaf","Νατζάφ","纳杰夫","ナジャフ","나자프","नजफ़","นะญัฟ","நஜஃப்","نجف","ნაჯაფი","Nadjaf","Nedżef","Nadžaf","Nedžef"],
    krb:["كربلاء","Karbala","Кербела","Kerbela","Kerbela","Karbala","Καρμπάλα","卡尔巴拉","カルバラー","카르발라","कर्बला","กัรบะลาอ์","கர்பலா","کربلا","ქერბელა","Kerbala","Kerbala","Karbalā","كربلا"],
    hil:["الحلة","Hillah","Хилла","Hilla","Hille","Hilla","Χίλα","希拉","ヒッラ","힐라","हिल्ला","ฮิลละห์","ஹில்லா","حلہ","ჰილა","Hilla","Al-Hillah","حله"],
    bab:["بابل","Babylon","Вавилон","Babylon","Babil","Babilônia","Βαβυλώνα","巴比伦","バビロン","바빌론","बेबीलोन","บาบิโลน","பாபிலோன்","بابل","ბაბილონი","Babylone","Babilonia","Babilon","Babylón","Babil"],
    kut:["الكوت","Kut","Эль-Кут","Kut","Kut","Kut","Κουτ","库特","クート","쿠트","कूत","กูต","கூட்","کوت","კუტი","Al-Kut","Wasit","واسط"],
    ama:["العمارة","Amarah","Амара","Amara","Amare","Amara","Αμάρα","阿马拉","アマーラ","아마라","अमारा","อะมาเราะห์","அமாரா","عمارہ","ამარა","Al-Amarah","Maysan","ميسان","عماره"],
    nas:["الناصرية","Nasiriyah","Насирия","Nasiriya","Nasıriye","Nasiriyah","Νασιρίγια","纳西里耶","ナーシリーヤ","나시리야","नासिरिया","นาซีรียะห์","நசிரியா","ناصریہ","ნასირია","Nassiriya","Nasiriyya","Dhi Qar","ذي قار","ناصریه"],
    ur:["أور","Ur","Ур","Ur","Ur","Ur","Ουρ","乌尔","ウル","우르","उर","อูร์","ஊர்","اور","ური","زقورة أور","زقوره اور"],
    dwn:["الديوانية","Diwaniyah","Дивания","Diwaniya","Divaniye","Diwaniyah","Ντιουανίγια","迪瓦尼耶","ディワニヤ","디와니야","दीवानिया","ดีวานียะห์","திவானியா","دیوانیہ","დივანია","Al-Diwaniyah","Qadisiyyah","القادسية","ديوانيه","دیوانیه"],
    sam:["السماوة","Samawah","Самава","Samawa","Semave","Samawah","Σαμάουα","萨马沃","サマーワ","사마와","समावा","สะมาวะห์","சமாவா","سماوہ","სამავა","Al-Samawah","Muthanna","المثنى","سماوه"],
    rmd:["الرمادي","Ramadi","Рамади","Ramadi","Ramadi","Ramadi","Ραμάντι","拉马迪","ラマーディ","라마디","रमादी","รอมาดี","ரமாதி","رمادی","რამადი","Anbar","الانبار","الأنبار"],
    flj:["الفلوجة","Fallujah","Эль-Фаллуджа","Falludscha","Felluce","Faluya","Φαλούτζα","费卢杰","ファッルージャ","팔루자","फलूजा","ฟัลลูจะห์","ஃபலூஜா","فلوجہ","ფალუჯა","Fallouja","Faludża","Falluja","فلوجه","فالوجه"],
    bqb:["بعقوبة","Baqubah","Баакуба","Baquba","Bakuba","Baquba","Μπακούμπα","巴古拜","バアクーバ","바쿠바","बाकूबा","บะอ์กูบะห์","பகுபா","بعقوبہ","ბაკუბა","Ba'qubah","Diyala","ديالى","بعقوبه"],
    tik:["تكريت","Tikrit","Тикрит","Tikrit","Tikrit","Tikrit","Τικρίτ","提克里特","ティクリート","티크리트","तिकरित","ติกรีต","திக்ரித்","تکریت","თიქრითი","Salahuddin","صلاح الدين"],
    smr:["سامراء","Samarra","Самарра","Samarra","Samarra","Samarra","Σαμάρα","萨迈拉","サーマッラー","사마라","सामर्रा","ซามาร์รา","சாமர்ரா","سامرا","სამარა","Samara","سامرا"],
    hlb:["حلبجة","Halabja","Халабджа","Halabdscha","Halepçe","Halabja","Χαλάμπτζα","哈拉卜贾","ハラブジャ","할라브자","हलब्जा","ฮาลับจา","ஹலப்ஜா","حلبچہ","ჰალაბჯა","Halabdja","Halabdża","حلبچه"],
    kuf:["الكوفة","Kufa","Куфа","Kufa","Kufe","Kufa","Κούφα","库法","クーファ","쿠파","कूफ़ा","กูฟะห์","கூஃபா","کوفہ","კუფა","Koufa","Kūfa","کوفه"],
    chb:["الجبايش","Chibayish","Эль-Чибайиш","Chibayish","Çibayiş","Chibayish","Τσιμπαγίς","奇巴伊什","チバーイシュ","치바이시","चिबायिश","ชิบายิช","சிபாயிஷ்","چبایش","ჩიბაიში","Al-Chibayish","Marshes","الاهوار","الأهوار"],
    htr:["الحضر","Hatra","Хатра","Hatra","Hatra","Hatra","Χάτρα","哈特拉","ハトラ","하트라","हत्रा","ฮัตรา","ஹத்ரா","حضر","ჰატრა"]
  };
  /* road segments in km (main highways) */
  var ROAD = [["bgd","bqb",60],["bgd","rmd",110],["bgd","flj",65],["flj","rmd",50],["bgd","hil",100],["bgd","krb",105],["bgd","kut",175],["bgd","smr",125],
    ["smr","tik",55],["tik","msl",225],["tik","kik",115],["kik","erb",95],["kik","sul",115],["erb","msl",85],["erb","sul",170],["msl","dhk",75],["dhk","zak",60],
    ["bqb","kik",190],["hil","krb",45],["hil","nja",65],["krb","nja",80],["nja","kuf",10],["hil","kuf",60],["hil","dwn",85],["nja","dwn",70],["dwn","sam",95],
    ["sam","nas",115],["nas","bsr",190],["kut","ama",165],["ama","bsr",175],["kut","nas",185],["nas","chb",95],["chb","bsr",120],["sul","hlb",80],["hil","bab",5],["nas","ur",15],["msl","htr",110],["tik","htr",120]];
  var CN = {}, CA = [];
  var LI = {ar:0,en:1,ru:2,de:3,tr:4,pt:5,el:6,zh:7,"zh-tw":7,ja:8,ko:9,hi:10,th:11,ta:12,ur:13,ka:14};
  function cityNames() { for (var id in CITY) { var a = CITY[id], i = LI[LG]; CN[id] = i != null ? a[i] : (LG === "fa" ? (a[13] || a[0]) : a[1]); } }
  (function () {
    cityNames();
    for (var id in CITY) CITY[id].forEach(function (nm) { var n = norm(nm); if (n.length >= 2) CA.push([n, id]); });
    CA.sort(function (x, y) { return y[0].length - x[0].length; });
  })();
  function citiesIn(q) {
    var n = " " + norm(q) + " ", found = [], at = [];
    for (var i = 0; i < CA.length; i++) {
      var nm = CA[i][0], id = CA[i][1], p = -1, from = 0;
      while ((p = n.indexOf(nm, from)) >= 0) {
        var bef = n.slice(0, p), ok = /[\s]$/.test(bef) || /(^|\s)(و?[بفل]?|و)$/.test(bef);
        var aft = n.charAt(p + nm.length);
        if (DENSE.test(nm)) ok = true;
        if (ok && (DENSE.test(nm) || aft === " " || /^[اةيهةيa-z]?\s/.test(n.slice(p + nm.length, p + nm.length + 2)) || nm.length >= 5)) {
          if (found.indexOf(id) < 0) { found.push(id); at.push(p); }
          n = n.slice(0, p) + Array(nm.length + 1).join("#") + n.slice(p + nm.length); break;
        }
        from = p + 1;
      }
    }
    var o = found.map(function (id, k) { return [at[k], id]; }).sort(function (a, b) { return a[0] - b[0]; });
    return o.map(function (x) { return x[1]; });
  }
  function road(a, b) {
    var D = {}, done = {}; for (var id in CITY) D[id] = 1e9; D[a] = 0;
    for (;;) {
      var u = null; for (var k in D) if (!done[k] && (u === null || D[k] < D[u])) u = k;
      if (u === null || D[u] >= 1e9) break; if (u === b) break; done[u] = 1;
      ROAD.forEach(function (r) { var v = r[0] === u ? r[1] : r[1] === u ? r[0] : null; if (v && D[u] + r[2] < D[v]) D[v] = D[u] + r[2]; });
    }
    return D[b] < 1e9 ? D[b] : null;
  }
  var DT = {
    ar:"المسافة بالسيارة بين {a} و{b} تقريباً {k} كم، أي حوالي {h} بالسيارة.",
    en:"The road distance between {a} and {b} is about {k} km, roughly {h} by car.",
    ru:"Расстояние по дороге между городами {a} и {b} — около {k} км, примерно {h} на машине.",
    de:"Die Strecke zwischen {a} und {b} beträgt etwa {k} km, mit dem Auto rund {h}.",
    fr:"La distance par la route entre {a} et {b} est d'environ {k} km, soit environ {h} en voiture.",
    es:"La distancia por carretera entre {a} y {b} es de unos {k} km, aproximadamente {h} en coche.",
    it:"La distanza su strada tra {a} e {b} è di circa {k} km, circa {h} in auto.",
    tr:"{a} ile {b} arasındaki karayolu mesafesi yaklaşık {k} km, arabayla yaklaşık {h}.",
    pt:"A distância por estrada entre {a} e {b} é de cerca de {k} km, aproximadamente {h} de carro.",
    vi:"Quãng đường bộ giữa {a} và {b} khoảng {k} km, đi ô tô mất khoảng {h}.",
    fa:"فاصله زمینی بین {a} و {b} حدود {k} کیلومتر است، یعنی حدود {h} با خودرو.",
    ur:"{a} اور {b} کے درمیان سڑک کا فاصلہ تقریباً {k} کلومیٹر ہے، یعنی گاڑی سے تقریباً {h}۔"
  };
  var HR = {ar:["ساعة","ساعات"],en:["hour","hours"],ru:["часа","часов"],de:["Stunde","Stunden"],fr:["heure","heures"],es:["hora","horas"],it:["ora","ore"],tr:["saat","saat"],pt:["hora","horas"],vi:["giờ","giờ"],fa:["ساعت","ساعت"],ur:["گھنٹہ","گھنٹے"]};
  function hrs(km) {
    var h = Math.max(0.5, Math.round(km / 85 * 2) / 2), w = HR[LG];
    if (!w) return "≈ " + h + " h";
    if (LG === "ar") { var f = Math.floor(h), half = h !== f ? " ونصف" : "";
      return f === 0 ? "نصف ساعة" : f === 1 ? "ساعة" + half : f === 2 ? "ساعتين" + half : f + " " + (f <= 10 ? "ساعات" : "ساعة") + half; }
    return String(h).replace(".", LG === "en" ? "." : ",") + " " + (h <= 1 ? w[0] : w[1]);
  }
  function distAnswer(ids) {
    if (ids.length === 1) ids = ids[0] === "bgd" ? null : ["bgd", ids[0]];
    if (!ids) return false;
    var out = [];
    for (var i = 0; i + 1 < ids.length && i < 3; i++) {
      var a = ids[i], b = ids[i + 1], k = road(a, b); if (k == null) continue;
      k = Math.round(k / 5) * 5;
      var t = DT[LG];
      out.push(t ? t.replace("{a}", CN[a]).replace("{b}", CN[b]).replace("{k}", k).replace("{h}", hrs(k))
                 : CN[a] + " ↔ " + CN[b] + ": ≈ " + k + " km 🚗 " + hrs(k));
    }
    if (!out.length) return false;
    say(out.join("\n"));
    return true;
  }

  /* ---------- current time in Baghdad ---------- */
  var TT = {
    ar:"الوقت الآن في بغداد: {t}\n(توقيت العراق UTC+3، بدون توقيت صيفي)",
    en:"The time in Baghdad now is {t}\n(Iraq time, UTC+3, no daylight saving)",
    ru:"Сейчас в Багдаде {t}\n(время Ирака UTC+3, без перехода на летнее время)",
    de:"In Bagdad ist es jetzt {t}\n(irakische Zeit UTC+3, keine Sommerzeit)",
    fr:"Il est actuellement {t} à Bagdad\n(heure de l'Irak UTC+3, sans heure d'été)",
    es:"En Bagdad ahora son las {t}\n(hora de Irak UTC+3, sin horario de verano)",
    it:"A Baghdad ora sono le {t}\n(ora irachena UTC+3, senza ora legale)",
    tr:"Bağdat'ta şu an saat {t}\n(Irak saati UTC+3, yaz saati uygulaması yok)",
    pt:"Agora em Bagdá são {t}\n(hora do Iraque UTC+3, sem horário de verão)",
    vi:"Bây giờ ở Baghdad là {t}\n(giờ Iraq UTC+3, không đổi giờ mùa hè)",
    fa:"ساعت اکنون در بغداد: {t}\n(وقت عراق UTC+3، بدون ساعت تابستانی)",
    ur:"بغداد میں اس وقت: {t}\n(عراق کا وقت UTC+3، ڈے لائٹ سیونگ نہیں)"
  };
  var DIF = {ar:"الفرق عن توقيتك: {d} ساعة",en:"Difference from your time: {d} h",ru:"Разница с вашим временем: {d} ч",de:"Unterschied zu Ihrer Zeit: {d} Std.",fr:"Décalage avec votre heure : {d} h",es:"Diferencia con tu hora: {d} h",it:"Differenza con la tua ora: {d} h",tr:"Sizin saatinizle fark: {d} saat",pt:"Diferença para o seu horário: {d} h",vi:"Chênh lệch với giờ của bạn: {d} giờ"};
  function timeAnswer() {
    var loc = LG === "zh-tw" ? "zh-TW" : LG === "ar" ? "ar-IQ-u-nu-latn" : LG, t;
    try { t = new Intl.DateTimeFormat(loc, { timeZone: "Asia/Baghdad", weekday: "long", day: "numeric", month: "long", hour: "numeric", minute: "2-digit" }).format(new Date()); }
    catch (e) { var d = new Date(Date.now() + 3 * 3600e3); t = d.toISOString().slice(0, 16).replace("T", " "); }
    var s = TT[LG] ? TT[LG].replace("{t}", t) : "Baghdad 🕒 " + t + " (UTC+3)";
    var diff = 3 + new Date().getTimezoneOffset() / 60;
    if (diff !== 0) { var ds = (diff > 0 ? "+" : "") + diff; s += "\n" + (DIF[LG] ? DIF[LG].replace("{d}", ds) : "Δ " + ds + " h"); }
    say(s);
  }

  /* ---------- knowledge from the language home page ---------- */
  var KB = null, kbWait = [], KBC = {}, BKC = {};
  function txt(el) { return el ? el.textContent.replace(/\s+/g, " ").trim() : ""; }
  function build(doc, cur) {
    var kb = { faq: [], prog: [], dt: [], ap: null, bk: null, dtNote: "" }, seen = {};
    function addFaq(d) {
      d.querySelectorAll("#faq details").forEach(function (x) {
        var q = txt(x.querySelector("summary")), c = x.cloneNode(true); c.querySelector("summary").remove();
        var a = txt(c); if (!q || !a || seen[q]) return; seen[q] = 1;
        kb.faq.push({ q: q, a: a, gq: grams(norm(q)), ga: grams(norm(a)), tags: intents(q) });
      });
    }
    addFaq(doc); if (cur && cur !== doc) addFaq(cur);
    doc.querySelectorAll("section.prog").forEach(function (p) {
      kb.prog.push({ id: p.id, eb: txt(p.querySelector(".prog-head .eyebrow")), h: txt(p.querySelector(".prog-head h3, .prog-head h2")), r: txt(p.querySelector(".route")), se: txt(p.querySelector(".se")) });
    });
    kb.dtNote = txt(doc.querySelector("#day-trips .dt-note"));
    doc.querySelectorAll("#day-trips article.dt").forEach(function (a) {
      var k = a.getAttribute("data-trip");
      kb.dt.push({ k: k, h: txt(a.querySelector("h3")), s: txt(a.querySelector(".dt-s")), p: ((txt(a.querySelector(".dt-total b")).match(/\$\s?[\d,.]+/) || [""])[0]), url: HOME + "day-trips/" + (SL[k] || "") + "/" });
    });
    var ap = doc.querySelector("#airport-transfer");
    if (ap) {
      var lis = []; ap.querySelectorAll(".ap-inc li").forEach(function (l) { lis.push(txt(l)); });
      kb.ap = { h: txt(ap.querySelector(".ap-toggle b")), p: txt(ap.querySelector(".ap-in p")), li: lis, url: HOME + "airport-transfer/" };
    }
    var g = doc.querySelector("#guide .ft-guide");
    if (g) {
      var gp = g.querySelector("p"), gi = g.querySelector("img");
      kb.guide = { eb: txt(g.querySelector(".eyebrow")), h: txt(g.querySelector("h2, h3")), p: txt(gp), img: gi ? gi.getAttribute("src") : "" };
      kb.guide.w = words(kb.guide.h).concat(["saif","سيف","التميمي","tamimi","сайф","саиф","тамими","सैफ","サイフ","사이프","賽義夫","赛义夫","سیف"].map(norm));
    }
    var f = doc.querySelector("#interest");
    if (f) kb.bk = { h: txt(f.querySelector("h2")), p: txt(f.querySelector(".formcard p")) };
    /* place words: day-trip names + programme route stops (common words removed) */
    var cnt = {};
    kb.dt.forEach(function (d) {
      var u = {}; words(d.h + " " + d.s).forEach(function (w) { u[w] = 1; });
      d.h.split(/[\s,&·()]+/).forEach(function (w) { if (w.length >= 2 && w.length < 4 && STOP.indexOf(norm(w)) < 0 && (w.charAt(0) !== w.charAt(0).toLowerCase() || (/[\u0600-\u06FF]/.test(w) && norm(w).length === 3))) u[norm(w)] = 1; });
      d.w = Object.keys(u); d.w.forEach(function (w) { cnt[w] = (cnt[w] || 0) + 1; });
    });
    var ct = {}; kb.dt.forEach(function (d) { d.tw = {}; words(d.h).forEach(function (w) { if (!d.tw[w]) { d.tw[w] = 1; ct[w] = (ct[w] || 0) + 1; } }); });
    kb.dt.forEach(function (d) { var hn = norm(d.h); d.w = d.w.filter(function (w) { return cnt[w] <= 2 && (!ct[w] || ct[w] <= 1 || hn === w); }); });
    kb.prog.forEach(function (p) { p.w = p.r.split(/[·,•|]/).map(function (x) { return norm(x); }).filter(function (x) { return x.length >= 2; }); });
    return kb;
  }
  var STOP = ["the","and","die","der","das","den","dem","des","les","los","las","el","la","le","il","lo","gli","de","del","du","di","da","do","och","og","en","et","und","van","het","een","von","ve","al","ile","na","ze","za","od","do","i","a","o","e","y","u","z","w","and","of","to","ja","och"];
  function strip(t) { return t.replace(/^(\u0648?[\u0628\u0641\u0643]?\u0627\u0644|\u0644\u0644)/, ""); }
  function has(n, w) {
    if (DENSE.test(w) || w.indexOf(" ") >= 0) return n.indexOf(w) >= 0;
    if (w.length >= 4 && n.indexOf(w) >= 0) return true;
    if ((" " + n + " ").indexOf(" " + w + " ") >= 0) return true;
    var a = strip(w); if (a.length < 4) return false;
    var tk = n.split(" ");
    for (var i = 0; i < tk.length; i++) {
      var b = strip(tk[i]); if (b.length < 4) continue;
      var m = Math.min(a.length, b.length), p = 0; while (p < m && a.charAt(p) === b.charAt(p)) p++;
      if (p >= Math.max(4, m - 1)) return true;
    }
    return false;
  }
  function words(s) { return norm(s).split(" ").filter(function (w) { return DENSE.test(w) ? w.length >= 2 : w.length >= 4; }); }
  function loadKB(cb) {
    if (KB) return cb(KB);
    kbWait.push(cb); if (kbWait.length > 1) return;
    var lg0 = LG; function done(doc) { KB = KBC[lg0] = build(doc, lg0 === PG ? document : null); var w = kbWait; kbWait = []; w.forEach(function (f) { f(KB); }); }
    var here = location.pathname.replace(/index\.html$/, "");
    if (here === HOME) return done(document);
    if (lg0 !== PG) { fetch(HOME).then(function (r) { return r.text(); }).then(function (h) { done(new DOMParser().parseFromString(h, "text/html")); }).catch(function () { kbWait = []; setLang(PG); loadKB(cb); }); return; }
    fetch(HOME, { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (h) {
      done(new DOMParser().parseFromString(h, "text/html"));
    }).catch(function () { done(document); });
  }

  /* ---------- blog knowledge (every article of this language, /blog-kb/<lang>.json) ---------- */
  var BK = null, bkWait = [];
  var RD = { ar:"اقرأ المقال كاملاً", ckb:"هەموو بابەتەکە بخوێنەوە", en:"Read the full article", ru:"Читать статью полностью", de:"Ganzen Artikel lesen", fr:"Lire l'article complet", es:"Leer el artículo completo", it:"Leggi l'articolo completo", tr:"Yazının tamamını okuyun", fa:"خواندن کامل مقاله", ur:"پورا مضمون پڑھیں", pl:"Przeczytaj cały artykuł", nl:"Lees het hele artikel", pt:"Ler o artigo completo", cs:"Přečíst celý článek", sk:"Prečítať celý článok", hr:"Pročitajte cijeli članak", ro:"Citește articolul complet", el:"Διαβάστε όλο το άρθρο", fi:"Lue koko artikkeli", sv:"Läs hela artikeln", da:"Læs hele artiklen", no:"Les hele artikkelen", ka:"სრული სტატიის წაკითხვა", zh:"阅读全文", "zh-tw":"閱讀全文", ja:"記事を全文読む", ko:"전체 글 읽기", ms:"Baca artikel penuh", id:"Baca artikel lengkap", th:"อ่านบทความฉบับเต็ม", hi:"पूरा लेख पढ़ें", ta:"முழு கட்டுரையைப் படிக்க", vi:"Đọc toàn bộ bài viết" };
  var RDT = RD[LG] || RD.en;
  /* question words that say nothing about the subject */
  var QW = "who,was,were,is,are,did,does,do,can,the,an,how much,what,where,when,which,whom,whose,wer,war,ist,sind,hat,qui,est,etait,quien,era,chi,kto,был,была,это,هل,كان,كانت,tell,about,explain,know,information,please,there,their,this,that,with,from,have,does,story,history,iraq,visit,ماهي,ماهو,اريد,اعرف,معلومات,احكيلي,حدثني,اخبرني,عن,ما,هي,هو,من,شنو,شني,شو,وين,اين,متى,كيف,ليش,لماذا,قصه,قصة,تاريخ,العراق,عراق,زياره,زيارة,что,такое,кто,такой,расскажи,расскажите,про,где,когда,история,ирак,erzahl,erzahlen,etwas,uber,wann,geschichte,irak,qu est,quoi,parle,moi,histoire,parlame,raccontami,storia,cuentame,sobre,historia,nedir,kimdir,hakkinda,tarihi,nedir".split(",").map(norm);
  function loadBK(cb) {
    if (BK) return cb(BK);
    bkWait.push(cb); if (bkWait.length > 1) return;
    function done(j) {
      BK = (j || []).map(function (p) {
        var id = p.t + " " + p.h + " " + p.p + " " + p.k;
        return { p: p, idn: norm(id), ttl: norm(p.t + " " + p.h + " " + p.p), all: norm(id + " " + p.s.map(function (x) { return x[0] + " " + x[1]; }).join(" ") + " " + p.q.map(function (x) { return x.join(" "); }).join(" ")),
          sec: p.s.map(function (x) { return { h: norm(x[0]), t: norm(x[1]) }; }), fq: p.q.map(function (x) { return grams(norm(x[0])); }) };
      });
      BKC[LG] = BK; var w = bkWait; bkWait = []; w.forEach(function (f) { f(BK); });
    }
    if (!window.fetch) return done([]);
    fetch("/blog-kb/" + LG + ".json").then(function (r) { return r.ok ? r.json() : []; }).then(done).catch(function () { done([]); });
  }
  function qTokens(n) {
    return n.split(" ").filter(function (w) {
      if (QW.indexOf(w) >= 0 || STOP.indexOf(w) >= 0) return false;
      return w.length >= 2;
    });
  }
  function blogFind(q) {
    if (!BK || !BK.length) return null;
    var n = norm(q), tk = qTokens(n); if (!tk.length) return null;
    var df = {}; tk.forEach(function (w) { df[w] = 0; BK.forEach(function (b) { if (has(b.all, w)) df[w]++; }); });
    var best = null, bs = 0;
    BK.forEach(function (b) {
      var strong = 0, sc = 0, hitId = [];
      tk.forEach(function (w) {
        if (!df[w]) return;
        var idf = 1 / df[w];
        if (has(b.ttl, w)) { strong++; sc += 4 * idf; hitId.push(w); }
        else if (has(b.idn, w)) { strong++; sc += 2 * idf; }
        else if (has(b.all, w)) sc += idf;
      });
      /* whole phrase of the question found in the title / keywords */
      for (var i = 0; i + 1 < tk.length; i++) { var ph = tk[i] + " " + tk[i + 1]; if (b.ttl.indexOf(ph) >= 0) sc += 2; else if (b.idn.indexOf(ph) >= 0) sc += 1; }
      if (strong && sc > bs) { bs = sc; best = { b: b, rest: tk.filter(function (w) { return hitId.indexOf(w) < 0; }), n: n }; }
    });
    return bs >= 1 ? best : null;
  }
  function cut(t, max) {
    if (t.length <= max) return t;
    var c = t.slice(0, max), i = Math.max(c.lastIndexOf(". "), c.lastIndexOf("。"), c.lastIndexOf(".\n"), c.lastIndexOf("\n"), c.lastIndexOf("؟ "), c.lastIndexOf("! "));
    return (i > max * 0.5 ? c.slice(0, i + 1) : c) + " …";
  }
  function blogAnswer(hit) {
    var b = hit.b, p = b.p, gq = grams(hit.n);
    /* 1) one of the article's own FAQ questions */
    var fb = -1, fs = 0; b.fq.forEach(function (g, i) { var fqn = norm(p.q[i][0]); if (hit.rest.length && !hit.rest.some(function (w) { return has(fqn, w); })) return; var c = Math.min(contain(gq, g), contain(g, gq)); if (c > fs) { fs = c; fb = i; } });
    /* 2) the section that best matches the rest of the question */
    var si = 0, ss = 0;
    if (hit.rest.length) b.sec.forEach(function (x, i) {
      var c = 0; hit.rest.forEach(function (w) { if (has(x.h, w)) c += 2; else if (has(x.t, w)) c += 1; }); if (c > ss) { ss = c; si = i; }
    });
    if (ss < 2) { si = 0; ss = 0; }
    /* a section heading that is (almost) the question itself, e.g. "What is the Ishtar Gate?" */
    var hs = 0, hi = -1; b.sec.forEach(function (x, i) { if (!i) return; var hg = grams(x.h), c = Math.min(contain(hg, gq), contain(gq, hg) + 0.15); if (c > hs) { hs = c; hi = i; } });
    if (hs >= 0.75 && hs >= fs) { si = hi; ss = 3; }
    var c = el("div", "ftb-card ftb-blog");
    if (p.c) c.appendChild(el("small")).textContent = p.c;
    if (fs >= 0.6 && ss < 3) {
      c.appendChild(el("b")).textContent = p.q[fb][0];
      c.appendChild(el("p")).textContent = p.q[fb][1];
    } else {
      var s = p.s[si] || p.s[0];
      c.appendChild(el("b")).textContent = s ? s[0] : p.t;
      if (s) c.appendChild(el("p")).textContent = cut(s[1], 1400);
      if (si === 0 && p.f && p.f.length) { var u = el("ul"); p.f.forEach(function (f) { u.appendChild(el("li")).textContent = f[0] + ": " + f[1]; }); c.appendChild(u); }
    }
    var a = el("a"); a.href = p.u; a.textContent = RDT + " →"; c.appendChild(a);
    M.appendChild(c); scroll();
  }

  /* ---------- UI ---------- */
  var css = ".ftb-blog p{white-space:pre-line}.ftb-blog ul{margin-top:8px}.ftb-l{position:fixed;inset-inline-start:18px;bottom:20px;z-index:31;width:56px;height:56px;border-radius:50%;border:0;background:var(--navy,#1B2A47);color:var(--gold,#B8955A);display:grid;place-items:center;cursor:pointer;box-shadow:0 0 0 2px var(--gold,#B8955A),0 8px 22px rgba(27,42,71,.35);transition:transform .2s}" +
    ".ftb-l:hover{transform:scale(1.06)}.ftb-l svg{width:27px;height:27px}" +
    ".ftb-l.wa-up{bottom:88px}" +
    ".ftb-tip{position:fixed;inset-inline-start:84px;z-index:31;background:#fff;color:var(--navy,#1B2A47);font-family:inherit;font-weight:600;font-size:14px;line-height:1.3;padding:9px 14px;border-radius:18px;box-shadow:0 6px 20px rgba(27,42,71,.25);border:1px solid var(--gold,#B8955A);cursor:pointer;opacity:0;transform:translateY(6px);transition:opacity .3s,transform .3s;pointer-events:none;white-space:nowrap}" +
    ".ftb-tip.on{opacity:1;transform:none;pointer-events:auto}" +
    ".ftb{position:fixed;inset-inline-start:18px;bottom:18px;z-index:60;width:380px;max-width:calc(100vw - 24px);height:min(600px,calc(100vh - 36px));height:min(600px,calc(100dvh - 36px));background:var(--paper,#FAF8F3);border-radius:14px;box-shadow:0 24px 70px rgba(10,18,34,.45);display:flex;flex-direction:column;overflow:hidden;border-top:4px solid var(--gold,#B8955A);font-size:15px;line-height:1.6;color:var(--ink,#1F2733)}" +
    ".ftb[hidden]{display:none}" +
    ".ftb-h{background:var(--navy,#1B2A47);color:#fff;display:flex;align-items:center;gap:10px;padding:12px 14px}" +
    ".ftb-h img{width:36px;height:36px;border-radius:50%;border:2px solid var(--gold,#B8955A);background:#fff}" +
    ".ftb-h b{flex:1;font-size:15.5px;font-weight:700;color:#EFE3C8}" +
    ".ftb-x{background:none;border:0;color:#EFE3C8;width:34px;height:34px;border-radius:50%;cursor:pointer;display:grid;place-items:center}.ftb-x:hover{background:rgba(255,255,255,.1)}" +
    ".ftb-m{flex:1;overflow-y:auto;padding:14px 12px;display:flex;flex-direction:column;gap:10px;overscroll-behavior:contain}" +
    ".ftb-b{max-width:88%;padding:10px 13px;border-radius:14px;white-space:pre-line;word-wrap:break-word}" +
    ".ftb-bot{align-self:flex-start;background:#fff;border:1px solid rgba(27,42,71,.1);border-start-start-radius:4px}" +
    ".ftb-me{align-self:flex-end;background:var(--navy,#1B2A47);color:#fff;border-start-end-radius:4px}" +
    ".ftb-c{display:flex;flex-wrap:wrap;gap:7px;align-self:flex-start;max-width:100%}" +
    ".ftb-ch{border:1px solid var(--gold,#B8955A);background:#fff;color:var(--navy,#1B2A47);font:inherit;font-size:13.5px;font-weight:600;padding:7px 12px;border-radius:18px;cursor:pointer;text-decoration:none;line-height:1.35;text-align:start}" +
    ".ftb-ch:hover{background:var(--gold,#B8955A);color:var(--navy,#1B2A47)}" +
    ".ftb-ch.wa{background:#25D366;border-color:#25D366;color:#fff}.ftb-ch.wa:hover{background:#1fb457}" +
    ".ftb-card{align-self:stretch;background:#fff;border:1px solid rgba(27,42,71,.1);border-inline-start:3px solid var(--gold,#B8955A);border-radius:8px;padding:10px 12px}" +
    ".ftb-card .ftb-av{float:inline-start;width:72px;height:72px;border-radius:50%;object-fit:cover;border:2px solid var(--gold,#B8955A);margin-inline-end:12px;margin-bottom:4px}" +
    ".ftb-card small{display:block;color:var(--gold,#B8955A);font-weight:700;font-size:12px;letter-spacing:.03em}" +
    ".ftb-card b{display:block;color:var(--navy,#1B2A47);font-size:15px;line-height:1.4}" +
    ".ftb-card p{margin:3px 0 0;font-size:13.5px;color:var(--muted,#5b6475)}" +
    ".ftb-card .pr{color:var(--navy,#1B2A47);font-weight:700;font-size:14px}" +
    ".ftb-card a{display:inline-block;margin-top:6px;color:var(--navy-2,#2A3D63);font-weight:700;font-size:13.5px}" +
    ".ftb-card ul{margin:6px 0 0;padding-inline-start:18px;font-size:13.5px}" +
    ".ftb-f{display:flex;gap:8px;padding:10px;border-top:1px solid rgba(27,42,71,.1);background:#fff}" +
    ".ftb-f input{flex:1;min-width:0;border:1px solid rgba(27,42,71,.2);border-radius:22px;padding:10px 15px;font:inherit;font-size:16px;background:var(--paper,#FAF8F3);color:inherit}" +
    ".ftb-f input:focus{outline:2px solid var(--gold,#B8955A);outline-offset:0;border-color:transparent}" +
    ".ftb-f button{width:44px;height:44px;border-radius:50%;border:0;background:var(--gold,#B8955A);color:var(--navy,#1B2A47);cursor:pointer;display:grid;place-items:center;flex:none}" +
    "[dir=rtl] .ftb-f button svg{transform:scaleX(-1)}" +
    ".ftb-dots{display:inline-flex;gap:4px}.ftb-dots i{width:7px;height:7px;border-radius:50%;background:#9aa3b2;animation:ftbd 1s infinite}.ftb-dots i:nth-child(2){animation-delay:.15s}.ftb-dots i:nth-child(3){animation-delay:.3s}" +
    "@keyframes ftbd{0%,60%,100%{opacity:.3}30%{opacity:1}}" +
    "@media (max-width:560px){.ftb{inset:auto 0 0 0;width:100%;max-width:100%;height:88vh;height:88dvh;border-radius:16px 16px 0 0}.ftb-tip{display:none}}" +
    "@media (prefers-reduced-motion:reduce){.ftb-l,.ftb-tip{transition:none}.ftb-dots i{animation:none}}";
  var IC_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12z"/><path d="M8.5 10.2h7M8.5 13.8h4.5"/></svg>';
  var IC_X = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  var IC_SEND = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg>';

  var L, tip, P, M, I, lastQ = "";
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function waUrl(q) { return "https://wa.me/" + WA + (q ? "?text=" + encodeURIComponent(q) : ""); }
  function scroll() { M.scrollTop = M.scrollHeight; }
  function say(text, me) { var b = el("div", "ftb-b " + (me ? "ftb-me" : "ftb-bot")); b.textContent = text; M.appendChild(b); scroll(); return b; }
  function chips(list) {
    var c = el("div", "ftb-c");
    list.forEach(function (x) {
      var b;
      if (x.href) { b = el("a", "ftb-ch" + (x.wa ? " wa" : "")); b.href = x.href; if (x.wa) { b.target = "_blank"; b.rel = "noopener"; b.addEventListener("click", function () { logBot("whatsapp", lastQ); }); } else if (/^tel:/.test(x.href)) b.addEventListener("click", function () { logBot("call", x.t); }); else b.addEventListener("click", function (e) { logBot("link", x.t); go(e, x.href); }); }
      else { b = el("button", "ftb-ch"); b.type = "button"; b.addEventListener("click", function () { logBot("topic", x.t); }); b.addEventListener("click", x.fn); }
      b.textContent = x.t; c.appendChild(b);
    });
    M.appendChild(c); scroll();
  }
  function card(o) {
    var c = el("div", "ftb-card");
    if (o.img) { var im = el("img", "ftb-av"); im.src = o.img; im.alt = o.title || ""; im.width = 72; im.height = 72; c.appendChild(im); }
    if (o.small) c.appendChild(el("small")).textContent = o.small;
    c.appendChild(el("b")).textContent = o.title;
    if (o.text) c.appendChild(el("p")).textContent = o.text;
    if (o.price) { var p = el("p", "pr"); p.textContent = o.price; c.appendChild(p); }
    if (o.list && o.list.length) { var u = el("ul"); o.list.forEach(function (t) { u.appendChild(el("li")).textContent = t; }); c.appendChild(u); }
    if (o.href) { var a = el("a"); a.href = o.href; a.textContent = T.open + " →"; a.addEventListener("click", function (e) { go(e, o.href); }); c.appendChild(a); }
    M.appendChild(c); scroll();
  }
  /* same-page links: open the section instead of reloading */
  function go(e, href) {
    var u; try { u = new URL(href, location.href); } catch (x) { return; }
    var here = location.pathname.replace(/index\.html$/, "");
    if (u.pathname === here && u.hash) {
      e.preventDefault(); openSection(u.hash.slice(1));
      if (window.innerWidth <= 560) close();
    }
  }
  function openSection(id) {
    var s = document.getElementById(id); if (!s) return;
    var t = s.querySelector(".dt-toggle[aria-expanded=false],.ap-toggle[aria-expanded=false]");
    if (t) t.click();
    s.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function menu() {
    var m = [{ t: T.prog, fn: function () { me(T.prog); topicProg(); } }];
    if (KB && KB.dt.length) m.push({ t: T.dt, fn: function () { me(T.dt); topicDt(); } });
    if (KB && KB.ap) m.push({ t: T.ap, fn: function () { me(T.ap); topicAp(); } });
    if (KB && KB.faq.length) m.push({ t: T.faq, fn: function () { me(T.faq); topicFaq(); } });
    m.push({ t: T.bk, fn: function () { me(T.bk); topicBk(); } });
    m.push({ t: T.wa, href: waUrl(""), wa: 1 });
    var cc = callChip(); if (cc) m.push(cc);
    chips(m);
  }
  function callChip() {
    var a = document.querySelector("a.us-call"); if (!a) return null;
    return { t: "📞 " + a.textContent.replace(/\s+/g, " ").trim().replace(/^(.*?)(\+1)/, "$1 $2").replace(/\s+/g, " "), href: a.getAttribute("href") };
  }
  function after(q) { chips([{ t: T.more, fn: function () { me(T.more); menu(); } }, { t: T.wa, href: waUrl(q || ""), wa: 1 }]); }
  function me(t) { say(t, true); }

  function topicProg(skipAfter) {
    KB.prog.forEach(function (p) { card({ small: p.eb, title: p.h, text: p.r, price: p.se, href: HOME + "#" + p.id }); });
    if (!skipAfter) after("");
  }
  function dtCard(d) { card({ title: d.h, text: d.s, price: d.p ? d.p + " · " + T.one : "", href: d.url }); }
  function topicDt(list) {
    if (!list && KB.dtNote) say(KB.dtNote);
    (list || KB.dt).forEach(dtCard);
    after("");
  }
  function topicGuide() {
    var g = KB.guide; card({ img: g.img, small: g.eb, title: g.h, text: g.p, href: HOME + "#guide" });
  }
  function topicAp() {
    var a = KB.ap; if (!a) return nf("");
    card({ title: a.h, text: a.p, list: a.li, href: a.url });
    after("");
  }
  function topicFaq() {
    var c = KB.faq.map(function (f) { return { t: f.q, fn: function () { me(f.q); say(f.a); after(f.q); } }; });
    chips(c);
  }
  function topicBk() {
    if (KB.bk && KB.bk.p) say(KB.bk.p);
    var formHere = document.getElementById("interest");
    chips([{ t: T.form, href: formHere ? location.pathname + "#interest" : HOME + "#interest" }, { t: T.wa, href: waUrl(""), wa: 1 }]);
  }
  function nf(q) { say(T.nf); var c = [{ t: T.wa, href: waUrl(q), wa: 1 }], cc = callChip(); if (cc) c.push(cc); c.push({ t: T.more, fn: function () { me(T.more); menu(); } }); chips(c); }

  function answer(q) {
    var it = intents(q), n = norm(q), gq = grams(n), shown = 0;
    var keys = Object.keys(it).filter(function (k) { return k !== "hi" && k !== "thx" && k !== "who" && k !== "spk" && k !== "inc2"; });
    if (!keys.length && it.thx) { say(T.thx); return after(""); }
    if (!keys.length && it.hi && n.split(" ").length <= 4) { say(T.hi); return menu(); }
    var cs = citiesIn(q);
    if (it.dist && !it.ap) { if (distAnswer(cs)) return after(q); return nf(q); }
    if (it.time && !it.dist) { timeAnswer(); return after(q); }
    if (KB.guide && (KB.guide.w.some(function (w) { return w && has(n, w); }) || (it.who && !it.spk && !it.price && (it.lang || /guide|مرشد|دليل|гид|reiseleit|guid|rehber|przewodn|pruvod|vodi|ghid|gids|opas|ξεναγ|导游|導遊|ガイド|가이드|pemandu|ไกด์|गाइड|راهنما|گائیڈ|გიდ/.test(n))))) { topicGuide(); return after(q); }
    if (it.ap) { topicAp(); return; }
    /* flights: always "yes, on request" (after the FAQ answer when asking if they are included) */
    if (it.fly) {
      if (it.inc2) { var fi = KB.faq.filter(function (f) { return f.tags.fly || f.tags.incl; })[0]; if (fi) say(fi.a); }
      say(T.svc); return after(q);
    }
    /* blog articles: places, people, events the blog has written about */
    if (!it.price && !it.book && !it.visa && !it.cancel && !it.pay && !it.group && !it.incl && !it.safe && !it.dt && !it.svc && !it.prog) {
      var bh = blogFind(q);
      if (bh) {
        blogAnswer(bh);
        var pl = norm(bh.b.p.p || "");
        var tr1 = KB.dt.map(function (d) { var c = 0; d.w.forEach(function (w) { if (pl && has(pl, w)) c++; }); return { d: d, c: c }; }).filter(function (x) { return x.c; }).sort(function (a, b) { return b.c - a.c; });
        if (tr1.length) dtCard(tr1[0].d);
        return after(q);
      }
    }
    /* places: day trips / programme stops named in the question */
    var trips = KB.dt.map(function (d) { var c = 0; d.w.forEach(function (w) { if (has(n, w)) c++; }); return { d: d, c: c }; })
      .filter(function (x) { return x.c; }).sort(function (a, b) { return b.c - a.c; }).map(function (x) { return x.d; });
    var progs = KB.prog.filter(function (p) { return p.w.some(function (w) { return has(n, w); }); });
    if (/(^| )(7|9|٧|٩|seven|nine|سبع|تسع)( |$)/.test(n) && !trips.length) { topicProg(); return; }
    if (it.dt && !trips.length) { topicDt(); return; }
    /* best FAQ */
    var best = null, bs = 0;
    KB.faq.forEach(function (f) {
      var ov = 0; for (var k in f.tags) if (it[k] && k !== "hi" && k !== "thx") ov++;
      var ex = 0; for (var k2 in f.tags) if (!it[k2]) ex++;
      var tq = contain(gq, f.gq), sc = ov * 2 - 1.0 * ex + tq + 0.5 * contain(gq, f.ga);
      if ((ov > 0 || tq >= 0.5) && sc > bs) { bs = sc; best = f; }
    });
    if (bs < 0.9) best = null;
    /* any other service the visitor asks for: "yes, on request" */
    if (it.svc && !it.dt && !it.visa && !it.cancel && !it.pay && !it.safe && !it.price && !it.prog && !it.group && !it.lang && !trips.length && !(best && bs >= 2)) { say(T.svc); return after(q); }
    var priceOnly = best && Object.keys(best.tags).length === 1 && best.tags.price;
    if (best && !(trips.length && (priceOnly || it.dt))) { say(best.a); shown++; }
    if (trips.length && (it.dt || it.price || !best || trips.length <= 3)) { trips.slice(0, 4).forEach(dtCard); shown++; }
    else if (progs.length && !best) { progs.forEach(function (p) { card({ small: p.eb, title: p.h, text: p.r, price: p.se, href: HOME + "#" + p.id }); }); shown++; }
    if (!shown && it.svc) { say(T.svc); return after(q); }
    if (!shown && it.book) { topicBk(); return; }
    if (!shown && it.prog) { topicProg(); return; }
    if (!shown && it.wa) { chips([{ t: T.wa, href: waUrl(q), wa: 1 }]); return; }
    if (!shown) return nf(q);
    after(q);
  }

  /* ---------- answer in the language of the question ---------- */
  function setLang(l) {
    if (l === LG && KB) return;
    LG = l; HOME = l === "ar" ? "/" : "/" + l + "/";
    if (l === PG) { for (var k in T0) T[k] = T0[k]; } else { setT(); T.svc = SV[l] || SV.en; }
    RDT = RD[l] || RD.en; cityNames();
    KB = KBC[l] || null; kbWait = []; BK = BKC[l] || null; bkWait = [];
  }
  var LW = {
    en:"the,is,are,what,how,much,does,do,can,you,where,when,which,i,my,want,visit,safe,cost,price,there,need,have,from,please,hello,hi,thanks,many,days,trip,go",
    de:"ich,ist,wie,was,viel,kostet,der,die,das,und,gibt,es,sie,wann,reise,nicht,kann,mit,ein,eine,wir,gibt's,hallo,danke,welche,wo",
    fr:"je,est,le,la,les,combien,coûte,coute,quel,quelle,vous,pour,une,des,du,et,comment,voyage,prix,bonjour,merci,peut,faut,où,ou,c'est,quels",
    es:"el,la,los,las,cuánto,cuanto,cuesta,qué,que,es,hay,cómo,como,para,viaje,precio,y,hola,gracias,puedo,dónde,donde,cuál,son,un,una",
    it:"il,lo,gli,quanto,costa,che,è,come,per,viaggio,prezzo,sono,una,della,e,ciao,grazie,posso,dove,quale,quali,del,un",
    pt:"o,os,quanto,custa,você,voce,é,como,para,viagem,preço,preco,uma,não,nao,do,da,e,olá,ola,obrigado,posso,onde,qual,são,um",
    nl:"de,het,een,wat,hoe,kost,is,ik,reis,prijs,van,en,niet,zijn,hallo,bedankt,kan,waar,welke,veel",
    sv:"vad,hur,kostar,jag,är,och,en,det,resa,pris,inte,hej,tack,kan,var,vilken,mycket",
    da:"hvad,hvordan,koster,jeg,er,og,en,det,rejse,pris,ikke,hej,tak,kan,hvor,hvilken,meget",
    no:"hva,hvordan,koster,jeg,er,og,en,det,reise,pris,ikke,hei,takk,kan,hvor,hvilken,mye",
    fi:"mitä,mita,paljonko,kuinka,onko,ja,on,matka,hinta,mikä,mika,voiko,hei,kiitos,missä,missa,kauanko",
    pl:"ile,kosztuje,jak,czy,jest,co,wycieczka,cena,nie,i,dzień,dobry,dziękuję,gdzie,można,który",
    cs:"kolik,stojí,stoji,jak,je,co,zájezd,zajezd,cena,a,není,dobrý,den,děkuji,kde,lze,který",
    sk:"koľko,kolko,stojí,ako,je,čo,zájazd,cena,nie,dobrý,ďakujem,kde,ktorý",
    hr:"koliko,košta,kosta,kako,je,što,sto,putovanje,cijena,i,bok,hvala,gdje,mogu,koji",
    ro:"cât,cat,costă,costa,cum,este,ce,excursie,preț,pret,și,si,bună,mulțumesc,unde,care,pot",
    tr:"ne,kadar,nasıl,nasil,mı,mi,mu,mü,var,fiyat,fiyatı,nedir,için,icin,merhaba,teşekkür,nerede,hangi,kaç,kac,ve,güvenli,guvenli,ücret,ucret,tur,turu,gezi",
    id:"berapa,harga,apa,bagaimana,saya,ini,itu,ada,untuk,dan,bisa,kapan,tidak,perjalanan,halo,terima,kasih,di,mana,yang",
    ms:"berapa,harga,apa,bagaimana,saya,ini,itu,ada,untuk,dan,boleh,bila,tidak,lawatan,helo,terima,kasih,di,mana,yang,berapakah,awak",
    vi:"giá,bao,nhiêu,không,có,là,tôi,của,và,được,đi,ngày,xin,chào,cảm,ơn,ở,đâu,nào,bạn,toàn,những,cho,với,này,người,gì,sao,thế,khi,mấy,muốn,xem,đến,mất,nhiều,tiền,chuyến,thì,hay"
  };
  var LWS = {}; for (var lw in LW) LWS[lw] = LW[lw].split(",");
  var LCH = { vi:/[ơưđạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]/g, tr:/[ğış]/g, pl:/[ąęłńśźż]/g, cs:/[ěřů]/g, sk:/[ľĺŕôä]/g, ro:/[ășțşţâî]/g,
    hr:/[đćčšž]/g, de:/[ßäöü]/g, da:/[æøå]/g, no:/[æøå]/g, sv:/[åäö]/g, fi:/[äö]/g, pt:/[ãõçáéêó]/g, es:/[ñ¿¡áéíóú]/g, fr:/[çèêëœàùûîé]/g, it:/[àèéìòù]/g };
  function detect(q) {
    var s = String(q || "").toLowerCase();
    if (/[가-힯]/.test(s)) return "ko";
    if (/[぀-ヿ]/.test(s)) return "ja";
    if (/[一-鿿]/.test(s)) {
      var tw = (s.match(/[這們麼嗎來時說會為與發現對點價錢遊覽飯館個機場導買賣車開關門問題]/g) || []).length,
          cn = (s.match(/[这们么吗来时说会为与发现对点价钱游览饭馆个机场导买卖车开关门问题]/g) || []).length;
      return tw > cn ? "zh-tw" : cn > tw ? "zh" : (PG === "zh-tw" || PG === "zh" ? PG : "zh");
    }
    if (/[฀-๿]/.test(s)) return "th";
    if (/[஀-௿]/.test(s)) return "ta";
    if (/[ऀ-ॿ]/.test(s)) return "hi";
    if (/[Ⴀ-ჿ]/.test(s)) return "ka";
    if (/[Ͱ-Ͽ]/.test(s)) return "el";
    if (/[Ѐ-ӿ]/.test(s)) return "ru";
    if (/[؀-ۿ]/.test(s)) {
      if (/[ڕڵۆێەڤ]/.test(s)) return "ckb";
      if (/[ےٹڈڑںۓ]/.test(s)) return "ur";
      var fa = (s.match(/[یکپژ]/g) || []).length + (/(^|\s)(است|می|چه|چقدر|چطور|آیا|هست|برای|را)(\s|$)/.test(s) ? 2 : 0),
          ar = (s.match(/[يكةى]/g) || []).length + (/(^|\s)(ال|هل|كم|ما|ماذا|كيف|هي|هو|في|على|من|شنو|شكد)/.test(s) ? 1 : 0);
      if (fa > ar) return PG === "ur" ? "ur" : "fa";
      if (ar > fa) return "ar";
      return ["ar", "fa", "ur", "ckb"].indexOf(PG) >= 0 ? PG : "ar";
    }
    if (!/[a-zà-ỹ]/.test(s)) return null;
    var tk = s.replace(/[^\p{L}\p{N}' ]/gu, " ").split(/\s+/).filter(Boolean), sc = {}, best = null, b1 = 0, b2 = 0;
    for (var l in LWS) {
      var c = 0;
      tk.forEach(function (w) { if (LWS[l].indexOf(w) >= 0) c += 1.5; });
      if (LCH[l]) c += Math.min(2, (s.match(LCH[l]) || []).length);
      sc[l] = c;
    }
    LCH.vi.lastIndex = 0; if (sc.vi >= 3 || (sc.vi >= 1.5 && LCH.vi.test(s))) return "vi";
    for (var l2 in sc) { if (sc[l2] > b1) { b2 = b1; b1 = sc[l2]; best = l2; } else if (sc[l2] > b2) b2 = sc[l2]; }
    if (!best || b1 < 2) return null;
    /* two close languages (ms/id, da/no, es/pt…): answer in the page language (Saif) */
    if ((best === "ms" || best === "id") && Math.abs(sc.ms - sc.id) < 1.5) return PG;
    /* close calls between related languages: keep the page / current language when it is one of them */
    if (b1 - b2 < 1) return PG;
    return best;
  }

  function send() {
    var q = I.value.trim(); if (!q) return;
    I.value = ""; me(q); lastQ = q; logBot("question", q);
    var dl = detect(q); if (dl && LANGS.concat("ar").indexOf(dl) >= 0 && dl !== LG) setLang(dl);
    var d = say(""); d.innerHTML = '<span class="ftb-dots"><i></i><i></i><i></i></span>';
    loadKB(function () { loadBK(function () { setTimeout(function () { d.remove(); answer(q); }, 350); }); });
  }

  var started = false;
  function open() {
    P.hidden = false; L.setAttribute("aria-expanded", "true"); hideTip();
    if (!started) {
      started = true; say(T.hi); logBot("open", document.referrer ? document.referrer.split("/")[2] || "" : "");
      var d = say(""); d.innerHTML = '<span class="ftb-dots"><i></i><i></i><i></i></span>';
      loadKB(function () { d.remove(); menu(); });
    }
    if (window.innerWidth > 560) setTimeout(function () { I.focus(); }, 50);
  }
  function close() { P.hidden = true; L.setAttribute("aria-expanded", "false"); L.focus({ preventScroll: true }); }
  function hideTip() { if (tip) tip.classList.remove("on"); }

  function init() {
    var st = el("style"); st.id = "ftb-css"; st.textContent = css; document.head.appendChild(st);
    var hasWa = !!document.querySelector(".wa-float,.wa-fab");
    L = el("button", "ftb-l" + (hasWa ? " wa-up" : ""), IC_CHAT);
    L.type = "button"; L.setAttribute("aria-label", T.t); L.setAttribute("aria-expanded", "false"); L.setAttribute("aria-controls", "ftb");
    L.addEventListener("click", function () { P.hidden ? open() : close(); });
    tip = el("div", "ftb-tip"); tip.textContent = T.q; tip.style.bottom = hasWa ? "98px" : "30px";
    tip.addEventListener("click", open);
    P = el("div", "ftb"); P.id = "ftb"; P.hidden = true; P.setAttribute("role", "dialog"); P.setAttribute("aria-label", T.t);
    var h = el("div", "ftb-h"); var lg = el("img"); lg.src = "/logo.png"; lg.alt = ""; lg.width = 36; lg.height = 36;
    h.appendChild(lg); h.appendChild(el("b")).textContent = T.t;
    var x = el("button", "ftb-x", IC_X); x.type = "button"; x.setAttribute("aria-label", T.close); x.addEventListener("click", close); h.appendChild(x);
    M = el("div", "ftb-m"); M.setAttribute("aria-live", "polite");
    var f = el("form", "ftb-f"); I = el("input"); I.type = "text"; I.placeholder = T.ph; I.setAttribute("aria-label", T.ph); I.maxLength = 300; I.autocomplete = "off";
    var sb = el("button", null, IC_SEND); sb.type = "submit"; sb.setAttribute("aria-label", T.send);
    f.appendChild(I); f.appendChild(sb); f.addEventListener("submit", function (e) { e.preventDefault(); send(); });
    P.appendChild(h); P.appendChild(M); P.appendChild(f);
    document.body.appendChild(L); document.body.appendChild(tip); document.body.appendChild(P);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !P.hidden) close(); });
    /* small "Have a question?" hint, once per visit */
    var shown = false; try { shown = sessionStorage.getItem("ftb-tip") === "1"; } catch (e) {}
    if (!shown && window.innerWidth > 560) setTimeout(function () {
      if (!P.hidden) return; tip.classList.add("on");
      try { sessionStorage.setItem("ftb-tip", "1"); } catch (e) {}
      setTimeout(hideTip, 9000);
    }, 6000);
    /* opening a section from a bot link on another page (#day-trips / #airport-transfer) */
    if (/^#(day-trips|airport-transfer)$/.test(location.hash)) setTimeout(function () { openSection(location.hash.slice(1)); }, 400);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
