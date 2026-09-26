#!/usr/bin/env bash
# Vault write rules over a commit range, judged by WHO is acting (GitHub account), not by commit metadata.
#   bash scripts/vault-guard-check.sh <base> <head> <actor-login>
#   env: VAULT_OWNER (default: GITHUB_REPOSITORY_OWNER or "Tradecreditor"), VAULT_CORE_LOGINS (optional, comma-separated extra core accounts)
# Rules:
#   everyone : raw/ is add-only (never modified, renamed or deleted, core included) · skills/*/SKILL.md must be valid
#              (name == folder, lowercase-hyphen, no claude/anthropic, description present, <=300 chars, contains "Use when")
#   non-core : may not delete or rename-away ANY file · may not touch protected paths: .github/ .claude/ .claude-plugin/
#              .obsidian/ routines/ scripts/ supabase/ templates/ CLAUDE.md AGENTS.md skills/*/scripts/
#   core     : deletions, renames and protected-path edits are allowed (audited/printed), never blocked
# Core = the repository owner account (Josep's own Claude Code sessions, Routines, obsidian-git) plus VAULT_CORE_LOGINS.
# Non-core = any other GitHub account, e.g. the machine account used by Codex / Gemini CLI / OpenClaw. Tokens inherit their account's role.
set -u
export LC_ALL=C.UTF-8
BASE="${1:?base}"; HEAD="${2:?head}"; ACTOR="${3:-unknown}"; FAIL=0
OWNER="${VAULT_OWNER:-${GITHUB_REPOSITORY_OWNER:-Tradecreditor}}"
CORE=",${OWNER},${VAULT_CORE_LOGINS:-},"; CORE="${CORE// /}"
lc() { printf '%s' "$1" | tr 'A-Z' 'a-z'; }
case "$(lc "$CORE")" in *",$(lc "$ACTOR"),"*) IS_CORE=1;; *) IS_CORE=0;; esac
echo "vault-guard: range $BASE..$HEAD, actor '$ACTOR' ($([ $IS_CORE = 1 ] && echo core || echo non-core); owner $OWNER)"

# 1) raw/ is immutable for everyone (add only)
CH=$(git diff --name-status -M50% "$BASE" "$HEAD" -- raw/ | grep -vE '^A' || true)
if [ -n "$CH" ]; then echo "::error::raw/ files may only be added, never modified, renamed or deleted:"; echo "$CH"; FAIL=1; else echo "raw/: ok"; fi

DEL=$(git diff --name-status -M50% "$BASE" "$HEAD" | awk '$1=="D" || $1 ~ /^R/ {print $0}')
PROT_PATTERN='^(\.github/|\.claude/|\.claude-plugin/|\.obsidian/|routines/|scripts/|supabase/|templates/|CLAUDE\.md$|AGENTS\.md$|skills/[^/]+/scripts/)'
# -z: NUL-separated raw paths. Without it git C-quotes any path with non-ASCII, quotes or spaces, and the pattern would never match.
PROT=$(git diff --name-status -z -M50% "$BASE" "$HEAD" | tr '\0' '\n' | grep -aE "$PROT_PATTERN" || true)

if [ $IS_CORE = 0 ]; then
  # 2) deletions (and renames, which delete the old path) only by core
  if [ -n "$DEL" ]; then
    echo "::error::'$ACTOR' is not a core account and may not delete or rename files. Retire entries with status: deprecated instead."
    echo "$DEL"; FAIL=1
  else echo "deletions/renames: none"; fi
  # 3) protected paths only by core
  if [ -n "$PROT" ]; then echo "::error::protected files changed by non-core account '$ACTOR':"; echo "$PROT"; FAIL=1; else echo "protected paths: untouched"; fi
else
  echo "core account: deletions, renames and protected-path edits allowed (audited)"
  [ -n "$DEL" ] && printf '%s\n' "$DEL" | sed 's/^/  /'
  [ -n "$PROT" ] && printf '%s\n' "$PROT" | sed 's/^/  protected: /'
  true
fi

# 4) skills/*/SKILL.md validity (everyone)
shopt -s nullglob
for f in skills/*/SKILL.md; do
  d=$(basename "$(dirname "$f")")
  fm=$(tr -d '\r' < "$f" | awk 'NR==1{ if ($0!="---") exit; next } $0=="---"{exit} {print}')
  n=$(printf '%s\n' "$fm" | grep -m1 -E '^name:' | sed -E "s/^name:[[:space:]]*//; s/^[\"']//; s/[\"'][[:space:]]*$//; s/[[:space:]]+$//")
  # description may be a plain, quoted or block (>- / |) scalar spanning several lines: join every indented continuation line before measuring
  desc=$(printf '%s\n' "$fm" | awk '
    /^description:/ { grab=1; sub(/^description:[[:space:]]*/, ""); v=$0; next }
    grab && /^[[:space:]]+[^[:space:]]/ { sub(/^[[:space:]]+/, ""); v = (v=="" ? $0 : v " " $0); next }
    grab { grab=0 }
    END { print v }' | sed -E "s/^[>|][+-]?[[:space:]]*//; s/^[\"']//; s/[\"'][[:space:]]*$//; s/[[:space:]]+$//")
  [ "$n" = "$d" ] || { echo "::error file=$f::frontmatter name '$n' must equal folder name '$d'"; FAIL=1; }
  [ -n "$desc" ] || { echo "::error file=$f::missing or empty description"; FAIL=1; }
  [ "${#desc}" -le 300 ] || { echo "::error file=$f::description longer than 300 characters"; FAIL=1; }
  [ -z "$desc" ] || printf '%s' "$desc" | grep -qF 'Use when' || { echo "::error file=$f::description must contain the phrase \"Use when\""; FAIL=1; }
  printf '%s' "$d" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$' || { echo "::error file=$f::folder name must be lowercase letters, digits and single hyphens"; FAIL=1; }
  case "$d" in *claude*|*anthropic*) echo "::error file=$f::skill names must not contain claude/anthropic"; FAIL=1;; esac
done
[ "$FAIL" = 0 ] && echo "vault-guard: all checks passed" || echo "vault-guard: FAILED"
exit $FAIL
