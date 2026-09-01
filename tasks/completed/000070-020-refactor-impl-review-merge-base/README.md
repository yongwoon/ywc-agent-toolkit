# 000070-020-refactor-impl-review-merge-base

## Purpose
Make `ywc-impl-review` review a caller's fixed point through `HEAD` using an auditable merge-base boundary.

## Scope
Add mutually exclusive `--base <ref>` handling, commit resolution, merge-base calculation, empty-diff rejection, consistent three-dot file/patch propagation, report-header evidence, and structural eval coverage while preserving `--git-range`, `--code`, and `--working-tree` semantics.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#amended-ywc-impl-review---base-contract` — exact target and diff semantics
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#updated-acceptance-and-evidence` — required fixture cases

### Summary
`--base` is a fourth mutually exclusive review target. It resolves `<ref>^{commit}`, computes `git merge-base <ref> HEAD`, rejects resolution/merge-base failures and empty `git diff --name-only <merge-base>...HEAD`, and sends the same three-dot boundary plus final contents to every Phase 1 worker. Explicit two-endpoint ranges remain unchanged.

### Out of Scope (from spec)
- Direct implementation workflow — handled by `000070-010-domain-ywc-implement-skill`.
- Handoff wording — handled by `000071-010-refactor-direct-lane-handoffs`.
- Generated marketplace synchronization — handled by `000072-010-infra-sync-codex-package-validation`.

## Dependencies

### Depends On
- `000070-010-domain-ywc-implement-skill` — establishes the direct lane's downstream review contract.

### Depended By
- `000071-010-refactor-direct-lane-handoffs` — references the finalized review target semantics.
- `000072-010-infra-sync-codex-package-validation` — validates the complete source set.

## Key Files
- `codex/skills/ywc-impl-review/SKILL.md` — target parsing and report contract.
- `codex/skills/ywc-impl-review/README*.md` — user-facing contract documentation.
- `codex/skills/ywc-impl-review/evals/evals.json` — merge-base and compatibility coverage.
- `codex/skills/ywc-impl-review/agents/openai.yaml` — regenerated metadata if description changes.

## Notes
Do not reinterpret explicit `--git-range A..B`, `--code`, or `--working-tree`. Keep target selection validation before review-file reads.

## Hardening Evidence

### Test Feedback Path
- RED-first target: `codex/skills/ywc-impl-review/evals/evals.json` with invalid/mixed/empty-diff cases.
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh`.

### Interface Contract
- Contract: review target selection and report header.
- Inputs: exactly one of `--base`, `--git-range`, `--code`, or `--working-tree`.
- Outputs: changed-file list, patch, final contents, and report header containing supplied base and resolved merge-base in base mode.
- Error model: `NEEDS_CONTEXT` for missing/mixed target, unresolved ref, no merge-base, or empty diff.

### Critical Surface Review
- Review requirement: full `ywc-impl-review` contract review and repository validation.

### Data Integrity Hardening
- Trigger surface: N/A — read-only review boundary and documentation.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-impl-review/**`

### Shared Surfaces
- Review target contract consumed by direct implementation and executor callers.
- Codex metadata and eval contract.

### Conflicts With
- `000071-010-refactor-direct-lane-handoffs` — references this contract and must wait for it.

### Parallelizable After
- `000070-010-domain-ywc-implement-skill`

### Task Verify
- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-impl-review`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Do not alter review worker rubrics, severity policy, or unrelated target modes.
