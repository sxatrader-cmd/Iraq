/* Referral attribution for the static Fable Tour site.
   Persists ?ref= for 30 days (cookie + localStorage) and, after a successful
   Web3Forms booking, records a pending booking. Does not change the request
   the booking form already sends. */
(function (root) {
  "use strict";

  var WINDOW_MS = 30 * 24 * 60 * 60 * 1000;
  var CODE_RE = /^[A-Z0-9]{4,12}$/;
  var SECRET = {
    access_key: 1, botcheck: 1, password: 1, apikey: 1, token: 1,
    authorization: 1, subject: 1, from_name: 1
  };
  var active = "";

  function normalizeCode(raw) {
    if (raw == null) return "";
    var code = String(raw).trim().toUpperCase();
    return CODE_RE.test(code) ? code : "";
  }

  function isConfigured(cfg) {
    if (!cfg || !cfg.supabaseUrl || !cfg.supabaseKey) return false;
    if (/YOUR_/i.test(cfg.supabaseUrl) || /YOUR_/i.test(cfg.supabaseKey)) return false;
    return /^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/i.test(cfg.supabaseUrl) && String(cfg.supabaseKey).length > 20;
  }

  function packBag(code, exp) {
    return code + "." + exp;
  }

  function parseBag(raw, now) {
    if (raw == null || raw === "") return null;
    var text = String(raw).trim();
    if (text.charAt(0) === "{") {
      try {
        var obj = JSON.parse(text);
        text = obj && obj.c ? (obj.c + "." + (obj.e || "")) : "";
      } catch (e) { return null; }
    }
    var dot = text.lastIndexOf(".");
    if (dot > 0) {
      var code = normalizeCode(text.slice(0, dot));
      var exp = parseInt(text.slice(dot + 1), 10);
      if (!code || !exp) return null;
      if (now > exp) return null;
      return { code: code, exp: exp };
    }
    var legacy = normalizeCode(text);
    if (!legacy) return null;
    return { code: legacy, exp: now + WINDOW_MS, legacy: true };
  }

  function decide(state) {
    var now = state.now || Date.now();
    var query = normalizeCode(state.query);
    if (query) {
      var exp = now + WINDOW_MS;
      return { code: query, exp: exp, write: true, countClick: true, clear: false };
    }
    var fromCookie = parseBag(state.cookie, now);
    if (fromCookie) {
      var packed = packBag(fromCookie.code, fromCookie.exp);
      return {
        code: fromCookie.code,
        exp: fromCookie.exp,
        write: state.storage !== packed,
        countClick: false,
        clear: false
      };
    }
    var fromStore = parseBag(state.storage, now);
    if (fromStore) {
      return { code: fromStore.code, exp: fromStore.exp, write: true, countClick: false, clear: false };
    }
    return { code: "", exp: 0, write: false, countClick: false, clear: !!(state.cookie || state.storage) };
  }

  function fieldOf(snap, body, names) {
    var fields = (snap && snap.fields) || {};
    var i, key, found;
    for (i = 0; i < names.length; i++) {
      found = fields[names[i]];
      if (found && String(found.value || "").trim()) return found;
    }
    if (!body) return null;
    for (i = 0; i < names.length; i++) {
      key = names[i];
      if (body[key] != null && String(body[key]).trim() !== "") {
        return { name: key, label: "", value: String(body[key]), text: String(body[key]), hidden: false };
      }
    }
    return null;
  }

  function flagged(value) {
    return value === true || value === 1 || value === "true" || value === "on";
  }

  function peopleOf(snap, body) {
    var keys = ["people", "persons", "pax", "adults", "adult", "guests", "travellers", "travelers", "children", "kids", "group_size"];
    var found = [];
    var i, item, fields, name, label;
    for (i = 0; i < keys.length; i++) {
      item = fieldOf(snap, body, [keys[i]]);
      if (item && String(item.value).trim() && !item.hidden) found.push(item);
    }
    fields = (snap && snap.fields) || {};
    for (name in fields) {
      if (!Object.prototype.hasOwnProperty.call(fields, name)) continue;
      if (keys.indexOf(name) !== -1) continue;
      item = fields[name];
      label = (item.label || "") + " " + name;
      if (/شخص|أشخاص|مسافر|people|pax|guest/i.test(label) && String(item.value || "").trim() && !item.hidden) {
        found.push(item);
      }
    }
    if (!found.length) return "";
    if (found.length === 1) return String(found[0].text || found[0].value).trim();
    return found.map(function (item) {
      return (item.label || item.name) + ": " + (item.text || item.value);
    }).join(" · ");
  }

  function dateOf(snap, body) {
    var group = fieldOf(snap, body, ["group_date"]);
    var priv = fieldOf(snap, body, ["private_date"]);
    var other = fieldOf(snap, body, ["travel_date", "date", "arrival_date"]);
    if (group && group.value && !group.hidden) return String(group.text || group.value).trim();
    if (priv && priv.value && !priv.hidden) return String(priv.text || priv.value).trim();
    if (group && group.value) return String(group.text || group.value).trim();
    if (priv && priv.value) return String(priv.text || priv.value).trim();
    if (other && other.value) return String(other.text || other.value).trim();
    return "";
  }

  function buildBooking(body, snapshot, meta) {
    body = body || {};
    meta = meta || {};
    if (flagged(body.botcheck) || (snapshot && flagged(snapshot.botcheck))) return null;
    var name = fieldOf(snapshot, body, ["name", "full_name", "customer_name"]);
    var customer = name ? String(name.text || name.value).trim() : "";
    if (!customer) return null;
    var email = fieldOf(snapshot, body, ["email"]);
    var phone = fieldOf(snapshot, body, ["whatsapp", "phone", "tel", "mobile"]);
    var program = fieldOf(snapshot, body, ["program", "tour", "package", "trip"]);
    var fields = [];
    var source = (snapshot && snapshot.fields) || {};
    var key;
    for (key in source) {
      if (!Object.prototype.hasOwnProperty.call(source, key)) continue;
      if (SECRET[String(key).toLowerCase()]) continue;
      fields.push({
        name: key,
        label: source[key].label || "",
        value: source[key].value == null ? "" : String(source[key].value),
        text: source[key].text == null ? "" : String(source[key].text)
      });
    }
    if (!fields.length) {
      for (key in body) {
        if (!Object.prototype.hasOwnProperty.call(body, key)) continue;
        if (SECRET[String(key).toLowerCase()]) continue;
        fields.push({ name: key, label: "", value: String(body[key]), text: String(body[key]) });
      }
    }
    var details = {
      page_title: meta.title || "",
      language: body.language || meta.lang || "",
      fields: fields
    };
    var encoded = "";
    try { encoded = JSON.stringify(details); } catch (e) { encoded = ""; }
    if (encoded.length > 20000) details = { truncated: true, page_title: meta.title || "" };
    return {
      customer_name: customer.slice(0, 200),
      customer_phone: phone ? String(phone.text || phone.value).trim().slice(0, 40) : "",
      customer_email: email ? String(email.value || email.text).trim().slice(0, 200) : "",
      program: program ? String(program.text || program.value).trim().slice(0, 300) : "",
      travel_date: dateOf(snapshot, body).slice(0, 200),
      people: peopleOf(snapshot, body).slice(0, 120),
      language: String(body.language || meta.lang || "").slice(0, 12),
      page_url: String(meta.pageUrl || "").slice(0, 300),
      details: details
    };
  }

  function readCookie(name) {
    var parts = String(document.cookie || "").split(";");
    var i, part, eq;
    for (i = 0; i < parts.length; i++) {
      part = parts[i].replace(/^\s+/, "");
      eq = part.indexOf("=");
      if (eq === -1) continue;
      if (part.slice(0, eq) === name) {
        try { return decodeURIComponent(part.slice(eq + 1)); } catch (e) { return part.slice(eq + 1); }
      }
    }
    return "";
  }

  function saveRef(code, exp) {
    var bag = packBag(code, exp);
    var maxAge = Math.max(1, Math.floor((exp - Date.now()) / 1000));
    var secure = location.protocol === "https:" ? "; Secure" : "";
    document.cookie = "ft_ref=" + encodeURIComponent(bag) + "; Max-Age=" + maxAge + "; Path=/; SameSite=Lax" + secure;
    try { localStorage.setItem("ft_ref", bag); } catch (e) {}
  }

  function clearRef() {
    document.cookie = "ft_ref=; Max-Age=0; Path=/; SameSite=Lax";
    try { localStorage.removeItem("ft_ref"); } catch (e) {}
  }

  function pagePath() {
    try {
      var url = new URL(location.href);
      url.searchParams.delete("ref");
      return (url.pathname + url.search + url.hash).slice(0, 300);
    } catch (e) {
      return (location.pathname || "/").slice(0, 300);
    }
  }

  function requestUrl(input) {
    if (typeof input === "string") return input;
    if (input && typeof input.url === "string") return input.url;
    return "";
  }

  function parseBody(init) {
    if (!init || typeof init.body !== "string") return null;
    try { return JSON.parse(init.body); } catch (e) { return null; }
  }

  function snapshot(form) {
    var out = { botcheck: false, fields: {} };
    var nodes = form.querySelectorAll("input, select, textarea");
    var i, el, hidden, label, text, id;
    for (i = 0; i < nodes.length; i++) {
      el = nodes[i];
      if (!el.name || el.disabled) continue;
      if (el.name === "botcheck") { out.botcheck = !!el.checked; continue; }
      if (el.type === "checkbox" && !el.checked) continue;
      hidden = !!el.hidden || el.type === "hidden";
      id = el;
      while (id && id !== form) {
        if (id.hidden) hidden = true;
        id = id.parentElement;
      }
      label = "";
      if (el.id) {
        var lab = form.querySelector('label[for="' + el.id + '"]');
        if (lab) label = lab.textContent.replace(/\s+/g, " ").trim();
      }
      text = el.value;
      if (el.tagName === "SELECT" && el.options && el.selectedIndex >= 0) {
        text = el.options[el.selectedIndex].textContent.replace(/\s+/g, " ").trim();
      }
      out.fields[el.name] = { name: el.name, label: label, value: el.value, text: text, hidden: hidden };
    }
    return out;
  }

  function post(cfg, fn, body) {
    var url = String(cfg.supabaseUrl).replace(/\/$/, "") + "/rest/v1/rpc/" + fn;
    try {
      var send = root.fetch;
      send.call(root, url, {
        method: "POST",
        keepalive: true,
        headers: {
          apikey: cfg.supabaseKey,
          Authorization: "Bearer " + cfg.supabaseKey,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      }).catch(function () {});
    } catch (e) {}
  }

  function recordBooking(cfg, body, snap) {
    if (!isConfigured(cfg) || !active) return;
    var payload = buildBooking(body || {}, snap, {
      pageUrl: pagePath(),
      lang: document.documentElement.lang || "",
      title: document.title || ""
    });
    if (!payload) return;
    post(cfg, "record_referral_booking", { p_code: active, p_payload: payload });
  }

  function install() {
    if (root.__ftAffInstalled) return;
    root.__ftAffInstalled = true;
    var cfg = root.FT_AFFILIATE_CONFIG || {};
    var query = "";
    try { query = new URLSearchParams(location.search).get("ref") || ""; } catch (e) {}
    var cookie = "";
    var storage = "";
    try { cookie = readCookie("ft_ref"); } catch (e) {}
    try { storage = localStorage.getItem("ft_ref") || ""; } catch (e) {}
    var decision = decide({ query: query, cookie: cookie, storage: storage, now: Date.now() });
    active = decision.code || "";
    if (decision.clear) clearRef();
    else if (decision.code && decision.write) saveRef(decision.code, decision.exp);
    if (decision.countClick && decision.code && isConfigured(cfg)) {
      var seen = "";
      try { seen = sessionStorage.getItem("ft_ref_hit") || ""; } catch (e) {}
      if (seen !== decision.code) {
        try { sessionStorage.setItem("ft_ref_hit", decision.code); } catch (e) {}
        post(cfg, "record_referral_click", { p_code: decision.code, p_page: pagePath() });
      }
    }
    document.addEventListener("submit", function (event) {
      var form = event.target;
      if (!form || form.id !== "form") return;
      try { root.__ftAffSnap = snapshot(form); } catch (e) { root.__ftAffSnap = null; }
    }, true);
    if (!root.__ftAffFetch && typeof root.fetch === "function") {
      root.__ftAffFetch = true;
      var original = root.fetch;
      root.fetch = function (input, init) {
        var url = requestUrl(input);
        var hit = url.indexOf("api.web3forms.com/submit") !== -1;
        var body = hit ? parseBody(init) : null;
        var snap = hit ? root.__ftAffSnap : null;
        var pending = original.apply(this, arguments);
        if (!hit) return pending;
        return Promise.resolve(pending).then(function (response) {
          try {
            response.clone().json().then(function (json) {
              if (json && json.success) recordBooking(cfg, body, snap);
            }).catch(function () {});
          } catch (e) {}
          return response;
        });
      };
    }
  }

  var api = {
    WINDOW_MS: WINDOW_MS,
    normalizeCode: normalizeCode,
    isConfigured: isConfigured,
    packBag: packBag,
    parseBag: parseBag,
    decide: decide,
    buildBooking: buildBooking,
    current: function () { return active; },
    install: install
  };

  root.FableAffiliate = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document !== "undefined") {
    if (root.FT_AFFILIATE_CONFIG) install();
    else {
      var tries = 0;
      (function wait() {
        if (root.FT_AFFILIATE_CONFIG || tries > 40) { install(); return; }
        tries += 1;
        setTimeout(wait, 25);
      })();
    }
  }
})(typeof window !== "undefined" ? window : globalThis);
