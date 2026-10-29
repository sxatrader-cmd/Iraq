#!/usr/bin/env python3
"""Local SEO for the Slovak, Croatian and Romanian homepages (Oct 2026):
- titles, meta/OG/Twitter descriptions, keywords and H1 built around the main search phrase
  people in that country use ("zájazd do Iraku", "putovanje u Irak", "circuit Irak");
- a section written for travellers from that country (getting there, time difference,
  money, best season), placed before the FAQ;
- three country-specific FAQ items, both visible and in the FAQPage JSON-LD.
Idempotent: re-run after add_lang_cs.py (which rebuilds the pages from Czech)."""
import re, json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

L = {
"sk": {
 "title": "Zájazd do Iraku 7 a 9 dní – Babylon, Ur, mokrade | Fable Tour",
 "desc": "Zájazd do Iraku s miestnym sprievodcom: Babylon, Ur, Karbala, Nadžaf, mokrade a Hatra. 7 dní z Bagdadu alebo 9 dní z Basry do Erbilu, platba v eurách.",
 "kw": "zájazd do Iraku, zájazd Irak, poznávací zájazd Irak, cesta do Iraku, dovolenka Irak, Irak cestovná kancelária, Babylon zájazd, Mezopotámia zájazd, Irak so sprievodcom, Bagdad, Ur, Fable Tour",
 "h1": "Zájazd do Iraku: poznávacia cesta Mezopotámiou",
 "eye": "Zo Slovenska do Iraku",
 "h2": "Zájazd do Iraku zo Slovenska: praktické informácie",
 "body": [
  ("Ako sa dostať do Iraku zo Slovenska", "Priame lety zo Slovenska do Iraku nie sú. Najpohodlnejšie je letieť z viedenského letiska Schwechat, ktoré je len kúsok od Bratislavy, alebo z Košíc či Budapešti s jedným prestupom – najčastejšie v Istanbule, Dubaji, Dauhe alebo Ammáne. 7-dňový zájazd začína aj končí na medzinárodnom letisku v Bagdade, 9-dňový začína v Basre a končí v Erbile. Na letisku vás privítame a o všetky presuny sa postaráme."),
  ("Časový posun, mena a platba", "Irak používa čas UTC+3 celý rok, takže v zime je o dve hodiny viac ako na Slovensku a v lete o hodinu viac. Miestnou menou je iracký dinár, no cenu zájazdu u nás môžete zaplatiť v eurách pri príchode – kurz sa na tejto stránke aktualizuje každý deň. Zálohu nepožadujeme."),
  ("Kedy ísť a čo si pribaliť", "Najlepšie obdobie na poznávací zájazd do Iraku je od októbra do apríla, keď sú dni slnečné a príjemne teplé. V lete teploty často prekračujú 45 °C. Pribaľte si pohodlnú obuv, pokrývku hlavy a oblečenie so zakrytými plecami a kolenami; ženám na návštevu svätýň požičiame abáju."),
  ("Prečo cestovať s miestnym sprievodcom", "Sprevádza vás Saif, sprievodca z Bagdadu, ktorý pozná každú lokalitu – od Ištarinej brány v Babylone po zikkurat v Ure. Zájazdy sú súkromné pre vašu skupinu alebo sa môžete pripojiť k malej skupine, s hotelmi 4★–5★ a súkromnou klimatizovanou dopravou."),
 ],
 "links": '<p>Prečítajte si aj: <a href="/sk/blog/navsteva-babylonu-irak-sprievodca/">Babylon v Iraku – sprievodca návštevou</a> · <a href="/sk/blog/mauzoleum-imama-aliho-nadzaf/">Mauzóleum imáma Alího v Nadžafe</a> · <a href="/sk/day-trips/babylon/">Výlet do Babylonu z Bagdadu</a></p>',
 "faq": [
  ("Ako sa dostanem zo Slovenska do Iraku?", "Priame lety nie sú. Najčastejšie sa letí z Viedne, Bratislavy, Košíc alebo Budapešti s prestupom v Istanbule, Dubaji, Dauhe či Ammáne do Bagdadu, Basry alebo Erbilu. Na letisku vás privítame."),
  ("Aký je časový posun medzi Slovenskom a Irakom?", "Irak má čas UTC+3 celý rok: v zime je o dve hodiny viac ako na Slovensku, v lete o jednu hodinu viac."),
  ("Môžem zájazd zaplatiť v eurách?", "Áno. Cenu uvádzame v amerických dolároch a pri príchode ju môžete zaplatiť v eurách podľa denného kurzu. Zálohu nepožadujeme."),
 ],
},
"hr": {
 "title": "Putovanje u Irak 7 i 9 dana – Babilon, Ur, močvare | Fable Tour",
 "desc": "Putovanje u Irak s lokalnim vodičem: Babilon, Ur, Karbala, Nadžaf, močvare i Hatra. 7 dana iz Bagdada ili 9 dana od Basre do Erbila, plaćanje u eurima.",
 "kw": "putovanje u Irak, Irak putovanje, putovanja Irak, Irak turistička agencija, kulturno putovanje Irak, odmor u Iraku, Babilon putovanje, Mezopotamija putovanje, Irak s vodičem, Bagdad, Ur, Fable Tour",
 "h1": "Putovanje u Irak: kroz drevnu Mezopotamiju",
 "eye": "Iz Hrvatske u Irak",
 "h2": "Putovanje u Irak iz Hrvatske: praktične informacije",
 "body": [
  ("Kako doći iz Hrvatske u Irak", "Izravnih letova iz Hrvatske za Irak nema. Najjednostavnije je letjeti iz Zagreba, Splita ili Dubrovnika s jednim presjedanjem – najčešće u Istanbulu, Dubaiju, Dohi ili Ammanu. Putovanje od 7 dana počinje i završava u Međunarodnoj zračnoj luci Bagdad, a putovanje od 9 dana počinje u Basri i završava u Erbilu. Dočekujemo vas u zračnoj luci i brinemo se za sve transfere."),
  ("Vremenska razlika, valuta i plaćanje", "Irak cijele godine ima vrijeme UTC+3, pa je zimi dva sata, a ljeti jedan sat ispred Hrvatske. Lokalna valuta je irački dinar, no cijenu putovanja kod nas možete platiti u eurima po dolasku – tečaj se na ovoj stranici ažurira svaki dan. Ne tražimo predujam."),
  ("Kada putovati i što ponijeti", "Najbolje razdoblje za putovanje u Irak je od listopada do travnja, kad su dani sunčani i ugodno topli. Ljeti temperature često prelaze 45 °C. Ponesite udobnu obuću, pokrivalo za glavu i odjeću koja pokriva ramena i koljena; ženama za posjet svetištima posuđujemo abaju."),
  ("Zašto putovati s lokalnim vodičem", "Vodi vas Saif, vodič iz Bagdada koji poznaje svako nalazište – od Ištarinih vrata u Babilonu do zigurata u Uru. Putovanja su privatna za vašu grupu ili se možete pridružiti maloj grupi, uz hotele 4★–5★ i privatni klimatizirani prijevoz."),
 ],
 "links": '<p>Pročitajte i: <a href="/hr/blog/posjet-babilonu-irak-vodic/">Babilon u Iraku – vodič za posjet</a> · <a href="/hr/blog/svetiste-imama-alija-nadzaf/">Svetište imama Alija u Nadžafu</a> · <a href="/hr/day-trips/babylon/">Izlet u Babilon iz Bagdada</a></p>',
 "faq": [
  ("Kako doći iz Hrvatske u Irak?", "Izravnih letova nema. Najčešće se leti iz Zagreba, Splita ili Dubrovnika s presjedanjem u Istanbulu, Dubaiju, Dohi ili Ammanu do Bagdada, Basre ili Erbila. Dočekujemo vas u zračnoj luci."),
  ("Kolika je vremenska razlika između Hrvatske i Iraka?", "Irak cijele godine ima vrijeme UTC+3: zimi je dva sata, a ljeti jedan sat ispred Hrvatske."),
  ("Mogu li putovanje platiti u eurima?", "Da. Cijenu navodimo u američkim dolarima, a po dolasku je možete platiti u eurima po dnevnom tečaju. Ne tražimo predujam."),
 ],
},
"ro": {
 "title": "Circuit Irak 7 și 9 zile – Babilon, Ur, Mesopotamia | Fable Tour",
 "desc": "Circuit în Irak cu ghid local: Babilon, Ur, Karbala, Najaf, mlaștinile și Hatra. 7 zile din Bagdad sau 9 zile din Basra la Erbil, plata în euro la sosire.",
 "kw": "circuit Irak, excursie Irak, călătorie în Irak, vacanță în Irak, agenție turism Irak, circuit Mesopotamia, Babilon excursie, Irak cu ghid, Bagdad, Ur, Fable Tour",
 "h1": "Circuit în Irak: călătorie prin Mesopotamia",
 "eye": "Din România în Irak",
 "h2": "Circuit în Irak din România: informații practice",
 "body": [
  ("Cum ajungeți din România în Irak", "Nu există zboruri directe din România spre Irak. Cel mai simplu este să zburați din București, Cluj-Napoca, Iași sau Timișoara cu o singură escală – de obicei la Istanbul, Dubai, Doha sau Amman. Circuitul de 7 zile începe și se încheie la Aeroportul Internațional Bagdad, iar cel de 9 zile începe la Basra și se încheie la Erbil. Vă întâmpinăm la aeroport și ne ocupăm de toate transferurile."),
  ("Diferența de fus orar, moneda și plata", "Irakul are tot anul ora UTC+3, deci iarna este cu o oră înaintea României, iar vara aveți aceeași oră. Moneda locală este dinarul irakian, dar prețul circuitului îl puteți plăti la noi în euro, la sosire – cursul se actualizează zilnic pe această pagină. Nu cerem avans."),
  ("Când să mergeți și ce să luați cu dumneavoastră", "Cea mai bună perioadă pentru un circuit în Irak este din octombrie până în aprilie, când zilele sunt însorite și plăcut de calde. Vara temperaturile depășesc adesea 45 °C. Luați încălțăminte comodă, o pălărie și haine care acoperă umerii și genunchii; pentru vizita la sanctuare, doamnelor le împrumutăm o abaya."),
  ("De ce să călătoriți cu un ghid local", "Vă însoțește Saif, ghid din Bagdad care cunoaște fiecare sit – de la Poarta Ishtar din Babilon până la ziguratul din Ur. Circuitele sunt private pentru grupul dumneavoastră sau vă puteți alătura unui grup mic, cu hoteluri de 4★–5★ și transport privat cu aer condiționat."),
 ],
 "links": '<p>Citiți și: <a href="/ro/blog/vizita-babilon-irak-ghid/">Babilon, Irak – ghid pentru vizită</a> · <a href="/ro/blog/sanctuarul-imamului-ali-najaf/">Sanctuarul Imamului Ali din Najaf</a> · <a href="/ro/day-trips/babylon/">Excursie la Babilon din Bagdad</a></p>',
 "faq": [
  ("Cum ajung din România în Irak?", "Nu există zboruri directe. De obicei se zboară din București, Cluj-Napoca, Iași sau Timișoara cu escală la Istanbul, Dubai, Doha sau Amman spre Bagdad, Basra sau Erbil. Vă întâmpinăm la aeroport."),
  ("Care este diferența de fus orar dintre România și Irak?", "Irakul are tot anul ora UTC+3: iarna este cu o oră înaintea României, iar vara ora este aceeași."),
  ("Pot plăti circuitul în euro?", "Da. Prețul este afișat în dolari americani și îl puteți plăti în euro la sosire, la cursul zilei. Nu cerem avans."),
 ],
},
"nl": {
 "title": "Rondreis Irak 7 en 9 dagen – Babylon, Ur, moerassen | Fable Tour",
 "desc": "Rondreis door Irak met een lokale gids: Babylon, Ur, Karbala, Najaf, de moerassen en Hatra. 7 dagen vanuit Bagdad of 9 dagen van Basra naar Erbil, betalen in euro.",
 "kw": "rondreis Irak, reis naar Irak, Irak reis, groepsreis Irak, privéreis Irak, vakantie Irak, reisbureau Irak, Babylon bezoeken, Mesopotamië rondreis, Irak met gids, Bagdad, Ur, Fable Tour",
 "h1": "Rondreis Irak: een reis door het oude Mesopotamië",
 "eye": "Vanuit Nederland en België naar Irak",
 "h2": "Rondreis Irak vanuit Nederland en België: praktische informatie",
 "body": [
  ("Hoe reist u naar Irak", "Er zijn geen rechtstreekse vluchten vanuit Nederland of België naar Irak. Het eenvoudigst vliegt u vanaf Amsterdam Schiphol, Eindhoven of Brussel met één overstap – meestal in Istanbul, Dubai, Doha of Amman. De 7-daagse rondreis begint en eindigt op de internationale luchthaven van Bagdad, de 9-daagse begint in Basra en eindigt in Erbil. We ontvangen u op de luchthaven en zorgen voor alle transfers."),
  ("Tijdsverschil, munteenheid en betalen", "Irak hanteert het hele jaar UTC+3: in de winter is het er twee uur later dan in Nederland en België, in de zomer één uur. De lokale munt is de Iraakse dinar, maar de reissom kunt u bij aankomst in euro betalen – de koers wordt op deze pagina dagelijks bijgewerkt. We vragen geen aanbetaling."),
  ("Wanneer gaan en wat neemt u mee", "De beste periode voor een rondreis door Irak is van oktober tot april, als de dagen zonnig en aangenaam warm zijn. In de zomer loopt de temperatuur vaak op tot boven de 45 °C. Neem comfortabele schoenen, iets voor op het hoofd en kleding die schouders en knieën bedekt mee; voor het bezoek aan heiligdommen lenen we vrouwen een abaya."),
  ("Waarom reizen met een lokale gids", "U wordt begeleid door Saif, een gids uit Bagdad die elke plek kent – van de Isjtarpoort in Babylon tot de ziggoerat van Ur. De reizen zijn privé voor uw groep, of u sluit aan bij een kleine groep, met 4★–5★-hotels en privévervoer met airco."),
 ],
 "links": '<p>Lees ook: <a href="/nl/blog/babylon-irak-bezoeken-reisgids/">Babylon in Irak – reisgids</a> · <a href="/nl/blog/heiligdom-imam-ali-najaf/">Het heiligdom van imam Ali in Najaf</a> · <a href="/nl/day-trips/babylon/">Dagtocht naar Babylon vanuit Bagdad</a></p>',
 "faq": [
  ("Hoe reis ik vanuit Nederland of België naar Irak?", "Er zijn geen rechtstreekse vluchten. Meestal vliegt u vanaf Amsterdam, Eindhoven of Brussel met een overstap in Istanbul, Dubai, Doha of Amman naar Bagdad, Basra of Erbil. We ontvangen u op de luchthaven."),
  ("Wat is het tijdsverschil tussen Nederland en Irak?", "Irak heeft het hele jaar UTC+3: in de winter is het er twee uur later dan in Nederland en België, in de zomer één uur."),
  ("Kan ik de reis in euro betalen?", "Ja. We vermelden de prijs in Amerikaanse dollars en u kunt bij aankomst in euro betalen tegen de dagkoers. We vragen geen aanbetaling."),
 ],
},
}

esc = lambda s: html.escape(s, quote=True)


def apply(l, d):
    f = ROOT / l / "index.html"
    s = f.read_text()
    old_t = re.search(r"<title>(.*?)</title>", s).group(1)
    old_d = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    old_h1 = re.search(r'<h1 class="disp" data-i="h1">(.*?)</h1>', s).group(1)
    s = s.replace(f"<title>{old_t}</title>", f"<title>{esc(d['title'])}</title>")
    for prop in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*"', lambda m: m.group(1) + esc(d["title"]) + '"', s)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*"', lambda m: m.group(1) + esc(d["desc"]) + '"', s)
    s = re.sub(r'(<meta name="keywords" content=")[^"]*"', lambda m: m.group(1) + esc(d["kw"]) + '"', s)
    # H1 in the markup and in the page's text table
    s = s.replace(f'data-i="h1">{old_h1}</h1>', f'data-i="h1">{esc(d["h1"])}</h1>')
    s = s.replace(f'"h1": {json.dumps(html.unescape(old_h1), ensure_ascii=False)}', f'"h1": {json.dumps(d["h1"], ensure_ascii=False)}')
    # JSON-LD: WebPage name/description, new FAQ items
    s = s.replace(json.dumps(html.unescape(old_t), ensure_ascii=False), json.dumps(d["title"], ensure_ascii=False))
    s = s.replace(json.dumps(html.unescape(old_d), ensure_ascii=False), json.dumps(d["desc"], ensure_ascii=False))

    def ld(m):
        try:
            data = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        nodes = data.get("@graph", [data])
        for n in nodes:
            if n.get("@type") == "FAQPage":
                have = {q["name"] for q in n["mainEntity"]}
                for q, a in d["faq"]:
                    if q not in have:
                        n["mainEntity"].append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)

    # visible FAQ items (append at the end of the list)
    if d["faq"][0][0] not in s.split('id="faq"', 1)[1].split("</section>", 1)[0]:
        items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in d["faq"])
        i = s.index('id="faq"')
        j = s.index("</div>", s.index('<div class="faq">', i))
        s = s[:j] + items + s[j:]

    # local section before the FAQ
    s = re.sub(r'\s*<section class="block in" style="padding-top:0" id="local-travel">.*?</section>', "", s, flags=re.S)
    body = "".join(f"<h3>{esc(h)}</h3><p>{esc(p)}</p>" for h, p in d["body"])
    sec = (f'\n  <section class="block in" style="padding-top:0" id="local-travel">\n'
           f'    <div class="sec-head"><span class="eyebrow">{esc(d["eye"])}</span><h2 class="disp">{esc(d["h2"])}</h2></div>\n'
           f'    <div class="local-travel">{body}{d["links"]}</div>\n  </section>')
    k = s.index('<section class="block in" style="padding-top:0" id="faq">')
    s = s[:k].rstrip() + sec + "\n  " + s[k:]
    if 'id="local-css"' not in s:
        s = s.replace("</head>", '<style id="local-css">.local-travel{max-width:760px}.local-travel h3{margin:22px 0 6px;font-size:1.08rem}.local-travel p{margin:0 0 10px;line-height:1.7}.local-travel a{color:var(--gold,#c9a14a)}</style>\n</head>', 1)
    f.write_text(s)
    print("ok", l)


if __name__ == "__main__":
    for l, d in L.items():
        apply(l, d)
