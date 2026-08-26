# 000054-010-test-skill-audit-validation

## Purpose

새 audit contract와 `ywc-agentic` activation boundary를 검증하고, audit evidence로 후속 pruning pilot 후보 하나를 추천한다.

## Scope

- 양 script의 정상/오류/report behavior, byte parity, skill structure, repository validator를 실행한다.
- near-500-line 후보 중 후속 deletion-test pilot 하나를 추천한다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/skill-engineering-hardening.md#fr-6-validate-and-selectnot-executea-pruning-pilot`
- `docs/ywc-plans/skill-engineering-hardening.md#iteration-1-amendments`
- `docs/ywc-plans/skill-engineering-hardening.md#validation-plan`

### Summary

Phase 000053의 두 변경이 merge된 뒤 수행하는 read-only close-out gate다. audit finding은 advisory이며 이 task는 long skill을 편집하거나 pruning을 실행하지 않고, terminal/PR evidence로 candidate와 근거만 보고한다.

### Out of Scope (from spec)

- `ywc-skill-author`/`ywc-agentic` 추가 수정
- `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-gen-testcase`, `ywc-task-generator` pruning 구현
- root CI policy/plugin 수동 편집

## Dependencies

### Depends On

- `000053-010-refactor-skill-author-audit-workflow` — audit script/rubric 제공
- `000053-020-refactor-agentic-autonomy-trigger` — narrowed trigger 제공

### Depended By

- (None — pilot은 새 승인 task로만 실행한다.)

## Key Files

- No production bundle file is expected to change.
- `tasks/000054-010-test-skill-audit-validation/**` — task evidence source.

## Notes

- Valid audit은 findings가 있어도 exit 0, invalid input은 exit 2.
- pilot 선정은 line count만이 아니라 report evidence와 safe representative deletion test를 근거로 한다.

## Hardening Evidence

### Test Feedback Path

- RED-first target: invalid root invocation must return exit 2.
- Existing coverage: added Codex eval fixture and skill-local validators.

### Interface Contract

- Inputs: bundle roots and representative user requests.
- Outputs: stable advisory report and correct activation boundary.
- Error model: invalid audit input returns 2; a finding is non-failing.
- Impacted tests: targeted shell commands and `bash scripts/validate.sh`.

### Critical Surface Review

- Review requirement: verify no finding becomes automatic deletion authorization.

### Data Integrity Hardening

- Trigger surface: N/A.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- Read-only `claude-code/skills/**`, `codex/skills/**`; task directory only for bookkeeping.

### Shared Surfaces

- `bash scripts/validate.sh`, paired bundle contracts

### Conflicts With

- (None identified after Phase 000053 merge.)

### Parallelizable After

- `000053-010-refactor-skill-author-audit-workflow`
- `000053-020-refactor-agentic-autonomy-trigger`

### Task Verify

- two directional audit commands
- `cmp -s` paired scripts
- `bash scripts/validate.sh`

## Out of Scope

- production bundle edits and selected-pilot implementation
