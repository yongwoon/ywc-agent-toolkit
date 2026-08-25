# 000025-040-docs-mission-brainstorm-plan-integration

## Purpose
Wire the mission-persistence consumers: `ywc-brainstorm` offers to persist its anchors to the mission file on handoff, and `ywc-plan` reads the mission file in Step 1 to frame clarification and seed Acceptance Criteria.

## Scope
- `ywc-brainstorm` Step 6 Handoff: after the four-anchor block, offer (opt-in) `ywc-project-mission update` persisting Mission (What+Why) and Success Criteria (Done When). Declining is a clean no-op. Add a `requires`/Integration note + one RD row.
- `ywc-plan` Step 1: read `docs/project-mission.md` when present (alongside the existing `docs/ubiquitous-language.md` read); absence is a clean no-op. Add the opt-in Step 5 write-back offer when ≥1 new durable success criterion is finalized (AC14, OQ1=opt-in).

## Spec Reference
### Primary Sources
- `docs/ywc-plans/tier2-harness-feedback-and-mission-persistence.md` — FR5, FR6, AC8/AC9/AC14; Existing Constraints (`ywc-brainstorm/SKILL.md:135-146`, `ywc-plan/SKILL.md:73/101`); Iteration 1 Amendments (four anchors named; "finalizes" defined; OQ1=opt-in).
### Summary
Best-effort, opt-in integration mirroring how ywc-plan already reads ubiquitous-language. No behavior blocks on the mission file's absence.
### Out of Scope (from spec)
Creating the ywc-project-mission skill (000025-020); catalog/CLAUDE.md.

## Criticality
normal — skill-instruction edits; no security surface.

## Dependencies
### Depends On
- `000025-020-docs-project-mission-skill` — provides the skill + `docs/project-mission.md` format to call.
### Depended By
- `000026-010-docs-catalog-claude-md-integration` — documents the two new mission edges.

## Key Files
- `claude-code/skills/ywc-brainstorm/SKILL.md` (+ README locale set if user-facing)
- `claude-code/skills/ywc-plan/SKILL.md` (+ README locale set if user-facing)

## Notes
- NFR2 no-block invariant: absence of the mission file must never block planning/handoff.
- "finalizes" (AC14 trigger) = plan reaches Step 5 handoff with ≥1 new durable success criterion not already in the mission file.

## Out of Scope
Skill creation; review-learnings; catalog.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-brainstorm/**`, `claude-code/skills/ywc-plan/**`
- **Shared Surfaces**: consumes the `docs/project-mission.md` format (read-only dependency on 000025-020).
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000025-020`. May run concurrently with `000025-030`.
- **Task Verify**: `bash scripts/validate.sh`
