# routines/

Prompts for the four Claude Code cloud Routines. Each file has a `## Prompt (paste verbatim)` heading; everything below that
heading is the routine's prompt. The prompts point at files in this repo, so tuning thresholds or rules later means editing
`wiki/hot-list/_config.yaml` or `CLAUDE.md`, never the routine itself.

| Routine | Trigger | Model | Writes |
|---|---|---|---|
| `capture-link` | API (fired by the Supabase `capture` function / iPhone Shortcut / Telegram) | Sonnet | pushes to `main` |
| `github-stars-sync` | Schedule, daily 07:00 HKT | Sonnet (Haiku drops the READMEs and writes English one-liners; see the prompt file) | pushes to `main` |
| `weekly-hot-list` | Schedule, Monday 09:00 HKT | Opus | opens a PR from `hot-list/YYYY-Www` |
| `vault-lint` | Schedule, Monday 10:00 HKT | Sonnet | pushes report to `main`; PR if it proposes merges |

---

## Step 0 — configure the environment once (shared by all four)

Every routine inherits its network policy from its cloud environment, so do this once before creating any routine.

1. Go to https://claude.ai/code/routines and click **New routine** (you can discard it afterwards, or continue into Step 1).
2. Below the **Instructions** box, click the cloud icon showing the environment name.
3. Hover the environment you want (e.g. **Skills Management**) and click the settings icon on its right.
4. Set **Network access** to **Custom**, tick **Also include default list of common package managers**, and add these
   **Allowed domains**:

   ```
   api.fxtwitter.com
   r.jina.ai
   api.github.com
   raw.githubusercontent.com
   graph.threads.net
   api.supadata.ai
   api.scrapecreators.com
   skills.sh
   clawhub.ai
   skillsmp.com
   www.youtube.com
   x.com
   www.threads.net
   www.instagram.com
   ```

5. Optional keys, only if you have them: add `SUPADATA_KEY` (YouTube / Reel transcripts), `SC_API_KEY` (Threads counts),
   `THREADS_APP_TOKEN`, `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` (burner account, X search for the weekly list).
   On Pro/Max prefer **API credentials** over plain environment variables: environment variables are visible to anyone
   using the environment.
6. **Save changes.** The policy applies from the next run.

Without this, requests to the reader hosts fail with `403` and `x-deny-reason: host_not_allowed`, and every capture lands with
`needs_manual_text: true`.

---

## Step 1 — `capture-link` (create on the web; it needs an API trigger)

The API URL and token only exist after the routine is saved, so this one cannot be done from the CLI.

1. https://claude.ai/code/routines → **New routine**.
2. **Name**: `capture-link`.
3. **Instructions**: paste everything below `## Prompt (paste verbatim)` in `routines/capture-link.md`.
4. **Model** (selector inside the instructions box): Sonnet.
5. **Repositories**: add `Tradecreditor/skills-vault`. If it is not listed, your account has no GitHub access to it yet:
   grant it at https://github.com/apps/claude or run `/web-setup` in a local Claude Code session inside the vault.
6. **Environment**: the one configured in Step 0.
7. **Select a trigger** → **API**. Save the routine first; the URL and token are generated afterwards.
8. **Connectors**: keep **Exa** and **GitHub**, remove the rest. Claude can use every tool of an included connector without
   asking during a run, so keep the list tight.
9. Click **Create**.
10. Reopen the routine → menu next to its name → **Edit** → **Select a trigger** → **Add another trigger** → **API**.
    Copy the URL, click **Generate token**, and copy the token immediately. **It is shown once and cannot be retrieved later.**
    Store both; `supabase/README.md` needs them as `ROUTINE_FIRE_URL` and `ROUTINE_TOKEN`.
11. Test: on the routine's detail page click **Run now** and supply a URL as the run text, e.g.
    `https://github.com/kepano/obsidian-skills`. Open the run and confirm it committed to `main`.

---

### Copying a prompt into the Routine UI

A Routine stores its own copy of the prompt. Editing the file in `routines/` changes nothing until you paste the
new text into claude.ai, so use the script rather than copying by eye:

```powershell
.\scripts\copy-prompt.ps1 github-stars-sync
```

Do not substitute a plain `Get-Content -Raw | Set-Clipboard`. Windows PowerShell 5.1 reads files in the system ANSI
code page unless told otherwise, so the Chinese in these prompts is mangled before it reaches the clipboard. That
is how the instruction "摘要 and 點解值得留意 are written in 繁體中文" reached a live routine as
"?? and 暺圾?澆??? are written in 蝜?銝剜?", and the routine wrote English summaries for days without anything
looking broken. The script reads UTF-8, reads the clipboard back, and refuses to report success unless it matches.

### Firing it afterwards

The API trigger gives you a URL ending in `/fire` and a token shown exactly once. Together they can start a run on your
account, so treat the token as a secret and keep it out of the repo.

`scripts/capture.ps1` (Windows) and `scripts/capture.sh` (macOS/Linux) wrap the call, so capturing a link is one command
instead of a remembered curl incantation. Each reads `VAULT_FIRE_URL` and `VAULT_FIRE_TOKEN` from the environment and
refuses to run if the URL does not end in `/fire` — a stray character there returns a 404 that reads like a broken routine
rather than a typo. Setup instructions are in the comment at the bottom of each script.

```powershell
.\scripts\capture.ps1 https://x.com/someone/status/123
```

## Steps 2-4 — the three scheduled routines

Two ways. The CLI is faster and attaches the right repository automatically.

### Option A (recommended): local Claude Code

`/schedule` is unavailable inside cloud sessions, so run this on your own machine:

```bash
cd ~/skills-vault        # Windows: cd $HOME\skills-vault
claude
```

Then, once per routine, paste this and follow Claude's questions:

```
/schedule create a routine named github-stars-sync that runs daily at 07:00 Hong Kong time,
using the repository Tradecreditor/skills-vault and the "Skills Management" environment,
with this prompt:

<paste everything below "## Prompt (paste verbatim)" in routines/github-stars-sync.md>
```

Repeat for `weekly-hot-list` (Mondays 09:00 HKT) and `vault-lint` (Mondays 10:00 HKT).

Claude confirms before saving. If it says it cannot reach your claude.ai account, or `/schedule` is an unknown command,
you are signed in with an API key rather than a claude.ai subscription; use Option B instead.

The model selector is part of the web form, so after `/schedule` saves each routine, open it on the web and set the model
from the table above. `/schedule list` shows what you have, `/schedule update` edits one, `/schedule run` fires it now.

### Option B: the web form

Same as Step 1, except **Select a trigger** → **Schedule**. Pick the nearest preset (daily / weekly, entered in your local
time), then use `/schedule update` from a local session if you want the exact cron (table below).

Timezones are the one thing that silently goes wrong here. A cron expression is always evaluated in UTC; there is no
timezone picker for it. The web form's *presets* are different: they are entered in your browser's local timezone and
then frozen into a fixed UTC cron the moment you save, so they do not follow you when you travel — moving between HKT
and CET shifts every routine by seven hours (six while Europe is on summer time) until you re-set it. A fixed UTC cron also does not observe daylight saving,
so a European summer setting drifts an hour in late October — the table's CET column below is winter time, so in summer
`0 6 * * *` is 08:00 local, not the 07:00 the table gives. Minimum interval is one hour, and runs may start a few minutes
late; the offset is consistent per routine. Whichever
route you take, after saving read the **next run** time the UI shows: that display is the only ground truth.

| Routine | Cron for HKT | Cron for CET | Local time both give |
|---|---|---|---|
| `github-stars-sync` | `0 23 * * *` | `0 6 * * *` | daily 07:00 |
| `weekly-hot-list` | `0 1 * * 1` | `0 8 * * 1` | Monday 09:00 |
| `vault-lint` | `0 2 * * 1` | `0 9 * * 1` | Monday 10:00 |

The last field is the day of the week (`1` = Monday). Leaving it as `*` means *every day*, which is how the weekly
hot list once ran seven times in a week on Opus before anyone noticed — nothing errors, the reports just pile up.

---

## Step 5 — first run and tuning

Open each routine and click **Run now** once, then read the transcript.

A green status only means the session started and exited without an infrastructure error. It does **not** mean the task
succeeded. Open the run and check what Claude actually did: blocked network requests, missing connector tools and task
failures all show up there, not in the status dot.

Expected on the first runs:

- `github-stars-sync` adds up to 6 new star notes per run and prints `no new stars` when the ledger is current; it prints
  `no stars on this account yet` only when the listing comes back empty (empty account, or stars hidden by the profile setting).
- `weekly-hot-list` may report a quiet week. That is by design: thresholds are never lowered to fill the list.
  Tune `wiki/hot-list/_config.yaml` after two real runs, not before.
- `vault-lint` will flag the vault as thin while it holds only a handful of notes.

## Things worth knowing

- **Never set a custom git author.** Commits from cloud sessions and Routines land as `Claude <noreply@anthropic.com>`
  (the identity the cloud environment configures), commits from your laptop as your own identity (plus the GitHub-web
  spelling of it on a PR merge); `git log --format='%an <%ae>' origin/main | sort | uniq -c` shows those, and a handful of
  `skills-vault-core` commits. That invented author left the repo's prompts on 2026-09-19, but the live `capture-link`
  Routine still runs the stored copy of the old prompt (see "Copying a prompt into the Routine UI" above), so re-paste it
  with `scripts/copy-prompt.ps1 capture-link`. Mixed authorship is expected and has not blocked the routines' pushes to
  `main`. What does break things is inventing an author: it defeats the "who wrote this" audit, and Claude Code refuses
  to push a branch not prefixed `claude/` (such as `main`) when it carries commits authored by someone other than you.
- Routines belong to your personal claude.ai account, count against a daily run cap, and draw down subscription usage.
- The `main-protection` ruleset has existed since 2026-09-21; the routines keep pushing to `main` because the owner
  account is on its bypass list. If you ever remove yourself from the bypass list, every routine push starts failing
  (the run reports success, nothing lands) — open the run transcript to see the rejection.
- Fire text arrives wrapped in a `<routine-fire-payload>` block marked untrusted. `capture-link`'s prompt references it
  explicitly, which is why it acts on the pasted URL; do not remove that wording.
- The GitHub proxy inside a cloud session returns `403` for `gh api user/starred`, `gh search repos` and GraphQL calls such
  as `gh repo view --json`, and for any repo not attached to the session. Every prompt already has a fallback path using
  plain `curl` against public `api.github.com` JSON, the GitHub connector's `search_repositories` / `get_file_contents`,
  and the Exa connector's `web_fetch_exa` on `https://api.github.com/...` URLs (verified working from a cloud session).
