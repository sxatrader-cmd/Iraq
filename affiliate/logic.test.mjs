import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const A = require("./track.js");

const NOW = Date.UTC(2026, 10, 14, 12, 0, 0);

test("normalizes referral codes and rejects junk", () => {
  assert.equal(A.normalizeCode(" ab12cd "), "AB12CD");
  assert.equal(A.normalizeCode("abc"), "");
  assert.equal(A.normalizeCode("../etc"), "");
  assert.equal(A.normalizeCode("ABCD-12"), "");
  assert.equal(A.normalizeCode("A".repeat(13)), "");
});

test("a fresh ?ref= wins, is stored for 30 days, and counts as a click", () => {
  const decision = A.decide({ query: "ab12cd", cookie: "OLD999." + (NOW + 1000), storage: "", now: NOW });
  assert.equal(decision.code, "AB12CD");
  assert.equal(decision.countClick, true);
  assert.equal(decision.write, true);
  assert.equal(decision.exp, NOW + A.WINDOW_MS);
  assert.equal(decision.exp - NOW, 30 * 24 * 60 * 60 * 1000);
});

test("cookie keeps the code after the query is gone, without a new click", () => {
  const exp = NOW + 5 * 24 * 60 * 60 * 1000;
  const bag = A.packBag("AB12CD", exp);
  const decision = A.decide({ query: "", cookie: bag, storage: bag, now: NOW });
  assert.equal(decision.code, "AB12CD");
  assert.equal(decision.countClick, false);
  assert.equal(decision.write, false);
  assert.equal(decision.exp, exp);
});

test("localStorage heals a missing cookie and an expired bag is dropped", () => {
  const exp = NOW + 1000;
  const healed = A.decide({ query: "", cookie: "", storage: A.packBag("ZZ99AA", exp), now: NOW });
  assert.equal(healed.code, "ZZ99AA");
  assert.equal(healed.write, true);
  assert.equal(healed.countClick, false);

  const expired = A.decide({
    query: "",
    cookie: A.packBag("ZZ99AA", NOW - 1),
    storage: A.packBag("ZZ99AA", NOW - 1),
    now: NOW
  });
  assert.equal(expired.code, "");
  assert.equal(expired.clear, true);
});

test("booking payload keeps the form fields and drops the mail key", () => {
  const body = {
    access_key: "secret-key",
    subject: "Iraq Tour",
    from_name: "Fable Tour Website",
    name: "علي حسين",
    email: "ali@example.com",
    whatsapp: "+9647501112233",
    tour: "Iraq Heritage Tour: 7 days / 6 nights",
    group_date: "",
    private_date: "2026-12-20",
    language: "ar",
    botcheck: false
  };
  const snapshot = {
    botcheck: false,
    fields: {
      name: { name: "name", label: "الاسم الكامل", value: "علي حسين", text: "علي حسين", hidden: false },
      email: { name: "email", label: "البريد", value: "ali@example.com", text: "ali@example.com", hidden: false },
      whatsapp: { name: "whatsapp", label: "واتساب", value: "+9647501112233", text: "+9647501112233", hidden: false },
      program: { name: "program", label: "البرنامج", value: body.tour, text: "رحلة التراث العراقي: 7 أيام / 6 ليالٍ — $2,500", hidden: false },
      group_date: { name: "group_date", label: "الموعد", value: "", text: "رحلة خاصة", hidden: false },
      private_date: { name: "private_date", label: "التاريخ", value: "2026-12-20", text: "2026-12-20", hidden: false },
      adults: { name: "adults", label: "عدد الأشخاص", value: "4", text: "4", hidden: false }
    }
  };
  const booking = A.buildBooking(body, snapshot, { pageUrl: "/tours/iraq-7-day-tour/", lang: "ar", title: "العراق" });
  assert.equal(booking.customer_name, "علي حسين");
  assert.equal(booking.customer_phone, "+9647501112233");
  assert.equal(booking.customer_email, "ali@example.com");
  assert.equal(booking.program, "رحلة التراث العراقي: 7 أيام / 6 ليالٍ — $2,500");
  assert.equal(booking.travel_date, "2026-12-20");
  assert.equal(booking.people, "4");
  assert.equal(booking.language, "ar");
  assert.equal(booking.status, undefined);
  assert.equal(booking.commission, undefined);
  assert.equal(JSON.stringify(booking).includes("secret-key"), false);
});

test("a visible group date is kept and a honeypot is ignored", () => {
  const snapshot = {
    fields: {
      name: { name: "name", value: "ليلى", text: "ليلى", hidden: false },
      group_date: { name: "group_date", value: "2026-12-04 — Friday", text: "الجمعة، 4 ديسمبر 2026", hidden: false },
      private_date: { name: "private_date", value: "2026-12-01", text: "2026-12-01", hidden: true }
    }
  };
  const booking = A.buildBooking({ name: "ليلى", botcheck: false }, snapshot, {});
  assert.equal(booking.travel_date, "الجمعة، 4 ديسمبر 2026");
  assert.equal(A.buildBooking({ name: "ليلى", botcheck: true }, snapshot, {}), null);
  assert.equal(A.buildBooking({ botcheck: false }, { botcheck: false, fields: {} }, {}), null);
});

test("keys are treated as missing until the owner pastes them", () => {
  assert.equal(A.isConfigured({ supabaseUrl: "YOUR_SUPABASE_URL", supabaseKey: "YOUR_SUPABASE_ANON_KEY" }), false);
  assert.equal(A.isConfigured({ supabaseUrl: "https://abcd.supabase.co", supabaseKey: "sb_publishable_example_key_123" }), true);
  assert.equal(A.isConfigured({ supabaseUrl: "http://abcd.supabase.co", supabaseKey: "sb_publishable_example_key_123" }), false);
});
