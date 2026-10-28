#!/usr/bin/env python3
"""Trustindex floating review card: hide it 60 seconds after it first appears on screen.
Only the floating (position:fixed) card is hidden; reviews shown inside the page stay.
Added to every page that loads the Trustindex widget. Idempotent."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SECONDS = 60
JS = """<script id="ti-autohide">
/* hide the floating Trustindex review card SECONDS s after it first shows */
(function(){
  var first=0, start=Date.now();
  function fixedTi(){
    var out=[], els=document.querySelectorAll('[class*="ti-widget"],[class*="ti-popup"],[class*="ti-floating"],[id*="trustindex"]');
    for(var i=0;i<els.length;i++){
      var el=els[i], p=el, fixed=false;
      while(p && p!==document.body){ if(getComputedStyle(p).position==="fixed"){fixed=true;break;} p=p.parentElement; }
      if(fixed) out.push(p);
    }
    return out;
  }
  var t=setInterval(function(){
    var f=fixedTi(), shown=false;
    for(var i=0;i<f.length;i++){ if(f[i].offsetWidth||f[i].offsetHeight){shown=true;} }
    if(shown && !first) first=Date.now();
    if(first && Date.now()-first>=SECONDS*1000){
      for(var j=0;j<f.length;j++){ f[j].style.setProperty("display","none","important"); }
    }
    if(Date.now()-start>15*60*1000) clearInterval(t);
  },1000);
})();
</script>""".replace("SECONDS", str(SECONDS))

n = 0
for f in ROOT.rglob("*.html"):
    if "_blog" in f.parts or ".git" in f.parts:
        continue
    s = f.read_text()
    if "cdn.trustindex.io" not in s:
        continue
    s2 = re.sub(r'\s*<script id="ti-autohide">.*?</script>', "", s, flags=re.S)
    s2 = s2.replace("</body>", JS + "\n</body>", 1)
    if s2 != s:
        f.write_text(s2); n += 1
print("updated", n, "pages")
