# 000012-030-docs-sequential-executor-test-first

## Purpose
`ywc-sequential-executor` Codex skill 이 task 실행 중 behavior-changing work 를 test-first 로 처리하고, deep-module/gray-box 관점의 contract reporting 을 남기도록 강화한다(FR-3, AC3, AC4, AC6, AC7).

## Scope
- `SKILL.md` 실행 루프에 failing test baseline 과 contract/deep-module check 추가
- Verification 및 final report 에 Changed Public Contracts, Critical Internals, TDD exception 항목 반영
- eval trigger cases 에 sequential execution 중 test-first/deep-module reporting 기대치를 추가 또는 갱신
- README locale 파일에 executor 동작 요약 갱신

## Spec Reference
### Primary Sources
- `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md` — FR-3, AC3, AC4, AC6, AC7
- `codex/skills/references/tdd-deep-module-gray-box.md` — 000012-010 산출물

### Summary
Sequential executor 는 이미 task 단위 검증 흐름이 강하지만 TDD 가 선호 수준에 머물러 있다. 이 작업은 behavior-changing task 의 시작 조건을 failing test 또는 existing failing assertion 확인으로 끌어올리고, 예외가 필요할 때 final report 에 이유를 남기게 한다.

### Out of Scope (from spec)
- `ywc-code-gen`, `ywc-parallel-executor` 수정
- Claude Code mirror 수정
- generated plugin package 직접 수정

## Dependencies
### Depends On
- `000012-010-docs-shared-tdd-boundary-contract`

### Depended By
- `000013-010-infra-codex-executor-contract-validation`

## Key Files
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/evals/evals.json`
- `codex/skills/ywc-sequential-executor/README.md`
- `codex/skills/ywc-sequential-executor/README.en.md`
- `codex/skills/ywc-sequential-executor/README.ja.md`
- `codex/skills/ywc-sequential-executor/README.ko.md`
- `codex/skills/ywc-sequential-executor/agents/openai.yaml` (metadata check only)

## Notes
- Sequential executor 는 user task files 를 실행하는 skill 이므로 "모든 task 에 새 테스트 작성"이 아니라 behavior-changing implementation task 에 test-first baseline 을 요구한다.
- docs-only, mechanical rename, no practical harness 등의 예외는 허용하되 final report 에 명시해야 한다.

## Out of Scope
- parallel scheduling semantics 변경
- code-gen worker prompt 변경
- task generator 규칙 변경

## Parallel Execution Metadata
- **Ownership:** `codex/skills/ywc-sequential-executor/**`
- **Shared Surfaces:** sequential executor implementation-step contract; shared TDD/deep-module/gray-box reference; Codex README localization surface
- **Conflicts With:** (None identified after `000012-010` merges)
- **Parallelizable After:** `000012-010-docs-shared-tdd-boundary-contract`
- **Task Verify:**
  - `rg -n "failing test|contract test|Changed Public Contracts|Critical Internals|tdd-deep-module-gray-box" codex/skills/ywc-sequential-executor`
  - `python3 -m json.tool codex/skills/ywc-sequential-executor/evals/evals.json >/dev/null`
  - `bash scripts/validate.sh`
