#!/usr/bin/env bash
# Copy one routine's prompt to the clipboard, intact, ready to paste into claude.ai.
#   ./scripts/copy-prompt.sh github-stars-sync
#
# macOS/Linux twin of copy-prompt.ps1. That script exists because Windows PowerShell 5.1 reads
# files in the system ANSI code page unless told otherwise, silently turning 繁體中文 into
# mojibake before it reaches the clipboard. Bash on macOS/Linux has no such code-page trap, but
# clipboard tools can still re-encode or truncate what they're given - so this script keeps the
# same discipline: read the file as UTF-8 (always, via python3), copy it, then read the clipboard
# back and refuse to report success unless it matches byte-for-byte what was sent.
#
# Clipboard tool used, first one found: pbcopy (macOS), wl-copy (Wayland), xclip, xsel.
# If none is installed, the prompt is printed to stdout instead so it can still be copied by hand.
#
# Exit codes:
#   0  copied to the clipboard and the read-back matched byte-for-byte
#   1  routines/<name>.md not found, has no '## Prompt (paste verbatim)' heading, the file
#      itself contains a replacement character (wrong encoding saved at some point), or the
#      clipboard round-trip did not match (do NOT paste - copy the section out by hand instead)
#   2  usage error: no <routine-name> argument given
#   3  no clipboard tool found (pbcopy/wl-copy/xclip/xsel) - the prompt was printed to stdout
#      instead; this is not a failure of the extraction, just of clipboard access
set -euo pipefail

NAME="${1:-}"
if [ -z "$NAME" ]; then
  echo "usage: $0 <routine-name>   (e.g. github-stars-sync -> routines/github-stars-sync.md)" >&2
  exit 2
fi

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROUTINE_PATH="$HERE/../routines/$NAME.md"
if [ ! -f "$ROUTINE_PATH" ]; then
  echo "usage: $0 <routine-name>   (e.g. github-stars-sync -> routines/github-stars-sync.md)" >&2
  echo "not found: $ROUTINE_PATH" >&2
  exit 1
fi

MARKER='## Prompt (paste verbatim)'
if ! grep -qF "$MARKER" "$ROUTINE_PATH"; then
  echo "$NAME.md has no '$MARKER' section" >&2
  exit 1
fi

SENT=$(mktemp)
RECEIVED=$(mktemp)
trap 'rm -f "$SENT" "$RECEIVED"' EXIT

# Extract everything below the marker heading and trim leading/trailing blank lines, the same
# way the .ps1's $text.Substring(...).Trim() does. Read and written as UTF-8 throughout so the
# Chinese text is never touched, let alone stripped or altered.
python3 - "$ROUTINE_PATH" "$MARKER" > "$SENT" <<'PYEOF'
import sys
path, marker = sys.argv[1], sys.argv[2]
with open(path, encoding='utf-8') as f:
    text = f.read()
i = text.find(marker)
body = text[i + len(marker):].strip()
sys.stdout.write(body)
PYEOF

if LC_ALL=C.UTF-8 grep -qF '�' "$SENT"; then
  echo "The file itself contains a replacement character - it was saved in the wrong encoding at some point." >&2
  exit 1
fi

COPY_CMD=()
PASTE_CMD=()
if command -v pbcopy >/dev/null 2>&1; then
  COPY_CMD=(pbcopy); PASTE_CMD=(pbpaste)
elif command -v wl-copy >/dev/null 2>&1; then
  COPY_CMD=(wl-copy); PASTE_CMD=(wl-paste --no-newline)
elif command -v xclip >/dev/null 2>&1; then
  COPY_CMD=(xclip -selection clipboard); PASTE_CMD=(xclip -o -selection clipboard)
elif command -v xsel >/dev/null 2>&1; then
  COPY_CMD=(xsel --clipboard --input); PASTE_CMD=(xsel --clipboard --output)
fi

if [ "${#COPY_CMD[@]}" -eq 0 ]; then
  cat "$SENT"
  echo >&2
  echo "no clipboard tool found (looked for pbcopy, wl-copy, xclip, xsel) - the prompt was printed to stdout above; copy it by hand into claude.ai/code/routines -> $NAME -> Instructions." >&2
  exit 3
fi

if ! "${COPY_CMD[@]}" < "$SENT"; then
  echo "clipboard copy failed (${COPY_CMD[*]}) - do NOT assume the clipboard holds the prompt." >&2
  exit 1
fi

if ! "${PASTE_CMD[@]}" > "$RECEIVED" 2>/dev/null; then
  echo "clipboard read-back failed (${PASTE_CMD[*]}) - could not verify what was copied; do NOT paste." >&2
  exit 1
fi

if ! LC_ALL=C.UTF-8 cmp -s "$SENT" "$RECEIVED"; then
  echo "Clipboard did not round-trip - do NOT paste this. Copy the prompt section out of $ROUTINE_PATH by hand instead." >&2
  exit 1
fi

CHARLEN=$(LC_ALL=C.UTF-8 python3 -c "import sys; print(len(open(sys.argv[1], encoding='utf-8').read()))" "$SENT")
CJK=$(LC_ALL=C.UTF-8 python3 -c "
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
print(len(re.findall(r'[一-鿿]', text)))
" "$SENT")

echo "copied $CHARLEN chars from $NAME.md ($CJK Chinese characters, verified intact)"
echo "Paste into claude.ai/code/routines -> $NAME -> Instructions (select all, delete, Ctrl+V)."
