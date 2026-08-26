# 000025-020-docs-project-mission-skill

## Purpose
Create the new `ywc-project-mission` skill that persists the project's durable Mission / Success Criteria / Out-of-Scope to `docs/project-mission.md`. Foundation for mission persistence. Mirrors the `ywc-review-learnings` stateful-file architecture (read/update/list/curate + user-confirmed writes).

## Scope
- New skill directory `claude-code/skills/ywc-project-mission/` authored via `ywc-skill-author` rules.
- Modes: `read` / `update` / `list` / `curate`.
- File `docs/project-mission.md` with sections **Mission / North-Star**, **Success Criteria** (table `ID | Criterion | Source | Added | Status`, `Added`=`YYYY-MM-DD`, `Source`=skill-provenance `brainstorm`/`plan`), **Out of Scope**, auto-maintained **Change Log**.
- `update` builds an ADD/MODIFY/DEPRECATE CHANGESET; writes only confirmed entries; idempotent (no-op on identical content); updates `<!-- updated: DATE -->`.
- On first file creation, print the `@docs/project-mission.md` CLAUDE.md activation prompt once (detect via file-exists, mirror review-learnings).

## Spec Reference
### Primary Sources
- `docs/ywc-plans/tier2-harness-feedback-and-mission-persistence.md` — FR4, FR7, AC5/AC6/AC7/AC10/AC15; Data Model (`docs/project-mission.md` format); Iteration 1 Amendments (date column, Source taxonomy, Change Log exemption, four-mode template = ywc-review-learnings).
### Summary
A per-project, committed, `@`-autoloaded mission file read by ywc-plan to frame planning. This task creates the skill + file format; consumer wiring is 000025-040.
### Out of Scope (from spec)
brainstorm/plan integration; catalog/CLAUDE.md; codex bundle.

## Criticality
normal — new skill operating on `docs/project-mission.md` under a confirmation gate; no security surface.

## Dependencies
### Depends On
- (root) — no predecessor.
### Depended By
- `000025-040-docs-mission-brainstorm-plan-integration` — needs the skill + file format to call.
- `000026-010-docs-catalog-claude-md-integration` — registers the new skill.

## Key Files
- `claude-code/skills/ywc-project-mission/SKILL.md`
- `claude-code/skills/ywc-project-mission/references/mission-format.md`
- `claude-code/skills/ywc-project-mission/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md`
- `claude-code/skills/ywc-project-mission/evals/evals.json`

## Notes
- Clone the four-mode `read/update/list/curate` shape from `ywc-review-learnings` (NOT ywc-ubiquitous-language, whose modes are new/extract/update).
- Body ≤500 lines — extract the full file-format spec to `references/mission-format.md`.
- Description: `(ywc) Use when ...` + KR/EN/JA triggers + `Do not use for ...` pointing at ywc-ubiquitous-language (vocabulary) and ywc-review-learnings (review prefs).

## Out of Scope
Consumer wiring; catalog/CLAUDE.md; any code outside the new skill dir.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-project-mission/**` (new directory).
- **Shared Surfaces**: the `docs/project-mission.md` file format (consumed by 000025-040); the skills catalog (updated in 000026-010).
- **Conflicts With**: (None identified)
- **Parallelizable After**: (root) — may run concurrently with `000025-010`.
- **Task Verify**: `bash scripts/validate.sh`
