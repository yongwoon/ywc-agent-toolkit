# yw-000033-030-domain-review-quality-evidence

## Purpose
Teach implementation review to consume only sanitized quality-gate evidence and report missing or residual evidence conservatively.

## Scope
Update `ywc-impl-review` QA/reference/report rules and evals for contract state, approved command identity/digest, artifact path, unavailable tools, residual survivors, and confidence downgrade without gate execution.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260910-codex-quality-gate-contract.md#fr-6-review-and-evaluation-coverage`
- `codex/skills/references/quality-gates.md`
- `codex/skills/ywc-impl-review/references/qa-agent.md`
### Summary
Review receives only the sanitized boundary from executor output. It must not execute a gate, infer missing evidence, or accept raw commands, output, secrets, transcripts, or full diffs. Missing required evidence lowers confidence or returns the appropriate non-pass status.
### Out of Scope (from spec)
- Gate dispatch and worker behavior — `yw-000033-010` and `yw-000033-020`.
- Final package sync and validation — `yw-000034-010`.

## Criticality
critical

## Dependencies
### Depends On
- `yw-000032-010-domain-plan-scaffold-quality-declaration`
- `yw-000032-020-domain-task-quality-gate-packet`
- `yw-000032-030-infra-quality-gate-workers`
### Depended By
- `yw-000034-010-infra-quality-gate-distribution-validation`

## Key Files
- `codex/skills/ywc-impl-review/SKILL.md`
- `codex/skills/ywc-impl-review/references/qa-agent.md`
- `codex/skills/ywc-impl-review/evals/evals.json`

## Notes
Follow the existing architecture-packet redaction and evidence-quality conventions; do not duplicate the canonical contract.

## Hardening Evidence
### Test Feedback Path
- RED-first target: implementation-review evals for valid boundary, missing evidence, raw-command rejection, and residual survivors.
### Interface Contract
- Contract: sanitized executor evidence → review confidence/report
- Owner task: this task
- Canonical signature: sanitized state/evidence/residuals → review finding or downgraded confidence
- Consumers: final validation and completion reporting
- Implementation opacity: reviewer never inspects raw worker internals.
- Mismatch action: `NEEDS_CONTEXT`
### Critical Surface Review
- Review requirement: manual full implementation review plus `ywc-impl-review`.
### Data Integrity Hardening
- Trigger surface: N/A — read-only evidence consumption.
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-impl-review/**`
### Shared Surfaces
- Sanitized completion evidence.
- `codex/skills/references/quality-gates.md`.
### Conflicts With
- (None identified)
### Parallelizable After
- All Phase `yw-000032` tasks.
### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `rg -n "quality gate|sanitized|approved.*digest|residual|NEEDS_CONTEXT|raw command|full diff" codex/skills/ywc-impl-review`

## Out of Scope
Executing quality gates, changing worker boundaries, and modifying executor lifecycle.
