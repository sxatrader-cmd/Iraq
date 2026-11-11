# Daily multilingual blog — instructions

Site: https://iraq.fabletour.com — 34 blogs: 33 languages (incl. Central Kurdish / Sorani `ckb`) + Traditional Chinese (`zh-tw`).

## 0. Publishing schedule — 7-weekday rotation (Saif's rule, from 2026-11-11)
ONE run per day (Baghdad date, Asia/Baghdad). Each run writes exactly ONE new article for every blog in that weekday's group, and nothing for any other blog. Every blog therefore gets one article per week; English gets two (Tuesday and Wednesday) — 35 articles per week in total. The same table is in `_blog/plan.json` → `schedule`.

| Day (Baghdad) | Blogs |
|---|---|
| Sunday | ckb, hi, ur, id, cs |
| Monday | ms, th, vi, ta, el |
| Tuesday | ro, sk, hr, ka, en |
| Wednesday | ar (root `/blog/`), en, de, ja, sv |
| Thursday | fr, es, ru, ko, fi |
| Friday | it, pt, tr, zh, da |
| Saturday | nl, pl, fa, zh-tw, no |

- Find today's weekday in Asia/Baghdad time and take that row. No post-count thresholds: the rotation applies to every blog no matter how many articles it has.
- Never write more than one article per blog per day, and never write for a blog outside today's row (no catch-up runs on other days).

Blog URLs: Arabic → `/blog/`, every other language L → `/L/blog/` (Traditional Chinese → `/zh-tw/blog/`). Sources live in `_blog/L/`.

## 1. Pick today's topic (Baghdad date, YYYY-MM-DD)
Open `_blog/plan.json` → `queue`.
Pick the topic separately for each blog L of today's row:
- **Backlog first:** the oldest queue item that already has a `"date"` and does not have L in `langs_done` → that is L's topic today (so a blog catches up one topic per week, oldest first).
- **Otherwise a new topic:** the first item with `"date": null`; set its `"date"` to today. Other blogs of today's row with no backlog item take this same new topic, so a day normally adds at most one new topic.
- TOPIC RULE (Saif's instruction): write ONLY about places, history and stories connected to the cities and sites in the two tour programmes — Baghdad (Kadhimiya, Mutanabbi St, Qishla, Mustansiriya, Aqar Quf), Babylon & Borsippa, Karbala, Kufa, Najaf, Uruk, Basra & Qurna, the Marshes, Ur, Samarra, Mosul & Nineveh, Nimrud, Hatra, Mar Mattai, Erbil. Topics can be a site, or a person/story tied to it (e.g. Najaf → biography of Imam Ali, stories from his life, his companions; Kufa → the Great Mosque, Muslim ibn Aqil; Karbala → Imam Hussein, al-Abbas, the companions of Hussein). If the queue runs out, add new topics of this kind only, rotating between cities, never places outside the programmes.
- The item's `title` is an English working title and `category_en` the category; translate the category consistently per language.
- Exactly one article per blog of today's row; if a run fails, the missed article is simply picked up by the backlog rule the next week.

## 2. Research once
If another language of this topic already exists (check `langs_done`; the files are `_blog/<lang>/posts/<slug>.html`), read it first and use it as the factual base. Otherwise research with web search (2–5 searches). Only write facts you can support. Never invent prices, opening hours or ticket costs.

## 3. Write each article — native, not a word-for-word translation
For each language L:
- 1,000–1,500 words (CJK incl. Korean and zh-tw: 2,000–3,000 characters; Thai similar length) of natural, fluent text for travellers from that country. Adapt the hook to the reader (Italian/Romanian: Verdi's Nabucco for Babylon; German: the Ishtar Gate in Berlin's Pergamon Museum; Malay/Indonesian/Persian/Arabic/Turkish/Urdu/Hindi/Tamil readers: religious-heritage (ziyarat) visitors are common — Urdu: use customary honorifics (ؑ after the Imams, ؐ/ﷺ after the Prophet); Hindi/Tamil: plain respectful wording; Chinese/Japanese/Korean: practical tone, clear structure. Korean (ko): South Korea currently bans its citizens from travelling to Iraq (MOFA travel-ban list), so never address the reader as a traveller from Korea or suggest booking from Korea; write cultural/historical guides for Korean speakers).
- Do local keyword thinking in L: the main keyword as people in that country search it (e.g. de "Babylon Irak besichtigen", fr "visiter Babylone", ru "Вавилон Ирак экскурсия", ja "バビロン遺跡 行き方", ko "바빌론 유적 이라크 여행", fi "Babylon Irak nähtävyydet", sv "besöka Babylon Irak", da "besøge Babylon Irak", no "besøke Babylon Irak", sk "Babylon Irak návšteva", hr "posjet Babilonu Irak", ro "vizită Babilon Irak", nl "Babylon Irak bezoeken", pt "visitar Babilónia Iraque", ckb "سەردانی بابل", vi "du lịch Babylon Iraq"). Use it in title, h1, first paragraph, one h2 and description — naturally.
- Body fragment → `_blog/L/posts/<slug>.html`:
  - Starts with `<p class="lead">…</p>`; then 5–8 `<h2>` sections, `<h3>` sub-points, one `<ul>` of practical tips, optional `<blockquote>` with a first-person note from the guide Saif.
  - Sections like: where it is / history / what to see / how to get there (from Baghdad or nearest city) / best time to visit / practical tips / the place in an Iraq trip.
  - Internal links: 1–3 to earlier articles in the SAME language (`/L/blog/<slug>/`, Arabic `/blog/<slug>/`), and to the tours: `/L/#tour-7-days` or `/L/#tour-9-days` (Arabic: `/#tour-7-days`).
  - Do NOT include H1, facts box, FAQ, CTA or author box — `build.py` adds them.
  - Visa/entry: only say rules change and must be checked; do not state rules for a nationality unless verified today.
- Slug: lowercase ASCII `a-z0-9-` only, 3–6 words. Latin-script languages: in that language without accents (`babylone-irak-guide-visite`; Nordic letters ä/å→a, ö/ø→o, æ→ae: `besoke-babylon-irak-guide`). Vietnamese (vi): Vietnamese words without diacritics (`du-lich-babylon-iraq`). Non-Latin (ar, ckb, fa, ru, el, zh, zh-tw, ja, ko, th, hi, ur, ta): English words (`babylon-iraq-travel-guide`).
- Append to `_blog/L/posts.json` (create the file as `[]` if missing):
  `topic` (the plan key — identical in all languages, this links translations via hreflang), `slug`, `date` (today), `title` (≤60 chars; CJK/Korean/zh-tw ≤32 chars), `h1`, `description` (130–155 chars; CJK 60–90 chars), `excerpt` (≤150), `keywords` (6–10, comma-separated), `category` (translated, keep the same wording for the same category every day — reuse what earlier posts in L used), `region` (in L), `place` (short name in L), `geo` [lat, lon] (only if confident), `tour` ("7"/"9" from plan), `image`, `image_alt` (in L), `image_credit`, `facts` (4–6 [label, value] in L), `faq` (5–6 [question, answer] in L, answers 1–3 sentences).
- Tone everywhere: touristic, cultural and respectful. No modern politics, no modern war/conflict/destruction narratives, no "dark tourism". Religious sites: spiritual, architectural and heritage significance.
- Biographies and stories of Imams, Prophets and companions (Imam Ali, Imam Hussein, al-Abbas, Zaynab, Malik al-Ashtar, Muslim ibn Aqil, etc.): write with deep respect, using the well-known historical accounts; use the honorifics customary in each language (Arabic/Persian: عليه السلام / (ع) after the Imams, صلى الله عليه وآله وسلم after the Prophet; Kurdish (ckb): (سڵاوی خوای لێ بێت) after the Imams and Prophets on first mention, (درودی خوای لەسەر بێت) after the Prophet Muhammad; other languages: "Imam Ali (peace be upon him)" on first mention is fine). Historical events like the Battle of Karbala (680 CE) are told as history, without graphic detail and without sectarian polemics or attacks on any group. Where accounts differ, say "according to tradition". Quote the Qur'an or sayings only briefly and only if certain of the wording; prefer paraphrase.
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
4. `git pull --rebase origin main`, rebuild if the pull changed `_blog/`, commit `Blog: <topic> (<langs>)` (several topics: `Blog: <topic> (<langs>) + <topic> (<langs>)`), push to `main` (never force-push). If the push is rejected, pull --rebase again and retry once.

Only touch `_blog/` (incl. `_blog/zh-tw/`), the `blog/` folders (incl. `zh-tw/blog/`), `blog-kb/`, `img/` and `sitemap.xml`. `build.py` also regenerates `blog-kb/<lang>.json` (the website chatbot answers visitors' questions from every article) — always commit it together with the article. Never edit the tour pages. For biography/story topics the `place` field is the related city or shrine (e.g. Najaf), and `geo` is that shrine's location.


## Central Kurdish (ckb) notes
Write natural Sorani (Central Kurdish) in Arabic script for Kurdish readers in Iraq (Erbil, Sulaymaniyah, Duhok) and the diaspora. Use Kurdish month names (کانوونی دووەم … کانوونی یەکەم). Tour links: `/ckb/#tour-7-days`, `/ckb/#tour-9-days`; blog: `/ckb/blog/<slug>/`. Categories used so far: شوێنەوارە مێژووییەکان (Archaeological sites), شوێنە پیرۆزەکان (Holy shrines), شار و کەلتوور (Cities & culture). Backfill: ckb started on 2026-11-04 with babylon, imam-ali-shrine-in-najaf and the-great-ziggurat-of-ur; older topics without ckb are filled by the backlog rule in §1 (one per week, oldest first).

## Vietnamese (vi) notes
Write natural Vietnamese (tiếng Việt) for travellers from Vietnam and the Vietnamese diaspora. Vietnam is a growing source market for Iraq (Saif: many Vietnamese tourists). Lead with history, archaeology and the Marshes; holy-shrine topics are explained respectfully as cultural and religious heritage. Practical notes: flights usually connect via Doha, Dubai or Istanbul; prices in USD. Tour links: `/vi/#tour-7-days`, `/vi/#tour-9-days`; blog: `/vi/blog/<slug>/`. Vietnamese started on 2026-11-04 with no articles; older topics are filled by the backlog rule in §1 (one per week, oldest first).

## Traditional Chinese (zh-tw) notes
Write natural Traditional Chinese with Taiwan usage (部落格, 資訊, 行程, 簡訊…) for readers in Taiwan, Hong Kong and the overseas Chinese community — adapt, do not just convert the Simplified article character by character (if the zh article of the topic exists, use it as the factual base). Sources: `_blog/zh-tw/posts.json` + `_blog/zh-tw/posts/<slug>.html`; output `/zh-tw/blog/<slug>/`. Slug: English words, preferably the same slug as the zh article of the topic. hreflang: `build.py` pairs zh-tw with the other languages by `topic` (zh-tw is inserted right after zh-Hans as `zh-Hant`; `<html lang="zh-Hant-TW">`). Tour links: `/zh-tw/#tour-7-days`, `/zh-tw/#tour-9-days`. Categories used so far: 考古遺址 (Archaeological sites), 聖地與陵寺 (Holy shrines); use 城市與文化 (Cities & culture) and 自然 (Nature). The two first articles (babylon, imam-ali-shrine-in-najaf, Oct 2026) were static pages migrated into the builder on 2026-11-11 with unchanged URLs and text.
