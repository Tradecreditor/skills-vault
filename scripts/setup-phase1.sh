#!/usr/bin/env bash
# Phase 1 helper for macOS / Linux / WSL. Idempotent; prints what it cannot do automatically.
set -u
VAULT_DIR="${VAULT_DIR:-$HOME/skills-vault}"
REPO="Tradecreditor/skills-vault"
say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }
need() { command -v "$1" >/dev/null 2>&1 || { echo "  missing: $1  -> $2"; return 1; }; return 0; }

say "1/6 tools"
ok=1
need git "https://git-scm.com" || ok=0
need gh "https://cli.github.com (then: gh auth login)" || ok=0
need node "Node 20+ (https://nodejs.org)" || ok=0
need python3 "Python 3.11+" || ok=0
need pipx "macOS: brew install pipx && pipx ensurepath · Debian/Ubuntu: sudo apt install pipx · else: python3 -m pip install --user --break-system-packages pipx" || ok=0
[ $ok = 1 ] || echo "  install the missing tools above, then re-run this script"

say "2/6 vault location"
if [ -f "wiki/index.md" ]; then
  VAULT_DIR="$(pwd)"
elif [ -f "$VAULT_DIR/wiki/index.md" ]; then
  cd "$VAULT_DIR" || { echo "vault not found: run this from your skills-vault folder"; exit 2; }
else
  echo "vault not found: run this from your skills-vault folder"
  exit 2
fi
echo "  vault: $VAULT_DIR"
if [ -d ".git" ]; then git pull --rebase -q && echo "  updated"; fi
if gh auth status >/dev/null 2>&1; then gh auth setup-git >/dev/null 2>&1 || true; else echo "  run: gh auth login   (needed if you want to push changes back; the repo itself is public)"; fi

say "3/6 Agent-Reach (reader toolbox; decision 1/4)"
if command -v agent-reach >/dev/null 2>&1; then echo "  already installed"; else
  pipx install https://github.com/Panniantong/agent-reach/archive/main.zip && echo "  installed agent-reach" || echo "  pipx install failed; see https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md"
fi
command -v agent-reach >/dev/null 2>&1 && { agent-reach install --env=auto || true; echo "  -> review the check above, then run:  agent-reach install --env=auto --system   (and later: agent-reach doctor)"; }

say "4/6 Firecrawl CLI (generic web fallback)"
command -v firecrawl >/dev/null 2>&1 && echo "  already installed" || echo "  run:  npx -y firecrawl-cli@latest init --all --browser   (uses your existing Firecrawl account)"

say "5/6 Claude Code plugin marketplace"
if command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add "$REPO" --scope user && echo "  marketplace tradecreditor-vault added" || echo "  (if it says already added, fine; otherwise in Claude Code run: /plugin marketplace add $REPO)"
  claude plugin install skills-vault@tradecreditor-vault --scope user && echo "  plugin skills-vault installed (user scope)" || echo "  (if it says already installed, fine; otherwise in Claude Code run: /plugin install skills-vault@tradecreditor-vault)"
  echo "  repo is public, so the marketplace add needs no token; gh auth setup-git (done above) only matters if you also push changes back"
elif command -v npx >/dev/null 2>&1; then
  echo "  Claude Code CLI not found (install from https://code.claude.com); installing vault-capture/vault-search into ~/.claude/skills meanwhile"
  npx -y skills add "$REPO" --skill vault-capture --skill vault-search -a claude-code -g -y || echo "  npx skills add failed; after installing Claude Code run: claude plugin marketplace add $REPO && claude plugin install skills-vault@tradecreditor-vault"
else echo "  Claude Code CLI not found; install from https://code.claude.com, then: claude plugin marketplace add $REPO && claude plugin install skills-vault@tradecreditor-vault"; fi

say "6/6 manual steps"
cat <<TXT
  a) Obsidian 1.12.7+: File > Open folder as vault -> $VAULT_DIR
     Settings > Community plugins > Browse "Git" -> install + enable ->
       Auto commit-and-sync interval: 10 (min) · Pull on startup: on · Auto pull interval: 10 · Pull before push: on
  b) SessionStart hook for every project: merge templates/claude-settings-user.json into ~/.claude/settings.json
  c) Smoke test: cd $VAULT_DIR && claude   then paste  https://x.com/Jackywine/status/2095750518941659567  and say "save"
     then ask: "have I saved anything about Obsidian?"  (vault-search)
  d) Optional Exa key for the mcporter route: agent-reach handles Exa without a key via MCP; in Claude Code the Exa connector is already there.
TXT
