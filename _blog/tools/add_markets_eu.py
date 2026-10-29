#!/usr/bin/env python3
"""Country landing pages (Oct 2026): Germany, Switzerland, Austria, Luxembourg, Portugal, Spain,
Belgium, the Netherlands and Indonesia — one page per local language (copy of that language's
homepage) plus English, all linked to each other with hreflang. Built with add_markets.build();
multilingual countries (CH, LU, BE) get the full hreflang set afterwards. Not linked from the
homepages. Idempotent:  python3 _blog/tools/add_markets_eu.py
German state pages: add_markets_de_states.py (run after this script)."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import add_markets as A

A.UI.update({
 "de": ("Für Reisende aus {c}", "Irak-Reisen aus {c}", "Anreise aus {c}", "Was Sie sehen", "Zu den Programmen ↓"),
 "fr": ("Pour les voyageurs de {c}", "Voyages en Irak depuis {c}", "Venir en Irak depuis {c}", "À voir", "Voir les programmes ↓"),
 "es": ("Para viajeros desde {c}", "Viajes a Irak desde {c}", "Cómo llegar a Irak desde {c}", "Qué verás", "Ver los programas ↓"),
 "nl": ("Voor reizigers uit {c}", "Irak-reizen vanuit {c}", "Reizen naar Irak vanuit {c}", "Wat u ziet", "Bekijk de programma's ↓"),
 "id": ("Untuk wisatawan dari {c}", "Tur Irak dari {c}", "Perjalanan dari {c} ke Irak", "Yang akan Anda lihat", "Lihat program ↓"),
 "pt": ("Para viajantes de {c}", "Viagens ao Iraque a partir de {c}", "Como chegar ao Iraque a partir de {c}", "O que vai ver", "Ver os programas ↓"),
})
VISA_EU = {
 "en": ("Iraq visa", "Citizens of EU countries and Switzerland apply online for the Iraqi e-visa before travel through the official portal (evisa.iq), which also covers the Kurdistan Region — visa on arrival is no longer available. The fee and validity are shown when you apply. Rules can change, so always check shortly before you travel."),
 "de": ("Visum für den Irak", "Bürger der EU-Staaten und der Schweiz beantragen das irakische E-Visum vor der Reise online über das offizielle Portal (evisa.iq), das auch die Region Kurdistan abdeckt — ein Visum bei Ankunft gibt es nicht mehr. Gebühr und Gültigkeit werden bei der Antragstellung angezeigt. Die Regeln können sich ändern; bitte prüfen Sie sie kurz vor der Reise."),
 "fr": ("Visa pour l'Irak", "Les citoyens de l'UE et de la Suisse demandent le visa électronique irakien en ligne avant le départ sur le portail officiel (evisa.iq), valable aussi pour la région du Kurdistan — le visa à l'arrivée n'est plus disponible. Les frais et la validité s'affichent lors de la demande. Les règles peuvent changer : vérifiez-les peu avant le départ."),
 "es": ("Visado para Irak", "Los ciudadanos de la UE y de Suiza solicitan el visado electrónico iraquí en línea antes de viajar en el portal oficial (evisa.iq), que también cubre la región del Kurdistán; el visado a la llegada ya no está disponible. La tasa y la validez se muestran al solicitarlo. Las normas pueden cambiar: compruébalas poco antes de viajar."),
 "nl": ("Visum voor Irak", "Burgers van EU-landen en Zwitserland vragen het Iraakse e-visum vóór vertrek online aan via het officiële portaal (evisa.iq), dat ook de regio Koerdistan dekt — een visum bij aankomst is niet meer mogelijk. Kosten en geldigheid ziet u bij de aanvraag. De regels kunnen veranderen; controleer ze kort voor vertrek."),
 "pt": ("Visto para o Iraque", "Os cidadãos da UE e da Suíça pedem o visto eletrónico iraquiano online antes da viagem no portal oficial (evisa.iq), válido também para a Região do Curdistão — o visto à chegada já não está disponível. A taxa e a validade aparecem no pedido. As regras podem mudar: confirme-as pouco antes de viajar."),
}
A.VISA.update({
 "id": ("Visa Irak", "Visa Irak diterbitkan melalui portal e-visa resmi (evisa.iq), yang juga mencakup Wilayah Kurdistan. Ketentuan berbeda menurut kewarganegaraan dan dapat berubah, jadi periksa kelayakan Anda di portal atau Kedutaan Besar Irak sebelum memesan. Jika kewarganegaraan Anda tidak dapat mengajukan secara online, kami mengurus visa Anda (US$300) bila Anda memesan tur lengkap — setengah dibayar di muka, sisanya saat tiba."),
})

HUB = {"en": "Istanbul, Doha, Dubai or Amman", "de": "Istanbul, Doha, Dubai oder Amman", "fr": "Istanbul, Doha, Dubaï ou Amman",
       "es": "Estambul, Doha, Dubái o Amán", "nl": "Istanbul, Doha, Dubai of Amman", "pt": "Istambul, Doha, Dubai ou Amã"}
HL = {
 "en": [("babylon", "Babylon", "The Ishtar Gate, the Processional Way and the Lion of Babylon."), ("ur", "Ur & the Marshes", "The ziggurat of Ur and a mashoof boat ride in the UNESCO-listed Marshes."), ("hatra", "Hatra & Mosul", "The desert temples of Hatra, Assyrian Nimrud and Old Mosul.")],
 "de": [("babylon", "Babylon", "Das Ischtar-Tor am Originalort, die Prozessionsstraße und der Löwe von Babylon."), ("ur", "Ur und die Marschen", "Die Zikkurat von Ur und eine Mashoof-Bootsfahrt durch die UNESCO-Marschen."), ("hatra", "Hatra und Mossul", "Die Wüstentempel von Hatra, das assyrische Nimrud und die Altstadt von Mossul.")],
 "fr": [("babylon", "Babylone", "La porte d'Ishtar, la voie processionnelle et le lion de Babylone."), ("ur", "Ur et les marais", "La ziggourat d'Ur et une balade en mashoof dans les marais classés par l'UNESCO."), ("hatra", "Hatra et Mossoul", "Les temples de Hatra dans le désert, Nimroud l'assyrienne et la vieille Mossoul.")],
 "es": [("babylon", "Babilonia", "La Puerta de Ishtar, la Vía Procesional y el León de Babilonia."), ("ur", "Ur y las marismas", "El zigurat de Ur y un paseo en mashoof por las marismas, Patrimonio de la UNESCO."), ("hatra", "Hatra y Mosul", "Los templos de Hatra en el desierto, la asiria Nimrud y el casco antiguo de Mosul.")],
 "nl": [("babylon", "Babylon", "De Isjtarpoort, de Processieweg en de Leeuw van Babylon."), ("ur", "Ur en de moerassen", "De ziggurat van Ur en een tocht met de mashoof door de UNESCO-moerassen."), ("hatra", "Hatra en Mosul", "De woestijntempels van Hatra, het Assyrische Nimrud en het oude Mosul.")],
 "pt": [("babylon", "Babilónia", "A Porta de Ishtar, a Via Processional e o Leão de Babilónia."), ("ur", "Ur e os pântanos", "O zigurate de Ur e um passeio de mashoof pelos pântanos, Património da UNESCO."), ("hatra", "Hatra e Mossul", "Os templos de Hatra no deserto, a assíria Nimrud e a velha Mossul.")],
}


def T(lang, title, desc, kw, h1, lead, intro, travel, hl=None):
    return dict(title=title, desc=desc, kw=kw, h1=h1, lead=lead, intro=intro, travel=travel, hl=hl or HL[lang])


EN_LEAD = "Babylon, Ur, the Marshes, Samarra, Hatra and Erbil — two programmes with 4★–5★ hotels and a private guide, from US$2,500."
EN_INTRO = "We arrange a private trip for you, your family or friends on the date you choose — airport welcome, private car and guide from arrival to departure — or join a small group."

# market key -> (slug, [languages, local first], names, texts, eu?)
MK = {}
def mk(key, langs, names, texts, eu=True):
    MK[key] = dict(slug=f"iraq-tours-from-{key}", langs=langs, names=names, texts=texts, eu=eu)

mk("germany", ["de", "en"], {"de": "Deutschland", "en": "Germany"}, {
 "de": T("de", "Irak-Reise aus Deutschland: Babylon, Ur & Marschen privat | Fable Tour",
   "Irak-Rundreise ab Deutschland: E-Visum für deutsche Pässe, Flüge ab Frankfurt, München, Berlin und Düsseldorf, Babylon, Ur, die Marschen und Hatra. Private 7- und 9-Tage-Touren ab $2,500.",
   "Irak Reise, Irak Rundreise Deutschland, Irak Reisen privat, Babylon besichtigen, Irak E-Visum Deutsche, Frankfurt Bagdad, Mesopotamien Reise, Fable Tour",
   "Irak-Reisen aus Deutschland", "Babylon, Ur, die Marschen, Samarra, Hatra und Erbil — zwei Programme mit 4★–5★-Hotels und privatem Reiseleiter, ab US$2,500.",
   "Das Ischtar-Tor kennen Sie vielleicht aus dem Pergamonmuseum — bei uns stehen Sie an seinem Originalort in Babylon. Wir organisieren Ihre private Reise zum Wunschtermin, mit Empfang am Flughafen, Privatwagen und Reiseleiter von der Ankunft bis zum Abflug.",
   f"Von Frankfurt, München, Berlin, Düsseldorf oder Hamburg fliegen Sie mit einem Umstieg über {HUB['de']} nach Bagdad, Basra oder Erbil; zeitweise gibt es auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen). Der Irak liegt im Winter 2 Stunden, im Sommer 1 Stunde vor Deutschland. Euro werden in großen Städten getauscht, am einfachsten sind US-Dollar in bar."),
 "en": T("en", "Iraq Tours from Germany: Flights, E-visa & Babylon | Fable Tour",
   "Iraq tours from Germany: e-visa for German passports, flights from Frankfurt, Munich, Berlin and Düsseldorf, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Germany, Iraq travel Germany, Frankfurt to Baghdad, Iraq e-visa German passport, Babylon tour, Fable Tour",
   "Iraq tours from Germany", EN_LEAD,
   "You may know the Ishtar Gate from Berlin's Pergamon Museum — with us you stand at its original site in Babylon. " + EN_INTRO,
   f"From Frankfurt, Munich, Berlin, Düsseldorf or Hamburg, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil; direct flights to Erbil operate in some seasons (check current schedules). Iraq is 2 hours ahead of Germany in winter, 1 hour in summer. Bring US dollars in cash.")})

mk("switzerland", ["de", "fr", "en"], {"de": "der Schweiz", "fr": "Suisse", "en": "Switzerland"}, {
 "de": T("de", "Irak-Reise aus der Schweiz: Babylon, Ur & Marschen | Fable Tour",
   "Irak-Rundreise ab der Schweiz: E-Visum für Schweizer Pässe, Flüge ab Zürich und Genf, Babylon, Ur, die Marschen und Hatra. Private 7- und 9-Tage-Touren ab $2,500.",
   "Irak Reise Schweiz, Irak Rundreise ab Zürich, Babylon besichtigen, Irak E-Visum Schweizer, Zürich Bagdad, Mesopotamien Reise, Fable Tour",
   "Irak-Reisen aus der Schweiz", "Babylon, Ur, die Marschen, Samarra, Hatra und Erbil — zwei Programme mit 4★–5★-Hotels und privatem Reiseleiter, ab US$2,500.",
   "Wir organisieren Ihre private Irak-Reise zum Wunschtermin — mit Empfang am Flughafen, Privatwagen und Reiseleiter von der Ankunft bis zum Abflug, oder Sie schliessen sich einer kleinen Gruppe an.",
   f"Ab Zürich, Genf oder Basel fliegen Sie mit einem Umstieg über {HUB['de']} nach Bagdad, Basra oder Erbil (aktuelle Flugpläne prüfen). Der Irak liegt im Winter 2 Stunden, im Sommer 1 Stunde vor der Schweiz. Franken lassen sich schwer wechseln — nehmen Sie US-Dollar in bar mit."),
 "fr": T("fr", "Voyage en Irak depuis la Suisse : Babylone, Ur et marais | Fable Tour",
   "Voyage en Irak depuis la Suisse : visa électronique pour passeports suisses, vols depuis Genève et Zurich, Babylone, Ur, les marais et Hatra. Circuits privés de 7 et 9 jours dès 2 500 $.",
   "voyage Irak Suisse, circuit Irak Genève, visiter Babylone, visa Irak Suisses, Genève Bagdad, voyage Mésopotamie, Fable Tour",
   "Voyages en Irak depuis la Suisse", "Babylone, Ur, les marais, Samarra, Hatra et Erbil — deux programmes en hôtels 4★–5★ avec guide privé, dès 2 500 $ US.",
   "Nous organisons votre voyage privé en Irak à la date de votre choix — accueil à l'aéroport, voiture privée et guide de l'arrivée au départ — ou rejoignez un petit groupe.",
   f"Depuis Genève, Zurich ou Bâle, comptez une escale via {HUB['fr']} pour Bagdad, Bassora ou Erbil (vérifiez les horaires en vigueur). L'Irak a 2 heures d'avance sur la Suisse en hiver, 1 heure en été. Les francs suisses se changent mal : prévoyez des dollars américains en espèces."),
 "en": T("en", "Iraq Tours from Switzerland: Flights, E-visa & Babylon | Fable Tour",
   "Iraq tours from Switzerland: e-visa for Swiss passports, flights from Zurich and Geneva, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Switzerland, Zurich to Baghdad, Geneva to Baghdad, Iraq e-visa Swiss passport, Babylon tour, Fable Tour",
   "Iraq tours from Switzerland", EN_LEAD, EN_INTRO,
   f"From Zurich, Geneva or Basel, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Iraq is 2 hours ahead of Switzerland in winter, 1 hour in summer. Swiss francs are hard to exchange — bring US dollars in cash.")})

mk("austria", ["de", "en"], {"de": "Österreich", "en": "Austria"}, {
 "de": T("de", "Irak-Reise aus Österreich: Babylon, Ur & Marschen | Fable Tour",
   "Irak-Rundreise ab Österreich: E-Visum für österreichische Pässe, Flüge ab Wien, Babylon, Ur, die Marschen und Hatra. Private 7- und 9-Tage-Touren ab $2,500.",
   "Irak Reise Österreich, Irak Rundreise ab Wien, Babylon besichtigen, Irak E-Visum Österreicher, Wien Bagdad, Wien Erbil, Fable Tour",
   "Irak-Reisen aus Österreich", "Babylon, Ur, die Marschen, Samarra, Hatra und Erbil — zwei Programme mit 4★–5★-Hotels und privatem Reiseleiter, ab US$2,500.",
   "Wir organisieren Ihre private Irak-Reise zum Wunschtermin — mit Empfang am Flughafen, Privatwagen und Reiseleiter von der Ankunft bis zum Abflug, oder Sie schließen sich einer kleinen Gruppe an.",
   f"Ab Wien fliegen Sie mit einem Umstieg über {HUB['de']} nach Bagdad, Basra oder Erbil; zeitweise gibt es auch Direktflüge nach Erbil (aktuelle Flugpläne prüfen). Ab Salzburg, Graz oder Innsbruck über Wien oder München. Der Irak liegt im Winter 2 Stunden, im Sommer 1 Stunde vor Österreich. Nehmen Sie US-Dollar in bar mit."),
 "en": T("en", "Iraq Tours from Austria: Flights from Vienna, E-visa | Fable Tour",
   "Iraq tours from Austria: e-visa for Austrian passports, flights from Vienna, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Austria, Vienna to Baghdad, Vienna to Erbil, Iraq e-visa Austrian passport, Babylon tour, Fable Tour",
   "Iraq tours from Austria", EN_LEAD, EN_INTRO,
   f"From Vienna, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil; direct flights to Erbil operate in some seasons (check current schedules). Iraq is 2 hours ahead of Austria in winter, 1 hour in summer. Bring US dollars in cash.")})

mk("luxembourg", ["fr", "de", "en"], {"fr": "Luxembourg", "de": "Luxemburg", "en": "Luxembourg"}, {
 "fr": T("fr", "Voyage en Irak depuis le Luxembourg : Babylone et Ur | Fable Tour",
   "Voyage en Irak depuis le Luxembourg : visa électronique, vols via Francfort, Bruxelles, Paris ou Istanbul, Babylone, Ur, les marais et Hatra. Circuits privés de 7 et 9 jours dès 2 500 $.",
   "voyage Irak Luxembourg, circuit Irak, visiter Babylone, visa Irak Luxembourgeois, Luxembourg Bagdad, Fable Tour",
   "Voyages en Irak depuis le Luxembourg", "Babylone, Ur, les marais, Samarra, Hatra et Erbil — deux programmes en hôtels 4★–5★ avec guide privé, dès 2 500 $ US.",
   "Nous organisons votre voyage privé en Irak à la date de votre choix — accueil à l'aéroport, voiture privée et guide de l'arrivée au départ — ou rejoignez un petit groupe.",
   f"Depuis Luxembourg (LUX), rejoignez Bagdad, Bassora ou Erbil avec une escale via Istanbul, ou au départ de Francfort, Bruxelles ou Paris via {HUB['fr']} (vérifiez les horaires en vigueur). L'Irak a 2 heures d'avance en hiver, 1 heure en été. Prévoyez des dollars américains en espèces."),
 "de": T("de", "Irak-Reise aus Luxemburg: Babylon, Ur & Marschen | Fable Tour",
   "Irak-Rundreise ab Luxemburg: E-Visum, Flüge über Frankfurt, Brüssel, Paris oder Istanbul, Babylon, Ur, die Marschen und Hatra. Private 7- und 9-Tage-Touren ab $2,500.",
   "Irak Reise Luxemburg, Irak Rundreise, Babylon besichtigen, Irak E-Visum, Luxemburg Bagdad, Fable Tour",
   "Irak-Reisen aus Luxemburg", "Babylon, Ur, die Marschen, Samarra, Hatra und Erbil — zwei Programme mit 4★–5★-Hotels und privatem Reiseleiter, ab US$2,500.",
   "Wir organisieren Ihre private Irak-Reise zum Wunschtermin — mit Empfang am Flughafen, Privatwagen und Reiseleiter von der Ankunft bis zum Abflug.",
   f"Ab Luxemburg (LUX) mit einem Umstieg in Istanbul, oder ab Frankfurt, Brüssel oder Paris über {HUB['de']} nach Bagdad, Basra oder Erbil (aktuelle Flugpläne prüfen). Nehmen Sie US-Dollar in bar mit."),
 "en": T("en", "Iraq Tours from Luxembourg: Flights, E-visa & Babylon | Fable Tour",
   "Iraq tours from Luxembourg: e-visa, flights via Frankfurt, Brussels, Paris or Istanbul, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Luxembourg, Luxembourg to Baghdad, Iraq e-visa Luxembourg, Babylon tour, Fable Tour",
   "Iraq tours from Luxembourg", EN_LEAD, EN_INTRO,
   f"From Luxembourg (LUX), connect via Istanbul, or fly from Frankfurt, Brussels or Paris via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Bring US dollars in cash.")})

mk("portugal", ["pt", "en"], {"pt": "Portugal", "en": "Portugal"}, {
 "pt": T("pt", "Viagem ao Iraque a partir de Portugal: Babilónia e Ur | Fable Tour",
   "Viagem ao Iraque a partir de Portugal: visto eletrónico para portugueses, voos de Lisboa e do Porto, Babilónia, Ur, os pântanos e Hatra. Viagens privadas de 7 e 9 dias desde $2,500.",
   "viagem ao Iraque, circuito Iraque Portugal, visitar Babilónia, visto Iraque portugueses, Lisboa Bagdade, viagem Mesopotâmia, Fable Tour",
   "Viagens ao Iraque a partir de Portugal", "Babilónia, Ur, os pântanos, Samarra, Hatra e Erbil — dois programas com hotéis 4★–5★ e guia privado, desde 2 500 US$.",
   "Organizamos a sua viagem privada ao Iraque na data que escolher — receção no aeroporto, carro privado e guia desde a chegada até à partida — ou junte-se a um pequeno grupo.",
   f"De Lisboa ou do Porto voa com uma escala via {HUB['pt']} até Bagdade, Baçorá ou Erbil (confirme os horários em vigor). O Iraque está 3 horas à frente de Portugal no inverno e 2 horas no verão. Leve dólares americanos em numerário."),
 "en": T("en", "Iraq Tours from Portugal: Flights from Lisbon, E-visa | Fable Tour",
   "Iraq tours from Portugal: e-visa for Portuguese passports, flights from Lisbon and Porto, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Portugal, Lisbon to Baghdad, Iraq e-visa Portugal, Babylon tour, Fable Tour",
   "Iraq tours from Portugal", EN_LEAD, EN_INTRO,
   f"From Lisbon or Porto, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Iraq is 3 hours ahead of Portugal in winter, 2 in summer. Bring US dollars in cash.")})

mk("spain", ["es", "en"], {"es": "España", "en": "Spain"}, {
 "es": T("es", "Viaje a Irak desde España: Babilonia, Ur y marismas | Fable Tour",
   "Viaje a Irak desde España: visado electrónico para españoles, vuelos desde Madrid y Barcelona, Babilonia, Ur, las marismas y Hatra. Tours privados de 7 y 9 días desde $2,500.",
   "viaje a Irak, viaje a Irak desde España, circuito Irak, visitar Babilonia, visado Irak españoles, Madrid Bagdad, Barcelona Bagdad, Fable Tour",
   "Viajes a Irak desde España", "Babilonia, Ur, las marismas, Samarra, Hatra y Erbil — dos programas con hoteles de 4★–5★ y guía privado, desde 2.500 USD.",
   "Organizamos tu viaje privado a Irak en la fecha que elijas — recepción en el aeropuerto, coche privado y guía desde la llegada hasta la salida — o únete a un grupo reducido.",
   f"Desde Madrid, Barcelona, Málaga o Valencia vuelas con una escala vía {HUB['es']} a Bagdad, Basora o Erbil (consulta los horarios vigentes). Irak va 2 horas por delante de España en invierno y 1 hora en verano. Lleva dólares estadounidenses en efectivo."),
 "en": T("en", "Iraq Tours from Spain: Flights from Madrid, E-visa | Fable Tour",
   "Iraq tours from Spain: e-visa for Spanish passports, flights from Madrid and Barcelona, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Spain, Madrid to Baghdad, Barcelona to Baghdad, Iraq e-visa Spain, Babylon tour, Fable Tour",
   "Iraq tours from Spain", EN_LEAD, EN_INTRO,
   f"From Madrid, Barcelona, Málaga or Valencia, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Iraq is 2 hours ahead of Spain in winter, 1 in summer. Bring US dollars in cash.")})

mk("belgium", ["nl", "fr", "en"], {"nl": "België", "fr": "Belgique", "en": "Belgium"}, {
 "nl": T("nl", "Reis naar Irak vanuit België: Babylon, Ur & moerassen | Fable Tour",
   "Rondreis Irak vanuit België: e-visum voor Belgische paspoorten, vluchten vanaf Brussel, Babylon, Ur, de moerassen en Hatra. Privéreizen van 7 en 9 dagen vanaf $2,500.",
   "reis naar Irak, rondreis Irak België, Babylon bezoeken, visum Irak Belgen, Brussel Bagdad, Mesopotamië reis, Fable Tour",
   "Irak-reizen vanuit België", "Babylon, Ur, de moerassen, Samarra, Hatra en Erbil — twee programma's met 4★–5★-hotels en een privégids, vanaf US$2,500.",
   "We organiseren uw privéreis naar Irak op de datum van uw keuze — ontvangst op de luchthaven, privéauto en gids van aankomst tot vertrek — of sluit aan bij een kleine groep.",
   f"Vanaf Brussel (BRU) of Charleroi vliegt u met één overstap via {HUB['nl']} naar Bagdad, Basra of Erbil (controleer de actuele dienstregeling). Irak loopt in de winter 2 uur, in de zomer 1 uur voor op België. Neem Amerikaanse dollars contant mee."),
 "fr": T("fr", "Voyage en Irak depuis la Belgique : Babylone et Ur | Fable Tour",
   "Voyage en Irak depuis la Belgique : visa électronique pour passeports belges, vols depuis Bruxelles, Babylone, Ur, les marais et Hatra. Circuits privés de 7 et 9 jours dès 2 500 $.",
   "voyage Irak Belgique, circuit Irak Bruxelles, visiter Babylone, visa Irak Belges, Bruxelles Bagdad, Fable Tour",
   "Voyages en Irak depuis la Belgique", "Babylone, Ur, les marais, Samarra, Hatra et Erbil — deux programmes en hôtels 4★–5★ avec guide privé, dès 2 500 $ US.",
   "Nous organisons votre voyage privé en Irak à la date de votre choix — accueil à l'aéroport, voiture privée et guide de l'arrivée au départ — ou rejoignez un petit groupe.",
   f"Depuis Bruxelles (BRU) ou Charleroi, comptez une escale via {HUB['fr']} pour Bagdad, Bassora ou Erbil (vérifiez les horaires en vigueur). L'Irak a 2 heures d'avance sur la Belgique en hiver, 1 heure en été. Prévoyez des dollars américains en espèces."),
 "en": T("en", "Iraq Tours from Belgium: Flights from Brussels, E-visa | Fable Tour",
   "Iraq tours from Belgium: e-visa for Belgian passports, flights from Brussels, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from Belgium, Brussels to Baghdad, Iraq e-visa Belgium, Babylon tour, Fable Tour",
   "Iraq tours from Belgium", EN_LEAD, EN_INTRO,
   f"From Brussels (BRU) or Charleroi, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Iraq is 2 hours ahead of Belgium in winter, 1 in summer. Bring US dollars in cash.")})

mk("netherlands", ["nl", "en"], {"nl": "Nederland", "en": "the Netherlands"}, {
 "nl": T("nl", "Reis naar Irak vanuit Nederland: Babylon & Ur privé | Fable Tour",
   "Rondreis Irak vanuit Nederland: e-visum voor Nederlandse paspoorten, vluchten vanaf Amsterdam, Babylon, Ur, de moerassen en Hatra. Privéreizen van 7 en 9 dagen vanaf $2,500.",
   "reis naar Irak, rondreis Irak Nederland, Babylon bezoeken, visum Irak Nederlanders, Amsterdam Bagdad, Mesopotamië reis, Fable Tour",
   "Irak-reizen vanuit Nederland", "Babylon, Ur, de moerassen, Samarra, Hatra en Erbil — twee programma's met 4★–5★-hotels en een privégids, vanaf US$2,500.",
   "We organiseren uw privéreis naar Irak op de datum van uw keuze — ontvangst op de luchthaven, privéauto en gids van aankomst tot vertrek — of sluit aan bij een kleine groep.",
   f"Vanaf Amsterdam Schiphol, Eindhoven of Rotterdam vliegt u met één overstap via {HUB['nl']} naar Bagdad, Basra of Erbil (controleer de actuele dienstregeling). Irak loopt in de winter 2 uur, in de zomer 1 uur voor op Nederland. Neem Amerikaanse dollars contant mee."),
 "en": T("en", "Iraq Tours from the Netherlands: Flights, E-visa & Babylon | Fable Tour",
   "Iraq tours from the Netherlands: e-visa for Dutch passports, flights from Amsterdam, Babylon, Ur, the Marshes and Hatra. Private 7 & 9-day tours from $2,500.",
   "Iraq tours from the Netherlands, Amsterdam to Baghdad, Iraq e-visa Dutch passport, Babylon tour, Fable Tour",
   "Iraq tours from the Netherlands", EN_LEAD, EN_INTRO,
   f"From Amsterdam Schiphol, Eindhoven or Rotterdam, fly with one stop via {HUB['en']} to Baghdad, Basra or Erbil (check current schedules). Iraq is 2 hours ahead of the Netherlands in winter, 1 in summer. Bring US dollars in cash.")})

mk("indonesia", ["id", "en"], {"id": "Indonesia", "en": "Indonesia"}, {
 "id": T("id", "Tur Ziarah & Wisata Irak dari Indonesia: Karbala, Najaf, Baghdad | Fable Tour",
   "Tur ziarah dan wisata Irak dari Indonesia bersama pemandu dari Baghdad: Karbala, Najaf, Kadhimiya, makam Syekh Abdul Qadir Jailani, Samarra dan Babilonia. Program 7 atau 9 hari.",
   "tur Irak dari Indonesia, ziarah Irak, ziarah Karbala, ziarah Najaf, makam Syekh Abdul Qadir Jailani, paket tur Irak, Jakarta Baghdad, Fable Tour",
   "Tur ziarah & wisata Irak dari Indonesia", "Ziarah ke Karbala, Najaf, Kadhimiya dan Samarra, makam Syekh Abdul Qadir Jailani dan Imam Abu Hanifah di Baghdad, serta Babilonia dan Ur — hotel bintang 4–5 dan pemandu pribadi, mulai US$2,500.",
   "Kami mengatur perjalanan pribadi untuk Anda dan keluarga pada tanggal pilihan Anda, dengan pemandu dari Baghdad dan mobil pribadi selama perjalanan, agar ziarah terasa nyaman dan tenang.",
   "Dari Jakarta (CGK), Surabaya atau Denpasar, penerbangan dengan satu transit melalui Doha, Dubai, Abu Dhabi atau Istanbul menuju Baghdad, Najaf atau Erbil (periksa jadwal terbaru). Irak 4 jam lebih lambat dari WIB. Bawa dolar AS tunai — rupiah sulit ditukar di Irak. Pemandu kami berbahasa Arab dan Inggris.",
   [("shrines", "Karbala & Najaf", "Makam Imam Husain dan Abbas di Karbala, makam Imam Ali di Najaf, Masjid Agung Kufah dan Wadi as-Salam."),
    ("gilani", "Makam-makam di Baghdad", "Syekh Abdul Qadir Jailani, Imam Abu Hanifah, Kadhimiya dan Junaid al-Baghdadi."),
    ("babylon", "Babilonia & Ur", "Gerbang Ishtar, Singa Babilonia dan ziggurat kuno di Ur.")]),
 "en": T("en", "Iraq Ziyarah & Tours from Indonesia: Karbala, Najaf | Fable Tour",
   "Iraq ziyarah and tours from Indonesia with a Baghdad-based guide: Karbala, Najaf, Kadhimiya, the shrine of Sheikh Abdul Qadir Gilani, Samarra and Babylon. 7 or 9 days.",
   "Iraq tours from Indonesia, Iraq ziyarah Indonesia, Karbala ziyarah, Najaf, Abdul Qadir Gilani shrine, Jakarta to Baghdad, Fable Tour",
   "Iraq ziyarah & tours from Indonesia", "Ziyarah to Karbala, Najaf, Kadhimiya and Samarra, the shrines of Sheikh Abdul Qadir Gilani and Imam Abu Hanifa in Baghdad, plus Babylon and Ur — 4★–5★ hotels and a private guide, from US$2,500.",
   "We arrange a private trip for you and your family on the date you choose, with a guide from Baghdad and a private car throughout, so you can visit in comfort and peace.",
   "From Jakarta (CGK), Surabaya or Denpasar, fly with one stop via Doha, Dubai, Abu Dhabi or Istanbul to Baghdad, Najaf or Erbil (check current schedules). Iraq is 4 hours behind Jakarta. Bring US dollars in cash. Our guides work in Arabic and English.",
   [("shrines", "Karbala & Najaf", "The shrines of Imam Hussein and al-Abbas, the shrine of Imam Ali, the Great Mosque of Kufa and Wadi al-Salam."),
    ("gilani", "The shrines of Baghdad", "Sheikh Abdul Qadir Gilani, Imam Abu Hanifa, Kadhimiya and Junayd al-Baghdadi."),
    ("babylon", "Babylon & Ur", "The Ishtar Gate, the Lion of Babylon and the ancient ziggurat of Ur.")])}, eu=False)


def url(key, lang):
    return f"{A.BASE}/{lang}/{MK[key]['slug']}/"


def run():
    urls = []
    base_visa = dict(A.VISA)
    for key, m in MK.items():
        alts = [(l, url(key, l)) for l in m["langs"]] + [("x-default", url(key, "en"))]
        for lang in m["langs"]:
            A.M.clear()
            A.market(key, m["slug"], lang, m["names"], m["texts"])
            A.VISA.clear(); A.VISA.update(base_visa)
            if m["eu"]:
                A.VISA[lang] = VISA_EU[lang]
            A.build(key, lang)
            f = A.ROOT / lang / m["slug"] / "index.html"
            s = f.read_text()
            s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", s)
            links = "".join(f'<link rel="alternate" hreflang="{l}" href="{x}">\n' for l, x in alts)
            s = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda x: x.group(1) + links, s, count=1)
            f.write_text(s)
            urls.append((url(key, lang), alts))
    A.VISA.clear(); A.VISA.update(base_visa)
    A.sitemap(urls)
    print("built", len(urls), "pages")


if __name__ == "__main__":
    run()
