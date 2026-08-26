# yw-000001-010-config-initials-writer

## Purpose
Persist validated collaborator initials in the existing Codex configuration without losing language settings or concurrent updates.

## Scope
Extend `ywc-setup` with `--initials`, atomic read-modify-write behavior, validation, documentation, and focused config fixtures.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#acceptance-criteria` — configuration and concurrency requirements
- `docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md#fr-1-resolve-and-persist-collaborator-initials` — CLI and persistence contract

### Summary
The existing `.codex/ywc.json` config must accept an optional lowercase alphanumeric `initials` value alongside `lang`. Setup writes must preserve existing and unknown keys, use a unique temporary file, serialize the complete operation, and validate the final JSON. The implementation is project/user scoped and must not introduce session configuration.

### Out of Scope (from spec)
- Task-generator resolution and PHASE allocation — handled by `yw-000002-010-task-generator-initials-allocation`.
- Claude Code configuration and `.ywc-config.json` — excluded by the spec.

## Criticality
critical

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000002-010-task-generator-initials-allocation` — consumes the persisted initials contract.

## Key Files
- `codex/skills/ywc-setup/SKILL.md`
- `codex/skills/ywc-setup/scripts/write-config.sh`
- `codex/skills/ywc-setup/evals/evals.json`
- `codex/skills/ywc-setup/README*.md`

## Notes
Keep config resolution compatible with malformed-tier fallback. Validate exactly `^[a-z0-9]{2,4}$`; do not normalize uppercase input.

## Hardening Evidence
### Test Feedback Path
- RED-first target: config smoke/concurrency fixtures for `write-config.sh`.

### Interface Contract
- Contract: `ywc-setup --scope <project|user> [--lang <value>] [--initials <value>]`
- Outputs: valid JSON retaining independent requested fields and unknown keys.
- Error model: usage error for missing operands or invalid initials; no partial file.
- Impacted tests: setup evals and focused shell/Python smoke checks.

### Critical Surface Review
- Review requirement: `ywc-impl-review` for atomic replacement and concurrent update behavior.

### Data Integrity Hardening
- Trigger surface: shared mutable state; duplicate-sensitive config update.
- Atomic / locking strategy: exclusive `fcntl.flock`, unique same-directory temporary file, fsync, atomic replace.
- Transaction boundary: complete JSON read/merge/flush/replace operation.
- Idempotency guard: last-write-preserving read-modify-write under the lock.
- Required tests: concurrent `lang`/`initials` updates, malformed input, missing operand, final JSON validation.

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-setup/**`
- `.codex/ywc.json` config contract

### Shared Surfaces
- `.codex/ywc.json`
- Setup CLI option contract

### Conflicts With
- `yw-000002-010-task-generator-initials-allocation` — consumes or documents config resolution.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `bash -n codex/skills/ywc-setup/scripts/*.sh`
- `python3 -m json.tool .codex/ywc.json >/dev/null`
- Run the focused setup config/concurrency fixtures added by this task.

## Out of Scope
- Task ID naming, PHASE scanning, Git reservation refs, and executor compatibility.
