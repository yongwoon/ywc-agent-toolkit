# yw-000021-030-docs-impl-review-localized-flow

## Purpose

Align all maintained `ywc-impl-review` README locales with the new scope guardrail, verification provenance, and generic Codex-worker terminology.

## Scope

- Revise the English source README and five maintained localized README surfaces.
- Remove Claude-only Sonnet, Haiku, and Opus model claims while retaining the five-axis and Phase 2 explanation.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#documentation-and-distribution-contract` — locale parity and model-language requirements.
- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#acceptance-criteria` — AC6 user-facing requirements.

### Summary

All six README surfaces must explain that review scope is bounded before fan-out and that eligible Critical/High Phase 1 claims gain an independent verification state. They must preserve the existing five-axis review model and Phase 2 advisor concept without making runtime-inapplicable model promises.

### Out of Scope (from spec)

- `SKILL.md` behavior and report-template implementation — handled by `yw-000021-010-domain-impl-review-verification-contract`.
- Behavioral eval assertions — handled by `yw-000021-020-test-impl-review-verification-evals`.
- Generated plugin synchronization — handled by `yw-000022-010-infra-impl-review-package-validation`.

## Criticality

normal

## Dependencies

### Depends On

- `yw-000021-010-domain-impl-review-verification-contract` — supplies exact report fields and verification terminology.

### Depended By

- `yw-000022-010-infra-impl-review-package-validation` — mirrors the complete source documentation and runs validation.

## Key Files

- `codex/skills/ywc-impl-review/README.en.md` — English source description.
- `codex/skills/ywc-impl-review/README.md` — default Korean surface.
- `codex/skills/ywc-impl-review/README.ko.md`, `README.ja.md`, `README.zh.md`, `README.es.md` — maintained localized surfaces.

## Notes

Use the source SKILL contract as authority when a README summary differs. Retain each locale's prose language and technical terms, paths, commands, and identifiers. `contract_state: N/A — no architecture contract`.

## Hardening Evidence

### Test Feedback Path

- Named exception: documentation-only change; use `rg -n 'Sonnet|Haiku|Opus' codex/skills/ywc-impl-review/README*.md` and `bash scripts/validate.sh` after package sync as replacement verification.

### Interface Contract

- Contract: User-facing implementation-review flow.
- Owner task: `yw-000021-010-domain-impl-review-verification-contract`.
- Canonical signature: `review target + findings -> bounded review outcome with verification provenance`.
- Consumers: README readers and `yw-000022-010-infra-impl-review-package-validation`.
- Implementation opacity: documentation reflects the source contract and does not redefine it.
- Mismatch action: `NEEDS_CONTEXT`.
- Inputs: final SKILL terminology and report fields.
- Outputs: aligned locale explanations.
- Error model: N/A — documentation surface.
- Impacted tests: `bash scripts/validate.sh` after generated-package synchronization.

### Critical Surface Review

- Review requirement: N/A — documentation-only task.

### Data Integrity Hardening

- Trigger surface: N/A — documentation-only task.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-impl-review/README.md`
- `codex/skills/ywc-impl-review/README.en.md`
- `codex/skills/ywc-impl-review/README.ko.md`
- `codex/skills/ywc-impl-review/README.ja.md`
- `codex/skills/ywc-impl-review/README.zh.md`
- `codex/skills/ywc-impl-review/README.es.md`

### Shared Surfaces

- User-visible review-flow terminology and report provenance owned by `yw-000021-010-domain-impl-review-verification-contract`.
- Generated plugin mirror documentation.

### Conflicts With

- `yw-000021-010-domain-impl-review-verification-contract` — finalized terms must be available before locale edits.
- `yw-000022-010-infra-impl-review-package-validation` — do not synchronize generated README mirrors while source locales are in flight.

### Parallelizable After

- `yw-000021-010-domain-impl-review-verification-contract`

### Task Verify

- `rg -n 'Sonnet|Haiku|Opus' codex/skills/ywc-impl-review/README*.md`
- `git diff --check -- codex/skills/ywc-impl-review/README*.md`

## Out of Scope

Do not edit the source SKILL, eval fixture, generated plugin files, or custom-agent TOML files.
