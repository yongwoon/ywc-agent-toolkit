# yw-000055-010-domain-executable-fallback-migration

## Purpose

Replace every Codex target-relative executable fallback and direct test-script execution with the trusted resolver contract.

## Scope

Migrate the 20-site closed inventory across ten Codex skill/script surfaces plus `ywc-task-generator`, preserving existing arguments, interpreter invocation, pipeline behavior, and fail-closed handling.

## Spec Reference

### Primary Sources

- [Executable-resolution hardening spec](../../../docs/ywc-plans/20260919-codex-executable-resolution-hardening.md#fr-2-migrate-the-full-current-codex-fallback-inventory)
- [Shared resolution contract](../../../codex/skills/references/shared-script-resolution.md)

### Summary

Each caller must resolve an absolute trusted executable before invocation. The migration covers all listed skill instructions and `mark-complete.sh`; interpreter-invoked non-executable files remain valid. `mark-complete.sh` must resolve its compactor before any directory, staging, or commit mutation.

### Out of Scope (from spec)

- Resolver implementation is owned by `yw-000054-010-infra-bundle-executable-resolver`.
- Regression harness, complement validation, and agent evaluation wiring are owned by `yw-000056-010-test-executable-resolution-regression`.
- Plugin synchronization is owned by `yw-000057-010-infra-executable-resolution-distribution`.
- Claude skills, agents, and new runtime dependencies are excluded.

## Criticality

critical

## Dependencies

### Depends On

- `yw-000054-010-infra-bundle-executable-resolver` — provides the launcher block and canonical resolver contract.

### Depended By

- `yw-000056-010-test-executable-resolution-regression` — tests the migrated inventory and closure behavior.

## Key Files

- `codex/skills/scripts/mark-complete.sh`
- `codex/skills/ywc-code-gen/SKILL.md`
- `codex/skills/ywc-create-pr/SKILL.md`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-handle-pr-reviews/SKILL.md`
- `codex/skills/ywc-onboard-repo/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-release-pr-list/SKILL.md`
- `codex/skills/ywc-skill-author/SKILL.md`
- `codex/skills/ywc-spec-writer/SKILL.md`
- `codex/skills/ywc-task-generator/SKILL.md`

## Notes

Use the exact shared bootstrap block; do not create per-caller trust logic or target-relative alternatives.

## Hardening Evidence

- Test feedback path: downstream closed-set complement and hostile-target tests.
- Interface Contract: every caller consumes the resolver's absolute path output and fixed invocation kind without changing arguments.
- Data Integrity trigger: `mark-complete.sh` mutation ordering; strategy is resolve-before-mkdir/move/stage/commit, transaction is shell sequencing, idempotency is no mutation on `BLOCKED`, required test is the unresolved-compactor regression.
- Critical surface review: required for every migrated invocation and pipeline.

## Out of Scope

Resolver internals, validation harness implementation, and generated bundle synchronization.

## Parallel Execution Metadata

- **Ownership:** The eleven listed Codex source files and their executable-selection clauses
- **Shared Surfaces:** Exact launcher-selection block; resolver CLI; existing argument and exit-result semantics
- **Conflicts With:** Any task editing the listed Codex callers
- **Parallelizable After:** `yw-000054-010`
- **Task Verify:** Complement search shows no unsafe target-relative executable command or assignment; targeted migrated caller checks pass

