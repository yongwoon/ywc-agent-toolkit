# yw-000023-010-docs-subagent-async-monitoring-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the specification is `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md`
- [ ] Confirm no Phase 2 consumer task is editing the shared reference concurrently

## Allowed Edit Scope
- [ ] Stay within `codex/skills/references/subagent-async-monitoring.md`
- [ ] Stop before editing any consumer skill, eval, agent TOML, or generated mirror

## Stop Conditions
- [ ] Stop if terminal-status ownership cannot be cited cleanly from `subagent-status-actions.md`
- [ ] Stop if a requirement needs persisted state, a new API, or a library not present in the spec
- [ ] Stop if the shared contract requires consumer-specific lifecycle policy

## Hardening Gate
- [ ] Classify as docs/reference-only with a named verification exception
- [ ] Record the shared contract signature and consumers in README before editing
- [ ] Data-integrity fields are documented because the contract governs duplicate-sensitive escalation; no persisted transaction is introduced
- [ ] Consumer behavior changes require `ywc-impl-review` in their own tasks

## Implementation Steps
- [ ] Create `codex/skills/references/subagent-async-monitoring.md` with label normalization and source-label/returned-target identity rules.
- [ ] Define event-first reconciliation across delivered terminal payloads, `wait_agent`, and complete `list_agents` roster observations.
- [ ] Define ≤60-second heartbeat cadence, 600-second implementation/review escalation, 300-second advisor escalation, one-request/one-interrupt bounds, and terminal-during-escalation precedence.
- [ ] Define API-failure quiescence, possibly-live blocking, preserved-failure eligibility, and late-evidence recovery handling without duplicating terminal status routing.
- [ ] Add the scenario matrix covering worker, advisor, review-worker, malformed identity, missing roster, API failure, and terminal-during-escalation cases.

## Task Verify
- [ ] `rg -n "canonical|source task|list_agents|wait_agent|heartbeat|60|300|600|quiescen|possibly-live|terminal" codex/skills/references/subagent-async-monitoring.md`
- [ ] `git diff --check`

## Verification
- [ ] Repository structure validation passes (`bash scripts/validate.sh`)
- [ ] Contract eval structure passes (`bash scripts/run-codex-skill-contract-evals.sh`)

## Implementation Notes (optional)

