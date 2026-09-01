# 000071-010-refactor-direct-lane-handoffs

## Purpose
Prevent routing ambiguity between direct implementation, generated code, and generated-task execution lanes.

## Scope
Update only the integration text and metadata in `ywc-code-gen` and `ywc-sequential-executor` that must name `ywc-implement` as the single approved-item alternative.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#fr-3-update-connected-skill-metadata-and-documentation-minimally` — constrained handoff scope
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#scope` — preserved ownership boundaries

### Summary
The existing multi-layer generator and generated-task lifecycle remain authoritative for their current jobs. Their descriptions may mention `ywc-implement` only where that prevents misrouting, without broadening either skill's ownership or changing their execution behavior.

### Out of Scope (from spec)
- New direct implementation behavior — handled by `000070-010-domain-ywc-implement-skill`.
- Merge-base review semantics — handled by `000070-020-refactor-impl-review-merge-base`.
- Generated package output — handled by `000072-010-infra-sync-codex-package-validation`.

## Dependencies

### Depends On
- `000070-020-refactor-impl-review-merge-base` — provides the finalized review contract to reference.

### Depended By
- `000072-010-infra-sync-codex-package-validation` — syncs and validates the finished source tree.

## Key Files
- `codex/skills/ywc-code-gen/SKILL.md` and required metadata/readmes if wording changes.
- `codex/skills/ywc-sequential-executor/SKILL.md` and required metadata/readmes if wording changes.

## Notes
Make the smallest wording change that removes overlap. If no wording change is necessary after inspection, record that result and leave the files untouched.

## Hardening Evidence

### Test Feedback Path
- Named exception: documentation-only routing audit; replacement verification is skill contract validation and diff inspection.

### Interface Contract
- Contract: activation and handoff descriptions only; no runtime behavior changes.
- Inputs/outputs: unchanged skill invocation contracts.
- Error model: unchanged.

### Critical Surface Review
- Review requirement: `N/A` — documentation-only routing change.

### Data Integrity Hardening
- Trigger surface: N/A — documentation-only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-code-gen/SKILL.md` and its directly required metadata/readmes.
- `codex/skills/ywc-sequential-executor/SKILL.md` and its directly required metadata/readmes.

### Shared Surfaces
- Codex skill activation descriptions and handoff wording.

### Conflicts With
- `000070-010-domain-ywc-implement-skill`, `000070-020-refactor-impl-review-merge-base` — source contracts must be finalized first.

### Parallelizable After
- `000070-020-refactor-impl-review-merge-base`

### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `git diff -- codex/skills/ywc-code-gen codex/skills/ywc-sequential-executor`

## Out of Scope
Do not modify implementation behavior, executor lifecycle, Claude skills, install scripts, or CI.
