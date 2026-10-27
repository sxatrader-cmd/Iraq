# Daily Italian blog article — instructions

Goal: publish ONE new Italian article per day on https://iraq.fabletour.com/it/blog/ about a landmark/place of Iraq, with strong SEO, matching the existing article `_blog/it/posts/babilonia-iraq-guida-visita.html` in quality, tone and structure.

## Steps
1. Open `_blog/it/plan.json` and take the FIRST item in `queue` with `"done": false`. (If the queue is empty, pick a well-known Iraqi landmark not yet covered in `_blog/it/posts.json` and add it to the queue.)
2. Research the place with web search (2–5 searches): location, distances from the nearest big city, history, what to see, opening/visiting practicalities. Only write facts you can support; if unsure, leave it out. Never invent prices, opening hours or ticket costs.
3. Do Italian keyword thinking: main keyword (e.g. "Ur Iraq", "ziggurat di Ur"), plus "visitare …", "cosa vedere …", "come arrivare a … da Baghdad". Use the main keyword in the title, H1, first paragraph, one H2 and the description — naturally, no stuffing.
4. Write the body fragment to `_blog/it/posts/<slug>.html` (slug: lowercase Italian, hyphens, no accents, 3–6 words, e.g. `ziggurat-di-ur-guida`):
   - 1,100–1,600 words of natural, fluent Italian written for Italian travellers.
   - Start with `<p class="lead">…</p>` (hook; an Italian cultural link if one exists naturally).
   - 5–8 `<h2>` sections, `<h3>` for sub-points, one `<ul>` of practical tips, an optional `<blockquote>` with a first-person guide note from Saif.
   - Include sections like: Dove si trova / Storia / Cosa vedere / Come arrivare (da Baghdad or nearest city) / Quando visitare / Consigli pratici / [Place] in un viaggio in Iraq.
   - 1–3 internal links to earlier blog articles where relevant: `<a href="/it/blog/<slug>/">…</a>`, and to the tours `/it/#tour-7-days` or `/it/#tour-9-days`.
   - Do NOT include the H1, facts box, FAQ, CTA or author box — `build.py` adds those.
   - Tone: purely touristic and cultural. No politics, no war/conflict/destruction narratives, no "dark tourism", no religious controversy. Religious sites are described by their spiritual, architectural and heritage significance.
   - No copied text from sources; everything in your own words. No song lyrics or poems.
5. Append an entry to `_blog/it/posts.json` with today's date (Baghdad time, YYYY-MM-DD) and these fields:
   `slug, date, title (≤60 chars, keyword first, may end with "(2026)"), h1, description (130–155 chars), excerpt (≤150 chars), keywords (comma list, 6–10), category (use the plan item's), region, place (short name), geo [lat, lon] (only if confident), tour ("7" or "9" from the plan item), image (path of a photo in /img/ only if one in the repo truly shows this place, else ""), facts (4–6 [label, value] pairs), faq (5–6 [question, answer] pairs, answers 1–3 sentences)`.
6. Mark the plan item `"done": true` and add `"slug"`.
7. Run `python3 _blog/build.py`. Fix any WARN about title/description length and rebuild.
8. Check the output: open `it/blog/<slug>/index.html`, confirm the JSON-LD parses (`python3 -c` with json.loads on each ld+json block) and internal links point to existing pages.
9. Commit with message `Blog IT: <place>` and push to `main`.

Never edit other language folders or the tour pages. Only touch `_blog/`, `it/blog/` and `sitemap.xml`.
