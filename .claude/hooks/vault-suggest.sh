#!/usr/bin/env bash
# SessionStart hook: suggest vault entries relevant to the current project (title + tags of index rows, skill descriptions).
# Register in ~/.claude/settings.json (see templates/claude-settings-user.json). Exits 0 silently when nothing matches.
set -u
INPUT=$(cat 2>/dev/null || true)
CWD=$(printf '%s' "$INPUT" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
[ -z "$CWD" ] && CWD="$PWD"
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
V="$HERE/../.."; [ -f "$V/wiki/index.md" ] || V="${VAULT_DIR:-}"; [ -n "$V" ] && [ -f "$V/wiki/index.md" ] || V="$HOME/Vaults/skills-vault"
[ -f "$V/wiki/index.md" ] || exit 0
V=$(cd "$V" && pwd)
case "$CWD" in "$V"|"$V"/*) exit 0;; esac                    # inside the vault itself: nothing to suggest
T=""; command -v timeout >/dev/null 2>&1 && T="timeout 20"; command -v gtimeout >/dev/null 2>&1 && T="gtimeout 20"
( cd "$V" && $T git -c core.askPass=true pull -q --rebase --autostash ) >/dev/null 2>&1 || true

STOP='dependencies|devdependencies|peerdependencies|version|scripts|name|description|license|private|type|main|true|false|null|import|from|const|function|return|http|https|github|readme|project|this|that|with|your|have|will|when|then|file|files|using|used|make|sure|also|into|about|should|other|more|than|each|only|does|which|what|node_modules|package|packages|build|start|test|tests|testing|lint|dev|prod|src|dist|latest|index|config|default|example|json|yaml|yml|todo|note|notes|user|users|data|app|apps|api|web|site|page|pages|list|item|items|value|values|key|keys|new|old|add|set|get|run|runs|open|close|read|write|create|update|delete|remove|install|npm|npx|yarn|pnpm|pip|python|node|shell|bash|code|codes|tool|tools|skill|skills|repo|repos|post|posts|video|videos|article|concept|draft|verified|deprecated|threads|youtube|instagram|twitter|small|internal|simple|basic|module|modules|library|support|feature|features|require|requires|engines|author|email|homepage|bugs|keywords|workspaces|resolutions|overrides|typescript|javascript|react|next|vite'
KW=$(cat "$CWD"/package.json "$CWD"/requirements*.txt "$CWD"/pyproject.toml "$CWD"/go.mod "$CWD"/Cargo.toml "$CWD"/Gemfile "$CWD"/README.md "$CWD"/CLAUDE.md 2>/dev/null \
  | tr -cs 'A-Za-z0-9._-' '\n' | tr 'A-Z' 'a-z' | sed -E 's/^[._-]+//; s/[._-]+$//' \
  | grep -E '^[a-z][a-z0-9._-]{3,30}$' | grep -vxE "$STOP" \
  | sort | uniq -c | sort -rn | awk '{print $2}' | head -60)
[ -z "$KW" ] && exit 0
PAT=$(printf '%s\n' "$KW" | sed -E 's/[][\\.*^$+?(){}|\/]/\\&/g' | paste -sd'|' -)
MATCHES=$( {
  grep -E '^\| ' "$V/wiki/index.md" | grep -vE '^\| slug |^\|-' \
    | awk -F'|' -v pat="$PAT" 'BEGIN{IGNORECASE=1} { t=$4; g=$8; gsub(/^ +| +$/,"",t); gsub(/^ +| +$/,"",g); s=$2; gsub(/^ +| +$/,"",s); if (tolower(t" "g) ~ pat) print t" ("s")" }' ;
  grep -ilE "^description:.*($PAT)" "$V"/skills/*/SKILL.md 2>/dev/null | sed 's#.*/skills/\([^/]*\)/SKILL.md#skill: \1#' ;
} | sort -u | head -6 )
[ -z "$MATCHES" ] && exit 0
CTX=$(printf 'Skills vault (Tradecreditor/skills-vault) entries that look relevant to this project:\n%s\nInstall a skill: npx skills add Tradecreditor/skills-vault --skill <name>  (Claude Code: /plugin install skills-vault@tradecreditor-vault). For more, read %s/wiki/hot.md then wiki/index.md, or run the vault-search skill.' "$(printf '%s\n' "$MATCHES" | sed 's/^/- /')" "$V")
CTX_JSON=""
command -v python3 >/dev/null 2>&1 && CTX_JSON=$(printf '%s' "$CTX" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || true)
if [ -z "$CTX_JSON" ]; then
  CTX_JSON="\"$(printf '%s' "$CTX" | tr '\t\r' '  ' | tr -d '\000-\010\013\014\016-\037' | sed 's/\\/\\\\/g; s/"/\\"/g' | tr '\n' ' ')\""
fi
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$CTX_JSON"
