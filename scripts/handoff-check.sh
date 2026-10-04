#!/usr/bin/env bash
# Does a change that alters the project's state also update handoff.md? (rule: CLAUDE.md "Keep handoff.md current").
#
#   bash scripts/handoff-check.sh <base> <head>   CI mode: judge the commits base..head; exit 1 when handoff.md is missing.
#   bash scripts/handoff-check.sh --hook          Claude Code Stop hook (.claude/settings.json): judge this branch against
#                                                 origin/main plus uncommitted and untracked files; print a "block" decision
#                                                 so the session updates handoff.md before it ends.
#
# Routine output and captures do not need a handoff line (Routines never edit handoff.md), so these paths are exempt:
# raw/, wiki/pages/, wiki/stars/, wiki/index.md, wiki/log.md, wiki/hot.md, wiki/github-stars.md, wiki/hot-list/ reports
# and snapshot (not _config.yaml), inbox/, agents/, outputs/health/. Anything else counts: routines/, scripts/, skills/,
# .claude/, .github/, config, CLAUDE.md / AGENTS.md, outputs/ reports.
set -uo pipefail

EXEMPT='^(raw/|wiki/pages/|wiki/stars/|wiki/index\.md$|wiki/log\.md$|wiki/hot\.md$|wiki/github-stars\.md$|wiki/hot-list/(20[0-9]{2}-W[0-9]{2}\.md|_snapshot\.json)$|inbox/|agents/|outputs/health/)'

judge() {   # stdin: changed paths, one per line. Prints the paths that need a handoff update; status 1 if handoff.md is missing.
  local files counted
  files=$(sort -u | sed '/^$/d')
  [ -z "$files" ] && return 0
  printf '%s\n' "$files" | grep -qx 'handoff.md' && return 0
  counted=$(printf '%s\n' "$files" | grep -Ev "$EXEMPT" || true)
  [ -z "$counted" ] && return 0
  printf '%s\n' "$counted"
  return 1
}

if [ "${1:-}" = "--hook" ]; then
  input=$(cat 2>/dev/null || true)
  # Second stop in a row: the session was already told once; let it end rather than loop.
  printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
  cd "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || exit 0
  [ -f handoff.md ] || exit 0
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
  case "$branch" in main|hot-list/*|lint/*|HEAD|"") exit 0 ;; esac   # Routine branches, and main (Routines push there)
  git rev-parse -q --verify origin/main >/dev/null || exit 0
  base=$(git merge-base origin/main HEAD 2>/dev/null) || exit 0
  missing=$( { git diff --name-only "$base" HEAD; git diff --name-only HEAD; git ls-files --others --exclude-standard; } | judge ) && exit 0
  list=$(printf '%s' "$missing" | head -8 | sed 's/^/  - /')
  reason="handoff.md is not updated, but this branch changed project state:
$list
Before ending, update handoff.md per skills/keeping-handoff-docs/SKILL.md (In flight rows you touched, Recently done, one Session log line) and commit it with the change. If this session really changed nothing worth handing off, say so in one line and stop."
  esc=$(printf '%s' "$reason" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/\\t/g' | awk 'NR>1{printf "\\n"} {printf "%s", $0}')
  printf '{"decision": "block", "reason": "%s"}\n' "$esc"
  exit 0
fi

if [ $# -ne 2 ]; then
  echo "usage: $0 <base> <head> | --hook" >&2
  exit 2
fi
if missing=$(git diff --name-only "$1" "$2" | judge); then
  echo "handoff: ok"
  exit 0
fi
echo "::warning file=handoff.md::This change alters project state but does not update handoff.md (CLAUDE.md: Keep handoff.md current)."
echo "handoff.md not updated; files that need a handoff line:"
printf '%s\n' "$missing" | sed 's/^/  - /'
exit 1
