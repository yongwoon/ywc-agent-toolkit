# 000034-010-infra-codex-integrity-validation

## Purpose

Codex data integrity skill hardening batch의 source edits, README mirrors, generated plugin sync, repository validation을 최종 hard gate로 검증한다.

## Scope

- Phase `000033`의 모든 Codex source 변경 결과 검토
- 필요 시 `bash scripts/sync-codex-plugin.sh` 실행
- `bash scripts/validate.sh` 실행 및 실패 원인 정리
- targeted `rg`로 spec의 핵심 용어가 intended skill surfaces에 반영됐는지 확인

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#ac5---no-scope-leak-into-generated-package` - generated package boundary
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#ac6---repository-validation-passes` - validation requirement
- `docs/ywc-plans/codex-data-integrity-skill-hardening.md#implementation-plan` - final validation and sync steps

### Summary

이 task는 source guidance task들이 모두 완료된 뒤 실행하는 hard gate다. Codex source files를 기준으로 generated plugin package를 동기화하고, repository validation을 통과시킨다. 검증 실패가 기존 stale package 또는 cache artifact 때문인지, 이번 batch 변경 때문인지 구분해서 보고한다.

### Out of Scope (from spec)

- Source guidance 작성 - `000033-010`, `000033-020`, `000033-030`
- Claude Code skill 변경 - spec Out of Scope
- 실제 application code 변경 - spec Out of Scope

## Dependencies

### Depends On

- `000033-010-docs-impl-review-integrity-catalog` - impl-review catalog and summary complete
- `000033-020-docs-spec-task-integrity-guidance` - spec/task generator guidance complete
- `000033-030-docs-executor-integrity-gates` - executor gate guidance complete

### Depended By

- (None - final hard gate)

## Key Files

- `codex/skills/ywc-impl-review/**`
- `codex/skills/ywc-spec-validate/**`
- `codex/skills/ywc-task-generator/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `plugins/ywc-agent-toolkit/skills/**` - generated output only if sync is required
- `scripts/sync-codex-plugin.sh`
- `scripts/validate.sh`

## Notes

- Do not manually edit generated plugin package files.
- If validation fails because of pre-existing `__pycache__` drift, report it separately and do not hide source validation status.
- If README mirrors were updated in source, confirm generated package mirrors them after sync.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/validate.sh`
- Existing coverage: `bash scripts/install.sh --list --codex`
- Existing coverage: targeted `rg` command from the spec

### Interface Contract

- Contract: Codex skill bundle package consistency
- Inputs: changed `codex/skills/**` source files
- Outputs: synced generated plugin package and passing validation
- Error model: validation failure blocks DONE and must be reported with exact failing check
- Impacted tests: repository validation scripts

### Critical Surface Review

- Review requirement: manual full implementation review of final diff, because skill behavior changes affect future review quality.

## Parallel Execution Metadata

### Ownership

- `plugins/ywc-agent-toolkit/skills/**` generated sync output
- validation command outputs only; source skill files may be touched only for validation fixes that are directly caused by Phase `000033`

### Shared Surfaces

- Codex generated plugin package
- Repository validation status

### Conflicts With

- Any task still editing `codex/skills/ywc-impl-review/**`
- Any task still editing `codex/skills/ywc-spec-validate/**`
- Any task still editing `codex/skills/ywc-task-generator/**`
- Any task still editing `codex/skills/ywc-sequential-executor/**`
- Any task still editing `codex/skills/ywc-parallel-executor/**`

### Parallelizable After

- `000033-010-docs-impl-review-integrity-catalog`
- `000033-020-docs-spec-task-integrity-guidance`
- `000033-030-docs-executor-integrity-gates`

### Task Verify

- `rg -n "race condition|concurrent write|partial write|transaction boundary|idempotency" codex/skills/ywc-impl-review codex/skills/ywc-spec-validate codex/skills/ywc-task-generator codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
- `bash scripts/install.sh --list --codex`
- `bash scripts/validate.sh`

## Out of Scope

- Do not change Claude Code skills.
- Do not add new validation scripts.
- Do not edit ignored local cache artifacts except when explicitly cleaning generated package drift is required.
