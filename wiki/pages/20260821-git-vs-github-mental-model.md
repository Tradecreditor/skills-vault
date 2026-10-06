---
title: "Git vs GitHub mental model: a change has to climb (RickTheEngineer)"
slug: 20260821-git-vs-github-mental-model
type: video
status: draft
source_url: "https://www.instagram.com/reel/DcTwB-cM64q/"
source_platform: instagram
author: "rick.theengineer"
published: "2026-08-21"
captured_at: "2026-10-06T00:00:00Z"
captured_by: "routine:capture-link"
canonical_id: "instagram:DcTwB-cM64q"
engagement: "not returned by reader"
tags: [topic/agent-tooling, git, github, version-control, beginner]
related: []
needs_manual_text: false
---
## 摘要
呢條 reel 用一個「變更要逐級爬上去」嘅心智模型解釋 Git 同 GitHub 唔係同一樣嘢：Git 係喺本機行嘅版本控制系統，GitHub 只係託管 Git repository 嘅網站。一個改動要經過 working directory、staging area、repository（commit）同 remote（push）四層。作者再用一句講晒 branch、merge、conflict、revert 同 reset，並指出日常 90% 只用 edit → add → commit → push，多人協作時 push 之前要先 pull。適合 Git 新手作速查。

## Key facts
- Git = local version control system; GitHub = website hosting Git repositories.
- Four stages: working directory → staging area → repository (`git commit`) → remote (`git push`).
- branch = new line off a commit; merge = line folding back; merge conflict = two branches changed the same line.
- revert = a NEW commit that undoes an old one (nothing erased); reset = moves the branch pointer backwards (easy to misuse).
- Daily loop: edit → `git add` → `git commit` → `git push`; `git pull` before you push when collaborating.
- Caption is fully substantive; spoken audio not fetched (no Supadata call needed).

## 點解值得留意
- 一頁式 Git 心智模型，可作為教非技術人用 agent / vault 同步流程嘅講解素材。
- 同 vault 嘅 `git pull --rebase` 再 push 流程直接相關。

## Source
- https://www.instagram.com/reel/DcTwB-cM64q/ — rick.theengineer, 2026-08-21. Engagement counts not returned. Reader: Jina (caption in Title and body).

- None yet.
