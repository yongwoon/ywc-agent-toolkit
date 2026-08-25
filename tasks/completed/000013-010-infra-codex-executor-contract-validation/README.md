# 000013-010-infra-codex-executor-contract-validation

## Purpose
Batch 4의 Codex executor skill 개선이 모두 병합된 뒤 repository validation, install scan, generated plugin sync 상태를 확인하는 hard gate 를 수행한다(FR-6, AC8, AC9).

## Scope
- `bash scripts/install.sh --list --codex`로 Codex skill scan 확인
- `bash scripts/validate.sh`로 repository structure validation 확인
- 필요한 경우 source-of-truth 인 `codex/skills/**`에서 generated package 로 sync 수행
- 변경 범위가 Codex-only 원칙을 지키는지 확인

## Spec Reference
### Primary Sources
- `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md` — FR-6, AC8, AC9
- Batch 4 tasks `000012-010`, `000012-020`, `000012-030`, `000012-040`

### Summary
이 task 는 구현 task 가 아니라 integration gate 이다. 모든 Phase 000012 작업이 병합된 뒤 실행하며, generated plugin artifact 가 stale 이면 sync script 로 갱신한다. Source skill 수정은 선행 task 소관으로 되돌린다.

### Out of Scope (from spec)
- 새로운 skill 지침 작성
- Claude Code mirror 수정
- unrelated cleanup

## Dependencies
### Depends On
- `000012-010-docs-shared-tdd-boundary-contract`
- `000012-020-docs-code-gen-contract-first`
- `000012-030-docs-sequential-executor-test-first`
- `000012-040-docs-parallel-executor-contract-gates`

### Depended By
- (없음) — Batch 4 final gate

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` (generated sync output only, if script modifies it)
- `codex/skills/**` (read-only inspection unless validation failure identifies a missed owning-task fix)

## Notes
- `plugins/ywc-agent-toolkit/skills/**`는 source of truth 가 아니므로 hand-edit 하지 않는다.
- Validation failure 가 source skill 내용 문제라면 해당 owning task 로 돌려보내고 이 gate 에서 직접 광범위 수정하지 않는다.

## Out of Scope
- Phase 000012 task 의 미완성 scope 보정
- eval rubric 대규모 재설계

## Parallel Execution Metadata
- **Ownership:** `plugins/ywc-agent-toolkit/skills/**` generated sync output only; repository validation workflow
- **Shared Surfaces:** Codex plugin generated package; install/validation CI surface
- **Conflicts With:** `000012-010`, `000012-020`, `000012-030`, `000012-040` until all are merged
- **Parallelizable After:** all Phase 000012 tasks complete
- **Task Verify:**
  - `bash scripts/install.sh --list --codex`
  - `bash scripts/sync-codex-plugin.sh` if generated plugin output is stale or repository convention requires sync
  - `bash scripts/validate.sh`
  - `git diff --name-only | rg '^claude-code/'` returns no results
