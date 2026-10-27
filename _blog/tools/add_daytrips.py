#!/usr/bin/env python3
"""Adds the 'Day trips from Baghdad' section (collapsed until clicked) to every language
homepage, plus a third card in 'Choose your programme'. Idempotent (re-run to update).
Prices are calculated in the browser from the formulas in PRICES below."""
import re, json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((pathlib.Path(__file__).parent / "daytrips_i18n.json").read_text())
LANGS = ["ar", "en", "ru", "de", "fr", "es", "it", "el", "cs", "pl", "zh", "ja", "tr", "fa", "ms", "id", "th"]
ORDER = ["aqarquf", "madain", "samarra", "babylon", "babylon4", "holy", "south"]

# price for n people (total for the group, USD) — same formulas are used in the page script
JS_PRICES = """{
 babylon:function(n){return n<2?200:240+50*(n-2)},
 babylon4:function(n){return n<2?220:260+40*(n-2)},
 holy:function(n){return 239+30*Math.max(0,n-3)},
 south:function(n){return [300,325,350][n-1]||350+40*(n-3)},
 samarra:function(n){return [150,200,225][n-1]||225+25*(n-3)},
 madain:function(n){return 100+25*(n-1)},
 aqarquf:function(n){return 50+25*(n-1)}
}"""
FROM = {"babylon": 200, "babylon4": 220, "holy": 239, "south": 300, "samarra": 150, "madain": 100, "aqarquf": 50}
IMG_Q = {}
PX = lambda i: f"https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg?auto=compress&cs=tinysrgb&w=900"
# free-licence photos (Pexels licence / Saif's own photo) — no credit shown
LOCAL_IMG = {"aqarquf": "img/aqar-quf-ziggurat.webp", "samarra": ["img/samarra-malwiya.webp", "img/samarra-2.webp"], "babylon": "img/babylon-ishtar-gate.webp",
             "babylon4": "img/borsippa-ziggurat.webp", "madain": "img/taq-kasra.webp", "holy": "img/kufa-great-mosque.webp", "south": ["img/marshes-mashoof.webp", "img/ur-ziggurat.webp", "img/marshes-mudhif.webp", "img/marshes-buffalo.webp"]}
MAXP = 12
COUNT = '<span class="dt-cnt" dir="ltr" aria-hidden="true">1 / {n}</span>'
ZOOM = '<span class="dt-zoom" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.5-4.5M11 8v6M8 11h6"/></svg></span>'

CSS = """
/* day trips */
.pcards{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))!important}
.dt-toggle{width:100%;display:flex;align-items:center;justify-content:space-between;gap:14px;background:var(--navy);color:#fff;border:0;border-radius:6px;padding:20px 22px;cursor:pointer;text-align:start;border-bottom:4px solid var(--gold)}
.dt-toggle .eyebrow{color:var(--gold-2)}
.dt-toggle b{display:block;font-family:var(--serif-en);font-weight:400;font-size:clamp(22px,3.6vw,28px);line-height:1.3;margin-top:4px}
html[lang="ar"] .dt-toggle b,html[lang="fa"] .dt-toggle b{font-family:var(--serif-ar);font-weight:700}
.dt-toggle small{display:block;color:#C9CFD9;font-size:14px;margin-top:4px}
.dt-toggle .dt-chev{flex:none;width:42px;height:42px;border-radius:50%;background:var(--gold);color:var(--navy);display:grid;place-items:center;transition:transform .25s}
.dt-toggle[aria-expanded="true"] .dt-chev{transform:rotate(180deg)}
.dt-note{margin:14px 2px 0;color:var(--muted);font-size:14px}
.dt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin-top:14px}
.dt{background:var(--paper);border:1px solid var(--line);border-radius:6px;overflow:hidden;display:flex;flex-direction:column}
.dt-ph{position:relative;aspect-ratio:16/10;background:var(--navy-2) center/cover no-repeat;filter:saturate(1.35) contrast(1.06) brightness(1.03)}
.dt-ph.none{filter:none}
.dt-ph[data-full]{cursor:zoom-in}
.dt-zoom{position:absolute;inset-inline-end:8px;bottom:8px;width:32px;height:32px;border-radius:50%;background:rgba(18,26,43,.55);color:#fff;display:grid;place-items:center;filter:none}
.dt-cnt{position:absolute;inset-inline-start:8px;bottom:8px;background:rgba(18,26,43,.55);color:#fff;font:600 12px var(--sans-en);padding:4px 8px;border-radius:999px;filter:none}
.dt-lb .nav{position:absolute;top:50%;transform:translateY(-50%);width:46px;height:46px;border-radius:50%;border:0;background:rgba(255,255,255,.85);color:var(--navy);font-size:26px;cursor:pointer;inset-inline-end:auto}
.dt-lb .prev{left:10px}.dt-lb .next{right:10px;left:auto}
.dt-lb .ct{position:absolute;bottom:max(16px,env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);color:#fff;font:600 13px var(--sans-en)}
.dt-lb{position:fixed;inset:0;z-index:60;background:rgba(10,15,28,.94);display:grid;place-items:center;padding:16px;touch-action:pinch-zoom}
.dt-lb img{max-width:100%;max-height:88vh;border-radius:4px;box-shadow:0 20px 60px rgba(0,0,0,.6);filter:saturate(1.3) contrast(1.05)}
.dt-lb .x{position:absolute;top:max(14px,env(safe-area-inset-top,0px));inset-inline-end:14px;width:44px;height:44px;border-radius:50%;border:0;background:var(--gold);color:var(--navy);font-size:24px;font-weight:700;cursor:pointer}
.dt-ph.none{background-size:56px;background-repeat:repeat;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='56' viewBox='0 0 56 56'%3E%3Cg fill='none' stroke='%23B8955A' stroke-width='1.2' opacity='.4'%3E%3Cpath d='M28 4 52 28 28 52 4 28z'/%3E%3Ccircle cx='28' cy='28' r='7'/%3E%3C/g%3E%3C/svg%3E")}
.dt-bd{padding:16px;display:flex;flex-direction:column;gap:8px;flex:1}
.dt-bd h3{font-family:var(--serif-en);font-weight:400;font-size:20px;color:var(--navy);line-height:1.3}
html[lang="ar"] .dt-bd h3,html[lang="fa"] .dt-bd h3{font-family:var(--serif-ar);font-weight:700;font-size:22px}
.dt-s{margin:0;font-size:14px;color:var(--muted);line-height:1.55}
.dt-inc{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 0;padding:0;list-style:none}
.dt-inc li{font-size:12.5px;background:var(--panel);color:var(--navy);border-radius:999px;padding:3px 10px}
.dt-inc li::before{content:"✓ ";color:var(--gold)}
.dt-calc{margin-top:auto;border-top:1px solid var(--line);padding-top:12px;display:grid;grid-template-columns:auto 1fr;gap:10px 12px;align-items:end}
.dt-pp{display:flex;flex-direction:column;gap:4px}
.dt-calc label{font-size:12px;color:var(--muted);letter-spacing:.04em;text-transform:none;font-weight:600}
.dt-step{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:4px;overflow:hidden}
.dt-step button{width:34px;height:34px;border:0;background:var(--panel);color:var(--navy);font-size:18px;cursor:pointer}
.dt-step output{min-width:34px;text-align:center;font-weight:600;color:var(--navy)}
.dt-total{justify-self:end;text-align:end}
.dt-total span{display:block;font-size:11.5px;color:var(--muted)}
.dt-total b{font-family:var(--serif-en);font-size:26px;font-weight:400;color:var(--navy);font-variant-numeric:tabular-nums}
.dt-book{grid-column:1/-1;display:flex;align-items:center;justify-content:center;gap:8px;background:#25D366;color:#fff;text-decoration:none;font-weight:600;font-size:14.5px;border-radius:4px;padding:11px 14px}
.dt-book:hover{filter:brightness(.95)}
"""

def esc(s): return html.escape(s, quote=True)

def section(l):
    u = D[l]["ui"]; T = D[l]["trips"]
    cards = ""
    for k in ORDER:
        title, stops, inc = T[k]
        img = ""
        if k in LOCAL_IMG:
            lst = LOCAL_IMG[k] if isinstance(LOCAL_IMG[k], list) else [LOCAL_IMG[k]]
            lst = [u if u.startswith("http") else ("" if l == "ar" else "../") + u for u in lst]
            src = lst[0]
            full = "|".join(u.replace("w=900", "w=1800") for u in lst)
            img = f' style="background-image:url(\'{src}\')" data-full="{esc(full)}" tabindex="0"'
        incs = "".join(f"<li>{esc(x)}</li>" for x in inc)
        cards += f"""<article class="dt" data-trip="{k}">
  <div class="dt-ph{'' if img else ' none'}"{img} role="{'button' if img else 'img'}" aria-label="{esc(title)}">{ZOOM if img else ''}{COUNT.format(n=len(LOCAL_IMG[k])) if isinstance(LOCAL_IMG.get(k), list) else ''}</div>
  <div class="dt-bd">
    <h3>{esc(title)}</h3>
    <p class="dt-s">{esc(stops)}</p>
    {f'<ul class="dt-inc" aria-label="{esc(u["inc"])}">{incs}</ul>' if incs else ''}
    <div class="dt-calc">
      <div class="dt-pp"><label>{esc(u["trav"])}</label><div class="dt-step"><button type="button" data-d="-1" aria-label="−">−</button><output>1</output><button type="button" data-d="1" aria-label="+">+</button></div></div>
      <div class="dt-total"><span>{esc(u["total"])}</span><b dir="ltr">${FROM[k]}</b></div>
      <a class="dt-book" href="https://wa.me/9647711745353" target="_blank" rel="noopener">{esc(u["book"])}</a>
    </div>
  </div>
</article>"""
    chev = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    return f"""
  <section class="block in" style="padding-top:0" id="day-trips">
    <button class="dt-toggle" type="button" aria-expanded="false" aria-controls="dt-body" data-show="{esc(u['show'])}" data-hide="{esc(u['hide'])}">
      <span><span class="eyebrow">{esc(u['eye'])} · <span dir="ltr">{esc(u['from'])} $50</span></span><b>{esc(u['h'])}</b><small class="dt-lbl">{esc(u['show'])}</small></span>
      <span class="dt-chev">{chev}</span>
    </button>
    <div id="dt-body" hidden>
      <p class="dt-note">{esc(u['p'])}</p>
      <div class="dt-grid">{cards}</div>
    </div>
  </section>
"""

def pcard(l):
    u = D[l]["ui"]
    route = " · ".join(D[l]["trips"][k][0] for k in ["aqarquf", "madain", "samarra", "babylon", "holy", "south"])
    arrow = "←" if l in ("ar", "fa") else "→"
    return (f'<a class="pcard" href="#day-trips" data-open-dt><span class="eyebrow">{esc(u["card_e"])}</span>'
            f'<b class="disp">{esc(u["card_t"])}</b><span class="r">{esc(route)}</span>'
            f'<span class="pp" dir="ltr">${50}+</span><span class="ppk">{esc(u["pg"])}</span><span class="go">{esc(u["card_go"])}</span></a>')

def script(l):
    u = D[l]["ui"]
    T = {k: D[l]["trips"][k][0] for k in ORDER}
    return """<script>/* day trips */(function(){
var P=%s,U=%s,T=%s,MAX=%d,loaded=false;
var tg=document.querySelector(".dt-toggle"),body=document.getElementById("dt-body");if(!tg||!body)return;
function setOpen(o){body.hidden=!o;tg.setAttribute("aria-expanded",o);tg.querySelector(".dt-lbl").textContent=o?tg.dataset.hide:tg.dataset.show;if(o)loadImgs();}
tg.addEventListener("click",function(){setOpen(body.hidden);});
document.querySelectorAll("[data-open-dt]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();setOpen(true);document.getElementById("day-trips").scrollIntoView({behavior:"smooth",block:"start"});});});
if(location.hash==="#day-trips")setOpen(true);
function fmt(v){return "$"+v.toLocaleString("en-US");}
document.querySelectorAll(".dt").forEach(function(c){var k=c.dataset.trip,n=1,out=c.querySelector("output"),tot=c.querySelector(".dt-total b"),bk=c.querySelector(".dt-book");
 function upd(){out.textContent=n;var p=fmt(P[k](n));tot.textContent=p;bk.href="https://wa.me/9647711745353?text="+encodeURIComponent(U.wa.replace("{trip}",T[k]).replace("{n}",n).replace("{price}",p));}
 c.querySelectorAll(".dt-step button").forEach(function(b){b.addEventListener("click",function(){n=Math.min(MAX,Math.max(1,n+(+b.dataset.d)));upd();});});upd();});
function loadImgs(){}
function lb(list,alt){var idx=0,o=document.createElement("div");o.className="dt-lb";o.dir="ltr";o.setAttribute("role","dialog");o.setAttribute("aria-modal","true");
 var i=document.createElement("img");i.alt=alt;var x=document.createElement("button");x.type="button";x.className="x";x.setAttribute("aria-label","×");x.textContent="×";
 o.appendChild(i);o.appendChild(x);var ct=null;
 function show(){i.src=list[idx];if(ct)ct.textContent=(idx+1)+" / "+list.length;}
 function go(d){idx=(idx+d+list.length)%%list.length;show();}
 if(list.length>1){var p=document.createElement("button");p.type="button";p.className="nav prev";p.textContent="‹";p.setAttribute("aria-label","‹");
  var n=document.createElement("button");n.type="button";n.className="nav next";n.textContent="›";n.setAttribute("aria-label","›");
  p.addEventListener("click",function(e){e.stopPropagation();go(-1);});n.addEventListener("click",function(e){e.stopPropagation();go(1);});
  ct=document.createElement("span");ct.className="ct";o.appendChild(p);o.appendChild(n);o.appendChild(ct);
  var sx=null;o.addEventListener("touchstart",function(e){if(e.touches.length===1)sx=e.touches[0].clientX;},{passive:true});
  o.addEventListener("touchend",function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)go(dx<0?1:-1);sx=null;});}
 show();document.body.appendChild(o);document.body.style.overflow="hidden";x.focus();
 function close(){o.remove();document.body.style.overflow="";document.removeEventListener("keydown",k);}
 function k(e){if(e.key==="Escape")close();else if(e.key==="ArrowRight")go(1);else if(e.key==="ArrowLeft")go(-1);}document.addEventListener("keydown",k);
 o.addEventListener("click",function(e){if(e.target===o||e.target===x)close();});}
document.querySelectorAll(".dt-ph[data-full]").forEach(function(ph){function open(){lb(ph.dataset.full.split("|"),ph.getAttribute("aria-label"));}
 ph.addEventListener("click",open);ph.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();open();}});});
})();</script>
""" % (JS_PRICES, json.dumps({"wa": u["wa"]}, ensure_ascii=False), json.dumps(T, ensure_ascii=False), MAXP)

def run():
    for l in LANGS:
        f = ROOT / ("index.html" if l == "ar" else f"{l}/index.html")
        s = f.read_text()
        # remove previous version
        s = re.sub(r'\n  <section class="block in" style="padding-top:0" id="day-trips">.*?</section>\n', "", s, flags=re.S)
        s = re.sub(r'<script>/\* day trips \*/.*?</script>\n', "", s, flags=re.S)
        s = re.sub(r'\n/\* day trips \*/.*?(?=</style>)', "\n", s, count=1, flags=re.S)
        s = re.sub(r'<a class="pcard" href="#day-trips" data-open-dt>.*?</a>', "", s, flags=re.S)
        # css
        i = s.find("</style>"); s = s[:i] + CSS + s[i:]
        # third programme card
        m = re.search(r'<div class="pcards">.*?</a></div>', s, re.S)
        s = s[:m.end() - 6] + pcard(l) + s[m.end() - 6:]
        # section after the itinerary block
        a = s.find('id="tour-9-days"'); e1 = s.find("</section>", a); e2 = s.find("</section>", e1 + 10) + 10
        s = s[:e2] + "\n" + section(l) + s[e2:]
        # script
        i = s.rfind("</body>"); s = s[:i] + script(l) + s[i:]
        f.write_text(s)
        print(l, s.count('class="dt"'), s.count("data-open-dt"))

if __name__ == "__main__":
    run()
