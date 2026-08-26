# Task: 000025-040-docs-mission-brainstorm-plan-integration

## Prerequisites
- [ ] `000025-020` merged — `ywc-project-mission` skill + `docs/project-mission.md` format exist.

## Allowed Edit Scope
`claude-code/skills/ywc-brainstorm/**` and `claude-code/skills/ywc-plan/**` only.

## Stop Conditions
- Stop and report if making the mission read mandatory would violate NFR2 (must stay best-effort / no-op on absence).
- Stop if a skill body would exceed 500 lines.

## Implementation Steps
- [ ] In `ywc-brainstorm/SKILL.md` Step 6 Handoff, add an opt-in offer to persist Mission (What+Why) + Success Criteria (Done When) via `ywc-project-mission update`; declining = no-op. Add an Integration note + one RD row.
- [ ] In `ywc-plan/SKILL.md` Step 1, add a best-effort read of `docs/project-mission.md` alongside the existing ubiquitous-language read; absence = no-op.
- [ ] In `ywc-plan/SKILL.md` Step 5, add the opt-in write-back offer (AC14) when ≥1 new durable success criterion is finalized; define "finalizes" inline.
- [ ] Update both skills' Integration sections to name the ywc-project-mission edges.
- [ ] Update README locale sets only where user-facing behavior is documented.

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `grep -n "project-mission" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-brainstorm/SKILL.md` shows both integrations.
- [ ] Both SKILL.md bodies ≤500 lines.

## Verification
- [ ] `bash scripts/validate.sh` passes.
