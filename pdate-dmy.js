/* Localized date picker: replaces native <input type="date"> (which always shows the
   device's own format, e.g. mm/dd/yyyy) with Day / Month / Year selects written in the
   page language. The original input stays as a hidden field holding YYYY-MM-DD, so the
   form, Web3Forms submission and min-date logic keep working unchanged. */
(function () {
  var lang = (document.documentElement.lang || "en").trim();
  var loc = lang.indexOf("ar") === 0 ? "ar-u-nu-latn-ca-gregory" : lang + "-u-ca-gregory";
  try { new Intl.DateTimeFormat(loc); } catch (e) { loc = "en"; }
  var rtl = document.documentElement.dir === "rtl";

  function cap(s) { return s ? s.charAt(0).toLocaleUpperCase(lang) + s.slice(1) : s; }
  function fmt(d, o) {
    try { return new Intl.DateTimeFormat(loc, Object.assign({ timeZone: "UTC" }, o)).format(d); }
    catch (e) { return ""; }
  }
  function field(k, fb) {
    try { var v = new Intl.DisplayNames([loc], { type: "dateTimeField" }).of(k); if (v) return cap(v); } catch (e) {}
    return fb;
  }
  // languages whose names browsers may not ship in their date data
  var FIX = {
    ckb: { l: ["ڕۆژ", "مانگ", "ساڵ"], m: ["کانوونی دووەم", "شوبات", "ئازار", "نیسان", "ئایار", "حوزەیران", "تەممووز", "ئاب", "ئەیلوول", "تشرینی یەکەم", "تشرینی دووەم", "کانوونی یەکەم"], o: ["day", "month", "year"] },
    ka: { l: ["დღე", "თვე", "წელი"], m: ["იანვარი", "თებერვალი", "მარტი", "აპრილი", "მაისი", "ივნისი", "ივლისი", "აგვისტო", "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"], o: ["day", "month", "year"] },
    el: { l: ["Ημέρα", "Μήνας", "Έτος"], m: ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"] }
  }[lang.split("-")[0]];
  var LBL = FIX ? { day: FIX.l[0], month: FIX.l[1], year: FIX.l[2] }
    : { day: field("day", "DD"), month: field("month", "MM"), year: field("year", "YYYY") };

  // order of day / month / year as written in this language
  var ORDER = ["day", "month", "year"];
  try {
    var parts = new Intl.DateTimeFormat(loc, { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" })
      .formatToParts(new Date(Date.UTC(2026, 10, 20)));
    var o = parts.map(function (p) { return p.type; }).filter(function (t) { return ORDER.indexOf(t) > -1; });
    if (o.length === 3) ORDER = o;
  } catch (e) {}
  if (FIX && FIX.o) ORDER = FIX.o;

  var MONTHS = [];
  for (var i = 0; i < 12; i++) MONTHS.push(FIX ? FIX.m[i] : cap(fmt(new Date(Date.UTC(2026, i, 15)), { month: "long" })) || String(i + 1));
  function num(n) { return fmt(new Date(Date.UTC(2026, 0, n)), { day: "numeric" }).replace(/\.$/, "") || String(n); }
  function yr(y) { return fmt(new Date(Date.UTC(y, 5, 15)), { year: "numeric" }).replace(/\.$/, "") || String(y); }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function dim(y, m) { return new Date(Date.UTC(y, m + 1, 0)).getUTCDate(); }
  function todayISO() { var n = new Date(Date.now() + 3 * 3600e3); return n.getUTCFullYear() + "-" + pad(n.getUTCMonth() + 1) + "-" + pad(n.getUTCDate()); }

  var css = ".dmy{display:flex;gap:6px;width:100%}.dmy select{flex:1 1 0;min-width:0;padding-left:8px!important;padding-right:8px!important}" +
    ".dmy select.dmy-month{flex:2.1 1 0}.dmy select.dmy-year{flex:1.2 1 0}" +
    ".ap-form .dmy select{padding-right:24px!important;background-position:calc(100% - 14px) 20px,calc(100% - 9px) 20px}" +
    "html[dir=rtl] .ap-form .dmy select{padding-right:8px!important;padding-left:24px!important;background-position:14px 20px,9px 20px}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function build(inp) {
    if (inp.dataset.dmy) return; inp.dataset.dmy = "1";
    var wrap = document.createElement("div"); wrap.className = "dmy"; wrap.dir = rtl ? "rtl" : "ltr";
    var S = {};
    ORDER.forEach(function (k) {
      var s = document.createElement("select"); s.className = "dmy-" + k; s.setAttribute("aria-label", LBL[k]);
      S[k] = s; wrap.appendChild(s);
    });
    inp.parentNode.insertBefore(wrap, inp.nextSibling);
    var box = inp.closest(".ap-form > *"); if (box) box.style.gridColumn = "1 / -1";  // full row in the airport form
    var wasRequired = inp.required;
    inp.type = "hidden";
    if (inp.id) { var l = document.querySelector('label[for="' + inp.id + '"]'); if (l) l.htmlFor = ""; }
    inp.focus = function () { (S.day.value ? (S.month.value ? S.year : S.month) : S.day).focus(); };

    function minParts() {
      var m = (inp.getAttribute("min") || inp.min || todayISO()).split("-");
      return { y: +m[0], m: +m[1] - 1, d: +m[2] };
    }
    function opts(s, list, val) {
      s.innerHTML = "";
      list.forEach(function (it) {
        var o = document.createElement("option"); o.value = it[0]; o.textContent = it[1];
        if (it[2]) o.disabled = true; s.appendChild(o);
      });
      s.value = val;
      if (s.value !== val || (s.selectedOptions[0] && s.selectedOptions[0].disabled)) s.value = "";
    }
    function render(y, m, d) {
      var mn = minParts(), ys = [["", LBL.year]];
      for (var k = mn.y; k <= mn.y + 2; k++) ys.push([String(k), yr(k)]);
      opts(S.year, ys, y);
      var Y = +S.year.value, ms = [["", LBL.month]];
      MONTHS.forEach(function (name, idx) { ms.push([String(idx), name, Y && Y === mn.y && idx < mn.m]); });
      opts(S.month, ms, m);
      var M = S.month.value === "" ? -1 : +S.month.value;
      var n = (Y && M > -1) ? dim(Y, M) : 31, ds = [["", LBL.day]];
      for (var j = 1; j <= n; j++) ds.push([String(j), num(j), Y === mn.y && M === mn.m && j < mn.d]);
      opts(S.day, ds, d);
    }
    var last = null;
    function sync(fire) {
      var v = (S.year.value && S.month.value !== "" && S.day.value)
        ? S.year.value + "-" + pad(+S.month.value + 1) + "-" + pad(+S.day.value) : "";
      if (inp.value !== v) inp.value = v;
      last = v;
      if (fire) { inp.dispatchEvent(new Event("input", { bubbles: true })); inp.dispatchEvent(new Event("change", { bubbles: true })); }
    }
    function fromValue() {
      var v = inp.value, p = v ? v.split("-") : null;
      if (p && p.length === 3) render(p[0], String(+p[1] - 1), String(+p[2]));
      else render(S.year.value, S.month.value, "");
      sync(false);
    }
    ORDER.forEach(function (k) {
      S[k].addEventListener("change", function () {
        render(S.year.value, S.month.value, S.day.value);
        sync(true);
      });
    });
    // follow programmatic changes to min / value made by the page's own scripts
    new MutationObserver(function () {
      if (inp.value !== last) { fromValue(); return; }   // value set/cleared by another script
      var before = last;                                  // min changed: re-check the chosen date
      render(S.year.value, S.month.value, S.day.value);
      sync(false);
      if (last !== before) sync(true);
    }).observe(inp, { attributes: true, attributeFilter: ["min", "value"] });
    fromValue();
  }

  // Georgian: some browsers lack Georgian date names, so the group-departure dates
  // fell back to English — write them in Georgian here.
  function kaDates() {
    if (lang.split("-")[0] !== "ka" || !FIX) return;
    var WD = ["კვირა", "ორშაბათი", "სამშაბათი", "ოთხშაბათი", "ხუთშაბათი", "პარასკევი", "შაბათი"];
    function d(iso) { var p = iso.split("-"); return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); }
    function full(x) { return WD[x.getUTCDay()] + ", " + x.getUTCDate() + " " + FIX.m[x.getUTCMonth()] + ", " + x.getUTCFullYear(); }
    var sel = document.getElementById("f-date");
    function opts() {
      if (!sel) return;
      [].forEach.call(sel.options, function (o) { var m = /^(\d{4}-\d{2}-\d{2})/.exec(o.value); if (m) { var t = full(d(m[1])); if (o.textContent !== t) o.textContent = t; } });
    }
    if (sel) { opts(); new MutationObserver(opts).observe(sel, { childList: true }); }
    document.querySelectorAll(".grp-dates .gd").forEach(function (c) {
      var b = c.querySelector("button[data-date]"); if (!b) return; var x = d(b.dataset.date);
      var m = c.querySelector(".gd-m"), w = c.querySelector(".gd-w");
      if (m) m.textContent = FIX.m[x.getUTCMonth()] + " " + x.getUTCFullYear();
      if (w) w.textContent = WD[x.getUTCDay()];
    });
  }

  function run() { document.querySelectorAll('input[type="date"]').forEach(build); kaDates(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
