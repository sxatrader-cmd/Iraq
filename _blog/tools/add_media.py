#!/usr/bin/env python3
"""Two YouTube Shorts (one between programme 1 and 2, one under programme 2, no text) and a
photo slideshow of Saif's own photos (20 photos, 5 s per slide) on every language homepage.
Idempotent."""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
V1, V2 = "1mDJ139QhMM", "87ApC9_ynRM"
PHOTOS = ["shabandar-cafe-tea", "kadhimiya-shrine-night", "qishla-clock-tower-view", "basra-shatt-al-arab-sunset",
          "abbasid-palace-arches", "uruk-warka", "mosul-al-hadba-nuri", "baghdadi-museum-scene", "hatra",
          "tigris-boat-clock-tower", "samarra-malwiya-b2b", "qishla-arcade", "nimrud", "abbasid-palace-courtyard",
          "adam-tree-qurna", "mutanabbi-statue", "wadi-al-salam", "qishla-balcony", "bahlul-shrine-dome",
          "baghdadi-museum-costumes"]
H = {"en": "From our journeys in Iraq", "ar": "من رحلاتنا في العراق", "ru": "Из наших поездок по Ираку",
     "de": "Von unseren Reisen im Irak", "fr": "Nos voyages en Irak", "es": "De nuestros viajes por Irak",
     "it": "Dai nostri viaggi in Iraq", "el": "Από τα ταξίδια μας στο Ιράκ", "cs": "Z našich cest po Iráku",
     "pl": "Z naszych podróży po Iraku", "zh": "我们的伊拉克旅程", "ja": "イラクの旅の風景", "tr": "Irak gezilerimizden",
     "fa": "از سفرهای ما در عراق", "ms": "Dari perjalanan kami di Iraq", "id": "Dari perjalanan kami di Irak",
     "th": "ภาพจากทริปของเราในอิรัก", "hi": "इराक़ में हमारी यात्राओं से", "ur": "عراق میں ہمارے سفروں سے",
     "ta": "இராக்கில் எங்கள் பயணங்களிலிருந்து", "fi": "Matkoiltamme Irakissa", "sv": "Från våra resor i Irak",
     "da": "Fra vores rejser i Irak", "no": "Fra reisene våre i Irak"}
EYE = {"ar": "معرض الصور", "fa": "گالری", "ur": "گیلری", "ru": "Галерея", "zh": "相册", "ja": "ギャラリー", "el": "Γκαλερί",
       "th": "แกลเลอรี", "hi": "गैलरी", "ta": "படங்கள்", "de": "Galerie", "fr": "Galerie", "es": "Galería", "it": "Galleria",
       "cs": "Galerie", "pl": "Galeria", "tr": "Galeri", "ms": "Galeri", "id": "Galeri", "fi": "Galleria", "sv": "Galleri",
       "da": "Galleri", "no": "Galleri", "en": "Gallery"}

CSS = """<style id="gal-css">
.xvid{margin:28px auto!important}
.gal{position:relative;border-radius:6px;overflow:hidden;background:var(--navy);aspect-ratio:4/3;box-shadow:0 0 0 3px var(--paper),0 0 0 4px var(--gold)}
@media(min-width:820px){.gal{aspect-ratio:16/9}}
.gal-s{position:absolute;inset:0;opacity:0;transition:opacity .9s ease}
.gal-s.on{opacity:1}
.gal-s img{width:100%;height:100%;object-fit:cover;display:block}
.gal-nav{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:rgba(14,22,40,.45);color:#fff;font-size:24px;line-height:1;cursor:pointer;display:grid;place-items:center;z-index:2}
.gal-prev{left:10px}.gal-next{right:10px}
.gal-dots{position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;gap:6px;z-index:2;flex-wrap:wrap;padding:0 40px}
.gal-dots button{width:7px;height:7px;padding:0;border:0;border-radius:50%;background:rgba(255,255,255,.55);cursor:pointer}
.gal-dots button.on{background:var(--gold);transform:scale(1.3)}
</style>"""

JS = """<script id="gal-js">(function(){
var g=document.querySelector(".gal");if(!g)return;var s=[].slice.call(g.querySelectorAll(".gal-s")),i=0,N=s.length;
function load(k){var im=s[k].querySelector("img");if(im&&im.dataset.src){im.src=im.dataset.src;im.removeAttribute("data-src");}}
function go(k){s[i].classList.remove("on");i=(k+N)%N;load(i);load((i+1)%N);s[i].classList.add("on");}
go(0);if(N>1)setInterval(function(){if(!document.hidden)go(i+1);},3000);
})();</script>"""


# Slovak, Croatian, Romanian (added Oct 2026)
H["sk"] = "Z našich ciest po Iraku"
H["hr"] = "S naših putovanja po Iraku"
H["ro"] = "Din călătoriile noastre în Irak"
EYE["sk"] = "Galéria"
EYE["hr"] = "Galerija"
EYE["ro"] = "Galerie"

# Dutch (added Oct 2026)
H["nl"] = "Van onze reizen in Irak"
EYE["nl"] = "Galerij"

# Georgian (added Oct 2026)
H["ka"] = "ჩვენი მოგზაურობებიდან ერაყში"
EYE["ka"] = "გალერეა"

# Korean (added Oct 2026)
H["ko"] = "우리의 이라크 여행에서"
EYE["ko"] = "갤러리"

# Portuguese (added Oct 2026)
H["pt"] = "Das nossas viagens pelo Iraque"
EYE["pt"] = "Galeria"

def vid(v):
    return (f'<div class="vid vert xvid"><iframe src="https://www.youtube-nocookie.com/embed/{v}?rel=0&amp;modestbranding=1&amp;playsinline=1" '
            'title="Fable Tour" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>\n')


def gallery(l):
    sl = "".join(f'<div class="gal-s{" on" if k == 0 else ""}"><img {"src" if k < 2 else "data-src"}="/img/{p}.webp" alt="{H[l]} – {k + 1}" decoding="async"{"" if k < 2 else ""}></div>'
                 for k, p in enumerate(PHOTOS))
    return (f'<section class="block in gal-wrap" style="padding-top:0" id="gallery"><div class="sec-head"><span class="eyebrow">{EYE[l]}</span><h2 class="disp">{H[l]}</h2></div>'
            f'<div class="gal" dir="ltr">{sl}'
            f'</div></section>\n')


def end_of(s, start):
    d = 0
    for m in re.finditer(r"<section\b|</section>", s[start:]):
        d += -1 if m.group(0) == "</section>" else 1
        if d == 0:
            return start + m.end()


def run():
    for l in H:
        f = ROOT / ("index.html" if l == "ar" else f"{l}/index.html")
        s = f.read_text()
        s = re.sub(r'<div class="vid vert xvid"[^>]*><iframe[^>]*></iframe></div>\n?', "", s)
        s = re.sub(r'\n?<div class="gal-wrap" id="gallery".*?<div class="gal-dots"></div></div></div>\n?', "", s, flags=re.S)
        s = re.sub(r'<section class="block in gal-wrap".*?<div class="gal-dots"></div></div></section>\n?', "", s, flags=re.S)
        s = re.sub(r'<style id="gal-css">.*?</style>\n?', "", s, flags=re.S)
        s = re.sub(r'<script id="gal-js">.*?</script>\n?', "", s, flags=re.S)
        a = s.index('<section class="prog" id="tour-9-days"')
        s = s[:a] + vid(V1) + s[a:]
        a = s.index('<section class="prog" id="tour-9-days"')
        e = end_of(s, a)
        s = s[:e] + "\n" + vid(V2) + s[e:]
        a = s.index('<section class="block in" style="padding-top:0" id="faq">')
        s = s[:a] + gallery(l) + "  " + s[a:]
        s = s.replace("</head>", CSS + "\n</head>", 1)
        s = s.replace("</body>", JS + "\n</body>", 1)
        f.write_text(s)
    print("media: done", len(H))


if __name__ == "__main__":
    run()
