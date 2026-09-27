---
name: scanning-agent-skills
description: Scans third-party agent skills, plugins and MCP servers with NVIDIA SkillSpector before install and gates on its 0-100 risk score. Use when installing a skill from GitHub, a zip or npx skills add, adding an MCP server, or auditing skills already installed.
metadata:
  source_url: "https://www.instagram.com/reel/DcllmSNv_Bk/"
  source_platform: "instagram"
  author: "nick_saraev"
  captured_at: "2026-09-27"
  engagement: "likes=3.9K comments=3.3K"
  origin_type: "post"
  vault_status: "draft"
---

# scanning-agent-skills

Run a static (and optionally LLM-assisted) security scan on a skill, plugin or MCP server before it is installed
into Claude Code, Codex, Gemini CLI or any other agent, and decide allow / warn / block from the result.
Tool: NVIDIA SkillSpector (`github.com/NVIDIA/SkillSpector`, Apache-2.0, Python 3.12+).

## When to use
- Before `npx skills add <owner>/<repo>`, `claude plugin install`, copying a `SKILL.md` into `~/.claude/skills/`, or adding an MCP server.
- When a starred or captured repo is about to be promoted from "saved" to "installed".
- Periodic audit of skills already installed (scan the skills folder as a batch).
- In CI for a repo that publishes skills (SARIF output, non-zero exit on high risk).

## Steps
1. Install the CLI once (no execution of the target skill happens at any point):
   ```bash
   uv tool install git+https://github.com/NVIDIA/skillspector.git
   # later: uv tool update skillspector
   ```
   Without Python: `git clone https://github.com/NVIDIA/skillspector.git && cd skillspector && docker build -t skillspector .`,
   then use `docker run --rm -v "$PWD:/scan" skillspector scan <target> --no-llm`.
2. Static scan first (file contents stay local; only dependency names go to OSV.dev):
   ```bash
   skillspector scan https://github.com/<owner>/<repo> --no-llm
   skillspector scan ./path/to/skill/ --no-llm
   skillspector scan ./SKILL.md --no-llm
   skillspector scan ./skill.zip --no-llm
   ```
3. Optional semantic pass to cut false positives (precision ~87%). No API key needed if a CLI agent is logged in:
   ```bash
   export SKILLSPECTOR_PROVIDER=claude_cli   # or codex_cli, gemini_cli
   skillspector scan https://github.com/<owner>/<repo>
   ```
   Hosted alternatives: `SKILLSPECTOR_PROVIDER=anthropic` + `ANTHROPIC_API_KEY`, `openai` + `OPENAI_API_KEY`, `ollama` (local).
   LLM mode sends file contents to that provider; skip it for private code you may not share.
4. Save a report when the result goes to someone else:
   ```bash
   skillspector scan <target> --no-llm --format markdown --output skillspector-report.md
   skillspector scan <target> --format json --output skillspector-report.json
   skillspector scan <target> --format sarif --output skillspector.sarif   # CI / IDE
   ```
5. Apply the gate:
   | Score | Severity | Recommendation | Action |
   |---|---|---|---|
   | 0-20 | LOW | SAFE | install |
   | 21-50 | MEDIUM | CAUTION | read every finding, then ask the user |
   | 51-100 | HIGH / CRITICAL | DO NOT INSTALL | block, report findings |
   Exit code: `0` score <= 50, `1` score > 50, `2` scan error. Add `--fail-on-findings` to fail on any active finding,
   `--fail-on-incomplete` to fail when analysis was partial.
6. For a skill you have reviewed and accept, record a baseline so re-scans only show new issues:
   ```bash
   skillspector baseline ./my-skill/ -o .skillspector-baseline.yaml
   skillspector scan ./my-skill/ --baseline .skillspector-baseline.yaml
   ```
7. Optional: let the agent scan by itself before installing, via the MCP server:
   ```bash
   uv tool install --force 'skillspector[mcp] @ git+https://github.com/NVIDIA/skillspector.git'
   claude mcp add skillspector -- skillspector mcp
   ```
   The tool `scan_skill(target, use_llm, output_format)` returns `risk_score`, `severity`, `recommendation`,
   `safe_to_install`, `findings`, `llm_used`, `scan_mode`.

## Reading findings
- High-signal IDs: `SC2` curl|bash, `SC3` obfuscated code, `E2` env-var harvesting, `PE3` credential access,
  `TT3` credentials to network, `RA2` cron/startup persistence, `P1`/`P2` instruction override or hidden instructions,
  `TR2` trigger that shadows a built-in command or another skill, `TP1`/`TP2` hidden text or Unicode tricks in MCP tool metadata.
- A static-only low score is not a clean bill of health: check `scan_mode` / `llm_used` before calling it safe.
- Executable scripts multiply the score by 1.3; skills that ship scripts are ~2x more likely to be vulnerable.

## Pitfalls
- It is a scanner, not a sandbox: it never runs the skill and cannot contain one you install anyway.
- Weak on non-English text, text inside images, and compiled/encrypted content: inspect those by hand.
- `skillspector mcp --transport http` has no authentication; keep it on stdio or `127.0.0.1`.
- `opencode_cli` provider fails closed unless OpenCode is exactly the version the release pins.
- Default provider is `nv_build` (needs `NVIDIA_INFERENCE_KEY`); set `SKILLSPECTOR_PROVIDER` or pass `--no-llm`.
- Never paste real API keys into a skill folder or report; use environment variables.

## Source
- Instagram reel by Nick Saraev (@nick_saraev), 2026-08-28: https://www.instagram.com/reel/DcllmSNv_Bk/
- Repo README: https://github.com/NVIDIA/SkillSpector (fetched 2026-09-27); vault note `wiki/pages/20260828-nvidia-skillspector-skill-security-scanner.md`, verbatim text in `raw/20260828-nvidia-skillspector-skill-security-scanner.md`.
