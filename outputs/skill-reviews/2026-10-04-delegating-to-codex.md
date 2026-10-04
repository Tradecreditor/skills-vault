# Skill review: delegating-to-codex — PASS

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `reviewer-approved`
- Content hash: `776a3a135735e30eb5f6520d161d0dddb4260b63a2b2129763b8ecdd5bb1aa5a`
- Static scan (`static_scan.py 2`): 0 block, 4 review findings; review rules R2, R8
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): openai/codex-plugin-cc (Claude Code plugin marketplace on GitHub) and @openai/codex (npm package, Codex CLI): not audited. The behaviour of /codex:* commands, including the read-only claim, the transfer command and the Stop hook, depends entirely on upstream code

## 摘要
過關。只用 OpenAI 官方嘅 Codex plugin 同 `@openai/codex` npm 套件，每個指令都由用家自己打。要留意：用 Codex 會將 diff 同對話內容送去 OpenAI，但 skill 冇講明。冇審查到嘅部分：上游 plugin 同 CLI。

## Reviewer verdict
```json
{
  "skill": "delegating-to-codex",
  "verdict": "PASS",
  "content_hash": "776a3a135735e30eb5f6520d161d0dddb4260b63a2b2129763b8ecdd5bb1aa5a",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: all three installs name the tool's own official sources: the openai/codex-plugin-cc marketplace (it matches metadata.source_url), its codex@openai-codex plugin, and the @openai/codex npm package. The user runs each one as an explicit slash command. They are unpinned, and the global npm install happens only through /codex:setup when Codex is missing",
    "R8": "acceptable: line 44 is a false positive. It says Codex reads its own ~/.codex/config.toml and does not write agent config. The one real config change, the review-gate Stop hook, is opt-in (--enable-review-gate) and documented with its cost risk"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only destinations are GitHub (the plugin), npm (the CLI) and OpenAI (the Codex service), all owned by the tool the skill is about. However, the skill never says that diffs, task text and, with /codex:transfer, the whole Claude Code session are sent to OpenAI",
    "S4": "ok",
    "S5": "acceptable: official OpenAI repo, marketplace and npm scope. Versions are not pinned, and the global npm install of @openai/codex is a stated prerequisite of the tool",
    "S6": "ok",
    "S7": "acceptable: installing the plugin is the skill's declared purpose and is shown as explicit user-run commands. The Stop-hook review gate is off by default, opt-in and comes with a warning, but the skill does not say how to turn it off",
    "S8": "acceptable: no deletions or resets. The only persistent changes are the global CLI install and the opt-in Stop hook, and both are documented",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "openai/codex-plugin-cc (Claude Code plugin marketplace on GitHub) and @openai/codex (npm package, Codex CLI): not audited. The behaviour of /codex:* commands, including the read-only claim, the transfer command and the Stop hook, depends entirely on upstream code",
  "summary": "The static scan found no block-class issues, and the R2 installs and R8 config mention both point to OpenAI's own official plugin and npm package, run explicitly by the user. The skill reads as a command reference more than a procedure. It does not say when to pick review, adversarial-review or rescue, does not say that code and session content go to OpenAI, and gives no way to turn the review gate off. Fixing that is worth doing before it is marked verified."
}
```
