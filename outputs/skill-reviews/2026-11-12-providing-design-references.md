# Skill review: providing-design-references (2026-11-12)

**Verdict: PASS**

- Reviewed by: routine:skill-review (independent `vault-skill-reviewer` subagent, verdict checked by the routine)
- Content hash (H): `78b15525add465fd5f974fc100f2c8c4c43ae8526381ddf28719a7e7916c7f87`
- Static scan: floor `NEEDS_REVIEW`, block findings 0, review findings 2, review rules R2 (R2×2)
- SkillSpector: not installed

## Verdict JSON
```json
{
  "skill": "providing-design-references",
  "verdict": "PASS",
  "content_hash": "78b15525add465fd5f974fc100f2c8c4c43ae8526381ddf28719a7e7916c7f87",
  "static": {"block": 0, "review_rules": ["R2"]},
  "skillspector": "not installed",
  "rules": {"R2": "acceptable: optional, user-run install of the transitions.dev skill from the project's own GitHub repo (Jakubantalik/transitions.dev, the source its site documents), pinned to commit 20d70c1262bf721c0300c2946cbe1fc7605a555c, scanned with the vault's scanning-agent-skills before install, installed with the pinned official skills CLI (skills@1.7.6) and --skill to limit scope; the third-party status is stated clearly"},
  "checklist": {"S1": "ok", "S2": "ok", "S3": "ok", "S4": "ok", "S5": "acceptable: the only install is optional and from the upstream project's own repo at a pinned commit, through the pinned vercel-labs skills CLI, with a scan step first; it also warns against the unpinned owner/repo@ref form and the separate npx transitions-dev package", "S6": "ok", "S7": "ok", "S8": "ok", "S9": "acceptable: 'vibe-coding an app' is broad, but the other triggers (generic UI output, matching spacing or type, pitch decks) are specific to design references and it claims no built-in commands", "S10": "ok"},
  "quality": "Pass",
  "critical": [],
  "upstream": "transitions.dev skill (github.com/Jakubantalik/transitions.dev at commit 20d70c12, Transitions.dev License) and the skills CLI (npm skills@1.7.6, github.com/vercel-labs/skills): not audited",
  "summary": "Static floor NEEDS_REVIEW with 0 block findings; SkillSpector is not installed. The single file, /home/user/skills-vault/skills/providing-design-references/SKILL.md, is a short and clear guide to using screenshots as design references. Its only install is optional, pinned, gated by a scan step and labelled as third-party, and the skill it references (/home/user/skills-vault/skills/scanning-agent-skills/SKILL.md) exists."
}
```

## 說明
通過。單一 SKILL.md，講點樣用截圖做設計參考；唯一嘅安裝係可選、鎖定 commit、先掃描、並標明係第三方嘅 transitions.dev skill。冇 block 級發現。未審核部分：transitions.dev skill 上游（commit 20d70c12）同 skills CLI（skills@1.7.6）。
