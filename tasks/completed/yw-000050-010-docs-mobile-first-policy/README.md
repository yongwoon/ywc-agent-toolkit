# yw-000050-010-docs-mobile-first-policy

## Purpose
Establish one canonical mobile-first UI policy and capture it in Codex planning and scaffolding guidance.

## Scope
Create the shared reference with Rule, Trigger, Escape hatch, and Backward compatibility sections. Update the plan NFR template and project-scaffold guidance so new end-user UI records the policy or an explicit PC/tablet-only exception.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#acceptance-criteria`
- `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md#functional-requirements`

### Summary
The shared policy applies only to new end-user UI. Base styles target the narrowest viewport, later additions expand with `min-width`, and existing desktop-first CSS is not retrofitted. Admin/internal tools remain outside the trigger; an otherwise in-scope PC/tablet-only surface must state its exception explicitly.

### Out of Scope (from spec)
- Task/executor worker instructions — handled by `yw-000051-010-docs-mobile-first-consumers`.
- TypeScript reviewer and evaluation changes — handled by `yw-000051-020-docs-mobile-first-reviewer` and `yw-000052-010-test-mobile-first-contract-eval`.
- Plugin synchronization — handled by `yw-000053-010-infra-mobile-first-distribution`.

## Criticality
normal — documentation and planning guidance only.

## Dependencies

### Depends On
- (None — root task.)

### Depended By
- `yw-000051-010-docs-mobile-first-consumers` — consumes the canonical policy in task and worker instructions.
- `yw-000051-020-docs-mobile-first-reviewer` — consumes the policy in the bounded reviewer contract.

## Key Files
- `codex/skills/references/mobile-first-ui.md` — canonical policy.
- `codex/skills/ywc-plan/references/spec-template.md` — planning capture.
- `codex/skills/ywc-project-scaffold/SKILL.md` — scaffold capture.

## Notes
Keep behavioral semantics centralized in the shared reference; consumers should link to it rather than create competing definitions.

## Hardening Evidence

### Test Feedback Path
- `(N/A — docs-only task; deterministic source-contract checks are added downstream.)`

### Interface Contract
- `(N/A — the shared reference is a documentation contract, not a callable interface.)`

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
- `codex/skills/references/mobile-first-ui.md`
- `codex/skills/ywc-plan/references/spec-template.md`
- `codex/skills/ywc-project-scaffold/SKILL.md`

### Shared Surfaces
- `codex/skills/references/mobile-first-ui.md` — canonical wording consumed downstream.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `git diff --check`
- `test -f codex/skills/references/mobile-first-ui.md`
- `rg -n "end-user UI|min-width|PC/tablet|no retrofit|Backward compatibility" codex/skills/references/mobile-first-ui.md codex/skills/ywc-plan/references/spec-template.md codex/skills/ywc-project-scaffold/SKILL.md`

## Out of Scope
Do not modify executor skills, custom agents, eval scripts, generated plugin files, Claude Code files, or existing CSS.
