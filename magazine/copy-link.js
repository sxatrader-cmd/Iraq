/* Same control as the day-trip and tour pages: gold pill, link icon, copied state. */
(function(){
  var LABELS={
    ar:["نسخ رابط الرحلة","تم نسخ الرابط ✓"],
    ckb:["کۆپیکردنی بەستەری گەشتەکە","بەستەرەکە کۆپی کرا ✓"],
    en:["Copy trip link","Link copied ✓"],
    tr:["Bağlantıyı kopyala","Bağlantı kopyalandı ✓"],
    ru:["Скопировать ссылку","Ссылка скопирована ✓"],
    de:["Link kopieren","Link kopiert ✓"],
    fr:["Copier le lien","Lien copié ✓"],
    es:["Copiar enlace","Enlace copiado ✓"],
    it:["Copia il link","Link copiato ✓"],
    el:["Αντιγραφή συνδέσμου","Ο σύνδεσμος αντιγράφηκε ✓"],
    cs:["Kopírovat odkaz","Odkaz zkopírován ✓"],
    pl:["Kopiuj link","Link skopiowany ✓"],
    zh:["复制链接","链接已复制 ✓"],
    "zh-tw":["複製連結","連結已複製 ✓"],
    ja:["リンクをコピー","コピーしました ✓"],
    fa:["کپی لینک سفر","لینک کپی شد ✓"],
    ms:["Salin pautan","Pautan disalin ✓"],
    id:["Salin tautan","Tautan disalin ✓"],
    th:["คัดลอกลิงก์","คัดลอกลิงก์แล้ว ✓"],
    hi:["लिंक कॉपी करें","लिंक कॉपी हो गया ✓"],
    ur:["لنک کاپی کریں","لنک کاپی ہو گیا ✓"],
    ta:["இணைப்பை நகலெடு","இணைப்பு நகலெடுக்கப்பட்டது ✓"],
    fi:["Kopioi retken linkki","Linkki kopioitu ✓"],
    sv:["Kopiera länk till utflykten","Länken är kopierad ✓"],
    da:["Kopiér link til turen","Linket er kopieret ✓"],
    no:["Kopier lenke til turen","Lenken er kopiert ✓"],
    sk:["Kopírovať odkaz","Odkaz skopírovaný ✓"],
    hr:["Kopiraj poveznicu","Poveznica kopirana ✓"],
    ro:["Copiază linkul","Link copiat ✓"],
    nl:["Link kopiëren","Link gekopieerd ✓"],
    ka:["ბმულის კოპირება","ბმული დაკოპირდა ✓"],
    ko:["링크 복사","링크가 복사되었습니다 ✓"],
    pt:["Copiar link","Link copiado ✓"],
    vi:["Sao chép liên kết","Đã sao chép liên kết ✓"],
    hu:["Link másolása","Link kimásolva ✓"]
  };
  if(!document.getElementById("pc-cp-css")){
    var st=document.createElement("style");
    st.id="pc-cp-css";
    st.textContent="button.pc-cp{display:inline-flex;align-items:center;gap:6px;height:38px;min-width:0;max-width:100%;background:transparent;border:1px solid var(--gold,#C5A46A);color:var(--gold-2,#E7D7B1);border-radius:999px;padding:0 12px;font:inherit;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap}"
      +"button.pc-cp svg{width:14px;height:14px;flex:none}"
      +"button.pc-cp:hover{background:var(--gold,#C5A46A);color:var(--navy,#0C2746)}"
      +"button.pc-cp.ok{background:#E3F4E8;border-color:#7CC492;color:#1D6B37}";
    document.head.appendChild(st);
  }
  var bar=document.getElementById("bar");
  if(!bar||document.getElementById("copyLink")) return;
  var lang=(document.documentElement.lang||"en").toLowerCase();
  var L=LABELS[lang]||LABELS.en;
  var btn=document.createElement("button");
  btn.type="button";
  btn.className="pc-cp";
  btn.id="copyLink";
  btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.5-1.5"/></svg><span></span>';
  var span=btn.querySelector("span");
  span.textContent=L[0];
  var snd=document.getElementById("snd");
  if(snd) bar.insertBefore(btn,snd); else bar.appendChild(btn);
  function editionUrl(){
    var path=location.pathname;
    if(path.slice(-1)!=="/") path+="/";
    return location.origin+path;
  }
  function fallback(u){
    var t=document.createElement("textarea");
    t.value=u; t.setAttribute("readonly","");
    t.style.cssText="position:fixed;top:0;opacity:0";
    document.body.appendChild(t); t.select(); t.setSelectionRange(0,u.length);
    try{document.execCommand("copy");}catch(e){}
    t.remove();
  }
  btn.addEventListener("click",function(e){
    e.stopPropagation();
    var u=editionUrl();
    function ok(){
      btn.classList.add("ok");
      span.textContent=L[1];
      clearTimeout(btn._t);
      btn._t=setTimeout(function(){btn.classList.remove("ok"); span.textContent=L[0];},2400);
    }
    if(navigator.clipboard&&window.isSecureContext){
      navigator.clipboard.writeText(u).then(ok,function(){fallback(u); ok();});
    }else{fallback(u); ok();}
  });
})();
