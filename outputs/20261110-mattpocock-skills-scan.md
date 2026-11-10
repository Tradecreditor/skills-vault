# mattpocock/skills — security scan before install (2026-11-10)

Scan of Matt Pocock's agent skills before 14 of them were installed into this vault at project level
(`.claude/skills/`), following `skills/scanning-agent-skills/SKILL.md`. Captured page:
`wiki/pages/20261003-matt-pocock-skills-repo-agent-skills.md`.

## What was scanned
- Repo: `https://github.com/mattpocock/skills`, commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`
  (2026-10-31, "software-factory: glossary skill for designing a factory (#1316)").
- NVIDIA SkillSpector v2.12.0 (source commit `33f878c`), static mode only (`--no-llm`: no file content sent to any model).
  OSV.dev answered 403 through the session proxy, so dependency advisories were not checked; none of the 14 installed
  folders has a dependency manifest.
- The vault's own `skills/auditing-agent-skills/scripts/static_scan.py` (version 4) on each of the 14 folders.
- Every file in the 14 folders (47 files) read by the scanning agent.

## Result
| Skill | SkillSpector | Finding | Flagged text | Judgment |
|---|---|---|---|---|
| `diagnosing-bugs` | **27** MEDIUM | HIGH `P6` "Direct Prompt Extraction", `scripts/hitl-loop.template.sh:10` | the comment `step "<instruction>" → show instruction, wait for Enter` | false positive: the words "show instruction" matched; the 45-line template only uses `read` and `printf`, no network, no file access |
| `to-tickets` | 17 LOW | HIGH `TM2` "Chaining Abuse", `SKILL.md:40` | prose on expand–contract refactors ("First expand… Then migrate…") | false positive |
| `grilling` | 8 LOW | MEDIUM `EA2`, `SKILL.md:28` | "don't ask the user for anything you could look up yourself" | false positive |
| `pr` | 8 LOW | MEDIUM `AS3` "Skill Enumeration", `SKILL.md:9` | a credits URL ending `skills/show-me/SKILL.md` | false positive |
| `setup-matt-pocock-skills` | 7 LOW | MEDIUM `EA2`, `SKILL.md:61` | "write it without asking" (the default domain-docs layout) | false positive; see "What to know" |
| `to-spec`, `implement`, `implement-spec`, `tdd`, `writing-for-agents`, `codebase-design`, `domain-modeling`, `research`, `prototype` | 0 LOW | none | | |

- `static_scan.py`: 0 block findings in all 14 folders. Review-class only: `diagnosing-bugs` R5 (`SKILL.md:27`, "Curl / HTTP
  script against a running dev server") and R11 (ships `scripts/hitl-loop.template.sh`); `tdd` R5 ×4 (`mocking.md:44–51`,
  `fetch(...)` in TypeScript examples).
- Whole-repository scan: 100 / 100, exit 1, 213 issues over 198 files. It is not the score of what was installed: the scanner
  treats the repository as one skill. 172 of the issues are unpinned dependencies in `package.json` / `package-lock.json`,
  19 are the text `npx skills` in docs, and the HIGH findings are in folders that were not installed
  (`misc/git-guardrails-claude-code`, `wizard/template.sh`, `in-progress/software-factory`, `to-questionnaire`, `docs/`).
  Only the 5 findings in the table are inside the 14 installed folders.

## Gate and decision
The vault's gate is 0–20 install, 21–50 read every finding and ask Jeff, above 50 do not install. `diagnosing-bugs` at 27 put
the install on hold. Jeff, 2026-11-10: accept that finding as a false positive and install all 14.
Excluding the script does not lower the score (`--exclude 'scripts/*'` gives 37: the exclusion is reported as partial coverage).

## What was installed
`npx skills@latest add mattpocock/skills@4ae2317ddb22b046e26455e4f9c9b3aaaf62212d -a claude-code -s <the 14 names> --copy -y`
(`skills` CLI 1.7.6): copies, no symlinks, 44 files under `.claude/skills/`, 14 entries added to `skills-lock.json`
(`source: mattpocock/skills`, `sourceType: github`). `diff -r` of every installed folder against the scanned clone: identical.

Installed: `to-spec`, `to-tickets`, `implement`, `implement-spec`, `tdd`, `diagnosing-bugs`, `pr`, `setup-matt-pocock-skills`,
`codebase-design`, `domain-modeling`, `research`, `prototype` (from `skills/engineering/`), `writing-for-agents`, `grilling`
(from `skills/productivity/`).

Left out on purpose (both score 0):
- `handoff`: it writes a conversation summary to the OS temp directory; this vault's `handoff.md` and
  `skills/keeping-handoff-docs` mean something else, and one name for two things invites mistakes.
- `code-review`: same name as Claude Code's built-in `/code-review`. `implement` and `implement-spec` call a skill named
  `code-review`, which here resolves to the built-in one.

`skills-lock.json` does not record the commit; `npx skills update` would pull whatever upstream has then. Scan again before updating.

## What to know before using them
- `/setup-matt-pocock-skills` was NOT run. It edits `CLAUDE.md` (or `AGENTS.md`), writes `docs/agents/*.md`, may run
  `git remote add`, and creates tracker labels with `gh label create` when `triage` is installed. Running it is Jeff's call.
  Without it, `to-spec` and `to-tickets` have no tracker configured and will say so.
- `to-spec` and `to-tickets` publish issues to the configured tracker (`gh issue create` on GitHub).
- `implement` commits to the current branch; `implement-spec` creates an integration branch, worktrees and possibly a draft PR.
- `prototype` commits throwaway code to a separate branch; `domain-modeling` creates `GLOSSARY.md` and `docs/adr/` at the repo root.
- `triage` (it checks out and runs code from external pull requests) is not installed.
- A static scan is not a clean bill of health: the LLM pass was not run.
