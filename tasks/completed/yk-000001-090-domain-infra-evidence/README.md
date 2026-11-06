# yk-000001-090-domain-infra-evidence

## Purpose
Applied scope and bounded FinOps implements FR-8 and AC-8 of the approved Codex adoption specification.

## Scope
- Accept one-time evidence_type state_backend|apply_record|applied_commit, exact binding_target and applied yes/no without provider queries or extra required revision fields.
- Scoped-only missing/unbound/unapplied returns BLOCKED with no reviewers; valid binding with missing/truncated content returns NEEDS_CONTEXT.
- For mixed input send identical eligible sets to all three lenses; exclude only ineligible scoped sets, never use them as fallback. Missing fresh or eligible content returns NEEDS_CONTEXT; preserve fresh-only/topology-only N/A headers and topology packets.
- Update performance agent to return bounded cost/risk alternatives inline; missing evidence returns NEEDS_CONTEXT; aggregator owns report files.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-8, AC-8, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers eligible applied scope and bounded inline FinOps evidence. It owns the FR-8 / AC-8 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-8 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
critical — Sensitive command, permission, durable-write or cross-caller gate contracts require full review.

## Dependencies
### Depends On
- yk-000001-080-domain-mission-anchor

### Depended By
- yk-000002-010-infra-distribution

## Key Files
- `codex/agents/README.md`
- `codex/skills/ywc-infra-review/`
- `codex/agents/ywc-performance-engineer.toml`
- `codex/agents/evals/evals.json`
- `tests/fixtures/codex-issue69/upstream-adoption/infra-evidence.json`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-8. Boundary: eligible applied scope and bounded inline FinOps evidence. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

### Critical Surface Review
Require ywc-impl-review or full manual implementation review before DONE.
### Data Integrity Hardening
- Trigger surface: permission, retryable commands or durable writes described by this task; apply codex/skills/references/data-integrity-hardening.md where triggered.
- Atomic / locking strategy: preserve existing guards; document all-or-nothing boundaries before changing write instructions.
- Transaction boundary: task-specific operation; no partial-success claim after required-command failure.
- Idempotency guard: refuse duplicate/unsafe side effects; N/A for pure source assertions.
- Required tests: refusal, failure injection and duplicate/retry paths for triggered operations; N/A for pure documentation.

## Parallel Execution Metadata
- Model Hint: `advanced` — Sensitive state and cross-skill reasoning.
### Ownership
- `codex/agents/README.md`
- `codex/skills/ywc-infra-review/`
- `codex/agents/ywc-performance-engineer.toml`
- `codex/agents/evals/evals.json`
- `tests/fixtures/codex-issue69/upstream-adoption/infra-evidence.json`

### Shared Surfaces
- `codex/agents/README.md`
- `codex/agents/evals/evals.json`

### Conflicts With
- yk-000001-020-domain-analyst-modes
- yk-000002-010-infra-distribution

### Parallelizable After
- yk-000001-080-domain-mission-anchor

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
