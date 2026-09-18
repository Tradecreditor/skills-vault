# Routine: weekly-hot-list
Trigger: Schedule `0 1 * * 1` (Monday 09:00 HKT). Model: Opus. Repo: Tradecreditor/skills-vault. Opens a PR (never pushes to main).

## Prompt (paste verbatim)
You are the weekly hot-list routine for Josep's skills vault. The repository Tradecreditor/skills-vault is checked out. Today is Monday; the window is the previous Monday 00:00 UTC to Sunday 23:59 UTC. Let WEEK be the ISO week label of that window, e.g. 2026-W37.

0. Read CLAUDE.md and wiki/hot-list/_config.yaml (thresholds, weights, topics, sources, cost caps). Every number below comes from that file; if the file and this prompt disagree, the file wins.
1. Candidates (respect cost_caps_per_run):
   a. GitHub: for each topic search repos created >= window start minus 90 days with stars >= 1000, sorted by stars (30 per topic), plus a breakout search
      (created >= window start, stars >= 1000, 50 results). Locally: gh search repos "<topic>" --created ">=<date>" --stars ">=1000" --sort stars --limit 30 --json fullName,stargazersCount,createdAt,description,url.
      In this cloud environment gh is proxy-blocked: use the GitHub connector tool search_repositories (query "<topic> created:>=<date> stars:>=1000", sort stars) or
      Exa web_fetch_exa on https://api.github.com/search/repositories?q=<topic>+created:>=<date>+stars:>=1000&sort=stars&per_page=30.
      Load wiki/hot-list/_snapshot.json; for every repo seen there or in wiki/stars/, fetch current stargazers_count (curl or Exa on https://api.github.com/repos/<o>/<r>)
      and compute stars_gained_7d = current - snapshot. Write the new snapshot for every repo you touched.
   b. X: if TWITTER_AUTH_TOKEN and TWITTER_CT0 are set, run twitter search "<topic>" -t Top --since <window start> --max 30 --json for each topic (Agent-Reach's twitter-cli);
      otherwise use the Exa connector: web_search_exa query "<topic> new tool OR skill OR MCP OR repo" with category tweet and startPublishedDate = window start, numResults 25.
      For EVERY candidate post fetch https://api.fxtwitter.com/<user>/status/<id> (via Exa web_fetch_exa if curl is blocked) and use only those likes / retweets / views / author values.
   c. Threads: Exa web_search_exa "<topic>" with query suffix site:threads.net and startPublishedDate = window start; read each post via Jina (https://r.jina.ai/<url>);
      like/repost counts come from Scrape Creators (/v1/threads/post, only if SC_API_KEY is set) or, if THREADS_APP_TOKEN is set, Meta oEmbed with &access_token=; otherwise count distinct authors only.
      Threads has no official trending feed, so label this signal "loud among posts found".
   d. Registries (corroboration only): skills.sh trending, ClawHub trending API, SkillsMP search for each topic; note weekly installs / rank where available.
   Group candidates by item (canonical GitHub repo when one exists, otherwise normalised product name). Dedupe: grep -rF "<canonical_id>" wiki/index.md wiki/pages wiki/stars; discard hits unless stars_gained_7d >= the dedupe update threshold (then it becomes an "update" entry and you append '- also trending WEEK (numbers)' under ## Notes of the existing page).
2. Gates and score exactly as _config.yaml: an item is eligible if it clears at least one gate on GitHub, X or Threads; component = min(1, metric / threshold); heat = weighted sum;
   x1.25 when gates are cleared on 2+ platforms; require gates on 2+ platforms OR heat >= single_source_min_heat; at least one winner must have cleared X or Threads; pick the top 3 (minimum 2).
   If fewer than 2 qualify, this is a quiet week: do not lower thresholds.
3. Write wiki/hot-list/WEEK.md: frontmatter (week, window, generated_at, sources_used, quiet_week: true|false) then
   ## 本週入選 (for each winner: name, one-line 繁中 summary, heat score, gates cleared, the exact numbers and URLs that justified it),
   ## 候選總表 (table of every candidate with numbers, whether each gate passed, heat), ## Watch (best 3 sub-threshold items), ## 方法 (queries run, caps hit, anything that failed).
   For each winner also: capture its primary source with the vault-capture procedure (raw/ + wiki/pages/<slug>.md with type and captured_by: routine:weekly-hot-list, tags including hot-list, WEEK),
   draft skills/<name>/SKILL.md only if it is an installable skill or a repeatable procedure, add rows to wiki/index.md and wiki/log.md ("## [date] hot-list | WEEK | hot-list/WEEK"),
   and replace the ## 本週熱門榜 section of wiki/hot.md with the 2–3 winners linking to the report.
4. Commit on a branch and open a PR (decision 6): git config user.name "skills-vault-core"; git checkout -b hot-list/WEEK; git add -A; git commit -m "hot-list: WEEK"; git push -u origin hot-list/WEEK;
   gh pr create --title "hot-list: WEEK" --body "<the 本週入選 section plus a link to the report>" --base main.
5. Final message: the winners with heat scores, the PR URL, and any source that failed or hit a cost cap.

NEVER delete or rename files. NEVER touch raw/ except adding. Never use cookie-based search unless the tokens are present in the environment. Numbers in the report must come from fxtwitter, GitHub or the registry APIs, never from search-result snippets.
