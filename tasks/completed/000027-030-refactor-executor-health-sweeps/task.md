# 000027-030-refactor-executor-health-sweeps — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000027-020-refactor-pr-health-handler` is completed and merged.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-parallel-executor/**` and `codex/skills/ywc-sequential-executor/**`.

## Stop Conditions
- [ ] Stop if handler contract differs from the expected PR health sweep model.
- [ ] Stop if executor changes require modifying helper scripts or handler metadata.
- [ ] Stop if aggregate PR guidance conflicts with existing merge-not-rebase rules.

## Implementation Steps
- [ ] Update `codex/skills/ywc-parallel-executor/SKILL.md`.
  - [ ] In draft / aggregate / per-task PR flow, call `ywc-handle-pr-reviews` as a health sweep after bot polling.
  - [ ] State the sweep runs regardless of `BOT_COUNT == 0`.
  - [ ] Require rerunning CI and polling after handler-applied fixes.
- [ ] Update `codex/skills/ywc-parallel-executor/references/aggregate-pr.md`.
  - [ ] Mirror the aggregate PR lifecycle rule.
  - [ ] Preserve existing aggregate requirements.
- [ ] Update `codex/skills/ywc-sequential-executor/SKILL.md`.
  - [ ] Apply the same health sweep rule to draft mode and normal PR range guidance.
  - [ ] Add long-range compaction guidance using one-line task status digests.
  - [ ] Declare `.ywc-run-state.json` plus task artifacts as durable source of truth.
- [ ] Update `codex/skills/ywc-sequential-executor/references/aggregate-pr.md` and `references/branch-lifecycle.md`.
  - [ ] Mirror the PR health sweep rule.
  - [ ] Keep merge-not-rebase guidance unchanged.

## Task Verify
- [ ] `rg -n "health sweep|regardless of BOT_COUNT|BOT_COUNT == 0|merge-readiness|CI status" codex/skills/ywc-parallel-executor codex/skills/ywc-sequential-executor`
- [ ] `rg -n "one-line task status|\\.ywc-run-state\\.json|durable source of truth|compaction" codex/skills/ywc-sequential-executor`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains no `claude-code/**` or handler script paths.
