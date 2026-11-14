/* Arabic affiliate and admin screens. Talks only to the public Supabase key. */
(function () {
  "use strict";

  var CFG = window.FT_AFFILIATE_CONFIG || {};
  var STATUS = { pending: "مبدئي", confirmed: "مؤكد", cancelled: "ملغي" };
  var SPONSOR_MS = 10 * 365 * 24 * 60 * 60 * 1000;

  function normSponsor(raw) {
    if (raw == null) return "";
    var code = String(raw).trim().toUpperCase();
    return /^[A-Z0-9]{4,12}$/.test(code) ? code : "";
  }
  function readCookie(name) {
    var parts = String(document.cookie || "").split(";");
    var i, bit;
    for (i = 0; i < parts.length; i++) {
      bit = parts[i].replace(/^\s+/, "");
      if (bit.indexOf(name + "=") === 0) return decodeURIComponent(bit.slice(name.length + 1));
    }
    return "";
  }
  function parseSponsor(raw, now) {
    if (!raw) return null;
    var text = String(raw).trim();
    var dot = text.lastIndexOf(".");
    if (dot > 0) {
      var code = normSponsor(text.slice(0, dot));
      var exp = parseInt(text.slice(dot + 1), 10);
      if (!code || !exp || now > exp) return null;
      return { code: code, exp: exp };
    }
    var legacy = normSponsor(text);
    return legacy ? { code: legacy, exp: now + SPONSOR_MS } : null;
  }
  function writeSponsor(code, exp) {
    var bag = code + "." + exp;
    var maxAge = Math.max(0, Math.round((exp - Date.now()) / 1000));
    var secure = location.protocol === "https:" ? "; Secure" : "";
    document.cookie = "ft_sponsor=" + encodeURIComponent(bag) + "; Max-Age=" + maxAge + "; Path=/; SameSite=Lax" + secure;
    try { localStorage.setItem("ft_sponsor", bag); } catch (e) {}
  }
  function currentSponsor() {
    var now = Date.now();
    var cookie = "", storage = "";
    try { cookie = readCookie("ft_sponsor"); } catch (e) {}
    try { storage = localStorage.getItem("ft_sponsor") || ""; } catch (e) {}
    var bag = parseSponsor(cookie, now) || parseSponsor(storage, now);
    return bag ? bag.code : "";
  }
  function captureSponsor() {
    var now = Date.now();
    var query = "";
    try { query = normSponsor(new URLSearchParams(location.search).get("sponsor")); } catch (e) {}
    if (query) { writeSponsor(query, now + SPONSOR_MS); return; }
    var cookie = "", storage = "";
    try { cookie = readCookie("ft_sponsor"); } catch (e) {}
    try { storage = localStorage.getItem("ft_sponsor") || ""; } catch (e) {}
    var bag = parseSponsor(cookie, now) || parseSponsor(storage, now);
    if (bag && storage !== bag.code + "." + bag.exp) writeSponsor(bag.code, bag.exp);
  }
  function missingFeature(error) {
    var message = ((error && (error.message || error.details || error.hint)) || "") + "";
    var code = (error && error.code) || "";
    return code === "PGRST202" || code === "42883" || code === "42P01" || code === "42703" || /schema cache|could not find|does not exist|aff_my_team|aff_confirm_booking|aff_commissions|sponsor_id/i.test(message);
  }

var MSG = {
  keys: "مفاتيح Supabase غير موجودة في الملف affiliate/config.js. الصق رابط المشروع والمفتاح العام ثم أعد نشر الموقع.",
  library: "تعذّر تحميل مكتبة الاتصال من الموقع نفسه. حدّث الصفحة بقوة. إذا استمر العطل فالمتصفح يمنع الملف /affiliate/vendor/supabase.js.",
  network: "تعذّر الاتصال بخادم Supabase. تحقق من الإنترنت، وأن المشروع غير متوقف.",
  badLogin: "البريد أو كلمة المرور غير صحيحة.",
  already: "هذا البريد مسجّل مسبقاً. انتقل إلى تسجيل الدخول.",
  short: "كلمة المرور قصيرة. استخدم 6 أحرف على الأقل.",
  mismatch: "كلمتا المرور غير متطابقتين.",
  badEmail: "البريد الإلكتروني غير صحيح.",
  db: "قاعدة البيانات غير جاهزة أو الحساب ليس مديراً. نفّذ ملف SQL كما في دليل الإعداد.",
  generic: "حدث خطأ. حاول مرة أخرى.",
  badForm: "يرجى كتابة الاسم ورقم واتساب وبريد صحيح.",
  suCreating: "جارٍ إنشاء الحساب…",
  suCreated: "أُنشئ الحساب. افتح رسالة البريد لتأكيده ثم سجّل الدخول. لبدء العمل فوراً أوقف تأكيد البريد كما في دليل الإعداد.",
  suNoRow: "تم الدخول، لكن صف الشريك غير موجود. نفّذ ملف SQL في Supabase ثم حدّث الصفحة.",
  suSubmit: "إنشاء الحساب",
  needBoth: "اكتب البريد وكلمة المرور.",
  liEntering: "جارٍ الدخول…",
  liSubmit: "دخول",
  hello: "مرحباً، {name}. هذا رابطك وحجوزات الزوار الذين دخلوا عن طريقه.",
  copied: "تم النسخ",
  copyFail: "انسخ الرابط يدوياً",
  empty: "لا توجد حجوزات بعد.",
  stPending: "مبدئي",
  stConfirmed: "مؤكد",
  stCancelled: "ملغي"
};

function keysOk() {
  var cfg = window.FT_AFFILIATE_CONFIG || CFG;
  if (!cfg || !cfg.supabaseUrl || !cfg.supabaseKey) return false;
  if (/YOUR_/i.test(String(cfg.supabaseUrl)) || /YOUR_/i.test(String(cfg.supabaseKey))) return false;
  return /^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/i.test(cfg.supabaseUrl) && String(cfg.supabaseKey).length > 20;
}

function hasLib() {
  return !!(window.supabase && typeof window.supabase.createClient === "function");
}

function problem() {
  if (!keysOk()) return "keys";
  if (!hasLib()) return "library";
  return "";
}

function isAdmin() {
  return !!(document.body && document.body.getAttribute("data-page") === "admin");
}

function t(key) {
  if (!isAdmin() && window.FT_UI) return window.FT_UI.t(key);
  return MSG[key] || key;
}

function showProblem(id, code) {
  var text = t(code) || MSG.network;
  if (id === "gate") {
    var gate = document.getElementById("gate");
    if (!gate) return;
    gate.hidden = false;
    gate.textContent = text;
    return;
  }
  show(id, text, "err");
}

function ensureLib(done) {
  if (hasLib()) { done(true); return; }
  var finished = false;
  function finish(ok) {
    if (finished) return;
    finished = true;
    done(!!ok && hasLib());
  }
  var script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.49.1/dist/umd/supabase.js";
  script.async = true;
  script.onload = function () { finish(true); };
  script.onerror = function () { finish(false); };
  document.head.appendChild(script);
  setTimeout(function () { finish(false); }, 8000);
}

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function money(value) {
    if (value == null || value === "") return "—";
    var number = Number(value);
    if (!isFinite(number)) return "—";
    return "$" + number.toLocaleString("en-US", { maximumFractionDigits: 2 });
  }

  function when(iso) {
    if (!iso) return "—";
    var loc = "ar";
    if (!isAdmin() && window.FT_UI) loc = window.FT_UI.lang() || "ar";
    if (loc === "zh-tw") loc = "zh-TW";
    try {
      return new Intl.DateTimeFormat(loc, { dateStyle: "medium", timeStyle: "short" }).format(new Date(iso));
    } catch (e) {
      return String(iso).replace("T", " ").slice(0, 16);
    }
  }

  function human(error) {
    var message = (error && (error.message || error.error_description || error.details) || "") + "";
    if (/invalid login|invalid credentials/i.test(message)) return t("badLogin");
    if (/already registered|already been registered|user already/i.test(message)) return t("already");
    if (/password/i.test(message)) return t("short");
    if (/email/i.test(message) && /invalid|valid/i.test(message)) return t("badEmail");
    if (/fetch|network|failed to fetch|load failed|timeout/i.test(message)) return t("network");
    if (/relation|schema|function|permission|not found|pgrst|42501|jwt/i.test(message)) return t("db");
    return t("generic");
  }

  function client() {
    return window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseKey, {
      auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
    });
  }

  function linkFor(code) {
    var origin = String(CFG.siteOrigin || "https://iraq.fabletour.com").replace(/\/$/, "");
    return origin + "/?ref=" + encodeURIComponent(code);
  }

  function totals(list) {
    var sum = { all: list.length, pending: 0, confirmed: 0, cancelled: 0, commission: 0 };
    list.forEach(function (row) {
      if (sum[row.status] != null) sum[row.status] += 1;
      if (row.status === "confirmed" && row.commission != null) sum.commission += Number(row.commission) || 0;
    });
    return sum;
  }

  function paintStats(sum, clicks) {
    var map = {
      "n-clicks": clicks,
      "n-all": sum.all,
      "n-pending": sum.pending,
      "n-ok": sum.confirmed,
      "n-no": sum.cancelled,
      "n-money": money(sum.commission)
    };
    Object.keys(map).forEach(function (id) {
      var node = document.getElementById(id);
      if (node) node.textContent = map[id];
    });
  }

  function bookingRows(list, names, admin) {
    var cols = admin ? 9 : 7;
    if (!list.length) {
      var empty = admin ? "لا توجد حجوزات بعد." : t("empty");
      return '<tr><td class="empty" colspan="' + cols + '">' + esc(empty) + "</td></tr>";
    }
    return list.map(function (row) {
      var people = row.people ? esc(row.people) : "—";
      var who = names && names[row.affiliate_id] ? '<span class="who">' + esc(names[row.affiliate_id]) + "</span>" : "";
      var actions = "";
      if (admin) {
        var commission = row.commission == null ? "" : String(row.commission);
        actions = '<td><div class="act">' +
          '<input class="comm" type="number" min="0" step="0.01" inputmode="decimal" placeholder="قيمة الحجز $" value="' + esc(row.amount != null ? row.amount : "") + '" aria-label="قيمة الحجز">' +
          '<button class="btn slim" type="button" data-act="confirmed" data-id="' + esc(row.id) + '">تأكيد</button>' +
          '<button class="btn slim quiet" type="button" data-act="cancelled" data-id="' + esc(row.id) + '">رفض</button>' +
          (row.status === "pending" ? "" : '<button class="btn slim quiet" type="button" data-act="pending" data-id="' + esc(row.id) + '">إرجاع</button>') +
          "</div></td>";
      }
      return "<tr data-status=\"" + esc(row.status) + "\">" +
        "<td>" + esc(when(row.created_at)) + "</td>" +
        "<td>" + esc(row.customer_name) + who + "<span class=\"who\" dir=\"ltr\">" + esc(row.customer_email || "") + "</span></td>" +
        "<td dir=\"ltr\">" + esc(row.customer_phone || "—") + "</td>" +
        "<td>" + esc(row.program || "—") + "</td>" +
        "<td>" + esc(row.travel_date || "—") + "</td>" +
        "<td>" + people + "</td>" +
        "<td><span class=\"badge " + esc(row.status) + "\">" + esc(admin ? (STATUS[row.status] || row.status) : t({ pending: "stPending", confirmed: "stConfirmed", cancelled: "stCancelled" }[row.status] || "stPending")) + "</span>" +
          (row.status === "confirmed" ? '<span class="who">' + esc(money(row.commission)) + "</span>" : "") + "</td>" +
        (admin ? '<td class="split" data-split="' + esc(row.id) + '"></td>' : "") +
        actions +
        "</tr>";
    }).join("");
  }

  function sample() {
    var affiliates = [
      { id: "a1", full_name: "أحمد كريم", phone: "+9647701234567", email: "ahmad@example.com", referral_code: "A7K3QM", is_admin: false, sponsor_id: null, sponsor_name: null, sponsor_code: null, created_at: "2026-10-02T09:00:00Z", clicks: 18, bookings: 1, confirmed: 1, commission: 250 },
      { id: "a2", full_name: "سارة محمد", phone: "+9647809876543", email: "sara@example.com", referral_code: "S4M8PL", is_admin: false, sponsor_id: "a1", sponsor_name: "أحمد كريم", sponsor_code: "A7K3QM", created_at: "2026-11-01T12:30:00Z", clicks: 7, bookings: 1, confirmed: 0, commission: 0 },
      { id: "a3", full_name: "ليلى كريم", phone: "+9647901122334", email: "layla.k@example.com", referral_code: "L2K9RT", is_admin: false, sponsor_id: "a2", sponsor_name: "سارة محمد", sponsor_code: "S4M8PL", created_at: "2026-11-10T08:00:00Z", clicks: 4, bookings: 2, confirmed: 1, commission: 100 }
    ];
    var bookings = [
      { id: "b1", affiliate_id: "a1", customer_name: "علي حسين", customer_phone: "+9647501112233", customer_email: "ali@example.com", program: "رحلة التراث العراقي: 7 أيام / 6 ليالٍ — $2,500", travel_date: "2026-12-20", people: "4", language: "ar", page_url: "/", status: "pending", amount: null, commission: null, created_at: "2026-11-12T14:05:00Z" },
      { id: "b2", affiliate_id: "a1", customer_name: "ليلى أحمد", customer_phone: "+9647510009988", customer_email: "layla@example.com", program: "العراق كله من البصرة إلى أربيل: 9 أيام / 8 ليالٍ — $3,400", travel_date: "الجمعة، 4 ديسمبر 2026", people: "—", language: "ar", page_url: "/tours/iraq-9-day-tour/", status: "confirmed", amount: 2500, commission: 250, created_at: "2026-11-08T10:20:00Z" },
      { id: "b4", affiliate_id: "a3", customer_name: "نورا سعيد", customer_phone: "+9647705556677", customer_email: "nora@example.com", program: "رحلة التراث العراقي: 7 أيام / 6 ليالٍ — $2,500", travel_date: "2026-12-04", people: "2", language: "ar", page_url: "/", status: "confirmed", amount: 2000, commission: 100, created_at: "2026-11-11T09:00:00Z" },
      { id: "b5", affiliate_id: "a3", customer_name: "هدى جاسم", customer_phone: "+9647718889900", customer_email: "huda@example.com", program: "رحلة بغداد وبابل وسامراء: 6 أيام / 5 ليالٍ — $1,200", travel_date: "2027-01-08", people: "2", language: "ar", page_url: "/", status: "pending", amount: 1000, commission: null, created_at: "2026-11-13T11:00:00Z" }
    ];
    var commissions = [
      { booking_id: "b2", affiliate_id: "a1", level: 0, rate: 0.1, amount: 250, status: "confirmed" },
      { booking_id: "b4", affiliate_id: "a3", level: 0, rate: 0.05, amount: 100, status: "confirmed" },
      { booking_id: "b4", affiliate_id: "a2", level: 1, rate: 0.025, amount: 50, status: "confirmed" },
      { booking_id: "b4", affiliate_id: "a1", level: 2, rate: 0.025, amount: 50, status: "confirmed" },
      { booking_id: "b5", affiliate_id: "a3", level: 0, rate: 0.05, amount: 50, status: "pending" },
      { booking_id: "b5", affiliate_id: "a2", level: 1, rate: 0.025, amount: 25, status: "pending" },
      { booking_id: "b5", affiliate_id: "a1", level: 2, rate: 0.025, amount: 25, status: "pending" }
    ];
    return { affiliates: affiliates, bookings: bookings, commissions: commissions, me: affiliates[0] };
  }

  function copyLink(button, text) {
    function done(ok) {
      var previous = button.textContent;
      button.textContent = ok ? t("copied") : t("copyFail");
      button.classList.toggle("ok", ok);
      setTimeout(function () { button.textContent = previous; button.classList.remove("ok"); }, 2200);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { fallback(); });
    } else fallback();
    function fallback() {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.cssText = "position:fixed;top:0;opacity:0";
      document.body.appendChild(area);
      area.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) {}
      area.remove();
      done(ok);
    }
  }

  function show(id, text, kind) {
    var node = document.getElementById(id);
    if (!node) return;
    node.textContent = text || "";
    node.className = kind ? (node.classList.contains("msg") ? "msg " + kind : "flash " + kind) : (node.classList.contains("msg") ? "msg" : "flash");
  }

  function bindSignup(sb) {
    var form = document.getElementById("join");
    form.dataset.ready = "1";
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var name = form.name.value.trim();
      var phone = form.phone.value.trim();
      var email = form.email.value.trim();
      var password = form.password.value;
      var again = form.again.value;
      if (!name || phone.replace(/\D/g, "").length < 8 || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        show("f-msg", t("badForm"), "err");
        return;
      }
      if (password.length < 6) {
        show("f-msg", t("short"), "err");
        return;
      }
      if (password !== again) {
        show("f-msg", t("mismatch"), "err");
        return;
      }
      if (!keysOk()) { showProblem("f-msg", "keys"); return; }
      if (!sb || !hasLib()) { showProblem("f-msg", "library"); return; }
      var button = document.getElementById("f-btn");
      button.disabled = true;
      button.textContent = t("suCreating");
      sb.auth.signUp({
        email: email,
        password: password,
        options: {
          data: { full_name: name, phone: phone, sponsor: currentSponsor() || undefined },
          emailRedirectTo: location.origin + "/affiliate/login.html"
        }
      }).then(function (result) {
        if (result.error) throw result.error;
        if (!result.data.session) {
          show("f-msg", t("suCreated"), "ok");
          button.disabled = false;
          button.textContent = t("suSubmit");
          return;
        }
        return sb.rpc("aff_ensure_affiliate").then(function (made) {
          if (made.error || !made.data) {
            show("f-msg", t("suNoRow"), "err");
            button.disabled = false;
            button.textContent = t("suSubmit");
            return;
          }
          location.href = "dashboard.html";
        });
      }).catch(function (error) {
        show("f-msg", human(error), "err");
        button.disabled = false;
        button.textContent = t("suSubmit");
      });
    });
  }

  function bindForgot(sb) {
    var button = document.getElementById("forgot");
    if (!button || !window.FT_PW) return;
    button.addEventListener("click", function () {
      var emailEl = document.getElementById("f-email");
      var email = emailEl ? emailEl.value.trim() : "";
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        show("f-msg", window.FT_PW.t("needEmail"), "err");
        if (emailEl) emailEl.focus();
        return;
      }
      if (!keysOk()) { showProblem("f-msg", "keys"); return; }
      if (!sb || !hasLib()) { showProblem("f-msg", "library"); return; }
      button.disabled = true;
      sb.auth.resetPasswordForEmail(email, { redirectTo: window.FT_PW.REDIRECT }).then(function (result) {
        if (result.error) throw result.error;
        show("f-msg", window.FT_PW.t("sent"), "ok");
      }).catch(function (error) {
        show("f-msg", human(error), "err");
      }).then(function () { button.disabled = false; });
    });
  }

  function bindReset(sb) {
    var form = document.getElementById("join");
    var wait = document.getElementById("reset-wait");
    if (!form) return;
    form.dataset.ready = "1";
    var saw = false;
    function arm(session) {
      if (!session) return;
      saw = true;
      if (wait) wait.hidden = true;
      form.hidden = false;
    }
    if (sb) {
      sb.auth.onAuthStateChange(function (event, session) {
        if (event === "PASSWORD_RECOVERY" || event === "SIGNED_IN" || event === "INITIAL_SESSION" || event === "TOKEN_REFRESHED") arm(session);
      });
      sb.auth.getSession().then(function (result) { arm(result.data.session); }).catch(function () {});
    }
    setTimeout(function () {
      if (saw) return;
      if (wait) wait.hidden = true;
      show("f-msg", window.FT_PW ? window.FT_PW.t("expired") : "", "err");
    }, 8000);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var password = form.password.value;
      var again = form.again.value;
      if (password.length < 6) { show("f-msg", window.FT_PW.t("short"), "err"); return; }
      if (password !== again) { show("f-msg", window.FT_PW.t("mismatch"), "err"); return; }
      if (!sb) { showProblem("f-msg", "library"); return; }
      var button = document.getElementById("f-btn");
      button.disabled = true;
      button.textContent = window.FT_PW.t("saving");
      sb.auth.updateUser({ password: password }).then(function (result) {
        if (result.error) throw result.error;
        show("f-msg", window.FT_PW.t("done"), "ok");
        setTimeout(function () { location.href = "dashboard.html"; }, 700);
      }).catch(function (error) {
        show("f-msg", human(error), "err");
        button.disabled = false;
        button.textContent = window.FT_PW.t("save");
      });
    });
  }

  function bindLogin(sb) {
    var form = document.getElementById("join");
    form.dataset.ready = "1";
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var email = form.email.value.trim();
      var password = form.password.value;
      if (!email || !password) {
        show("f-msg", t("needBoth"), "err");
        return;
      }
      if (!keysOk()) { showProblem("f-msg", "keys"); return; }
      if (!sb || !hasLib()) { showProblem("f-msg", "library"); return; }
      var button = document.getElementById("f-btn");
      button.disabled = true;
      button.textContent = t("liEntering");
      sb.auth.signInWithPassword({ email: email, password: password }).then(function (result) {
        if (result.error) throw result.error;
        var next = new URLSearchParams(location.search).get("next");
        location.href = next === "admin" ? "admin.html" : "dashboard.html";
      }).catch(function (error) {
        show("f-msg", human(error), "err");
        button.disabled = false;
        button.textContent = t("liSubmit");
      });
    });
    bindForgot(sb);
  }

  var dashCache = null;
  function drawDashboard(me, clicks, bookings) {
    dashCache = { me: me, clicks: clicks, bookings: bookings };
    var app = document.getElementById("app");
    app.hidden = false;
    var hello = document.getElementById("hello");
    if (hello) hello.textContent = t("hello").replace("{name}", me.full_name);
    var url = linkFor(me.referral_code);
    document.getElementById("ref-link").textContent = url;
    var copy = document.getElementById("copy");
    copy.onclick = function () { copyLink(copy, url); };
    paintStats(totals(bookings), clicks);
    document.getElementById("rows").innerHTML = bookingRows(bookings, null, false);
    if (window.FTTeam) {
      var origin = String(CFG.siteOrigin || "https://iraq.fabletour.com").replace(/\/$/, "");
      FTTeam.setLink(origin + "/affiliate/?sponsor=" + encodeURIComponent(me.referral_code));
    }
    if (window.FTMaterials) window.FTMaterials.show(me.referral_code);
  }

  function paintSplits(rows, names) {
    document.querySelectorAll("[data-split]").forEach(function (cell) {
      var id = cell.getAttribute("data-split");
      var mine = (rows || []).filter(function (row) { return row.booking_id === id; });
      mine.sort(function (a, b) { return a.level - b.level; });
      if (!mine.length) { cell.textContent = "—"; return; }
      cell.innerHTML = mine.map(function (row) {
        var who = names[row.affiliate_id] || "";
        var label = row.level === 0 ? "البائع" : row.level === 1 ? "الراعي" : "الأعلى";
        var pct = Math.round(Number(row.rate) * 1000) / 10;
        return "<div><b>" + esc(label) + "</b> " + esc(who) + " · " + esc(money(row.amount)) + ' <span class="who" dir="ltr">' + esc(pct) + "%</span></div>";
      }).join("");
    });
  }

  function legacyShare(amount) {
    if (amount == null || amount === "") return null;
    var number = Number(amount);
    if (!isFinite(number)) return null;
    return Math.round(number * 10) / 100;
  }
  function saveBooking(sb, id, status, amount) {
    return sb.rpc("aff_confirm_booking", { p_id: id, p_status: status, p_amount: amount }).then(function (result) {
      if (result.error && missingFeature(result.error)) {
        return sb.rpc("aff_set_booking_status", {
          p_id: id,
          p_status: status,
          p_commission: status === "confirmed" ? legacyShare(amount) : null
        });
      }
      if (result.error) throw result.error;
      return result;
    });
  }
  function loadTeam(sb, me) {
    if (!window.FTTeam) return;
    sb.rpc("aff_my_team").then(function (team) {
      if (team.error) {
        if (missingFeature(team.error)) { FTTeam.unavailable(); return null; }
        throw team.error;
      }
      FTTeam.showTeam(team.data || []);
      return sb.from("aff_commissions").select("level,amount,status").eq("affiliate_id", me.id);
    }).then(function (pay) {
      if (!pay) return;
      if (pay.error) {
        if (missingFeature(pay.error)) FTTeam.unavailable();
        return;
      }
      var sum = sumEarnings(pay.data || []);
      FTTeam.showEarnings(sum.ownP, sum.ownC, sum.teamP, sum.teamC);
    }).catch(function (error) {
      if (missingFeature(error) && window.FTTeam) FTTeam.unavailable();
    });
  }
  function sumEarnings(rows) {
    var out = { ownP: 0, ownC: 0, teamP: 0, teamC: 0 };
    (rows || []).forEach(function (row) {
      var n = Number(row.amount) || 0;
      var own = Number(row.level) === 0;
      if (row.status === "confirmed") { if (own) out.ownC += n; else out.teamC += n; }
      else if (row.status === "pending") { if (own) out.ownP += n; else out.teamP += n; }
    });
    return out;
  }

  function drawAdmin(affiliates, bookings, splits) {
    var app = document.getElementById("app");
    app.hidden = false;
    var clicks = 0;
    var names = {};
    affiliates.forEach(function (row) {
      clicks += Number(row.clicks) || 0;
      names[row.id] = row.full_name;
    });
    var sum = totals(bookings);
    var paid = sum.commission;
    if (splits && splits.length) {
      paid = splits.reduce(function (acc, row) {
        return acc + (row.status === "confirmed" ? Number(row.amount) || 0 : 0);
      }, 0);
    }
    var nodes = {
      "a-partners": affiliates.length,
      "a-clicks": clicks,
      "a-ok": sum.confirmed,
      "a-money": money(paid)
    };
    Object.keys(nodes).forEach(function (id) {
      var node = document.getElementById(id);
      if (node) node.textContent = nodes[id];
    });
    document.getElementById("aff-rows").innerHTML = affiliates.length ? affiliates.map(function (row) {
      return "<tr><td>" + esc(row.full_name) + (row.is_admin ? ' <span class="badge confirmed">مدير</span>' : "") +
        "<span class=\"who\" dir=\"ltr\">" + esc(row.email) + "</span></td>" +
        "<td dir=\"ltr\">" + esc(row.phone || "—") + "</td>" +
        "<td dir=\"ltr\">" + esc(row.referral_code) + "</td>" +
        "<td>" + (row.sponsor_code ? esc(row.sponsor_name || "—") + ' <span class="who" dir="ltr">' + esc(row.sponsor_code) + "</span>" : "—") + "</td>" +
        "<td class=\"num\">" + esc(row.clicks) + "</td>" +
        "<td class=\"num\">" + esc(row.bookings) + "</td>" +
        "<td class=\"num\">" + esc(row.confirmed) + "</td>" +
        "<td class=\"num\">" + esc(money(row.commission)) + "</td>" +
        "<td>" + esc(when(row.created_at)) + "</td></tr>";
    }).join("") : '<tr><td class="empty" colspan="9">لا يوجد شركاء بعد.</td></tr>';
    document.getElementById("rows").innerHTML = bookingRows(bookings, names, true);
    paintSplits(splits, names);
  }

  function bindAdminActions(apply) {
    var body = document.getElementById("rows");
    body.addEventListener("click", function (event) {
      var button = event.target.closest("[data-act]");
      if (!button) return;
      var status = button.getAttribute("data-act");
      var id = button.getAttribute("data-id");
      var row = button.closest("tr");
      var input = row ? row.querySelector(".comm") : null;
      var commission = null;
      if (status === "confirmed") {
        var raw = input ? input.value.trim() : "";
        if (raw !== "") {
          commission = Number(raw);
          if (!isFinite(commission) || commission < 0) {
            show("act-msg", "اكتب قيمة الحجز صفراً أو أكثر، أو اترك الحقل فارغاً.", "err");
            return;
          }
        }
      }
      if (status === "cancelled" && !window.confirm("رفض هذا الحجز؟")) return;
      if (status === "pending" && !window.confirm("إرجاع الحجز إلى مبدئي؟")) return;
      button.disabled = true;
      Promise.resolve(apply(id, status, commission)).then(function () {
        show("act-msg", "تم تحديث الحالة.", "ok");
      }).catch(function (error) {
        show("act-msg", human(error), "err");
        button.disabled = false;
      });
    });
  }

  function logout(sb) {
    var button = document.getElementById("logout");
    if (!button) return;
    button.addEventListener("click", function () {
      var done = function () { location.href = "login.html"; };
      if (!sb) { done(); return; }
      sb.auth.signOut().then(done, done);
    });
  }

  function watch(sb, reload) {
    function quiet() {
      var el = document.activeElement;
      if (el && el.classList && el.classList.contains("comm")) return;
      reload();
    }
    window.addEventListener("focus", quiet);
    try {
      sb.channel("aff-booking-status")
        .on("postgres_changes", { event: "*", schema: "public", table: "aff_bookings" }, quiet)
        .subscribe();
    } catch (e) {}
  }

  function start() {
    captureSponsor();
    var page = document.body.getAttribute("data-page");
    if (page !== "reset" && window.FT_PW && window.FT_PW.isRecovery()) {
      location.replace("/affiliate/reset.html" + location.search + location.hash);
      return;
    }
    var preview = new URLSearchParams(location.search).get("preview") === "1";
    var lang = document.getElementById("langSel");
    if (lang && page !== "admin") lang.addEventListener("change", function () {
      if (window.FT_UI) window.FT_UI.apply(lang.value, true);
      if (window.FT_PW) window.FT_PW.apply(lang.value, false);
      if (window.FTMaterials) window.FTMaterials.apply(lang.value, false);
      if (window.FTTeam) window.FTTeam.apply();
      if (dashCache) drawDashboard(dashCache.me, dashCache.clicks, dashCache.bookings);
    });

    function connect(then) {
      if (!keysOk()) { then(null, "keys"); return; }
      ensureLib(function (ok) {
        if (!ok) { then(null, "library"); return; }
        try { then(client(), ""); }
        catch (e) { then(null, "library"); }
      });
    }

    if (page === "reset") {
      connect(function (sb) { bindReset(sb); });
      return;
    }

    if (page === "signup" || page === "login") {
      connect(function (sb, code) {
        if (page === "signup") bindSignup(sb);
        else bindLogin(sb);
        if (code) return;
        sb.auth.getSession().then(function (result) {
          if (!result.data.session) return;
          if (page === "signup") { location.href = "dashboard.html"; return; }
          var next = new URLSearchParams(location.search).get("next");
          location.href = next === "admin" ? "admin.html" : "dashboard.html";
        }).catch(function () {});
      });
      return;
    }

    if (page === "materials") {
      connect(function (sb, code) {
        if (!sb) { showProblem("gate", code || "library"); return; }
        sb.auth.getSession().then(function (result) {
          var session = result.data.session;
          if (!session) { location.replace("login.html?next=materials"); return null; }
          return sb.from("aff_affiliates").select("referral_code,full_name").eq("id", session.user.id).maybeSingle();
        }).then(function (profile) {
          if (!profile) return;
          if (profile.error || !profile.data) {
            showProblem("gate", "keys");
            return;
          }
          if (window.FTMaterials) window.FTMaterials.show(profile.data.referral_code);
          logout(sb);
        }).catch(function (error) {
          var gate = document.getElementById("gate");
          if (gate) { gate.hidden = false; gate.textContent = human(error); }
        });
      });
      return;
    }

    if (page === "dashboard" && preview) {
      var demo = sample();
      document.getElementById("preview").hidden = false;
      drawDashboard(demo.me, demo.me.clicks, demo.bookings.filter(function (row) { return row.affiliate_id === demo.me.id; }));
      if (window.FTTeam) {
        var mine = demo.commissions.filter(function (row) { return row.affiliate_id === demo.me.id; });
        var earned = sumEarnings(mine);
        FTTeam.showTeam([
          { full_name: "سارة محمد", created_at: "2026-11-01T12:30:00Z", depth: 1, bookings: 1 },
          { full_name: "ليلى كريم", created_at: "2026-11-10T08:00:00Z", depth: 2, bookings: 2 }
        ]);
        FTTeam.showEarnings(earned.ownP, earned.ownC, earned.teamP, earned.teamC);
      }
      logout(null);
      return;
    }
    if (page === "admin" && preview) {
      var data = sample();
      document.getElementById("preview").hidden = false;
      drawAdmin(data.affiliates, data.bookings, data.commissions);
      bindAdminActions(function (id, status, amount) {
        data.bookings.forEach(function (row) {
          if (row.id !== id) return;
          row.status = status;
          row.amount = status === "pending" ? null : (status === "confirmed" ? amount : row.amount);
          row.commission = status === "confirmed" && amount != null ? legacyShare(amount) : null;
        });
        drawAdmin(data.affiliates, data.bookings, data.commissions);
      });
      logout(null);
      return;
    }

    connect(function (sb, code) {
    if (!sb) { showProblem("gate", code || "library"); return; }

    sb.auth.getSession().then(function (result) {
      var session = result.data.session;
      if (!session) {
        location.replace("login.html?next=" + (page === "admin" ? "admin" : "dashboard"));
        return;
      }
      if (page === "dashboard") {
        logout(sb);
        var load = function () {
          return sb.rpc("aff_ensure_affiliate").then(function (made) {
            if (made.error) throw made.error;
            return sb.from("aff_affiliates").select("*").eq("id", session.user.id).maybeSingle();
          }).then(function (profile) {
            if (profile.error) throw profile.error;
            if (!profile.data) throw new Error("relation aff_affiliates");
            return Promise.all([
              sb.from("aff_referral_clicks").select("id", { count: "exact", head: true }).eq("affiliate_id", session.user.id),
              sb.from("aff_bookings").select("*").eq("affiliate_id", session.user.id).order("created_at", { ascending: false })
            ]).then(function (parts) {
              if (parts[1].error) throw parts[1].error;
              drawDashboard(profile.data, parts[0].count || 0, parts[1].data || []);
              loadTeam(sb, profile.data);
              var adminLink = document.getElementById("admin-link");
              if (adminLink) adminLink.hidden = !profile.data.is_admin;
            });
          }).catch(function (error) {
            document.getElementById("gate").hidden = false;
            document.getElementById("gate").textContent = human(error);
          });
        };
        load();
        watch(sb, load);
        var refresh = document.getElementById("refresh");
        if (refresh) refresh.addEventListener("click", load);
        return;
      }
      logout(sb);
      var loadAdmin = function () {
        return sb.from("aff_affiliates").select("is_admin").eq("id", session.user.id).maybeSingle().then(function (me) {
          if (me.error) throw me.error;
          if (!me.data || !me.data.is_admin) {
            document.getElementById("gate").hidden = false;
            document.getElementById("gate").innerHTML = "هذه الصفحة لصاحب الموقع فقط. <a href=\"dashboard.html\">العودة إلى لوحتك</a>";
            return;
          }
          return Promise.all([
            sb.from("aff_affiliate_stats").select("*").order("created_at", { ascending: false }),
            sb.from("aff_bookings").select("*").order("created_at", { ascending: false }),
            sb.from("aff_commissions").select("booking_id,affiliate_id,level,rate,amount,status")
          ]).then(function (parts) {
            if (parts[0].error) throw parts[0].error;
            if (parts[1].error) throw parts[1].error;
            var splits = [];
            if (parts[2] && !parts[2].error) splits = parts[2].data || [];
            else if (parts[2] && parts[2].error && !missingFeature(parts[2].error)) throw parts[2].error;
            drawAdmin(parts[0].data || [], parts[1].data || [], splits);
          });
        }).catch(function (error) {
          document.getElementById("gate").hidden = false;
          document.getElementById("gate").textContent = human(error);
        });
      };
      bindAdminActions(function (id, status, commission) {
        return saveBooking(sb, id, status, commission).then(function (result) {
          if (result.error) throw result.error;
          return loadAdmin();
        });
      });
      loadAdmin();
      watch(sb, loadAdmin);
      var refreshAdmin = document.getElementById("refresh");
      if (refreshAdmin) refreshAdmin.addEventListener("click", loadAdmin);
    }).catch(function (error) {
      var gate = document.getElementById("gate");
      if (!gate) return;
      gate.hidden = false;
      gate.textContent = human(error);
    });
    });
  }

  window.FTAuth = { keysOk: keysOk, hasLib: hasLib, problem: problem, message: function (code) { return t(code) || ""; } };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
