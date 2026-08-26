# 000020-030-docs-runtime-fit-wording-polish

## Purpose

Polish high-value S7=3 Codex skills so their instructions fit the Codex runtime cleanly without changing their behavior.

## Scope

- Review the fresh S7=3 list from the 2026-06-18 report.
- Prioritize these skills unless the report proves they are no longer relevant:
  - `codex/skills/ywc-plan/SKILL.md`
  - `codex/skills/ywc-code-gen/SKILL.md`
  - `codex/skills/ywc-finish-branch/SKILL.md`
  - `codex/skills/ywc-refactor-clean/SKILL.md`
  - `codex/skills/ywc-tdd-ritual/SKILL.md`
- Rewrite ambiguous slash invocation, workspace-specific paths, and Claude-only phrasing into Codex-native wording.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-eval-quality-improvement-cycle.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/skill-rubric.md`

### Summary

Implements AC3 and FR-3. This is wording-only unless fresh score evidence proves a real behavioral gap.

### Out of Scope

- Rewriting skill workflow logic.
- Adding dependencies, scripts, new skills, or new agents.
- Editing `.claude/**`, `claude-code/**`, generated plugin files manually, or evaluator scripts.

## Dependencies

### Depends On

- `000020-010-docs-codex-eval-judgment-report`

### Depended By

- `000021-010-infra-codex-eval-sync-validation`

## Key Files

- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-code-gen/SKILL.md`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-refactor-clean/SKILL.md`
- `codex/skills/ywc-tdd-ritual/SKILL.md`

## Parallel Execution Metadata

- **Ownership:** The listed `codex/skills/<skill>/SKILL.md` files only.
- **Shared Surfaces:** Codex skill instruction wording and generated plugin sync surface.
- **Conflicts With:** Any task editing the same `SKILL.md` files.
- **Parallelizable After:** `000020-010-docs-codex-eval-judgment-report`
- **Task Verify:** See `task.md`.

## Notes

- Do not remove useful examples merely because they contain command-like syntax; rewrite examples only when they are runtime-inaccurate for Codex.
