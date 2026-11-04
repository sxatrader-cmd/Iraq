/* Fable Tour – "Latest from the blog" section above the booking form.
   Reads the newest posts from the blog of the page's own language, so each
   language page only shows articles written in that language. */
(function () {
  "use strict";
  var LANGS = ["zh-tw","cs","da","de","el","en","es","fa","fi","fr","hi","hr","id","it","ja","ka","ko","ms","nl","no","pl","pt","ro","ru","sk","sv","ta","th","tr","ur","zh","ckb"];
  var seg = (location.pathname.split("/")[1] || "").toLowerCase();
  var LG = LANGS.indexOf(seg) >= 0 ? seg : "ar";
  var BLOG = (LG === "ar" ? "/" : "/" + LG + "/") + "blog/";
  var MAX = 3;

  function txt(el) { return el ? el.textContent.replace(/\s+/g, " ").trim() : ""; }
  function bg(el) { var m = el && (el.getAttribute("style") || "").match(/url\(['"]?([^'")]+)['"]?\)/); return m ? m[1] : ""; }
  function el(tag, cls, t) { var e = document.createElement(tag); if (cls) e.className = cls; if (t != null) e.textContent = t; return e; }

  var css = ".lp{padding-top:0}" +
    ".lp-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}" +
    ".lp-head h2{margin:4px 0 0}" +
    ".lp-all{color:var(--navy,#1B2A47);font-weight:700;font-size:14.5px;text-decoration:none;border-bottom:2px solid var(--gold,#B8955A);padding-bottom:2px;white-space:nowrap}" +
    ".lp-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}" +
    ".lp-c{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line,rgba(27,42,71,.12));border-radius:6px;overflow:hidden;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s}" +
    ".lp-c:hover{box-shadow:0 10px 26px -14px rgba(27,42,71,.45);transform:translateY(-2px)}" +
    ".lp-ph{aspect-ratio:16/9;background:var(--navy,#1B2A47) center/cover no-repeat;position:relative;filter:saturate(1.3) contrast(1.05) brightness(1.03)}" +
    ".lp-ph span{position:absolute;inset-inline-start:12px;bottom:10px;background:var(--gold,#B8955A);color:var(--navy,#1B2A47);font-size:11.5px;font-weight:700;padding:4px 8px;border-radius:3px}" +
    ".lp-bd{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}" +
    ".lp-bd h3{margin:0;font-size:18px;line-height:1.4;color:var(--navy,#1B2A47)}" +
    ".lp-bd p{margin:0;font-size:14.5px;color:var(--muted,#5b6475);line-height:1.55}" +
    ".lp-bd small{margin-top:auto;padding-top:4px;font-size:12.5px;color:var(--muted,#5b6475)}" +
    "@media (max-width:900px){.lp-grid{grid-template-columns:1fr 1fr}}" +
    "@media (max-width:600px){.lp-grid{grid-template-columns:1fr}}";

  function render(doc) {
    var posts = [], seen = {};
    function add(a, cat) {
      var href = a.getAttribute("href"); if (!href || seen[href]) return; seen[href] = 1;
      var ph = a.querySelector(".ph");
      posts.push({ href: href, img: bg(ph), cat: cat || txt(ph && ph.querySelector("span")),
        h: txt(a.querySelector("h2, h3")), p: txt(a.querySelector("p")), d: txt(a.querySelector("small")) });
    }
    var f = doc.querySelector("a.featured");
    var label = "";
    if (f) {
      var eb = txt(f.querySelector(".eyebrow")).split("·");
      label = (eb[0] || "").trim();
      add(f, (eb[1] || "").trim());
    }
    doc.querySelectorAll("#posts a.pc, a.pc").forEach(function (a) { add(a); });
    if (!posts.length) return;
    var form = document.getElementById("interest"); if (!form || document.getElementById("latest-posts")) return;

    var st = el("style"); st.textContent = css; document.head.appendChild(st);
    var sec = el("section", "block in lp"); sec.id = "latest-posts";
    var head = el("div", "lp-head"), hl = el("div");
    var blogWord = txt(document.querySelector(".blog-link")) || "Blog";
    hl.appendChild(el("span", "eyebrow", label || blogWord));
    var h2 = el("h2", "disp", txt(doc.querySelector("h1")) || blogWord); hl.appendChild(h2);
    var all = el("a", "lp-all", blogWord + (document.documentElement.dir === "rtl" ? " ←" : " →")); all.href = BLOG;
    head.appendChild(hl); head.appendChild(all); sec.appendChild(head);
    var grid = el("div", "lp-grid");
    posts.slice(0, MAX).forEach(function (p) {
      var a = el("a", "lp-c"); a.href = p.href;
      var ph = el("div", "lp-ph"); if (p.img) ph.style.backgroundImage = "url('" + p.img + "')";
      if (p.cat) ph.appendChild(el("span", null, p.cat));
      var bd = el("div", "lp-bd"); bd.appendChild(el("h3", null, p.h));
      if (p.p) bd.appendChild(el("p", null, p.p));
      if (p.d) bd.appendChild(el("small", null, p.d));
      a.appendChild(ph); a.appendChild(bd); grid.appendChild(a);
    });
    sec.appendChild(grid);
    form.parentNode.insertBefore(sec, form);
  }

  function go() {
    if (!document.getElementById("interest")) return;
    fetch(BLOG, { credentials: "same-origin" }).then(function (r) { if (!r.ok) throw 0; return r.text(); })
      .then(function (h) { render(new DOMParser().parseFromString(h, "text/html")); })
      .catch(function () {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go); else go();
})();
