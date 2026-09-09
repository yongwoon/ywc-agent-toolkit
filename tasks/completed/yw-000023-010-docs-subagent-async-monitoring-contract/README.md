# yw-000023-010-docs-subagent-async-monitoring-contract

## Purpose
Define one shared asynchronous-subagent monitoring contract so consumer skills use identical identity, liveness, escalation, and quiescence rules.

## Scope
Add the shared reference and its phase-specific scenario matrix. Establish the citation boundary with `subagent-status-actions.md`; do not implement consumer behavior here.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#functional-requirements` — FR-1 and shared constraints
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#acceptance-criteria` — AC1–AC6

### Summary
The reference owns label normalization, successful-dispatch identity capture, full-roster reconciliation, bounded heartbeats, escalation timing, API-failure handling, and quiescence. It must cite `subagent-status-actions.md` for terminal-status interpretation instead of duplicating lifecycle policy. Consumer tasks will reference this contract after it lands.

### Out of Scope (from spec)
- Parallel executor behavior — handled by `yw-000024-010-domain-parallel-monitor-gate`
- Sequential advisor behavior — handled by `yw-000024-020-domain-sequential-advisor-monitor`
- Review output behavior — handled by `yw-000024-030-domain-review-monitor-output`
- Generated marketplace mirror — handled by `yw-000025-010-infra-codex-package-validation`

## Criticality
normal

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `yw-000024-010-domain-parallel-monitor-gate` — consumes the canonical worker monitoring contract
- `yw-000024-020-domain-sequential-advisor-monitor` — consumes the advisor monitoring contract
- `yw-000024-030-domain-review-monitor-output` — consumes review-worker monitoring and quiescence rules

## Key Files
- `codex/skills/references/subagent-async-monitoring.md` — new shared contract

## Notes
- No persisted schema, external API, library, or agent TOML change is required.
- Preserve the source-of-truth rule: generated marketplace files are not edited in this task.

## Hardening Evidence

### Test Feedback Path
- Named exception: docs/reference-only contract with no executable implementation; verify required terminology and cross-links with `rg` and `git diff --check`.

### Interface Contract
- Contract: shared subagent async-monitoring contract
- Owner task: `yw-000023-010-docs-subagent-async-monitoring-contract`
- Canonical signature: source task label + returned canonical target + collaboration observations → attributable terminal/quiescence decision inputs
- Consumers: `ywc-parallel-executor`, `ywc-sequential-executor`, `ywc-impl-review`
- Implementation opacity: consumers trust this contract and do not restate its algorithm
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: dispatch result, canonical target, `wait_agent`/`list_agents` observations, elapsed time, delivered payloads
- Outputs: normalized identity mapping, terminal-evidence classification, escalation/quiescence outcome
- Error model: missing or malformed identity is non-terminal; unproved quiescence remains blocked
- Impacted tests: `bash scripts/run-codex-skill-contract-evals.sh`

### Critical Surface Review
- Review requirement: `ywc-impl-review` for consumer behavior tasks; reference-only task does not require separate full review

### Data Integrity Hardening
- Trigger surface: shared mutable in-memory monitor mapping
- Atomic / locking strategy: equivalent serialized guard — one monitor owns each source-to-target mapping and transition
- Transaction boundary: one dispatch-monitor lifecycle; no persisted write
- Idempotency guard: one status request and one interrupt per target
- Required tests: duplicate escalation and terminal-during-escalation scenarios in the shared scenario matrix

## Parallel Execution Metadata

### Ownership
- `codex/skills/references/subagent-async-monitoring.md`

### Shared Surfaces
- `codex/skills/references/subagent-status-actions.md` citation boundary
- Collaboration API semantics: `spawn_agent`, `list_agents`, `wait_agent`, `send_message`, `interrupt_agent`

### Conflicts With
- Phase 2 consumer tasks while this contract is being authored

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `rg -n "canonical|list_agents|wait_agent|60|300|600|quiescen|scenario" codex/skills/references/subagent-async-monitoring.md`
- `git diff --check`

## Out of Scope
- Consumer-specific dispatch gates, fallback tables, review aggregation, eval scenario files, and generated package synchronization.
