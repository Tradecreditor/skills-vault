#!/usr/bin/env bash
# Plugin hook (hooks/hooks.json): keep Jeff's Notion database "Skill Installs" current without anyone asking.
#   PostToolUse (Bash): when the command Claude just ran installed, removed or updated a skill or a Claude Code plugin
#                       (npx skills add/remove/update, claude plugin install/uninstall/update/enable/disable), record this
#                       project's installs; with -g / --global or a plugin command, also this computer's global installs.
#   SessionStart:       compare this project's (and the computer's) installs with the last recorded state and record only
#                       what changed (--if-changed: a local fingerprint, no network when nothing changed, at most 7 days old).
# Runs ${CLAUDE_PLUGIN_ROOT}/scripts/skills-inventory.py (the vault's own script; the plugin is the vault repository).
# Always exits 0 and never blocks Claude. Silent when NOTION_TOKEN is not set, when the input is not a hook payload, or
# when nothing changed. Never prints NOTION_TOKEN. Windows: needs Git Bash on PATH (as the vault's other hooks do); the
# same logic is in skill-install-sync.ps1 for a PowerShell-only setup.
set -u
[ -n "${NOTION_TOKEN:-}" ] || exit 0
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SCRIPT="$ROOT/scripts/skills-inventory.py"
[ -f "$SCRIPT" ] || exit 0
INPUT=$(cat 2>/dev/null || true)
[ -n "$INPUT" ] || exit 0

# a Python that really runs (on Windows `python3` may be the Store stub that only prints "Python was not found")
PY=""
for cand in "py -3" python3 python; do
  if $cand -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1; then PY="$cand"; break; fi
done
[ -n "$PY" ] || exit 0

field() {   # first string value of a JSON key anywhere in the payload (hook payloads are flat enough for this)
  printf '%s' "$INPUT" | $PY -c 'import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    sys.exit(0)
def find(o,k):
    if isinstance(o,dict):
        if k in o and isinstance(o[k],str): return o[k]
        for v in o.values():
            r=find(v,k)
            if r is not None: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v,k)
            if r is not None: return r
r=find(d,sys.argv[1]); print(r if r is not None else "")' "$1" 2>/dev/null
}

EVENT=$(field hook_event_name)
PROJECT="${CLAUDE_PROJECT_DIR:-$(field cwd)}"
[ -n "$PROJECT" ] && [ -d "$PROJECT" ] || PROJECT="$PWD"
GLOBAL=0
case "$EVENT" in
  PostToolUse)
    CMD=$(field command)
    [ -n "$CMD" ] || exit 0
    printf '%s' "$CMD" | grep -qE '(^|[^A-Za-z0-9_-])(skills[[:space:]]+(add|remove|rm|update|experimental_install|experimental_sync)|claude[[:space:]]+plugin[[:space:]]+(install|uninstall|update|enable|disable))([[:space:]]|$)' || exit 0
    printf '%s' "$CMD" | grep -qE '(^|[[:space:]])(-g|--global)([[:space:]]|$)|claude[[:space:]]+plugin' && GLOBAL=1
    ;;
  SessionStart) GLOBAL=1 ;;
  *) exit 0 ;;
esac

report() {   # print the summary line unless it says nothing happened (SessionStart output becomes context: keep it quiet)
  case "$1" in
    *"unchanged since the last run"*|*"created=0 updated=0 removed=0"*) [ "$EVENT" = PostToolUse ] && printf '%s\n' "$1" ;;
    *) printf '%s\n' "$1" ;;
  esac
}
OUT=$($PY "$SCRIPT" --root "$PROJECT" --if-changed 2>/dev/null) && report "$OUT"
if [ "$GLOBAL" = 1 ]; then
  OUT=$($PY "$SCRIPT" --global --if-changed 2>/dev/null) && report "$OUT"
fi
exit 0
