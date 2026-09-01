# 000033-030-docs-executor-integrity-gates

## Purpose

Sequential/parallel executor가 task.md에 생성된 concurrency, transaction rollback, idempotency verification을 mandatory Task Verify gate로 취급하도록 보강한다.

## Scope

- `codex/skills/ywc-sequential-executor/SKILL.md` implementation/verification guidance 갱신
- `codex/skills/ywc-parallel-executor/SKILL.md` worker prompt / Task Verify guidance 갱신
- 필요 시 두 executor skill README mirror 갱신

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#fr-5-reinforce-executor-behavior` - executor behavior requirement
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#ac4---executors-honor-generated-checks` - acceptance criteria
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#edge-cases` - no harness and distributed system constraints

### Summary

이 task는 executor가 generated Task Verify 항목을 축소하지 않도록 한다. DB/API write task에서 concurrency, rollback, idempotency check는 lint/typecheck/build로 대체할 수 없는 task-specific gate다. Executor는 프로젝트 harness에 맞게 command를 조정할 수 있지만 검증 의도는 유지해야 한다.

### Out of Scope (from spec)

- Task Verify 항목을 생성하는 `ywc-task-generator` 변경 - `000033-020-docs-spec-task-integrity-guidance`
- `ywc-impl-review` catalog 변경 - `000033-010-docs-impl-review-integrity-catalog`
- generated plugin package 직접 수정 - `000034-010-infra-codex-integrity-validation`

## Dependencies

### Depends On

- `000033-010-docs-impl-review-integrity-catalog` - 공통 defect class와 severity 기준 제공

### Depended By

- `000034-010-infra-codex-integrity-validation` - 최종 sync/validation 대상

## Key Files

- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/README*.md`
- `codex/skills/ywc-parallel-executor/README*.md`

## Notes

- Keep executor guidance operational: "run the generated Task Verify checks" rather than re-teaching the full data integrity concepts.
- Do not add new stop reasons unless existing Task Verify failure handling already covers the case.
- Preserve existing non-stop/range/wave execution contracts.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only executor guidance task. Replacement verification: targeted `rg` and full repository validation in `000034-010`.

### Interface Contract

- Contract: executor Task Verify behavior
- Inputs: task.md with concurrency/rollback/idempotency verification entries
- Outputs: executor runs or adapts those checks before delivery
- Error model: failed Task Verify blocks merge/delivery according to each executor's existing failure handling
- Impacted tests: repository validation and targeted text evidence

### Critical Surface Review

- Review requirement: manual full implementation review or `ywc-impl-review`, because this affects merge gates for data integrity tasks.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`

### Shared Surfaces

- Executor Task Verify semantics
- README locale mirror sets for sequential and parallel executor

### Conflicts With

- Any task editing `codex/skills/ywc-sequential-executor/**`
- Any task editing `codex/skills/ywc-parallel-executor/**`

### Parallelizable After

- `000033-010-docs-impl-review-integrity-catalog`

### Task Verify

- `rg -n "concurrency|concurrent|rollback|idempotency|Task Verify" codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
- `bash scripts/install.sh --list --codex`

## Out of Scope

- Do not edit task-generator in this task.
- Do not edit generated plugin files directly.
- Do not change branch, PR, CI, or worktree lifecycle behavior.
