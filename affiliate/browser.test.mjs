/**
 * End-to-end checks against the static site:
 * referral persistence, the real homepage booking form, and the Arabic screens.
 * Run: NODE_PATH=/tmp/ppt/node_modules node affiliate/browser.test.mjs
 */
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const puppeteer = require(process.env.PUPPETEER_CORE || "/tmp/ppt/node_modules/puppeteer-core");

const root = fileURLToPath(new URL("..", import.meta.url));
const types = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".svg": "image/svg+xml", ".xml": "application/xml", ".txt": "text/plain" };

function startServer() {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://127.0.0.1");
      let path = decodeURIComponent(url.pathname);
      if (path.endsWith("/")) path += "index.html";
      const file = normalize(join(root, path));
      if (!file.startsWith(root)) { res.writeHead(403); res.end(); return; }
      const body = await readFile(file);
      res.writeHead(200, { "Content-Type": types[extname(file)] || "application/octet-stream" });
      res.end(body);
    } catch {
      res.writeHead(404); res.end("not found");
    }
  });
  return new Promise((resolve) => server.listen(0, "127.0.0.1", () => resolve(server)));
}

const CONFIG = `window.FT_AFFILIATE_CONFIG={supabaseUrl:"https://example.supabase.co",supabaseKey:"sb_publishable_example_key_123",siteOrigin:"https://iraq.fabletour.com"};`;
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "*",
  "Content-Type": "application/json"
};

function assert(cond, message) {
  if (!cond) throw new Error(message);
}

const shots = process.argv.includes("--shots");
const server = await startServer();
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await puppeteer.launch({
  executablePath: "/usr/local/bin/google-chrome",
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--lang=ar"]
});

const clicks = [];
const bookings = [];
const forms = [];

try {
  const page = await browser.newPage();
  page.setDefaultTimeout(45000);
  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1 });
  page.on("dialog", (dialog) => dialog.accept());
  page.on("pageerror", (error) => console.error("PAGE", error.message));
  await page.setRequestInterception(true);
  page.on("request", (req) => {
    const url = req.url();
    if (req.method() === "OPTIONS") {
      req.respond({ status: 204, headers: CORS });
      return;
    }
    if (url.includes("/affiliate/config.js")) {
      req.respond({ status: 200, contentType: "text/javascript", body: CONFIG });
      return;
    }
    if (url.includes("api.web3forms.com/submit")) {
      forms.push(req.postData() || "");
      req.respond({ status: 200, headers: CORS, body: JSON.stringify({ success: true }) });
      return;
    }
    if (url.includes("/rpc/aff_record_referral_click")) {
      clicks.push(req.postData() || "");
      req.respond({ status: 200, headers: CORS, body: "null" });
      return;
    }
    if (url.includes("/rpc/aff_record_referral_booking")) {
      bookings.push(req.postData() || "");
      req.respond({ status: 200, headers: CORS, body: "null" });
      return;
    }
    if (url.includes("supabase.co") || url.includes("youtube") || url.includes("unsplash.com") || url.includes("wikimedia.org") || url.includes("ytimg.com") || url.includes("googletagmanager") || url.includes("google-analytics")) {
      req.respond({ status: 204, headers: CORS, body: "" });
      return;
    }
    if (!shots && req.resourceType() === "image" && !/logo|hero|favicon|apple-touch/.test(url)) {
      req.abort();
      return;
    }
    req.continue();
  });

  await page.goto(origin + "/?ref=ab12cd", { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => window.FableAffiliate && window.FableAffiliate.current() === "AB12CD");
  const stored = await page.evaluate(() => ({ cookie: document.cookie, bag: localStorage.getItem("ft_ref") }));
  assert(stored.cookie.includes("AB12CD."), "cookie did not keep the referral code");
  assert(stored.bag && stored.bag.startsWith("AB12CD."), "localStorage did not keep the referral code");
  await page.waitForFunction(() => window.__clicksSeen || true);
  await new Promise((r) => setTimeout(r, 400));
  assert(clicks.length === 1, "expected one click, got " + clicks.length + " " + clicks.join("|"));
  assert(JSON.parse(clicks[0]).p_code === "AB12CD", "click code mismatch");

  await page.goto(origin + "/affiliate/login.html", { waitUntil: "domcontentloaded" });
  await page.addScriptTag({ url: origin + "/affiliate/track.js" });
  await page.waitForFunction(() => window.FableAffiliate && window.FableAffiliate.current() === "AB12CD");
  assert(clicks.length === 1, "a page without ?ref= counted another click");

  await page.goto(origin + "/", { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => window.__ftAffFetch === true && window.FableAffiliate.current() === "AB12CD");
  await page.evaluate(() => {
    document.getElementById("f-name").value = "علي حسين";
    document.getElementById("f-email").value = "ali@example.com";
    document.getElementById("f-wa").value = "+9647501112233";
    const date = document.getElementById("f-pdate");
    if (date) date.value = "2026-12-20";
  });
  await page.click("#f-btn");
  await page.waitForSelector("#f-msg.ok");
  const message = await page.$eval("#f-msg", (el) => el.textContent);
  assert(message.includes("تم استلام طلبك"), "booking form success message changed: " + message);
  await page.waitForFunction(() => window.__bookings === 1, { timeout: 8000 }).catch(() => {});
  await new Promise((r) => setTimeout(r, 500));
  assert(forms.length === 1, "Web3Forms was not called once");
  const sent = JSON.parse(forms[0]);
  assert(sent.name === "علي حسين", "form name was altered");
  assert(sent.access_key === "9e405ed2-6f37-467e-aea0-4b7678c7e635", "form access key was altered");
  assert(sent.tour && sent.tour.includes("7 days"), "form tour value was altered");
  assert(!forms[0].includes("p_code"), "referral payload leaked into the email form");
  assert(bookings.length === 1, "pending booking was not recorded: " + bookings.length);
  const saved = JSON.parse(bookings[0]);
  assert(saved.p_code === "AB12CD", "booking attributed to the wrong code");
  assert(saved.p_payload.customer_name === "علي حسين");
  assert(saved.p_payload.customer_phone === "+9647501112233");
  assert(saved.p_payload.customer_email === "ali@example.com");
  assert(saved.p_payload.program.includes("رحلة التراث"), "program label was not kept: " + saved.p_payload.program);
  assert(saved.p_payload.travel_date === "2026-12-20", "date was " + saved.p_payload.travel_date);
  assert(!JSON.stringify(saved).includes("9e405ed2"), "mail key was copied into the booking");
  assert(saved.p_payload.status == null && saved.p_payload.commission == null, "client tried to set status");

  await page.goto(origin + "/affiliate/", { waitUntil: "domcontentloaded" });
  await page.waitForSelector("#join[data-ready='1']");
  const dir = await page.$eval("html", (el) => el.getAttribute("dir"));
  assert(dir === "rtl", "signup page is not RTL");
  await page.click("#f-btn");
  await page.waitForFunction(() => document.getElementById("f-msg").textContent.includes("واتساب"));
  const scripts = await page.evaluate(() => ({
    config: document.querySelectorAll("script[src*='config.js']").length,
    auth: document.querySelectorAll("script[src*='auth.js']").length,
    vendor: document.querySelectorAll("script[src*='vendor/supabase.js']").length,
    cdn: document.querySelectorAll("script[src*='jsdelivr']").length
  }));
  assert(scripts.config === 1 && scripts.auth === 1 && scripts.vendor === 1 && scripts.cdn === 0, JSON.stringify(scripts));
  await page.waitForFunction(() => window.FTAuth && window.FTAuth.hasLib() && window.FTAuth.problem() === "");
  const classified = await page.evaluate(() => {
    var keepCfg = window.FT_AFFILIATE_CONFIG;
    var keepLib = window.supabase;
    window.FT_AFFILIATE_CONFIG = { supabaseUrl: "YOUR_SUPABASE_URL", supabaseKey: "YOUR_SUPABASE_ANON_KEY" };
    var keys = window.FTAuth.problem();
    window.FT_AFFILIATE_CONFIG = keepCfg;
    window.supabase = undefined;
    var library = window.FTAuth.problem();
    window.supabase = keepLib;
    return {
      keys: keys,
      library: library,
      keysText: window.FTAuth.message("keys"),
      libraryText: window.FTAuth.message("library"),
      networkText: window.FTAuth.message("network")
    };
  });
  assert(classified.keys === "keys" && classified.library === "library", JSON.stringify(classified));
  assert(classified.keysText !== classified.libraryText && classified.libraryText !== classified.networkText);
  assert(!classified.keysText.includes("أو تعذّر"), classified.keysText);

  await page.goto(origin + "/affiliate/login.html", { waitUntil: "domcontentloaded" });
  const loginScripts = await page.evaluate(() => document.querySelectorAll("script[src*='config.js'], script[src*='auth.js'], script[src*='vendor/supabase.js']").length);
  assert(loginScripts === 3, "login page should include each script once, got " + loginScripts);

  await page.goto(origin + "/affiliate/dashboard.html", { waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => {
    var gate = document.getElementById("gate");
    return location.pathname.indexOf("login") !== -1 || (gate && !gate.hidden && gate.textContent);
  });
  const gateText = await page.evaluate(() => {
    var gate = document.getElementById("gate");
    return gate && !gate.hidden ? gate.textContent : "";
  });
  assert(!gateText.includes("لم تُلصق مفاتيح"), gateText);
  assert(!gateText.includes("غير موجودة"), gateText);

  await page.goto(origin + "/affiliate/dashboard.html?preview=1", { waitUntil: "domcontentloaded" });
  await page.waitForSelector("#app:not([hidden]) #ref-link");
  const link = await page.$eval("#ref-link", (el) => el.textContent);
  assert(link === "https://iraq.fabletour.com/?ref=A7K3QM", link);
  const dash = await page.evaluate(() => ({
    clicks: document.getElementById("n-clicks").textContent,
    all: document.getElementById("n-all").textContent,
    pending: document.getElementById("n-pending").textContent,
    actions: document.querySelectorAll("[data-act]").length,
    text: document.body.innerText
  }));
  assert(dash.clicks === "18" && dash.all === "2" && dash.pending === "1", JSON.stringify(dash));
  assert(dash.actions === 0, "affiliate dashboard exposed status buttons");
  assert(dash.text.includes("علي حسين") && dash.text.includes("مبدئي") && !dash.text.includes("جون"), "affiliate saw another partner's booking");

  await page.goto(origin + "/affiliate/admin.html?preview=1", { waitUntil: "domcontentloaded" });
  await page.waitForSelector("tr[data-status='pending'] [data-act='confirmed']");
  await page.$eval("tr[data-status='pending'] .comm", (el) => { el.value = "175"; });
  await page.click("tr[data-status='pending'] [data-act='confirmed']");
  await page.waitForFunction(() => document.body.innerText.includes("تم تحديث الحالة"));
  const after = await page.evaluate(() => ({
    money: document.getElementById("a-money").textContent,
    confirmed: document.querySelectorAll("tr[data-status='confirmed']").length,
    ali: [...document.querySelectorAll("tr")].some((row) => row.textContent.includes("علي حسين") && row.textContent.includes("مؤكد"))
  }));
  assert(after.ali, "confirm did not mark the booking");
  assert(after.confirmed === 2, "confirmed count " + after.confirmed);
  assert(after.money.includes("325"), after.money);

  if (shots) {
    const dirOut = "/opt/cursor/artifacts";
    async function shot(name) {
      await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; });
      await page.waitForFunction(() => {
        const img = document.querySelector(".hero-img");
        return img && img.complete && img.naturalWidth > 0;
      });
      await new Promise((r) => setTimeout(r, 250));
      await page.screenshot({ path: dirOut + "/" + name, fullPage: true });
    }
    await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1 });
    await page.goto(origin + "/affiliate/", { waitUntil: "domcontentloaded" });
    await shot("affiliate-signup.png");
    await page.goto(origin + "/affiliate/login.html", { waitUntil: "domcontentloaded" });
    await shot("affiliate-login.png");
    await page.goto(origin + "/affiliate/dashboard.html?preview=1", { waitUntil: "domcontentloaded" });
    await page.waitForSelector("#ref-link");
    await shot("affiliate-dashboard.png");
    await page.goto(origin + "/affiliate/admin.html?preview=1", { waitUntil: "domcontentloaded" });
    await page.waitForSelector("[data-act='confirmed']");
    await shot("affiliate-admin.png");
    await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
    await page.goto(origin + "/affiliate/", { waitUntil: "domcontentloaded" });
    await shot("affiliate-signup-mobile.png");
  }

  console.log("browser checks passed");
} finally {
  await browser.close();
  server.close();
}
