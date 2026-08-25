# 000004-010-infra-parallel-docker-hooks

## Purpose

`ywc-docker-isolate` package를 `ywc-parallel-executor` workflow에 연결한다. 이 task는 pre-flight audit, per-task setup, successful-task teardown hook을 추가하면서 현재 repository의 `ywc-worktrees` delegation을 유지한다.

## Scope

- `codex/skills/ywc-parallel-executor/SKILL.md`에 Docker isolation hook 3개 추가
- 필요한 경우 `codex/skills/ywc-parallel-executor/README*.md`에 user-facing Docker isolation behavior 반영
- 기존 `ywc-worktrees --mode create`, `audit`, `prune` delegation 유지
- source PR의 direct `tools/codex-skill/.../cleanup-worktree.sh` style로 회귀하지 않도록 방지

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-2-integrate-docker-isolation-with-parallel-execution` - hook 위치와 behavior
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac3---parallel-executor-docker-hooks-are-present` - hook acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac4---parallel-executor-keeps-worktrees-delegation` - worktree delegation guardrail

### Summary

Parallel executor는 worktree lifecycle을 이미 `ywc-worktrees`에 위임하고 있다. Docker isolation은 그 lifecycle을 대체하지 않고 selected task audit, resolved worktree path setup, successful-task teardown으로 감싸야 한다. BLOCKED 또는 preserved worktree는 teardown을 skip해야 한다.

### Out of Scope (from spec)

- `ywc-docker-isolate` package 생성 - handled by `000003-010-infra-docker-isolate-package`
- PR #129 sequential worktree rollout과 parallel-executor granularity note - handled by `000004-020-infra-worktree-rollout`
- `.codex-plugin` sync와 catalog update - handled by `000005-010-infra-codex-package-validation`

## Dependencies

### Depends On

- `000003-010-infra-docker-isolate-package` - provides the skill and scripts being invoked

### Depended By

- `000004-020-infra-worktree-rollout` - may also touch `ywc-parallel-executor/SKILL.md`; this task should land first to reduce conflicts
- `000005-010-infra-codex-package-validation` - final validation checks the integrated package

## Key Files

- `codex/skills/ywc-parallel-executor/SKILL.md` - hook integration points
- `codex/skills/ywc-parallel-executor/README.md` - Korean user-facing update if needed
- `codex/skills/ywc-parallel-executor/README.en.md` - English source update if needed
- `codex/skills/ywc-parallel-executor/README.ja.md` - Japanese update if needed
- `codex/skills/ywc-parallel-executor/README.ko.md` - Korean locale update if needed

## Notes

- Hook commands should prefer skill-call form: `ywc-docker-isolate --mode audit|setup|teardown`.
- Setup must run only after `ywc-worktrees --mode create` has produced a resolved worktree path.
- Teardown failure after successful task delivery should be reported as `LEAKED_DOCKER_STACK`, not used to roll back a delivered task.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/README*.md`

### Shared Surfaces

- Parallel executor workflow contract
- Worktree lifecycle delegation contract
- Docker stack lifecycle behavior

### Conflicts With

- `000004-020-infra-worktree-rollout` - both tasks can modify `codex/skills/ywc-parallel-executor/SKILL.md`

### Parallelizable After

- `000003-010-infra-docker-isolate-package`

### Task Verify

- `rg -n "ywc-docker-isolate --mode (audit|setup|teardown)" codex/skills/ywc-parallel-executor/SKILL.md`
- `rg -n "ywc-worktrees --mode (create|audit|prune)" codex/skills/ywc-parallel-executor/SKILL.md`
- `rg -n 'tools/codex-skill' codex/skills/ywc-parallel-executor/SKILL.md && exit 1 || true`

## Out of Scope

- Modifying `ywc-worktrees` implementation
- Running `.codex-plugin` sync
- Changing sequential executor behavior
