# yw-000021-020-test-impl-review-verification-evals — Implementation Checklist

## Prerequisites

- [ ] `yw-000021-010-domain-impl-review-verification-contract` is completed and merged.

## Allowed Edit Scope

- [ ] Modify only `codex/skills/ywc-impl-review/evals/evals.json`.
- [ ] Stop and report if an assertion requires `SKILL.md`, README, package, or runner edits.

## Stop Conditions

- [ ] Stop if the finalized source workflow uses a status or packet shape not described by the specification.
- [ ] Stop if a required assertion cannot fit the existing eval JSON schema.
- [ ] Stop if a scenario would require a runtime fixture or custom-agent implementation.

## Hardening Gate

- [ ] Classify this task as test-only.
- [ ] Add the focused eval expectation before considering the source contract sufficiently covered.
- [ ] Consume the owner task's orchestration protocol; return `NEEDS_CONTEXT` on an owner, signature, or consumer mismatch.
- [ ] Data Integrity Hardening is N/A because this is an eval fixture.
- [ ] Critical surface review is N/A because this task has no production behavior edit.

## Implementation Steps

- [ ] Add scope-guardrail scenarios to `codex/skills/ywc-impl-review/evals/evals.json`.
  - [ ] Cover empty `--git-range`, empty `--code`, and otherwise empty selected targets returning `NEEDS_CONTEXT` before Phase 1 dispatch.
  - [ ] Cover values above 200 files and, for diff targets, 5,000 changed lines, including exact counts and five-largest-file reporting; assert that `--code` has no fabricated line metric.
- [ ] Add blind independent-verification scenarios.
  - [ ] Assert minimal `file:line` plus severity packet content, no original rationale, Critical-before-High ordering, and the 20-call cap.
  - [ ] Cover reproduced evidence, `verification-failed`, `verification-error`, and cap-unverified outcomes.
- [ ] Add routing and report assertions.
  - [ ] Assert failed/error candidates are prioritized into Phase 2 before budget selection without reducing `--advisor-budget`.
  - [ ] Assert `--no-advisor` keeps every non-reproduced or cap-skipped item explicitly unverified and preserves verification counts/provenance.

## Task Verify

- [ ] `jq empty codex/skills/ywc-impl-review/evals/evals.json`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification

- [ ] JSON is valid and IDs remain unique.
- [ ] The structural contract-eval runner passes.
- [ ] Generated package parity is deferred to `yw-000022-010-infra-impl-review-package-validation`.

## Implementation Notes (optional)

