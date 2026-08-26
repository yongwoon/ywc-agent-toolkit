# 000025-030-docs-rootcause-postmortem-prevention-emit

## Purpose
Wire the harness-feedback consumers: `ywc-debug-rootcause` and `ywc-incident-postmortem` emit a systemic-prevention proposal that routes into `ywc-review-learnings` via the new `--source debug|incident` values.

## Scope
- `ywc-debug-rootcause`: add **Phase 4 §6 — Systemic Prevention (emit)** AFTER §3 (red-green-red verification), independent of the §5 architecture branch. Recurring-class vs one-off; if recurring, offer `ywc-review-learnings --mode update --source debug`; if one-off, print `No systemic learning warranted — one-off cause`. Update the Phase 4 exit condition. Add one RD row wired to §6.
- `ywc-incident-postmortem`: in **Step 6 Prevention Action Items**, tag recurrence-preventing vs operational; recurrence-preventing items route to `ywc-review-learnings --mode update --source incident`; operational items stay in the report only.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/tier2-harness-feedback-and-mission-persistence.md` — FR1, FR2, AC1/AC2/AC3/AC13; Existing Constraints (`ywc-debug-rootcause/SKILL.md:118-135`, `ywc-incident-postmortem/SKILL.md:90`); Iteration 1 Amendments (FR1 §6 insertion pin).
### Summary
The skills already find root causes; this task adds the promotion step so a recurring class becomes a durable learning. Insertion pinned: §6 after §3, NOT after §5.
### Out of Scope (from spec)
The `--source` enum extension itself (000025-010); editing review-learnings; catalog/CLAUDE.md.

## Criticality
normal — skill-instruction edits; incident-postmortem may handle security incidents but this task adds only a routing step, no security logic.

## Dependencies
### Depends On
- `000025-010-docs-review-learnings-prevention-sources` — provides `--source debug|incident`.
### Depended By
- `000026-010-docs-catalog-claude-md-integration` — documents the two new harness-feedback edges.

## Key Files
- `claude-code/skills/ywc-debug-rootcause/SKILL.md` (+ README locale set if user-facing)
- `claude-code/skills/ywc-incident-postmortem/SKILL.md` (+ README locale set if user-facing)

## Notes
- AC2 requires the explicit one-off line. AC13 requires operational items to be explicitly retained, not promoted.

## Out of Scope
review-learnings edits; new skill; catalog.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-debug-rootcause/**`, `claude-code/skills/ywc-incident-postmortem/**`
- **Shared Surfaces**: consumes the `ywc-review-learnings --source` contract (read-only dependency).
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000025-010`. May run concurrently with `000025-040`.
- **Task Verify**: `bash scripts/validate.sh`
