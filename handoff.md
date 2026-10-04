# handoff.md — where skills-vault stands (read this first)

One file, one project. Any session or agent that changes code, prompts, config, skills, data or the plan updates this file before it ends (SOP: `skills/keeping-handoff-docs/SKILL.md`). Cloud Routines read it and never edit it. Keep it under ~150 lines; long detail goes to `outputs/` and is linked from here.

Last updated: 2026-10-04 13:20 UTC by Claude Code cloud (session 0196PKoiJ83bGN8ofvFmKCWt).

## Snapshot
- Josep's personal agent skills vault: an Obsidian vault, a Karpathy-style LLM wiki and an installable Agent-Skills library. Rules: `CLAUDE.md` (`AGENTS.md` is an identical copy). Folder roles, note format, skill format and commit vocabulary are all there.
- Core = the `Tradecreditor` GitHub account (Josep's sessions, the cloud Routines, obsidian-git): pushes to `main`. Everyone else (machine account `tradecreditor-ui`, forks) only through a PR; the `guard` workflow blocks deletions, renames, `raw/` edits and protected paths.
- Cloud Routines (prompts in `routines/`, each Routine stores its own copy — re-paste with `scripts/copy-prompt.ps1 <name>` / `.sh` after any edit): `capture-link` (API, fired by `scripts/capture.*`), `github-stars-sync` (daily 06:00 UTC), `weekly-hot-list` (Mon 08:00 UTC, opens a PR), `vault-lint` (Mon 09:00 UTC). Operating notes: `routines/README.md`.
- Credentials live on the cloud environment "Skills Management" as environment variables / API credentials (`SUPADATA_KEY`, `TYPESAFE_API_KEY`), never in the repo.

## In flight
| Workstream | State | Next step | Detail |
|---|---|---|---|
| Jev pilot 1 — `weekly-hot-list` prefilter (H1 `in_scope`, H2 `topical`) | Merged and live (PR #15, #16, #17, #18); live prompt re-pasted 2026-10-03 11:29 UTC; proven in a development run (0 fallbacks, no classifier denial). Pre-flight 2026-10-04: config intact, live `jev_ask.py probe` exit 0 (`jev-1.13.0`, no denial), offline `JEV_FAKE` probe/ask/secret-refusal OK | After the Monday 2026-10-05 08:00 UTC run: check the `jev:` line in `wiki/hot-list/2026-W40.md` ## 方法, no permission denial in the transcript, the H1 act list; then decide `jev.in_scope.act_min` 2.5 → 3.0 in `wiki/hot-list/_config.yaml` | `outputs/20261003-jev-pilots-handoff.md` §2–3 |
| Jev pilots 2–4 (`github-stars-sync` S2, `vault-lint` L1, `capture-link` C1–C5) | Not started; question sets and thresholds written. Review for Josep 2026-10-03 (chat, not yet his decision) recommends: 2a S2 next (real blind spot, near-zero cost); 2b S1 optional; 3a L1 wait until the vault passes ~150 entries or lint reports a real duplicate (48 entries, 0 duplicates today); 3b L2 after 2026-10-19 when the 09-19 star batch crosses 30 days; 4 skip or `type` / `topic` only | Pilot 2 first: `summary_from_readme` in `routines/github-stars-sync.md` step 5b, test with Run now; its `jev:` line also goes in the commit body (check 8 reads it) | `outputs/20261003-jev-pilots-handoff.md` §4–6; `skills/judging-with-jev/references/vault-routine-questions.md` |
| Hot list 2026-W40 | Development report on branch `hot-list/2026-W40`, PR #19 open — **do not merge** | Monday's scheduled run force-pushes the branch and updates the PR with the full week; Josep reviews that version | `wiki/hot-list/2026-W40.md` |
| DEV trigger "weekly-hot-list DEV run (Jev pilot 1, 2026-10-02)" | Enabled, fire-only (no cron), no Exa, no repo binding | Disable or delete when no longer wanted (Josep, Routines UI) | trigger `trig_01AFdkexceR6xHxAsNiRmquo` |
| Jev health check — `vault-lint` check 8 | Live: PR #22 merged, prompt re-pasted, Run now 2026-10-03 passed (commit `1b28a6d`, `outputs/health/2026-W40.md` §8 ✅: read the line from branch `hot-list/2026-W40`, fallbacks 0/145). Reads the hot list's `jev:` line from `hot-list/WEEK` + `jev:` lines in commit bodies on `main`; ⚠️ on missing / off-while-enabled / fallbacks > `jev.health.fallback_max_ratio` (0.10, `_config.yaml`) | Week-label fix live: PR #24 merged 2026-10-04 13:06 UTC, `vault-lint` re-pasted by Josep and verified identical to `main` (13:12 UTC). First scheduled read Mon 2026-10-05 ~09:10 UTC: `outputs/health/2026-W41.md` §8 should say it read `hot-list/2026-W40` and be ✅ | `routines/vault-lint.md` check 8; `routines/README.md` Jev bullet |
| Lint W40 follow-up — `## Related` fill | Merged (PR #23, `b2ecd6b`). Pre-check 2026-10-04 on `main`: checks 1, 3, 4 pass, but 3 star pages linked to `wiki/pages/` with a bare `[[slug|…]]` that also matches `raw/<slug>.md`, so a strict resolver still counted `20260925-ex-googler-tech-interview-prep-tools` as an orphan; rewritten to `[[../pages/<slug>|…]]` on branch `claude/trusting-hopper-0ktqli` → 0 orphans, 0 empty / missing Related, 0 broken links | Fixed (PR #24 merged). Monday's lint check 4 should read 0 / 0 | `outputs/health/2026-W40.md` §4 |

## Open loops
- `main-protection` ruleset: the `guard` check is not yet in `required_status_checks` (a check appears in the picker only after it has run on one PR from the machine account) — `CLAUDE.md` "How this is actually configured".
- Non-core agent onboarding (Codex / Gemini CLI / OpenClaw with the `tradecreditor-ui` PAT, 90-day expiry): do when Josep asks; he asked to be reminded — `CLAUDE.md` "Onboarding a non-core agent".
- Every skill except `vault-capture` and `vault-search` is `vault_status: draft` pending Josep's review — `skills/README.md`.
- Snapshot refresh gap in the hot list: runs so far refreshed only repos a search returned; tracked repos outside the searches are not re-fetched — `outputs/20261003-jev-pilots-handoff.md` §3.4.
- No global Jev kill switch: `jev.enabled` in `wiki/hot-list/_config.yaml` only governs the hot list; pilots 2–3 plan to hard-code thresholds in their prompts. Suggested 2026-10-03: have `jev_ask.py` honour a `JEV_DISABLED=1` environment variable so one environment setting stops every routine if TypeSafe misbehaves. Not done.

## Recently done (last 7 days)
- 2026-10-04: pre-Monday testpoints run (model-tiering: Sonnet subagents ran the checks, main loop reviewed): lint checks 1/3/4 on `main` ✅ after fixing 3 bare star→page links; Jev live probe ✅; check 8 dry-run ✅ on W40 but exposed the W41/W40 week-label bug (fixed, needs merge + re-paste); `jev-fake.example.json` gained a `probe` answer so an offline `JEV_FAKE` probe exits 0 instead of 4.
- 2026-10-03 (later): Jev review for Josep (verdict in the pilots 2–4 row above); PR #22 `vault-lint` check 8 Jev health + `jev.health` config, merged, prompt re-pasted, Run now by Josep → lint W40 re-run `1b28a6d` with check 8 ✅ (first real read, from branch `hot-list/2026-W40`); that run's 3 orphans + 2 empty `## Related` filled in `b2ecd6b` (unmerged, see In flight).
- 2026-10-03: PR #20 Jev pilots handoff doc; PR #18 `jev_ask.py` client + `jev.client` config + prompt; live `weekly-hot-list` prompt re-pasted (Josep). `handoff.md` and `keeping-handoff-docs` created (this change).
- 2026-10-02: PR #13 hot-list 2026-W39 (first report with winners); PR #15 Jev report + `judging-with-jev` skill; PR #16 Jev API shape, configurable provider, env-var key; PR #17 "test routine changes immediately" practice (`routines/README.md` Step 5); W40 development run (PR #19).

## Environment facts that bite
- `TYPESAFE_API_KEY` must be an **environment variable**; the Bearer-type API-credential injection never reached TypeSafe (4 variants, 2026-10-02). The custom-header credential used for `SUPADATA_KEY` works — `routines/README.md` Step 0.
- The auto-mode permission classifier can deny a raw `curl` that carries a key ("Data Exfiltration", 2026-10-02) and let the identical call through an hour earlier; every Jev call goes through `skills/judging-with-jev/scripts/jev_ask.py` — `outputs/20261003-jev-pilots-handoff.md` §8.
- Inside cloud sessions `api.github.com` search answers 403 ("sessions are bound to their configured repositories"); use the GitHub connector, Exa `web_fetch_exa` on the API URL, or the Jina relay (blocks anonymous use after ~20 calls). `raw.githubusercontent.com` is fine.
- Exa web search returns no `x.com` / `threads.net` posts; X evidence comes from fxtwitter profile timelines (`api.fxtwitter.com/2/profile/<handle>/statuses`, field `reposts`).
- Agents cannot change the four vault Routines: `update_trigger` answers "created via http_api, not by an agent" (2026-10-04), so every prompt edit needs Josep's re-paste. Fix: stub prompts (`routines/README.md` Step 4b) — each Routine reads `routines/<name>.md` from `main` at run time; Josep pastes the four stubs once (pending), after which no prompt edit needs a re-paste. Live prompts matched `main` on 2026-10-04.
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
- 2026-10-03 · same session · PR #22 merged, `vault-lint` re-pasted and Run now by Josep: check 8 ✅ first time (`1b28a6d`); handoff row updated · next: Monday 2026-10-05 — hot list 08:00 UTC (pilot 1 acceptance), lint 09:00 UTC (check 8 on the real run), then pilot 2a.
- 2026-10-03 · same session · `wiki:` filled `## Related` on the 5 pages lint W40 flagged (3 orphans now have inbound links, 2 empty sections filled; 10 files, frontmatter `related:` kept in sync) · next: unchanged (Monday runs, then pilot 2a).
- 2026-10-04 · same session · handoff refreshed on Josep's ask: pilots 2–4 row carries the review verdict, new In-flight row for the unmerged Related fill, open loop for a global Jev kill switch · next: Josep opens + merges the PR for this branch; Monday runs; then pilot 2a.
- 2026-10-04 · Claude Code cloud, session 0196PKoiJ83bGN8ofvFmKCWt · pre-Monday testpoints from this file: lint 1/3/4 pre-check, Jev pre-flight, check 8 dry-run; fixed check 8 week label (`routines/vault-lint.md`, README), 3 bare star→page links, fake-file `probe` · next: Josep merges PR #24 and re-pastes `vault-lint` before Mon 09:00 UTC; Monday acceptance unchanged.
- 2026-10-04 · same session · PR #24 merged; `vault-lint` re-pasted by Josep and checked against `main` via `get_trigger` · next: Monday 2026-10-05 hot list 08:00 UTC (pilot 1 acceptance), lint ~09:10 UTC (§8 on W40), then pilot 2a.
- 2026-10-04 · same session · stub prompts documented (`routines/README.md` Step 4b) so Routines read their prompt from `main` · next: Josep pastes the four stubs once; Monday runs as above.
