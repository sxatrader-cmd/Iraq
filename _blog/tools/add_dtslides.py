#!/usr/bin/env python3
"""Day-trip cards with more than one photo play as a slideshow (crossfade, 5 s per photo,
only while the card is on screen). Tapping still opens the full-size viewer, starting at
the photo on screen. Applied to every page that has the day-trips section. Idempotent."""
import re, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CSS = """<style id="dts-css">
.dt-ph .dts{position:absolute;inset:0;background:center/cover no-repeat;opacity:0;transition:opacity 1s ease}
.dt-ph .dts.on{opacity:1}
.dt-ph>.dt-zoom,.dt-ph>.dt-cnt{z-index:2}
</style>"""
JS = """<script id="dts-js">(function(){
var cards=[].slice.call(document.querySelectorAll(".dt-ph[data-full]")).filter(function(p){return p.dataset.full.indexOf("|")>-1;});
if(!cards.length)return;
cards.forEach(function(ph){
 var list=ph.dataset.full.split("|"),n=list.length,i=0,cnt=ph.querySelector(".dt-cnt"),t=null,vis=false;
 ph.dataset.all=ph.dataset.full;
 var L=[0,1].map(function(){var d=document.createElement("div");d.className="dts";ph.insertBefore(d,ph.firstChild);return d;}),cur=0;
 function pre(k){var im=new Image();im.src=list[k];}
 function show(k){i=(k+n)%n;var nx=L[1-cur];nx.style.backgroundImage="url('"+list[i]+"')";nx.classList.add("on");L[cur].classList.remove("on");cur=1-cur;
  if(cnt)cnt.textContent=(i+1)+" / "+n;ph.dataset.full=list.slice(i).concat(list.slice(0,i)).join("|");pre((i+1)%n);}
 function start(){if(t)return;t=setInterval(function(){if(vis&&!document.hidden)show(i+1);},5000);}
 L[cur].style.backgroundImage="url('"+list[0]+"')";L[cur].classList.add("on");pre(1);
 if("IntersectionObserver" in window){new IntersectionObserver(function(es){vis=es[0].isIntersecting;},{threshold:.3}).observe(ph);}else vis=true;
 var x=null;ph.addEventListener("touchstart",function(e){x=e.touches[0].clientX;},{passive:true});
 ph.addEventListener("touchend",function(e){if(x===null)return;var dx=e.changedTouches[0].clientX-x;if(Math.abs(dx)>40){e.preventDefault();show(i+(dx<0?1:-1));clearInterval(t);t=null;start();}x=null;});
 start();
});
})();</script>"""


def run():
    files = [ROOT / "index.html"] + [pathlib.Path(p) for p in glob.glob(str(ROOT / "*/index.html")) + glob.glob(str(ROOT / "day-trips/*/index.html")) + glob.glob(str(ROOT / "*/day-trips/*/index.html"))]
    n = 0
    for f in files:
        s = f.read_text()
        if 'id="day-trips"' not in s:
            continue
        s = re.sub(r'<style id="dts-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="dts-js">.*?</script>\n?', "", s, flags=re.S)
        s = s.replace("</head>", CSS + "\n</head>", 1)
        s = s.replace("</body>", JS + "\n</body>", 1)
        f.write_text(s)
        n += 1
    print("slides:", n)


if __name__ == "__main__":
    run()
