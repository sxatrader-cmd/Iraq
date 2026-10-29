#!/usr/bin/env python3
"""Adds the 'Baghdad Airport pickup & hotel transfer' section (collapsed until clicked)
after the day-trips section on every language homepage. Idempotent.

Price (USD, per car, one car for every 3 travellers) — shown only after the guest
picks arrival date AND time:
  arrival 10:00–19:59  -> $75 per car
  arrival 20:00–09:59  -> $125 per car
Run add_euro.py afterwards (it converts the shown price on EU-language pages)."""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DAY, NIGHT, PER_CAR, MAXP = 75, 125, 3, 9
IMG = "/img/airport-pickup-baghdad.webp"

K = ["eye", "h", "show", "hide", "p", "i1", "i2", "i3", "i4", "date", "time", "trav", "hotel", "flight",
     "hint", "total", "night", "book", "wa", "big", "alt"]
S = {
"en": ["Airport transfer", "Baghdad Airport pickup & hotel transfer", "Show details", "Hide details",
 "We meet you in the arrivals hall at Baghdad International Airport and drive you in a private car straight to your hotel in Baghdad.",
 "Meet & greet in the arrivals hall", "Private air-conditioned car", "Help with your luggage", "Drop-off at your hotel in Baghdad",
 "Arrival date", "Arrival time (local)", "Travellers", "Hotel (optional)", "Flight number (optional)",
 "Choose your arrival date and time to see the price.", "Total price", "Night rate for arrivals between 8 pm and 10 am",
 "Book on WhatsApp", "Hello! I'd like to book a pickup at Baghdad International Airport with transfer to my hotel. Arrival: {date} at {time}, {n} travellers.{extra} Price: {price}.",
 "More than 9 travellers? Message us on WhatsApp.", "Fable Tour guide waiting for guests in the arrivals hall at Baghdad International Airport"],
"ar": ["الاستقبال في المطار", "الاستقبال في مطار بغداد الدولي والتوصيل إلى الفندق", "عرض التفاصيل", "إخفاء التفاصيل",
 "نستقبلك في صالة القادمين في مطار بغداد الدولي ونوصلك بسيارة خاصة مباشرة إلى فندقك في بغداد.",
 "الاستقبال في صالة القادمين", "سيارة خاصة مكيّفة", "المساعدة في حمل الأمتعة", "التوصيل إلى فندقك في بغداد",
 "تاريخ الوصول", "وقت الوصول (بتوقيت بغداد)", "عدد المسافرين", "الفندق (اختياري)", "رقم الرحلة (اختياري)",
 "اختر تاريخ ووقت وصولك ليظهر السعر.", "السعر الإجمالي", "سعر ليلي للوصول بين الساعة 8 مساءً و10 صباحاً",
 "احجز عبر واتساب", "مرحباً! أرغب بحجز استقبال في مطار بغداد الدولي والتوصيل إلى الفندق. الوصول: {date} الساعة {time}، عدد المسافرين {n}.{extra} السعر: {price}.",
 "أكثر من 9 مسافرين؟ راسلنا على واتساب.", "مرشد Fable Tour بانتظار الضيوف في صالة القادمين في مطار بغداد الدولي"],
"ru": ["Трансфер из аэропорта", "Встреча в аэропорту Багдада и трансфер в отель", "Подробнее", "Скрыть",
 "Мы встретим вас в зале прилёта международного аэропорта Багдада и отвезём на частном автомобиле прямо в ваш отель в Багдаде.",
 "Встреча в зале прилёта", "Частный автомобиль с кондиционером", "Помощь с багажом", "Доставка до вашего отеля в Багдаде",
 "Дата прилёта", "Время прилёта (местное)", "Путешественники", "Отель (необязательно)", "Номер рейса (необязательно)",
 "Выберите дату и время прилёта, чтобы увидеть цену.", "Итоговая цена", "Ночной тариф для прилётов с 20:00 до 10:00",
 "Забронировать в WhatsApp", "Здравствуйте! Хочу заказать встречу в международном аэропорту Багдада и трансфер в отель. Прилёт: {date} в {time}, путешественников: {n}.{extra} Цена: {price}.",
 "Больше 9 человек? Напишите нам в WhatsApp.", "Гид Fable Tour встречает гостей в зале прилёта международного аэропорта Багдада"],
"de": ["Flughafentransfer", "Abholung am Flughafen Bagdad & Transfer zum Hotel", "Details anzeigen", "Details ausblenden",
 "Wir empfangen Sie in der Ankunftshalle des Internationalen Flughafens Bagdad und bringen Sie im privaten Wagen direkt zu Ihrem Hotel in Bagdad.",
 "Empfang in der Ankunftshalle", "Privates klimatisiertes Fahrzeug", "Hilfe mit dem Gepäck", "Fahrt bis zu Ihrem Hotel in Bagdad",
 "Ankunftsdatum", "Ankunftszeit (Ortszeit)", "Reisende", "Hotel (optional)", "Flugnummer (optional)",
 "Wählen Sie Datum und Uhrzeit Ihrer Ankunft, um den Preis zu sehen.", "Gesamtpreis", "Nachttarif für Ankünfte zwischen 20 und 10 Uhr",
 "Per WhatsApp buchen", "Hallo! Ich möchte eine Abholung am Internationalen Flughafen Bagdad mit Transfer zum Hotel buchen. Ankunft: {date} um {time}, {n} Reisende.{extra} Preis: {price}.",
 "Mehr als 9 Reisende? Schreiben Sie uns auf WhatsApp.", "Fable-Tour-Guide erwartet Gäste in der Ankunftshalle des Internationalen Flughafens Bagdad"],
"fr": ["Transfert aéroport", "Accueil à l'aéroport de Bagdad et transfert à l'hôtel", "Voir les détails", "Masquer les détails",
 "Nous vous accueillons dans le hall des arrivées de l'aéroport international de Bagdad et vous conduisons en voiture privée jusqu'à votre hôtel à Bagdad.",
 "Accueil dans le hall des arrivées", "Voiture privée climatisée", "Aide pour les bagages", "Dépose à votre hôtel à Bagdad",
 "Date d'arrivée", "Heure d'arrivée (locale)", "Voyageurs", "Hôtel (facultatif)", "Numéro de vol (facultatif)",
 "Choisissez la date et l'heure d'arrivée pour voir le prix.", "Prix total", "Tarif de nuit pour les arrivées entre 20 h et 10 h",
 "Réserver sur WhatsApp", "Bonjour ! Je souhaite réserver un accueil à l'aéroport international de Bagdad avec transfert à mon hôtel. Arrivée : {date} à {time}, {n} voyageurs.{extra} Prix : {price}.",
 "Plus de 9 voyageurs ? Écrivez-nous sur WhatsApp.", "Guide Fable Tour attendant des voyageurs dans le hall des arrivées de l'aéroport international de Bagdad"],
"es": ["Traslado al aeropuerto", "Recogida en el aeropuerto de Bagdad y traslado al hotel", "Ver detalles", "Ocultar detalles",
 "Te recibimos en la sala de llegadas del Aeropuerto Internacional de Bagdad y te llevamos en coche privado directamente a tu hotel en Bagdad.",
 "Recepción en la sala de llegadas", "Coche privado con aire acondicionado", "Ayuda con el equipaje", "Traslado hasta tu hotel en Bagdad",
 "Fecha de llegada", "Hora de llegada (local)", "Viajeros", "Hotel (opcional)", "Número de vuelo (opcional)",
 "Elige la fecha y la hora de llegada para ver el precio.", "Precio total", "Tarifa nocturna para llegadas entre las 20:00 y las 10:00",
 "Reservar por WhatsApp", "¡Hola! Quiero reservar una recogida en el Aeropuerto Internacional de Bagdad con traslado a mi hotel. Llegada: {date} a las {time}, {n} viajeros.{extra} Precio: {price}.",
 "¿Más de 9 viajeros? Escríbenos por WhatsApp.", "Guía de Fable Tour esperando a los viajeros en la sala de llegadas del Aeropuerto Internacional de Bagdad"],
"it": ["Transfer aeroporto", "Accoglienza all'aeroporto di Baghdad e transfer in hotel", "Mostra dettagli", "Nascondi dettagli",
 "Ti accogliamo nella sala arrivi dell'Aeroporto Internazionale di Baghdad e ti accompagniamo in auto privata direttamente al tuo hotel a Baghdad.",
 "Accoglienza nella sala arrivi", "Auto privata con aria condizionata", "Aiuto con i bagagli", "Arrivo al tuo hotel a Baghdad",
 "Data di arrivo", "Ora di arrivo (locale)", "Viaggiatori", "Hotel (facoltativo)", "Numero del volo (facoltativo)",
 "Scegli data e ora di arrivo per vedere il prezzo.", "Prezzo totale", "Tariffa notturna per arrivi tra le 20:00 e le 10:00",
 "Prenota su WhatsApp", "Ciao! Vorrei prenotare l'accoglienza all'Aeroporto Internazionale di Baghdad con transfer in hotel. Arrivo: {date} alle {time}, {n} viaggiatori.{extra} Prezzo: {price}.",
 "Più di 9 viaggiatori? Scrivici su WhatsApp.", "Guida Fable Tour in attesa dei viaggiatori nella sala arrivi dell'Aeroporto Internazionale di Baghdad"],
"el": ["Μεταφορά από το αεροδρόμιο", "Υποδοχή στο αεροδρόμιο της Βαγδάτης και μεταφορά στο ξενοδοχείο", "Δείτε λεπτομέρειες", "Απόκρυψη λεπτομερειών",
 "Σας υποδεχόμαστε στην αίθουσα αφίξεων του Διεθνούς Αεροδρομίου της Βαγδάτης και σας μεταφέρουμε με ιδιωτικό αυτοκίνητο κατευθείαν στο ξενοδοχείο σας στη Βαγδάτη.",
 "Υποδοχή στην αίθουσα αφίξεων", "Ιδιωτικό κλιματιζόμενο αυτοκίνητο", "Βοήθεια με τις αποσκευές", "Μεταφορά στο ξενοδοχείο σας στη Βαγδάτη",
 "Ημερομηνία άφιξης", "Ώρα άφιξης (τοπική)", "Ταξιδιώτες", "Ξενοδοχείο (προαιρετικό)", "Αριθμός πτήσης (προαιρετικό)",
 "Επιλέξτε ημερομηνία και ώρα άφιξης για να δείτε την τιμή.", "Συνολική τιμή", "Νυχτερινή χρέωση για αφίξεις από 20:00 έως 10:00",
 "Κράτηση μέσω WhatsApp", "Γεια σας! Θα ήθελα να κλείσω υποδοχή στο Διεθνές Αεροδρόμιο της Βαγδάτης με μεταφορά στο ξενοδοχείο. Άφιξη: {date} στις {time}, {n} ταξιδιώτες.{extra} Τιμή: {price}.",
 "Πάνω από 9 ταξιδιώτες; Γράψτε μας στο WhatsApp.", "Ξεναγός της Fable Tour περιμένει ταξιδιώτες στην αίθουσα αφίξεων του Διεθνούς Αεροδρομίου της Βαγδάτης"],
"cs": ["Transfer z letiště", "Vyzvednutí na letišti v Bagdádu a odvoz do hotelu", "Zobrazit podrobnosti", "Skrýt podrobnosti",
 "Přivítáme vás v příletové hale Mezinárodního letiště Bagdád a soukromým autem vás odvezeme přímo do vašeho hotelu v Bagdádu.",
 "Přivítání v příletové hale", "Soukromé klimatizované auto", "Pomoc se zavazadly", "Odvoz až k vašemu hotelu v Bagdádu",
 "Datum příletu", "Čas příletu (místní)", "Cestující", "Hotel (nepovinné)", "Číslo letu (nepovinné)",
 "Vyberte datum a čas příletu a zobrazí se cena.", "Celková cena", "Noční sazba pro přílety mezi 20:00 a 10:00",
 "Rezervovat přes WhatsApp", "Dobrý den! Chci si objednat vyzvednutí na Mezinárodním letišti Bagdád s odvozem do hotelu. Přílet: {date} v {time}, počet cestujících: {n}.{extra} Cena: {price}.",
 "Více než 9 cestujících? Napište nám na WhatsApp.", "Průvodce Fable Tour čeká na hosty v příletové hale Mezinárodního letiště Bagdád"],
"pl": ["Transfer z lotniska", "Odbiór z lotniska w Bagdadzie i transfer do hotelu", "Pokaż szczegóły", "Ukryj szczegóły",
 "Witamy Cię w hali przylotów Międzynarodowego Portu Lotniczego Bagdad i zawozimy prywatnym samochodem prosto do Twojego hotelu w Bagdadzie.",
 "Powitanie w hali przylotów", "Prywatny klimatyzowany samochód", "Pomoc z bagażem", "Dowóz do Twojego hotelu w Bagdadzie",
 "Data przylotu", "Godzina przylotu (lokalna)", "Podróżni", "Hotel (opcjonalnie)", "Numer lotu (opcjonalnie)",
 "Wybierz datę i godzinę przylotu, aby zobaczyć cenę.", "Cena całkowita", "Stawka nocna dla przylotów między 20:00 a 10:00",
 "Zarezerwuj przez WhatsApp", "Dzień dobry! Chcę zarezerwować odbiór z Międzynarodowego Portu Lotniczego Bagdad z transferem do hotelu. Przylot: {date} o {time}, liczba osób: {n}.{extra} Cena: {price}.",
 "Więcej niż 9 osób? Napisz do nas na WhatsApp.", "Przewodnik Fable Tour czeka na gości w hali przylotów lotniska w Bagdadzie"],
"zh": ["机场接送", "巴格达国际机场接机及送往酒店", "查看详情", "收起详情",
 "我们在巴格达国际机场到达大厅迎接您，并用专车直接送您到巴格达的酒店。",
 "到达大厅接机", "私人空调专车", "协助搬运行李", "送达您在巴格达的酒店",
 "到达日期", "到达时间（当地时间）", "人数", "酒店（选填）", "航班号（选填）",
 "选择到达日期和时间后即可看到价格。", "总价", "晚上8点至上午10点到达适用夜间价格",
 "通过WhatsApp预订", "您好！我想预订巴格达国际机场接机并送往酒店。到达时间：{date} {time}，共{n}人。{extra}价格：{price}。",
 "超过9人？请通过WhatsApp联系我们。", "Fable Tour导游在巴格达国际机场到达大厅等候客人"],
"ja": ["空港送迎", "バグダッド国際空港お出迎え・ホテル送迎", "詳細を見る", "詳細を閉じる",
 "バグダッド国際空港の到着ロビーでお出迎えし、専用車でバグダッドのホテルまで直接お送りします。",
 "到着ロビーでお出迎え", "エアコン付き専用車", "お荷物のお手伝い", "バグダッドのホテルまでお送り",
 "到着日", "到着時刻（現地時間）", "人数", "ホテル（任意）", "便名（任意）",
 "到着日と到着時刻を選ぶと料金が表示されます。", "合計料金", "20時〜翌10時の到着は夜間料金です",
 "WhatsAppで予約", "こんにちは！バグダッド国際空港でのお出迎えとホテルへの送迎を予約したいです。到着：{date} {time}、{n}名。{extra}料金：{price}。",
 "10名以上の場合はWhatsAppでご連絡ください。", "バグダッド国際空港の到着ロビーでお客様を待つFable Tourのガイド"],
"tr": ["Havalimanı transferi", "Bağdat Havalimanı'nda karşılama ve otele transfer", "Ayrıntıları göster", "Ayrıntıları gizle",
 "Sizi Bağdat Uluslararası Havalimanı'nın geliş salonunda karşılıyor ve özel araçla doğrudan Bağdat'taki otelinize götürüyoruz.",
 "Geliş salonunda karşılama", "Klimalı özel araç", "Bagajlarınıza yardım", "Bağdat'taki otelinize bırakma",
 "Varış tarihi", "Varış saati (yerel)", "Yolcu sayısı", "Otel (isteğe bağlı)", "Uçuş numarası (isteğe bağlı)",
 "Fiyatı görmek için varış tarihini ve saatini seçin.", "Toplam fiyat", "20:00 ile 10:00 arasındaki varışlar için gece tarifesi",
 "WhatsApp'tan rezervasyon", "Merhaba! Bağdat Uluslararası Havalimanı'nda karşılama ve otele transfer rezervasyonu yapmak istiyorum. Varış: {date}, saat {time}, {n} yolcu.{extra} Fiyat: {price}.",
 "9 kişiden fazla mısınız? Bize WhatsApp'tan yazın.", "Bağdat Uluslararası Havalimanı geliş salonunda misafirleri bekleyen Fable Tour rehberi"],
"fa": ["ترانسفر فرودگاه", "استقبال در فرودگاه بغداد و انتقال به هتل", "نمایش جزئیات", "پنهان کردن جزئیات",
 "در سالن ورودی فرودگاه بین‌المللی بغداد از شما استقبال می‌کنیم و با خودروی اختصاصی مستقیم به هتل‌تان در بغداد می‌رسانیم.",
 "استقبال در سالن ورودی", "خودروی اختصاصی کولردار", "کمک در حمل چمدان‌ها", "رساندن به هتل شما در بغداد",
 "تاریخ ورود", "ساعت ورود (به وقت محلی)", "تعداد مسافران", "هتل (اختیاری)", "شماره پرواز (اختیاری)",
 "برای دیدن قیمت، تاریخ و ساعت ورود را انتخاب کنید.", "قیمت کل", "نرخ شبانه برای ورود بین ساعت ۸ شب تا ۱۰ صبح",
 "رزرو از طریق واتساپ", "سلام! می‌خواهم استقبال در فرودگاه بین‌المللی بغداد و انتقال به هتل را رزرو کنم. ورود: {date} ساعت {time}، {n} مسافر.{extra} قیمت: {price}.",
 "بیش از ۹ مسافر؟ در واتساپ به ما پیام دهید.", "راهنمای Fable Tour در انتظار مسافران در سالن ورودی فرودگاه بین‌المللی بغداد"],
"ms": ["Pemindahan lapangan terbang", "Sambutan di Lapangan Terbang Baghdad & hantar ke hotel", "Lihat butiran", "Sembunyi butiran",
 "Kami menyambut anda di dewan ketibaan Lapangan Terbang Antarabangsa Baghdad dan menghantar anda dengan kereta persendirian terus ke hotel anda di Baghdad.",
 "Sambutan di dewan ketibaan", "Kereta persendirian berhawa dingin", "Bantuan dengan bagasi", "Hantar ke hotel anda di Baghdad",
 "Tarikh ketibaan", "Waktu ketibaan (waktu tempatan)", "Bilangan pelancong", "Hotel (pilihan)", "Nombor penerbangan (pilihan)",
 "Pilih tarikh dan waktu ketibaan untuk melihat harga.", "Jumlah harga", "Kadar malam untuk ketibaan antara 8 malam dan 10 pagi",
 "Tempah melalui WhatsApp", "Assalamualaikum! Saya ingin menempah sambutan di Lapangan Terbang Antarabangsa Baghdad dan hantar ke hotel. Ketibaan: {date} pada {time}, {n} orang.{extra} Harga: {price}.",
 "Lebih daripada 9 orang? Hubungi kami di WhatsApp.", "Pemandu pelancong Fable Tour menunggu tetamu di dewan ketibaan Lapangan Terbang Antarabangsa Baghdad"],
"id": ["Transfer bandara", "Penjemputan di Bandara Baghdad & antar ke hotel", "Lihat detail", "Sembunyikan detail",
 "Kami menyambut Anda di aula kedatangan Bandara Internasional Baghdad dan mengantar Anda dengan mobil pribadi langsung ke hotel Anda di Baghdad.",
 "Penyambutan di aula kedatangan", "Mobil pribadi ber-AC", "Bantuan membawa bagasi", "Antar sampai hotel Anda di Baghdad",
 "Tanggal kedatangan", "Jam kedatangan (waktu setempat)", "Jumlah wisatawan", "Hotel (opsional)", "Nomor penerbangan (opsional)",
 "Pilih tanggal dan jam kedatangan untuk melihat harga.", "Total harga", "Tarif malam untuk kedatangan antara pukul 20.00 dan 10.00",
 "Pesan lewat WhatsApp", "Halo! Saya ingin memesan penjemputan di Bandara Internasional Baghdad dan antar ke hotel. Kedatangan: {date} pukul {time}, {n} orang.{extra} Harga: {price}.",
 "Lebih dari 9 orang? Hubungi kami lewat WhatsApp.", "Pemandu Fable Tour menunggu tamu di aula kedatangan Bandara Internasional Baghdad"],
"th": ["รถรับส่งสนามบิน", "รับที่สนามบินแบกแดดและส่งถึงโรงแรม", "ดูรายละเอียด", "ซ่อนรายละเอียด",
 "เราจะรอรับคุณที่โถงผู้โดยสารขาเข้าของท่าอากาศยานนานาชาติแบกแดด และพาคุณไปส่งถึงโรงแรมในแบกแดดด้วยรถส่วนตัว",
 "รอรับที่โถงผู้โดยสารขาเข้า", "รถส่วนตัวติดแอร์", "ช่วยยกกระเป๋าสัมภาระ", "ส่งถึงโรงแรมของคุณในแบกแดด",
 "วันที่เดินทางถึง", "เวลาที่เดินทางถึง (เวลาท้องถิ่น)", "จำนวนผู้เดินทาง", "โรงแรม (ไม่บังคับ)", "เที่ยวบิน (ไม่บังคับ)",
 "เลือกวันที่และเวลาที่เดินทางถึงเพื่อดูราคา", "ราคารวม", "อัตรากลางคืนสำหรับเที่ยวบินที่ถึงระหว่าง 20:00 ถึง 10:00 น.",
 "จองทาง WhatsApp", "สวัสดีครับ/ค่ะ! ต้องการจองบริการรับที่ท่าอากาศยานนานาชาติแบกแดดและส่งถึงโรงแรม เดินทางถึง: {date} เวลา {time} จำนวน {n} คน{extra} ราคา: {price}",
 "มากกว่า 9 คน? ติดต่อเราทาง WhatsApp", "ไกด์ของ Fable Tour รอรับแขกที่โถงผู้โดยสารขาเข้าท่าอากาศยานนานาชาติแบกแดด"],
"hi": ["एयरपोर्ट ट्रांसफ़र", "बग़दाद एयरपोर्ट पर स्वागत और होटल तक ट्रांसफ़र", "विवरण देखें", "विवरण छिपाएँ",
 "हम बग़दाद अंतरराष्ट्रीय हवाई अड्डे के आगमन हॉल में आपका स्वागत करते हैं और निजी कार से सीधे बग़दाद में आपके होटल तक पहुँचाते हैं।",
 "आगमन हॉल में स्वागत", "निजी एसी कार", "सामान उठाने में मदद", "बग़दाद में आपके होटल तक छोड़ना",
 "आगमन की तारीख़", "आगमन का समय (स्थानीय)", "यात्री", "होटल (वैकल्पिक)", "फ़्लाइट नंबर (वैकल्पिक)",
 "क़ीमत देखने के लिए आगमन की तारीख़ और समय चुनें।", "कुल क़ीमत", "रात 8 बजे से सुबह 10 बजे के बीच आगमन पर रात की दर",
 "WhatsApp पर बुक करें", "नमस्ते! मैं बग़दाद अंतरराष्ट्रीय हवाई अड्डे पर स्वागत और होटल तक ट्रांसफ़र बुक करना चाहता/चाहती हूँ। आगमन: {date}, {time} बजे, {n} यात्री।{extra} क़ीमत: {price}।",
 "9 से ज़्यादा यात्री? हमें WhatsApp पर लिखें।", "बग़दाद अंतरराष्ट्रीय हवाई अड्डे के आगमन हॉल में मेहमानों का इंतज़ार करते Fable Tour गाइड"],
"ur": ["ایئرپورٹ ٹرانسفر", "بغداد ایئرپورٹ پر استقبال اور ہوٹل تک ٹرانسفر", "تفصیلات دیکھیں", "تفصیلات چھپائیں",
 "ہم بغداد انٹرنیشنل ایئرپورٹ کے آمد ہال میں آپ کا استقبال کرتے ہیں اور نجی گاڑی میں سیدھا بغداد میں آپ کے ہوٹل تک پہنچاتے ہیں۔",
 "آمد ہال میں استقبال", "نجی ایئرکنڈیشنڈ گاڑی", "سامان اٹھانے میں مدد", "بغداد میں آپ کے ہوٹل تک پہنچانا",
 "آمد کی تاریخ", "آمد کا وقت (مقامی)", "مسافر", "ہوٹل (اختیاری)", "فلائٹ نمبر (اختیاری)",
 "قیمت دیکھنے کے لیے آمد کی تاریخ اور وقت منتخب کریں۔", "کل قیمت", "رات 8 بجے سے صبح 10 بجے کے درمیان آمد پر رات کا نرخ",
 "واٹس ایپ پر بکنگ کریں", "السلام علیکم! میں بغداد انٹرنیشنل ایئرپورٹ پر استقبال اور ہوٹل تک ٹرانسفر بک کرنا چاہتا/چاہتی ہوں۔ آمد: {date}، وقت {time}، {n} مسافر۔{extra} قیمت: {price}۔",
 "9 سے زیادہ مسافر؟ ہمیں واٹس ایپ پر لکھیں۔", "بغداد انٹرنیشنل ایئرپورٹ کے آمد ہال میں مہمانوں کا منتظر Fable Tour کا گائیڈ"],
"ta": ["விமான நிலைய இடமாற்றம்", "பாக்தாத் விமான நிலைய வரவேற்பு & ஹோட்டலுக்கு அழைத்துச் செல்லுதல்", "விவரங்களைக் காண்க", "விவரங்களை மறை",
 "பாக்தாத் சர்வதேச விமான நிலையத்தின் வருகை மண்டபத்தில் உங்களை வரவேற்று, தனியார் காரில் பாக்தாதில் உள்ள உங்கள் ஹோட்டலுக்கு நேரடியாக அழைத்துச் செல்கிறோம்.",
 "வருகை மண்டபத்தில் வரவேற்பு", "குளிரூட்டப்பட்ட தனியார் கார்", "சாமான்களுக்கு உதவி", "பாக்தாதில் உங்கள் ஹோட்டலில் இறக்கிவிடுதல்",
 "வருகை தேதி", "வருகை நேரம் (உள்ளூர்)", "பயணிகள்", "ஹோட்டல் (விருப்பம்)", "விமான எண் (விருப்பம்)",
 "விலையைக் காண வருகை தேதியையும் நேரத்தையும் தேர்ந்தெடுக்கவும்.", "மொத்த விலை", "இரவு 8 மணி முதல் காலை 10 மணி வரை வருகைக்கு இரவு கட்டணம்",
 "WhatsApp மூலம் முன்பதிவு", "வணக்கம்! பாக்தாத் சர்வதேச விமான நிலைய வரவேற்பு மற்றும் ஹோட்டலுக்கு இடமாற்றம் முன்பதிவு செய்ய விரும்புகிறேன். வருகை: {date}, நேரம் {time}, {n} பயணிகள்.{extra} விலை: {price}.",
 "9 பேருக்கு மேல்? WhatsApp-இல் எங்களுக்கு எழுதுங்கள்.", "பாக்தாத் சர்வதேச விமான நிலைய வருகை மண்டபத்தில் விருந்தினர்களுக்காகக் காத்திருக்கும் Fable Tour வழிகாட்டி"],
"fi": ["Lentokenttäkuljetus", "Vastaanotto Bagdadin lentoasemalla ja kuljetus hotelliin", "Näytä tiedot", "Piilota tiedot",
 "Otamme sinut vastaan Bagdadin kansainvälisen lentoaseman tuloaulassa ja ajamme yksityisellä autolla suoraan hotelliisi Bagdadissa.",
 "Vastaanotto tuloaulassa", "Yksityinen ilmastoitu auto", "Apua matkatavaroiden kanssa", "Kuljetus hotelliisi Bagdadissa",
 "Saapumispäivä", "Saapumisaika (paikallista aikaa)", "Matkustajat", "Hotelli (valinnainen)", "Lennon numero (valinnainen)",
 "Valitse saapumispäivä ja -aika nähdäksesi hinnan.", "Kokonaishinta", "Yöhinta klo 20–10 saapuville",
 "Varaa WhatsAppissa", "Hei! Haluaisin varata vastaanoton Bagdadin kansainvälisellä lentoasemalla ja kuljetuksen hotelliin. Saapuminen: {date} klo {time}, {n} matkustajaa.{extra} Hinta: {price}.",
 "Yli 9 matkustajaa? Kirjoita meille WhatsAppissa.", "Fable Tourin opas odottaa matkailijoita Bagdadin kansainvälisen lentoaseman tuloaulassa"],
"sv": ["Flygplatstransfer", "Mottagning på Bagdads flygplats och transfer till hotellet", "Visa detaljer", "Dölj detaljer",
 "Vi tar emot dig i ankomsthallen på Bagdads internationella flygplats och kör dig med privat bil direkt till ditt hotell i Bagdad.",
 "Mottagning i ankomsthallen", "Privat luftkonditionerad bil", "Hjälp med bagaget", "Avlämning vid ditt hotell i Bagdad",
 "Ankomstdatum", "Ankomsttid (lokal tid)", "Resenärer", "Hotell (valfritt)", "Flightnummer (valfritt)",
 "Välj ankomstdatum och tid för att se priset.", "Totalpris", "Nattpris för ankomster mellan 20.00 och 10.00",
 "Boka via WhatsApp", "Hej! Jag vill boka mottagning på Bagdads internationella flygplats med transfer till hotellet. Ankomst: {date} kl. {time}, {n} resenärer.{extra} Pris: {price}.",
 "Fler än 9 resenärer? Skriv till oss på WhatsApp.", "Fable Tour-guide väntar på resenärer i ankomsthallen på Bagdads internationella flygplats"],
"da": ["Lufthavnstransfer", "Afhentning i Bagdads lufthavn og transfer til hotellet", "Vis detaljer", "Skjul detaljer",
 "Vi tager imod dig i ankomsthallen i Bagdads internationale lufthavn og kører dig i privat bil direkte til dit hotel i Bagdad.",
 "Modtagelse i ankomsthallen", "Privat bil med aircondition", "Hjælp med bagagen", "Kørsel helt til dit hotel i Bagdad",
 "Ankomstdato", "Ankomsttid (lokal tid)", "Rejsende", "Hotel (valgfrit)", "Flynummer (valgfrit)",
 "Vælg ankomstdato og -tid for at se prisen.", "Samlet pris", "Nattakst for ankomster mellem kl. 20 og 10",
 "Book via WhatsApp", "Hej! Jeg vil gerne booke afhentning i Bagdads internationale lufthavn med transfer til hotellet. Ankomst: {date} kl. {time}, {n} rejsende.{extra} Pris: {price}.",
 "Mere end 9 rejsende? Skriv til os på WhatsApp.", "Guide fra Fable Tour venter på rejsende i ankomsthallen i Bagdads internationale lufthavn"],
"no": ["Flyplasstransfer", "Henting på Bagdad lufthavn og transfer til hotellet", "Vis detaljer", "Skjul detaljer",
 "Vi tar imot deg i ankomsthallen på Bagdad internasjonale lufthavn og kjører deg i privat bil rett til hotellet ditt i Bagdad.",
 "Mottak i ankomsthallen", "Privat bil med klimaanlegg", "Hjelp med bagasjen", "Levering ved hotellet ditt i Bagdad",
 "Ankomstdato", "Ankomsttid (lokal tid)", "Reisende", "Hotell (valgfritt)", "Flightnummer (valgfritt)",
 "Velg ankomstdato og -tid for å se prisen.", "Totalpris", "Nattpris for ankomster mellom kl. 20 og 10",
 "Bestill på WhatsApp", "Hei! Jeg vil gjerne bestille henting på Bagdad internasjonale lufthavn med transfer til hotellet. Ankomst: {date} kl. {time}, {n} reisende.{extra} Pris: {price}.",
 "Flere enn 9 reisende? Skriv til oss på WhatsApp.", "Guide fra Fable Tour venter på reisende i ankomsthallen på Bagdad internasjonale lufthavn"],
}
EXTRA = {  # "hotel: X" and "flight: Y" fragments in the WhatsApp message
"en": ("Hotel: {h}.", "Flight: {f}."), "ar": ("الفندق: {h}.", "رقم الرحلة: {f}."), "ru": ("Отель: {h}.", "Рейс: {f}."),
"de": ("Hotel: {h}.", "Flug: {f}."), "fr": ("Hôtel : {h}.", "Vol : {f}."), "es": ("Hotel: {h}.", "Vuelo: {f}."),
"it": ("Hotel: {h}.", "Volo: {f}."), "el": ("Ξενοδοχείο: {h}.", "Πτήση: {f}."), "cs": ("Hotel: {h}.", "Let: {f}."),
"pl": ("Hotel: {h}.", "Lot: {f}."), "zh": ("酒店：{h}。", "航班：{f}。"), "ja": ("ホテル：{h}。", "便名：{f}。"),
"tr": ("Otel: {h}.", "Uçuş: {f}."), "fa": ("هتل: {h}.", "پرواز: {f}."), "ms": ("Hotel: {h}.", "Penerbangan: {f}."),
"id": ("Hotel: {h}.", "Penerbangan: {f}."), "th": (" โรงแรม: {h}", " เที่ยวบิน: {f}"), "hi": ("होटल: {h}।", "फ़्लाइट: {f}।"),
"ur": ("ہوٹل: {h}۔", "فلائٹ: {f}۔"), "ta": ("ஹோட்டல்: {h}.", "விமானம்: {f}."), "fi": ("Hotelli: {h}.", "Lento: {f}."),
"sv": ("Hotell: {h}.", "Flight: {f}."), "da": ("Hotel: {h}.", "Fly: {f}."), "no": ("Hotell: {h}.", "Fly: {f}."),
}

CSS = """<style id="ap-css">
.ap-toggle{width:100%;display:flex;align-items:center;justify-content:space-between;gap:14px;background:var(--navy);color:#fff;border:0;border-radius:6px;padding:20px 22px;cursor:pointer;text-align:start;border-bottom:4px solid var(--gold);font:inherit}
.ap-toggle .eyebrow{color:var(--gold-2)}
.ap-toggle b{display:block;font-family:var(--serif-en);font-weight:400;font-size:clamp(21px,3.4vw,27px);line-height:1.3;margin-top:4px}
html[lang="ar"] .ap-toggle b,html[lang="fa"] .ap-toggle b,html[lang="ur"] .ap-toggle b{font-family:var(--serif-ar);font-weight:700}
.ap-toggle small{display:block;color:#C9CFD9;font-size:14px;margin-top:4px}
.ap-chev{flex:none;width:42px;height:42px;border-radius:50%;background:var(--gold);color:var(--navy);display:grid;place-items:center;transition:transform .25s}
.ap-toggle[aria-expanded="true"] .ap-chev{transform:rotate(180deg)}
.ap-card{margin-top:14px;background:var(--paper);border:1px solid var(--line);border-radius:6px;overflow:hidden;display:grid;grid-template-columns:1fr}
@media(min-width:820px){.ap-card{grid-template-columns:5fr 6fr}}
.ap-ph{position:relative;min-height:240px;background:var(--navy) center/cover no-repeat}
.ap-ph img{width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3}
.ap-in{padding:22px 22px 24px}
.ap-in>p{margin:0 0 14px;line-height:1.6;color:var(--ink)}
.ap-inc{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:7px}
.ap-inc li{display:flex;gap:9px;align-items:flex-start;font-size:15px}
.ap-inc li::before{content:"✓";color:var(--gold);font-weight:700;flex:none}
.ap-form{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.ap-form label{display:flex;flex-direction:column;gap:5px;font-size:13px;color:var(--muted);min-width:0}
.ap-form .wide{grid-column:1/-1}
.ap-form input,.ap-form select{width:100%;box-sizing:border-box;height:46px;padding:0 12px;border:1px solid var(--line);border-radius:5px;background:#fff;color:var(--ink);font:16px var(--sans-en);-webkit-appearance:none;appearance:none;min-width:0}
.ap-form select{background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);background-position:calc(100% - 18px) 20px,calc(100% - 13px) 20px;background-size:5px 5px;background-repeat:no-repeat}
html[dir="rtl"] .ap-form select{background-position:18px 20px,13px 20px}
.ap-price{margin-top:16px;padding:14px 16px;border-radius:6px;background:var(--panel);border:1px solid var(--line)}
.ap-price .ap-hint{color:var(--muted);font-size:14px}
.ap-price .ap-tot span{display:block;font-size:12px;color:var(--muted);letter-spacing:.04em}
.ap-price .ap-tot b{font-family:var(--serif-en);font-weight:400;font-size:30px;color:var(--navy)}
.ap-price .ap-tot .eur{display:block;font-size:.55em}
.ap-night{display:block;margin-top:4px;font-size:12.5px;color:var(--muted)}
.ap-night[hidden],.ap-tot[hidden],.ap-hint[hidden]{display:none}
.ap-book{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:14px;height:50px;border-radius:5px;background:#25D366;color:#fff;font-weight:600;text-decoration:none}
.ap-book[aria-disabled="true"]{opacity:.45;pointer-events:none}
.ap-big{margin-top:10px;font-size:13px;color:var(--muted)}
</style>"""


# Slovak, Croatian, Romanian (added Oct 2026)
S["sk"] = ["Transfer z letiska", "Vyzdvihnutie na letisku v Bagdade a odvoz do hotela", "Zobraziť podrobnosti", "Skryť podrobnosti", "Privítame vás v príletovej hale Medzinárodného letiska Bagdad a súkromným autom vás odvezieme priamo do vášho hotela v Bagdade.", "Privítanie v príletovej hale", "Súkromné klimatizované auto", "Pomoc s batožinou", "Odvoz až k vášmu hotelu v Bagdade", "Dátum príletu", "Čas príletu (miestny)", "Cestujúci", "Hotel (nepovinné)", "Číslo letu (nepovinné)", "Vyberte dátum a čas príletu a zobrazí sa cena.", "Celková cena", "Nočná sadzba pre prílety medzi 20:00 a 10:00", "Rezervovať cez WhatsApp", "Dobrý deň! Chcem si objednať vyzdvihnutie na Medzinárodnom letisku Bagdad s odvozom do hotela. Prílet: {date} o {time}, počet cestujúcich: {n}.{extra} Cena: {price}.", "Viac ako 9 cestujúcich? Napíšte nám na WhatsApp.", "Sprievodca Fable Tour čaká na hostí v príletovej hale Medzinárodného letiska Bagdad"]
S["hr"] = ["Transfer iz zračne luke", "Doček u zračnoj luci Bagdad i prijevoz do hotela", "Prikaži detalje", "Sakrij detalje", "Dočekujemo vas u dolaznoj dvorani Međunarodne zračne luke Bagdad i privatnim automobilom vozimo vas izravno do vašeg hotela u Bagdadu.", "Doček u dolaznoj dvorani", "Privatni klimatizirani automobil", "Pomoć s prtljagom", "Prijevoz do vašeg hotela u Bagdadu", "Datum dolaska", "Vrijeme dolaska (lokalno)", "Putnici", "Hotel (neobavezno)", "Broj leta (neobavezno)", "Odaberite datum i vrijeme dolaska da biste vidjeli cijenu.", "Ukupna cijena", "Noćna tarifa za dolaske između 20:00 i 10:00", "Rezerviraj putem WhatsAppa", "Pozdrav! Želim rezervirati doček u Međunarodnoj zračnoj luci Bagdad s prijevozom do hotela. Dolazak: {date} u {time}, broj putnika: {n}.{extra} Cijena: {price}.", "Više od 9 putnika? Pišite nam na WhatsApp.", "Vodič Fable Toura čeka goste u dolaznoj dvorani Međunarodne zračne luke Bagdad"]
S["ro"] = ["Transfer de la aeroport", "Preluare de la aeroportul Bagdad și transfer la hotel", "Vezi detaliile", "Ascunde detaliile", "Vă întâmpinăm în sala de sosiri a Aeroportului Internațional Bagdad și vă ducem cu o mașină privată direct la hotelul dumneavoastră din Bagdad.", "Întâmpinare în sala de sosiri", "Mașină privată cu aer condiționat", "Ajutor cu bagajele", "Transfer până la hotelul dumneavoastră din Bagdad", "Data sosirii", "Ora sosirii (locală)", "Călători", "Hotel (opțional)", "Număr de zbor (opțional)", "Alegeți data și ora sosirii pentru a vedea prețul.", "Preț total", "Tarif de noapte pentru sosiri între 20:00 și 10:00", "Rezervă pe WhatsApp", "Bună ziua! Doresc să rezerv preluarea de la Aeroportul Internațional Bagdad cu transfer la hotel. Sosire: {date} la {time}, {n} călători.{extra} Preț: {price}.", "Mai mult de 9 călători? Scrieți-ne pe WhatsApp.", "Ghid Fable Tour care așteaptă oaspeții în sala de sosiri a Aeroportului Internațional Bagdad"]
EXTRA["sk"] = ("Hotel: {h}.", "Let: {f}.")
EXTRA["hr"] = ("Hotel: {h}.", "Let: {f}.")
EXTRA["ro"] = ("Hotel: {h}.", "Zbor: {f}.")

# Dutch (added Oct 2026)
S["nl"] = ["Luchthaventransfer", "Ophalen op de luchthaven van Bagdad en transfer naar het hotel", "Details bekijken", "Details verbergen", "We ontvangen u in de aankomsthal van de internationale luchthaven van Bagdad en brengen u met een privéauto rechtstreeks naar uw hotel in Bagdad.", "Ontvangst in de aankomsthal", "Privéauto met airco", "Hulp met uw bagage", "Transfer naar uw hotel in Bagdad", "Aankomstdatum", "Aankomsttijd (lokaal)", "Reizigers", "Hotel (optioneel)", "Vluchtnummer (optioneel)", "Kies uw aankomstdatum en -tijd om de prijs te zien.", "Totaalprijs", "Nachttarief voor aankomsten tussen 20:00 en 10:00", "Boeken via WhatsApp", "Hallo! Ik wil graag een ophaalservice boeken op de internationale luchthaven van Bagdad met transfer naar mijn hotel. Aankomst: {date} om {time}, {n} reizigers.{extra} Prijs: {price}.", "Meer dan 9 reizigers? Stuur ons een bericht via WhatsApp.", "Gids van Fable Tour wacht op gasten in de aankomsthal van de internationale luchthaven van Bagdad"]
EXTRA["nl"] = ("Hotel: {h}.", "Vlucht: {f}.")

# Georgian (added Oct 2026)
S["ka"] = ["აეროპორტის ტრანსფერი", "დახვედრა ბაღდადის აეროპორტში და ტრანსფერი სასტუმრომდე", "დეტალების ნახვა", "დეტალების დამალვა", "დაგხვდებით ბაღდადის საერთაშორისო აეროპორტის ჩამოსვლის დარბაზში და კერძო მანქანით პირდაპირ ბაღდადში თქვენს სასტუმრომდე მიგიყვანთ.", "დახვედრა ჩამოსვლის დარბაზში", "კონდიციონერიანი კერძო მანქანა", "დახმარება ბარგთან", "ტრანსფერი თქვენს სასტუმრომდე ბაღდადში", "ჩამოსვლის თარიღი", "ჩამოსვლის დრო (ადგილობრივი)", "მოგზაურები", "სასტუმრო (არასავალდებულო)", "რეისის ნომერი (არასავალდებულო)", "ფასის სანახავად აირჩიეთ ჩამოსვლის თარიღი და დრო.", "საერთო ფასი", "ღამის ტარიფი 20:00-დან 10:00-მდე ჩამოსვლისთვის", "დაჯავშნა WhatsApp-ით", "გამარჯობა! მინდა დავჯავშნო დახვედრა ბაღდადის საერთაშორისო აეროპორტში და ტრანსფერი სასტუმრომდე. ჩამოსვლა: {date}, {time}, {n} მოგზაური.{extra} ფასი: {price}.", "9-ზე მეტი მოგზაური? მოგვწერეთ WhatsApp-ზე.", "Fable Tour-ის გიდი სტუმრებს ბაღდადის საერთაშორისო აეროპორტის ჩამოსვლის დარბაზში ელოდება"]
EXTRA["ka"] = ("სასტუმრო: {h}.", "რეისი: {f}.")

def esc(s): return html.escape(s, quote=True)


def section(l):
    t = dict(zip(K, S[l]))
    opts = "".join(f'<option value="{n}">{n}</option>' for n in range(1, MAXP + 1))
    return f'''
  <section class="block in" style="padding-top:0" id="airport-transfer">
    <button class="ap-toggle" type="button" aria-expanded="false" aria-controls="ap-body" data-show="{esc(t["show"])}" data-hide="{esc(t["hide"])}">
      <span><span class="eyebrow">{esc(t["eye"])}</span><b>{esc(t["h"])}</b><small class="ap-lbl">{esc(t["show"])}</small></span>
      <span class="ap-chev"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span>
    </button>
    <div id="ap-body" hidden>
      <div class="ap-card">
        <div class="ap-ph"><img src="{IMG}" alt="{esc(t["alt"])}" width="1400" height="1050" loading="lazy" decoding="async"></div>
        <div class="ap-in">
          <p>{esc(t["p"])}</p>
          <ul class="ap-inc"><li>{esc(t["i1"])}</li><li>{esc(t["i2"])}</li><li>{esc(t["i3"])}</li><li>{esc(t["i4"])}</li></ul>
          <div class="ap-form">
            <label>{esc(t["date"])}<input type="date" id="ap-date" required></label>
            <label>{esc(t["time"])}<input type="time" id="ap-time" required></label>
            <label class="wide">{esc(t["trav"])}<select id="ap-n">{opts}</select></label>
            <label>{esc(t["hotel"])}<input type="text" id="ap-hotel" autocomplete="off"></label>
            <label>{esc(t["flight"])}<input type="text" id="ap-flight" autocomplete="off"></label>
          </div>
          <div class="ap-price" aria-live="polite">
            <div class="ap-hint">{esc(t["hint"])}</div>
            <div class="ap-tot" hidden><span>{esc(t["total"])}</span><b dir="ltr"></b></div>
          </div>
          <a class="ap-book" href="https://wa.me/9647711745353" target="_blank" rel="noopener" aria-disabled="true">{esc(t["book"])}</a>
          <div class="ap-big">{esc(t["big"])}</div>
        </div>
      </div>
    </div>
  </section>
'''


def script(l):
    t = dict(zip(K, S[l]))
    eh, ef = EXTRA[l]
    cfg = json.dumps({"wa": t["wa"], "eh": eh, "ef": ef, "show": t["show"], "hide": t["hide"]}, ensure_ascii=False)
    return f'''<script id="ap-js">(function(){{
var C={cfg},DAY={DAY},NIGHT={NIGHT},PER={PER_CAR};
var b=document.querySelector(".ap-toggle"),body=document.getElementById("ap-body"),lbl=b&&b.querySelector(".ap-lbl");if(!b||!body)return;
function setOpen(o){{body.hidden=!o;b.setAttribute("aria-expanded",o);if(lbl)lbl.textContent=o?C.hide:C.show;}}
b.addEventListener("click",function(){{setOpen(body.hidden);}});
if(location.hash==="#airport-transfer")setOpen(true);
var d=document.getElementById("ap-date"),tm=document.getElementById("ap-time"),n=document.getElementById("ap-n"),h=document.getElementById("ap-hotel"),f=document.getElementById("ap-flight");
var hint=body.querySelector(".ap-hint"),tot=body.querySelector(".ap-tot"),out=tot.querySelector("b"),bk=body.querySelector(".ap-book");
try{{var td=new Date();td.setMinutes(td.getMinutes()-td.getTimezoneOffset());d.min=td.toISOString().slice(0,10);}}catch(e){{}}
function upd(){{
 if(!d.value||!tm.value){{hint.hidden=false;tot.hidden=true;bk.setAttribute("aria-disabled","true");bk.href="https://wa.me/9647711745353";return;}}
 var hr=parseInt(tm.value.split(":")[0],10),isNight=!(hr>=10&&hr<20),k=+n.value||1,cars=Math.ceil(k/PER),p=(isNight?NIGHT:DAY)*cars,ps="$"+p.toLocaleString("en-US");
 hint.hidden=true;tot.hidden=false;out.textContent=ps;
 var ex="";if(h.value.trim())ex+=" "+C.eh.replace("{{h}}",h.value.trim());if(f.value.trim())ex+=" "+C.ef.replace("{{f}}",f.value.trim());
 var msg=C.wa.replace("{{date}}",d.value).replace("{{time}}",tm.value).replace("{{n}}",k).replace("{{extra}}",ex).replace("{{price}}",ps);
 bk.href="https://wa.me/9647711745353?text="+encodeURIComponent(msg);bk.removeAttribute("aria-disabled");}}
[d,tm,n,h,f].forEach(function(x){{x.addEventListener("input",upd);x.addEventListener("change",upd);}});
}})();</script>'''


def home_files():
    yield "ar", ROOT / "index.html"
    for l in S:
        if l != "ar":
            yield l, ROOT / l / "index.html"


def run():
    for l, f in home_files():
        s = f.read_text()
        s = re.sub(r'\n  <section class="block in" style="padding-top:0" id="airport-transfer">.*?</section>\n', "", s, flags=re.S)
        s = re.sub(r'<style id="ap-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="ap-js">.*?</script>\n?', "", s, flags=re.S)
        i = s.index('id="day-trips"'); st = s.rfind("<section", 0, i); depth = 0
        for m in re.finditer(r"<section\b|</section>", s[st:]):
            depth += -1 if m.group(0) == "</section>" else 1
            if depth == 0:
                end = st + m.end(); break
        s = s[:end] + section(l) + s[end:]
        s = s.replace("</head>", CSS + "\n</head>", 1)
        s = s.replace("</body>", script(l) + "\n</body>", 1)
        f.write_text(s)
        print("airport:", l)


if __name__ == "__main__":
    run()
