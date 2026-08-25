# 000020-020-docs-codex-eval-scoreboard-update

## Purpose

Update the Codex eval scoreboard to reflect the 2026-06-18 judgment report without inventing score movement.

## Scope

- Update `docs/skill-agent-eval/codex/scoreboard.md`.
- Preserve existing `Current`, `Previous`, `Trend`, and `Last evaluated` semantics.
- Mark `up` only when the 2026-06-18 report supports an actual score change; otherwise use `same`.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-eval-quality-improvement-cycle.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- `docs/skill-agent-eval/codex/scoreboard.md`

### Summary

Implements AC2 and FR-2. This task depends on the new report because the scoreboard is a summary of judged evidence, not a place to perform first-pass scoring.

### Out of Scope

- Editing the full sweep report except for typo fixes that do not change scoring semantics.
- Editing Codex skills, agents, generated plugin output, `.claude/**`, or `claude-code/**`.

## Dependencies

### Depends On

- `000020-010-docs-codex-eval-judgment-report`

### Depended By

- `000021-010-infra-codex-eval-sync-validation`

## Key Files

- `docs/skill-agent-eval/codex/scoreboard.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md` (read-only input)

## Parallel Execution Metadata

- **Ownership:** `docs/skill-agent-eval/codex/scoreboard.md`
- **Shared Surfaces:** Codex eval score/trend semantics.
- **Conflicts With:** Other scoreboard update tasks.
- **Parallelizable After:** `000020-010-docs-codex-eval-judgment-report`
- **Task Verify:** See `task.md`.

## Notes

- Recent Karpathy integration candidates include `ywc-code-gen`, `ywc-task-generator`, `ywc-skill-author`, and Codex custom agents, but score movement must be evidence-backed.
