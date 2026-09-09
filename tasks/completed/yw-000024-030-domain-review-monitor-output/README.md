# yw-000024-030-domain-review-monitor-output

## Purpose
Make Phase 1 review output bounded, read-only, attributable, and honest about unavailable or possibly-live reviewers.

## Scope
Update shared status-action semantics and `ywc-impl-review` monitoring/output precedence, then add focused review eval coverage.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#functional-requirements` — FR-1 and FR-4
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#acceptance-criteria` — AC5–AC6

### Summary
Phase 1 generic or named reviewers may return only bounded inline fields and may not write files. `ywc-impl-review` monitors successful lanes and applies possibly-live → `BLOCKED`, quiescent unavailable → `DONE_WITH_CONCERNS`, then ordinary aggregation; `subagent-status-actions.md` remains the terminal-status authority.

### Out of Scope (from spec)
- Shared liveness contract — handled by `yw-000023-010-docs-subagent-async-monitoring-contract`
- Parallel implementation worker gate — handled by `yw-000024-010-domain-parallel-monitor-gate`
- Sequential advisor fallback — handled by `yw-000024-020-domain-sequential-advisor-monitor`
- Agent TOML changes and generated package sync — handled by `yw-000025-010-infra-codex-package-validation`

## Criticality
critical

## Dependencies

### Depends On
- `yw-000023-010-docs-subagent-async-monitoring-contract` — provides review-worker liveness and quiescence rules

### Depended By
- `yw-000025-010-infra-codex-package-validation` — validates final source and generated package

## Key Files
- `codex/skills/references/subagent-status-actions.md` — Phase 1 inline exception
- `codex/skills/ywc-impl-review/SKILL.md` — monitor gate and report precedence
- `codex/skills/ywc-impl-review/evals/evals.json` — reviewer scenarios

## Notes
- Within this task, update `subagent-status-actions.md` first, then make `ywc-impl-review` consume it.
- Do not touch executor state helpers, worktrees, cleanup, or `preserved_failed` for the read-only review lane.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `codex/skills/ywc-impl-review/evals/evals.json`
- RED-first target: add reviewer unavailable, possibly-live, and malformed-output eval cases before finalizing review prose.

### Interface Contract
- Contract: Phase 1 bounded read-only reviewer payload
- Owner task: `yw-000024-030-domain-review-monitor-output`
- Canonical signature: reviewer dispatch → canonical target, `Status`, one-line `Summary`, 0–5 confirmed findings, 0–2 advisor candidates inline
- Consumers: Phase 1 review lanes and Phase 2 selection/aggregation
- Implementation opacity: downstream aggregation trusts only validated bounded payloads and monitor precedence
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: reviewer target, inline payload, roster state, elapsed time, raw-evidence category
- Outputs: ordinary aggregation, `DONE_WITH_CONCERNS`, or minimal monitoring-blocked `BLOCKED`
- Error model: malformed/status-less/ambiguous/non-attributable output is non-terminal
- Impacted tests: `bash scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review
- Review requirement: `ywc-impl-review` plus manual full implementation review of the monitor precedence

### Data Integrity Hardening
- Trigger surface: shared mutable review aggregation state and duplicate-sensitive lifecycle gating
- Atomic / locking strategy: equivalent serialized guard — each lane transitions once after terminal/quiescence evidence
- Transaction boundary: Phase 1 lane monitoring through Phase 2/aggregation gate
- Idempotency guard: one bounded request/interrupt per target; no review redispatch
- Required tests: unavailable, possibly-live, malformed output, and clean-all-lanes scenarios

## Parallel Execution Metadata

### Ownership
- `codex/skills/references/subagent-status-actions.md`
- `codex/skills/ywc-impl-review/SKILL.md`
- `codex/skills/ywc-impl-review/evals/evals.json`

### Shared Surfaces
- Terminal-status semantics in `subagent-status-actions.md`
- Phase 1/Phase 2 review report contract

### Conflicts With
- `yw-000024-010-domain-parallel-monitor-gate` and `yw-000024-020-domain-sequential-advisor-monitor` only if they attempt to modify shared status or monitoring references

### Parallelizable After
- `yw-000023-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-impl-review/evals/evals.json", "utf8"))'`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
- Review agent TOMLs, Phase 2 rubric selection changes unrelated to monitoring precedence, and executor lifecycle helpers.
