# yw-000051-010-docs-mobile-first-consumers

## Purpose
Carry the canonical mobile-first policy into generated UI tasks and both Codex execution modes.

## Scope
Update task-generator, sequential-executor, and parallel-executor instructions to read the shared policy before layout/style work and order mobile base styles before `min-width` expansion, while honoring explicit exceptions.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#functional-requirements`
- `codex/skills/references/mobile-first-ui.md`

### Summary
The task generator must make mobile-first ordering explicit for UI layout/style tasks. Sequential and parallel workers must consume the same reference before implementation. The instruction is conditional and does not rewrite legacy UI or apply to non-UI work.

### Out of Scope (from spec)
- Canonical policy wording — handled by `yw-000050-010-docs-mobile-first-policy`.
- Reviewer-specific checks and deterministic evaluator implementation — handled by `yw-000051-020-docs-mobile-first-reviewer` and `yw-000052-010-test-mobile-first-contract-eval`.
- Generated plugin parity — handled by `yw-000053-010-infra-mobile-first-distribution`.

## Criticality
normal — skill instruction changes only.

## Dependencies

### Depends On
- `yw-000050-010-docs-mobile-first-policy` — provides the canonical reference and trigger semantics.

### Depended By
- `yw-000052-010-test-mobile-first-contract-eval` — validates all five named consumers.

## Key Files
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`

## Notes
Keep the trigger, `min-width` direction, exception, and no-retrofit semantics aligned with `codex/skills/references/mobile-first-ui.md`.

## Hardening Evidence

### Test Feedback Path
- `(N/A — documentation contract; downstream deterministic checker provides evidence.)`

### Interface Contract
- Contract: `mobile-first UI task/worker instruction`
- Owner task: `yw-000050-010-docs-mobile-first-policy`
- Canonical signature: `end-user UI layout/style work -> read policy, mobile base first, then min-width expansion; explicit exception permitted`
- Consumers: `ywc-task-generator`, `ywc-sequential-executor`, `ywc-parallel-executor`
- Implementation opacity: consumers trust the shared policy and do not redefine its semantics.
- Mismatch action: `NEEDS_CONTEXT`

### Critical Surface Review
- Review requirement: `N/A`

### Data Integrity Hardening
- Trigger surface: `N/A — docs-only`
- Atomic / locking strategy: `N/A`
- Transaction boundary: `N/A`
- Idempotency guard: `N/A`
- Required tests: `N/A`

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`

### Shared Surfaces
- `codex/skills/references/mobile-first-ui.md`
- UI task and worker instruction wording.

### Conflicts With
- `yw-000051-020-docs-mobile-first-reviewer` — avoid changing shared policy wording while reviewer semantics are being authored.

### Parallelizable After
- `yw-000050-010-docs-mobile-first-policy`

### Task Verify
- `git diff --check`
- `rg -n "mobile-first-ui|min-width|PC/tablet|end-user UI|legacy" codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`

## Out of Scope
Do not modify the shared reference, custom-agent TOML, eval JSON, contract runner, generated plugin, or Claude Code skills.
