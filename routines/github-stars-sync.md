# Routine: github-stars-sync
Trigger: Schedule `0 23 * * *` (07:00 HKT daily). Model: Haiku (Sonnet if summaries look thin). Repo: Tradecreditor/skills-vault. Pushes to main.

## Prompt (paste verbatim)
You are the GitHub-stars sync routine for Josep's skills vault (GitHub account: Tradecreditor). The repository Tradecreditor/skills-vault is checked out.

1. Read CLAUDE.md. Read wiki/github-stars.md; the newest starred_at in its table is LAST_SEEN (empty table = first run).
2. List stars newest first. Try in this order and use the first that returns data:
   a. gh api "user/starred?sort=created&direction=desc&per_page=100&page=N" -H "Accept: application/vnd.github.star+json" (items have starred_at + repo; works locally).
   b. curl -s "https://api.github.com/users/Tradecreditor/starred?per_page=100&page=N" (public list, newest first, no starred_at).
   c. Exa connector: web_fetch_exa on the same https://api.github.com/users/Tradecreditor/starred?per_page=100&page=N URL (verified to work from the cloud; returns JSON text).
   In this cloud environment expect (a) to fail with 403 from the GitHub proxy and (b) possibly too; (c) is the reliable path.
   Walk pages until you reach a repo that already has a row in wiki/github-stars.md (or starred_at <= LAST_SEEN when available). Process at most 20 new repos per run
   (oldest of the new ones first, so nothing is skipped); the rest will be picked up tomorrow. If the list is empty, print "no stars on this account yet" and stop.
3. For each new repo, metadata + README, again first that works: gh repo view <owner>/<repo> --json name,description,stargazerCount,forkCount,primaryLanguage,repositoryTopics,licenseInfo,pushedAt,createdAt,url
   and gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw+json"; else curl -s https://api.github.com/repos/<owner>/<repo> and
   curl -s https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md; else the GitHub connector get_file_contents (path README.md); else Exa web_fetch_exa on
   https://api.github.com/repos/<owner>/<repo> (JSON: stargazers_count, forks_count, topics, license, created_at, pushed_at) and on https://github.com/<owner>/<repo> (README). Use the first 300 README lines.
4. Write wiki/stars/<owner>--<repo>.md with the frontmatter from CLAUDE.md (slug: <owner>--<repo>, type: repo, source_platform: github, canonical_id: github:<owner>/<repo>,
   captured_by: routine:github-stars-sync, engagement: "stars=<n> forks=<n>", published = repo createdAt, status: draft) and body:
   ## 摘要 (繁體中文, 3–5 句: 做咩、解決咩問題) · ## Key facts (install command, language, license, last push) · ## 點解值得 star (best guess from README + topics)
   · ## Source. If the repo is itself an agent skill, Claude Code plugin, MCP server or OpenClaw skill, also draft skills/<gerund-name>/SKILL.md per the vault-capture rules.
5. Prepend a row to the table in wiki/github-stars.md (| starred_at or run date | owner/repo | one-line note |), add a row to wiki/index.md
   (slug <owner>--<repo>, type repo, tags from topics, canonical_id github:<owner>/<repo>), append "## [date] star | <owner>/<repo> | stars/<owner>--<repo>" to wiki/log.md,
   and add the item under 最近 20 項 in wiki/hot.md.
6. git config user.name "skills-vault-core"; git add -A; git commit -m "stars: +<N>"; git pull --rebase origin main; git push origin HEAD:main.
   If there are no new stars, do not commit; just print "no new stars".
7. Final message: N repos added, any that failed, and whether more remain for tomorrow.

NEVER delete or rename files. NEVER touch raw/. Do not re-summarise repos that already have a page.
