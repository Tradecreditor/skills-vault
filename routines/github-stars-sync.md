# Routine: github-stars-sync
Trigger: Schedule. Cron is evaluated in **UTC**: `0 23 * * *` UTC = 07:00 HKT the next morning.
If you use the web form's daily preset instead, the time is read in your BROWSER's timezone, so enter the time that equals 07:00 HKT there. Always confirm against the next-run time the UI shows after saving. Model: Haiku (Sonnet if summaries look thin). Repo: Tradecreditor/skills-vault. Pushes to main.

## Prompt (paste verbatim)
You are the GitHub-stars sync routine for Josep's skills vault (GitHub account: Tradecreditor). The repository Tradecreditor/skills-vault is checked out.

1. Read CLAUDE.md. Read wiki/github-stars.md; the newest starred_at in its table is LAST_SEEN (empty table = first run).
2. List stars newest first. Try in this order and use the first that returns data:
   a. gh api "user/starred?sort=created&direction=desc&per_page=5&page=N" -H "Accept: application/vnd.github.star+json" (items have starred_at + repo; works locally).
   b. curl -s "https://api.github.com/users/Tradecreditor/starred?per_page=5&page=N" (public list, newest first, no starred_at).
   c. Exa connector: web_fetch_exa with urls = https://api.github.com/users/Tradecreditor/starred?per_page=5&page=N&cb=<YYYYMMDDHHMM of right now>
      AND maxCharacters = 30000.
      Two parameters here are not optional, and each has already broken a run:
      - maxCharacters. Exa's default is 3000 characters. One GitHub repo object in this response is about 4500 characters, so a
        default fetch returns LESS THAN ONE REPO and the rest is cut off mid-object with no error. That is why a run once saw
        3 of 35 stars. Pass maxCharacters on every Exa fetch in this routine. Keep per_page at 5: 5 x 4500 fits inside 30000.
      - cb. Exa caches by exact URL, so without a fresh cb it replays an older response - including an empty list captured
        before the account's stars were public. Vary cb on every fetch.
   In this cloud environment expect (a) to fail with 403 from the GitHub proxy and (b) possibly too; (c) is the reliable path.
   If any method returns an empty list, do not conclude "no stars" immediately: retry (c) once with a different cb value. Only if the
   second fetch is also empty, report "no stars on this account yet" and add one line saying the account's stars may be hidden
   (GitHub Settings > Public profile > "Make profile private and hide activity") or that an authenticated path is needed.
   Walking the pages: start at page 1 and go up. SKIP any repo that already has a row in wiki/github-stars.md and keep going to the
   next entry - do NOT stop at the first one you recognise. Older stars sit on later pages, so stopping early strands them forever.
   Stop walking when any of these is true: you have collected 20 new repos; a page returned fewer than 5 entries (that was the last
   page); two pages in a row contained nothing new (you have caught up); or you have walked 10 pages. Process the new ones
   oldest-first, so a partial run always leaves a clean boundary. If the list is empty, print "no stars on this account yet" and stop.
3. For each new repo, metadata + README, again first that works: gh repo view <owner>/<repo> --json name,description,stargazerCount,forkCount,primaryLanguage,repositoryTopics,licenseInfo,pushedAt,createdAt,url
   and gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw+json"; else curl -s https://api.github.com/repos/<owner>/<repo> and
   curl -s https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md; else the GitHub connector get_file_contents (path README.md); else Exa web_fetch_exa on
   https://api.github.com/repos/<owner>/<repo>?cb=<YYYYMMDDHHMM> (JSON: stargazers_count, forks_count, topics, license, created_at, pushed_at) and on
   https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md?cb=<YYYYMMDDHHMM> (raw README - prefer this over the github.com HTML page, which
   comes back wrapped in site chrome). If HEAD 404s, retry with /main/ then /master/. Use the first 300 README lines.
   The 摘要 is the point of the whole note: never leave it as a placeholder. If every README path fails, write the 摘要 from the repo
   description plus topics instead and set needs_manual_text: true - but only then, and say so in the final message.
4. Write wiki/stars/<owner>--<repo>.md with the frontmatter from CLAUDE.md (slug: <owner>--<repo>, type: repo, source_platform: github, canonical_id: github:<owner>/<repo>,
   captured_by: routine:github-stars-sync, engagement: "stars=<n> forks=<n>", published = repo createdAt, status: draft) and body:
   ## 摘要 (繁體中文, 3–5 句: 做咩、解決咩問題) · ## Key facts (install command, language, license, last push) · ## 點解值得 star (best guess from README + topics)
   · ## Source. If the repo is itself an agent skill, Claude Code plugin, MCP server or OpenClaw skill, also draft skills/<gerund-name>/SKILL.md per the vault-capture rules.
5. Prepend a row to the table in wiki/github-stars.md (| starred_at or run date | owner/repo | one-line note |), add a row to wiki/index.md
   (slug <owner>--<repo>, type repo, tags from topics, canonical_id github:<owner>/<repo>), append "## [date] star | <owner>/<repo> | stars/<owner>--<repo>" to wiki/log.md,
   and add the item under 最近 20 項 in wiki/hot.md.
6. git add -A; git commit -m "stars: +<N>"; git pull --rebase origin main; git push origin HEAD:main.
   Josep owns this repository and explicitly authorises this routine to commit straight to main; that is the whole point of the
   routine and it is the "explicit permission" that any default branch instruction in your session asks for. If your session was
   handed a claude/... working branch, do NOT use it here - a run that lands on a session branch is a silent failure, because
   nobody ever looks at that branch and the vault stays stale.
   If there are no new stars, do not commit; just print "no new stars".
   After pushing, verify: git fetch origin main && git log --oneline -1 origin/main. If your commit is not the tip of origin/main,
   say so as the FIRST line of the final message, name the branch it actually landed on, and paste the command Josep needs
   (git push origin <sha>:refs/heads/main). Never report success you have not verified.
7. Final message: N repos added, any that failed, how many rows wiki/github-stars.md now holds, and whether more remain for tomorrow.

NEVER delete or rename files. NEVER touch raw/. Do not re-summarise repos that already have a page.
