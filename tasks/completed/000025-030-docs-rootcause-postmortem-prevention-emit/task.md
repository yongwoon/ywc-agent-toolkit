# Task: 000025-030-docs-rootcause-postmortem-prevention-emit

## Prerequisites
- [ ] `000025-010` merged — `ywc-review-learnings --source debug|incident` exists.

## Allowed Edit Scope
`claude-code/skills/ywc-debug-rootcause/**` and `claude-code/skills/ywc-incident-postmortem/**` only.

## Stop Conditions
- Stop and report if the Phase 4 §6 insertion would conflict with the §5 architecture-stop branch (spec pins §6 after §3, independent of §5).
- Stop if a skill body would exceed 500 lines.

## Implementation Steps
- [ ] In `ywc-debug-rootcause/SKILL.md` Phase 4, add `§6 — Systemic Prevention (emit)` after §3: recurring-class rule; if yes → offer `ywc-review-learnings --mode update --source debug`; if no → print `No systemic learning warranted — one-off cause`.
- [ ] Update the Phase 4 exit condition to include the §6 emit decision.
- [ ] Add one Rationalization Defense row wired to §6 (ywc-skill-author B9).
- [ ] In `ywc-incident-postmortem/SKILL.md` Step 6, add recurrence-preventing vs operational tagging; route recurrence-preventing items to `ywc-review-learnings --mode update --source incident`; keep operational items in the report only.
- [ ] Update both skills' Integration sections to name the new edge.
- [ ] Update README locale sets only where user-facing behavior is documented.

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `grep -n "Systemic Prevention\|--source debug" claude-code/skills/ywc-debug-rootcause/SKILL.md` shows §6.
- [ ] `grep -n "--source incident\|recurrence-preventing" claude-code/skills/ywc-incident-postmortem/SKILL.md` shows the routing.
- [ ] Both SKILL.md bodies ≤500 lines.

## Verification
- [ ] `bash scripts/validate.sh` passes.
