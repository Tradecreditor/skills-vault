#!/usr/bin/env bash
# Fire the capture-link Routine with one URL.
#   ./scripts/capture.sh https://x.com/someone/status/123
# Needs VAULT_FIRE_URL and VAULT_FIRE_TOKEN in the environment (see the bottom of this file).
set -euo pipefail
URL="${1:-}"
[ -n "$URL" ] || { echo "usage: $0 <url>" >&2; exit 2; }
: "${VAULT_FIRE_URL:?set VAULT_FIRE_URL - see the comment at the bottom of scripts/capture.sh}"
: "${VAULT_FIRE_TOKEN:?set VAULT_FIRE_TOKEN - see the comment at the bottom of scripts/capture.sh}"
case "$VAULT_FIRE_URL" in
  */fire) ;;
  *) echo "VAULT_FIRE_URL must end in /fire - a stray character there returns 404, which reads like a broken routine." >&2; exit 2;;
esac

code=$(curl -sS -o /tmp/vault-fire.out -w '%{http_code}' -X POST "$VAULT_FIRE_URL" \
  -H "Authorization: Bearer $VAULT_FIRE_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "content-type: application/json" \
  --data "$(printf '{"text":%s}' "$(printf '%s' "$URL" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")")
if [ "$code" -ge 200 ] && [ "$code" -lt 300 ]; then
  echo "fired: $URL"
  echo "The routine runs in the cloud; watch it at https://claude.ai/code/routines"
else
  echo "fire failed (HTTP $code):" >&2; cat /tmp/vault-fire.out >&2; echo >&2; exit 1
fi

# One-time setup, in ~/.bashrc or ~/.zshrc. The token is a secret: it can start runs on your account.
#   export VAULT_FIRE_URL="https://api.anthropic.com/v1/claude_code/routines/trig_XXXX/fire"
#   export VAULT_FIRE_TOKEN="<the token shown once when the API trigger was created>"
