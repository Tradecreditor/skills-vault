# Skill review: using-obsidian-skills (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `0e6b3c37034ee19f1bfdb0f175368c90c35613e6f8ca70b6b8cc340ee72a0adb`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 4, review rules R2, R8 (R2×3, R8×1)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "using-obsidian-skills",
  "verdict": "PASS",
  "content_hash": "0e6b3c37034ee19f1bfdb0f175368c90c35613e6f8ca70b6b8cc340ee72a0adb",
  "static": {"block": 0, "review_rules": ["R2", "R8"]},
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: the /plugin marketplace add, npx skills@1.7.6 add and git clone lines all install kepano/obsidian-skills from its own GitHub repository (github.com/kepano/obsidian-skills), which is the pack the description says it installs. The user's agent runs them with normal prompts, and the skill says the upstream is unpinned.",
    "R8": "acceptable: copying the pack's skills/ folder into ~/.codex/skills, or into the project's .claude/ folder (Option C), is the skill's stated purpose of installing skills for the agent. It writes no settings, hooks, MCP servers or memory files, and it warns that .claude/ is protected in this vault."
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "ok",
    "S4": "ok",
    "S5": "acceptable: every install source is the official kepano/obsidian-skills repo. The skills CLI is pinned to 1.7.6, but the upstream repo is unpinned, and the skill says so. No piping into a shell and no sudo.",
    "S6": "ok",
    "S7": "acceptable: it adds skills to agent skill folders (.claude/, ~/.codex/skills, ~/.opencode/skills), which is its declared purpose. Permissions, hooks, MCP servers and CLAUDE.md/AGENTS.md are left alone.",
    "S8": "ok",
    "S9": "ok",
    "S10": "ok"
  },
  "quality": "Pass",
  "critical": [],
  "upstream": "kepano/obsidian-skills (github.com/kepano/obsidian-skills, unpinned), the skills CLI (npm package skills@1.7.6), and the Defuddle and Knap tools it links to without install commands: not audited",
  "summary": "The skill is one SKILL.md with no scripts. It installs kepano/obsidian-skills from its official repository using the upstream README's install options, and no block findings were raised. The R2 and R8 hits are the installs and skill-folder writes the description declares. Minor quality notes: Options C and E give prose rather than exact commands, and the review metadata in the frontmatter is stale against the current hash."
}
```

## 說明
通過。呢個 skill 只有一個 SKILL.md，冇 script，靜態掃描冇 block 級發現；R2（安裝指令）同 R8（寫入 skill 資料夾）都係佢描述入面講明嘅用途：由 kepano/obsidian-skills 官方 repo 安裝 Obsidian skills。未審核部分：kepano/obsidian-skills 上游本身（未鎖版本）、skills CLI（npm skills@1.7.6），以及只有連結、冇安裝指令嘅 Defuddle 同 Knap。
