/* Private visitors view: one row per visitor, bot / human labels, page journey. Data: Supabase RPCs visitor_stats / visitor_journey (PIN-checked server-side). */
(function () {
  "use strict";
  var API = "https://zrbbnveaqockoptftqst.supabase.co/rest/v1/rpc/", K = "sb_publishable_YscqakXUfq9ngPjaAhe2KA__sFDoMcl";
  var $ = function (i) { return document.getElementById(i); }, vout = $("vout"), tab = "S", data = [], filt = "all", grp = "v", busy = false;
  var CN = null; try { CN = new Intl.DisplayNames(["ar"], { type: "region" }); } catch (e) {}
  function esc(t) { var d = document.createElement("div"); d.textContent = t == null ? "" : String(t); return d.innerHTML; }
  function flag(c) { if (!c || c.length !== 2 || c === "XX" || c === "T1") return "🌐"; return String.fromCodePoint.apply(null, c.toUpperCase().split("").map(function (x) { return 127397 + x.charCodeAt(0); })); }
  function cname(c) { if (!c || c === "XX" || c === "T1") return "غير معروف"; try { return CN ? CN.of(c.toUpperCase()) : c; } catch (e) { return c; } }
  function dt(t) { try { return new Date(t).toLocaleString("en-GB", { timeZone: "Asia/Baghdad", day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false }); } catch (e) { return t; } }
  function tm(t) { try { return new Date(t).toLocaleTimeString("en-GB", { timeZone: "Asia/Baghdad", hour12: false }); } catch (e) { return t; } }
  function dur(ms) { ms = +ms || 0; if (ms < 1000) return ms ? "<1ث" : "—"; var s = Math.round(ms / 1000); return s < 60 ? s + "ث" : Math.floor(s / 60) + "د " + (s % 60) + "ث"; }
  function rpc(fn, body) {
    return fetch(API + fn, { method: "POST", headers: { apikey: K, Authorization: "Bearer " + K, "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { if (r.status === 404) throw { missing: 1 }; return j; }); });
  }

  /* ---- source / device ---- */
  function source(v) {
    var u = v.utm || {};
    if (u.gclid) return "Google (إعلان)"; if (u.ttclid) return "TikTok (إعلان)"; if (u.msclkid) return "Bing (إعلان)";
    if (u.utm_source) return u.utm_source + (u.utm_medium ? " / " + u.utm_medium : "") + (u.utm_campaign ? " · " + u.utm_campaign : "");
    var h = ""; try { h = v.referrer ? new URL(v.referrer).hostname.replace(/^www\.|^m\.|^l\.|^lm\./, "") : ""; } catch (e) {}
    if (u.fbclid && !h) return "Facebook";
    if (!h) return "مباشر / بدون مصدر";
    if (/(^|\.)google\./.test(h)) return "Google"; if (/bing\.com$/.test(h)) return "Bing"; if (/yandex\./.test(h)) return "Yandex";
    if (/duckduckgo/.test(h)) return "DuckDuckGo"; if (/facebook\.com$|fb\.com$|fb\.me$/.test(h)) return "Facebook"; if (/instagram\.com$/.test(h)) return "Instagram";
    if (/tiktok\.com$/.test(h)) return "TikTok"; if (/^t\.co$|x\.com$|twitter\.com$/.test(h)) return "X"; if (/youtube\.com$|youtu\.be$/.test(h)) return "YouTube";
    if (/chatgpt\.com$|openai\.com$/.test(h)) return "ChatGPT"; if (/perplexity/.test(h)) return "Perplexity";
    if (h === location.hostname) return "داخلي (من صفحة بالموقع)";
    return h;
  }
  function device(ua) {
    ua = ua || ""; var os = /iPhone/.test(ua) ? "iPhone" : /iPad/.test(ua) ? "iPad" : /Android/.test(ua) ? "Android" : /Windows/.test(ua) ? "Windows" : /Mac OS X|Macintosh/.test(ua) ? "Mac" : /CrOS/.test(ua) ? "ChromeOS" : /Linux/.test(ua) ? "Linux" : "؟";
    var b = /FBAN|FBAV|FB_IAB/.test(ua) ? "تطبيق Facebook" : /Instagram/.test(ua) ? "تطبيق Instagram" : /musical_ly|BytedanceWebview|TikTok/i.test(ua) ? "تطبيق TikTok" : /HeadlessChrome/.test(ua) ? "Chrome مخفي" :
      /Edg\//.test(ua) ? "Edge" : /OPR\/|Opera/.test(ua) ? "Opera" : /SamsungBrowser/.test(ua) ? "Samsung" : /Firefox|FxiOS/.test(ua) ? "Firefox" : /CriOS|Chrome\//.test(ua) ? "Chrome" : /Safari/.test(ua) ? "Safari" : "؟";
    return os + " · " + b;
  }

  /* ---- bot scoring ---- */
  var DC = /alibaba|aliyun|tencent|amazon|\baws\b|google cloud|google llc|microsoft|azure|digitalocean|digital ocean|linode|akamai|\bovh|hetzner|contabo|vultr|choopa|constant company|oracle|huawei|m247|leaseweb|datacamp|cdn77|scaleway|ionos|hostinger|colocrossing|zenlayer|ucloud|baidu|bytedance|byteplus|cloudflare|fastly|hosting|\bhost|server|data ?cent|\bvps\b|cloud|psychz|quadranet|kamatera|hostwinds|netcup|g-?core|selectel|timeweb|serverius|worldstream|hivelocity|packethub|datapacket|tzulo|ipxo|censys|shodan|palo alto|internet-measurement|dedicated/i;
  var RELAY = /akamai|cloudflare|fastly/i;
  function tzOff(z) { try { var d = new Date(), s = d.toLocaleString("en-US", { timeZone: z }); return (new Date(s) - new Date(d.toLocaleString("en-US", { timeZone: "UTC" }))) / 36e5; } catch (e) { return null; } }
  function score(v) {
    var r = [], s = 0, ua = v.ua || "", i = v.ipinfo || {}, org = [i.org, i.isp, i.asn].filter(Boolean).join(" ");
    if (v.webdriver) { s += 5; r.push("متصفح يُدار آلياً (webdriver)"); }
    if (!ua) { s += 3; r.push("بدون معرّف متصفح"); }
    else if (/headless|phantom|puppeteer|playwright|selenium|bot\b|bot\/|crawl|spider|python|curl|wget|httpclient|go-http|java\/|axios|node-fetch|scrapy|lighthouse|pagespeed|gtmetrix/i.test(ua)) { s += 5; r.push("معرّف متصفح آلي"); }
    var dc = org && DC.test(org);
    if (dc && /Safari/.test(ua) && !/Chrome|CriOS|Android/.test(ua) && RELAY.test(org)) { s += 1; r.push("IP شبكة " + (i.org || i.isp) + " (قد يكون iCloud Private Relay)"); dc = false; }
    else if (dc) { s += 3; r.push("IP سيرفرات: " + (i.org || i.isp || i.asn)); }
    if (/^(800x600|1024x768|0x0)@1$/.test(v.screen || "")) { s += 2; r.push("حجم شاشة متصفح مخفي " + v.screen); }
    if (!v.lang) { s += 1; r.push("بدون لغة متصفح"); }
    if (!v.interacted) { var p = v.views >= 3 ? 2 : 1; s += p; r.push("لا حركة ماوس ولا سكرول ولا لمس"); }
    if (v.views >= 4 && v.med_gap != null && v.med_gap < 3) { s += 2; r.push(v.views + " صفحات بفارق " + v.med_gap + " ثانية"); }
    if (dc && !v.referrer && !v.utm) { s += 1; r.push("بدون مصدر + IP سيرفر"); }
    if (v.tz && i.tz && v.tz !== i.tz) { var a = tzOff(v.tz), b = tzOff(i.tz); if (a != null && b != null && Math.abs(a - b) >= 2) { s += 1; r.push("توقيت الجهاز (" + v.tz + ") لا يطابق دولة الـ IP (" + i.tz + ")"); } }
    var conv = (v.wa || 0) + (v.calls || 0) + (v.bot_q || 0) + (v.bot_wa || 0) + (v.bot_call || 0);
    if (conv && !v.webdriver) { s -= 2; r.push("✓ تواصل فعلي (واتساب/اتصال/سؤال)"); }
    if (v.interacted && v.dwell_ms > 10000 && !v.webdriver) { s -= 1; r.push("✓ تفاعل وبقي " + dur(v.dwell_ms)); }
    v._s = s; v._r = r; v._l = s >= 4 ? "b" : s >= 2 ? "s" : "h";
    if (!v.ipinfo && v._l === "h" && v.ip) v._pending = 1;
    return v;
  }

  /* ---- IP info lookup (ipwho.is, fallback ipapi.is), saved server-side once ---- */
  function norm(j, src) {
    if (src === 1) return j && j.success ? { city: j.city, region: j.region, cc: j.country_code, org: j.connection && j.connection.org, isp: j.connection && j.connection.isp, asn: j.connection && j.connection.asn ? "AS" + j.connection.asn : "", tz: j.timezone && j.timezone.id } : null;
    return j && j.ip ? { city: j.city, region: j.region, country: j.country, org: j.company, isp: j.company, asn: j.asn, tz: j.timezone } : null;
  }
  function look(ip) {
    return fetch("https://ipwho.is/" + encodeURIComponent(ip)).then(function (r) { return r.json(); }).then(function (j) { var n = norm(j, 1); if (n) return n; throw 0; })
      .catch(function () { return fetch("https://api.ipapi.is/?q=" + encodeURIComponent(ip)).then(function (r) { return r.json(); }).then(function (j) { return norm(j, 2); }); })
      .catch(function () { return null; });
  }
  function enrich(pin) {
    var need = {}, list = [];
    data.forEach(function (v) { if (v.ip && !v.ipinfo && !need[v.ip]) { need[v.ip] = 1; list.push(v.ip); } });
    list = list.slice(0, 120); if (!list.length) return;
    var got = [], i = 0, run = 0;
    function next() {
      if (i >= list.length) { if (!run) fin(); return; }
      var ip = list[i++]; run++;
      look(ip).then(function (n) { run--; if (n) { got.push({ ip: ip, info: n }); data.forEach(function (v) { if (v.ip === ip) v.ipinfo = n; }); } if (got.length % 15 === 0) render(); next(); });
    }
    function fin() { render(); if (got.length) for (var k = 0; k < got.length; k += 100) rpc("visitor_ipinfo_save", { items: got.slice(k, k + 100), pin: pin }).catch(function () {}); }
    for (var c = 0; c < 4; c++) next();
  }

  /* ---- grouping by IP ---- */
  function byIp(list) {
    var m = {}, out = [];
    list.forEach(function (v) {
      var k = v.ip || v.visitor_id, g = m[k];
      if (!g) { g = m[k] = JSON.parse(JSON.stringify(v)); g._vids = [v.visitor_id]; out.push(g); return; }
      g._vids.push(v.visitor_id); g.views += v.views; g.sessions += v.sessions; g.pages = Math.max(g.pages, v.pages); g.dwell_ms += v.dwell_ms;
      g.interacted = g.interacted || v.interacted; g.webdriver = g.webdriver || v.webdriver; g.wa += v.wa; g.calls += v.calls; g.other_clicks += v.other_clicks;
      g.bot_open += v.bot_open; g.bot_q += v.bot_q; g.bot_wa += v.bot_wa; g.bot_call += v.bot_call;
      if (v.first_seen < g.first_seen) { g.first_seen = v.first_seen; g.referrer = v.referrer || g.referrer; g.utm = v.utm || g.utm; g.landing = v.landing; }
      if (v.last_seen > g.last_seen) g.last_seen = v.last_seen;
      if (v.med_gap != null) g.med_gap = g.med_gap == null ? v.med_gap : Math.min(g.med_gap, v.med_gap);
    });
    return out;
  }

  var LBL = { h: "إنسان", b: "بوت", s: "مشكوك" };
  function render() {
    var list = (grp === "ip" ? byIp(data) : data.map(function (v) { var c = JSON.parse(JSON.stringify(v)); c._vids = [v.visitor_id]; return c; })).map(score);
    var n = { h: 0, b: 0, s: 0 }, pv = { h: 0, b: 0, s: 0 }; list.forEach(function (v) { n[v._l]++; pv[v._l] += v.views; });
    var conv = list.filter(function (v) { return v._l !== "b" && (v.wa + v.calls + v.bot_q + v.bot_wa + v.bot_call) > 0; }).length;
    var h = '<div class="kpis">' +
      '<div class="k"><b style="color:#2E7D4F">' + n.h + '</b><span>إنسان حقيقي · ' + pv.h + ' صفحة</span></div>' +
      '<div class="k"><b style="color:#C98A1B">' + n.s + '</b><span>مشكوك · ' + pv.s + ' صفحة</span></div>' +
      '<div class="k"><b style="color:#B03A2E">' + n.b + '</b><span>بوت · ' + pv.b + ' صفحة</span></div>' +
      '<div class="k"><b>' + conv + '</b><span>تواصلوا (واتساب / اتصال / سؤال)</span></div></div>';
    h += '<div class="fl">' + [["all", "الكل (" + list.length + ")"], ["h", "إنسان"], ["s", "مشكوك"], ["b", "بوت"], ["c", "تواصلوا فقط"]].map(function (x) { return '<button data-f="' + x[0] + '"' + (filt === x[0] ? ' class="on"' : "") + ">" + x[1] + "</button>"; }).join("") +
      '<span style="flex:1"></span>' + [["v", "حسب الجهاز"], ["ip", "حسب الـ IP"]].map(function (x) { return '<button data-g="' + x[0] + '"' + (grp === x[0] ? ' class="on"' : "") + ">" + x[1] + "</button>"; }).join("") + "</div>";
    var shown = list.filter(function (v) { return filt === "all" || filt === v._l || (filt === "c" && (v.wa + v.calls + v.bot_q + v.bot_wa + v.bot_call) > 0); });
    if (!shown.length) h += '<p class="msg">لا يوجد زوار بهذا التصنيف</p>';
    h += shown.slice(0, 600).map(function (v, ix) {
      var i = v.ipinfo || {}, place = flag(v.country) + " " + cname(v.country) + (i.city ? " · " + esc(i.city) : "");
      var cv = [];
      if (v.wa) cv.push("واتساب ×" + v.wa); if (v.calls) cv.push("اتصال ×" + v.calls); if (v.other_clicks) cv.push("تيليغرام/فايبر/إيميل ×" + v.other_clicks);
      if (v.bot_open) cv.push("فتح البوت"); if (v.bot_q) cv.push("سأل البوت ×" + v.bot_q); if (v.bot_wa) cv.push("واتساب من البوت");
      return '<div class="vc" data-i="' + ix + '"><div class="top"><span class="lb ' + v._l + '">' + LBL[v._l] + '</span><span class="ip">' + esc(v.ip || "؟") + "</span>" +
        (v.ips && v.ips.length > 1 ? '<small style="color:var(--muted)">+' + (v.ips.length - 1) + " IP</small>" : "") +
        "<span>" + place + "</span>" + (cv.length ? cv.map(function (c) { return '<span class="cv">' + esc(c) + "</span>"; }).join("") : "") + "</div>" +
        '<div class="meta"><span>🏢 ' + esc(i.org || i.isp || (v._pending ? "…" : "—")) + (i.asn ? " <small>" + esc(i.asn) + "</small>" : "") + "</span><span>📱 " + esc(device(v.ua)) + (v.screen ? " · " + esc(v.screen) : "") + "</span>" +
        "<span>🔁 " + v.sessions + " زيارة · " + v.views + " صفحة · " + dur(v.dwell_ms) + "</span>" + (v._vids.length > 1 ? "<span>👥 " + v._vids.length + " أجهزة/متصفحات</span>" : "") +
        "<span>🔗 " + esc(source(v)) + "</span><span>🕒 " + dt(v.first_seen) + " ← " + dt(v.last_seen) + "</span><span>📍 " + esc(decodeURI(v.landing || "")) + "</span></div>" +
        (v._r.length ? '<div class="why">' + v._r.map(esc).join(" · ") + "</div>" : "") + '<div class="jr" style="display:none"></div></div>';
    }).join("");
    if (shown.length > 600) h += '<p class="msg">يُعرض أول 600 فقط</p>';
    h += '<p class="msg" style="font-size:12px">التصنيف تقديري حسب علامات متعددة · الأوقات بتوقيت بغداد · الـ IP كامل ومحمي بالرمز · البيانات تُحذف بعد 90 يوماً</p>';
    vout.innerHTML = h; vout._list = shown;
  }

  vout.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (b && b.dataset.f) { filt = b.dataset.f; render(); return; }
    if (b && b.dataset.g) { grp = b.dataset.g; render(); return; }
    if (e.target.closest(".jr")) return;
    var c = e.target.closest(".vc"); if (!c) return;
    var j = c.querySelector(".jr"); if (j.style.display === "block") { j.style.display = "none"; return; }
    j.style.display = "block"; j.innerHTML = '<p class="msg">جارٍ التحميل…</p>';
    var v = vout._list[+c.dataset.i], pin = $("pin").value.trim();
    Promise.all(v._vids.map(function (id) { return rpc("visitor_journey", { vid: id, pin: pin }); })).then(function (rs) {
      var ev = [].concat.apply([], rs.filter(Array.isArray)).sort(function (a, b) { return a.at < b.at ? -1 : 1; }), last = "", h = "";
      ev.forEach(function (x) {
        if (x.session_id !== last) { last = x.session_id; h += '<div class="sep">زيارة ' + dt(x.at) + (x.ip ? " · " + esc(x.ip) : "") + (x.referrer && x.kind === "view" ? " · من " + esc(source({ referrer: x.referrer, utm: x.utm })) : "") + "</div>"; }
        h += '<div class="st"><time>' + tm(x.at) + "</time>" + (x.kind === "click"
          ? '<span class="pg">👆 ضغط ' + esc((x.detail || "").split(":")[0]) + " <small>" + esc(decodeURI(x.page || "")) + "</small></span>"
          : '<span class="pg">' + esc(decodeURI(x.page || "")) + (x.title ? " <small style='color:var(--muted)'>" + esc(x.title) + "</small>" : "") + "</span><span>" + dur(x.dwell_ms) + (x.scroll_pct ? " · ↓" + x.scroll_pct + "%" : "") + (x.interacted ? "" : " · بلا حركة") + "</span>") + "</div>";
      });
      j.innerHTML = h || '<p class="msg">لا توجد تفاصيل</p>';
    }).catch(function () { j.innerHTML = '<p class="msg">تعذّر التحميل</p>'; });
  });

  function loadV() {
    var pin = $("pin").value.trim(); if (!pin || busy) return;
    busy = true; vout.innerHTML = '<p class="msg">جارٍ التحميل…</p>';
    rpc("visitor_stats", { days: Math.min(90, +$("days").value), pin: pin }).then(function (d) {
      busy = false;
      if (!d || d.error || d.message) { vout.innerHTML = '<p class="msg">' + (d && d.error === "bad pin" ? "الرمز غير صحيح (أو محاولات خاطئة كثيرة، انتظر 15 دقيقة)" : "خطأ: " + esc(d && (d.message || d.error))) + "</p>"; return; }
      data = d.visitors || []; render(); enrich(pin);
    }).catch(function (e) {
      busy = false;
      vout.innerHTML = '<p class="msg">' + (e && e.missing ? "صفحة الزوار جاهزة، لكن قاعدة البيانات لم تُفعَّل بعد (يلزم تشغيل ملف SQL في Supabase مرة واحدة)." : "تعذّر الاتصال") + "</p>";
    });
  }
  function show(t) {
    tab = t; $("tS").className = t === "S" ? "on" : ""; $("tV").className = t === "V" ? "on" : "";
    $("out").style.display = t === "S" ? "" : "none"; vout.style.display = t === "V" ? "" : "none";
    document.querySelector("main").className = t === "V" ? "wide" : "";
    if (t === "V" && !data.length) loadV();
  }
  $("tS").addEventListener("click", function () { show("S"); });
  $("tV").addEventListener("click", function () { show("V"); });
  $("go").addEventListener("click", function () { if (tab === "V") loadV(); });
  $("days").addEventListener("change", function () { if (tab === "V") loadV(); });
  $("pin").addEventListener("keydown", function (e) { if (e.key === "Enter" && tab === "V") loadV(); });
})();
