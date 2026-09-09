# yw-000024-010-domain-parallel-monitor-gate

## Purpose
Make parallel worker dispatch distinguish attributable completion from silent or possibly-live workers before lifecycle actions proceed.

## Scope
Update the post-dispatch gate, preserve source task names for state/worktree/report operations, use returned canonical targets for collaboration calls, and add focused parallel-executor eval coverage.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#functional-requirements` — FR-1 and FR-2
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#acceptance-criteria` — AC1–AC3

### Summary
The parallel executor must consume the shared monitoring reference after successful dispatch. Missing or malformed returned targets stay outside the active roster and use existing dispatch-failure handling; silent workers may only become preserved failures after quiescence, while possibly-live workers block cleanup, next waves, reports, and `DONE`.

### Out of Scope (from spec)
- Shared monitoring contract — handled by `yw-000023-010-docs-subagent-async-monitoring-contract`
- Sequential advisors — handled by `yw-000024-020-domain-sequential-advisor-monitor`
- Review-worker output — handled by `yw-000024-030-domain-review-monitor-output`
- Package sync — handled by `yw-000025-010-infra-codex-package-validation`

## Criticality
critical

## Dependencies

### Depends On
- `yw-000023-010-docs-subagent-async-monitoring-contract` — provides canonical identity and quiescence rules

### Depended By
- `yw-000025-010-infra-codex-package-validation` — validates the final source and generated package

## Key Files
- `codex/skills/ywc-parallel-executor/SKILL.md` — post-dispatch monitoring gate
- `codex/skills/ywc-parallel-executor/evals/evals.json` — worker monitoring scenarios

## Notes
- Do not invent canonical identity from agent IDs or requested labels.
- Reuse preserved-failure handling only after quiescence evidence and exactly one source-task transition.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `codex/skills/ywc-parallel-executor/evals/evals.json` and `codex/skills/ywc-parallel-executor/scripts/test-transition-safety.py`
- RED-first target: add the silent-stall and terminal-during-escalation eval cases before finalizing prose changes.

### Interface Contract
- Contract: shared async-monitoring consumer gate
- Owner task: `yw-000024-010-domain-parallel-monitor-gate`
- Canonical signature: successful dispatch result + source task → returned canonical target used only for collaboration operations; source task remains lifecycle identity
- Consumers: existing parallel wave/failure/report paths
- Implementation opacity: downstream paths rely on the source/target split and do not infer identity independently
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: dispatch result, source task, monitor observations
- Outputs: terminal evidence or preserved failure/blocking decision
- Error model: absent identity/non-terminal payload is dispatch failure or blocked; possibly-live forbids lifecycle progression
- Impacted tests: `bash scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review
- Review requirement: `ywc-impl-review`

### Data Integrity Hardening
- Trigger surface: shared mutable task/worktree lifecycle and retryable collaboration commands
- Atomic / locking strategy: equivalent serialized guard — one source task transition and bounded per-target escalation
- Transaction boundary: dispatch-monitor-failure transition before cleanup or next wave
- Idempotency guard: at most one request and one interrupt per target; no auto-redispatch
- Required tests: silent stall, terminal during escalation, failed/unparseable spawn, duplicate transition

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/evals/evals.json`
- `codex/skills/ywc-parallel-executor/scripts/test-transition-safety.py` only if needed for task-owned assertions

### Shared Surfaces
- `codex/skills/references/subagent-async-monitoring.md` — read-only dependency
- Parallel executor task/worktree/preserved-failure lifecycle

### Conflicts With
- `yw-000024-020-domain-sequential-advisor-monitor` and `yw-000024-030-domain-review-monitor-output` only if they attempt to modify the shared reference

### Parallelizable After
- `yw-000023-010-docs-subagent-async-monitoring-contract`

### Task Verify
- `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-parallel-executor/evals/evals.json", "utf8"))'`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
- Changing task-state authority, worktree cleanup policy, agent TOMLs, or automatic redispatch.
