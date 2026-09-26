#!/usr/bin/env bash
# Usage: search.sh "<query words>"  — ORs the words (literal, case-insensitive); searches index rows, skill descriptions, page frontmatter, then full text.
set -u
Q="${*:-}"
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
V="$HERE/../../.."; [ -f "$V/wiki/index.md" ] || V="${VAULT_DIR:-}"; [ -n "$V" ] && [ -f "$V/wiki/index.md" ] || V="$HOME/skills-vault"
[ -f "$V/wiki/index.md" ] || { echo "vault not found (set VAULT_DIR)"; exit 2; }
V=$(cd "$V" && pwd)
# split on whitespace, drop empties and 1-char words, escape regex metacharacters
PAT=$(printf '%s\n' $Q | sed -E '/^.?$/d; s/[][\\.*^$+?(){}|\/]/\\&/g' | paste -sd'|' -)
[ -z "$PAT" ] && { echo "usage: search.sh <query words>"; exit 1; }
echo "## index rows matching: $Q"
grep -E '^\| ' "$V/wiki/index.md" | grep -vE '^\| slug |^\|-' | grep -iE "($PAT)" || echo "(none)"
echo; echo "## skills (description match)"
out=$(grep -iHE "^description:.*($PAT)" "$V"/skills/*/SKILL.md 2>/dev/null | sed "s#^$V/##; s#/SKILL.md:description:#  —#")
if [ -n "$out" ]; then printf '%s\n' "$out"; else echo "(none)"; fi
echo; echo "## pages / stars (frontmatter match)"
out=$(grep -ilE "^(title|tags|type|source_platform|author):.*($PAT)" "$V"/wiki/pages/*.md "$V"/wiki/stars/*.md 2>/dev/null | sed "s#^$V/##")
if [ -n "$out" ]; then printf '%s\n' "$out"; else echo "(none)"; fi
echo; echo "## full text (top 15 files)"
out=$(grep -rilE "($PAT)" "$V/wiki/pages" "$V/wiki/stars" "$V/skills" "$V/wiki/hot-list" 2>/dev/null | head -15 | sed "s#^$V/##")
if [ -n "$out" ]; then printf '%s\n' "$out"; else echo "(none)"; fi
