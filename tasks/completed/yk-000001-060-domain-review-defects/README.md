# yk-000001-060-domain-review-defects

## Purpose
Review defects and targeted linters implements FR-5 and AC-5 of the approved Codex adoption specification.

## Scope
- Add A-005 checkout credentials, A-006 unawaited/boolean Promise, A-007 discarded errors with provenance and severity rationale; preserve existing catalog.
- Use only installed stack-appropriate changed-file linters: ruff S110/BLE001/B904, zizmor artipacked/unpinned-uses, TypeScript Promise rules and Go errcheck; report unavailable tools.
- Require verify-before-surface for every linter hit; do not install tools or change lint configuration.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-5, AC-5, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers A-005–007 and installed targeted-linter evidence. It owns the FR-5 / AC-5 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-5 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
normal — Bounded instruction and evaluation changes using existing patterns.

## Dependencies
### Depends On
- (None)

### Depended By
- yk-000001-070-domain-operational-safety
- yk-000002-010-infra-distribution

## Key Files
- `codex/skills/ywc-impl-review/`
- `tests/fixtures/codex-issue69/upstream-adoption/review-defects.json`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-5. Boundary: A-005–007 and installed targeted-linter evidence. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

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
- `codex/skills/ywc-impl-review/`
- `tests/fixtures/codex-issue69/upstream-adoption/review-defects.json`

### Shared Surfaces


### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
