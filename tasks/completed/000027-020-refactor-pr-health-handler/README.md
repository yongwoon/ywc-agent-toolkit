# 000027-020-refactor-pr-health-handler

## Purpose
`ywc-handle-pr-reviews`를 comments-only handler에서 PR health sweep으로 확장한다.

## Scope
- `fetch-unresolved-comments.sh` runtime reference를 `fetch-pr-review-artifacts.sh`로 대체하거나 supersede한다.
- Helper script가 review artifacts, status check rollup, merge readiness를 normalized JSON으로 emit하게 한다.
- `SKILL.md`가 empty review artifact array에서도 CI와 merge-readiness를 확인하도록 갱신한다.
- `agents/openai.yaml` display metadata와 default prompt를 PR health sweep에 맞춘다.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/develop-with-llm-pr132-133-134-140-codex-port.md#fr-2-port-pr-133-ywc-handle-pr-reviews-pr-health-sweep`

### Summary
PR review comments가 없더라도 failed CI와 merge blockers가 남아 있으면 handler가 끝나면 안 된다. Helper script와 skill instructions를 함께 바꿔 review artifacts, CI status, merge-readiness를 하나의 PR health sweep으로 만든다. Comment-like artifact에만 marker-based reply를 유지하고 status/merge artifact에는 reply를 만들지 않는다.

### Out of Scope (from spec)
- Executor call-site lifecycle 변경은 `000027-030-refactor-executor-health-sweeps`에서 처리한다.
- Generated plugin sync는 `000028-010-infra-plugin-sync-validation`에서 처리한다.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000027-030-refactor-executor-health-sweeps` — executor가 canonical PR health sweep으로 이 handler를 호출한다.
- `000028-010-infra-plugin-sync-validation` — helper executable bit와 generated plugin freshness를 검증한다.

## Key Files
- `codex/skills/ywc-handle-pr-reviews/SKILL.md`
- `codex/skills/ywc-handle-pr-reviews/agents/openai.yaml`
- `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- `codex/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh`

## Notes
Helper script must use portable Bash with `set -euo pipefail`. API/gh failures should exit `3`; usage errors should use a separate nonzero code.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-handle-pr-reviews/**`

### Shared Surfaces
- PR health artifact schema
- GitHub CLI usage contract
- Handler summary output contract

### Conflicts With
- `000027-030-refactor-executor-health-sweeps` — it depends on the handler's final invocation contract.

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- `test -x codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- `rg -n "review artifacts, CI status, and merge-readiness|fetch-pr-review-artifacts|merge_readiness|status_check" codex/skills/ywc-handle-pr-reviews`
- `rg -n "fetch-unresolved-comments" codex/skills/ywc-handle-pr-reviews`

## Out of Scope
- Changing executor PR polling loops
- Posting replies for CI or merge-readiness artifacts
- Any `claude-code/**` port
