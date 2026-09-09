# yw-000021-010-domain-impl-review-verification-contract

## Purpose

Define the Codex `ywc-impl-review` scope guardrail and independent-verification orchestration contract. This prevents oversized or empty reviews from reaching Phase 1 and prevents uncorroborated Critical or High findings from being reported as facts.

## Scope

- Add the Step 2.5 review-scope guardrail and Step 4.5 blind verifier pass to `SKILL.md`.
- Route verifier outcomes through the existing Phase 2 budget flow and extend the report contract with per-finding provenance and aggregate verification counts.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#functional-requirements` — required scope, verifier, routing, and report behavior.
- `docs/ywc-plans/20260909-ywc-impl-review-independent-verification.md#acceptance-criteria` — acceptance criteria AC1–AC5 governing this task.

### Summary

The source skill must reject empty review targets and targets exceeding 200 files or, where a diff exists, 5,000 changed lines before Phase 1 dispatch. It must independently and blindly re-derive eligible Phase 1 Critical and High findings, with a 20-call cap and explicit reproduced, failed, error, and cap-skipped states. Verification-derived candidates join Phase 2 without consuming the advisor budget.

### Out of Scope (from spec)

- Behavioral contract-eval scenarios — handled by `yw-000021-020-test-impl-review-verification-evals`.
- Localized user documentation — handled by `yw-000021-030-docs-impl-review-localized-flow`.
- Plugin synchronization and repository-wide validation — handled by `yw-000022-010-infra-impl-review-package-validation`.
- `codex/agents/*.toml` changes and Claude Code synchronization — excluded by the specification.

## Criticality

normal

## Dependencies

### Depends On

- (None — prior numbered phases are complete.)

### Depended By

- `yw-000021-020-test-impl-review-verification-evals` — consumes the finalized orchestration and report contract.
- `yw-000021-030-docs-impl-review-localized-flow` — describes the finalized user-visible review flow.
- `yw-000022-010-infra-impl-review-package-validation` — synchronizes the finished source artifact.

## Key Files

- `codex/skills/ywc-impl-review/SKILL.md` — authoritative review workflow and report contract.

## Notes

Keep `--advisor-budget`, the five Phase 1 axes, Phase 2 selection policy, and custom-agent contracts unchanged. `--code` has no intrinsic changed-line metric, so it receives only the file-count guardrail. `contract_state: N/A — no architecture contract`; this repository has no `architecture-invariants.yaml`.

## Hardening Evidence

### Test Feedback Path

- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh` after the downstream eval-contract task is merged.

### Interface Contract

- Contract: Implementation-review orchestration protocol.
- Owner task: `yw-000021-010-domain-impl-review-verification-contract`.
- Canonical signature: `selected target + Phase 1 findings -> scope decision, verification status, Phase 2 candidate priority, report fields`.
- Consumers: `yw-000021-020-test-impl-review-verification-evals`, `yw-000021-030-docs-impl-review-localized-flow`, and Codex users.
- Implementation opacity: downstream tasks consume this documented contract and do not redesign Phase 1, Phase 2, or custom-agent internals.
- Mismatch action: `NEEDS_CONTEXT`.
- Inputs: one valid target mode and Phase 1 findings with location and severity.
- Outputs: bounded refusal or findings with provenance, verification status, and aggregate counts.
- Error model: empty/oversized target is `NEEDS_CONTEXT`; malformed or unavailable verifier result is `verification-error`.
- Impacted tests: `codex/skills/ywc-impl-review/evals/evals.json`; `bash scripts/run-codex-skill-contract-evals.sh`.

### Critical Surface Review

- Review requirement: manual full implementation review; the task changes the trust semantics of high-severity review findings.

### Data Integrity Hardening

- Trigger surface: N/A — instruction and report-contract change only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-impl-review/SKILL.md`

### Shared Surfaces

- Review-flow contract consumed by `evals/evals.json` and all six localized README files.
- Generated plugin mirror under `plugins/ywc-agent-toolkit/skills/ywc-impl-review/`.

### Conflicts With

- `yw-000021-020-test-impl-review-verification-evals` — must wait for the finalized workflow contract.
- `yw-000021-030-docs-impl-review-localized-flow` — must wait for finalized user-visible terminology.
- `yw-000022-010-infra-impl-review-package-validation` — generated mirror must not be synchronized from a partial source contract.

### Parallelizable After

- Root task — no predecessor required.

### Task Verify

- `rg -n 'Step 2\.5|Step 4\.5|200 files|5,000|20' codex/skills/ywc-impl-review/SKILL.md`
- `git diff --check -- codex/skills/ywc-impl-review/SKILL.md`

## Out of Scope

Do not edit eval JSON, README files, plugin mirror files, or `codex/agents/*.toml` in this task.
