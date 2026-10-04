# Skill review: scanning-agent-skills — PASS

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `reviewer-approved`
- Content hash: `5b7900c8b36740e78972c56233b8df937972549235962cfc4fb274cf63e52bd9`
- Static scan (`static_scan.py 2`): 0 block, 10 review findings; review rules R1, R2, R6, R8
- SkillSpector: not installed
- Gate (routine step 4): all checks passed
- Not audited (upstream): NVIDIA SkillSpector (github.com/NVIDIA/skillspector, installed unpinned via uv tool install from git, an optional local Docker build, and the optional skillspector[mcp] MCP server): not audited

## 摘要
過關。只會從 NVIDIA 官方 repo 安裝 SkillSpector，金鑰只經環境變數讀取。建議喺第 4、6 步加 `--no-llm`，同埋鎖定版本。冇審查到嘅部分：SkillSpector 本身。

## Reviewer verdict
```json
{
  "skill": "scanning-agent-skills",
  "verdict": "PASS",
  "content_hash": "5b7900c8b36740e78972c56233b8df937972549235962cfc4fb274cf63e52bd9",
  "static": {
    "block": 0,
    "review_rules": [
      "R1",
      "R2",
      "R6",
      "R8"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R1": "acceptable: false positive; line 76 names SkillSpector's rule id SC2 ('curl|bash') in a findings glossary, and no download is piped into a shell anywhere in the skill",
    "R2": "acceptable: the only installs are SkillSpector from its official repo github.com/NVIDIA/skillspector (uv tool install from git, the [mcp] extra with --force, or a local docker build of the cloned official repo), all matching the README captured in raw/; lines 3 and 21 only name third-party installs as the trigger to scan; the installs are unpinned (git HEAD)",
    "R6": "acceptable: API keys appear only as environment variable names the user sets (ANTHROPIC_API_KEY, OPENAI_API_KEY, NVIDIA_INFERENCE_KEY); nothing is printed, written or committed, and the Pitfalls say never to paste keys into a skill folder or report",
    "R8": "acceptable: line 21 names ~/.claude/skills and MCP servers only as install events that should trigger a scan; the one config write is step 7's optional 'claude mcp add skillspector -- skillspector mcp', which is shown in full, runs a local stdio server from the same official package, and comes with a warning not to expose the http transport"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: destinations are disclosed and belong to the tool or to the LLM provider the user picks (OSV.dev gets dependency names only; LLM mode sends file contents to the chosen provider, with a warning to skip it for private code); however, the step 4 json/sarif commands and the step 6 baseline commands leave out --no-llm, so they run with SkillSpector's default nv_build provider unless the user sets one",
    "S4": "ok",
    "S5": "acceptable: every install comes from the official NVIDIA/skillspector repository, which matches the project; none is pinned to a tag or commit",
    "S6": "ok",
    "S7": "acceptable: the only agent-config change is an optional, explicitly shown 'claude mcp add' for SkillSpector's own local stdio MCP server; there are no permission, sandbox, hook or memory-file changes",
    "S8": "ok",
    "S9": "acceptable: the triggers are specific to skill and MCP installs and audits; they overlap with auditing-agent-skills on vetting a third-party skill before install, but that skill uses this one as its second scanner",
    "S10": "ok"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "NVIDIA SkillSpector (github.com/NVIDIA/skillspector, installed unpinned via uv tool install from git, an optional local Docker build, and the optional skillspector[mcp] MCP server): not audited",
  "summary": "SkillSpector setup guide with a single SKILL.md: no block findings, no shipped code, and every install and claim matches the official NVIDIA README captured in raw/. Main fix: add --no-llm to the step 4 report commands and the step 6 baseline commands so they do not quietly run LLM mode, and pin the git installs to a release tag. The optional MCP registration should also be mentioned in the description."
}
```
