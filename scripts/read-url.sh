#!/usr/bin/env bash
# Read a URL as text, for any agent or routine (CLAUDE.md "Reading a URL"). Jina Reader first, then a direct fetch.
# The page goes to stdout; one line "reader: <name>" goes to stderr so the caller can record which reader produced it.
#
#   bash scripts/read-url.sh [--fresh] [--json] <url>
#     --fresh   send X-No-Cache: true to Jina. Use it for anything re-read: a starred list, a weekly page, a search result.
#     --json    ask Jina for JSON (Accept: application/json; the page is in .data.content). The direct reader prints the body as is.
#
# Order:
#   1. Jina Reader (r.jina.ai). When JINA_API_KEY is set it is sent as a Bearer token from inside this script, so the key never
#      appears on a command line. An anonymous call can get 401 "bad IP reputation" from a cloud IP; a keyed call does not.
#      On 429 wait 20 s and retry once. Any other failure moves on.
#   2. Direct fetch of the URL with curl. Works locally, and in a cloud session only when the host is in the environment's
#      allowed domains. HTML is reduced to markdown-ish text (headings, list items, links kept) with Python's html.parser.
#   3. Nothing worked: exit 2 and name the host. The caller's next reader is the Exa MCP (web_fetch_exa), which a shell cannot call
#      (CLAUDE.md "Reading a URL": Jina first, then Exa).
# Exit: 0 ok, 2 every reader failed, 64 usage.
set -uo pipefail

fresh=0 json=0 url=""
while [ $# -gt 0 ]; do
  case "$1" in
    --fresh) fresh=1 ;;
    --json) json=1 ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    -*) echo "read-url: unknown option $1" >&2; exit 64 ;;
    *) url="$1" ;;
  esac
  shift
done
[ -n "$url" ] || { echo "usage: $0 [--fresh] [--json] <url>" >&2; exit 64; }
case "$url" in http://*|https://*) ;; *) url="https://$url" ;; esac
host=$(printf '%s' "$url" | sed -E 's#^[a-z]+://([^/:?#]+).*#\1#')

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

jina() {   # $1 = output file; prints the HTTP status
  local args=(-s -m 60 -o "$1" -w '%{http_code}')
  [ "$fresh" = 1 ] && args+=(-H "X-No-Cache: true")
  [ "$json" = 1 ] && args+=(-H "Accept: application/json")
  if [ -n "${JINA_API_KEY:-}" ]; then
    # Header read from a file descriptor, not argv, so the key is not visible in the process list.
    curl "${args[@]}" -H @<(printf 'Authorization: Bearer %s\n' "$JINA_API_KEY") "https://r.jina.ai/$url" 2>/dev/null
  else
    curl "${args[@]}" "https://r.jina.ai/$url" 2>/dev/null
  fi
}

reader="jina"; [ -n "${JINA_API_KEY:-}" ] && reader="jina+key"
code=$(jina "$tmp/jina")
if [ "$code" = 429 ]; then sleep 20; code=$(jina "$tmp/jina"); fi
if [ "$code" = 200 ] && [ -s "$tmp/jina" ]; then
  cat "$tmp/jina"; echo "reader: $reader" >&2; exit 0
fi
why="jina $code"
[ "$code" = 401 ] && [ -z "${JINA_API_KEY:-}" ] && why="jina 401 (anonymous call refused; set JINA_API_KEY)"

meta=$(curl -sL --compressed -m 45 -A "Mozilla/5.0 (compatible; skills-vault-reader)" \
  -o "$tmp/direct" -w '%{http_code} %{content_type}' "$url" 2>/dev/null)
dcode=${meta%% *}; ctype=${meta#* }
if [ "$dcode" = 200 ] && [ -s "$tmp/direct" ]; then
  if [ "$json" = 0 ] && printf '%s' "$ctype" | grep -qi 'html'; then
    python3 -I - "$tmp/direct" <<'PY'
import sys
from html.parser import HTMLParser

SKIP = {"script", "style", "noscript", "svg", "template", "head"}
BLOCK = {"p", "div", "section", "article", "main", "header", "footer", "nav", "aside", "tr", "table",
         "ul", "ol", "br", "hr", "blockquote", "pre", "form", "figure"}

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.href, self.title, self.in_title = [], 0, None, "", False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.in_title = True
        if tag in SKIP: self.skip += 1; return
        if tag in BLOCK: self.out.append("\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"): self.out.append("\n" + "#" * int(tag[1]) + " ")
        elif tag == "li": self.out.append("\n- ")
        elif tag == "a" and a.get("href"): self.href = a["href"]; self.out.append("[")
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag in SKIP: self.skip = max(0, self.skip - 1); return
        if tag == "a" and self.href is not None: self.out.append("](" + self.href + ")"); self.href = None
        elif tag in BLOCK or tag.startswith("h") and tag[1:].isdigit(): self.out.append("\n")
    def handle_data(self, data):
        if self.in_title: self.title += data
        if not self.skip: self.out.append(data)

p = Text()
with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
    p.feed(f.read())
lines = [" ".join(l.split()) for l in "".join(p.out).splitlines()]
body, blank = [], False
for l in lines:
    if l in ("", "[]()"):
        if not blank and body: body.append("")
        blank = True
    else:
        body.append(l); blank = False
if p.title.strip(): print("Title: " + " ".join(p.title.split()) + "\n")
print("\n".join(body).strip())
PY
  else
    cat "$tmp/direct"
  fi
  echo "reader: direct ($why)" >&2
  exit 0
fi

echo "read-url: every reader failed for $url: $why; direct ${dcode:-000}. Next reader: Exa web_fetch_exa (CLAUDE.md \"Reading a URL\")." >&2
hint=""; [ -z "${JINA_API_KEY:-}" ] && hint=" (or set JINA_API_KEY)"
[ "${dcode:-000}" = 000 ] && echo "read-url: $host is unreachable from here. In a cloud session, add $host to the environment's allowed domains$hint." >&2
exit 2
