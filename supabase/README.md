# Supabase capture proxy (Phase 2)

Why: the Routine fire API has no de-duplication and its token should not live on your phone. This Edge Function (~160 lines) keeps the token
server-side, records every link in a `captures` table (an agent-visible inbox), and fires the `capture-link` Routine once per request.

```bash
# once, from the vault root
supabase login
supabase init            # creates supabase/config.toml next to these files (local only, gitignored; set [functions.capture] verify_jwt = false there or pass --no-verify-jwt below)
supabase link --project-ref <your-project-ref>
supabase db push         # applies every pending file in migrations/
supabase secrets set CAPTURE_SECRET="$(openssl rand -hex 24)" \
  ROUTINE_FIRE_URL="https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire" \
  ROUTINE_TOKEN="<token shown once when you added the API trigger>"
# Telegram (optional): all three are required together; with TELEGRAM_ALLOWED_USERS empty the bot refuses everyone.
# Chicken-and-egg: you learn your Telegram ID by messaging the bot (it replies with it), so run this once without
# knowing it, set the webhook below, message the bot, then re-run with TELEGRAM_ALLOWED_USERS filled in.
supabase secrets set TELEGRAM_BOT_TOKEN=<from BotFather> TELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 16)" TELEGRAM_ALLOWED_USERS=<your Telegram user id, comma-separated for several>
supabase functions deploy capture --no-verify-jwt   # or set [functions.capture] verify_jwt = false in supabase/config.toml
# re-run 'supabase db push' after pulling: migrations/20260925000000_captures_grants.sql re-issues the GRANTs that were added to an already-applied migration

# test
curl -sS -X POST "https://<project-ref>.supabase.co/functions/v1/capture" \
  -H "content-type: application/json" -H "x-capture-secret: <CAPTURE_SECRET>" \
  -d '{"url":"https://github.com/kepano/obsidian-skills","note":"test"}'
```

Telegram webhook (optional): `curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<project-ref>.supabase.co/functions/v1/capture&secret_token=<TELEGRAM_WEBHOOK_SECRET>&allowed_updates=%5B%22message%22%5D"`. Requests that look like Telegram updates are rejected unless the secret matches, so the webhook secret is mandatory. Only the user IDs in `TELEGRAM_ALLOWED_USERS` (comma-separated) can capture; anyone else gets "This bot is private" with their own ID, so to find yours, message the bot before setting it. Secrets set with `supabase secrets set` are live in the function immediately; no redeploy is needed.

iPhone Shortcut "Save to Vault": Shortcuts → + → Details: *Show in Share Sheet*, accepts URLs and Text → action **Get Contents of URL**:
Method POST, URL `https://<project-ref>.supabase.co/functions/v1/capture`, Headers `x-capture-secret: <CAPTURE_SECRET>`,
Request Body JSON `{ "url": Shortcut Input, "note": Ask Each Time }` → action **Show Notification** with the result.

Behaviour: duplicate URLs are ignored (X share suffixes, tracking params and t.co links are canonicalised first); a URL whose Routine fire failed can be re-sent; the response is HTTP 502 with ok:false when the Routine could not be fired.

Free tier note: Supabase pauses free projects after 7 idle days; a few captures a week keep it alive, otherwise Pro (US$25/mo) removes pausing.

## Names used elsewhere

The Supabase secrets `ROUTINE_FIRE_URL` / `ROUTINE_TOKEN` hold the same values that `scripts/capture.sh` / `scripts/capture.ps1` read from
`VAULT_FIRE_URL` / `VAULT_FIRE_TOKEN`: the scripts are for your shell, the secrets are for the function, and they are deliberately not renamed
to match. `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are injected by Supabase automatically (never set them yourself). The function's
`anthropic-beta` header is the beta gate for the Routine fire API.

## Known gaps

- The `captures` table's `done` status and `manual` source are never written by anything yet (no routine writes back), so a URL whose
  Routine run failed after `fired` stays `duplicate` on the next capture attempt.
- Phase 5b full-text search is not started.
