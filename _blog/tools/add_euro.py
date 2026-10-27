#!/usr/bin/env python3
"""Euro prices on the pages in the languages of European Union countries (+ Norwegian).
Every $ price stays the base price and gets the euro amount next to it, converted in
the browser with the day's USD→EUR rate (ECB reference rate via frankfurter.dev,
cached for the day; open.er-api.com as backup; FALLBACK below if both fail).
A line under each price says the guest can pay in euros on arrival.
English, Arabic and all other languages keep dollars only.
Idempotent: re-run after rebuilding pages."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
FALLBACK = 0.86  # USD→EUR, used only if both rate services are unreachable

NOTE = {
    "de": "Zahlung in Euro bei Ankunft möglich · Kurs täglich aktualisiert",
    "fr": "Paiement possible en euros à l'arrivée · taux mis à jour chaque jour",
    "es": "Puedes pagar en euros a tu llegada · tipo de cambio actualizado a diario",
    "it": "Puoi pagare in euro all'arrivo · cambio aggiornato ogni giorno",
    "el": "Πληρωμή σε ευρώ κατά την άφιξη · ισοτιμία με καθημερινή ενημέρωση",
    "cs": "Platba v eurech při příjezdu · kurz aktualizovaný denně",
    "pl": "Płatność w euro na miejscu po przyjeździe · kurs aktualizowany codziennie",
    "fi": "Voit maksaa euroina saapuessasi · kurssi päivitetään päivittäin",
    "sv": "Du kan betala i euro vid ankomst · kursen uppdateras dagligen",
    "da": "Du kan betale i euro ved ankomst · kursen opdateres dagligt",
    "no": "Du kan betale i euro ved ankomst · kursen oppdateres daglig",
}

CSS = """<style id="eur-css">
.eur{display:inline-block;margin-inline-start:.4em;font-size:.78em;font-weight:inherit;opacity:.8;white-space:nowrap;letter-spacing:0}
.amount .eur{display:block;margin:6px 0 0;font-size:.5em;opacity:1;color:var(--gold,#c9a14a)}
.dt-total b .usd-p{display:inline;font-size:inherit;color:inherit}
.dt-total b .eur{display:block;margin:2px 0 0;font-size:14px;color:var(--muted)}
.eur-pay{display:block;margin-top:9px;font-size:12.5px;line-height:1.5;color:inherit;opacity:.8}
.eur-pay::before{content:"€";display:inline-grid;place-items:center;width:17px;height:17px;margin-inline-end:6px;border-radius:50%;background:var(--gold,#c9a14a);color:#fff;font-size:10.5px;font-weight:700;vertical-align:-3px}
.eur-pay .eur-rate{white-space:nowrap}
</style>"""

JS = """<script id="eur-js">(function(){
var L=document.documentElement.lang||"de",FB=%s,KEY="fable_usd_eur",today=new Date().toISOString().slice(0,10),R=null,busy=false;
var F=new Intl.NumberFormat(L==="no"?"nb":L,{style:"currency",currency:"EUR",maximumFractionDigits:0});
var F4=new Intl.NumberFormat(L==="no"?"nb":L,{minimumFractionDigits:2,maximumFractionDigits:4});
var RX=/(?:US)?\\$\\s?(\\d{1,3}(?:,\\d{3})+|\\d+)(?![\\d,])/g;
function eur(usd){return F.format(Math.round(usd*R));}
function num(s){return parseInt(String(s).replace(/,/g,""),10);}
function skip(n){for(var p=n.parentNode;p&&p!==document.body;p=p.parentNode){var t=p.nodeName;if(t==="SCRIPT"||t==="STYLE"||t==="TEXTAREA"||t==="OPTION"||t==="TITLE"||(p.classList&&(p.classList.contains("eur")||p.classList.contains("usd-p"))))return true;}return false;}
function texts(root){var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),a=[],n;while(n=w.nextNode()){RX.lastIndex=0;if(RX.test(n.nodeValue)&&!skip(n))a.push(n);}return a;}
function wrap(n){var s=n.nodeValue,f=document.createDocumentFragment(),last=0,m;RX.lastIndex=0;
 while(m=RX.exec(s)){if(m.index>last)f.appendChild(document.createTextNode(s.slice(last,m.index)));
  var u=document.createElement("span");u.className="usd-p";u.textContent=m[0];f.appendChild(u);
  var e=document.createElement("span");e.className="eur";e.setAttribute("dir","ltr");e.dataset.usd=num(m[1]);e.textContent="≈ "+eur(num(m[1]));
  var host=n.parentNode&&n.parentNode.closest?n.parentNode.closest(".amount"):null;
  if(host){f.appendChild(document.createTextNode(""));host.appendChild(e);}else f.appendChild(e);
  last=m.index+m[0].length;}
 if(last<s.length)f.appendChild(document.createTextNode(s.slice(last)));n.parentNode.replaceChild(f,n);}
function opts(){document.querySelectorAll("option").forEach(function(o){if(o.dataset.eur)return;RX.lastIndex=0;var m=RX.exec(o.textContent);if(m){o.dataset.eur=1;o.textContent+=" (≈ "+eur(num(m[1]))+")";}});}
function wa(){document.querySelectorAll('a[href*="wa.me"][href*="text="]').forEach(function(a){var h=a.getAttribute("href"),i=h.indexOf("text=");if(i<0)return;var t;try{t=decodeURIComponent(h.slice(i+5));}catch(e){return;}
 if(t.indexOf("€")>-1)return;RX.lastIndex=0;var m=RX.exec(t);if(!m)return;var nt=t.replace(m[0],m[0]+" (≈ "+eur(num(m[1]))+")");a.setAttribute("href",h.slice(0,i+5)+encodeURIComponent(nt));});}
function rate(){var v="· 1 USD = "+F4.format(R)+" €";document.querySelectorAll(".eur-rate").forEach(function(s){if(s.textContent!==v)s.textContent=v;});}
function run(){if(R===null||busy)return;busy=true;try{texts(document.body).forEach(wrap);opts();wa();rate();}finally{busy=false;}}
function go(r){R=r;run();var q=0;new MutationObserver(function(){if(busy||q)return;q=requestAnimationFrame(function(){q=0;run();});}).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["href"]});}
function save(r){try{localStorage.setItem(KEY,JSON.stringify({d:today,r:r}));}catch(e){}}
var c=null;try{c=JSON.parse(localStorage.getItem(KEY)||"null");}catch(e){}
if(c&&c.d===today&&c.r>0){go(c.r);return;}
function j(u){return fetch(u,{cache:"no-store"}).then(function(r){if(!r.ok)throw 0;return r.json();});}
j("https://api.frankfurter.dev/v1/latest?base=USD&symbols=EUR").then(function(d){return d.rates.EUR;})
 .catch(function(){return j("https://open.er-api.com/v6/latest/USD").then(function(d){return d.rates.EUR;});})
 .then(function(r){if(!(r>0))throw 0;save(r);go(r);})
 .catch(function(){go(c&&c.r>0?c.r:FB);});
})();</script>"""


def note(lang):
    return f'<div class="eur-pay" data-eur-note>{NOTE[lang]} <span class="eur-rate" dir="ltr"></span></div>'


def apply(f, lang):
    s = f.read_text()
    s = re.sub(r'<style id="eur-css">.*?</style>\n?', "", s, flags=re.S)
    s = re.sub(r'<script id="eur-js">.*?</script>\n?', "", s, flags=re.S)
    s = re.sub(r'<div class="eur-pay" data-eur-note>[^<]*<span class="eur-rate"[^>]*></span></div>', "", s)
    # note under each programme price and under the day-trips intro
    s = re.sub(r'(<div class="per">[^<]*</div>)', lambda m: m.group(1) + note(lang), s)
    s = re.sub(r'(<p class="dt-note">[^<]*</p>)', lambda m: m.group(1) + note(lang), s, count=1)
    s = s.replace("</head>", CSS + "\n</head>", 1)
    s = s.replace("</body>", JS % FALLBACK + "\n</body>", 1)
    f.write_text(s)


def run():
    for lang in NOTE:
        for f in sorted((ROOT / lang).glob("index.html")) + sorted((ROOT / lang / "day-trips").glob("*/index.html")):
            apply(f, lang)
        print("euro:", lang)


if __name__ == "__main__":
    run()
