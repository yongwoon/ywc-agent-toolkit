# Task: 000035-030-docs-executor-integrity-gates

## Prerequisites

- [ ] `000035-010-docs-impl-review-integrity-catalog` 병합 완료 (defect class 명칭 canonical source 확정)

## Allowed Edit Scope

- `claude-code/skills/ywc-sequential-executor/SKILL.md` 와 `claude-code/skills/ywc-parallel-executor/SKILL.md` 만 편집한다. 각 파일에서 Rationalization Defense 표만 손댄다.

## Stop Conditions

- 두 SKILL.md의 Rationalization Defense 표(sequential line 13, parallel line 15)를 찾지 못하면 멈추고 보고한다.
- 변경이 Rationalization Defense 표 1행을 넘어 Step 4/4c 실행 로직을 고쳐야 하면 멈추고 보고한다 (범위 초과 — spec은 executor 다른 섹션 무변경).

## Implementation Steps

- [ ] `claude-code/skills/ywc-sequential-executor/SKILL.md` line 13 Rationalization Defense 표에 row 1개 추가:
  - Excuse: "concurrency/idempotency Task Verify가 로컬에서 느리거나 만족시키기 어렵다 — lint/typecheck/build 통과로 대신한다"
  - Reality: "Task Verify Layer-1이 이미 merge를 gate한다. 만족시키기 어려운 concurrency 검증은 Layer-4로 격하할 게 아니라 task의 대체 검증 note(code-level lock/transaction proof 또는 integration test plan)로 충족하라."
- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md` line 15 Rationalization Defense 표에 위와 동일 취지의 row 1개 추가 (parallel 4c Task Verify 맥락으로 표현).
- [ ] 두 파일 모두 Step 4/4c 실행 로직·다른 섹션은 변경하지 않는다.
- [ ] executor README가 Rationalization Defense 표를 상세 mirror하는지 확인 — mirror하지 않으면 README 변경 없음(기록).

## Task Verify

- [ ] `rg -n "concurrency|idempoten|lint/typecheck/build|Layer-1|integration test plan" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` — 각 파일에 새 row hit
- [ ] `git diff --stat claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` — 변경이 Rationalization Defense 표 근처로 국한됐는지 확인

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] executor README 변경이 있었다면 markdownlint 0 error; 없었다면 무변경 기록
