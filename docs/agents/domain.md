# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring it.
The vault's rules live in `CLAUDE.md` (`AGENTS.md` is an identical copy): where a glossary entry or a decision record
disagrees with `CLAUDE.md`, `CLAUDE.md` wins and the disagreement is worth reporting.

## Before exploring, read these

- **`GLOSSARY.md`** at the repo root.
- **`docs/adr/`**: read the decision records that touch the area you are about to work in.

If these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The
`/domain-modeling` skill creates them when a term or a decision actually gets resolved.

## File structure

Single-context repo:

```
/
├── GLOSSARY.md
└── docs/
    ├── agents/        ← this folder: configuration the engineering skills read
    └── adr/
        └── 0001-<decision>.md
```

## Use the glossary's vocabulary

When your output names a domain concept (in a ticket title, a refactor proposal, a hypothesis, a test name), use the term as
defined in `GLOSSARY.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use
(reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007, but worth reopening because…_
