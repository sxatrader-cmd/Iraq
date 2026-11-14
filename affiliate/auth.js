/* Arabic affiliate and admin screens. Talks only to the public Supabase key. */
(function () {
  "use strict";

  var CFG = window.FT_AFFILIATE_CONFIG || {};
  var STATUS = { pending: "مبدئي", confirmed: "مؤكد", cancelled: "ملغي" };

var MSG = {
  keys: "مفاتيح Supabase غير موجودة في الملف affiliate/config.js. الصق رابط المشروع والمفتاح العام ثم أعد نشر الموقع.",
  library: "تعذّر تحميل مكتبة الاتصال من الموقع نفسه. حدّث الصفحة بقوة. إذا استمر العطل فالمتصفح يمنع الملف /affiliate/vendor/supabase.js.",
  network: "تعذّر الاتصال بخادم Supabase. تحقق من الإنترنت، وأن المشروع غير متوقف."
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

function showProblem(id, code) {
  var text = MSG[code] || MSG.network;
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
    try {
      return new Intl.DateTimeFormat("ar-u-nu-latn", { dateStyle: "medium", timeStyle: "short" }).format(new Date(iso));
    } catch (e) {
      return String(iso).replace("T", " ").slice(0, 16);
    }
  }

  function human(error) {
    var message = (error && (error.message || error.error_description || error.details) || "") + "";
    if (/invalid login|invalid credentials/i.test(message)) return "البريد أو كلمة المرور غير صحيحة.";
    if (/already registered|already been registered|user already/i.test(message)) return "هذا البريد مسجّل مسبقاً. انتقل إلى تسجيل الدخول.";
    if (/password/i.test(message)) return "كلمة المرور قصيرة. استخدم 6 أحرف على الأقل.";
    if (/email/i.test(message) && /invalid|valid/i.test(message)) return "البريد الإلكتروني غير صحيح.";
    if (/fetch|network|failed to fetch|load failed|timeout/i.test(message)) return MSG.network;
    if (/relation|schema|function|permission|not found|pgrst|42501|jwt/i.test(message)) return "قاعدة البيانات غير جاهزة أو الحساب ليس مديراً. نفّذ ملف SQL كما في دليل الإعداد.";
    return "حدث خطأ. حاول مرة أخرى.";
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
    var cols = admin ? 8 : 7;
    if (!list.length) {
      return '<tr><td class="empty" colspan="' + cols + '">لا توجد حجوزات بعد.</td></tr>';
    }
    return list.map(function (row) {
      var people = row.people ? esc(row.people) : "—";
      var who = names && names[row.affiliate_id] ? '<span class="who">' + esc(names[row.affiliate_id]) + "</span>" : "";
      var actions = "";
      if (admin) {
        var commission = row.commission == null ? "" : String(row.commission);
        actions = '<td><div class="act">' +
          '<input class="comm" type="number" min="0" step="0.01" inputmode="decimal" placeholder="العمولة $" value="' + esc(commission) + '" aria-label="مبلغ العمولة">' +
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
        "<td><span class=\"badge " + esc(row.status) + "\">" + esc(STATUS[row.status] || row.status) + "</span>" +
          (row.status === "confirmed" ? '<span class="who">' + esc(money(row.commission)) + "</span>" : "") + "</td>" +
        actions +
        "</tr>";
    }).join("");
  }

  function sample() {
    var affiliates = [
      { id: "a1", full_name: "أحمد كريم", phone: "+9647701234567", email: "ahmad@example.com", referral_code: "A7K3QM", is_admin: false, created_at: "2026-10-02T09:00:00Z", clicks: 18, bookings: 2, confirmed: 1, commission: 150 },
      { id: "a2", full_name: "سارة محمد", phone: "+9647809876543", email: "sara@example.com", referral_code: "S4M8PL", is_admin: false, created_at: "2026-11-01T12:30:00Z", clicks: 7, bookings: 1, confirmed: 0, commission: 0 }
    ];
    var bookings = [
      { id: "b1", affiliate_id: "a1", customer_name: "علي حسين", customer_phone: "+9647501112233", customer_email: "ali@example.com", program: "رحلة التراث العراقي: 7 أيام / 6 ليالٍ — $2,500", travel_date: "2026-12-20", people: "4", language: "ar", page_url: "/", status: "pending", commission: null, created_at: "2026-11-12T14:05:00Z" },
      { id: "b2", affiliate_id: "a1", customer_name: "ليلى أحمد", customer_phone: "+9647510009988", customer_email: "layla@example.com", program: "العراق كله من البصرة إلى أربيل: 9 أيام / 8 ليالٍ — $3,400", travel_date: "الجمعة، 4 ديسمبر 2026", people: "—", language: "ar", page_url: "/tours/iraq-9-day-tour/", status: "confirmed", commission: 150, created_at: "2026-11-08T10:20:00Z" },
      { id: "b3", affiliate_id: "a2", customer_name: "جون سميث", customer_phone: "+447700900123", customer_email: "john@example.com", program: "رحلة بغداد وبابل وسامراء: 6 أيام / 5 ليالٍ — $1,200", travel_date: "2027-01-15", people: "2", language: "en", page_url: "/en/", status: "cancelled", commission: null, created_at: "2026-11-10T16:40:00Z" }
    ];
    return { affiliates: affiliates, bookings: bookings, me: affiliates[0] };
  }

  function copyLink(button, text) {
    function done(ok) {
      var previous = button.textContent;
      button.textContent = ok ? "تم النسخ" : "انسخ الرابط يدوياً";
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
        show("f-msg", "يرجى كتابة الاسم ورقم واتساب وبريد صحيح.", "err");
        return;
      }
      if (password.length < 6) {
        show("f-msg", "كلمة المرور قصيرة. استخدم 6 أحرف على الأقل.", "err");
        return;
      }
      if (password !== again) {
        show("f-msg", "كلمتا المرور غير متطابقتين.", "err");
        return;
      }
      if (!keysOk()) { showProblem("f-msg", "keys"); return; }
      if (!sb || !hasLib()) { showProblem("f-msg", "library"); return; }
      var button = document.getElementById("f-btn");
      button.disabled = true;
      button.textContent = "جارٍ إنشاء الحساب…";
      sb.auth.signUp({
        email: email,
        password: password,
        options: {
          data: { full_name: name, phone: phone },
          emailRedirectTo: location.origin + "/affiliate/login.html"
        }
      }).then(function (result) {
        if (result.error) throw result.error;
        if (!result.data.session) {
          show("f-msg", "أُنشئ الحساب. افتح رسالة البريد لتأكيده ثم سجّل الدخول. لبدء العمل فوراً أوقف تأكيد البريد كما في دليل الإعداد.", "ok");
          button.disabled = false;
          button.textContent = "إنشاء الحساب";
          return;
        }
        return sb.rpc("aff_ensure_affiliate").then(function (made) {
          if (made.error || !made.data) {
            show("f-msg", "تم الدخول، لكن صف الشريك غير موجود. نفّذ ملف SQL في Supabase ثم حدّث الصفحة.", "err");
            button.disabled = false;
            button.textContent = "إنشاء الحساب";
            return;
          }
          location.href = "dashboard.html";
        });
      }).catch(function (error) {
        show("f-msg", human(error), "err");
        button.disabled = false;
        button.textContent = "إنشاء الحساب";
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
        show("f-msg", "اكتب البريد وكلمة المرور.", "err");
        return;
      }
      if (!keysOk()) { showProblem("f-msg", "keys"); return; }
      if (!sb || !hasLib()) { showProblem("f-msg", "library"); return; }
      var button = document.getElementById("f-btn");
      button.disabled = true;
      button.textContent = "جارٍ الدخول…";
      sb.auth.signInWithPassword({ email: email, password: password }).then(function (result) {
        if (result.error) throw result.error;
        var next = new URLSearchParams(location.search).get("next");
        location.href = next === "admin" ? "admin.html" : "dashboard.html";
      }).catch(function (error) {
        show("f-msg", human(error), "err");
        button.disabled = false;
        button.textContent = "دخول";
      });
    });
    bindForgot(sb);
  }

  function drawDashboard(me, clicks, bookings) {
    var app = document.getElementById("app");
    app.hidden = false;
    var hello = document.getElementById("hello");
    if (hello) hello.textContent = "مرحباً، " + me.full_name + ". هذا رابطك وحجوزات الزوار الذين دخلوا عن طريقه.";
    var url = linkFor(me.referral_code);
    document.getElementById("ref-link").textContent = url;
    var copy = document.getElementById("copy");
    copy.onclick = function () { copyLink(copy, url); };
    paintStats(totals(bookings), clicks);
    document.getElementById("rows").innerHTML = bookingRows(bookings, null, false);
  }

  function drawAdmin(affiliates, bookings) {
    var app = document.getElementById("app");
    app.hidden = false;
    var clicks = 0;
    var names = {};
    affiliates.forEach(function (row) {
      clicks += Number(row.clicks) || 0;
      names[row.id] = row.full_name;
    });
    var sum = totals(bookings);
    var nodes = {
      "a-partners": affiliates.length,
      "a-clicks": clicks,
      "a-ok": sum.confirmed,
      "a-money": money(sum.commission)
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
        "<td class=\"num\">" + esc(row.clicks) + "</td>" +
        "<td class=\"num\">" + esc(row.bookings) + "</td>" +
        "<td class=\"num\">" + esc(row.confirmed) + "</td>" +
        "<td class=\"num\">" + esc(money(row.commission)) + "</td>" +
        "<td>" + esc(when(row.created_at)) + "</td></tr>";
    }).join("") : '<tr><td class="empty" colspan="8">لا يوجد شركاء بعد.</td></tr>';
    document.getElementById("rows").innerHTML = bookingRows(bookings, names, true);
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
            show("act-msg", "اكتب مبلغ عمولة صفراً أو أكثر، أو اترك الحقل فارغاً.", "err");
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
    var page = document.body.getAttribute("data-page");
    if (page !== "reset" && window.FT_PW && window.FT_PW.isRecovery()) {
      location.replace("/affiliate/reset.html" + location.search + location.hash);
      return;
    }
    var preview = new URLSearchParams(location.search).get("preview") === "1";
    var lang = document.getElementById("langSel");
    if (lang) lang.addEventListener("change", function () {
      if (page === "reset" && window.FT_PW) {
        window.FT_PW.apply(lang.value, true);
        return;
      }
      var value = lang.value;
      location.href = "/" + (value === "ar" ? "" : value + "/");
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

    if (page === "dashboard" && preview) {
      var demo = sample();
      document.getElementById("preview").hidden = false;
      drawDashboard(demo.me, demo.me.clicks, demo.bookings.filter(function (row) { return row.affiliate_id === demo.me.id; }));
      logout(null);
      return;
    }
    if (page === "admin" && preview) {
      var data = sample();
      document.getElementById("preview").hidden = false;
      drawAdmin(data.affiliates, data.bookings);
      bindAdminActions(function (id, status, commission) {
        data.bookings.forEach(function (row) {
          if (row.id !== id) return;
          row.status = status;
          row.commission = status === "confirmed" ? commission : null;
        });
        data.affiliates.forEach(function (person) {
          var mine = data.bookings.filter(function (row) { return row.affiliate_id === person.id; });
          var sum = totals(mine);
          person.bookings = sum.all;
          person.confirmed = sum.confirmed;
          person.commission = sum.commission;
        });
        drawAdmin(data.affiliates, data.bookings);
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
            sb.from("aff_bookings").select("*").order("created_at", { ascending: false })
          ]).then(function (parts) {
            if (parts[0].error) throw parts[0].error;
            if (parts[1].error) throw parts[1].error;
            drawAdmin(parts[0].data || [], parts[1].data || []);
          });
        }).catch(function (error) {
          document.getElementById("gate").hidden = false;
          document.getElementById("gate").textContent = human(error);
        });
      };
      bindAdminActions(function (id, status, commission) {
        return sb.rpc("aff_set_booking_status", { p_id: id, p_status: status, p_commission: commission }).then(function (result) {
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

  window.FTAuth = { keysOk: keysOk, hasLib: hasLib, problem: problem, message: function (code) { return MSG[code] || ""; } };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
