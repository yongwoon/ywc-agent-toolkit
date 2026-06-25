# Task: 000029-020-refactor-pr-health-handler

## Prerequisites

- [ ] batch 단일 branch에서 작업 중인지 확인
- [ ] upstream 참조: `gh pr diff 133 --repo yongwoon/develop-with-llm` (claude-code 경로만)
- [ ] "before" 상태 확인: `ywc-handle-pr-reviews/SKILL.md`에 `### 1.` 번호 체계 + `### 6.5 CI Status Check` + `### 6.6 Merge-Readiness` 존재, `## Definition of Done` 부재

## Allowed Edit Scope

- `claude-code/skills/ywc-handle-pr-reviews/**`
- 그 외 경로 편집 금지(특히 executor skill — `000029-030` 담당, `codex/**`).

## Stop Conditions

- 이미 `## Definition of Done` 또는 `### Step 7` 형식이 존재하면 중단(중복 적용).
- es/zh README 누락 시 중단·보고.
- Step 재번호화 후 1–9 비연속이거나 내부 참조가 깨지면 중단·재검토.

## Implementation Steps

- [ ] frontmatter `description`을 mergeable framing으로 재작성하고 trigger에 `fix PR CI`, `PR conflict 해결` 추가.
- [ ] Announce 줄 + intro 문단을 "comment 응답이 아니라 PR을 mergeable로 남긴다 — 3 gate" 취지로 갱신.
- [ ] Rationalization Defense에 "No unresolved comments — nothing to handle, the PR is done" 1행 추가(zero comment는 gate 1만 통과; Step 7·8 필수).
- [ ] `## Definition of Done` 신설: 3-gate 표(① comments Steps 2–5, ② CI Step 7, ③ merge-readiness Step 8) + "착수 전 TodoWrite로 3 gate 등록" 강제 문구.
- [ ] step 헤더를 `### 1.`→`### Step 1:` … `### Step 9`로 연속 재번호화.
- [ ] Step 2 마지막에 empty-array reroute 추가: `[]`이면 Step 3–5는 건너뛰되 Step 7(CI)·Step 8(merge-readiness)는 반드시 실행 — final summary로 직행 금지.
- [ ] `### 6.5`→`### Step 7: CI Status Gate — run on EVERY invocation`(zero-comment 포함 항상 실행 문구) + 내부 "proceed to Step 8"로 갱신.
- [ ] `### 6.6`→`### Step 8: Merge-Readiness / Conflict Gate — run on EVERY invocation` + "proceed to Step 9".
- [ ] `### 7. Final Summary`→`### Step 9: Final Summary`(comments/CI/merge-readiness 3-gate 상태 모두 보고).
- [ ] DONE_WITH_CONCERNS 잔존 참조의 step 번호(예: "Step 7's summary"→"Step 9's summary")를 정합화.
- [ ] `README.{md,en,es,ja,ko,zh}.md`: intro mergeable/three-gates 문단 + Key Features 항목(en/ja) + 특징·실행 흐름 renumber(md/ko); es/zh는 en 기준 번역.

## Task Verify

- [ ] `rg -n "Definition of Done" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (>0)
- [ ] `rg -n "EVERY invocation" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (Step 7·8, ≥2)
- [ ] `rg -n "### Step 9: Final Summary" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (>0)
- [ ] `! rg -n "### 6\.5|### 6\.6" claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (구 번호 잔존 없음)
- [ ] `ls claude-code/skills/ywc-handle-pr-reviews/README.{es,zh}.md`
- [ ] `wc -l claude-code/skills/ywc-handle-pr-reviews/SKILL.md` (≤500)

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-handle-pr-reviews/README*.md"` (0 errors)
- [ ] `git diff --name-only` 결과가 `claude-code/skills/ywc-handle-pr-reviews/` 내부로 한정(특히 `codex/` 미포함)
