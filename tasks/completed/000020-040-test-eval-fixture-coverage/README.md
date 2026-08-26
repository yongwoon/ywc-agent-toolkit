# 000020-040-test-eval-fixture-coverage

## Purpose

Improve objective eval fixture coverage for selected S5=3 Codex skills without adding low-signal prompt restatements.

## Scope

- Review S5=3 candidates from the 2026-06-18 report.
- Prioritize:
  - `codex/skills/ywc-spec-ready/evals/evals.json`
  - `codex/skills/ywc-verify-done/evals/evals.json`
  - `codex/skills/ywc-finish-branch/evals/evals.json`
  - `codex/skills/ywc-agentic/evals/evals.json`
  - `codex/skills/ywc-brainstorm/evals/evals.json`
- Add objective fixtures where the expected output/behavior can be verified without a model judge.
- Record omission reasons in the report if a candidate is not suitable this cycle.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-eval-quality-improvement-cycle.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- Existing `codex/skills/*/evals/evals.json` conventions

### Summary

Implements AC4 and FR-4. This task improves test evidence where objective fixtures are possible and avoids weak evals where they are not.

### Out of Scope

- Changing evaluator rubric/scorer behavior.
- Adding model-judge-only evals.
- Editing `.claude/**`, `claude-code/**`, generated plugin files manually, or unrelated skill instructions.

## Dependencies

### Depends On

- `000020-010-docs-codex-eval-judgment-report`

### Depended By

- `000021-010-infra-codex-eval-sync-validation`

## Key Files

- `codex/skills/ywc-spec-ready/evals/evals.json`
- `codex/skills/ywc-verify-done/evals/evals.json`
- `codex/skills/ywc-finish-branch/evals/evals.json`
- `codex/skills/ywc-agentic/evals/evals.json`
- `codex/skills/ywc-brainstorm/evals/evals.json`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md` (omission reasons only)

## Parallel Execution Metadata

- **Ownership:** Listed `evals/evals.json` files and omission-reason notes in the 2026-06-18 report.
- **Shared Surfaces:** Codex eval fixture schema and final generated plugin sync surface.
- **Conflicts With:** Any task editing the same eval files; report edits conflict with `000020-010` until it merges.
- **Parallelizable After:** `000020-010-docs-codex-eval-judgment-report`
- **Task Verify:** See `task.md`.

## Notes

- If a skill has no objective fixture candidate, leave the score unchanged and document the reason rather than adding a shallow eval.
