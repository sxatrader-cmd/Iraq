/* Fable Tour – Iraq site Q&A assistant (no server, no API, free).
   Knowledge is read from the visitor's language home page (FAQ, programs,
   day trips, airport transfer, booking), so answers always match the site. */
(function () {
  "use strict";
  if (window.__ftBot) return; window.__ftBot = 1;

  var WA = "9647711745353";
  var LANGS = ["zh-tw","cs","da","de","el","en","es","fa","fi","fr","hi","hr","id","it","ja","ka","ko","ms","nl","no","pl","pt","ro","ru","sk","sv","ta","th","tr","ur","zh"];
  var SL = {"ziyara":"baghdad-holy-shrines","oldtown":"baghdad-old-town","aqarquf":"aqar-quf","madain":"al-madain-ctesiphon","samarra":"samarra","babylon":"babylon","babylon4":"babylon-borsippa-kifl","holy":"kufa-najaf-karbala","south":"ur-marshes"};

  var seg = (location.pathname.split("/")[1] || "").toLowerCase();
  var LG = LANGS.indexOf(seg) >= 0 ? seg : "ar";
  var HOME = LG === "ar" ? "/" : "/" + LG + "/";

  /* ---------- interface text (32 languages) ---------- */
  var K = ["t","hi","ph","nf","wa","more","prog","dt","ap","faq","bk","one","open","q","thx","send","close","form"];
  var S = {
    ar:["مساعد Fable Tour","أهلاً بك! أجيبك عن أسئلتك حول رحلاتنا في العراق. اختر موضوعاً أو اكتب سؤالك.","اكتب سؤالك…","لم أجد إجابة لهذا السؤال. راسلنا على واتساب وسنرد عليك بسرعة.","تواصل عبر واتساب","مواضيع أخرى","البرامج والأسعار","رحلات اليوم الواحد","الاستقبال من المطار","أسئلة شائعة","احجز رحلتك","لشخص واحد","التفاصيل","عندك سؤال؟","العفو! هل تريد شيئاً آخر؟","إرسال","إغلاق","افتح نموذج الحجز"],
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
    pt:["Assistente Fable Tour","Olá! Respondo às suas perguntas sobre os nossos circuitos no Iraque. Escolha um tema ou escreva a sua pergunta.","Escreva a sua pergunta…","Não encontrei resposta para essa pergunta. Escreva-nos pelo WhatsApp e respondemos rapidamente.","Falar pelo WhatsApp","Outros temas","Programas e preços","Passeios de um dia","Recolha no aeroporto","Perguntas frequentes","Reservar a viagem","para 1 pessoa","Detalhes","Tem uma pergunta?","De nada! Mais alguma coisa?","Enviar","Fechar","Abrir o formulário de reserva"]
  };
  var T = {}; (function () { var a = S[LG] || S.en; for (var i = 0; i < K.length; i++) T[K[i]] = a[i]; })();

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
    price:"price,prices,cost,how much,usd,dollar,euro,$,€,سعر,اسعار,الاسعار,كلفه,تكلفه,بكم,كم السعر,قيمه,цен,стоим,сколько,preis,kost,prix,cout,combien,tarif,precio,cuesta,cuanto,prezz,costo,quanto,fiyat,ucret,ne kadar,cena,ceny,koszt,kosztuj,stoji,cijen,koliko,pret,prijs,hinta,maksaa,pris,koster,kostar,preco,τιμ,κοστ,价格,价钱,多少钱,费用,價格,費用,料金,値段,いくら,가격,얼마,비용,harga,berapa,ราคา,เท่าไ,விலை,कीमत,कितन,قیمت,کتنا,هزینه,چند,ფას,ღირ",
    visa:"visa,viza,visum,vize,виз,فيز,تاشير,ویزا,ويزا,ویزہ,ვიზ,签证,簽證,ビザ,비자,วีซ,விசா,वीज़ा,वीजा,βιζα,θεωρησ",
    cancel:"cancel,annul,отмен,الغاء,الغي,storn,zrus,odwol,anul,iptal,cancela,annull,otkaz,peruu,avbok,afbestil,ακυρ,取消,キャンセル,취소,batal,ยกเลิก,ரத்து,रद्द,منسوخ,لغو,გაუქმ,refund,استرجاع,возврат",
    pay:"pay,paying,ادفع,payment,deposit,دفع,عربون,مقدم,оплат,предоплат,депозит,zahl,anzahl,paiement,payer,acompte,pago,pagar,deposito,pagament,acconto,odeme,depozit,platb,zaloh,plat,zaliczk,placan,avans,betal,aanbetal,maksu,ennakko,depositum,πληρω,προκαταβολ,付款,定金,支付,訂金,支払,前金,결제,보증금,bayar,ชำระ,มัดจำ,கட்டண,भुगतान,ادائیگی,پرداخت,بیعانه,گادا,გადახდ",
    safe:"safe,safety,secur,danger,امان,امن,خطر,безопас,опасн,sicher,gefahr,securi,segur,sicur,pericol,guven,tehlike,bezpieczn,niebezpie,bezpecn,sigur,veilig,turvall,saker,sikker,ασφαλ,κινδυν,安全,危险,危險,안전,위험,aman,bahaya,ปลอดภัย,อันตราย,பாதுகாப்,सुरक्षित,محفوظ,امنیت,ایمن,უსაფრთხ",
    lang:"language,speak,guide,english,russian,لغه,لغات,مرشد,دليل,يتكلم,язык,гид,говор,sprach,sprich,reiseleiter,langue,parle,idioma,habla,guia,lingu,parla,dil,rehber,konus,jezyk,przewodnik,jazyk,pruvodc,sprievodc,vodic,limb,ghid,taal,gids,kieli,opas,sprak,sprog,γλωσσ,ξεναγ,语言,導遊,导游,語言,言語,ガイド,언어,가이드,bahasa,pemandu,ภาษา,ไกด์,மொழி,வழிகாட்ட,भाषा,गाइड,زبان,گائیڈ,راهنما,ენა,გიდ",
    group:"private,group,join,departure,خاص,جماعي,مجموعه,انطلاق,индивидуал,групп,privat,gruppe,abfahrt,prive,groupe,depart,privad,grupo,salida,gruppo,partenz,ozel,grup,kalkis,prywat,grupow,soukrom,skupin,sukrom,groep,vertrek,yksityi,ryhma,grupp,ιδιωτ,ομαδ,私人,团队,團體,プライベート,グループ,개인,단체,pribadi,rombongan,persendirian,kumpulan,ส่วนตัว,กลุ่ม,தனிப்பட்ட,குழு,निजी,समूह,پرائیویٹ,گروپ,خصوصی,گروه,კერძო,ჯგუფ",
    incl:"includ,flight,flights,meals,طيران,تذاكر,يشمل,شامل,وجبات,включ,перел,авиабил,inklusiv,flug,inclu,vol,vuelo,volo,compres,dahil,ucak,wliczon,zahrn,ukljuc,inbegrepen,vlucht,sisalt,lento,ingar,flyg,inkluder,περιλαμβ,πτησ,包含,包括,机票,機票,含まれ,航空券,포함,항공,termasuk,penerbangan,รวม,เที่ยวบิน,அடங்கும,விமானம்,शामिल,उड़ान,پرواز,ჩათვლ,ფრენ",
    book:"book,booking,reserv,حجز,احجز,брон,buch,prenot,rezerv,boek,varaa,varaus,bestil,boka,κρατ,预订,預訂,予約,예약,tempah,pesan,จอง,முன்பதிவு,बुक,بک,رزرو,დაჯავშ",
    prog:"program,programs,itinerar,difference,7 day,9 day,برنامج,برامج,البرنامجين,الفرق,مسار,программ,маршрут,отлича,unterschied,rundreise,circuit,programa,itinerario,diferencia,programm,differenz,fark,rozni,rozdil,razlik,diferent,verschil,skillnad,forskel,διαφορ,行程,区别,區別,違い,차이,perbezaan,perbedaan,ความต่าง,வித்தியாச,अंतर,فرق,განსხვ",
    dt:"day trip,day trips,one day,same day,excursion,يوم واحد,اليوم الواحد,يوميه,однодн,экскурси,tagesaus,ausflug,journee,excursi,escursion,giornat,gunubirlik,jednodnio,jednoden,jednodnov,jednodnevn,izlet,o zi,dagtocht,dagstur,dagsutfl,dagstur,paivaret,ημερησι,εκδρομ,一日游,一日遊,日帰り,당일,sehari,satu hari,วันเดียว,หนึ่งวัน,ஒரு நாள்,एक दिन,ایک دن,یکروزه,یک روزه,ერთდღ,ექსკურს",
    ap:"airport,pickup,pick up,transfer,مطار,استقبال,توصيل,аэропорт,трансфер,flughafen,abholung,aeroport,aeropuerto,aeroporto,havaliman,lotnisk,letist,letisk,zracn,luchthaven,lentoken,flygplats,lufthavn,flyplass,αεροδρομ,机场,機場,空港,공항,lapangan terbang,bandara,สนามบิน,விமான நிலைய,हवाई अड्डा,एयरपोर्ट,ایئرپورٹ,فرودگاه,აეროპორტ",
    wa:"whatsapp,واتس,واتساب,contact,phone,call,تواصل,اتصل,هاتف,رقم,связ,телефон,kontakt,telefon,contatt,iletisim,kontakti,επικοινων,联系,聯絡,連絡,연락,hubungi,ติดต่อ,தொடர்பு,संपर्क,رابطہ,تماس,კონტაქტ",
    hi:"hello,hi,hey,مرحبا,السلام,اهلا,هلا,привет,здравств,hallo,bonjour,salut,hola,ciao,merhaba,selam,czesc,dzien dobry,dobry den,ahoj,zdravo,buna,hoi,hei,hej,γεια,你好,您好,こんにちは,안녕,halo,hai,สวัสดี,வணக்கம்,नमस्ते,سلام,გამარჯობ,ola",
    thx:"thank,thanks,thx,شكرا,مشكور,спасибо,danke,merci,gracias,grazie,tesekkur,sagol,dzieku,dekuj,dakuj,hvala,multum,bedankt,dank,kiitos,tack,takk,ευχαριστ,谢谢,謝謝,ありがとう,감사,고마,terima kasih,ขอบคุณ,நன்றி,धन्यवाद,شکریہ,ممنون,مرسی,მადლობ,obrigad"
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

  /* ---------- knowledge from the language home page ---------- */
  var KB = null, kbWait = [];
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
    var f = doc.querySelector("#interest");
    if (f) kb.bk = { h: txt(f.querySelector("h2")), p: txt(f.querySelector(".formcard p")) };
    /* place words: day-trip names + programme route stops (common words removed) */
    var cnt = {};
    kb.dt.forEach(function (d) {
      var u = {}; words(d.h + " " + d.s).forEach(function (w) { u[w] = 1; });
      d.h.split(/[\s,&·()]+/).forEach(function (w) { if (w.length >= 2 && w.length < 4 && w.charAt(0) !== w.charAt(0).toLowerCase() && STOP.indexOf(norm(w)) < 0) u[norm(w)] = 1; });
      d.w = Object.keys(u); d.w.forEach(function (w) { cnt[w] = (cnt[w] || 0) + 1; });
    });
    kb.dt.forEach(function (d) { d.w = d.w.filter(function (w) { return cnt[w] <= 2; }); });
    kb.prog.forEach(function (p) { p.w = p.r.split(/[·,•|]/).map(function (x) { return norm(x); }).filter(function (x) { return x.length >= 2; }); });
    return kb;
  }
  var STOP = ["the","and","die","der","das","den","dem","des","les","los","las","el","la","le","il","lo","gli","de","del","du","di","da","do","och","og","en","et","und","van","het","een","von","ve","al","ile","na","ze","za","od","do","i","a","o","e","y","u","z","w","and","of","to","ja","och"];
  function has(n, w) {
    if (DENSE.test(w) || w.length >= 4 || w.indexOf(" ") >= 0) return n.indexOf(w) >= 0;
    return (" " + n + " ").indexOf(" " + w + " ") >= 0;
  }
  function words(s) { return norm(s).split(" ").filter(function (w) { return DENSE.test(w) ? w.length >= 2 : w.length >= 4; }); }
  function loadKB(cb) {
    if (KB) return cb(KB);
    kbWait.push(cb); if (kbWait.length > 1) return;
    function done(doc) { KB = build(doc, document); var w = kbWait; kbWait = []; w.forEach(function (f) { f(KB); }); }
    var here = location.pathname.replace(/index\.html$/, "");
    if (here === HOME) return done(document);
    fetch(HOME, { credentials: "same-origin" }).then(function (r) { return r.text(); }).then(function (h) {
      done(new DOMParser().parseFromString(h, "text/html"));
    }).catch(function () { done(document); });
  }

  /* ---------- UI ---------- */
  var css = ".ftb-l{position:fixed;inset-inline-start:18px;bottom:20px;z-index:31;width:56px;height:56px;border-radius:50%;border:0;background:var(--navy,#1B2A47);color:var(--gold,#B8955A);display:grid;place-items:center;cursor:pointer;box-shadow:0 0 0 2px var(--gold,#B8955A),0 8px 22px rgba(27,42,71,.35);transition:transform .2s}" +
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
      if (x.href) { b = el("a", "ftb-ch" + (x.wa ? " wa" : "")); b.href = x.href; if (x.wa) { b.target = "_blank"; b.rel = "noopener"; } else b.addEventListener("click", function (e) { go(e, x.href); }); }
      else { b = el("button", "ftb-ch"); b.type = "button"; b.addEventListener("click", x.fn); }
      b.textContent = x.t; c.appendChild(b);
    });
    M.appendChild(c); scroll();
  }
  function card(o) {
    var c = el("div", "ftb-card");
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
    chips(m);
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
  function nf(q) { say(T.nf); chips([{ t: T.wa, href: waUrl(q), wa: 1 }, { t: T.more, fn: function () { me(T.more); menu(); } }]); }

  function answer(q) {
    var it = intents(q), n = norm(q), gq = grams(n), shown = 0;
    var keys = Object.keys(it).filter(function (k) { return k !== "hi" && k !== "thx"; });
    if (!keys.length && it.thx) { say(T.thx); return after(""); }
    if (!keys.length && it.hi && n.split(" ").length <= 4) { say(T.hi); return menu(); }
    if (it.ap) { topicAp(); return; }
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
    var priceOnly = best && Object.keys(best.tags).length === 1 && best.tags.price;
    if (best && !(trips.length && (priceOnly || it.dt))) { say(best.a); shown++; }
    if (trips.length && (it.dt || it.price || !best || trips.length <= 3)) { trips.slice(0, 4).forEach(dtCard); shown++; }
    else if (progs.length && !best) { progs.forEach(function (p) { card({ small: p.eb, title: p.h, text: p.r, price: p.se, href: HOME + "#" + p.id }); }); shown++; }
    if (!shown && it.book) { topicBk(); return; }
    if (!shown && it.prog) { topicProg(); return; }
    if (!shown && it.wa) { chips([{ t: T.wa, href: waUrl(q), wa: 1 }]); return; }
    if (!shown) return nf(q);
    after(q);
  }

  function send() {
    var q = I.value.trim(); if (!q) return;
    I.value = ""; me(q); lastQ = q;
    var d = say(""); d.innerHTML = '<span class="ftb-dots"><i></i><i></i><i></i></span>';
    loadKB(function () { setTimeout(function () { d.remove(); answer(q); }, 350); });
  }

  var started = false;
  function open() {
    P.hidden = false; L.setAttribute("aria-expanded", "true"); hideTip();
    if (!started) {
      started = true; say(T.hi);
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
