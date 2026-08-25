# 000027-030-refactor-executor-health-sweeps

## Purpose
Sequential and parallel executor PR lifecycle 문서를 `ywc-handle-pr-reviews` 기반 PR health sweep으로 맞춘다.

## Scope
- `ywc-parallel-executor` draft / aggregate / per-task PR flow에서 handler를 health sweep으로 호출하게 한다.
- `ywc-sequential-executor` draft mode와 range PR guidance에서 동일한 health sweep rule을 적용한다.
- Sequential executor long-range compaction guidance를 durable state 기준으로 추가한다.
- 관련 aggregate / branch lifecycle references를 갱신한다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-3-port-pr-133-executor-pr-health-call-sites`
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-6-port-pr-134-agent-context-and-long-run-compaction-guidance`

### Summary
Executor는 bot review comment count를 PR health의 proxy로 취급하면 안 된다. PR handler가 review, CI, merge-readiness를 모두 보게 된 뒤에는 executor가 comment 유무와 관계없이 health sweep을 호출해야 한다. Sequential executor는 긴 range 실행에서 `.ywc-run-state.json`과 task artifacts를 durable source of truth로 취급하는 compaction rule도 가져야 한다.

### Out of Scope (from spec)
- Handler helper script 구현은 `000027-020-refactor-pr-health-handler`에서 처리한다.
- `ywc-agentic` compaction guidance는 `000027-040-refactor-agent-context-compaction`에서 처리한다.
- Plugin sync는 `000028-010-infra-plugin-sync-validation`에서 처리한다.

## Dependencies

### Depends On
- `000027-020-refactor-pr-health-handler` — canonical handler contract와 helper name을 제공한다.

### Depended By
- `000028-010-infra-plugin-sync-validation` — updated executor docs를 generated plugin package에 sync한다.

## Key Files
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/references/aggregate-pr.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/references/aggregate-pr.md`
- `codex/skills/ywc-sequential-executor/references/branch-lifecycle.md`

## Notes
Preserve existing merge-not-rebase guidance. Do not treat `BOT_COUNT == 0` as a terminal success condition.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-sequential-executor/**`

### Shared Surfaces
- PR lifecycle contract
- Aggregate PR guidance
- Sequential executor state / compaction guidance

### Conflicts With
- `000027-020-refactor-pr-health-handler` — handler contract must land first.

### Parallelizable After
- `000027-020-refactor-pr-health-handler`

### Task Verify
- `rg -n "health sweep|regardless of BOT_COUNT|BOT_COUNT == 0|merge-readiness|CI status" codex/skills/ywc-parallel-executor codex/skills/ywc-sequential-executor`
- `rg -n "one-line task status|\\.ywc-run-state\\.json|durable source of truth|compaction" codex/skills/ywc-sequential-executor`

## Out of Scope
- Editing `ywc-handle-pr-reviews`
- Editing `ywc-agentic`
- Generated plugin sync
