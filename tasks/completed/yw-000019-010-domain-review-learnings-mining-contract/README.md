# yw-000019-010-domain-review-learnings-mining-contract

## Purpose
Extend the Codex `ywc-review-learnings` contract so the new batch miner can hand off project-local candidates through a confirmation-gated `mining` source.

## Scope
Update the source enum, capture-source procedure, and mining-source eval fixture. Preserve `ywc-review-learnings` as the sole durable-write owner and require aggregated distinct-PR provenance, representative evidence, rule, why, polarity, and the same confirmed changeset.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr1--skill-metadata-and-localized-documentation`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#fr3--classification-routing-and-confirmation`
- `docs/ywc-plans/20260909-codex-mine-review-history-pr226-port.md#module-boundaries`

### Summary
This task defines the consumer-side contract for mining-derived learnings. `mining` must preserve the existing rule/why/polarity and confirmation gate while adding aggregated distinct-PR provenance and representative evidence. It must not give the producer direct write authority.

### Out of Scope (from spec)
- New producer skill and helper — handled by `yw-000019-020-domain-mine-review-history-skill`.
- Mining behavior and hermetic helper tests — handled by `yw-000019-030-test-mine-review-history-contract`.
- Shared recurring-defect catalog mutation — never performed at runtime.

## Criticality
normal

## Dependencies
### Depends On
- (None — root task)

### Depended By
- `yw-000019-020-domain-mine-review-history-skill` — consumes the confirmed `mining` handoff contract.
- `yw-000019-030-test-mine-review-history-contract` — adds fixtures for this source contract.

## Key Files
- `codex/skills/ywc-review-learnings/SKILL.md` — add `mining` source and handoff requirements.
- `codex/skills/ywc-review-learnings/references/capture-sources.md` — document mining evidence and provenance.
- `codex/skills/ywc-review-learnings/evals/evals.json` — add mining-source behavior fixture.

## Notes
Keep the existing `feedback`, `review`, and `pr` semantics intact. Use the canonical term `mining` consistently; do not introduce a synonym such as `batch` as an enum value.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: `python3 -m json.tool codex/skills/ywc-review-learnings/evals/evals.json >/dev/null` and `bash scripts/run-codex-skill-contract-evals.sh`.
- Named exception: documentation/fixture contract change; targeted source inspection replaces RED-first production testing.

### Interface Contract
- Contract: `ywc-review-learnings --mode update --source mining`
- Owner task: `yw-000019-010-domain-review-learnings-mining-contract`
- Canonical signature: aggregated mining evidence + confirmed changeset → project-local durable learning update
- Consumers: `yw-000019-020-domain-mine-review-history-skill`, `ywc-impl-review`
- Implementation opacity: consumers trust this handoff contract and do not bypass its write authority.
- Mismatch action: `NEEDS_CONTEXT`
- Inputs: distinct PR list, representative comment/evidence, rule, why, polarity, target, confirmed changeset
- Outputs: confirmed project-local learning update or no write before confirmation
- Error model: incomplete evidence is dropped/accounted for; unconfirmed changesets are not written
- Impacted tests: `codex/skills/ywc-review-learnings/evals/evals.json`, contract-eval runner

### Critical Surface Review
- Review requirement: N/A — contract documentation and fixtures only.

### Data Integrity Hardening
- Trigger surface: duplicate-sensitive side effect
- Atomic / locking strategy: confirmation gate plus existing learning-file owner
- Transaction boundary: one confirmed changeset applied by `ywc-review-learnings`
- Idempotency guard: existing duplicate/modify handling in the learning-file owner
- Required tests: duplicate recurrence fixture and confirmation-before-write fixture

## Parallel Execution Metadata
### Ownership
- `codex/skills/ywc-review-learnings/SKILL.md`
- `codex/skills/ywc-review-learnings/references/capture-sources.md`
- `codex/skills/ywc-review-learnings/evals/evals.json`

### Shared Surfaces
- `ywc-review-learnings` source grammar and confirmation handoff

### Conflicts With
- `yw-000019-020-domain-mine-review-history-skill` — both depend on the exact mining handoff wording; execute sequentially.

### Parallelizable After
- Root task — no predecessor required.

### Task Verify
- `rg -n "source.*mining|--source mining|distinct-PR|confirmation" codex/skills/ywc-review-learnings/SKILL.md codex/skills/ywc-review-learnings/references/capture-sources.md`
- `python3 -m json.tool codex/skills/ywc-review-learnings/evals/evals.json >/dev/null`

## Out of Scope
- Creating or syncing the new skill.
- Editing any generated marketplace package.
