# 000012-040-docs-parallel-executor-contract-gates

## Purpose
`ywc-parallel-executor` Codex skill 의 parallel worker contract 를 강화한다. 각 worker 가 task 착수 전 shared surface, public contract, test-first baseline 을 확인하고, wave aggregation 에서 gray-box contract report 를 수집하도록 만든다(FR-4, AC3, AC5, AC6, AC7).

## Scope
- `SKILL.md`의 worker dispatch payload 와 wave execution guidance 에 contract/test-first/deep-module checks 추가
- 병렬 task 간 shared surfaces/ownership 충돌 판단에 public contract 변경 가능성을 반영
- final aggregation report 에 Changed Public Contracts, Critical Internals, TDD Exceptions, per-task tests authored/executed 추가
- eval trigger cases 에 parallel execution 중 worker-level contract gates 를 검증하는 문구 추가
- README locale 파일에 parallel worker contract 요약 갱신

## Spec Reference
### Primary Sources
- `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md` — FR-4, AC3, AC5, AC6, AC7
- `codex/skills/references/tdd-deep-module-gray-box.md` — 000012-010 산출물

### Summary
Parallel executor 는 병렬성/격리 지침은 강하지만 Pocock pitfalls 3/4/5 대응이 약했다. 이 작업은 병렬 worker 에게 test-first contract gate 를 주고, aggregation 단계에서 contract-level evidence 를 모아 최종 보고하게 한다.

### Out of Scope (from spec)
- `ywc-code-gen`, `ywc-sequential-executor` 수정
- Claude Code mirror 수정
- generated plugin package 직접 수정

## Dependencies
### Depends On
- `000012-010-docs-shared-tdd-boundary-contract`

### Depended By
- `000013-010-infra-codex-executor-contract-validation`

## Key Files
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/evals/evals.json`
- `codex/skills/ywc-parallel-executor/README.md`
- `codex/skills/ywc-parallel-executor/README.en.md`
- `codex/skills/ywc-parallel-executor/README.ja.md`
- `codex/skills/ywc-parallel-executor/README.ko.md`
- `codex/skills/ywc-parallel-executor/agents/openai.yaml` (metadata check only)

## Notes
- Worker payload 는 "각자 알아서 테스트"가 아니라 task-level verification evidence 를 명시적으로 반환하도록 한다.
- Parallel scheduling 은 file ownership 만 보지 말고 shared public contract 변경 가능성도 conflict signal 로 취급한다.
- `aggregate-pr` 등 주변 reference 는 꼭 필요한 경우에만 건드린다.

## Out of Scope
- Worktree creation mechanics 변경
- Code generation role prompt 변경
- Task generator metadata schema 변경

## Parallel Execution Metadata
- **Ownership:** `codex/skills/ywc-parallel-executor/**`
- **Shared Surfaces:** parallel executor worker payload contract; parallel scheduling Shared Surfaces semantics; shared TDD/deep-module/gray-box reference; Codex README localization surface
- **Conflicts With:** (None identified after `000012-010` merges)
- **Parallelizable After:** `000012-010-docs-shared-tdd-boundary-contract`
- **Task Verify:**
  - `rg -n "shared contract|Contract|failing test|authored|Critical Internals|tdd-deep-module-gray-box" codex/skills/ywc-parallel-executor`
  - `python3 -m json.tool codex/skills/ywc-parallel-executor/evals/evals.json >/dev/null`
  - `bash scripts/validate.sh`
