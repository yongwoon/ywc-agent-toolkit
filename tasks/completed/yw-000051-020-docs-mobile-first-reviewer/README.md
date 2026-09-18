# yw-000051-020-docs-mobile-first-reviewer

## Purpose
Extend the bounded TypeScript reviewer with conditional mobile-first UI review behavior and its evaluation scenario.

## Scope
Update the existing read-only reviewer and add one `ywc-typescript-reviewer` eval scenario. The reviewer checks only end-user UI layout/style diffs, flags desktop-first claw-back patterns, skips legacy UI absent redesign scope, and returns `NEEDS_CONTEXT` when target-surface evidence is missing.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#functional-requirements`
- `codex/skills/references/mobile-first-ui.md`

### Summary
The reviewer remains read-only and bounded to the supplied TypeScript/JavaScript diff and evidence packet. The new Framework-idiom finding is conditional on end-user UI layout/style scope and must not infer intent for missing evidence. The eval record must preserve the existing agent-eval schema.

### Out of Scope (from spec)
- Shared policy creation — handled by `yw-000050-010-docs-mobile-first-policy`.
- Skill consumer wording — handled by `yw-000051-010-docs-mobile-first-consumers`.
- Deterministic cross-file source checker — handled by `yw-000052-010-test-mobile-first-contract-eval`.
- Plugin synchronization — handled by `yw-000053-010-infra-mobile-first-distribution`.

## Criticality
normal — bounded read-only review contract; no production runtime behavior.

## Dependencies

### Depends On
- `yw-000050-010-docs-mobile-first-policy` — provides the canonical policy semantics.

### Depended By
- `yw-000052-010-test-mobile-first-contract-eval` — validates the reviewer directive and eval record.

## Key Files
- `codex/agents/ywc-typescript-reviewer.toml`
- `codex/agents/evals/evals.json`

## Notes
Do not create a new agent role or alter the read-only, bounded evidence, sandbox, or model contract.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `bash scripts/check-codex-agent-evals.sh`
- Named exception: source-contract assertions are added in `yw-000052-010-test-mobile-first-contract-eval`.

### Interface Contract
- Contract: `ywc-typescript-reviewer bounded review packet -> findings/status`
- Owner task: `yw-000051-020-docs-mobile-first-reviewer`
- Canonical signature: `evidence packet + bounded TS/JS diff -> read-only findings; missing target-surface evidence -> NEEDS_CONTEXT`
- Consumers: `scripts/run-codex-skill-contract-evals.sh`, agent eval harness
- Implementation opacity: callers use the bounded reviewer contract without expanding its scope.
- Mismatch action: `NEEDS_CONTEXT`

### Critical Surface Review
- Review requirement: `N/A — no production or security-sensitive behavior`

### Data Integrity Hardening
- Trigger surface: `N/A — read-only documentation/agent contract`
- Atomic / locking strategy: `N/A`
- Transaction boundary: `N/A`
- Idempotency guard: `N/A`
- Required tests: `N/A`

## Parallel Execution Metadata

### Ownership
- `codex/agents/ywc-typescript-reviewer.toml`
- `codex/agents/evals/evals.json` — one reviewer scenario only.

### Shared Surfaces
- `codex/skills/references/mobile-first-ui.md`
- `codex/agents/evals/evals.json` schema.

### Conflicts With
- `yw-000051-010-docs-mobile-first-consumers` — avoid simultaneous edits to shared policy wording.

### Parallelizable After
- `yw-000050-010-docs-mobile-first-policy`

### Task Verify
- `jq empty codex/agents/evals/evals.json`
- `bash scripts/check-codex-agent-evals.sh`
- `git diff --check`

## Out of Scope
Do not modify reviewer execution code, add agent roles, change sandbox/model contracts, or alter non-UI review behavior.
