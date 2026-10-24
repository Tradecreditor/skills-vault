# Prompt: blind review of the gold labels (optional, before or after the run)

Most gold labels were written by one Claude Code session on 2026-10-24, and for suite A that session could see Jev 1.13's
production probabilities in the hot-list reports. That can tilt the key toward Jev. A blind second labeller removes the doubt.
Run this with a model that is **not** one of the contestants, or give `cases.csv` to a person.

---

You are labelling items for Jeff's skills-vault. You will get cases one at a time as JSON `{state, questions}`.
For each question, answer from the state and the definitions in `instructions` / `criteria` only:

- noul: `true` or `false`, plus `unsure` if a careful reader could reasonably go either way.
- score: the level number (0 = first criterion) that fits best, plus the lowest and highest level you would accept.
- choice: the label that fits best.

Return one JSON line per case: `{"id": "...", "answers": {...}, "unsure": [question names]}`.
Do not look at any other field of `cases.jsonl`; read only `request`. Do not search the web.

---

Then compare: `python3 - <<'EOF'` with a few lines that load `cases.jsonl` and your labels and list every case where your
label differs from `gold`. Send that list to Jeff with one sentence per case. Jeff decides; nobody edits `cases.jsonl` in place
(a corrected key is a new file, `cases-v2.jsonl`, so earlier runs stay comparable).
