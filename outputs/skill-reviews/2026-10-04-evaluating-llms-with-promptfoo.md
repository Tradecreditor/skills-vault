# Skill review: evaluating-llms-with-promptfoo — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `26c39aef27c8158448e486953fafcbaa64d9cd19a1b587dc6bc551315f5f3794`
- Static scan (`static_scan.py 2`): 0 block, 5 review findings; review rules R2, R6
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: S10; reviewer verdict FAIL
- Not audited (upstream): promptfoo (npm package promptfoo, Homebrew formula promptfoo, PyPI package promptfoo, github.com/promptfoo/promptfoo): not audited

## 摘要
唔過關。Pitfalls 寫住「資料唔會離開你部機」，但 skill 自己嘅步驟會將 prompt 同測試資料送去 OpenAI／Anthropic API，係錯誤嘅私隱聲明（S10）。改正嗰句之後就可以再審。

## Reviewer verdict
```json
{
  "skill": "evaluating-llms-with-promptfoo",
  "verdict": "FAIL",
  "content_hash": "26c39aef27c8158448e486953fafcbaa64d9cd19a1b587dc6bc551315f5f3794",
  "static": {
    "block": 0,
    "review_rules": [
      "R2",
      "R6"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "acceptable: npm promptfoo, Homebrew promptfoo, PyPI promptfoo and npx promptfoo@latest (lines 30-36) are the install routes promptfoo's own README documents (raw/20260923-promptfoo.md), and the user runs them; nothing is pinned and npm -g installs globally, so pinning a version or using npx/a local devDependency is advised",
    "R6": "acceptable: lines 49-50 are placeholder exports (sk-...) of provider keys into environment variables the user sets; nothing reads, prints, writes or commits a key"
  },
  "checklist": {
    "S1": "ok",
    "S2": "ok",
    "S3": "acceptable: the only destinations are the LLM provider APIs the user configures, which evaluating models requires; any network use on promptfoo's own side (result sharing, red-team attack generation) is upstream behaviour and was not audited",
    "S4": "acceptable: keys come only from environment variables the user exports; the file has placeholders only and no step echoes or stores a key",
    "S5": "acceptable: every install names promptfoo's official package or formula as documented upstream, with a no-install npx alternative; unpinned",
    "S6": "ok",
    "S7": "ok",
    "S8": "ok",
    "S9": "acceptable: the triggers are tied to promptfoo-style evals and red teaming, but 'comparing models' and 'securing AI apps' are broad enough to fire on general model-choice or app-security questions; narrowing is advised",
    "S10": "fail: Pitfalls line 86 says 'Evals run 100% locally — no data leaves your machine', yet steps 3-4 set OpenAI/Anthropic keys, so every prompt and test case is sent to those providers' APIs. Upstream only claims that promptfoo itself does not upload prompts, so the skill gives a false data-handling assurance"
  },
  "quality": "Needs Improvement",
  "critical": [],
  "upstream": "promptfoo (npm package promptfoo, Homebrew formula promptfoo, PyPI package promptfoo, github.com/promptfoo/promptfoo): not audited",
  "summary": "FAIL on S10 only: line 86 says no data leaves the machine, but the skill's own steps send prompts and test data to the OpenAI/Anthropic APIs. Replace that line with an accurate one (data goes to the configured provider; use a local provider such as Ollama to keep it local) and re-review. The static scan is clean (0 block, R2/R6 acceptable). Quality needs improvement: there is no example promptfooconfig.yaml, and 'promptfoo eval --ci', the redteam subcommands and the datacenter-IP pitfall do not appear in the captured source and are unverified."
}
```
