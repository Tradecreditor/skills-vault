// Supabase Edge Function `capture`
// Receives a link from the iPhone Shortcut (JSON {url, note}) or a Telegram bot webhook, de-duplicates it in the
// `captures` table, and fires the Claude Code Routine "capture-link" once with all new URLs.
// Secrets: CAPTURE_SECRET (Shortcut header), ROUTINE_FIRE_URL, ROUTINE_TOKEN, and for Telegram BOTH
// TELEGRAM_WEBHOOK_SECRET (mandatory: Telegram-shaped requests are rejected without it) and TELEGRAM_BOT_TOKEN (replies),
// plus TELEGRAM_ALLOWED_USERS (your Telegram user ID; everyone else is refused).
// Deploy: supabase functions deploy capture --no-verify-jwt
import { createClient } from "npm:@supabase/supabase-js@2";

const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const CAPTURE_SECRET = Deno.env.get("CAPTURE_SECRET") ?? "";
const FIRE_URL = Deno.env.get("ROUTINE_FIRE_URL") ?? "";      // https://api.anthropic.com/v1/claude_code/routines/trig_.../fire
const ROUTINE_TOKEN = Deno.env.get("ROUTINE_TOKEN") ?? "";
const TG_SECRET = Deno.env.get("TELEGRAM_WEBHOOK_SECRET") ?? "";
const TG_BOT_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN") ?? "";
// Comma-separated Telegram user IDs allowed to capture. Empty = nobody: anyone who finds the bot could otherwise spend
// the Routine's daily runs. A rejected sender is told their own ID, which is how the owner finds the value to set.
const TG_ALLOWED = new Set((Deno.env.get("TELEGRAM_ALLOWED_USERS") ?? "").split(",").map((s) => s.trim()).filter(Boolean));
const URL_RE = /https?:\/\/[^\s<>"'`)\]]+/g;
const GLOBAL_STRIP = /^(utm_.*|fbclid|gclid|igsh|igshid|si)$/i;
const HOST_STRIP: Record<string, RegExp> = {
  "x.com": /^(s|t|ref_src|ref_url)$/i,
  "youtube.com": /^(t|feature|list|index|pp)$/i,
  "threads.net": /^(xmt|hl)$/i,
  "instagram.com": /^(img_index|hl)$/i,
};
const SHORTENERS = new Set(["t.co", "bit.ly", "lnkd.in", "vt.tiktok.com", "vm.tiktok.com", "youtu.be"]);
const RETRY_STATUSES = new Set(["fire_failed"]);
const STALE_QUEUED_MS = 10 * 60 * 1000;

function extractUrls(text: string): string[] {
  return (text.match(URL_RE) ?? []).map((u) => u.replace(/[.,!?;:'"]+$/, ""));
}

async function expand(raw: string): Promise<string> {
  let u = raw;
  for (let hop = 0; hop < 3; hop++) {
    let host = "";
    try { host = new URL(u).hostname.toLowerCase().replace(/^www\./, ""); } catch { return u; }
    if (!SHORTENERS.has(host) || host === "youtu.be") break;
    try {
      const r = await fetch(u, { method: "HEAD", redirect: "manual", signal: AbortSignal.timeout(5000) });
      const loc = r.headers.get("location");
      if (!loc) break;
      u = new URL(loc, u).toString();
    } catch { break; }
  }
  return u;
}

function normalise(raw: string): string {
  try {
    const u = new URL(raw.trim());
    u.hash = "";
    let host = u.hostname.toLowerCase().replace(/^(www|m|mobile)\./, "");
    if (host === "twitter.com" || host === "fxtwitter.com" || host === "vxtwitter.com") host = "x.com";
    if (host === "threads.com") host = "threads.net";
    if (host === "youtu.be") { u.searchParams.set("v", u.pathname.split("/")[1] ?? ""); u.pathname = "/watch"; host = "youtube.com"; }
    u.hostname = host;
    if (host === "x.com") {                                            // /<handle>/status/<id>[/photo/1] -> /<handle>/status/<id>
      const m = u.pathname.match(/^\/([^/]+)\/status\/(\d+)/);
      if (m) { u.pathname = `/${m[1].toLowerCase()}/status/${m[2]}`; u.search = ""; }
    }
    if (host === "youtube.com" && u.pathname.startsWith("/shorts/")) { u.searchParams.set("v", u.pathname.split("/")[2] ?? ""); u.pathname = "/watch"; }
    if (host === "instagram.com") { const m = u.pathname.match(/^\/(p|reel|reels|tv)\/([^/]+)/); if (m) { u.pathname = `/${m[1] === "reels" ? "reel" : m[1]}/${m[2]}/`; u.search = ""; } }
    const hostStrip = HOST_STRIP[host];
    for (const k of [...u.searchParams.keys()]) if (GLOBAL_STRIP.test(k) || (hostStrip && hostStrip.test(k))) u.searchParams.delete(k);
    if (host === "youtube.com" && u.searchParams.has("v")) { const v = u.searchParams.get("v")!; u.search = ""; u.searchParams.set("v", v); }
    u.pathname = u.pathname.replace(/\/{2,}/g, "/");
    if (u.pathname.length > 1 && u.pathname.endsWith("/") && host !== "instagram.com") u.pathname = u.pathname.slice(0, -1);
    return u.toString();
  } catch { return raw.trim(); }
}

async function fire(text: string) {
  try {
    const r = await fetch(FIRE_URL, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${ROUTINE_TOKEN}`,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "experimental-cc-routine-2026-04-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(20000),
    });
    const body = await r.json().catch(() => ({}));
    if (!r.ok) console.error("routine fire failed", r.status, JSON.stringify(body));
    return { ok: r.ok, status: r.status, body };
  } catch (e) {
    console.error("routine fire error", String(e));
    return { ok: false, status: 0, body: {} };
  }
}

async function tgReply(chatId: number | string, text: string) {
  if (!TG_BOT_TOKEN) return;
  await fetch(`https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }), signal: AbortSignal.timeout(5000),
  }).catch(() => {});
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });
  const body = await req.json().catch(() => ({}));
  const isTelegram = typeof body?.update_id === "number" || req.headers.has("x-telegram-bot-api-secret-token");
  let urls: string[] = [], note = "", source = "shortcut", chatId: number | string | null = null;

  if (isTelegram) {
    if (!TG_SECRET || req.headers.get("x-telegram-bot-api-secret-token") !== TG_SECRET) return new Response("forbidden", { status: 403 });
    const msg = body.message ?? body.channel_post ?? null;
    if (!msg) return Response.json({ ok: true, ignored: "no message" });       // 200 so Telegram stops retrying
    const senderId = String(msg.from?.id ?? msg.chat?.id ?? "");
    if (!TG_ALLOWED.has(senderId)) {
      if (msg.chat?.id) await tgReply(msg.chat.id, `This bot is private. Your Telegram ID is ${senderId}; the owner adds it to TELEGRAM_ALLOWED_USERS.`);
      return Response.json({ ok: true, ignored: "sender not allowed" });      // 200 so Telegram stops retrying
    }
    const t: string = msg.text ?? msg.caption ?? "";
    const ents = (msg.entities ?? msg.caption_entities ?? []) as { type: string; url?: string }[];
    urls = [...extractUrls(t), ...ents.filter((e) => e.type === "text_link" && e.url).map((e) => e.url!)];
    note = t.replace(URL_RE, "").trim().slice(0, 500); source = "telegram"; chatId = msg.chat?.id ?? null;
    if (!urls.length) { if (chatId) await tgReply(chatId, "Send me a link and I will save it to the vault."); return Response.json({ ok: true }); }
  } else {
    if (!CAPTURE_SECRET || req.headers.get("x-capture-secret") !== CAPTURE_SECRET) return new Response("forbidden", { status: 403 });
    urls = extractUrls(String(body.url ?? body.text ?? "")); note = String(body.note ?? "").slice(0, 500);
    if (!urls.length) return Response.json({ ok: false, error: "no url" }, { status: 400 });
  }

  const canon = [...new Set(await Promise.all(urls.map(async (u) => normalise(await expand(u)))))];
  const fresh: string[] = [], results: Record<string, string>[] = [];
  for (const u of canon) {
    const { data: existing } = await sb.from("captures").select("url,status,updated_at").eq("url", u).maybeSingle();
    if (existing) {
      const stale = existing.status === "queued" && Date.now() - new Date(existing.updated_at).getTime() > STALE_QUEUED_MS;
      if (!RETRY_STATUSES.has(existing.status) && !stale) { results.push({ url: u, status: "duplicate" }); continue; }
      await sb.from("captures").update({ note, source, status: "queued" }).eq("url", u);
      fresh.push(u); continue;
    }
    const { data: ins, error } = await sb.from("captures").upsert({ url: u, note, source, status: "queued" }, { onConflict: "url", ignoreDuplicates: true }).select("url");
    if (error) { results.push({ url: u, status: "db_error", error: error.message }); continue; }
    if (!ins || ins.length === 0) { results.push({ url: u, status: "duplicate" }); continue; }   // lost a race: someone inserted first
    fresh.push(u);
  }

  let fireOk = true;
  if (fresh.length) {
    const text = `Capture these links into the skills vault:\n${fresh.join("\n")}${note ? `\nUser note: ${note}` : ""}`;
    const f = await fire(text);
    fireOk = f.ok;
    const sessionId = f.body?.claude_code_session_id ?? f.body?.session_id ?? null;
    const sessionUrl = f.body?.claude_code_session_url ?? null;
    await sb.from("captures").update({ status: f.ok ? "fired" : "fire_failed", session_id: sessionId, session_url: sessionUrl }).in("url", fresh);
    for (const u of fresh) results.push({ url: u, status: f.ok ? "fired" : "fire_failed", http: String(f.status) });
  }

  if (chatId) {
    const firedN = results.filter((r) => r.status === "fired").length, dupN = results.filter((r) => r.status === "duplicate").length;
    await tgReply(chatId, `Vault: ${firedN} queued${dupN ? `, ${dupN} already saved` : ""}${fireOk ? "" : " — routine fire failed, check the function logs"}.`);
  }
  return Response.json({ ok: fireOk, results }, { status: fireOk ? 200 : 502 });
});
