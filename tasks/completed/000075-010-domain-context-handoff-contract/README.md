# 000075-010-domain-context-handoff-contract

## Purpose
Define the closed, privacy-safe context handoff wire contract used to reconstruct executor state without becoming a new authority.

## Scope
Add the shared handoff reference covering schema, locations, validation, stale-file recovery, privacy rejection, and atomic replacement.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-5-context-handoff-wire-contract`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#d-context-handoff-schema-location-and-privacy-boundary`
### Summary
The handoff is a local reconstruction cache beside authoritative run state. It has a closed schema, bounded fields, checkpoint identity matching, and atomic replacement semantics. Readers fall back to checkpoint state and current task sources when the handoff is missing, malformed, stale, or mismatched.
### Out of Scope (from spec)
- Executor integration — handled by `000076-030-domain-sequential-transition-safety` and `000076-040-domain-parallel-transition-safety`.
- Changing checkpoint, task metadata, or worktree data models.

## Criticality
critical

## Dependencies
### Depends On
- (None — root task)
### Depended By
- `000076-010-domain-producer-result-artifact-profile` — uses the shared privacy and artifact-path conventions.
- `000076-030-domain-sequential-transition-safety` — implements sequential handoff lifecycle.
- `000076-040-domain-parallel-transition-safety` — implements aggregate parallel handoff lifecycle.

## Key Files
- `codex/skills/references/context-handoff.md` — new canonical wire contract.

## Notes
The contract must not introduce cleanup or completion authority. Paths are repository-relative, schema version is literal `1`, and raw response/tool-output fields are forbidden.

## Hardening Evidence
### Test Feedback Path
- RED-first target: handoff fixture cases for malformed, stale, mismatched, privacy-violating, and atomic-write-failure inputs.
### Interface Contract
- Contract: `.ywc-context-handoff.json`.
- Inputs: closed JSON object with required fields and documented nested keys.
- Outputs: validated handoff or discard-and-reconstruct decision.
- Error model: bounded field/rule diagnostic without raw content.
- Impacted tests: focused handoff evaluation fixtures.
### Critical Surface Review
- Review requirement: `ywc-impl-review` or manual full implementation review.
### Data Integrity Hardening
- Trigger surface: duplicate-sensitive side effect / atomic state replacement.
- Atomic / locking strategy: same-directory temporary sibling, fsync, rename, parent-directory fsync where supported.
- Transaction boundary: handoff replacement only; checkpoint state remains unchanged on failure.
- Idempotency guard: preserve prior valid destination when replacement fails.
- Required tests: failure injection and malformed/stale/mismatched recovery.

## Parallel Execution Metadata
### Ownership
- `codex/skills/references/context-handoff.md`
### Shared Surfaces
- Checkpoint identity and run-state locations.
- Artifact path and privacy rules.
### Conflicts With
- (None identified)
### Parallelizable After
- (Root task — no predecessor required)
### Task Verify
- `test -f codex/skills/references/context-handoff.md`
- `bash scripts/validate.sh`

## Out of Scope
- Runtime code changes in executor skills.
- Changes to `.ywc-run-state.json`, task metadata, or worktree lifecycle.
