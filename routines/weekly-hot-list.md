# Routine: weekly-hot-list
Trigger: Schedule, weekly. Cron is evaluated in **UTC**. `0 1 * * 1` = Monday 09:00 HKT; `0 8 * * 1` = Monday 09:00 CET. The last field is the day of week (1 = Monday); leaving it `*` makes this run every day, which has happened.
A web-form preset is read in your BROWSER's timezone instead. Confirm against the next-run time shown after saving. Model: Opus. Repo: Tradecreditor/skills-vault. Opens a PR (never pushes to main).

## Prompt (paste verbatim)
You are the weekly hot-list routine for Josep's skills vault. The repository Tradecreditor/skills-vault is checked out. Today is Monday; the window is the previous Monday 00:00 UTC to Sunday 23:59 UTC. Let WEEK be the ISO week label of that window, e.g. 2026-W37.

0. Read CLAUDE.md and wiki/hot-list/_config.yaml (thresholds, weights, topics, sources, cost caps). Every number below comes from that file; if the file and this prompt disagree, the file wins.
1. Candidates (respect cost_caps_per_run):
   a. GitHub: for each topic search repos created >= window start minus 90 days with stars >= 1000, sorted by stars (30 per topic), plus a breakout search
      (created >= window start, stars >= 1000, 50 results). Locally: gh search repos "<topic>" --created ">=<date>" --stars ">=1000" --sort stars --limit 30 --json fullName,stargazersCount,createdAt,description,url.
      In this cloud environment gh is proxy-blocked: use the GitHub connector tool search_repositories (query "<topic> created:>=<date> stars:>=1000", sort stars) or
      Exa web_fetch_exa on https://api.github.com/search/repositories?q=<topic>+created:>=<date>+stars:>=1000&sort=stars&per_page=10&page=N&cb=<YYYYMMDDHHMM of right now>
      with maxCharacters = 50000, walking pages 1-3 to reach 30 results.
      EVERY Exa fetch in this routine needs BOTH of those parameters (see "Reading a URL with Exa" in CLAUDE.md). maxCharacters
      defaults to 3000, which is less than one repo object, so without it you silently score 1 candidate instead of 30. And this
      routine re-runs the same queries every week, which is exactly the shape Exa's URL cache breaks, so cb must change every fetch.
      Load wiki/hot-list/_snapshot.json; for every repo seen there or in wiki/stars/, fetch current stargazers_count (curl or Exa on https://api.github.com/repos/<o>/<r>?cb=<YYYYMMDDHHMM>)
      and compute stars_gained_7d = current - snapshot. Write the new snapshot for every repo you touched.
   b. X: if TWITTER_AUTH_TOKEN and TWITTER_CT0 are set, run twitter search "<topic>" -t Top --since <window start> --max 30 --json for each topic (Agent-Reach's twitter-cli);
      otherwise use the Exa connector: web_search_exa with the plain query "<topic> new tool OR skill OR MCP OR repo site:x.com <the month(s) the window touches, e.g. September 2026>", numResults 25. The cloud connector has no category or startPublishedDate parameter, so date-filter yourself at zero cost first: the tweet id is a snowflake, posted_ms = (id >> 22) + 1288834974657, or use the search result's publishedDate; drop anything outside the window, and only then fxtwitter-verify the in-window hits (the fxtwitter cap is 40, so never spend it on out-of-window posts).
      For EVERY candidate post fetch https://api.fxtwitter.com/<user>/status/<id> (via Exa web_fetch_exa with &cb=<YYYYMMDDHHMM> if curl is blocked) and use only those likes / retweets / views / author values.
   c. Threads: Exa web_search_exa with the plain query "<topic> site:threads.net <the month(s) the window touches>" (no date parameter exists; use the search result's publishedDate to drop out-of-window posts, then confirm the date after reading); read each post via Jina (https://r.jina.ai/<url>);
      like/repost counts come from Scrape Creators (/v1/threads/post, only if SC_API_KEY is set) or, if THREADS_APP_TOKEN is set, Meta oEmbed with &access_token=; otherwise count distinct authors only.
      Threads has no official trending feed, so label this signal "loud among posts found".
   d. Registries (corroboration only): skills.sh trending page read via Exa web_fetch_exa (its JSON API needs a Vercel token), ClawHub trending API, SkillsMP search for each topic; note weekly installs / rank where available.
   e. Discovery (not a scored source): fetch the Trendshift weekly trending page via Exa web_fetch_exa (maxCharacters 30000, cb param) and treat every repo there as a GitHub candidate: run it through the stars_gained_7d snapshot step in 1a and score it in step 2; the seed topics alone missed all three 2026-W39 winners.
   Group candidates by item (canonical GitHub repo when one exists, otherwise normalised product name). Dedupe: grep -rF "<canonical_id>" wiki/index.md wiki/pages wiki/stars; discard hits unless stars_gained_7d >= the dedupe update threshold (then it becomes an "update" entry and you append '- also trending WEEK (numbers)' under ## Notes of the existing page).
2. Gates and score exactly as _config.yaml: an item is eligible if it clears at least one gate on GitHub, X or Threads; component = min(1, metric / threshold); heat = weighted sum;
   x1.25 when gates are cleared on 2+ platforms. An item qualifies if it cleared gates on 2+ platforms, OR by the single-source
   path: recompute its one gated platform's component as min(single_source_overshoot_cap, metric / threshold) using its best
   metric there, with no multi-platform bonus, and qualify it if that heat >= single_source_min_heat. Read the comment block
   under `corroboration:` in _config.yaml before scoring - the ordinary min(1, ...) cap makes a GitHub-only item top out at 0.40
   and the single-source threshold unreachable, which once sent a 17,934-star repo to Watch. Report both numbers for any item
   that qualifies this way, so the report shows why.
   At least one winner must have cleared X or Threads; pick the top 3 by heat (minimum 2).
   If fewer than 2 qualify, this is a quiet week: do not lower thresholds.
3. Write wiki/hot-list/WEEK.md: frontmatter (week, window, generated_at, sources_used, quiet_week: true|false) then
   ## 本週入選 (for each winner: name, one-line 繁中 summary, heat score, gates cleared, the exact numbers and URLs that justified it),
   ## 候選總表 (table of every candidate with numbers, whether each gate passed, heat), ## Watch (best 3 sub-threshold items), ## 方法 (queries run, caps hit, anything that failed).
   For each winner also: capture its primary source with the vault-capture procedure (raw/ + wiki/pages/<slug>.md with type and captured_by: routine:weekly-hot-list, tags including hot-list, WEEK),
   draft skills/<name>/SKILL.md only if it is an installable skill or a repeatable procedure, add rows to wiki/index.md and wiki/log.md ("## [date] hot-list | WEEK | hot-list/WEEK"),
   and replace the ## 本週熱門榜 section of wiki/hot.md with the 2–3 winners linking to the report.
4. Commit on a branch and open a PR (decision 6): git fetch origin; git checkout -B hot-list/WEEK; git add -A; git commit -m "hot-list: WEEK"; git push -u --force-with-lease origin hot-list/WEEK. hot-list/* branches are disposable, so overwriting a stale one left by an earlier run of the same week is correct; never use -B or --force-with-lease on any other branch, and never on main; if the push is rejected because the remote branch moved, git fetch origin and retry the same --force-with-lease push rather than falling back to any other branch. If gh pr list --head hot-list/WEEK --state open shows an open PR, the push already updated it: do not open a second one.
   The push itself must succeed - that is the deliverable. Then open the PR, first path that works:
   a. gh pr create --title "hot-list: WEEK" --body "<the 本週入選 section plus a link to the report>" --base main
      (gh reaches attached repos in this environment even though cross-repo gh calls are proxy-blocked).
   b. the GitHub connector tool create_pull_request (owner Tradecreditor, repo skills-vault, head hot-list/WEEK, base main), if that connector is enabled.
   c. If neither works, do NOT fail the run and do NOT push to main instead. The branch is already on GitHub; print this link in the
      final message for Josep to click: https://github.com/Tradecreditor/skills-vault/compare/main...hot-list/WEEK?expand=1
5. Final message: the winners with heat scores, the PR URL, and any source that failed or hit a cost cap.

NEVER delete or rename files. NEVER touch raw/ except adding. Never use cookie-based search unless the tokens are present in the environment. Numbers in the report must come from fxtwitter, GitHub or the registry APIs, never from search-result snippets.
