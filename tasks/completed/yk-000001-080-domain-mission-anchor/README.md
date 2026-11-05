# yk-000001-080-domain-mission-anchor

## Purpose
Durable mission anchor implements FR-7 and AC-7 of the approved Codex adoption specification.

## Scope
- Port full frozen #348 mission skill and mission-format reference, Tier 1 locales, metadata and evals.
- Support read/update/curate at docs/mission.md; read absence yields empty anchor. Read whole file and present exact ADD/MODIFY/DEPRECATE CHANGESET before confirmed nonempty writes.
- Keep one active mission, observable SC+rationale, RA reason, stable IDs/provenance/history and optional NG reason/CN rationale; anchors include active entries only. Empty/dry-run changes do not write or update dates; preserve deprecated history and offer steering activation guidance only.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-7, AC-7, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers read/update/curate mission with stable NG/CN history. It owns the FR-7 / AC-7 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-7 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
critical — Sensitive command, permission, durable-write or cross-caller gate contracts require full review.

## Dependencies
### Depends On
- (None)

### Depended By
- yk-000001-090-domain-infra-evidence
- yk-000002-010-infra-distribution

## Key Files
- `codex/skills/ywc-mission/`
- `tests/fixtures/codex-issue69/upstream-adoption/mission-anchor.json`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-7. Boundary: read/update/curate mission with stable NG/CN history. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

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
- `codex/skills/ywc-mission/`
- `tests/fixtures/codex-issue69/upstream-adoption/mission-anchor.json`

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
