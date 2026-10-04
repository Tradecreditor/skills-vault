# Security checklist (S1–S10)

Answer each item `ok`, `acceptable: <reason>` or `fail: <reason>`. Any `fail` makes the verdict FAIL.
Read the whole folder first; judge what an agent following the skill would actually do, not what the skill says about itself.

| id | Question | Fail examples |
|---|---|---|
| S1 | **Injection and concealment.** Is any text aimed at the agent reading it, to change its behaviour beyond the skill's stated purpose? | Telling the agent to set aside earlier or system instructions; addressing the reviewer, auditor or routine; asking the agent to hide an action, a file or a result from the user; role-play or "developer mode" framing; instructions tucked into HTML comments, link titles, image alt text or reference files that the body never mentions |
| S2 | **Scope.** Is every action the body asks for needed for what the description promises? | Telemetry, uploads, account sign-ups, starring or following repos, contacting third parties, or editing unrelated files that the description does not mention |
| S3 | **Data leaving the machine.** Is every network destination named, owned by the tool the skill is about, and sent only what the task needs? | Posting repo contents, chat content, file listings or environment details to any host; URL shorteners or raw IPs; a host that does not belong to the named project |
| S4 | **Credentials.** Are keys read only from environment variables the user sets, and never printed, logged, written to files or committed? | Asking for a password or key in chat; reading cookies, browser profiles or keychains; echoing a token; writing a key into a config file inside the repo |
| S5 | **Installs and supply chain.** Does each install name the project's own official source (registry package name or repository that matches the project), preferably pinned? | Piping a download into a shell from a host other than the project's own; look-alike package names; installing from a fork or a personal mirror without saying why; global installs the description does not mention |
| S6 | **Execution.** Do the shipped scripts do exactly what SKILL.md says, with no execution of downloaded or decoded content? | `eval` of fetched text; `shell=True` with interpolated input; a script that does more than SKILL.md describes; commands meant to run without the user's normal permission prompts |
| S7 | **Permissions and agent configuration.** Does the skill leave permission modes, sandboxes, hooks, MCP servers and memory files (CLAUDE.md, AGENTS.md) alone, unless changing them is its declared purpose and it shows the change first? | Bypass-permissions or skip-sandbox flags as a default; silently adding hooks or MCP servers; appending rules to CLAUDE.md or AGENTS.md |
| S8 | **Destructive and persistent actions.** Are deletions limited to files the skill itself created, and is anything scheduled or added to startup only when that is the declared purpose? | Recursive deletes outside a temp folder; force pushes or hard resets the user did not ask for; cron jobs, launch agents, shell-profile edits |
| S9 | **Trigger hygiene.** Is the description specific enough not to hijack unrelated tasks or shadow built-in commands and other skills? | "Use when doing anything", "Use for every task", claiming `/review`, `/init` or another skill's triggers |
| S10 | **Honesty.** Do the skill's claims match its content? | Claiming to be official, verified or audited when it is not; benchmark numbers used to justify a risky step; a description that hides what the body does |

## Static rule ids the reviewer must judge

| id | Flags | Usually acceptable when |
|---|---|---|
| R1 | download piped into an interpreter | the host is the project's own documented installer, and the description says the skill installs that tool |
| R2 | third-party installs | the package or repo is the official one for the tool the skill is about |
| R3 | sudo or loose permissions | a system package install the description names; never `chmod 777` |
| R4 | dynamic execution in scripts | fixed argument lists, no shell interpolation of untrusted input |
| R5 | network access | destinations belong to the tool or API the skill is about |
| R6 | secrets and tokens | read from environment variables, never printed or written |
| R7 | weakened permissions or sandbox | essentially never; only a skill about configuring that mode, with the risk stated |
| R8 | agent configuration writes | the skill's purpose is configuring that agent and it shows the change first |
| R9 | persistence | the skill's purpose is scheduling something, stated in the description |
| R10 | deletes or rewrites | limited to files the skill created, or a user-requested git operation |
| R11 | shipped executable code | the script is short enough to read in full and does what SKILL.md says |
