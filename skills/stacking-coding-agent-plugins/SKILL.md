---
name: stacking-coding-agent-plugins
description: Scans, then installs what passes the scan gate - Graphify (pinned PyPI CLI, /graphify skill, CLAUDE.md entry) and chosen addyosmani/agent-skills skills at a pinned tag; only describes Ponytail (hooks) and OmniRoute (gateway). Use when asked to set up Graphify or Agent Skills, or to assess Ponytail or OmniRoute.
metadata:
  source_url: "https://www.instagram.com/reel/DdjkD4xi1ma/"
  source_platform: "instagram"
  author: "peterstewiestartup"
  captured_at: "2026-09-26"
  engagement: ""
  origin_type: "post"
  vault_status: "draft"
  reviewed_at: "2026-11-07T07:48:47Z"
  reviewed_by: "routine:skill-review"
  review_hash: "665efe4c655de4c0532073782826114b9b73a91012810a7598a7711b5e3d994b"
  review_report: "outputs/skill-reviews/2026-11-07-stacking-coding-agent-plugins.md"
---

# stacking-coding-agent-plugins

Sets up two add-ons for a coding agent, each from a pinned version, and describes two more without installing them.
The source reel named four tools. Each was checked on 2026-11-10 against its own repository and registry entry:

| Tool | This skill | What it changes, or would change |
|---|---|---|
| Graphify | installs `graphifyy==0.9.103` from PyPI | two commands, one skill folder, one entry in the user's CLAUDE.md; no hook |
| Agent Skills | installs chosen skills from tag `0.6.15` | Markdown skill folders in the project, plus `skills-lock.json` |
| Ponytail | describes only | a plugin whose hooks run at every session start and on every prompt |
| OmniRoute | describes only | a gateway that carries every model request and holds the provider credentials |

## When to use

- The user asks to set up Graphify so the agent can query a knowledge graph of a repository.
- The user asks to add workflow skills from `addyosmani/agent-skills` (spec, plan, build, test, review, ship) to a project.
- The user asks what Ponytail or OmniRoute would change before deciding about them.

Start an install only when the user asked for that tool. A slow session or a usage limit is not a request to install anything.

## Ground rules

1. Before each step, tell the user what it changes (listed under the step). Run every command through the agent's normal permission prompts.
2. Scan before installing, with the vault's `scanning-agent-skills` skill, and apply its gate: 20 or lower install, 21 to 50 read every finding and ask the user, above 50 do not install: report the findings as the scanner gives them and stop. Do not explain findings away on the user's behalf. After a stop, the step continues only if the user, having read the findings, tells you to install anyway; that is the user's decision, not this skill's advice.
3. Keep the pins. A newer version is a different thing: read its release notes, scan it, then change the number.

## Steps

### 1. Graphify: knowledge graph of a repository

Graphify is a Python command-line tool from Graphify Labs (`github.com/Graphify-Labs/graphify`, Apache-2.0). Its PyPI name is
`graphifyy`, with two y's: the project README names that package as the official one and says other `graphify*` packages on
PyPI are not affiliated, and the PyPI entry links back to the same repository. Needs Python 3.10+ and uv.

**Scan first.** The text the agent will read is the skill Graphify registers. In an empty scratch folder outside the
project, download the pinned wheel without installing it, unpack it, and scan that text (`python3` where that is the
command name):

```bash
python -m pip download graphifyy==0.9.103 --no-deps -d graphify-wheel
python -m zipfile -e graphify-wheel/graphifyy-0.9.103-py3-none-any.whl graphify-wheel/unpacked
skillspector scan graphify-wheel/unpacked/graphify/skill.md --no-llm
skillspector scan graphify-wheel/unpacked/graphify/skills/claude --no-llm
```

On Windows the registered files are `skill-windows.md` and `skills/windows`. Result on 2026-11-10 with SkillSpector 2.12.0,
static pass: `skill.md` scored 88, with six HIGH findings, and its references 49. Under ground rule 2 a score of 88 means do
not install, so expect this step to stop here: show the user the findings and leave Graphify uninstalled. Your own scan of the
version you are about to install decides, not this figure. The commands below are for a scan at or under the gate, or for a
user who has read the findings and told you to install anyway.

```bash
uv tool install graphifyy==0.9.103
graphify install
```

Then, from the root of each repository, build or refresh its code graph (local parsing, no model calls):

```bash
graphify update .
```

**What changes**

- `uv tool install` adds two commands to uv's tool directory: `graphify` and `graphify-mcp`. If `graphify` is not found
  afterwards, the README says to run `uv tool update-shell`.
- `graphify install` copies the skill to the `skills/graphify/` folder of the user's Claude Code configuration directory and
  appends this block to the `CLAUDE.md` in that directory (the directory is `CLAUDE_CONFIG_DIR` when that variable is set):
  ```
  # graphify
  - **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
  When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.
  ```
  Show the user this block and wait for their yes before running the command. In 0.9.103 this form of the command registers no hook and leaves the
  settings file alone. The bare command targets Claude Code, and on Windows it installs the Windows variant of the skill.
- `graphify update .` writes a `graphify-out/` folder in the repository.
- Code is parsed on the machine with tree-sitter; the README states that nothing leaves the machine for code and that there is
  no telemetry. Typing `/graphify .` in the assistant also maps docs, PDFs and images, and that pass sends them to the
  assistant's model or to a configured API key.

**Not run by this skill:** `graphify install --project`, `graphify claude install` and `graphify hook install`. The first two
also register a hook in the project's Claude Code settings that fires before file reads and searches; the third adds git hooks
that rebuild the graph on commit and checkout. Run one only when the user asks for that behaviour by name.

**Use:** `graphify query "<question>"`, `graphify path "A" "B"`, `graphify explain "X"`.

**Remove:** `graphify uninstall` (removes the skill folder and the CLAUDE.md block; `--purge` also deletes `graphify-out/`),
then `uv tool uninstall graphifyy`.

### 2. Agent Skills: workflow skills for spec, plan, build, test, review, ship

`addyosmani/agent-skills` (MIT, by Addy Osmani) is a pack of 25 Markdown skills. Its README installs them with the open
`skills` CLI (`vercel-labs/skills`, npm package `skills`), which copies skill folders into the project. Installed this way the
skills load by name or through their descriptions. The `/spec` to `/ship` slash commands and the pack's `hooks/` folder belong
to the README's separate Claude Code plugin route, which this skill does not use.

**Scan first.** Fetch the tagged pack into an empty scratch folder, never the project, and scan each skill:

```bash
npx skills@1.7.6 add https://github.com/addyosmani/agent-skills/tree/0.6.15 -a claude-code -y
skillspector scan .claude/skills --no-llm --recursive
```

Result on 2026-11-10 with SkillSpector 2.12.0, static pass, tag `0.6.15`: 15 skills scored 20 or lower; 9 scored 21 to 50
(`source-driven-development`, `browser-testing-with-devtools`, `constraint-driven-development`, `context-engineering`,
`ci-cd-and-automation`, `git-workflow-and-versioning`, `doubt-driven-development`, `spec-driven-development`,
`code-simplification`); `security-and-hardening` scored 100. So the whole pack is not installed in one go. Your own scan
decides, not this list.

Then, in the project, install only the skills that passed the gate or that the user accepted after reading their findings.
Example with four that scored 20 or lower:

```bash
npx skills@1.7.6 add https://github.com/addyosmani/agent-skills/tree/0.6.15 -a claude-code -y --skill planning-and-task-breakdown --skill incremental-implementation --skill test-driven-development --skill code-review-and-quality
```

**What changes**

- One folder per chosen skill under `.claude/skills/` in the project, and a `skills-lock.json` in the project root that records
  the source and `"ref": "0.6.15"` for each skill. Apart from npm's own download cache, nothing is written outside the project.
  `-g` would install for the whole user account and is not used here.
- No hook, no settings change, no CLAUDE.md edit.
- `-a` names the agent and `-y` skips the CLI's own confirmation prompts. The agent's permission prompt for the command still applies.
- The `skills` CLI sends anonymous usage data unless `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` is set in the environment. Its
  README asks for Node.js 22.20 or later.
- Two skills ship a script: `constraint-driven-development/scripts/quality-gate.mjs` and `idea-refine/scripts/idea-refine.sh`.
  Read a script before letting the agent run it.

**Remove:** `npx skills@1.7.6 remove <skill-name>`.

## Described only: this skill does not install these

### Ponytail

Ponytail (`github.com/DietrichGebert/ponytail`, MIT, by Dietrich Gebert; npm `@dietrichgebert/ponytail`, 5.3.3 on 2026-11-10)
is a prompt that pushes the agent toward the smallest change that works, packaged as a plugin for Claude Code and other agents.
Its plugin manifest registers three hooks, on session start, on subagent start and on every submitted prompt, each running a
Node script from the plugin folder. It also loads a module that draws a status band above the prompt and writes one row per
task to `~/.config/ponytail/band/`. An optional webhook setting sends each task row to an address the user enters; it is empty
by default.

That is third-party code running in every session from then on, so this skill gives no install command for it. If the user
wants it: read its README and `hooks/` folder at a release tag together with the user, scan the repository with
`scanning-agent-skills`, and leave the install to the user.

### OmniRoute

OmniRoute (`github.com/diegosouzapw/OmniRoute`, by Diego Souza; npm `omniroute`, 3.8.53 on 2026-11-10; the npm entry lists
`github.com/cheaper-inference/OmniRoute`, which answered with the same HEAD commit) is a self-hosted gateway between coding
tools and model providers. It runs a local server (default `http://localhost:20128`). The user connects provider accounts or
API keys in its dashboard, and Claude Code is pointed at it through `ANTHROPIC_BASE_URL` and an OmniRoute token. From then on
every model request of every session, prompts, code and tool output included, passes through the gateway to the upstream
provider it selects for that request, which can be a provider other than Anthropic. The gateway stores the provider credentials.

Re-routing all model traffic and credentials is a decision about data handling and provider terms, not a plugin install, so
this skill gives no install or configuration command for it. If the user wants it, treat it as a separate task the user asks
for by name: read its security and Claude Code configuration docs at a release tag, and let the user decide which providers
may receive the code.

## Pitfalls

- The graph goes stale when files change: run `graphify update .` again after changing code or pulling.
- The PyPI package is `graphifyy`; the command is `graphify`. Graphify is a Python package, so there is nothing to run with npx.
- With `skills` CLI 1.7.6 the shorthand `addyosmani/agent-skills@0.6.15` printed the tag but listed the default branch (tested
  2026-11-10: with tag `0.5.0` it listed skills that do not exist at that tag). The `/tree/<tag>` URL form used above checked
  out the tag and failed on an unknown tag. After installing, confirm `"ref"` in `skills-lock.json`.
- Scanned as one target, the Agent Skills repository or the whole installed pack adds every skill's findings together and
  scored 100; scan per skill with `--recursive`.
- The reel quotes savings figures and a provider count. None is repeated here: the reel gives no source for them.

## Source

All read on 2026-11-10.

- https://www.instagram.com/reel/DdjkD4xi1ma/ — @peterstewiestartup, 2026-09-21: names the four tools and their repositories, no commands.
- https://github.com/Graphify-Labs/graphify — README at tag `v0.9.103` (install commands, official-package note, privacy section).
  https://pypi.org/project/graphifyy/ — version 0.9.103, uploaded 2026-11-05, repository link, Python >= 3.10; the wheel's
  `graphify/install.py` and `entry_points.txt` for what `graphify install` writes; its skill files and `install.py` are
  identical to the repository at tag `v0.9.103`. 0.9.105 was the newest release. 0.9.103 is the version tested in this vault
  on Windows on 2026-11-06.
- https://github.com/addyosmani/agent-skills — README at tag `0.6.15` (the newest tag): install command, plugin route, project structure.
- https://github.com/vercel-labs/skills — README and `docs/commands.md` (source formats, `-a`, `-y`, `-g`, `--skill`, `remove`,
  telemetry); npm `skills` 1.7.6, the newest release. Pinned install, `skills-lock.json` and remove were run in a scratch folder.
- https://github.com/DietrichGebert/ponytail — README, `.claude-plugin/plugin.json` and `hooks/claude-codex-hooks.json` at commit `96608e0`.
- https://github.com/diegosouzapw/OmniRoute — README and `docs/guides/CLAUDE-CODE-CONFIGURATION.md` at commit `895c0f3`.
