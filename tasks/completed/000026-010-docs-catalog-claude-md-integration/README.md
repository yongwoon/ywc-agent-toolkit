# 000026-010-docs-catalog-claude-md-integration

## Purpose
Finalize Tier 2 by registering the new skill and the four new integration edges in the catalog and the skills-directory conventions doc (FR7 / AC11).

## Scope
- `claude-code/skills/README.md` catalog: add `ywc-project-mission`.
- `claude-code/skills/CLAUDE.md`: add `docs/project-mission.md` to the stateful-file family description; document the four new cross-skill edges.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/tier2-harness-feedback-and-mission-persistence.md` — FR7, AC11; Iteration 1 Amendments §"Enumerated integration edges" (authoritative four-edge list, superseding AC11's "two").
### Summary
Pure registration/documentation task; runs last because it references all skills created/edited in phase 000025.
### Out of Scope (from spec)
Any skill behavior change; codex bundle catalog.

## Criticality
normal — documentation only.

## Dependencies
### Depends On
- `000025-010`, `000025-020`, `000025-030`, `000025-040` — all referenced skills must exist/be edited first.
### Depended By
- (None) — terminal task.

## Key Files
- `claude-code/skills/README.md`
- `claude-code/skills/CLAUDE.md`

## Notes
- The four edges: (1) ywc-debug-rootcause → ywc-review-learnings (`--source debug`); (2) ywc-incident-postmortem → ywc-review-learnings (`--source incident`); (3) ywc-brainstorm → ywc-project-mission (handoff persist); (4) ywc-plan ← ywc-project-mission (Step 1 read).

## Out of Scope
Skill behavior; prior-task logic.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/README.md`, `claude-code/skills/CLAUDE.md`
- **Shared Surfaces**: the catalog + conventions doc (touched only here — that is why this is terminal).
- **Conflicts With**: (None identified) — must run AFTER all phase 000025 tasks (hard phase gate).
- **Parallelizable After**: all of phase 000025 merged.
- **Task Verify**: `bash scripts/validate.sh`
