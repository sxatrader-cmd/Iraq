# Daily multilingual blog — instructions

Site: https://iraq.fabletour.com — 30 languages. Every day ONE place in Iraq gets ONE article in EVERY language.
Four scheduled runs share the work; each run handles one language group (see `groups` in `_blog/plan.json`):
- Group A (first run of the day): en, ar, ru, de, fr, it
- Group B: es, el, cs, pl, tr, fa
- Group C: zh, ja, ms, id, th, hi, ur, ta, ko (Korean)
- Group D: fi, sv, da, no, sk, hr, ro, nl, ka (Finnish, Swedish, Danish, Norwegian Bokmål, Slovak, Croatian, Romanian, Dutch, Georgian)

Blog URLs: Arabic → `/blog/`, every other language L → `/L/blog/`. Sources live in `_blog/L/`.

## 1. Pick today's topic (Baghdad date, YYYY-MM-DD)
Open `_blog/plan.json` → `queue`.
- If an item has `"date"` == today → that is today's topic.
- Otherwise (normally only group A): take the first item with `"date": null`, set its `"date"` to today.
- TOPIC RULE (Saif's instruction): write ONLY about places, history and stories connected to the cities and sites in the two tour programmes — Baghdad (Kadhimiya, Mutanabbi St, Qishla, Mustansiriya, Aqar Quf), Babylon & Borsippa, Karbala, Kufa, Najaf, Uruk, Basra & Qurna, the Marshes, Ur, Samarra, Mosul & Nineveh, Nimrud, Hatra, Mar Mattai, Erbil. Topics can be a site, or a person/story tied to it (e.g. Najaf → biography of Imam Ali, stories from his life, his companions; Kufa → the Great Mosque, Muslim ibn Aqil; Karbala → Imam Hussein, al-Abbas, the companions of Hussein). If the queue runs out, add new topics of this kind only, rotating between cities, never places outside the programmes.
- The item's `title` is an English working title and `category_en` the category; translate the category consistently per language.
- Write only the languages of YOUR group that are not yet in the item's `langs_done`.
- If an earlier day's item still has languages of your group missing (a run failed), do those too after today's, max 3 extra articles.

## 2. Research once
If another language of this topic already exists (check `langs_done`; the files are `_blog/<lang>/posts/<slug>.html`), read it first and use it as the factual base. Otherwise research with web search (2–5 searches). Only write facts you can support. Never invent prices, opening hours or ticket costs.

## 3. Write each article — native, not a word-for-word translation
For each language L:
- 1,000–1,500 words (CJK incl. Korean: 2,000–3,000 characters; Thai similar length) of natural, fluent text for travellers from that country. Adapt the hook to the reader (Italian/Romanian: Verdi's Nabucco for Babylon; German: the Ishtar Gate in Berlin's Pergamon Museum; Malay/Indonesian/Persian/Arabic/Turkish/Urdu/Hindi/Tamil readers: religious-heritage (ziyarat) visitors are common — Urdu: use customary honorifics (ؑ after the Imams, ؐ/ﷺ after the Prophet); Hindi/Tamil: plain respectful wording; Chinese/Japanese/Korean: practical tone, clear structure. Korean (ko): South Korea currently bans its citizens from travelling to Iraq (MOFA travel-ban list), so never address the reader as a traveller from Korea or suggest booking from Korea; write cultural/historical guides for Korean speakers).
- Do local keyword thinking in L: the main keyword as people in that country search it (e.g. de "Babylon Irak besichtigen", fr "visiter Babylone", ru "Вавилон Ирак экскурсия", ja "バビロン遺跡 行き方", ko "바빌론 유적 이라크 여행", fi "Babylon Irak nähtävyydet", sv "besöka Babylon Irak", da "besøge Babylon Irak", no "besøke Babylon Irak", sk "Babylon Irak návšteva", hr "posjet Babilonu Irak", ro "vizită Babilon Irak", nl "Babylon Irak bezoeken"). Use it in title, h1, first paragraph, one h2 and description — naturally.
- Body fragment → `_blog/L/posts/<slug>.html`:
  - Starts with `<p class="lead">…</p>`; then 5–8 `<h2>` sections, `<h3>` sub-points, one `<ul>` of practical tips, optional `<blockquote>` with a first-person note from the guide Saif.
  - Sections like: where it is / history / what to see / how to get there (from Baghdad or nearest city) / best time to visit / practical tips / the place in an Iraq trip.
  - Internal links: 1–3 to earlier articles in the SAME language (`/L/blog/<slug>/`, Arabic `/blog/<slug>/`), and to the tours: `/L/#tour-7-days` or `/L/#tour-9-days` (Arabic: `/#tour-7-days`).
  - Do NOT include H1, facts box, FAQ, CTA or author box — `build.py` adds them.
  - Visa/entry: only say rules change and must be checked; do not state rules for a nationality unless verified today.
- Slug: lowercase ASCII `a-z0-9-` only, 3–6 words. Latin-script languages: in that language without accents (`babylone-irak-guide-visite`; Nordic letters ä/å→a, ö/ø→o, æ→ae: `besoke-babylon-irak-guide`). Non-Latin (ar, fa, ru, el, zh, ja, ko, th, hi, ur, ta): English words (`babylon-iraq-travel-guide`).
- Append to `_blog/L/posts.json` (create the file as `[]` if missing):
  `topic` (the plan key — identical in all languages, this links translations via hreflang), `slug`, `date` (today), `title` (≤60 chars; CJK/Korean ≤32 chars), `h1`, `description` (130–155 chars; CJK 60–90 chars), `excerpt` (≤150), `keywords` (6–10, comma-separated), `category` (translated, keep the same wording for the same category every day — reuse what earlier posts in L used), `region` (in L), `place` (short name in L), `geo` [lat, lon] (only if confident), `tour` ("7"/"9" from plan), `image`, `image_alt` (in L), `image_credit`, `facts` (4–6 [label, value] in L), `faq` (5–6 [question, answer] in L, answers 1–3 sentences).
- Tone everywhere: touristic, cultural and respectful. No modern politics, no modern war/conflict/destruction narratives, no "dark tourism". Religious sites: spiritual, architectural and heritage significance.
- Biographies and stories of Imams, Prophets and companions (Imam Ali, Imam Hussein, al-Abbas, Zaynab, Malik al-Ashtar, Muslim ibn Aqil, etc.): write with deep respect, using the well-known historical accounts; use the honorifics customary in each language (Arabic/Persian: عليه السلام / (ع) after the Imams, صلى الله عليه وآله وسلم after the Prophet; other languages: "Imam Ali (peace be upon him)" on first mention is fine). Historical events like the Battle of Karbala (680 CE) are told as history, without graphic detail and without sectarian polemics or attacks on any group. Where accounts differ, say "according to tradition". Quote the Qur'an or sayings only briefly and only if certain of the wording; prefer paraphrase.
- Everything in your own words, no copied text, no song lyrics or poems.

## 4. Images — free, no attribution, bright colours (one hero photo per topic, reuse it in every language)
Saif's rule: photos must be free of rights, shown WITHOUT any source/credit, and in bright, vivid colours.
- If another language of this topic already has an image, reuse the same `image`.
- Allowed sources ONLY: Pexels (pexels.com) and Unsplash (unsplash.com, free photos — not Unsplash+), whose licences allow use without attribution; or Wikimedia Commons files that are Public Domain or CC0. Never CC BY / CC BY-SA (they require a credit). Not allowed: Google Images, news sites, blogs, social media, watermarked stock, unclear licences, people as the main subject, public figures, and any image depicting the Prophet, the Imams or their family.
- Prefer colourful photos: blue sky, golden domes, sunsets, greenery, water — avoid black-and-white or dull grey shots.
- Confirm the photo really shows THIS place (WebSearch with allowed_domains pexels.com / unsplash.com, WebFetch the photo page for place and licence). For a biography/story topic use a photo of the related shrine, mosque or city.
- If the shell can download it, save `img/<topic>.webp` (≈1600px) and use that path. Otherwise the CDN URL: Pexels `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1600&h=800&fit=crop`; Unsplash `https://images.unsplash.com/photo-...?w=1600&q=80`.
- Leave `image_credit` empty (""). Nothing about the source is shown on the page.
- No suitable free photo of the exact place → `""` (decorative pattern), never a wrong or copyrighted photo.

## 5. Build, check, publish
1. Add your languages to the plan item's `langs_done`.
2. `python3 _blog/build.py` — fix any WARN (title/description length) and rebuild.
3. Check: every new page exists; ld+json blocks parse (`json.loads`); internal links point to existing files; `sitemap.xml` parses as XML.
4. `git pull --rebase origin main` (another group may have pushed), rebuild if the pull changed `_blog/`, commit `Blog: <topic> (<langs>)`, push to `main`. If the push is rejected, pull --rebase again and retry once.

Only touch `_blog/`, the `blog/` folders, `img/` and `sitemap.xml`. Never edit the tour pages. For biography/story topics the `place` field is the related city or shrine (e.g. Najaf), and `geo` is that shrine's location.
