# yk-000002-010-infra-distribution

## Purpose
Bundle distribution integration implements FR-10 and AC-10 of the approved Codex adoption specification.

## Scope
- Update repository skill catalogs, agent documentation, locales and actual counts for the completed source bundle; regenerate plugin from source.
- Verify unique numeric skill eval IDs with source_id provenance and nonempty agent expectations. Run contract, behavior, installation and validation gates.
- Test selected new skills and agent-only installs with temporary CODEX_HOME; distinguish source assertions, expected traces, extracted runnable recipes, existing helper execution and live evidence. Record unavailable live execution as UNVERIFIED.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-10, AC-10, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers catalog counts/locales, generated plugin and temporary installs. It owns the FR-10 / AC-10 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-10 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
normal — Bounded instruction and evaluation changes using existing patterns.

## Dependencies
### Depends On
- yk-000001-010-domain-model-hints
- yk-000001-020-domain-analyst-modes
- yk-000001-030-domain-authoring-feedback
- yk-000001-040-domain-session-retro
- yk-000001-050-domain-session-handoff
- yk-000001-060-domain-review-defects
- yk-000001-070-domain-operational-safety
- yk-000001-080-domain-mission-anchor
- yk-000001-090-domain-infra-evidence
- yk-000001-100-domain-pr-worktrees
- yk-000001-110-domain-convergence-callers
- yk-000001-120-domain-pr-body

### Depended By
- (None)

## Key Files
- `README.es.md`, `README.ja.md`, `README.ko.md`, `README.md`, `README.zh.md`
- `codex/README.md`
- `codex/agents/README.md`
- `plugins/ywc-agent-toolkit/`
- `tests/fixtures/codex-issue69/upstream-adoption/distribution.json`
- `tests/codex_issue69_behavior_test.py`
- `tests/fixtures/codex-issue69/upstream-behavior/distribution/`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-10. Boundary: catalog counts/locales, generated plugin and temporary installs. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

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
- `README.es.md`, `README.ja.md`, `README.ko.md`, `README.md`, `README.zh.md`
- `codex/README.md`
- `codex/agents/README.md`
- `plugins/ywc-agent-toolkit/`
- `tests/fixtures/codex-issue69/upstream-adoption/distribution.json`
- `tests/codex_issue69_behavior_test.py`
- `tests/fixtures/codex-issue69/upstream-behavior/distribution/`

### Shared Surfaces
- `codex/agents/README.md`
- `tests/codex_issue69_behavior_test.py`

### Conflicts With
- yk-000001-020-domain-analyst-modes
- yk-000001-070-domain-operational-safety
- yk-000001-090-domain-infra-evidence
- yk-000001-100-domain-pr-worktrees

### Parallelizable After
- yk-000001-010-domain-model-hints
- yk-000001-020-domain-analyst-modes
- yk-000001-030-domain-authoring-feedback
- yk-000001-040-domain-session-retro
- yk-000001-050-domain-session-handoff
- yk-000001-060-domain-review-defects
- yk-000001-070-domain-operational-safety
- yk-000001-080-domain-mission-anchor
- yk-000001-090-domain-infra-evidence
- yk-000001-100-domain-pr-worktrees
- yk-000001-110-domain-convergence-callers
- yk-000001-120-domain-pr-body

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `python3 tests/codex_issue69_behavior_test.py`
- `bash scripts/install.sh --list --codex`
- `bash scripts/install.sh --list --codex-agents`
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
