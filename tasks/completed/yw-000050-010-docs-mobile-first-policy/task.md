# yw-000050-010-docs-mobile-first-policy — Implementation Checklist

## Prerequisites
- [ ] Confirm the source specification is `docs/ywc-plans/20260918-codex-mobile-first-ui-default.md`.
- [ ] Confirm no architecture manifest was supplied for this docs-only change.

## Allowed Edit Scope
- [ ] Modify only the three Ownership surfaces declared in `README.md`.
- [ ] Stop and report if the policy requires framework-specific breakpoint values or legacy CSS changes.

## Stop Conditions
- [ ] Stop if wording would apply to admin/internal tools or unchanged legacy UI.
- [ ] Stop if the PC/tablet exception cannot be limited to otherwise in-scope end-user UI.
- [ ] Stop if a consumer needs a different rule than the shared reference.

## Hardening Gate
- [ ] Classify as docs-only.
- [ ] Named exception: source-contract and downstream evaluator checks replace RED-first production tests.
- [ ] Mark interface, data-integrity, and critical-review obligations as N/A for this docs-only task.

## Implementation Steps
- [ ] Create `codex/skills/references/mobile-first-ui.md` with Rule, Trigger, Escape hatch, and Backward compatibility sections.
  - Define narrowest-viewport base styles and outward `min-width` expansion.
  - Explicitly reject desktop-first `max-width` claw-back semantics.
  - State the end-user UI trigger, PC/tablet-only exception, and no-retrofit boundary.
- [ ] Update `codex/skills/ywc-plan/references/spec-template.md` so Medium/Large UI-touching plans record the policy or explicit exception.
- [ ] Update `codex/skills/ywc-project-scaffold/SKILL.md` with the conditional end-user UI note and exception requirement.
- [ ] Preserve existing non-UI, admin/internal, and legacy desktop-first guidance.

## Task Verify
- [ ] `git diff --check`
- [ ] `test -f codex/skills/references/mobile-first-ui.md`
- [ ] `rg -n "end-user UI|min-width|PC/tablet|no retrofit|Backward compatibility" codex/skills/references/mobile-first-ui.md codex/skills/ywc-plan/references/spec-template.md codex/skills/ywc-project-scaffold/SKILL.md`

## Verification
- [ ] lint passes (`N/A — repository has no separate Markdown lint command in AGENTS.md`)
- [ ] typecheck passes (`N/A — docs-only task`)
- [ ] unit tests pass (`N/A — docs-only task`)
- [ ] integration tests pass (`N/A — docs-only task`)
- [ ] app builds without error (`N/A — docs-only task`)

## Implementation Notes

