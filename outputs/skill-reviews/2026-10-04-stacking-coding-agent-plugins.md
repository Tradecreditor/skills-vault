# Skill review: stacking-coding-agent-plugins — FAIL

- Reviewed: 2026-10-04T15:35:29Z by the `vault-skill-reviewer` subagent (Opus), one skill per subagent; first run, from a Claude Code cloud session following `routines/skill-review.md` before the Routine existed
- Status set: `draft`
- Content hash: `c02d9e0be86915af7e3c52b0bc846c9f4e17ceb7d0db4a1e44f543b699f8831a`
- Static scan (`static_scan.py 2`): 0 block, 5 review findings; review rules R2
- SkillSpector: not installed
- Gate (routine step 4): not ok/acceptable: R2, S3, S4, S5, S7, S8, S9, S10; 3 critical quality issue(s); reviewer verdict FAIL
- Not audited (upstream): Graphify (github.com/Graphify-Labs/graphify, plus npm package 'graphify' via npx), Agent Skills (github.com/addyosmani/agent-skills via npx skills add), Ponytail (github.com/DietrichGebert/ponytail), OmniRoute (github.com/diegosouzapw/OmniRoute) and every provider OmniRoute forwards to: not audited, none fetched

## 摘要
唔過關，係今次風險最高嘅一個。佢會將 API 金鑰同程式碼經第三方 proxy（OmniRoute）轉發去冇講明嘅供應商，仲會加 session-start hook 同改 CLAUDE.md，描述全部冇提；安裝指令都係估出嚟（S3、S4、S5、S7、S8、S9、S10 全部 fail）。唔好喺任何 project 用。

## Reviewer verdict
```json
{
  "skill": "stacking-coding-agent-plugins",
  "verdict": "FAIL",
  "content_hash": "c02d9e0be86915af7e3c52b0bc846c9f4e17ceb7d0db4a1e44f543b699f8831a",
  "static": {
    "block": 0,
    "review_rules": [
      "R2"
    ]
  },
  "skillspector": "not installed",
  "rules": {
    "R2": "not acceptable: five installs, none pinned (lines 31-32, 45, 53, 62). The source reel (raw/20260921-4-claude-code-plugins.md) lists only repo links and holds back the setup commands for people who comment, so these commands are the drafter's guesses. The Ponytail clone-and-hook step contradicts its documented install, '/plugin marketplace add DietrichGebert/ponytail' (wiki/stars/DietrichGebert--ponytail.md). 'npx graphify build --repo' run outside the clone fetches whatever npm package is named 'graphify', not the cloned code. Only 'npx skills add addyosmani/agent-skills' looks like the project's own route."
  },
  "checklist": {
    "S1": "ok",
    "S2": "acceptable: each step serves one of the four tools the description names; the config changes the description leaves out are judged under S3, S7 and S8",
    "S3": "fail: step 4 points ANTHROPIC_BASE_URL at a third-party proxy that 'silently switches' to any of 352 unnamed providers, so prompts, repo contents and code go to hosts the skill neither names nor vets, and the description does not say so",
    "S4": "fail: sending traffic through OmniRoute gives the Anthropic API key or OAuth token to unaudited proxy code, and the fallback providers' keys go into omniroute.config.json without saying where it lives or keeping the keys in environment variables",
    "S5": "fail: unpinned clones from GitHub accounts whose only provenance is an Instagram reel; the commands are not from the source or the projects' docs; the Ponytail step contradicts its documented /plugin install; 'npx graphify' may resolve to a different npm package; 'Follow repo README' hands the install to upstream instructions nobody reviewed",
    "S6": "ok",
    "S7": "fail: the body has the agent add Graphify to CLAUDE.md or a session-start hook, register Ponytail as a session-start hook 'per the repo README', and override ANTHROPIC_BASE_URL. The description promises only to install plugins, and none of these changes is shown before it is made",
    "S8": "fail: two session-start hooks run third-party code at every session start, and the base-URL override persists; the description does not say it adds anything to startup",
    "S9": "fail: the triggers 'hitting context or quota limits' and 'wanting a structured workflow' come up in ordinary sessions, and what they trigger is installing third-party hooks and rerouting API traffic",
    "S10": "fail: guessed install commands are presented as fact; the Pitfalls section does not come from the source; unverified figures from the reel (~54%/94% less code, ~20% cost, 352 providers, 'eliminates redundant file reads') justify a startup hook and an API reroute; the description hides the CLAUDE.md, hook and base-URL changes"
  },
  "quality": "Needs Major Revision",
  "critical": [
    "Steps too vague to follow without guessing at commands: Ponytail says only 'Follow repo README to register as a Claude Code session-start hook'. OmniRoute has no install or run step, no endpoint value ('or equivalent') and no config format. Graphify says 'Add to CLAUDE.md or a session-start hook' without the content to add.",
    "Body does more than the description promises: the description says it installs four plugins, but the body also edits CLAUDE.md, adds session-start hooks and points ANTHROPIC_BASE_URL at a third-party proxy.",
    "Commands are wrong or made up: the source gives no setup commands; the Ponytail route contradicts its documented /plugin install; after 'cd graphify && npm install', running 'npx graphify build --repo /path' does not reliably run the cloned code."
  ],
  "upstream": "Graphify (github.com/Graphify-Labs/graphify, plus npm package 'graphify' via npx), Agent Skills (github.com/addyosmani/agent-skills via npx skills add), Ponytail (github.com/DietrichGebert/ponytail), OmniRoute (github.com/diegosouzapw/OmniRoute) and every provider OmniRoute forwards to: not audited, none fetched",
  "summary": "FAIL: the static scan found no blocking issues, but step 4 sends code and API credentials through an unaudited proxy that quietly forwards them to unnamed providers, and steps 1 and 3 add session-start hooks and CLAUDE.md edits the description does not mention. The install commands are guesses: the source reel gives only repo links, and the Ponytail step contradicts its documented /plugin install. Steps 3 and 4 cannot be followed without inventing commands."
}
```
