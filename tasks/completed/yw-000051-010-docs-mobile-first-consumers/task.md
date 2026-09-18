# yw-000051-010-docs-mobile-first-consumers — Implementation Checklist

## Prerequisites
- [ ] `yw-000050-010-docs-mobile-first-policy` is completed and merged.
- [ ] `codex/skills/references/mobile-first-ui.md` exists and defines the trigger and exception.

## Allowed Edit Scope
- [ ] Modify only the three consumer skill files in Ownership.
- [ ] Stop before editing the shared reference or eval runner.

## Stop Conditions
- [ ] Stop if a consumer would apply the rule to non-UI work, admin/internal tools, or unchanged legacy CSS.
- [ ] Stop if the consumer wording diverges from the shared reference.

## Hardening Gate
- [ ] Classify as docs-only behavior-contract work.
- [ ] Use downstream deterministic source checks as named replacement verification.
- [ ] Preserve the bounded interface contract and return `NEEDS_CONTEXT` on a policy mismatch.
- [ ] Mark data integrity and critical review as N/A.

## Implementation Steps
- [ ] Update `codex/skills/ywc-task-generator/SKILL.md` so `ui` layout/style tasks put mobile base layout before later `min-width` expansion.
  - Require an explicit exception statement for PC/tablet-only end-user surfaces.
  - Link the shared reference and preserve logic-only UI-task applicability boundaries.
- [ ] Update `codex/skills/ywc-sequential-executor/SKILL.md` with a conditional pre-implementation policy-reading directive.
  - Require mobile-first implementation order only for new end-user layout/style work.
  - Preserve no-retrofit behavior for legacy desktop-first UI.
- [ ] Update `codex/skills/ywc-parallel-executor/SKILL.md` at the worker prompt injection point.
  - Append the same conditional directive to frontend worker prompts.
  - Keep worker ownership, sandbox, and delivery contracts unchanged.

## Task Verify
- [ ] `git diff --check`
- [ ] `rg -n "mobile-first-ui|min-width|PC/tablet|end-user UI|legacy" codex/skills/ywc-task-generator/SKILL.md codex/skills/ywc-sequential-executor/SKILL.md codex/skills/ywc-parallel-executor/SKILL.md`

## Verification
- [ ] lint passes (`N/A — repository has no separate Markdown lint command in AGENTS.md`)
- [ ] typecheck passes (`N/A — documentation-only task`)
- [ ] unit tests pass (`N/A — deterministic contract test is downstream`)
- [ ] integration tests pass (`N/A — documentation-only task`)
- [ ] app builds without error (`N/A — documentation-only task`)

## Implementation Notes

