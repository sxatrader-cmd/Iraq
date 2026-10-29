#!/usr/bin/env python3
"""North-America landing pages (Oct 2026).
- es/iraq-tours-from-usa/   : Spanish version of the US page (copy of the Spanish homepage)
- fr/iraq-tours-from-canada/: French version of the Canada page (copy of the French homepage)
- en/iraq-tours-from-<state>/ for US states and Canadian provinces with Iraqi / Arab communities
  (copies of the English USA / Canada page with their own panel, meta, H1 and JSON-LD).
The English USA and Canada pages get a "by state / by province" links card and hreflang to es / fr.
Not linked from any homepage. Idempotent: run again after editing the texts."""
import re, json, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from add_markets import absolutize, BASE, TODAY

ROOT = pathlib.Path(__file__).resolve().parents[2]
esc = lambda s: html.escape(s, quote=True)
HUBS = "Istanbul (Turkish Airlines), Doha (Qatar Airways), Dubai (Emirates) or Amman (Royal Jordanian)"

# ------------------------------------------------------------------ US states / Canadian provinces
# key: (slug-part, name, country, cities in intro, community text, airports [(label, text)], highlights keys, extra tip)
S = {}
def st(key, name, country, cities, community, flights, hl, tip):
    S[key] = dict(slug=f"iraq-tours-from-{key}", name=name, country=country, cities=cities,
                  community=community, flights=flights, hl=hl, tip=tip)

st("michigan", "Michigan", "us", "Dearborn, Detroit, Sterling Heights and Troy",
   "Metro Detroit is home to one of the largest Iraqi and Arab communities outside the Middle East — from Dearborn and Dearborn Heights to the Chaldean neighbourhoods of Sterling Heights, Warren, Troy and West Bloomfield. Many families here travel back to Baghdad, Basra, Mosul and the Nineveh Plains every year; we help you turn that visit into a proper journey through the country.",
   [("Detroit (DTW) → Baghdad (BGW), Erbil (EBL) or Basra (BSR)", f"One-stop connections via {HUBS} are the usual routes. Many Detroit families fly into Erbil for the north and Baghdad for the centre and south."),
    ("Grand Rapids (GRR), Flint (FNT), Lansing (LAN)", "Connect through Detroit, Chicago or a European hub.")],
   ["mosul", "babylon", "kadhimiya"],
   "Visiting relatives in the Nineveh Plains? Our 7- and 9-day programmes pass through Mosul, Nimrud and Hatra — we can end a day near your family's town.")

st("california", "California", "us", "San Diego, El Cajon, Los Angeles, Anaheim and the Central Valley",
   "California has large Iraqi communities — El Cajon and San Diego County above all, with Chaldean and Assyrian families, as well as Los Angeles, Anaheim's Little Arabia, Sacramento and the Assyrian communities of Turlock and Modesto. Whether you were born in Baghdad or grew up in San Diego, we show you Iraq with a private guide.",
   [("San Diego (SAN), Los Angeles (LAX) → Baghdad (BGW) / Erbil (EBL)", f"One-stop or two-stop routes via {HUBS}. From LAX there are long-haul flights to Doha, Dubai and Istanbul."),
    ("San Francisco (SFO), Sacramento (SMF), Fresno (FAT)", "Usually via Doha, Dubai, Istanbul or a European hub, with a connection from smaller airports.")],
   ["mosul", "babylon", "ur"],
   "The flight from the West Coast is long: we recommend arriving a day early in Baghdad. We can meet you at the airport and take you to your hotel.")

st("illinois", "Illinois", "us", "Chicago, Skokie, Niles and Bridgeview",
   "Chicagoland has deep Assyrian and Iraqi roots on the North Side and in Skokie, Niles and Morton Grove, and a large Arab community in the south-west suburbs around Bridgeview. We meet families and second-generation travellers from Chicago who want to see Babylon, Ur and the Marshes — not only the family home.",
   [("Chicago O'Hare (ORD) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}. O'Hare has nonstop flights to Istanbul, Doha and Dubai (check current schedules)."),
    ("Midway (MDW), Peoria (PIA), Springfield (SPI)", "Connect through O'Hare or another US hub.")],
   ["mosul", "babylon", "marshes"],
   "Many of our Chicago guests start in the north (Erbil, Mosul, Nimrud) and finish in Baghdad — our 9-day tour does the route the other way, from Basra to Erbil.")

st("texas", "Texas", "us", "Houston, Dallas, Arlington and Austin",
   "Texas has growing Iraqi and Arab communities in Houston, Dallas–Fort Worth, Arlington, Richardson and Austin. Many families resettled here after 2007 and now travel back with children who have never seen Iraq. We build a private trip around your dates — with an Arabic- or English-speaking guide.",
   [("Houston (IAH), Dallas–Fort Worth (DFW) → Baghdad (BGW)", f"One-stop connections via {HUBS}; both airports have long-haul flights to the Gulf and Istanbul (check current schedules)."),
    ("Austin (AUS), San Antonio (SAT), El Paso (ELP)", "Connect through Houston, Dallas or another hub.")],
   ["babylon", "shrines", "marshes"],
   "Coming in summer? Iraq is very hot from June to August. For touring, October to April is the best season — the 9-day tour from Basra to Erbil is perfect in spring.")

st("new-york", "New York", "us", "Brooklyn, Queens, Manhattan and Buffalo",
   "New York has long-established Arab communities — Bay Ridge in Brooklyn, Astoria and Steinway Street in Queens — and an Iraqi community that grew in Buffalo and upstate cities with refugee resettlement. From JFK you are one connection away from Baghdad.",
   [("New York JFK / Newark (EWR) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}. JFK has several daily nonstops to Istanbul, Doha and Dubai (check current schedules)."),
    ("Buffalo (BUF), Albany (ALB), Rochester (ROC)", "Connect through New York, Washington, Chicago or Toronto.")],
   ["babylon", "kadhimiya", "ur"],
   "Short on time? Our 7-day tour starts and ends at Baghdad International Airport — easy to fit between two weekends.")

st("new-jersey", "New Jersey", "us", "Paterson, Jersey City, Bayonne and Clifton",
   "New Jersey's Arab community is one of the most visible in the country — Paterson's South Main Street, Clifton, Jersey City and Bayonne — with Iraqi families across the state. Newark puts you one connection away from Iraq.",
   [("Newark (EWR) / New York JFK → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS} (check current schedules)."),
    ("Atlantic City (ACY), Trenton (TTN)", "Fly from Newark, JFK or Philadelphia.")],
   ["babylon", "shrines", "qishla"],
   "Travelling as a family with grandparents? We pace the days, arrange hotel rooms near each other and our guide speaks Arabic.")

st("arizona", "Arizona", "us", "Phoenix, Glendale, Peoria and Tucson",
   "Arizona has one of the newer Iraqi communities in the United States, centred on Phoenix, Glendale and Peoria, with families in Tucson too. Many came after 2007 and now go back to visit relatives — we add Babylon, Ur and the Marshes to that trip.",
   [("Phoenix (PHX) → Baghdad (BGW)", f"Usually two connections: via a US hub (Dallas, Chicago, New York, Los Angeles), then {HUBS}."),
    ("Tucson (TUS)", "Connect through Phoenix, Dallas or Los Angeles.")],
   ["babylon", "ur", "marshes"],
   "If you are visiting family in Baghdad, book only the days you need: same-day trips from Baghdad to Babylon, Samarra or Karbala and Najaf.")

st("virginia", "Virginia", "us", "Fairfax, Falls Church, Alexandria and Arlington",
   "Northern Virginia and the Washington, DC area are home to a large, well-established Arab community and many Iraqi families — in Fairfax County, Falls Church, Alexandria, Arlington and nearby Maryland. Dulles is one of the best-connected airports in the country for flights to Iraq.",
   [("Washington Dulles (IAD) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}; Dulles has nonstops to Istanbul, Doha and Dubai (check current schedules)."),
    ("Reagan National (DCA), Richmond (RIC), Norfolk (ORF)", "Connect through Dulles or another hub.")],
   ["babylon", "qishla", "hatra"],
   "Interested in history in depth? Ask for extra time at Babylon, Hatra and Nimrud — our guide explains each site on the spot.")

st("ohio", "Ohio", "us", "Toledo, Columbus, Cleveland and Dayton",
   "Ohio has one of the oldest Arab-American communities in the country in Toledo, plus Iraqi and Arab families in Columbus, Cleveland, Dayton and Cincinnati. Detroit is close, too, so many Ohio families share flights and trips with relatives in Michigan.",
   [("Columbus (CMH), Cleveland (CLE), Cincinnati (CVG) → Baghdad (BGW)", f"Connect through a US hub or fly from Detroit, Chicago or New York, then via {HUBS}."),
    ("Toledo (TOL), Dayton (DAY)", "Detroit (DTW) is often the most convenient airport.")],
   ["babylon", "kadhimiya", "marshes"],
   "Travelling with friends or relatives from Michigan? Join as one private group — the price per person stays the same.")

st("florida", "Florida", "us", "Jacksonville, Tampa, Orlando and Miami",
   "Florida's Arab community is spread across Jacksonville, Tampa Bay, Orlando and South Florida, with Iraqi families in each region. Miami and Orlando are well connected to Istanbul and the Gulf hubs.",
   [("Miami (MIA), Orlando (MCO), Tampa (TPA) → Baghdad (BGW)", f"One-stop or two-stop routes via {HUBS} (check current schedules)."),
    ("Jacksonville (JAX), Fort Lauderdale (FLL)", "Connect through Atlanta, New York, Miami or another hub.")],
   ["babylon", "basra", "marshes"],
   "Used to the Florida heat? Iraq's winter (November–March) is mild and sunny — the best time for Babylon, Ur and the Marshes.")

st("pennsylvania", "Pennsylvania", "us", "Philadelphia, Pittsburgh and Allentown",
   "Pennsylvania has Arab communities with long histories in Allentown and Pittsburgh, and Iraqi and Arab families in Philadelphia and its suburbs. Philadelphia, Newark and JFK all give one-stop options to Iraq.",
   [("Philadelphia (PHL) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via Istanbul or Doha, or through New York / Newark then via {HUBS}."),
    ("Pittsburgh (PIT), Allentown (ABE), Harrisburg (MDT)", "Connect through a US hub.")],
   ["babylon", "ur", "samarra"],
   "Want to see Samarra's spiral minaret? It is on day 5 of our 7-day tour and on our same-day trips from Baghdad.")

st("tennessee", "Tennessee", "us", "Nashville, Antioch and Memphis",
   "Nashville is home to the largest Kurdish community in the United States — 'Little Kurdistan' — along with Iraqi and Arab families across Middle Tennessee and Memphis. Many families fly into Erbil or Sulaymaniyah; we help you see the rest of Iraq too.",
   [("Nashville (BNA) → Erbil (EBL) / Baghdad (BGW)", f"Connect through a US hub (Chicago, New York, Washington, Atlanta) or Europe, then via {HUBS}."),
    ("Memphis (MEM), Knoxville (TYS)", "Connect through Atlanta, Chicago or another hub.")],
   ["mosul", "hatra", "babylon"],
   "Visiting family in Kurdistan? Our 9-day tour runs from Basra to Erbil, so you can stay on in the north after the tour ends.")

st("massachusetts", "Massachusetts", "us", "Boston, Worcester, Quincy and Lowell",
   "Massachusetts has Lebanese and Syrian communities that go back over a century, and Iraqi and Arab families across Greater Boston, Worcester and the Merrimack Valley. Boston Logan has nonstop flights to Istanbul, Doha and Dubai (check current schedules).",
   [("Boston (BOS) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}."),
    ("Worcester (ORH), Hartford (BDL), Providence (PVD)", "Connect through Boston, New York or another hub.")],
   ["babylon", "ur", "kadhimiya"],
   "Students and researchers: ask about extra time at Uruk, Ur and Babylon — the sites where writing, law and cities began.")

st("washington", "Washington", "us", "Seattle, Kent, SeaTac and Tacoma",
   "The Seattle area has a growing Iraqi community, especially in Kent, SeaTac, Renton and Tacoma, alongside Arab families across the Puget Sound region. Seattle-Tacoma has long-haul flights to the Gulf and Istanbul.",
   [("Seattle-Tacoma (SEA) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS} (check current schedules)."),
    ("Spokane (GEG), Portland (PDX)", "Connect through Seattle or another hub.")],
   ["babylon", "ur", "marshes"],
   "Long flight from the Pacific Northwest? Add our airport pickup in Baghdad and rest a night before the tour starts.")

st("new-mexico", "New Mexico", "us", "Albuquerque, Rio Rancho, Santa Fe and Las Cruces",
   "New Mexico has a small, close-knit Arab community and Iraqi families who settled in Albuquerque and Rio Rancho, with more in Santa Fe and Las Cruces. Many travel back to see relatives in Baghdad — we add Babylon, Ur and the Marshes to the trip, with a guide who speaks Arabic and English.",
   [("Albuquerque (ABQ) → Baghdad (BGW)", f"Usually two connections: via a US hub (Dallas, Houston, Chicago, Los Angeles), then {HUBS}."),
    ("Santa Fe (SAF), El Paso (ELP) for Las Cruces", "Connect through Dallas, Denver or Phoenix.")],
   ["babylon", "ur", "marshes"],
   "Long journey from the Southwest? Add our Baghdad airport pickup and a rest night before the tour starts.")

st("las-vegas", "Las Vegas", "us", "Las Vegas, Henderson and North Las Vegas",
   "Las Vegas and Henderson have a growing Arab community and Iraqi families who have moved to Southern Nevada in recent years. From Harry Reid Airport you are two short connections away from Baghdad — we take care of everything from the moment you land.",
   [("Las Vegas (LAS) → Baghdad (BGW) / Erbil (EBL)", f"Connect through Los Angeles, Dallas, Chicago or New York, then via {HUBS} (check current schedules)."),
    ("Reno (RNO)", "Connect through Las Vegas, San Francisco or another hub.")],
   ["babylon", "kadhimiya", "samarra"],
   "Prefer a short trip? Our 7-day tour starts and ends at Baghdad International Airport, and our same-day trips from Baghdad fit around a family visit.")

# Canada
st("ontario", "Ontario", "ca", "Toronto, Mississauga, Ottawa, Windsor and London",
   "Ontario is home to Canada's largest Iraqi and Arab communities — in Mississauga, Toronto, Brampton, Ottawa, Windsor (next to Detroit), London and Hamilton. Many families travel back every year; we help you combine the family visit with Babylon, Ur and the Marshes.",
   [("Toronto Pearson (YYZ) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}; Toronto has nonstops to Istanbul, Doha and Dubai (check current schedules)."),
    ("Ottawa (YOW), Windsor (YQG), London (YXU), Hamilton (YHM)", "Connect through Toronto or Montreal — Windsor families often fly from Detroit (DTW).")],
   ["babylon", "kadhimiya", "marshes"],
   "Bring US dollars: Canadian dollars are hard to exchange in Iraq.")

st("quebec", "Quebec", "ca", "Montreal, Laval and Quebec City",
   "Montreal and Laval have large Arab communities, with many Iraqi, Lebanese and Syrian families, and Quebec City has a growing community too. Many of our guests from Quebec speak Arabic and French — our guide works in Arabic or English.",
   [("Montreal (YUL) → Baghdad (BGW) / Erbil (EBL)", f"One-stop connections via {HUBS}, or via Paris or another European hub (check current schedules)."),
    ("Quebec City (YQB)", "Connect through Montreal or Toronto.")],
   ["babylon", "ur", "samarra"],
   "Prefer reading in French? Our full programme is also available in French on this site.")

st("alberta", "Alberta", "ca", "Calgary and Edmonton",
   "Alberta has active Iraqi and Arab communities in Calgary and Edmonton — Edmonton's Lebanese community is one of the oldest in Western Canada. Both airports connect to Iraq with one or two stops.",
   [("Calgary (YYC), Edmonton (YEG) → Baghdad (BGW) / Erbil (EBL)", f"Connect through Toronto, a US hub or Europe, then via {HUBS}.")],
   ["babylon", "mosul", "marshes"],
   "Used to Alberta winters? Iraq's winter is mild and sunny — November to March is ideal for touring.")

st("british-columbia", "British Columbia", "ca", "Vancouver, Surrey, Burnaby and Coquitlam",
   "Metro Vancouver has a growing Iraqi and Arab community across Surrey, Burnaby, Coquitlam and North Vancouver. Vancouver has long-haul flights to Asia and Europe and connects easily to Istanbul and the Gulf hubs.",
   [("Vancouver (YVR) → Baghdad (BGW) / Erbil (EBL)", f"One or two stops via {HUBS}, or via Europe (check current schedules)."),
    ("Victoria (YYJ), Kelowna (YLW)", "Connect through Vancouver or Calgary.")],
   ["babylon", "ur", "kadhimiya"],
   "The journey from the West Coast is long: add our Baghdad airport pickup and a rest day before the tour.")

IMG = {"shrines": ("wadi-al-salam", "Karbala & Najaf", "The shrines of Imam Hussein and al-Abbas in Karbala and Imam Ali in Najaf, with the Great Mosque of Kufa."),
       "babylon": ("babylon-ishtar-gate", "Babylon", "The Ishtar Gate, the Processional Way and the Lion of Babylon."),
       "marshes": ("marshes-mashoof", "The Marshes", "A mashoof boat ride among reed houses, water buffalo and a masgouf lunch."),
       "kadhimiya": ("kadhimiya-shrine-night", "Baghdad", "Al-Kadhimiya, Mutanabbi Street, the Qishla and the Abbasid Palace."),
       "samarra": ("samarra-malwiya", "Samarra", "The spiral Malwiya minaret and the golden dome of al-Askari."),
       "qishla": ("qishla-clock-tower-view", "Old Baghdad", "The Qishla clock tower, Mutanabbi Street and tea at Shabandar Café."),
       "mosul": ("mosul-al-hadba-nuri", "Mosul & Nineveh", "Old Mosul and the al-Hadba minaret, Assyrian Nimrud and Hatra."),
       "hatra": ("hatra", "Hatra", "The temples of Hatra, a UNESCO World Heritage city of the desert."),
       "basra": ("basra-shatt-al-arab-sunset", "Basra", "Sunset on the Shatt al-Arab and the shanasheel houses of old Basra."),
       "ur": ("ur-ziggurat", "Ur & Uruk", "The ziggurat of Ur and Uruk, where writing began.")}

COUNTRY = {
 "us": dict(src="en/iraq-tours-from-usa/index.html", parent="iraq-tours-from-usa", pname="the USA", pass_="US",
            advice='<strong>US Department of State travel advice.</strong> Please read the latest official advice on <a href="https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/iraq-travel-advisory.html" target="_blank" rel="noopener">travel.state.gov — Iraq travel advisory</a> before you decide, and confirm that your travel insurance covers the destination.',
            money="Bring clean, recent US dollar notes — they are accepted widely; card acceptance is limited outside hotels.",
            by="Iraq tours by US state"),
 "ca": dict(src="en/iraq-tours-from-canada/index.html", parent="iraq-tours-from-canada", pname="Canada", pass_="Canadian",
            advice='<strong>Government of Canada travel advice.</strong> Please read the latest official advice on <a href="https://travel.gc.ca/destinations/iraq" target="_blank" rel="noopener">travel.gc.ca — Iraq travel advice</a> before you decide, and confirm that your travel insurance covers the destination.',
            money="Budget in US dollars — Canadian dollars are hard to exchange in Iraq; card acceptance is limited outside hotels.",
            by="Iraq tours by province"),
}

PRICES_EN = """      <div class="market-card" id="prices">
        <h3>Public prices &amp; payment</h3>
        <ul>
          <li><strong>7-day tour:</strong> US$2,500 per person in a double room</li>
          <li><strong>9-day tour:</strong> US$3,400 per person in a double room</li>
          <li>Single-room supplement on private tours: US$540</li>
          <li>Infants (1 month–2 years) travel free</li>
        </ul>
        <p>Free cancellation. International flights, the Iraqi visa, lunches and dinners are not included. Prefer a shorter trip? See our <a href="#day-trips">same-day trips from Baghdad</a>.</p>
      </div>"""


def state_links(country, current=None, lang="en"):
    items = "".join(
        f'<li><a href="/en/{v["slug"]}/">{esc(v["name"])}</a></li>' if k != current else f'<li><strong>{esc(v["name"])}</strong></li>'
        for k, v in S.items() if v["country"] == country)
    title = {"en": COUNTRY[country]["by"], "es": "Viajes a Irak por estado (en inglés)", "fr": "Voyages en Irak par province (en anglais)"}[lang]
    return (f'    <div class="market-card market-links" style="margin-top:16px" id="by-region"><h3>{esc(title)}</h3>'
            f'<ul class="mkt-links">{items}</ul></div>\n')


LINKS_CSS = '<style id="mkt-links-css">.mkt-links{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.mkt-links li a,.mkt-links li strong{display:inline-block;padding:6px 12px;border:1px solid rgba(27,42,71,.18);border-radius:20px;font-size:14px;text-decoration:none;color:var(--navy,#1B2A47);background:#fff}.mkt-links li strong{background:var(--gold,#C9A96A);border-color:var(--gold,#C9A96A)}</style>'


def state_panel(key):
    v, c = S[key], COUNTRY[S[key]["country"]]
    fl = "".join(f"<li><strong>{esc(a)}:</strong> {esc(b)}</li>" for a, b in v["flights"])
    hl = "".join(f'<div class="hl"><div class="ph" style="background-image:url(\'/img/{IMG[i][0]}.webp\')" role="img" aria-label="{esc(IMG[i][1])}"></div>'
                 f'<div class="bd"><h3>{esc(IMG[i][1])}</h3><p>{esc(IMG[i][2])}</p></div></div>' for i in v["hl"])
    n = esc(v["name"])
    return f"""<section class="block in market-panel" id="for-{key}" aria-labelledby="{key}-heading">
    <div class="sec-head">
      <span class="eyebrow">Travellers from {n}</span>
      <h2 class="disp" id="{key}-heading">Iraq tours from {n}</h2>
      <p>{esc(v["community"])}</p>
    </div>
    <div class="market-grid">
      <div class="market-card" id="flights">
        <h3>Flights from {n} to Iraq</h3>
        <p>International flights are <strong>not</strong> included in the tour price. There is no nonstop from {"the United States" if v["country"] == "us" else "Canada"} to Iraq; common options:</p>
        <ul>{fl}</ul>
        <p class="market-note">We do not quote airfares — prices move daily. Pickup is arranged at Baghdad, Basra or Erbil airport depending on the programme. {esc(c["money"])}</p>
      </div>
      <div class="market-card" id="visa">
        <h3>Visa: {c["pass_"]} or Iraqi passport</h3>
        <p><strong>Iraqi passport holders</strong> (including dual citizens) can travel on their valid Iraqi passport and need no visa.</p>
        <p><strong>{c["pass_"]} passport only:</strong> apply online through the official Iraqi e-visa portal before you travel — the fee and validity are shown when you apply.</p>
        <ul>
          <li><a href="https://eservice.evisa.iq" target="_blank" rel="noopener">eservice.evisa.iq</a> — application portal</li>
          <li><a href="https://evisa.iq/en" target="_blank" rel="noopener">evisa.iq</a> — information and instructions</li>
        </ul>
        <div class="market-info"><p><strong>Please reconfirm before you travel.</strong> Rules can change. Passport validity of at least six months from arrival is typically required.</p></div>
      </div>
    </div>
    <div class="market-grid" style="margin-top:16px">
      <div class="market-card" id="family">
        <h3>Visiting family in Iraq?</h3>
        <p>Combine your family visit with a few days of touring. We can meet you at <a href="#airport-transfer">Baghdad International Airport</a>, take you to your hotel or your relatives' home, and plan <a href="#day-trips">same-day trips</a> to Babylon, Samarra, Karbala and Najaf or the Marshes. Your guide speaks Arabic and English — comfortable for parents and grandparents, and for children raised abroad.</p>
        <p>{esc(v["tip"])}</p>
      </div>
{PRICES_EN}
    </div>
    <div class="market-card" style="margin-top:16px" id="highlights">
      <h3>What you will see</h3>
      <div class="market-hl">{hl}</div>
    </div>
{state_links(v["country"], key)}    <div class="market-info" id="travel-advice" style="margin-top:16px"><p>{c["advice"]} We run private programmes with local guides and do not pressure anyone to travel against their government’s advice. See also: <a href="/en/{c["parent"]}/">Iraq tours from {c["pname"]}</a>.</p></div>
  </section>"""


def state_meta(key):
    v = S[key]
    n, ab = v["name"], v["cities"].split(",")[0]
    t = f"Iraq Tours from {n}: Flights, Visa & Family Visits | Fable Tour"
    d = (f"Iraq tours for travellers from {n} — {v['cities']}. Flights, e-visa or Iraqi passport, family visits, "
         f"Babylon, Ur and the Marshes. Private 7 & 9-day tours from $2,500.")
    kw = (f"Iraq tours from {n}, {ab} to Baghdad, Iraq trip from {n}, Iraqi community {n}, Arab community {n}, "
          f"visit Iraq family, Baghdad tour, Babylon tour, Fable Tour")
    lead = f"For travellers from {v['cities']}: flights, visa and family visits, with Babylon, Ur and the Marshes. Two programmes with 5-star hotels and a private guide."
    return dict(title=t, desc=d, kw=kw, h1=f"Iraq tours from {n}", eyebrow=f"Travellers from {n}", lead=lead)


# ------------------------------------------------------------------ Spanish USA / French Canada
ES_PANEL = """<section class="block in market-panel" id="for-usa" aria-labelledby="usa-heading">
    <div class="sec-head">
      <span class="eyebrow">Viajeros desde Estados Unidos</span>
      <h2 class="disp" id="usa-heading">Viajes a Irak desde Estados Unidos</h2>
      <p>Visado electrónico para pasaportes estadounidenses, vuelos desde Nueva York, Washington, Chicago, Houston, Miami y Los Ángeles, Babilonia, Ur y las marismas — con Fable Tour, operador con sede en Bagdad. Respondemos por WhatsApp en minutos en horario laboral y por correo en menos de 6 horas.</p>
    </div>
    <div class="market-grid">
      <div class="market-card" id="visa">
        <h3>Visado de Irak para pasaportes de EE. UU.</h3>
        <p>Los ciudadanos estadounidenses necesitan un visado iraquí antes de viajar y lo solicitan en línea en el portal oficial de visado electrónico de Irak. El visado a la llegada para visitas ordinarias ya no está disponible. La tasa y la validez aparecen en el portal al solicitarlo; solicítelo unos días antes de salir y confirme siempre las normas vigentes.</p>
        <ul>
          <li><a href="https://eservice.evisa.iq" target="_blank" rel="noopener">eservice.evisa.iq</a> — portal de solicitud</li>
          <li><a href="https://evisa.iq/en" target="_blank" rel="noopener">evisa.iq</a> — información e instrucciones</li>
        </ul>
        <div class="market-info">
          <p><strong>Confírmelo antes de viajar.</strong> Las normas pueden cambiar. Imprima el visado electrónico / código QR para el control fronterizo. Lleve billete de regreso o de continuación; normalmente se exige un pasaporte con validez mínima de seis meses desde la llegada.</p>
          <p>Si tiene otra nacionalidad que no puede tramitar el visado en línea, Fable Tour puede obtenerlo por <strong>300 USD</strong> al reservar un tour completo.</p>
        </div>
      </div>
      <div class="market-card" id="flights">
        <h3>Vuelos desde Estados Unidos</h3>
        <p>Los vuelos internacionales <strong>no</strong> están incluidos en el precio. No hay vuelos directos de EE. UU. a Irak; las opciones habituales con una escala son:</p>
        <ul><li><strong>Nueva York (JFK), Washington (IAD), Chicago (ORD) → Bagdad (BGW) / Erbil (EBL):</strong> con escala en Estambul (Turkish Airlines), Doha (Qatar Airways), Dubái (Emirates) o Amán (Royal Jordanian).</li><li><strong>Miami (MIA), Houston (IAH), Dallas (DFW), Los Ángeles (LAX):</strong> normalmente vía Estambul, Doha, Dubái o Amán.</li></ul>
        <p class="market-note">No publicamos tarifas aéreas: cambian a diario. La recogida se organiza en los aeropuertos de Bagdad, Basora o Erbil según el programa. Lleve billetes de dólar estadounidense limpios y recientes: se aceptan en todas partes; las tarjetas se aceptan poco fuera de los hoteles.</p>
      </div>
    </div>
    <div class="market-grid" style="margin-top:16px">
      <div class="market-card" id="prices">
        <h3>Precios públicos y pago</h3>
        <ul>
          <li><strong>Tour de 7 días:</strong> 2.500 USD por persona en habitación doble</li>
          <li><strong>Tour de 9 días:</strong> 3.400 USD por persona en habitación doble</li>
          <li>Suplemento de habitación individual en tours privados: 540 USD</li>
          <li>Bebés (1 mes–2 años) viajan gratis</li>
        </ul>
        <p>Cancelación gratuita. Si podemos tramitar su visado electrónico en línea, paga el tour a su llegada a Irak. Si obtenemos el visado por usted (300 USD), la mitad del precio se paga por adelantado y el resto a la llegada. No incluye vuelos internacionales, el visado iraquí, almuerzos ni cenas.</p>
      </div>
      <div class="market-card" id="guide-lang">
        <h3>Idiomas del guía</h3>
        <p>Su guía profesional habla inglés, ruso o árabe. Para viajeros hispanohablantes de Estados Unidos trabajamos en inglés; si viaja con familia de origen árabe, el guía también puede explicar en árabe.</p>
      </div>
    </div>
    <div class="market-card" style="margin-top:16px" id="highlights">
      <h3>Por qué los viajeros de Estados Unidos eligen Irak</h3>
      <p>Vienen por el corazón arqueológico de Mesopotamia — Babilonia, Ur y las marismas vivas — y por la cultura viva de Bagdad, con un guía privado desde la llegada hasta la salida.</p>
      <div class="market-hl">
        <div class="hl"><div class="ph" style="background-image:url('/img/babylon-ishtar-gate.webp')" role="img" aria-label="Babilonia"></div><div class="bd"><h3>Babilonia y Ur</h3><p>La Puerta de Ishtar, el zigurat de Ur y las ciudades de la antigua Sumeria en ambos programas.</p></div></div>
        <div class="hl"><div class="ph" style="background-image:url('/img/marshes-mashoof.webp')" role="img" aria-label="Marismas"></div><div class="bd"><h3>Las marismas</h3><p>Paseos en barca mashoof y la hospitalidad del mudhif en las marismas de Mesopotamia.</p></div></div>
        <div class="hl"><div class="ph" style="background-image:url('/img/kadhimiya-shrine-night.webp')" role="img" aria-label="Bagdad"></div><div class="bd"><h3>Bagdad</h3><p>La calle Mutanabbi, la Qishla, el Palacio Abasí y el santuario de Al-Kadhimiya.</p></div></div>
      </div>
    </div>
{LINKS}    <div class="market-info" id="travel-advice" style="margin-top:16px"><p><strong>Recomendaciones del Departamento de Estado de EE. UU.</strong> Lea los avisos oficiales más recientes en <a href="https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories/iraq-travel-advisory.html" target="_blank" rel="noopener">travel.state.gov — aviso de viaje a Irak</a> antes de decidir y confirme que su seguro de viaje cubre el destino. Organizamos programas privados con guías locales y no presionamos a nadie para viajar en contra de las recomendaciones de su gobierno.</p></div>
  </section>"""

FR_PANEL = """<section class="block in market-panel" id="for-canada" aria-labelledby="canada-heading">
    <div class="sec-head">
      <span class="eyebrow">Voyageurs du Canada</span>
      <h2 class="disp" id="canada-heading">Voyages en Irak depuis le Canada</h2>
      <p>Visa électronique pour passeports canadiens, vols depuis Montréal, Toronto, Ottawa et Vancouver, Babylone, Ur et les marais — avec Fable Tour, agence réceptive basée à Bagdad. Nous répondons sur WhatsApp en quelques minutes aux heures de bureau, et par courriel en moins de 6 heures.</p>
    </div>
    <div class="market-grid">
      <div class="market-card" id="visa">
        <h3>Visa pour l'Irak avec un passeport canadien</h3>
        <p>Les citoyens canadiens doivent obtenir un visa irakien avant le départ, en ligne sur le portail officiel de visa électronique de l'Irak. Le visa à l'arrivée pour les visites ordinaires n'est plus disponible. Les frais et la durée de validité sont indiqués sur le portail lors de la demande — faites-la quelques jours avant le départ et vérifiez toujours les règles en vigueur.</p>
        <ul>
          <li><a href="https://eservice.evisa.iq" target="_blank" rel="noopener">eservice.evisa.iq</a> — portail de demande</li>
          <li><a href="https://evisa.iq/en" target="_blank" rel="noopener">evisa.iq</a> — informations et instructions</li>
        </ul>
        <div class="market-info">
          <p><strong>Vérifiez avant de partir.</strong> Les règles peuvent changer. Imprimez le visa électronique / code QR pour le contrôle frontalier. Ayez un billet de retour ou de continuation ; un passeport valide au moins six mois après l'arrivée est généralement exigé.</p>
          <p>Si vous avez une autre nationalité qui ne permet pas la demande en ligne, Fable Tour peut obtenir le visa pour <strong>300 $ US</strong> lorsque vous réservez un circuit complet.</p>
          <p>Vous êtes d'origine irakienne et avez un passeport irakien valide ? Vous pouvez voyager avec, sans visa.</p>
        </div>
      </div>
      <div class="market-card" id="flights">
        <h3>Vols depuis Montréal, Toronto et Vancouver</h3>
        <p>Les vols internationaux ne sont <strong>pas</strong> inclus dans le prix. Il n'y a pas de vol direct du Canada vers l'Irak ; options courantes avec une escale :</p>
        <ul><li><strong>Montréal (YUL) / Toronto (YYZ) → Bagdad (BGW) / Erbil (EBL) :</strong> via Istanbul (Turkish Airlines), Doha (Qatar Airways), Dubaï (Emirates), Amman (Royal Jordanian) ou Paris.</li><li><strong>Ottawa (YOW), Québec (YQB), Vancouver (YVR), Calgary (YYC) :</strong> correspondance via Montréal, Toronto ou un hub européen.</li></ul>
        <p class="market-note">Nous ne publions pas de tarifs aériens — ils changent chaque jour. L'accueil se fait aux aéroports de Bagdad, Bassora ou Erbil selon le programme. Prévoyez des dollars américains — les dollars canadiens sont difficiles à changer en Irak ; la carte bancaire est peu acceptée hors des hôtels.</p>
      </div>
    </div>
    <div class="market-grid" style="margin-top:16px">
      <div class="market-card" id="prices">
        <h3>Prix publics et paiement</h3>
        <ul>
          <li><strong>Circuit de 7 jours :</strong> 2 500 $ US par personne en chambre double</li>
          <li><strong>Circuit de 9 jours :</strong> 3 400 $ US par personne en chambre double</li>
          <li>Supplément chambre individuelle (circuits privés) : 540 $ US</li>
          <li>Bébés (1 mois–2 ans) : gratuit</li>
        </ul>
        <p>Annulation gratuite. Si vous pouvez obtenir le visa électronique en ligne, vous payez le circuit à votre arrivée en Irak. Si nous obtenons le visa pour vous (300 $ US), la moitié du prix est payée d'avance et le reste à l'arrivée. Vols internationaux, visa irakien, déjeuners et dîners non inclus.</p>
      </div>
      <div class="market-card" id="guide-lang">
        <h3>Langues du guide</h3>
        <p>Votre guide professionnel parle anglais, russe ou arabe. Pour les voyageurs du Québec, nous travaillons en anglais ou en arabe — idéal pour les familles d'origine arabe.</p>
      </div>
    </div>
    <div class="market-card" style="margin-top:16px" id="highlights">
      <h3>Pourquoi les Canadiens choisissent l'Irak</h3>
      <p>Pour le cœur archéologique de la Mésopotamie — Babylone, Ur et les marais vivants — et pour la culture de Bagdad, avec un guide privé de l'arrivée au départ.</p>
      <div class="market-hl">
        <div class="hl"><div class="ph" style="background-image:url('/img/babylon-ishtar-gate.webp')" role="img" aria-label="Babylone"></div><div class="bd"><h3>Babylone et Ur</h3><p>La porte d'Ishtar, la ziggourat d'Ur et les cités de l'ancienne Sumer dans les deux programmes.</p></div></div>
        <div class="hl"><div class="ph" style="background-image:url('/img/marshes-mashoof.webp')" role="img" aria-label="Marais"></div><div class="bd"><h3>Les marais</h3><p>Promenade en barque mashoof et hospitalité du mudhif dans les marais de Mésopotamie.</p></div></div>
        <div class="hl"><div class="ph" style="background-image:url('/img/samarra-malwiya.webp')" role="img" aria-label="Samarra"></div><div class="bd"><h3>Samarra et Bagdad</h3><p>Le minaret en spirale de Samarra, la rue Mutanabbi et la Qishla à Bagdad.</p></div></div>
      </div>
    </div>
{LINKS}    <div class="market-info" id="travel-advice" style="margin-top:16px"><p><strong>Conseils aux voyageurs du gouvernement du Canada.</strong> Lisez les conseils officiels les plus récents sur <a href="https://voyage.gc.ca/destinations/irak" target="_blank" rel="noopener">voyage.gc.ca — Irak</a> avant de décider, et vérifiez que votre assurance voyage couvre la destination. Nous organisons des programmes privés avec des guides locaux et ne poussons personne à voyager contre l'avis de son gouvernement.</p></div>
  </section>"""

LOCAL = {
 "es": dict(key="usa", en="iraq-tours-from-usa", panel=ES_PANEL, country="us",
            title="Viajes a Irak desde Estados Unidos: visado y vuelos | Fable Tour",
            desc="Viajes a Irak desde Estados Unidos: visado electrónico para pasaportes de EE. UU., vuelos desde Nueva York, Miami, Houston y Los Ángeles, Babilonia, Ur y las marismas. Tours privados de 7 y 9 días desde 2.500 USD.",
            kw="viajes a Irak desde Estados Unidos, tour Irak desde EE. UU., visado Irak ciudadanos estadounidenses, vuelos Nueva York Bagdad, Miami Bagdad, Babilonia, Fable Tour",
            eyebrow="Viajeros desde Estados Unidos", h1="Viajes a Irak desde Estados Unidos",
            lead="Visado electrónico, vuelos desde Nueva York, Miami, Houston y Los Ángeles, Babilonia, Ur y las marismas. Dos programas con hoteles de 5★ y guía privado.",
            crumb="Viajes a Irak desde Estados Unidos"),
 "fr": dict(key="canada", en="iraq-tours-from-canada", panel=FR_PANEL, country="ca",
            title="Voyage en Irak depuis le Canada : visa et vols de Montréal | Fable Tour",
            desc="Voyages en Irak depuis le Canada : visa électronique pour passeports canadiens, vols depuis Montréal, Toronto et Vancouver, Babylone, Ur et les marais. Circuits privés de 7 et 9 jours dès 2 500 $ US.",
            kw="voyage Irak depuis le Canada, circuit Irak Montréal, visa Irak Canadiens, vol Montréal Bagdad, voyage Irak Québec, Babylone, Fable Tour",
            eyebrow="Voyageurs du Canada", h1="Voyages en Irak depuis le Canada",
            lead="Visa électronique, vols depuis Montréal, Toronto et Vancouver, Babylone, Ur et les marais. Deux programmes en hôtels 5★ avec guide privé.",
            crumb="Voyages en Irak depuis le Canada"),
}


# ------------------------------------------------------------------ page surgery helpers
def set_meta(s, u, m, alts):
    s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", s)
    links = "".join(f'<link rel="alternate" hreflang="{l}" href="{x}">\n' for l, x in alts)
    s = re.sub(r'<link rel="canonical" href="[^"]*">\n?', f'<link rel="canonical" href="{u}">\n' + links, s, count=1)
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(m['title'])}</title>", s, count=1, flags=re.S)
    for p in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(rf'(<meta {p} content=")[^"]*"', lambda x: x.group(1) + esc(m["desc"]) + '"', s)
    for p in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(rf'(<meta {p} content=")[^"]*"', lambda x: x.group(1) + esc(m["title"]) + '"', s)
    s = re.sub(r'(<meta name="keywords" content=")[^"]*"', lambda x: x.group(1) + esc(m["kw"]) + '"', s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*"', lambda x: x.group(1) + u + '"', s)
    s = re.sub(r'(<span class="eyebrow" data-i="eyebrow">).*?(</span>)', lambda x: x.group(1) + esc(m["eyebrow"]) + x.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<h1 class="disp" data-i="h1">).*?(</h1>)', lambda x: x.group(1) + esc(m["h1"]) + x.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p data-i="lead">).*?(</p>)', lambda x: x.group(1) + esc(m["lead"]) + x.group(2), s, count=1, flags=re.S)
    k = s.index("const T = ")
    head, tail = s[:k], s[k:]
    for key_ in ("title", "eyebrow", "h1", "lead"):
        tail = re.sub(r'("%s": )"(?:\\.|[^"\\])*"' % key_, lambda x: x.group(1) + json.dumps(m[key_], ensure_ascii=False), tail, count=1)
    return head + tail


def set_ld(s, u, m, lang, parents):
    def ld(x):
        try:
            data = json.loads(x.group(1))
        except Exception:
            return x.group(0)
        for n in data.get("@graph", [data]):
            if n.get("@type") == "WebPage":
                n.update({"@id": u + "#webpage", "url": u, "name": m["title"], "description": m["desc"], "inLanguage": lang,
                          "dateModified": TODAY, "breadcrumb": {"@id": u + "#breadcrumb"}})
            if n.get("@type") == "BreadcrumbList":
                n["@id"] = u + "#breadcrumb"
                items = [{"@type": "ListItem", "position": 1, "name": "Fable Tour", "item": BASE + "/"}]
                for name, href in parents + [(m.get("crumb", m["h1"]), u)]:
                    items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": href})
                n["itemListElement"] = items
            if n.get("@type") == "ItemList" and str(n.get("@id", "")).endswith("#tours"):
                n["@id"] = u + "#tours"
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', ld, s, flags=re.S)


def put_panel(s, panel):
    if 'class="block in market-panel"' in s:
        return re.sub(r'<section class="block in market-panel".*?</section>', lambda _: panel, s, count=1, flags=re.S)
    hero_end = s.index("</section>", s.index('data-i="h1"')) + len("</section>")
    return s[:hero_end] + "\n  " + panel + "\n" + s[hero_end:]


def add_css(s, css_block, ident):
    if f'id="{ident}"' not in s:
        s = s.replace("</head>", css_block + "\n</head>", 1)
    return s


def url(path):
    return f"{BASE}/{path}/"


# ------------------------------------------------------------------ build
def run():
    usa_src = (ROOT / COUNTRY["us"]["src"]).read_text()
    market_css = re.search(r'<style id="market-css">.*?</style>', usa_src, re.S).group(0)
    sm_urls = []

    # state / province pages (English)
    for key, v in S.items():
        c = COUNTRY[v["country"]]
        src = (ROOT / c["src"]).read_text()
        u = url(f"en/{v['slug']}")
        m = state_meta(key)
        s = set_meta(src, u, m, [("en", u), ("x-default", u)])
        s = put_panel(s, state_panel(key))
        s = set_ld(s, u, m, "en", [(f"Iraq tours from {c['pname']}", url(f"en/{c['parent']}"))])
        s = add_css(s, LINKS_CSS, "mkt-links-css")
        out = ROOT / "en" / v["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s)
        sm_urls.append((u, [("en", u), ("x-default", u)]))

    # Spanish USA / French Canada (copies of the local homepage) + English pages' hreflang & links card
    for lang, L in LOCAL.items():
        u_loc, u_en = url(f"{lang}/{L['en']}"), url(f"en/{L['en']}")
        alts = [("en", u_en), (lang, u_loc), ("x-default", u_en)]
        s = absolutize((ROOT / lang / "index.html").read_text(), lang)
        s = set_meta(s, u_loc, L, alts)
        s = re.sub(r'\s*<div class="(?:mkt|[a-z]+)-banner">.*?</div>', "", s, flags=re.S)
        s = put_panel(s, L["panel"].replace("{LINKS}", state_links(L["country"], lang=lang)))
        s = set_ld(s, u_loc, L, lang, [])
        s = add_css(s, market_css, "market-css")
        s = add_css(s, LINKS_CSS, "mkt-links-css")
        out = ROOT / lang / L["en"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(s)
        sm_urls.append((u_loc, alts))

        f = ROOT / "en" / L["en"] / "index.html"
        e = f.read_text()
        e = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", e)
        e = re.sub(r'(<link rel="canonical" href="[^"]*">\n?)', lambda x: x.group(1) + "".join(
            f'<link rel="alternate" hreflang="{l}" href="{h}">\n' for l, h in alts), e, count=1)
        e = re.sub(r'\s*<div class="market-card market-links".*?</ul></div>\n?', "\n", e, flags=re.S)
        e = e.replace('    <div class="market-info" id="travel-advice"', state_links(L["country"]) + '    <div class="market-info" id="travel-advice"', 1)
        e = add_css(e, LINKS_CSS, "mkt-links-css")
        f.write_text(e)
        sm_urls.append((u_en, alts))

    # sitemap
    sm = ROOT / "sitemap.xml"
    t = sm.read_text()
    add = ""
    for u, pair in sm_urls:
        t = re.sub(r"  <url>\n    <loc>" + re.escape(u) + r"</loc>.*?</url>\n", "", t, flags=re.S)
        links = "".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{x}"/>\n' for l, x in pair)
        add += (f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n"
                f"    <priority>0.8</priority>\n{links}  </url>\n")
    sm.write_text(t.replace("</urlset>", add + "</urlset>"))
    print("built", len(S), "state/province pages + es/fr country pages;", len(sm_urls), "sitemap entries")


if __name__ == "__main__":
    run()
