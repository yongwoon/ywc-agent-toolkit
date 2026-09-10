# yw-000032-020-domain-task-quality-gate-packet

## Purpose
Propagate a valid quality-gate declaration into generated task metadata without exposing executable command text or placeholders.

## Scope
Update `ywc-task-generator` guidance, README/task templates, references, and evals with a conditional Quality Gate Contract/Owned Interface section bound to exact Ownership, approved IDs/digests, thresholds, attempt cap, and sanitized evidence paths.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-2-task-owned-interface-propagation`
- `codex/skills/references/quality-gates.md`
- `codex/skills/ywc-task-generator/references/task-metadata-rules.md`
### Summary
Generated tasks include the quality packet only when a valid declaration is present. The packet is bounded worker input and must omit raw commands, transcript, full diff, or invented placeholders. No contract means the conditional section is omitted entirely.
### Out of Scope (from spec)
- Producer declaration — `yw-000032-010-domain-plan-scaffold-quality-declaration`.
- Worker, executor, reviewer, and release changes — later tasks.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000031-010-docs-quality-gate-contract` — canonical packet semantics.
- `yw-000032-010-domain-plan-scaffold-quality-declaration` — producer declaration shape.
### Depended By
- `yw-000033-010-domain-sequential-quality-gate` — consumes per-task packet.
- `yw-000033-020-domain-parallel-quality-gate` — consumes per-task packet.

## Key Files
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/README.md.template`
- `codex/skills/ywc-task-generator/references/task.md.template`
- `codex/skills/ywc-task-generator/references/task-metadata-rules.md`
- `codex/skills/ywc-task-generator/evals/evals.json`

## Notes
Reuse the existing conditional architecture-packet pattern; do not create a second contract verifier.

## Hardening Evidence
### Test Feedback Path
- RED-first target: `codex/skills/ywc-task-generator/evals/evals.json` cases for valid, absent, incomplete, and raw-command rejection.
### Interface Contract
- Contract: task metadata → executor gate packet
- Owner task: this task
- Canonical signature: valid declaration + task Ownership → sanitized per-task packet
- Consumers: sequential and parallel executor tasks
- Implementation opacity: executors use only the packet fields and do not inspect generator internals.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: `ywc-impl-review` via final validation.
### Data Integrity Hardening
- Trigger surface: N/A
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-task-generator/**`
### Shared Surfaces
- `codex/skills/references/quality-gates.md` — read-only.
- Generated task metadata templates — consumed by executors.
### Conflicts With
- (None identified)
### Parallelizable After
- `yw-000031-010-docs-quality-gate-contract`
- `yw-000032-010-domain-plan-scaffold-quality-declaration`
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `rg -n "Quality Gate Contract|approved.*digest|sanitized.*evidence|raw command|N/A — no quality gate contract" codex/skills/ywc-task-generator`

## Out of Scope
Implementing dispatch, worker behavior, executor aggregation, or review consumption.
