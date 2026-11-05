# yk-000001-030-domain-authoring-feedback

## Purpose
Authoring feedback loops implements FR-3 and AC-3 of the approved Codex adoption specification.

## Scope
- Inspect repository facts before asking one unresolved prerequisite question; retain approval gates.
- Record public-seam catches/misses and finish one behavior RED/GREEN/REFACTOR cycle before another; do not expose private helpers.
- Add Writing Levers: remove no-ops, positive goals, conditions first, observable completion, canonical references.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-3, AC-3, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers repository-first questions, behavior TDD and Writing Levers. It owns the FR-3 / AC-3 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-3 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
normal — Bounded instruction and evaluation changes using existing patterns.

## Dependencies
### Depends On
- yk-000001-020-domain-analyst-modes

### Depended By
- yk-000001-040-domain-session-retro
- yk-000001-110-domain-convergence-callers
- yk-000002-010-infra-distribution

## Key Files
- `codex/skills/ywc-brainstorm/`
- `codex/skills/ywc-tdd-ritual/`
- `codex/skills/ywc-skill-author/`
- `tests/fixtures/codex-issue69/upstream-adoption/authoring-feedback.json`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-3. Boundary: repository-first questions, behavior TDD and Writing Levers. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

### Critical Surface Review
N/A — instruction/evaluation work; escalate if a sensitive runtime surface is introduced.
### Data Integrity Hardening
- Trigger surface: N/A — instruction/evaluation only.
- Atomic / locking strategy: preserve existing guards; document all-or-nothing boundaries before changing write instructions.
- Transaction boundary: task-specific operation; no partial-success claim after required-command failure.
- Idempotency guard: refuse duplicate/unsafe side effects; N/A for pure source assertions.
- Required tests: refusal, failure injection and duplicate/retry paths for triggered operations; N/A for pure documentation.

## Parallel Execution Metadata
- Model Hint: `standard` — Existing-pattern instruction and fixture changes.
### Ownership
- `codex/skills/ywc-brainstorm/`
- `codex/skills/ywc-tdd-ritual/`
- `codex/skills/ywc-skill-author/`
- `tests/fixtures/codex-issue69/upstream-adoption/authoring-feedback.json`

### Shared Surfaces
- `codex/skills/ywc-skill-author/`

### Conflicts With
- yk-000001-110-domain-convergence-callers

### Parallelizable After
- yk-000001-020-domain-analyst-modes

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
