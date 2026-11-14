(function () {
  "use strict";
  var RTL = { ar: 1, ckb: 1, fa: 1, ur: 1 };
  var ALIAS = { "zh-hans": "zh", "zh-cn": "zh", "zh-hant": "zh-tw", "zh-hant-tw": "zh-tw", nb: "no", nn: "no" };
  var PACKS = {"ar":{"title":"المواد الإعلانية | Fable Tour","eye":"الإعلانات","h1":"المواد الإعلانية","lead":"بانرات جاهزة بهوية Fable Tour. انسخ الشفرة وفيها رمز إحالتك، أو نزّل الملف.","all":"الكل","png":"صورة ثابتة","gif":"صورة متحركة","html":"HTML متحرك","download":"تنزيل","copy":"نسخ الشفرة","copied":"تم النسخ","back":"العودة إلى لوحتي","static":"ثابت","animated":"متحرك"},"ckb":{"title":"کەرەستەی ڕیکلام | Fable Tour","eye":"ڕیکلام","h1":"کەرەستەی ڕیکلام","lead":"بانەری ئامادەی Fable Tour. کۆدەکە لەگەڵ بەستەری خۆت کۆپی بکە، یان فایلەکە دابەزێنە.","all":"هەموو","png":"وێنەی جێگیر","gif":"وێنەی جوڵاو","html":"HTMLی جوڵاو","download":"داگرتن","copy":"کۆپیکردنی کۆد","copied":"کۆپی کرا","back":"گەڕانەوە بۆ تەختەکەم","static":"جێگیر","animated":"جوڵاو"},"en":{"title":"Marketing materials | Fable Tour","eye":"Ads","h1":"Marketing materials","lead":"Ready-made Fable Tour banners. Copy the code with your referral link, or download the file.","all":"All","png":"Still image","gif":"Animated image","html":"Animated HTML","download":"Download","copy":"Copy code","copied":"Copied","back":"Back to my dashboard","static":"Still","animated":"Animated"},"tr":{"title":"Reklam materyalleri | Fable Tour","eye":"Reklam","h1":"Reklam materyalleri","lead":"Hazır Fable Tour afişleri. Kendi yönlendirme kodunuzla kodu kopyalayın veya dosyayı indirin.","all":"Tümü","png":"Sabit görsel","gif":"Hareketli görsel","html":"Hareketli HTML","download":"İndir","copy":"Kodu kopyala","copied":"Kopyalandı","back":"Panoya dön","static":"Sabit","animated":"Hareketli"},"ru":{"title":"Рекламные материалы | Fable Tour","eye":"Реклама","h1":"Рекламные материалы","lead":"Готовые баннеры Fable Tour. Скопируйте код со своей ссылкой или скачайте файл.","all":"Все","png":"Неподвижное изображение","gif":"Анимация","html":"Анимированный HTML","download":"Скачать","copy":"Копировать код","copied":"Скопировано","back":"Назад к панели","static":"Неподвижное","animated":"Анимация"},"de":{"title":"Werbemittel | Fable Tour","eye":"Werbung","h1":"Werbemittel","lead":"Fertige Fable-Tour-Banner. Kopieren Sie den Code mit Ihrem Link oder laden Sie die Datei herunter.","all":"Alle","png":"Standbild","gif":"Animiertes Bild","html":"Animiertes HTML","download":"Herunterladen","copy":"Code kopieren","copied":"Kopiert","back":"Zurück zur Übersicht","static":"Standbild","animated":"Animiert"},"fr":{"title":"Supports publicitaires | Fable Tour","eye":"Publicité","h1":"Supports publicitaires","lead":"Bannières Fable Tour prêtes. Copiez le code avec votre lien, ou téléchargez le fichier.","all":"Tout","png":"Image fixe","gif":"Image animée","html":"HTML animé","download":"Télécharger","copy":"Copier le code","copied":"Copié","back":"Retour au tableau","static":"Fixe","animated":"Animé"},"es":{"title":"Materiales publicitarios | Fable Tour","eye":"Anuncios","h1":"Materiales publicitarios","lead":"Banners listos de Fable Tour. Copia el código con tu enlace o descarga el archivo.","all":"Todo","png":"Imagen fija","gif":"Imagen animada","html":"HTML animado","download":"Descargar","copy":"Copiar código","copied":"Copiado","back":"Volver a mi panel","static":"Fija","animated":"Animada"},"it":{"title":"Materiali pubblicitari | Fable Tour","eye":"Pubblicità","h1":"Materiali pubblicitari","lead":"Banner pronti di Fable Tour. Copia il codice con il tuo link oppure scarica il file.","all":"Tutti","png":"Immagine fissa","gif":"Immagine animata","html":"HTML animato","download":"Scarica","copy":"Copia codice","copied":"Copiato","back":"Torna al pannello","static":"Fissa","animated":"Animata"},"el":{"title":"Διαφημιστικό υλικό | Fable Tour","eye":"Διαφήμιση","h1":"Διαφημιστικό υλικό","lead":"Έτοιμα banner της Fable Tour. Αντιγράψτε τον κώδικα με τον σύνδεσμό σας ή κατεβάστε το αρχείο.","all":"Όλα","png":"Στατική εικόνα","gif":"Κινούμενη εικόνα","html":"Κινούμενο HTML","download":"Λήψη","copy":"Αντιγραφή κώδικα","copied":"Αντιγράφηκε","back":"Επιστροφή στον πίνακα","static":"Στατικό","animated":"Κινούμενο"},"cs":{"title":"Reklamní materiály | Fable Tour","eye":"Reklama","h1":"Reklamní materiály","lead":"Hotové bannery Fable Tour. Zkopírujte kód se svým odkazem nebo stáhněte soubor.","all":"Vše","png":"Statický obrázek","gif":"Animovaný obrázek","html":"Animované HTML","download":"Stáhnout","copy":"Kopírovat kód","copied":"Zkopírováno","back":"Zpět na nástěnku","static":"Statický","animated":"Animovaný"},"pl":{"title":"Materiały reklamowe | Fable Tour","eye":"Reklama","h1":"Materiały reklamowe","lead":"Gotowe banery Fable Tour. Skopiuj kod ze swoim linkiem albo pobierz plik.","all":"Wszystkie","png":"Obraz statyczny","gif":"Obraz animowany","html":"Animowany HTML","download":"Pobierz","copy":"Kopiuj kod","copied":"Skopiowano","back":"Wróć do panelu","static":"Statyczny","animated":"Animowany"},"zh":{"title":"广告素材 | Fable Tour","eye":"广告","h1":"广告素材","lead":"现成的 Fable Tour 横幅。复制带有你的推荐码的代码，或下载文件。","all":"全部","png":"静态图片","gif":"动态图片","html":"动态 HTML","download":"下载","copy":"复制代码","copied":"已复制","back":"返回我的面板","static":"静态","animated":"动态"},"zh-tw":{"title":"廣告素材 | Fable Tour","eye":"廣告","h1":"廣告素材","lead":"現成的 Fable Tour 橫幅。複製含你推薦碼的程式碼，或下載檔案。","all":"全部","png":"靜態圖片","gif":"動態圖片","html":"動態 HTML","download":"下載","copy":"複製程式碼","copied":"已複製","back":"返回我的面板","static":"靜態","animated":"動態"},"ja":{"title":"広告素材 | Fable Tour","eye":"広告","h1":"広告素材","lead":"Fable Tourのバナーです。紹介コード入りのコードをコピーするか、ファイルをダウンロードしてください。","all":"すべて","png":"静止画","gif":"アニメ画像","html":"アニメHTML","download":"ダウンロード","copy":"コードをコピー","copied":"コピーしました","back":"ダッシュボードへ","static":"静止","animated":"アニメ"},"fa":{"title":"مواد تبلیغاتی | Fable Tour","eye":"تبلیغ","h1":"مواد تبلیغاتی","lead":"بنرهای آماده Fable Tour. کد را با پیوند خود کپی کنید یا فایل را دانلود کنید.","all":"همه","png":"تصویر ثابت","gif":"تصویر متحرک","html":"HTML متحرک","download":"دانلود","copy":"کپی کد","copied":"کپی شد","back":"بازگشت به داشبورد","static":"ثابت","animated":"متحرک"},"ms":{"title":"Bahan iklan | Fable Tour","eye":"Iklan","h1":"Bahan iklan","lead":"Sepanduk Fable Tour yang sedia ada. Salin kod dengan pautan anda, atau muat turun fail.","all":"Semua","png":"Imej tetap","gif":"Imej bergerak","html":"HTML bergerak","download":"Muat turun","copy":"Salin kod","copied":"Disalin","back":"Kembali ke papan","static":"Tetap","animated":"Bergerak"},"id":{"title":"Materi iklan | Fable Tour","eye":"Iklan","h1":"Materi iklan","lead":"Spanduk Fable Tour yang siap dipakai. Salin kode dengan tautan Anda, atau unduh berkasnya.","all":"Semua","png":"Gambar diam","gif":"Gambar bergerak","html":"HTML bergerak","download":"Unduh","copy":"Salin kode","copied":"Tersalin","back":"Kembali ke dasbor","static":"Diam","animated":"Bergerak"},"th":{"title":"สื่อโฆษณา | Fable Tour","eye":"โฆษณา","h1":"สื่อโฆษณา","lead":"แบนเนอร์ Fable Tour พร้อมใช้ คัดลอกโค้ดที่มีลิงก์ของคุณ หรือดาวน์โหลดไฟล์","all":"ทั้งหมด","png":"ภาพนิ่ง","gif":"ภาพเคลื่อนไหว","html":"HTML เคลื่อนไหว","download":"ดาวน์โหลด","copy":"คัดลอกโค้ด","copied":"คัดลอกแล้ว","back":"กลับไปแดชบอร์ด","static":"นิ่ง","animated":"เคลื่อนไหว"},"hi":{"title":"विज्ञापन सामग्री | Fable Tour","eye":"विज्ञापन","h1":"विज्ञापन सामग्री","lead":"तैयार Fable Tour बैनर। अपना रेफ़रल लिंक सहित कोड कॉपी करें, या फ़ाइल डाउनलोड करें।","all":"सभी","png":"स्थिर चित्र","gif":"चलचित्र","html":"चल HTML","download":"डाउनलोड","copy":"कोड कॉपी","copied":"कॉपी हो गया","back":"डैशबोर्ड पर वापस","static":"स्थिर","animated":"चल"},"ur":{"title":"اشتہاری مواد | Fable Tour","eye":"اشتہار","h1":"اشتہاری مواد","lead":"تیار Fable Tour بینرز۔ اپنا ریفرل کوڈ سمیت کوڈ کاپی کریں، یا فائل ڈاؤن لوڈ کریں۔","all":"سب","png":"ساکت تصویر","gif":"متحرک تصویر","html":"متحرک HTML","download":"ڈاؤن لوڈ","copy":"کوڈ کاپی","copied":"کاپی ہو گیا","back":"ڈیش بورڈ پر واپس","static":"ساکت","animated":"متحرک"},"ta":{"title":"விளம்பரப் பொருட்கள் | Fable Tour","eye":"விளம்பரம்","h1":"விளம்பரப் பொருட்கள்","lead":"தயார் Fable Tour பதாகைகள். உங்கள் இணைப்புடன் குறியீட்டை நகலெடுக்கவும் அல்லது கோப்பைப் பதிவிறக்கவும்.","all":"அனைத்தும்","png":"நிலைப்படம்","gif":"அசைவுப்படம்","html":"அசையும் HTML","download":"பதிவிறக்கம்","copy":"குறியீட்டை நகலெடு","copied":"நகலெடுக்கப்பட்டது","back":"பலகைக்குத் திரும்பு","static":"நிலை","animated":"அசைவு"},"fi":{"title":"Mainosmateriaalit | Fable Tour","eye":"Mainokset","h1":"Mainosmateriaalit","lead":"Valmiit Fable Tour -bannerit. Kopioi koodi omalla linkilläsi tai lataa tiedosto.","all":"Kaikki","png":"Pysäytyskuva","gif":"Animoitu kuva","html":"Animoitu HTML","download":"Lataa","copy":"Kopioi koodi","copied":"Kopioitu","back":"Takaisin paneeliin","static":"Pysäytys","animated":"Animoitu"},"sv":{"title":"Annonsmaterial | Fable Tour","eye":"Annonser","h1":"Annonsmaterial","lead":"Färdiga Fable Tour-banners. Kopiera koden med din länk eller ladda ner filen.","all":"Alla","png":"Stillbild","gif":"Animerad bild","html":"Animerad HTML","download":"Ladda ner","copy":"Kopiera kod","copied":"Kopierad","back":"Tillbaka till panelen","static":"Still","animated":"Animerad"},"da":{"title":"Annoncemateriale | Fable Tour","eye":"Annoncer","h1":"Annoncemateriale","lead":"Færdige Fable Tour-bannere. Kopiér koden med dit link, eller hent filen.","all":"Alle","png":"Stillbillede","gif":"Animeret billede","html":"Animeret HTML","download":"Hent","copy":"Kopiér kode","copied":"Kopieret","back":"Tilbage til panelet","static":"Stille","animated":"Animeret"},"no":{"title":"Annonsemateriell | Fable Tour","eye":"Annonser","h1":"Annonsemateriell","lead":"Ferdige Fable Tour-bannere. Kopier koden med lenken din, eller last ned filen.","all":"Alle","png":"Stillbilde","gif":"Animert bilde","html":"Animert HTML","download":"Last ned","copy":"Kopier kode","copied":"Kopiert","back":"Tilbake til panelet","static":"Stille","animated":"Animert"},"sk":{"title":"Reklamné materiály | Fable Tour","eye":"Reklama","h1":"Reklamné materiály","lead":"Hotové bannery Fable Tour. Skopírujte kód so svojím odkazom alebo stiahnite súbor.","all":"Všetko","png":"Statický obrázok","gif":"Animovaný obrázok","html":"Animované HTML","download":"Stiahnuť","copy":"Kopírovať kód","copied":"Skopírované","back":"Späť na nástenku","static":"Statický","animated":"Animovaný"},"hr":{"title":"Promotivni materijali | Fable Tour","eye":"Oglasi","h1":"Promotivni materijali","lead":"Gotovi natpisi Fable Tour. Kopirajte kod sa svojom poveznicom ili preuzmite datoteku.","all":"Sve","png":"Nepomična slika","gif":"Animirana slika","html":"Animirani HTML","download":"Preuzmi","copy":"Kopiraj kod","copied":"Kopirano","back":"Natrag na ploču","static":"Nepomično","animated":"Animirano"},"ro":{"title":"Materiale publicitare | Fable Tour","eye":"Reclame","h1":"Materiale publicitare","lead":"Bannere gata făcute Fable Tour. Copiați codul cu linkul dvs. sau descărcați fișierul.","all":"Toate","png":"Imagine statică","gif":"Imagine animată","html":"HTML animat","download":"Descarcă","copy":"Copiază codul","copied":"Copiat","back":"Înapoi la panou","static":"Static","animated":"Animat"},"nl":{"title":"Reclamemateriaal | Fable Tour","eye":"Advertenties","h1":"Reclamemateriaal","lead":"Kant-en-klare Fable Tour-banners. Kopieer de code met jouw link of download het bestand.","all":"Alles","png":"Stilstaand beeld","gif":"Bewegend beeld","html":"Bewegende HTML","download":"Downloaden","copy":"Code kopiëren","copied":"Gekopieerd","back":"Terug naar mijn paneel","static":"Stil","animated":"Bewegend"},"ka":{"title":"სარეკლამო მასალა | Fable Tour","eye":"რეკლამა","h1":"სარეკლამო მასალა","lead":"მზა Fable Tour ბანერები. დააკოპირეთ კოდი თქვენი ბმულით ან გადმოწერეთ ფაილი.","all":"ყველა","png":"უძრავი სურათი","gif":"მოძრავი სურათი","html":"მოძრავი HTML","download":"გადმოწერა","copy":"კოდის კოპირება","copied":"დაკოპირდა","back":"პანელზე დაბრუნება","static":"უძრავი","animated":"მოძრავი"},"ko":{"title":"광고 자료 | Fable Tour","eye":"광고","h1":"광고 자료","lead":"준비된 Fable Tour 배너입니다. 추천 링크가 들어간 코드를 복사하거나 파일을 받으세요.","all":"전체","png":"정지 이미지","gif":"움직이는 이미지","html":"움직이는 HTML","download":"다운로드","copy":"코드 복사","copied":"복사됨","back":"대시보드로","static":"정지","animated":"움직임"},"pt":{"title":"Materiais publicitários | Fable Tour","eye":"Anúncios","h1":"Materiais publicitários","lead":"Banners prontos da Fable Tour. Copie o código com a sua ligação ou transfira o ficheiro.","all":"Tudo","png":"Imagem fixa","gif":"Imagem animada","html":"HTML animado","download":"Transferir","copy":"Copiar código","copied":"Copiado","back":"Voltar ao painel","static":"Fixa","animated":"Animada"},"vi":{"title":"Tài liệu quảng cáo | Fable Tour","eye":"Quảng cáo","h1":"Tài liệu quảng cáo","lead":"Biểu ngữ Fable Tour sẵn có. Sao chép mã kèm liên kết của bạn hoặc tải tệp.","all":"Tất cả","png":"Ảnh tĩnh","gif":"Ảnh động","html":"HTML động","download":"Tải xuống","copy":"Sao chép mã","copied":"Đã sao chép","back":"Về bảng điều khiển","static":"Tĩnh","animated":"Động"},"hu":{"title":"Hirdetési anyagok | Fable Tour","eye":"Hirdetés","h1":"Hirdetési anyagok","lead":"Kész Fable Tour bannerek. Másolja a kódot a saját linkjével, vagy töltse le a fájlt.","all":"Mind","png":"Állókép","gif":"Animált kép","html":"Animált HTML","download":"Letöltés","copy":"Kód másolása","copied":"Másolva","back":"Vissza a panelre","static":"Álló","animated":"Animált"}};
  var SIZES = [[728,90],[300,250],[336,280],[160,600],[300,600],[320,50],[970,250],[1080,1080],[1080,1920]];
  var NAMES = { ar: "العربية", ckb: "کوردی", en: "English", tr: "Türkçe", ru: "Русский", de: "Deutsch", fr: "Français", es: "Español", it: "Italiano", el: "Ελληνικά", cs: "Čeština", pl: "Polski", zh: "简体中文", "zh-tw": "繁體中文", ja: "日本語", fa: "فارسی", ms: "Melayu", id: "Indonesia", th: "ไทย", hi: "हिन्दी", ur: "اردو", ta: "தமிழ்", fi: "Suomi", sv: "Svenska", da: "Dansk", no: "Norsk", sk: "Slovenčina", hr: "Hrvatski", ro: "Română", nl: "Nederlands", ka: "ქართული", ko: "한국어", pt: "Português", vi: "Tiếng Việt", hu: "Magyar" };
  var LANG_LABEL = { ar: "لغة البانر", ckb: "زمانی بانەر", en: "Banner language", tr: "Afiş dili", ru: "Язык баннера", de: "Bannersprache", fr: "Langue de la bannière", es: "Idioma del banner", it: "Lingua del banner", el: "Γλώσσα banner", cs: "Jazyk banneru", pl: "Język banera", zh: "横幅语言", "zh-tw": "橫幅語言", ja: "バナーの言語", fa: "زبان بنر", ms: "Bahasa sepanduk", id: "Bahasa spanduk", th: "ภาษาแบนเนอร์", hi: "बैनर की भाषा", ur: "بینر کی زبان", ta: "பதாகை மொழி", fi: "Bannerin kieli", sv: "Banner språk", da: "Banner sprog", no: "Banner språk", sk: "Jazyk bannera", hr: "Jezik bannera", ro: "Limba bannerului", nl: "Bannertaal", ka: "ბანერის ენა", ko: "배너 언어", pt: "Língua do banner", vi: "Ngôn ngữ biểu ngữ", hu: "Banner nyelve" };
  var current = "ar";
  var bannerLang = "";
  var bannerTouched = false;
  var code = "";
  var sizeFilter = "all";
  var typeFilter = "all";
  function known(c) { return !!(c && PACKS[c]); }
  function norm(raw) {
    var s = String(raw || "").toLowerCase().replace(/_/g, "-");
    if (known(s)) return s;
    if (ALIAS[s]) return ALIAS[s];
    if (s.indexOf("zh-hant") === 0 || s.indexOf("zh-tw") === 0) return "zh-tw";
    var p = s.split("-")[0];
    if (known(p)) return p;
    if (ALIAS[p]) return ALIAS[p];
    return "";
  }
  function detect() {
    var q = "", saved = "", nav = "";
    try { q = new URLSearchParams(location.search).get("lang") || ""; } catch (e) {}
    try { saved = localStorage.getItem("ft_aff_lang") || ""; } catch (e) {}
    try { nav = (navigator.languages && navigator.languages[0]) || navigator.language || ""; } catch (e) {}
    return norm(q) || norm(saved) || norm(nav) || "ar";
  }
  function t(key) {
    if (key === "langLabel") return LANG_LABEL[current] || LANG_LABEL.en;
    var pack = PACKS[current] || PACKS.en;
    return (pack && pack[key]) || PACKS.en[key] || key;
  }
  function bannerCode() {
    return known(bannerLang) ? bannerLang : current;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }
  function apply(force, updateUrl) {
    current = norm(force) || detect();
    document.documentElement.lang = current;
    document.documentElement.dir = RTL[current] ? "rtl" : "ltr";
    document.querySelectorAll("[data-mat]").forEach(function (el) { el.textContent = t(el.getAttribute("data-mat")); });
    if (!bannerTouched) bannerLang = current;
    syncLangSelect();
    if (document.body && document.body.getAttribute("data-page") === "materials") document.title = t("title");
    var sel = document.getElementById("langSel");
    if (sel) sel.value = current;
    try { localStorage.setItem("ft_aff_lang", current); } catch (e) {}
    if (updateUrl) {
      var url = new URL(location.href);
      url.searchParams.set("lang", current);
      history.replaceState(null, "", url.pathname + url.search + url.hash);
    }
    labelFilters();
    if (code) draw();
    return current;
  }
  function file(type, w, h) {
    var lang = bannerCode();
    if (type === "html") return "/affiliate/materials/html/" + lang + "/" + w + "x" + h + ".html";
    return "/affiliate/materials/" + type + "/" + lang + "/" + w + "x" + h + "." + (type === "png" ? "png" : "gif");
  }
  function abs(path) { return "https://iraq.fabletour.com" + path; }
  function site(lang) {
    return lang === "ar" ? "https://iraq.fabletour.com/" : "https://iraq.fabletour.com/" + lang + "/";
  }
  function syncLangSelect() {
    var sel = document.getElementById("mat-lang");
    var label = document.querySelector("[data-mat-langlabel]");
    if (label) label.textContent = t("langLabel");
    if (!sel) return;
    if (!sel.dataset.ready) {
      Object.keys(NAMES).forEach(function (id) {
        var opt = document.createElement("option");
        opt.value = id;
        opt.textContent = NAMES[id];
        sel.appendChild(opt);
      });
      sel.dataset.ready = "1";
      sel.addEventListener("change", function () {
        bannerTouched = true;
        bannerLang = sel.value;
        draw();
      });
    }
    if (sel.value !== bannerCode()) sel.value = bannerCode();
  }
  function embed(type, w, h) {
    var href = site(bannerCode()) + "?ref=" + encodeURIComponent(code);
    if (type === "html") {
      return '<iframe src="' + abs(file(type, w, h)) + "?ref=" + encodeURIComponent(code) + '" width="' + w + '" height="' + h + '" style="border:0;overflow:hidden" scrolling="no" title="Fable Tour Iraq"></iframe>';
    }
    return '<a href="' + href + '" target="_blank" rel="noopener"><img src="' + abs(file(type, w, h)) + '" width="' + w + '" height="' + h + '" alt="Fable Tour Iraq"></a>';
  }
  function matches(type) {
    if (typeFilter === "all") return true;
    if (typeFilter === "static") return type === "png";
    if (typeFilter === "animated") return type !== "png";
    return type === typeFilter;
  }
  function kindLabel(type) {
    return type === "png" ? t("png") : type === "gif" ? t("gif") : t("html");
  }
  function draw() {
    var root = document.getElementById("mat-grid");
    if (!root) return;
    var html = "";
    var n = 0;
    SIZES.forEach(function (s) {
      ["png", "gif", "html"].forEach(function (type) {
        if (sizeFilter !== "all" && sizeFilter !== s[0] + "x" + s[1]) return;
        if (!matches(type)) return;
        var i = n++;
        var label = s[0] + "×" + s[1];
        var scale = Math.min(1, 280 / s[0], 260 / s[1]);
        var prev = type === "html"
          ? '<iframe title="Fable Tour" scrolling="no" src="' + file("html", s[0], s[1]) + "?ref=" + encodeURIComponent(code) + '" width="' + s[0] + '" height="' + s[1] + '" style="width:' + s[0] + 'px;height:' + s[1] + 'px;transform:scale(' + scale + ');transform-origin:center center"></iframe>'
          : '<img alt="" src="' + file(type, s[0], s[1]) + '">';
        var wide = s[0] > s[1] * 2 ? " wide" : "";
        html += '<article class="mat"><div class="mat-prev' + wide + '">' + prev + '</div><b class="dim" dir="ltr">' + label + " · " + esc(kindLabel(type)) + '</b><div class="row"><a class="btn slim" href="' + file(type, s[0], s[1]) + '" download>' + esc(t("download")) + '</a><button class="btn slim" type="button" data-copy="' + i + '">' + esc(t("copy")) + '</button></div><textarea readonly id="emb-' + i + '">' + esc(embed(type, s[0], s[1])) + '</textarea></article>';
      });
    });
    root.innerHTML = html;
    root.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var text = document.getElementById("emb-" + btn.getAttribute("data-copy")).value;
        var done = function () {
          var old = btn.textContent;
          btn.textContent = t("copied");
          setTimeout(function () { btn.textContent = old; }, 1600);
        };
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
        else fallback(text, done);
      });
    });
  }
  function fallback(text, done) {
    var area = document.createElement("textarea");
    area.value = text;
    area.style.cssText = "position:fixed;opacity:0";
    document.body.appendChild(area);
    area.select();
    try { document.execCommand("copy"); } catch (e) {}
    area.remove();
    done();
  }
  function labelFilters() {
    var box = document.getElementById("mat-filters");
    if (!box) return;
    box.querySelectorAll("button").forEach(function (btn) {
      var kind = btn.getAttribute("data-kind");
      var value = btn.getAttribute("data-value");
      if (kind === "size" && value === "all") btn.textContent = t("all");
      if (kind === "type" && value === "static") btn.textContent = t("static");
      if (kind === "type" && value === "animated") btn.textContent = t("animated");
      var on = (kind === "size" && value === sizeFilter) || (kind === "type" && value === typeFilter);
      btn.classList.toggle("on", on);
    });
  }
  function bindFilters() {
    var box = document.getElementById("mat-filters");
    if (!box || box.dataset.bound) return;
    box.dataset.bound = "1";
    box.addEventListener("click", function (event) {
      var btn = event.target.closest("button");
      if (!btn) return;
      var kind = btn.getAttribute("data-kind");
      var value = btn.getAttribute("data-value");
      if (kind === "size") sizeFilter = value;
      else typeFilter = typeFilter === value ? "all" : value;
      labelFilters();
      draw();
    });
  }
  window.FTMaterials = {
    apply: apply,
    show: function (referral) {
      code = String(referral || "").toUpperCase();
      apply();
      var app = document.getElementById("app");
      if (app) app.hidden = false;
      var who = document.getElementById("mat-code");
      if (who) who.textContent = code;
      bindFilters();
      labelFilters();
      draw();
    }
  };
  function boot() {
    apply();
    if (window.__ftMatPreview && document.body && document.body.getAttribute("data-page") === "materials") {
      window.FTMaterials.show(window.__ftMatPreview);
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
