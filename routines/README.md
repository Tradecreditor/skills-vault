# routines/
Prompts for the Claude Code cloud Routines (claude.ai/code → Routines). Create each Routine with the settings in its file and paste its
prompt verbatim. Prompts point at files in this repo, so tuning thresholds or rules never requires editing the Routine itself.

| Routine | Trigger | Model (tiering) | Writes |
|---|---|---|---|
| capture-link | API (fired by the Supabase `capture` function / iPhone Shortcut / Telegram) | Sonnet | pushes to `main` |
| github-stars-sync | Schedule `0 23 * * *` (07:00 HKT daily) | Haiku (or Sonnet) | pushes to `main` |
| weekly-hot-list | Schedule `0 1 * * 1` (Monday 09:00 HKT) | Opus | opens a PR from `hot-list/YYYY-Www` |
| vault-lint | Schedule `0 2 * * 1` (Monday 10:00 HKT) | Sonnet | pushes report to `main`; PR if it proposes merges |

Common settings for all four: repository `Tradecreditor/skills-vault`; environment "Skills Management" with network access set to
**Custom** including the default package-manager list plus: `api.fxtwitter.com`, `r.jina.ai`, `graph.threads.net`, `api.github.com`,
`raw.githubusercontent.com`, `api.supadata.ai`, `api.scrapecreators.com`, `skills.sh`, `clawhub.ai`, `skillsmp.com`, `www.youtube.com`,
`x.com`, `www.threads.net`, `www.instagram.com`; connectors: Exa (backup reader; also the cloud route to GitHub JSON), GitHub;
**Permissions → Allow unrestricted branch pushes** enabled for this repo (Routines act as the owner account, so they may push to `main`);
optional secrets `SUPADATA_KEY`, `SC_API_KEY`, `THREADS_APP_TOKEN`, `TWITTER_AUTH_TOKEN`, `TWITTER_CT0` (burner account only).

Cloud caveat (verified 2026-09-13 inside a Claude cloud session): the sandbox's GitHub proxy returns 403 for `gh api user/starred`,
`gh search repos`, GraphQL (`gh repo view --json`) and any repo not attached to the session. Every prompt below therefore has a cloud path
that uses plain `curl` to public `api.github.com` JSON (may also be blocked), the GitHub connector's `search_repositories` /
`get_file_contents` tools, and the Exa connector's `web_fetch_exa` on `https://api.github.com/...` URLs (verified working).
