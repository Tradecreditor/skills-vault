# inbox/
Drop zone. Anything here is unprocessed. The core agent (or the next capture run) turns each file into `raw/` + `wiki/pages/`.
Web Clipper template "Skill capture" writes here with `source_url`, `author`, `published`, `status: draft` frontmatter.
Nothing sweeps this folder automatically (decision 2026-10-01: no inbox sweep). A file here is processed only when its path or link is handed to a capture session; for links, prefer the Telegram bot or `scripts/capture.sh`, which fire the capture routine directly.
