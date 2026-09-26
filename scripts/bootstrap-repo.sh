#!/usr/bin/env bash
# First push of this scaffold to GitHub. Creates the public repo with gh if it does not exist yet. Run once from inside this folder.
set -euo pipefail
REPO="${1:-Tradecreditor/skills-vault}"
[ -f CLAUDE.md ] && [ -f wiki/index.md ] || { echo "run this from the scaffold folder (where CLAUDE.md lives)"; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "gh CLI missing: https://cli.github.com then gh auth login"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "run: gh auth login"; exit 1; }
[ -d .git ] || git init -q -b main
git add -A
git -c user.name="skills-vault-core" -c user.email="${VAULT_CORE_EMAIL:-skills-vault-core@users.noreply.github.com}" commit -q -m "init: skills vault scaffold" || true
if gh repo view "$REPO" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
  if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
    echo "remote main already has commits (e.g. an auto-generated README); rebasing on top of it"
    git pull --rebase --allow-unrelated-histories origin main || { echo "could not rebase onto remote main; resolve conflicts and re-run"; exit 1; }
  fi
  git push -u origin main
else
  gh repo create "$REPO" --public --source=. --remote=origin --push --description "Personal agent skills vault: Obsidian vault + LLM wiki + installable Agent Skills"
fi
echo "done: https://github.com/$REPO"
echo "next: bash scripts/setup-phase1.sh"
