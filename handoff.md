# handoff.md — where skills-vault stands (read this first)

One file, one project. Any session or agent that changes code, prompts, config, skills, data or the plan updates this file before it ends (SOP: `skills/keeping-handoff-docs/SKILL.md`). Cloud Routines read it and never edit it. Keep it under ~150 lines; long detail goes to `outputs/` and is linked from here.

Last updated: 2026-10-03 13:30 UTC by Claude Code cloud (Fable 5.1, session 016Po43wctJLFNs4b3MhJuPW).

## Snapshot
- Josep's personal agent skills vault: an Obsidian vault, a Karpathy-style LLM wiki and an installable Agent-Skills library. Rules: `CLAUDE.md` (`AGENTS.md` is an identical copy). Folder roles, note format, skill format and commit vocabulary are all there.
- Core = the `Tradecreditor` GitHub account (Josep's sessions, the cloud Routines, obsidian-git): pushes to `main`. Everyone else (machine account `tradecreditor-ui`, forks) only through a PR; the `guard` workflow blocks deletions, renames, `raw/` edits and protected paths.
- Cloud Routines (prompts in `routines/`, each Routine stores its own copy — re-paste with `scripts/copy-prompt.ps1 <name>` / `.sh` after any edit): `capture-link` (API, fired by `scripts/capture.*`), `github-stars-sync` (daily 06:00 UTC), `weekly-hot-list` (Mon 08:00 UTC, opens a PR), `vault-lint` (Mon 09:00 UTC). Operating notes: `routines/README.md`.
- Credentials live on the cloud environment "Skills Management" as environment variables / API credentials (`SUPADATA_KEY`, `TYPESAFE_API_KEY`), never in the repo.

## In flight
| Workstream | State | Next step | Detail |
|---|---|---|---|
| Jev pilot 1 — `weekly-hot-list` prefilter (H1 `in_scope`, H2 `topical`) | Merged and live (PR #15, #16, #17, #18); live prompt re-pasted 2026-10-03 11:29 UTC; proven in a development run (0 fallbacks, no classifier denial) | After the Monday 2026-10-05 08:00 UTC run: check the `jev:` line in `wiki/hot-list/2026-W40.md` ## 方法, no permission denial in the transcript, the H1 act list; then decide `jev.in_scope.act_min` 2.5 → 3.0 in `wiki/hot-list/_config.yaml` | `outputs/20261003-jev-pilots-handoff.md` §2–3 |
| Jev pilots 2–4 (`github-stars-sync` S2, `vault-lint` L1, `capture-link` C1–C5) | Not started; question sets and thresholds written | Pilot 2 first: `summary_from_readme` in `routines/github-stars-sync.md` step 5b, test with Run now | `outputs/20261003-jev-pilots-handoff.md` §4–6; `skills/judging-with-jev/references/vault-routine-questions.md` |
| Hot list 2026-W40 | Development report on branch `hot-list/2026-W40`, PR #19 open — **do not merge** | Monday's scheduled run force-pushes the branch and updates the PR with the full week; Josep reviews that version | `wiki/hot-list/2026-W40.md` |
| DEV trigger "weekly-hot-list DEV run (Jev pilot 1, 2026-10-02)" | Enabled, fire-only (no cron), no Exa, no repo binding | Disable or delete when no longer wanted (Josep, Routines UI) | trigger `trig_01AFdkexceR6xHxAsNiRmquo` |
| Jev health check — `vault-lint` check 8 | PR #22 open (branch `claude/hopeful-maxwell-zqojwl`); reads the hot list's `jev:` line from `hot-list/WEEK` + `jev:` lines in commit bodies on `main`, ⚠️ on missing / off-while-enabled / fallbacks > `jev.health.fallback_max_ratio` (0.10, `_config.yaml`) | Josep merges, `copy-prompt vault-lint` re-paste, Run now once (writes `outputs/health/2026-W40.md` again — fine); first scheduled read is Mon 2026-10-05 09:00 UTC, one hour after the hot list | `routines/vault-lint.md` check 8; `routines/README.md` Jev bullet |

## Open loops
- `main-protection` ruleset: the `guard` check is not yet in `required_status_checks` (a check appears in the picker only after it has run on one PR from the machine account) — `CLAUDE.md` "How this is actually configured".
- Non-core agent onboarding (Codex / Gemini CLI / OpenClaw with the `tradecreditor-ui` PAT, 90-day expiry): do when Josep asks; he asked to be reminded — `CLAUDE.md` "Onboarding a non-core agent".
- Every skill except `vault-capture` and `vault-search` is `vault_status: draft` pending Josep's review — `skills/README.md`.
- Snapshot refresh gap in the hot list: runs so far refreshed only repos a search returned; tracked repos outside the searches are not re-fetched — `outputs/20261003-jev-pilots-handoff.md` §3.4.

## Recently done (last 7 days)
- 2026-10-03 (later): Jev review for Josep (verdict: pilot 1 + 2a worth doing, 3a wait until the vault is bigger, 4 skip); `vault-lint` check 8 Jev health + `jev.health` config, pilots 2–3 now also put their `jev:` line in the commit body (branch `claude/hopeful-maxwell-zqojwl`).
- 2026-10-03: PR #20 Jev pilots handoff doc; PR #18 `jev_ask.py` client + `jev.client` config + prompt; live `weekly-hot-list` prompt re-pasted (Josep). `handoff.md` and `keeping-handoff-docs` created (this change).
- 2026-10-02: PR #13 hot-list 2026-W39 (first report with winners); PR #15 Jev report + `judging-with-jev` skill; PR #16 Jev API shape, configurable provider, env-var key; PR #17 "test routine changes immediately" practice (`routines/README.md` Step 5); W40 development run (PR #19).

## Environment facts that bite
- `TYPESAFE_API_KEY` must be an **environment variable**; the Bearer-type API-credential injection never reached TypeSafe (4 variants, 2026-10-02). The custom-header credential used for `SUPADATA_KEY` works — `routines/README.md` Step 0.
- The auto-mode permission classifier can deny a raw `curl` that carries a key ("Data Exfiltration", 2026-10-02) and let the identical call through an hour earlier; every Jev call goes through `skills/judging-with-jev/scripts/jev_ask.py` — `outputs/20261003-jev-pilots-handoff.md` §8.
- Inside cloud sessions `api.github.com` search answers 403 ("sessions are bound to their configured repositories"); use the GitHub connector, Exa `web_fetch_exa` on the API URL, or the Jina relay (blocks anonymous use after ~20 calls). `raw.githubusercontent.com` is fine.
- Exa web search returns no `x.com` / `threads.net` posts; X evidence comes from fxtwitter profile timelines (`api.fxtwitter.com/2/profile/<handle>/statuses`, field `reposts`).
- A schedule-type Routine's "Run now" passes no run text (only API-type Routines have the box); agents can `fire_trigger` only triggers they created; `create_trigger` cannot attach connectors.
- Exa `web_fetch_exa` defaults to 3,000 characters and truncates silently; always pass `maxCharacters` and a changing `cb=` — `CLAUDE.md` "Reading a URL with Exa".

## How to update this file
- Edit the sections above in place; keep facts, dates, PR numbers, trigger / session ids.
- Append one line to the Session log; never rewrite old lines.
- Commit it with the change it describes (same commit or PR). Routines read it and never edit it.

## Session log (append-only; newest last)
- 2026-10-02 · Claude Code cloud, Fable 5.1, session 018ZbUMaCg8HwBtjhZjMPHVB · Jev report + `judging-with-jev` skill (PR #15), pilot 1 wiring and API fixes (PR #16), test-now practice (PR #17), key / credential debugging, `jev_ask.py` (PR #18), W40 development run (PR #19) · next: Monday acceptance of pilot 1.
- 2026-10-03 · same session · PR #18 and #20 merged; live prompt re-pasted by Josep; `handoff.md` + `keeping-handoff-docs` SOP added · next: Monday acceptance, then pilot 2 (see In flight).
- 2026-10-03 · Claude Code cloud, Fable 5.1, session 016Po43wctJLFNs4b3MhJuPW · Jev plan review for Josep; `vault-lint` check 8 Jev health + `jev.health.fallback_max_ratio`; pilots 2–3 told to put the jev line in the commit body (PR #22) · next: Josep merges + re-pastes `vault-lint`, Run now; Monday acceptance of pilot 1 unchanged.
