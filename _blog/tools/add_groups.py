#!/usr/bin/env python3
"""Adds the 'group departures' block (3 dates + Book button) to both programmes
on every language homepage, plus a group-date field in the booking form.
Dates are recalculated in the browser every visit (7 days: every Friday;
9 days: first Friday of each month); the HTML also carries today's dates as a fallback.
Idempotent: re-running refreshes the fallback dates."""
import re, json, glob, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
I18N = json.loads((ROOT / "_blog" / "i18n.json").read_text())

S = {
"en": ["Group departures","Next group dates","Join a small group on one of these dates — same price, {price} per person in a double room.","Book","Group date","Private tour — I'll choose my date"],
"ar": ["رحلات جماعية","مواعيد الكروبات القادمة","انضم إلى مجموعة صغيرة في أحد هذه المواعيد — بنفس السعر، {price} للشخص في الغرفة المزدوجة.","احجز","موعد الكروب","رحلة خاصة — أختار التاريخ بنفسي"],
"ru": ["Групповые туры","Ближайшие даты групп","Присоединяйтесь к небольшой группе в одну из этих дат — по той же цене, {price} за человека в двухместном номере.","Забронировать","Дата группы","Индивидуальный тур — выберу дату сам"],
"de": ["Gruppenreisen","Nächste Gruppentermine","Reisen Sie in einer kleinen Gruppe an einem dieser Termine – zum gleichen Preis, {price} pro Person im Doppelzimmer.","Buchen","Gruppentermin","Private Reise – Termin nach Wahl"],
"fr": ["Départs en groupe","Prochaines dates de groupe","Rejoignez un petit groupe à l'une de ces dates — même prix, {price} par personne en chambre double.","Réserver","Date du groupe","Circuit privé — je choisis ma date"],
"es": ["Salidas en grupo","Próximas fechas de grupo","Únete a un grupo reducido en una de estas fechas — mismo precio, {price} por persona en habitación doble.","Reservar","Fecha del grupo","Tour privado — elijo mi fecha"],
"it": ["Partenze di gruppo","Prossime date di gruppo","Unisciti a un piccolo gruppo in una di queste date — stesso prezzo, {price} a persona in camera doppia.","Prenota","Data del gruppo","Tour privato — scelgo io la data"],
"el": ["Ομαδικές αναχωρήσεις","Επόμενες ημερομηνίες ομάδων","Ταξιδέψτε με μια μικρή ομάδα σε μία από αυτές τις ημερομηνίες — στην ίδια τιμή, {price} ανά άτομο σε δίκλινο.","Κράτηση","Ημερομηνία ομάδας","Ιδιωτική περιήγηση — επιλέγω ημερομηνία"],
"cs": ["Skupinové odjezdy","Nejbližší termíny skupin","Připojte se k malé skupině v jednom z těchto termínů — za stejnou cenu, {price} na osobu ve dvoulůžkovém pokoji.","Rezervovat","Termín skupiny","Soukromý zájezd — termín si zvolím"],
"pl": ["Wyjazdy grupowe","Najbliższe terminy grup","Dołącz do małej grupy w jednym z tych terminów — w tej samej cenie, {price} za osobę w pokoju dwuosobowym.","Zarezerwuj","Termin grupy","Wycieczka prywatna — sam wybiorę termin"],
"zh": ["拼团出发","近期团期","选择以下任一日期加入小团——价格不变，每人{price}（双人间）。","预订","团期","私人团——自选日期"],
"ja": ["グループ出発","次回のグループ出発日","以下の日程で少人数グループにご参加いただけます。料金は同じく1名{price}（2名1室利用）です。","予約する","出発日","プライベートツアー（日程は自分で選ぶ）"],
"tr": ["Grup turları","Yaklaşan grup tarihleri","Bu tarihlerden birinde küçük bir gruba katılın — aynı fiyatla, iki kişilik odada kişi başı {price}.","Rezervasyon","Grup tarihi","Özel tur — tarihi ben seçerim"],
"fa": ["تورهای گروهی","تاریخ‌های گروهی پیش رو","در یکی از این تاریخ‌ها به یک گروه کوچک بپیوندید — با همان قیمت، {price} برای هر نفر در اتاق دوتخته.","رزرو","تاریخ گروه","تور خصوصی — تاریخ را خودم انتخاب می‌کنم"],
"ms": ["Trip berkumpulan","Tarikh kumpulan akan datang","Sertai kumpulan kecil pada salah satu tarikh ini — harga yang sama, {price} seorang dalam bilik berdua.","Tempah","Tarikh kumpulan","Lawatan persendirian — saya pilih tarikh"],
"id": ["Keberangkatan grup","Jadwal grup berikutnya","Bergabunglah dengan grup kecil di salah satu tanggal ini — harga sama, {price} per orang di kamar double.","Pesan","Tanggal grup","Tur privat — saya pilih tanggal sendiri"],
"th": ["ทัวร์กรุ๊ป","วันเดินทางกรุ๊ปถัดไป","ร่วมเดินทางกับกรุ๊ปเล็กในวันใดวันหนึ่งต่อไปนี้ ราคาเดิม {price} ต่อท่าน พักห้องคู่","จอง","วันเดินทางกรุ๊ป","ทัวร์ส่วนตัว — เลือกวันเอง"],
"hi": ["ग्रुप टूर","अगली ग्रुप तारीख़ें","इनमें से किसी तारीख़ पर एक छोटे ग्रुप में शामिल हों — वही कीमत, डबल रूम में प्रति व्यक्ति {price}।","बुक करें","ग्रुप की तारीख़","निजी टूर — तारीख़ मैं खुद चुनूँगा/चुनूँगी"],
"ur": ["گروپ ٹور","اگلی گروپ تاریخیں","ان میں سے کسی تاریخ پر ایک چھوٹے گروپ میں شامل ہوں — وہی قیمت، ڈبل روم میں فی کس {price}۔","بک کریں","گروپ کی تاریخ","پرائیویٹ ٹور — تاریخ میں خود چنوں گا"],
"ta": ["குழுப் பயணங்கள்","அடுத்த குழுப் பயணத் தேதிகள்","இந்தத் தேதிகளில் ஒன்றில் ஒரு சிறு குழுவுடன் இணையுங்கள் — அதே விலை, இரட்டை அறையில் ஒருவருக்கு {price}.","முன்பதிவு","குழுத் தேதி","தனிப்பட்ட சுற்றுலா — தேதியை நானே தேர்வு செய்வேன்"],
}
PRICE = {"7": "$2,500", "9": "$3,400"}
LEAD = {"7": 5, "9": 10}          # minimum days between today and the first date shown

def baghdad_today():
    return (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)).date()

def next_dates(tour, today):
    start = today + datetime.timedelta(days=LEAD[tour]); out = []
    if tour == "7":
        d = start + datetime.timedelta(days=(4 - start.weekday()) % 7)
        while len(out) < 3: out.append(d); d += datetime.timedelta(days=7)
    else:
        y, m = today.year, today.month
        while len(out) < 3:
            first = datetime.date(y, m, 1)
            ff = first + datetime.timedelta(days=(4 - first.weekday()) % 7)
            if ff >= start: out.append(ff)
            m += 1
            if m > 12: m, y = 1, y + 1
    return out

def fallback_label(l, d):
    t = I18N[l]
    return t["date"].format(d=d.day, M=t["months"][d.month - 1], y=d.year)

CSS = """
/* group departures */
.grp{margin:18px 0 8px;background:var(--panel);border-radius:6px;padding:18px 18px 16px;border-top:4px solid var(--gold)}
.grp h4{margin:4px 0 4px;font-family:var(--serif-en);font-weight:400;font-size:21px;color:var(--navy)}
html[lang="ar"] .grp h4,html[lang="fa"] .grp h4,html[lang="ur"] .grp h4{font-family:var(--serif-ar);font-weight:700;font-size:23px}
.grp p{margin:0;color:var(--muted);font-size:14.5px}
.grp-dates{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}
.gd{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:14px 12px;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;min-width:0}
.gd .gd-d{font-family:var(--serif-en);font-size:34px;line-height:1;color:var(--navy)}
.gd .gd-m{font-weight:600;color:var(--navy);font-size:15px}
.gd .gd-w{font-size:13px;color:var(--muted)}
.gd button{margin-top:4px;width:100%;background:var(--gold);color:var(--navy);border:0;border-radius:4px;padding:10px 12px;font:600 14px var(--sans-en);cursor:pointer}
html[lang="ar"] .gd button,html[lang="fa"] .gd button,html[lang="ur"] .gd button{font-family:var(--sans-ar)}
.gd button:hover{background:var(--navy);color:#EFE3C8}
@media (max-width:560px){.grp-dates{grid-template-columns:1fr}.gd{flex-direction:row;flex-wrap:wrap;justify-content:space-between;text-align:start;gap:4px 12px}.gd .gd-d{font-size:28px}.gd .gd-txt{flex:1;min-width:0}.gd button{width:auto;margin:0}}
"""

def block(l, tour, today):
    e, h, p, book, _, _ = S[l]
    cards = ""
    for d in next_dates(tour, today):
        cards += (f'<div class="gd" data-date="{d.isoformat()}"><span class="gd-d">{d.day}</span>'
                  f'<span class="gd-txt"><span class="gd-m" style="display:block">{fallback_label(l, d)}</span><span class="gd-w"></span></span>'
                  f'<button type="button" data-book="{tour}" data-date="{d.isoformat()}">{book}</button></div>')
    return (f'\n   <div class="grp" data-tour="{tour}"><span class="eyebrow">{e}</span><h4>{h}</h4>'
            f'<p>{p.replace("{price}", f"<span dir=\"ltr\">{PRICE[tour]}</span>")}</p><div class="grp-dates">{cards}</div></div>')

def js(l):
    e, h, p, book, lbl, anyd = S[l]
    return """<script>/* group departures */(function(){
var BOOK=%s,ANY=%s,LEAD={"7":5,"9":10},lang=document.documentElement.lang;
var loc=(lang.indexOf("ar")===0?"ar-u-nu-latn-ca-gregory":lang+"-u-ca-gregory");
function today(){var n=new Date(Date.now()+3*3600e3);return new Date(Date.UTC(n.getUTCFullYear(),n.getUTCMonth(),n.getUTCDate()));}
function add(d,k){return new Date(d.getTime()+k*864e5);}
function dates(t){var s=add(today(),LEAD[t]),o=[];if(t==="7"){var d=add(s,(5-s.getUTCDay()+7)%%7);while(o.length<3){o.push(d);d=add(d,7);}}
 else{var y=s.getUTCFullYear(),m=today().getUTCMonth();y=today().getUTCFullYear();while(o.length<3){var f=new Date(Date.UTC(y,m,1));f=add(f,(5-f.getUTCDay()+7)%%7);if(f>=s)o.push(f);m++;if(m>11){m=0;y++;}}}return o;}
function iso(d){return d.toISOString().slice(0,10);}
function part(d,o){try{return new Intl.DateTimeFormat(loc,Object.assign({timeZone:"UTC"},o)).format(d);}catch(e){return "";}}
function full(d){return part(d,{weekday:"long",day:"numeric",month:"long",year:"numeric"});}
var D={"7":dates("7"),"9":dates("9")};
document.querySelectorAll(".grp").forEach(function(g){var t=g.dataset.tour,box=g.querySelector(".grp-dates");box.innerHTML="";
 D[t].forEach(function(d){var c=document.createElement("div");c.className="gd";
  c.innerHTML='<span class="gd-d"></span><span class="gd-txt"><span class="gd-m" style="display:block"></span><span class="gd-w"></span></span><button type="button"></button>';
  c.querySelector(".gd-d").textContent=part(d,{day:"numeric"});c.querySelector(".gd-m").textContent=part(d,{month:"long",year:"numeric"});
  c.querySelector(".gd-w").textContent=part(d,{weekday:"long"});var b=c.querySelector("button");b.textContent=BOOK;b.dataset.book=t;b.dataset.date=iso(d);box.appendChild(c);});});
var prog=document.getElementById("f-prog"),sel=document.getElementById("f-date");
function fill(t,v){if(!sel)return;sel.innerHTML="";var a=document.createElement("option");a.value="";a.textContent=ANY;sel.appendChild(a);
 D[t].forEach(function(d){var o=document.createElement("option");o.value=iso(d)+" — "+full(d);o.textContent=full(d);if(v===iso(d))o.selected=true;sel.appendChild(o);});}
function tourOf(){return prog&&prog.selectedIndex===1?"9":"7";}
if(prog){prog.addEventListener("change",function(){fill(tourOf());});fill(tourOf());}
document.addEventListener("click",function(e){var b=e.target.closest("[data-book]");if(!b)return;var t=b.dataset.book;
 if(prog)prog.selectedIndex=(t==="9"?1:0);fill(t,b.dataset.date);
 var f=document.getElementById("interest");if(f)f.scrollIntoView({behavior:"smooth",block:"start"});
 setTimeout(function(){var n=document.getElementById("f-name");if(n)n.focus({preventScroll:true});},600);});
})();</script>
""" % (json.dumps(book, ensure_ascii=False), json.dumps(anyd, ensure_ascii=False))

def run():
    today = baghdad_today()
    files = {"ar": ROOT / "index.html", **{l: ROOT / l / "index.html" for l in S if l != "ar"}}
    for l, f in files.items():
        s = f.read_text()
        # remove previous version (idempotent)
        s = re.sub(r'\n   <div class="grp" data-tour="\d">.*?</div></div></div>', "", s, flags=re.S)
        s = re.sub(r'<script>/\* group departures \*/.*?</script>\n', "", s, flags=re.S)
        s = re.sub(r'\n/\* group departures \*/.*?(?=</style>)', "\n", s, count=1, flags=re.S)
        s = re.sub(r'<div class="field" id="f-date-field">.*?</div>', "", s, flags=re.S)
        # css
        i = s.find("</style>"); s = s[:i] + CSS + s[i:]
        # blocks at the end of each programme (below the last day)
        for tour in ("7", "9"):
            a = s.find(f'id="tour-{tour}-days"'); end = s.find("</section>", a)   # end of the programme
            s = s[:end] + block(l, tour, today) + "\n   " + s[end:]
        # form field after programme select
        lbl = S[l][4]
        m = re.search(r'(<div class="field"><label for="f-prog".*?</select></div>)', s, re.S)
        s = s[:m.end()] + f'<div class="field" id="f-date-field"><label for="f-date">{lbl}</label><select id="f-date" name="group_date"><option value="">{S[l][5]}</option></select></div>' + s[m.end():]
        # send the date with the booking
        if "group_date:" not in s:
            s = s.replace('tour:(document.getElementById("f-prog")||{}).value||"",',
                          'tour:(document.getElementById("f-prog")||{}).value||"",group_date:(document.getElementById("f-date")||{}).value||"",', 1)
            s = s.replace('subject:"Iraq Tour — New booking request: "+(document.getElementById("f-prog")||{}).value+"',
                          'subject:"Iraq Tour — New booking request: "+(document.getElementById("f-prog")||{}).value+((document.getElementById("f-date")||{}).value?" | Group "+document.getElementById("f-date").value.slice(0,10):"")+"', 1)
        # script before </body>
        i = s.rfind("</body>"); s = s[:i] + js(l) + s[i:]
        f.write_text(s)
        print(l, "ok", s.count('class="grp"'), "group_date:" in s)

if __name__ == "__main__":
    run()
