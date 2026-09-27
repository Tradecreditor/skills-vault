---
name: reviewing-code-security
description: "Reviews code for security flaws with the OWASP Secure Coding checklist plus checks for Supabase (RLS, grants, edge functions), webhooks, shell scripts, GitHub Actions and leaked secrets. Use when asked for a security check, review or audit, or before merging auth, webhook or data-access code."
metadata:
  source_url: "https://github.com/OWASP/secure-coding-practices-quick-reference-guide"
  source_platform: "github"
  author: "OWASP"
  captured_at: "2026-09-27"
  engagement: "stars=50 forks=13"
  origin_type: "repo"
  vault_status: "draft"
---

# reviewing-code-security

Draft, unreviewed. A read-only security review procedure built on the OWASP Secure Coding Practices
Quick Reference Guide (full 14-section checklist in `references/source.md`), plus concrete checks for the
stacks the checklist does not name: Supabase, webhook/edge functions, shell/PowerShell scripts, GitHub Actions.

The review **reads** code and runs read-only searches. It never edits files, rotates keys or runs the project's
scripts; fixes are proposed, and applied only when the user asks.

## When to use

- "Security check / security review / audit this repo / this branch / this PR"
- Before merging code that touches auth, webhooks, secrets, database access, file uploads or CI workflows
- After adding a new entry point (HTTP handler, bot webhook, CLI that takes user input, cron job)

## Steps

### 1. Fix the scope

```sh
git diff --name-only origin/main...HEAD      # branch / PR review: only these files and what they call
git ls-files                                 # whole-repo audit
```
State the scope in the report. A diff review still follows data flow into unchanged files when needed.

### 2. Map the attack surface (before reading line by line)

List, with `file:line`:
- **Entry points**: HTTP/edge handlers, webhooks, bot endpoints, CLI args, files read from disk, env vars, CI triggers.
- **Trust boundaries**: who can reach each entry point (public internet, authenticated user, owner only, CI fork PR).
- **Privileged credentials**: service-role keys, API tokens, bot tokens, deploy keys — where loaded, where used.
- **Data stores and sinks**: DB tables, shell/exec calls, outbound `fetch`, HTML output, logs.

The high-value findings live where an untrusted entry point reaches a privileged credential or a dangerous sink.

### 3. Sweep for secrets

```sh
git grep -nIE '(sk-[A-Za-z0-9_-]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{40,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{10,}\.eyJ|-----BEGIN [A-Z ]*PRIVATE KEY)'
git grep -nIiE '(api[_-]?key|secret|token|password|passwd|service_role)\s*[:=]\s*["'"'"'][^"'"'"'$]{8,}'
git log -p --all -S 'PRIVATE KEY' --oneline | head      # secrets removed from HEAD but still in history
git ls-files | grep -iE '(^|/)\.env($|\.)|\.pem$|\.p12$|id_rsa|cookies?\.(txt|json)$'
```
Also check `.gitignore` covers `.env*`, cookie files and local credential stores. A secret found in history is
still leaked: the fix is rotation, not deletion.

### 4. Walk the OWASP checklist against the surface

Open `references/source.md` and go section by section, but only for sections the surface actually touches.
The table says what each section usually means in code:

| OWASP section | Look for |
|---|---|
| Input validation | Server-side allow-list validation of type, length, range; URL/host allow-lists before `fetch`; JSON body shape checked before use |
| Output encoding | Untrusted data into HTML, SQL, shell, Markdown sent to a chat API, or log lines without encoding |
| Authentication and password management | Every non-public endpoint authenticates **before** doing work; secrets compared in constant time; no default or empty secret that disables the check |
| Session management | Token expiry, cookie flags (`HttpOnly`, `Secure`, `SameSite`), logout invalidation |
| Access control | Per-user authorization on every data access (IDOR); deny by default; owner/allow-list checks on bots and webhooks |
| Cryptographic practices | Vetted libraries only; no home-made crypto; random values from a CSPRNG |
| Error handling and logging | No stack traces, secrets or tokens in responses or logs; failures fail closed |
| Data protection | Least data returned; secrets only in env/secret stores; no sensitive data in URLs or query strings |
| Communication security | HTTPS everywhere; TLS verification never disabled (`verify=False`, `-k`, `NODE_TLS_REJECT_UNAUTHORIZED=0`) |
| System configuration | Debug off; least-privilege tokens and CI permissions; dependencies pinned and current |
| Database security | Parameterised queries; least-privilege DB roles; row-level security on multi-tenant tables |
| File management | Path traversal on user-supplied paths; upload type/size limits; no execution of uploaded files |
| Memory management | Relevant only for C/C++/unsafe code: bounds, lengths, freeing |
| General coding practices | No user data into `eval`/`exec`/`Function`/`Invoke-Expression`; third-party code reviewed; safe update channels |

### 5. Stack-specific checks

**Supabase / Postgres**
- `alter table ... enable row level security` on every table in an exposed schema (`public`); a table without RLS is
  readable and writable by anyone holding the anon key.
- RLS enabled with **no policies** means only `service_role` can touch it — fine if intended; say so in the report.
- Policies: `using (true)` / `with check (true)` for `anon` or `authenticated` is effectively no RLS.
- `grant ... to anon, authenticated` on tables that should be server-only.
- `security definer` functions must `set search_path = ''` (or a fixed schema) and check the caller themselves.
- The `service_role` key appears only in server code (edge functions, backend env), never in client bundles,
  mobile apps, shortcuts, or committed files.

**Edge functions / webhooks deployed with `--no-verify-jwt`**
- The function is public: it must authenticate every request itself (shared-secret header, platform signature
  such as Telegram's `X-Telegram-Bot-Api-Secret-Token` or Stripe/GitHub HMAC) **before** any DB write or outbound call.
- An empty or unset secret must reject, not accept (`if (!SECRET || header !== SECRET) return 401`).
- Prefer constant-time comparison for secrets.
- Outbound `fetch` of user-supplied URLs = SSRF risk: restrict hosts, block private/link-local IPs, set
  `redirect: "manual"` and a timeout, cap the number of hops.
- Rate/volume limits where a request can spend money (LLM calls, Routine runs, paid APIs).
- Replies never echo secrets; error bodies do not include stack traces.

**Shell scripts (`*.sh`)**
- `set -euo pipefail` (or explicit error handling); every variable expansion quoted (`"$var"`).
- No `eval`, no `bash -c "$input"`, no `curl ... | sh` of unpinned URLs.
- Secrets passed via env or stdin, not argv (argv is visible in `ps` and CI logs).
- Temp files via `mktemp`, not fixed `/tmp/name`.

**PowerShell scripts (`*.ps1`)**
- No `Invoke-Expression` / `iex` on downloaded or user-supplied strings.
- `-ExecutionPolicy Bypass` only where documented; secrets not written to transcripts or history.

**GitHub Actions (`.github/workflows/*.yml`)**
- Top-level `permissions:` set to least privilege (`contents: read`), widened per job only when needed.
- `pull_request_target` or `workflow_run` + checkout of the PR head = untrusted code with secrets: flag as Critical.
- Script injection: `${{ github.event.* }}` (PR title, body, branch name, comment) interpolated directly into `run:`;
  pass through `env:` instead.
- Third-party actions pinned to a full commit SHA (at minimum a major tag for first-party `actions/*`).
- Secrets never echoed; not exposed to jobs that run fork code.

**LLM / agent code** (prompts, tool definitions, routines)
- Untrusted text (fetched pages, emails, chat messages) is treated as data; it cannot trigger tool calls with
  side effects without a check. Tokens given to agents are least-privilege.
- For systematic red teaming of an LLM app, pair with the `evaluating-llms-with-promptfoo` skill.

### 6. Verify every finding before reporting

For each candidate, write the concrete path: *who* sends *what* to *which* entry point, and *what* they gain.
Drop anything that needs an attacker who already has the privilege in question, and anything only reachable from
tests or fixtures. Mark the rest **Confirmed** (path traced in code) or **Plausible** (depends on config you cannot see,
e.g. dashboard settings, deployed env vars).

### 7. Report

Most severe first. One entry per finding:

```
### [High] Webhook accepts requests when secret is unset
- Where: functions/webhook/index.ts:42      (illustrative example)
- Status: Confirmed
- Scenario: WEBHOOK_SECRET is unset → `(header ?? "") === (WEBHOOK_SECRET ?? "")` is true for a request with no header → anyone can trigger paid jobs.
- Fix: reject when the secret is empty; compare in constant time.
```

Severity: **Critical** (remote, unauthenticated, data or credential compromise) · **High** (auth bypass, privilege
escalation, secret exposure) · **Medium** (needs some access or unusual config) · **Low** (hardening, defence in depth).
End with a short "Checked, no issues" list so the reader knows what was covered, and the scope from step 1.
If the project keeps long-form agent output in a folder (e.g. `outputs/`), write the report there and link it.

## Pitfalls

- The OWASP list is a checklist of practices, not a vulnerability catalogue: a missing practice is a finding only
  when you can show how it is exploited here.
- Do not report secrets that are placeholders (`sk-...`, `<your-key>`, `example`) or env-var names.
- Row-level security with zero policies is a deliberate "service role only" pattern, not a bug.
- A diff-only review misses a vulnerability that the diff merely makes reachable; follow the data flow.
- Never paste a real secret value into the report — name the file and line, then say "rotate".

## Source

OWASP Secure Coding Practices Quick Reference Guide — https://owasp.org/www-project-secure-coding-practices-quick-reference-guide
(repo archived: https://github.com/OWASP/secure-coding-practices-quick-reference-guide), CC BY-SA 4.0.
Full checklist: `references/source.md`. Stack-specific sections were added for this vault.
