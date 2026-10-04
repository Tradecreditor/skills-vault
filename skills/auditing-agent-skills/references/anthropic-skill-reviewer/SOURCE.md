# Source of the vendored files

- `skill-reviewer.md`: Anthropic's `skill-reviewer` agent from the official Claude Code plugin marketplace,
  https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/agents/skill-reviewer.md
  (repository commit `d182ca456ca09d31d139f7d3818d1d333b103cce`, 2026-10-02), copied verbatim on 2026-10-04.
- `LICENSE`: that plugin's license file (Apache License 2.0), copied verbatim.

Neither file has been modified. It is kept here as a reference for the quality step of `auditing-agent-skills`; it is not
registered as an agent in this repository. To use Anthropic's version as a live agent instead:
`/plugin marketplace add anthropics/claude-plugins-official` then `/plugin install plugin-dev@claude-plugins-official`.
To refresh: copy the two files again from the current `main` and update the commit above.
