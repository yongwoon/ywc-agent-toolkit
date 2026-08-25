# Task: 000026-010-docs-catalog-claude-md-integration

## Prerequisites
- [ ] `000025-010`, `000025-020`, `000025-030`, `000025-040` all merged.

## Allowed Edit Scope
`claude-code/skills/README.md` and `claude-code/skills/CLAUDE.md` only.

## Stop Conditions
- Stop and report if any referenced skill from phase 000025 is missing (prerequisite not actually merged).

## Implementation Steps
- [ ] Add `ywc-project-mission` to the `claude-code/skills/README.md` catalog (description + one-line purpose, matching the catalog format).
- [ ] In `claude-code/skills/CLAUDE.md`, add `docs/project-mission.md` to the stateful-file family description (alongside review-learnings / ubiquitous-language).
- [ ] In `claude-code/skills/CLAUDE.md`, document the four new cross-skill edges.

## Task Verify
- [ ] `bash scripts/validate.sh` exits 0.
- [ ] `grep -n "ywc-project-mission" claude-code/skills/README.md claude-code/skills/CLAUDE.md` shows both registrations.

## Verification
- [ ] `bash scripts/validate.sh` passes.
