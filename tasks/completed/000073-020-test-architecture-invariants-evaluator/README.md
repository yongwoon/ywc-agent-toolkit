# 000073-020-test-architecture-invariants-evaluator

## Purpose
Create executable coverage proving the architecture-invariant contracts, terminal semantics, security boundaries, and zero-process-launch guarantee.

## Scope
Add the standard-library `unittest` fixture runner and focused skill eval cases covering AC1–AC8, including positive, negative, malformed, ambiguous, unsafe, no-manifest, evidence-coverage, and v1 no-execution cases.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-2-amendments--final-readiness-closure` — final fixture and terminal-result requirements
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#verification-plan` — required repository verification commands

### Summary
Tests must exercise the shared helper through deterministic fixtures rather than trusting prose or static shape checks. Every AC requires positive and negative evidence where applicable, and contract data must never cause a child process launch. Consumer packet cases are completed by `000073-030`; this task owns the evaluator and foundational fixture inventory.

### Out of Scope (from spec)
- Consumer implementation and architect adapter — `000073-030`.
- Generated package and isolated install validation — `000074-010`.

## Criticality
normal

## Dependencies

### Depends On
- `000073-010-domain-architecture-invariants-contract` — provides the helper and normative schemas.

### Depended By
- `000073-030-refactor-architecture-consumer-packets` — uses fixture IDs and packet expectations.
- `000074-010-infra-architecture-invariants-distribution` — runs the complete test and eval gates.

## Key Files
- `tests/architecture_invariants_test.py` — stdlib fixture runner.
- `codex/skills/ywc-architecture-invariants/evals/evals.json` — named skill contract cases.

## Notes
- Tests must use process-launch instrumentation and assert zero launches.
- Include literal, `*`, terminal `**`, zero-segment `**`, non-match, digest mismatch, partial coverage, allow/forbid, unsafe path, and unknown executable-field cases.

## Parallel Execution Metadata

### Ownership
- `tests/architecture_invariants_test.py`
- `codex/skills/ywc-architecture-invariants/evals/evals.json`

### Shared Surfaces
- Helper CLI and JSON contracts from `000073-010`.
- Fixture IDs consumed by consumer evals.

### Conflicts With
- `000073-010-domain-architecture-invariants-contract` — fixtures must follow the merged contract.
- `000073-030-refactor-architecture-consumer-packets` — shared eval inventory may need final packet case additions.

### Parallelizable After
- `000073-010-domain-architecture-invariants-contract`

### Task Verify
- `python3 tests/architecture_invariants_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Hardening Evidence
- Test feedback path: this task is the named RED/GREEN fixture path for AC1–AC8.
- Interface contract: fixture assertions bind the helper's closed JSON inputs and audit result outputs.
- Data Integrity Hardening: N/A — no application persistence.
- Critical surface review: verify forbidden executable fields and zero process launches recursively.

## Out of Scope
- Consumer routing changes, run-evidence persistence, generated plugin output, and release metadata.
