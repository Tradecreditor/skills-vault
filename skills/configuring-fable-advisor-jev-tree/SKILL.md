---
name: configuring-fable-advisor-jev-tree
description: "Configures one Claude Code setup: Opus main session at high effort, Fable as /advisor, explorer/worker/researcher subagents, and an optional Jev leaf (third-party TypeSafe API) through judging-with-jev. Use when setting up or auditing /advisor fable with an Opus subagent tree."
metadata:
  source_url: "https://x.com/thedelost/status/2104677530825634273"
  source_platform: "x"
  author: "thedelost"
  captured_at: "2026-09-29"
  engagement: "likes=1902 retweets=151 views=446089 bookmarks=3708"
  origin_type: "post"
  vault_status: "reviewer-approved"
  reviewed_at: "2026-11-12T07:51:49Z"
  reviewed_by: "routine:skill-review"
  review_hash: "51552f1ef53c500d7aed1d87304b36f46e9262c2876e215a477f2c8acc66326d"
  review_report: "outputs/skill-reviews/2026-11-12-configuring-fable-advisor-jev-tree.md"
---

# configuring-fable-advisor-jev-tree

Sets up one specific Claude Code arrangement, from the top of the tree to the bottom:

| Layer | Who | Job | Set with |
|---|---|---|---|
| Advisor | Fable (alias `fable`) | consulted at decision points; reads the whole conversation | `/advisor fable` (step 3) |
| Main session | Opus (alias `opus`) at effort `high` | plans, decides, integrates | `/model opus`, `/effort high` (step 2) |
| Subagents | `explorer`, `worker`, `researcher`, each `model: opus`, `effort: medium` | read code · edit and run tests · pull docs | definition files (step 4) |
| Judgment leaf, optional | Jev, a **third-party API** from TypeSafe AI | the same typed yes/no, pick-one or score question over many items | the `judging-with-jev` skill (step 6) |

This skill is only for building or auditing that arrangement. Choosing a model tier or an effort level in general is
[[../model-tiering/SKILL|model-tiering]]; asking Jev a question in general is [[../judging-with-jev/SKILL|judging-with-jev]].

## What the source gives, and what it does not

The source post describes the first three layers and a prompt that builds them. Everything it names for those layers was
checked against the Claude Code documentation on 2026-11-10 (URLs under Source), with two corrections: the effort setting
(step 2), and the post's "only speaks up at three points", which the documentation describes as a tendency, not a rule (step 5).

About Jev the post has one sentence and no configuration: forks that "need no thinker (which file, which tool, retry or stop)"
go to Jev. Claude Code has no setting that hands its own tool choices or retry decisions to another provider's model; none of
the documentation pages under Source describes one. So in this skill the Jev layer means step 6 and nothing more: an agent in
the tree asks Jev typed questions through `judging-with-jev` when a step is a judgment repeated over many items.

## Steps

Ground rules: show every file change as a diff and wait for the user's approval before writing. Slash commands are typed by
the user; ask for them and wait for the confirmation.

1. **Audit, change nothing.** Report what would keep the tree from working:
   - Provider. The advisor needs the Anthropic API; it is not available on Amazon Bedrock, Claude Platform on AWS, Google
     Cloud's Agent Platform or Microsoft Foundry.
   - Fable access. Fable as advisor needs Fable access, and on some plans a one-time consent to bill Fable to usage credits:
     the user runs `/model fable` and accepts. That also makes Fable the selected model, so step 2 switches back.
   - Environment variables:
     ```bash
     for v in CLAUDE_CODE_DISABLE_ADVISOR_TOOL DISABLE_TELEMETRY DO_NOT_TRACK DISABLE_GROWTHBOOK \
              CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC CLAUDE_CODE_EFFORT_LEVEL CLAUDE_CODE_SUBAGENT_MODEL_FORCE; do
       printf '%s=%s\n' "$v" "$(printenv "$v" || echo '<unset>')"
     done
     ```
     | Variable | Effect on this tree |
     |---|---|
     | `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` set to `1` | advisor off: `/advisor` is unavailable and a saved `advisorModel` is ignored |
     | `DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `DISABLE_GROWTHBOOK`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | each can turn feature-flag fetching off (its row in the env-vars page says for which values); the advisor is switched on by a fetched flag, so it stays off |
     | `CLAUDE_CODE_EFFORT_LEVEL` | outranks `/effort`, `--effort`, the effort settings and a subagent's `effort` field |
     | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` | while on, the `model` field in subagent definitions is ignored |

     The `env` key of a settings file sets variables for the session too; check it if the loop prints `<unset>` and the
     advisor still stays off. Opting out of telemetry is the user's choice: report the conflict, do not unset anything.
2. **Main session: Opus at `high`.** The user runs `/model opus`, then `/effort high`. Claude Code saves the level for that
   model under `modelSettings` in the user settings. Correction to the post: it sets a top-level `effortLevel` in the user
   settings file, and the documentation says that key does not count for Opus 5.5 or models released after it; Opus 5.5 then
   stays at its default, `medium`.
3. **Advisor: Fable.** The user runs `/advisor fable`. Claude Code answers `Advisor set to` plus the model name and saves the
   pick to `advisorModel` in the user settings, so it holds in later sessions. For one session only: `claude --advisor fable`.
   An Opus main model accepts Fable as advisor; without the consent from step 1 Claude Code saves nothing and points to
   `/model fable`.
4. **Subagents.** Look in `.claude/agents/` (this project) and `~/.claude/agents/` (every project) for definitions that already
   fit `explorer`, `worker` and `researcher`. Reuse those; list, and leave alone, any that pin a different model; draft only the
   missing ones, in the folder the user picks. A definition is a Markdown file whose body is the subagent's system prompt:
   ```markdown
   ---
   name: explorer
   description: Reads the codebase and reports where things are. Use for search and code reading before any edit.
   tools: Read, Glob, Grep
   model: opus
   effort: medium
   ---

   You explore the codebase and report what you find with file paths. You do not edit files.
   ```
   Only `name` and `description` are required; leave `tools` out for `worker` and `researcher` so they inherit every tool
   available to subagents. Claude Code ignores a field it does not recognise without an error, so spell `effort` exactly.
   Subagents inherit the configured advisor.
5. **Consult rule.** Claude decides when to call the advisor: it tends to consult before committing to an approach, when an
   error keeps recurring and before declaring a task done, but no setting caps or forces a call, so instructions are the only
   lever. Add one line to the project's `CLAUDE.md` (or to `~/.claude/CLAUDE.md`, if the user wants it in every project):
   `Consult the advisor before a large plan, when the same error repeats, and before calling a long task done.`
6. **Jev leaf (optional).** Jev is not an Anthropic model and not part of Claude Code: it is TypeSafe AI's decision model,
   reached over a third-party API with its own key and its own bill, and whatever is put in a question leaves the machine for
   that provider. Skip this step unless the user wants it and `judging-with-jev` is available in the project.
   - Follow `judging-with-jev` for everything mechanical: the script, the key, the hosts, the question types, the thresholds,
     the fallback and the log line. Nothing of that is repeated here. Run its probe first; if it reports Jev off, stop here
     and say so.
   - Route to Jev only a step that asks the same typed question over many items (classify, gate, rank, dedupe). Plans, code,
     prose, single decisions and anything a deterministic check can compute stay with the Opus agents.
   - Wire it in by adding this paragraph to the body of each subagent that should use it. That subagent needs `Bash` (the
     skill's script) and `Skill` among its tools, or no `tools` line at all; the read-only `explorer` above has neither.
     ```text
     When a step is the same yes/no, pick-one or score question over many items, follow the judging-with-jev skill
     instead of reading every item yourself. Act on its confident answers, decide the deferred ones yourself, and report
     how many were asked, acted on, deferred and fell back. If Jev is off, do the step the usual way and say so.
     ```
     The `skills` frontmatter field can preload the skill's full text at startup instead; a listed skill that is missing is
     skipped with only a warning in the debug log, so check that it loaded.
   - This is the post's idea in a form that exists: Jev settles the clear cases, and the Opus agent sees only the ones Jev
     defers.
7. **Verify.** A new session shows `Advisor Tool (experimental) is on and may use more tokens · /advisor`. During a
   consultation the transcript shows an `Advising` line with the advisor model's name. While a subagent runs, `/tasks` shows
   its model and effort. With step 6 in place, the run ends with the `jev:` line that `judging-with-jev` defines.

To undo: `/advisor off`; `/effort auto` clears the saved level for the active model; the subagent files and the `CLAUDE.md`
line are reverted from their diffs.

## Pitfalls

- The advisor can be missing without an error. Claude Code does not attach an advisor that ranks below the main model, and
  when the API refuses a pairing the conversation continues without one. A Fable main model accepts only a Fable advisor.
- Each advisor call reads the full transcript again, uncached, at the advisor model's rates. On plans where Fable bills to
  usage credits, a Fable advisor does too.
- The post names Fable 5.1 and Opus 5.5. The `fable` and `opus` aliases resolve to whatever version the installed Claude Code
  release defaults to, so do not write version numbers into the setup.
- Version floors from the docs: `/advisor` outside the terminal picker needs Claude Code v2.1.260, a Fable 5.1 advisor
  v2.1.257, a Fable 5.2 advisor v2.1.321, effort in `/tasks` v2.1.242.
- The advisor is marked experimental: behaviour, pricing and availability may change. When a step here disagrees with the
  advisor page, the page wins.
- Three Opus subagents at `medium` is the post's choice, not a rule. `model-tiering` puts bulk mechanical work on a cheaper
  tier; decide with that skill before copying the tree as is.

## Source

- Post: https://x.com/thedelost/status/2104677530825634273 · @thedelost · 2026-09-28 (`raw/20260928-claude-code-fable-advisor-jev-tree.md`).
- Claude Code documentation, read 2026-11-10:
  - https://code.claude.com/docs/en/advisor — `/advisor`, `advisorModel`, `--advisor`, accepted pairings, consent, requirements, what a session shows, cost, turning it off.
  - https://code.claude.com/docs/en/model-config — effort levels, `/effort`, resolution order, the `effortLevel` exception for Opus 5.5, aliases.
  - https://code.claude.com/docs/en/settings-reference — `advisorModel`, `effortLevel`, `modelSettings`, `env`.
  - https://code.claude.com/docs/en/sub-agents — definition files, frontmatter fields (`model`, `effort`, `tools`, `skills`), `/tasks`.
  - https://code.claude.com/docs/en/env-vars — the variables in step 1 and "Features that need feature-flag fetching".
  - https://code.claude.com/docs/en/memory — where the project and user `CLAUDE.md` files live.
- The API-side advisor tool, for code that calls the Claude API instead of a Claude Code session: `skills/model-tiering/references/advisor-tool.md`.
