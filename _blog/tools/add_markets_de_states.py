#!/usr/bin/env python3
"""German state pages (Oct 2026): /de/iraq-tours-from-<land>/ for all 16 Bundesländer, in German
only, cloned from /de/iraq-tours-from-germany/ (run add_markets_eu.py first) with their own
panel (Anreise, Visum, Familienbesuch, Preise, Highlights, Links zu allen Ländern), meta, H1 and
JSON-LD. The Germany pages get a "nach Bundesland" links card. Idempotent."""
import re, json, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from add_markets import BASE, TODAY
import add_markets_na as NA

ROOT = pathlib.Path(__file__).resolve().parents[2]
esc = lambda s: html.escape(s, quote=True)
HUB = "Istanbul (Turkish Airlines), Doha (Qatar Airways), Dubai (Emirates) oder Amman (Royal Jordanian)"

# slug-part: (Name, "aus …", Städte, Einleitung, [(Flughafen, Text)], Highlights, Tipp)
L = {
 "baden-wuerttemberg": ("Baden-Württemberg", "aus Baden-Württemberg", "Stuttgart, Mannheim, Karlsruhe und Freiburg",
   "Aus Stuttgart, Mannheim, Karlsruhe, Freiburg oder Ulm: Wir zeigen Ihnen das Zweistromland mit privatem Reiseleiter — Babylon, Ur, die Marschen und Hatra, im eigenen Tempo und zum Wunschtermin.",
   [("Stuttgart (STR) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB}."), ("Karlsruhe/Baden-Baden (FKB), Basel-Mulhouse (BSL/EAP) für Freiburg", "Mit Umstieg in Istanbul oder über Frankfurt.")],
   ["babylon", "ur", "hatra"], "Gut zu wissen: Frankfurt ist von Stuttgart und Mannheim schnell mit dem ICE erreichbar — dort haben Sie die größte Flugauswahl."),
 "bayern": ("Bayern", "aus Bayern", "München, Nürnberg, Augsburg und Regensburg",
   "Aus München, Nürnberg, Augsburg, Regensburg oder Würzburg in das Land von Babylon und Ur: private Rundreisen mit Reiseleiter, 4★–5★-Hotels und Empfang am Flughafen.",
   [("München (MUC) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB}; zeitweise auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen)."), ("Nürnberg (NUE), Memmingen (FMM)", "Mit Umstieg in Istanbul oder über München.")],
   ["babylon", "samarra", "marshes"], "Beste Reisezeit ist Oktober bis April — dann ist es im Irak angenehm warm, wenn in Bayern der Winter beginnt."),
 "berlin": ("Berlin", "aus Berlin", "Berlin",
   "Berlin und Babylon sind eng verbunden: Robert Koldewey grub ab 1899 für die Deutsche Orient-Gesellschaft Babylon aus, und das Ischtar-Tor steht heute im Pergamonmuseum. Bei uns erleben Sie Babylon an seinem Originalort — mit privatem Reiseleiter, der Ihnen die Prozessionsstraße und den Löwen von Babylon zeigt.",
   [("Berlin Brandenburg (BER) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB}; zeitweise auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen).")],
   ["babylon", "ur", "mosul"], "Tipp für Museumsfans: Nach dem Besuch im Pergamonmuseum sehen Sie in Babylon die Ziegel des Originaltores, auf denen Nebukadnezars Name noch in Keilschrift steht."),
 "brandenburg": ("Brandenburg", "aus Brandenburg", "Potsdam, Cottbus, Brandenburg an der Havel und Frankfurt (Oder)",
   "Aus Potsdam, Cottbus oder Frankfurt (Oder) — der Flughafen BER liegt vor der Tür. Wir organisieren Ihre private Irak-Reise zum Wunschtermin: Babylon, Ur, die Marschen, Samarra und Hatra.",
   [("Berlin Brandenburg (BER) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB} (aktuelle Flugpläne prüfen).")],
   ["babylon", "marshes", "samarra"], "Wenig Urlaubstage? Die 7-Tage-Tour beginnt und endet am Flughafen Bagdad — passt zwischen zwei Wochenenden."),
 "bremen": ("Bremen", "aus Bremen", "Bremen und Bremerhaven",
   "Aus Bremen und Bremerhaven ins alte Mesopotamien: Babylon, die Zikkurat von Ur und die Marschen, mit privatem Reiseleiter und Privatwagen von der Ankunft bis zum Abflug.",
   [("Bremen (BRE) → Bagdad (BGW) / Erbil (EBL)", "Mit Umstieg in Istanbul oder über Frankfurt bzw. München."), ("Hamburg (HAM)", f"Größere Auswahl mit einem Umstieg über {HUB}.")],
   ["babylon", "ur", "marshes"], "Reisen Sie mit Familie oder Freunden? Als private Gruppe bestimmen Sie Termin und Tempo selbst."),
 "hamburg": ("Hamburg", "aus Hamburg", "Hamburg",
   "Von der Elbe an Euphrat und Tigris: Wir zeigen Ihnen Babylon, Ur, die Marschen und das abbasidische Bagdad — privat, zum Wunschtermin und mit Reiseleiter, der Deutsch-sprachige Gäste gewohnt ist.",
   [("Hamburg (HAM) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB} (aktuelle Flugpläne prüfen).")],
   ["babylon", "qishla", "ur"], "Hafenstadt trifft Hafenstadt: Auf der 9-Tage-Tour beginnen Sie in Basra am Schatt al-Arab."),
 "hessen": ("Hessen", "aus Hessen", "Frankfurt, Wiesbaden, Darmstadt und Kassel",
   "Frankfurt ist das wichtigste Drehkreuz für Irak-Reisen aus Deutschland. Aus Frankfurt, Wiesbaden, Darmstadt, Offenbach oder Kassel erreichen Sie Bagdad, Basra und Erbil mit einem Umstieg — wir holen Sie am Flughafen ab.",
   [("Frankfurt (FRA) → Bagdad (BGW) / Erbil (EBL) / Basra (BSR)", f"Mit einem Umstieg über {HUB}; zeitweise auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen)."), ("Kassel", "Mit dem ICE nach Frankfurt.")],
   ["babylon", "ur", "hatra"], "Für Geschichtsinteressierte: Auf Wunsch planen wir mehr Zeit in Babylon, Hatra und Nimrud ein."),
 "mecklenburg-vorpommern": ("Mecklenburg-Vorpommern", "aus Mecklenburg-Vorpommern", "Rostock, Schwerin, Greifswald und Stralsund",
   "Aus Rostock, Schwerin, Greifswald oder Stralsund in das Land, in dem die Schrift erfunden wurde: Uruk, Ur und Babylon, mit privatem Reiseleiter und Empfang am Flughafen.",
   [("Hamburg (HAM), Berlin (BER)", f"Mit einem Umstieg über {HUB} nach Bagdad oder Erbil."), ("Rostock-Laage (RLG)", "Begrenzte Verbindungen, meist über ein deutsches Drehkreuz.")],
   ["ur", "babylon", "marshes"], "Lange Anreise? Buchen Sie unseren Flughafentransfer in Bagdad und starten Sie ausgeruht."),
 "niedersachsen": ("Niedersachsen", "aus Niedersachsen", "Hannover, Braunschweig, Oldenburg, Osnabrück und Celle",
   "Niedersachsen hat große irakische, kurdische und jesidische Gemeinschaften — in Hannover, Celle, Oldenburg, Osnabrück und Braunschweig. Ob Familienbesuch oder Rundreise: Wir verbinden beides mit Babylon, Ur, Mossul und Erbil.",
   [("Hannover (HAJ) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB}; viele Familien fliegen nach Erbil (aktuelle Flugpläne prüfen)."), ("Bremen (BRE), Hamburg (HAM)", "Alternativen mit größerer Flugauswahl.")],
   ["mosul", "babylon", "hatra"], "Familie im Norden? Die 9-Tage-Tour endet in Erbil — Sie können danach in Kurdistan bleiben."),
 "nordrhein-westfalen": ("Nordrhein-Westfalen", "aus Nordrhein-Westfalen", "Köln, Düsseldorf, Dortmund, Essen, Bonn und Münster",
   "In NRW leben besonders viele Menschen mit irakischen und kurdischen Wurzeln — in Köln, Düsseldorf, Essen, Dortmund, Bielefeld und Bonn. Wir verbinden Ihren Familienbesuch mit einer echten Rundreise, oder zeigen deutschen Gästen das Zweistromland.",
   [("Düsseldorf (DUS), Köln/Bonn (CGN) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB}; zeitweise auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen)."), ("Dortmund (DTM), Münster/Osnabrück (FMO)", "Mit Umstieg in Istanbul oder über Frankfurt.")],
   ["babylon", "kadhimiya", "marshes"], "Mit Großeltern unterwegs? Wir planen ruhige Tage, nahe Hotelzimmer, und unser Reiseleiter spricht Arabisch."),
 "rheinland-pfalz": ("Rheinland-Pfalz", "aus Rheinland-Pfalz", "Mainz, Ludwigshafen, Koblenz, Trier und Kaiserslautern",
   "Aus Mainz, Ludwigshafen, Koblenz, Trier oder Kaiserslautern — Frankfurt liegt nah. Wir organisieren Ihre private Irak-Reise: Babylon, Ur, die Marschen, Samarra und Hatra.",
   [("Frankfurt (FRA)", f"Von Mainz in 30 Minuten; mit einem Umstieg über {HUB} nach Bagdad oder Erbil."), ("Frankfurt-Hahn (HHN), Luxemburg (LUX) für Trier", "Weitere Möglichkeiten je nach Flugplan.")],
   ["babylon", "samarra", "ur"], "Zu zweit oder als Familie? Auch als private Gruppe bleibt der Preis pro Person gleich."),
 "saarland": ("Saarland", "aus dem Saarland", "Saarbrücken, Neunkirchen und Saarlouis",
   "Aus Saarbrücken, Neunkirchen oder Saarlouis ins alte Mesopotamien — mit Empfang am Flughafen, Privatwagen und Reiseleiter von der Ankunft bis zum Abflug.",
   [("Frankfurt (FRA), Luxemburg (LUX)", f"Mit einem Umstieg über {HUB} nach Bagdad oder Erbil."), ("Saarbrücken (SCN)", "Begrenzte Verbindungen, meist über ein Drehkreuz.")],
   ["babylon", "ur", "marshes"], "Lieber kurz? Unsere Tagesausflüge ab Bagdad führen nach Babylon, Samarra oder an die Zikkurat von Aqar Quf."),
 "sachsen": ("Sachsen", "aus Sachsen", "Dresden, Leipzig und Chemnitz",
   "Aus Dresden, Leipzig oder Chemnitz zu den Ursprüngen der Zivilisation: Uruk, Ur und Babylon, dazu das abbasidische Bagdad — privat und zum Wunschtermin.",
   [("Leipzig/Halle (LEJ), Dresden (DRS)", "Mit Umstieg in Istanbul oder über Frankfurt bzw. München."), ("Berlin (BER), Prag (PRG)", f"Größere Auswahl mit einem Umstieg über {HUB}.")],
   ["ur", "babylon", "qishla"], "Für Kulturreisende: In Bagdad besuchen wir die Mustansiriya, eine der ältesten Universitäten der Welt (1234)."),
 "sachsen-anhalt": ("Sachsen-Anhalt", "aus Sachsen-Anhalt", "Halle, Magdeburg und Dessau",
   "Aus Halle, Magdeburg oder Dessau in das Land zwischen Euphrat und Tigris: Babylon, Ur, die Marschen, Samarra und Hatra, mit privatem Reiseleiter.",
   [("Leipzig/Halle (LEJ)", "Mit Umstieg in Istanbul oder über ein deutsches Drehkreuz."), ("Berlin (BER)", f"Mit einem Umstieg über {HUB}.")],
   ["babylon", "hatra", "marshes"], "Gut zu wissen: Der Irak liegt im Winter 2 Stunden vor Deutschland — kaum Jetlag."),
 "schleswig-holstein": ("Schleswig-Holstein", "aus Schleswig-Holstein", "Kiel, Lübeck, Flensburg und Neumünster",
   "Aus Kiel, Lübeck, Flensburg oder Neumünster — über Hamburg in das Land von Babylon und Ur. Private Rundreisen mit 4★–5★-Hotels und Reiseleiter.",
   [("Hamburg (HAM) → Bagdad (BGW) / Erbil (EBL)", f"Mit einem Umstieg über {HUB} (aktuelle Flugpläne prüfen).")],
   ["babylon", "basra", "marshes"], "Wasser gewohnt? Die Mashoof-Bootsfahrt durch die Marschen gehört zu den schönsten Momenten der Reise."),
 "thueringen": ("Thüringen", "aus Thüringen", "Erfurt, Jena, Weimar und Gera",
   "Thüringen hat eine besondere Verbindung zu Mesopotamien: Die Hilprecht-Sammlung der Universität Jena bewahrt Tausende Keilschrifttafeln aus Nippur. Bei uns sehen Sie die Orte, aus denen solche Schätze stammen — Babylon, Ur und Uruk.",
   [("Erfurt-Weimar (ERF), Leipzig/Halle (LEJ)", "Mit Umstieg über ein deutsches Drehkreuz oder Istanbul."), ("Frankfurt (FRA)", f"Mit dem ICE erreichbar; mit einem Umstieg über {HUB}.")],
   ["ur", "babylon", "samarra"], "Für Keilschrift-Begeisterte: In Babylon sehen Sie Originalziegel mit Nebukadnezars Namen in Keilschrift."),
}

HL = {"babylon": ("babylon-ishtar-gate", "Babylon", "Das Ischtar-Tor am Originalort, die Prozessionsstraße und der Löwe von Babylon."),
      "ur": ("ur-ziggurat", "Ur und Uruk", "Die über 4.000 Jahre alte Zikkurat von Ur und Uruk, wo die Schrift entstand."),
      "marshes": ("marshes-mashoof", "Die Marschen", "Mashoof-Bootsfahrt durch die UNESCO-Marschen, Schilfhäuser und Wasserbüffel."),
      "hatra": ("hatra", "Hatra", "Die Tempel der Wüstenstadt Hatra, UNESCO-Welterbe."),
      "samarra": ("samarra-malwiya", "Samarra", "Das Spiralminarett Malwiya und die goldene Kuppel von al-Askari."),
      "mosul": ("mosul-al-hadba-nuri", "Mossul und Ninive", "Die Altstadt von Mossul, das assyrische Nimrud und Hatra."),
      "kadhimiya": ("kadhimiya-shrine-night", "Bagdad", "Al-Kadhimiya, die Mutanabbi-Straße, die Qishla und der Abbasidenpalast."),
      "qishla": ("qishla-clock-tower-view", "Altes Bagdad", "Der Uhrturm der Qishla, die Mutanabbi-Straße und Tee im Café Shabandar."),
      "basra": ("basra-shatt-al-arab-sunset", "Basra", "Sonnenuntergang am Schatt al-Arab und die Shanasheel-Häuser der Altstadt.")}

PRICES = """      <div class="market-card" id="prices">
        <h3>Preise &amp; Zahlung</h3>
        <ul>
          <li><strong>7-Tage-Tour:</strong> US$2,500 pro Person im Doppelzimmer</li>
          <li><strong>9-Tage-Tour:</strong> US$3,400 pro Person im Doppelzimmer</li>
          <li>Einzelzimmerzuschlag bei Privatreisen: US$540</li>
          <li>Kleinkinder (1 Monat–2 Jahre) reisen kostenlos</li>
        </ul>
        <p>Kostenlose Stornierung, keine Anzahlung, Zahlung in Euro bei Ankunft möglich. Nicht enthalten: internationale Flüge, Visum, Mittag- und Abendessen. Lieber kürzer? Siehe unsere <a href="#day-trips">Tagesausflüge ab Bagdad</a>.</p>
      </div>"""


def links(cur):
    items = "".join((f'<li><strong>{esc(v[0])}</strong></li>' if k == cur else f'<li><a href="/de/iraq-tours-from-{k}/">{esc(v[0])}</a></li>') for k, v in L.items())
    return (f'    <div class="market-card market-links" style="margin-top:16px" id="by-state"><h3>Irak-Reisen nach Bundesland</h3>'
            f'<ul class="mkt-links">{items}</ul></div>\n')


def panel(key):
    n, aus, cities, intro, fl, hl, tip = L[key]
    fli = "".join(f"<li><strong>{esc(a)}:</strong> {esc(b)}</li>" for a, b in fl)
    hls = "".join(f'<div class="hl"><div class="ph" style="background-image:url(\'/img/{HL[i][0]}.webp\')" role="img" aria-label="{esc(HL[i][1])}"></div>'
                  f'<div class="bd"><h3>{esc(HL[i][1])}</h3><p>{esc(HL[i][2])}</p></div></div>' for i in hl)
    return f"""<section class="block in market-panel" id="for-{key}" aria-labelledby="{key}-heading">
    <div class="sec-head">
      <span class="eyebrow">Für Reisende {esc(aus)}</span>
      <h2 class="disp" id="{key}-heading">Irak-Reisen {esc(aus)}</h2>
      <p>{esc(intro)}</p>
    </div>
    <div class="market-grid">
      <div class="market-card" id="flights">
        <h3>Anreise {esc(aus)}</h3>
        <p>Internationale Flüge sind <strong>nicht</strong> im Reisepreis enthalten. Übliche Verbindungen:</p>
        <ul>{fli}</ul>
        <p class="market-note">Wir nennen keine Flugpreise — sie ändern sich täglich. Abholung je nach Programm in Bagdad, Basra oder Erbil. Nehmen Sie US-Dollar in bar mit; Karten werden außerhalb der Hotels selten akzeptiert.</p>
      </div>
      <div class="market-card" id="visa">
        <h3>Visum: deutscher oder irakischer Pass</h3>
        <p><strong>Deutscher Pass:</strong> Beantragen Sie das irakische E-Visum vor der Reise online über das offizielle Portal — ein Visum bei Ankunft gibt es nicht mehr. Gebühr und Gültigkeit sehen Sie bei der Antragstellung.</p>
        <p><strong>Irakischer Pass</strong> (auch bei doppelter Staatsangehörigkeit): Sie können mit Ihrem gültigen irakischen Pass ohne Visum einreisen.</p>
        <ul>
          <li><a href="https://eservice.evisa.iq" target="_blank" rel="noopener">eservice.evisa.iq</a> — Antragsportal</li>
          <li><a href="https://evisa.iq/en" target="_blank" rel="noopener">evisa.iq</a> — Informationen</li>
        </ul>
        <div class="market-info"><p><strong>Bitte vor der Reise prüfen.</strong> Die Regeln können sich ändern; der Pass sollte bei Ankunft meist noch mindestens sechs Monate gültig sein.</p></div>
      </div>
    </div>
    <div class="market-grid" style="margin-top:16px">
      <div class="market-card" id="family">
        <h3>Familienbesuch im Irak?</h3>
        <p>Verbinden Sie den Besuch bei Verwandten mit ein paar Tagen Rundreise. Wir holen Sie am <a href="#airport-transfer">Flughafen Bagdad</a> ab, bringen Sie ins Hotel oder zu Ihrer Familie und planen <a href="#day-trips">Tagesausflüge</a> nach Babylon, Samarra, Kerbela und Nadschaf oder in die Marschen. Unser Reiseleiter spricht Arabisch und Englisch.</p>
        <p>{esc(tip)}</p>
      </div>
{PRICES}
    </div>
    <div class="market-card" style="margin-top:16px" id="highlights">
      <h3>Was Sie sehen</h3>
      <div class="market-hl">{hls}</div>
    </div>
{links(key)}    <div class="market-info" id="travel-advice" style="margin-top:16px"><p><strong>Reisehinweise des Auswärtigen Amtes.</strong> Bitte lesen Sie vor Ihrer Entscheidung die aktuellen <a href="https://www.auswaertiges-amt.de/de/service/laender/irak-node/iraksicherheit-202738" target="_blank" rel="noopener">Reise- und Sicherheitshinweise für den Irak</a> und prüfen Sie, ob Ihre Reiseversicherung das Ziel abdeckt. Wir führen private Programme mit lokalen Reiseleitern durch und drängen niemanden zu einer Reise gegen die Empfehlungen seiner Regierung. Siehe auch: <a href="/de/iraq-tours-from-germany/">Irak-Reisen aus Deutschland</a>.</p></div>
  </section>"""


def meta(key):
    n, aus, cities, *_ = L[key]
    first = cities.split(",")[0].split(" und ")[0]
    return dict(title=f"Irak-Reise {aus}: Babylon, Ur & Marschen privat | Fable Tour",
                desc=f"Irak-Rundreise {aus} — {cities}: Flüge, E-Visum oder irakischer Pass, Familienbesuch, Babylon, Ur und die Marschen. Private 7- und 9-Tage-Touren ab $2,500.",
                kw=f"Irak Reise {n}, Irak Rundreise {first}, {first} Bagdad, Irak Reisen privat, Babylon besichtigen, Familienbesuch Irak, Irak E-Visum, Fable Tour",
                h1=f"Irak-Reisen {aus}", eyebrow=f"Für Reisende {aus}",
                lead=f"Für Reisende aus {cities}: Anreise, Visum und Familienbesuch, dazu Babylon, Ur und die Marschen — zwei Programme mit 4★–5★-Hotels und privatem Reiseleiter.",
                crumb=f"Irak-Reisen {aus}")


def run():
    src = (ROOT / "de/iraq-tours-from-germany/index.html").read_text()
    urls = []
    for key in L:
        u = f"{BASE}/de/iraq-tours-from-{key}/"
        m = meta(key)
        s = NA.set_meta(src, u, m, [("de", u), ("x-default", u)])
        s = NA.put_panel(s, panel(key))
        s = NA.set_ld(s, u, m, "de", [("Irak-Reisen aus Deutschland", f"{BASE}/de/iraq-tours-from-germany/")])
        s = NA.add_css(s, NA.LINKS_CSS, "mkt-links-css")
        out = ROOT / "de" / f"iraq-tours-from-{key}" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s)
        urls.append((u, [("de", u), ("x-default", u)]))
    # links card on the German-language Germany page
    f = ROOT / "de/iraq-tours-from-germany/index.html"
    s = f.read_text()
    s = re.sub(r'\s*<div class="market-card market-links"[^>]*id="by-state".*?</ul></div>\n?', "\n", s, flags=re.S)
    i = s.index("</section>", s.index('class="block in market-panel"'))
    s = s[:i].rstrip() + "\n" + links(None) + "  " + s[i:]
    s = NA.add_css(s, NA.LINKS_CSS, "mkt-links-css")
    f.write_text(s)
    import add_markets as A
    A.sitemap(urls)
    print("built", len(urls), "state pages")


if __name__ == "__main__":
    run()
