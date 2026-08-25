# 000021-010-infra-codex-eval-sync-validation

## Purpose

Run the final Codex source/generated sync and validation hard gate for the evaluation quality improvement cycle.

## Scope

- Run plugin sync after any `codex/skills/**` source edits.
- Run repository validation, Codex install list checks, Codex agent install list checks, and evaluator CI.
- Inspect final diff scope for forbidden paths and generated plugin consistency.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-eval-quality-improvement-cycle.md`
- `codex/AGENTS.md`
- `AGENTS.md`

### Summary

Implements AC6, AC7, AC8, and FR-6. This is a phase hard gate and must wait for all Phase `000020` tasks.

### Out of Scope

- New feature edits beyond fixes required to make validation pass.
- Manual edits to generated plugin output before running sync.
- Editing `.claude/**`, `claude-code/**`, or product code.

## Dependencies

### Depends On

- `000020-010-docs-codex-eval-judgment-report`
- `000020-020-docs-codex-eval-scoreboard-update`
- `000020-030-docs-runtime-fit-wording-polish`
- `000020-040-test-eval-fixture-coverage`
- `000020-050-docs-agent-behavioral-evidence`

### Depended By

- (None)

## Key Files

- `plugins/ywc-agent-toolkit/skills/**`
- `plugins/ywc-agent-toolkit/plugin.json`
- `docs/skill-agent-eval/codex/**`
- `codex/skills/**`
- `codex/agents/**`

## Parallel Execution Metadata

- **Ownership:** Final sync/validation commands and generated plugin output produced by `bash scripts/sync-codex-plugin.sh`.
- **Shared Surfaces:** Repository validation, generated Codex plugin package, Codex install metadata.
- **Conflicts With:** All implementation tasks until they merge.
- **Parallelizable After:** All Phase `000020` tasks are merged.
- **Task Verify:** See `task.md`.

## Notes

- This task may touch generated plugin files only by running `bash scripts/sync-codex-plugin.sh`.
- Existing dirty `.claude/**` files are unrelated user work and must not be reverted.
