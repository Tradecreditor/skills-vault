# Supabase capture proxy (Phase 2)

Why: the Routine fire API has no de-duplication and its token should not live on your phone. This ~80-line Edge Function keeps the token
server-side, records every link in a `captures` table (an agent-visible inbox), and fires the `capture-link` Routine once per request.

```bash
# once, from the vault root
supabase login
supabase init            # creates supabase/config.toml next to these files (keep the generated file)
supabase link --project-ref <your-project-ref>
supabase db push         # applies migrations/20260913000000_captures.sql
supabase secrets set CAPTURE_SECRET="$(openssl rand -hex 24)" \
  ROUTINE_FIRE_URL="https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire" \
  ROUTINE_TOKEN="<token shown once when you added the API trigger>"
# Telegram (optional): BOTH are required if you set the webhook: TELEGRAM_BOT_TOKEN=<from BotFather> TELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 16)"
supabase functions deploy capture --no-verify-jwt   # or set [functions.capture] verify_jwt = false in supabase/config.toml

# test
curl -sS -X POST "https://<project-ref>.supabase.co/functions/v1/capture" \
  -H "content-type: application/json" -H "x-capture-secret: <CAPTURE_SECRET>" \
  -d '{"url":"https://github.com/kepano/obsidian-skills","note":"test"}'
```

Telegram webhook (optional): `curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<project-ref>.supabase.co/functions/v1/capture&secret_token=<TELEGRAM_WEBHOOK_SECRET>&allowed_updates=%5B%22message%22%5D"`. Requests that look like Telegram updates are rejected unless the secret matches, so the webhook secret is mandatory.

iPhone Shortcut "Save to Vault": Shortcuts → + → Details: *Show in Share Sheet*, accepts URLs and Text → action **Get Contents of URL**:
Method POST, URL `https://<project-ref>.supabase.co/functions/v1/capture`, Headers `x-capture-secret: <CAPTURE_SECRET>`,
Request Body JSON `{ "url": Shortcut Input, "note": Ask Each Time }` → action **Show Notification** with the result.

Behaviour: duplicate URLs are ignored (X share suffixes, tracking params and t.co links are canonicalised first); a URL whose Routine fire failed can be re-sent; the response is HTTP 502 with ok:false when the Routine could not be fired.

Free tier note: Supabase pauses free projects after 7 idle days; a few captures a week keep it alive, otherwise Pro (US$25/mo) removes pausing.
