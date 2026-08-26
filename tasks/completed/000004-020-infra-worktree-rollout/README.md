# 000004-020-infra-worktree-rollout

## Purpose

PR #129의 Codex sequential worktree rollout을 현재 repository의 worktree architecture에 맞게 port한다. 이 task는 `ywc-worktrees --keep-branch`, `ywc-sequential-executor --worktree`, state script support, `ywc-finish-branch --worktree-path`, references, tests/evals를 하나의 LLM-sized vertical slice로 처리한다.

## Scope

- `ywc-worktrees` contract와 cleanup script에 `--keep-branch` 추가
- `ywc-sequential-executor`에 run-level `--worktree` mode, reference doc, checkpoint/resume state support 추가
- `ywc-finish-branch`에 `--worktree-path <path>` mode 추가
- source worktree-mode test/eval 또는 repository schema에 맞는 equivalent regression coverage 추가
- README locale files에 user-facing behavior 반영
- `ywc-parallel-executor`의 sequential-vs-parallel worktree granularity note 추가

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-5-port-pr-129-worktree-rollout` - worktree rollout scope
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac9---worktrees-keep-branch-works-at-contract-level` - keep-branch acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac10---sequential-worktree-mode-is-documented` - sequential worktree mode acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac11---sequential-state-scripts-support-worktree-files` - state script acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac12---finish-branch-worktree-path-mode-is-documented` - finish-branch acceptance criteria

### Summary

Sequential executor needs a run-level worktree mode so a full sequential run can execute outside the repository root. Worktree cleanup must be able to preserve branches during this flow, and finish-branch must be able to operate against a specified worktree path. Current repository refinements, especially centralized `ywc-worktrees` lifecycle ownership, must be preserved.

### Out of Scope (from spec)

- Docker isolate package creation - handled by `000003-010-infra-docker-isolate-package`
- Initial parallel Docker hook integration - handled by `000004-010-infra-parallel-docker-hooks`
- Final catalog and `.codex-plugin` sync - handled by `000005-010-infra-codex-package-validation`

## Dependencies

### Depends On

- `000004-010-infra-parallel-docker-hooks` - establishes earlier `ywc-parallel-executor/SKILL.md` edits before adding PR #129's granularity note

### Depended By

- `000005-010-infra-codex-package-validation` - final validation compiles state scripts, checks README locale behavior, and syncs package copy

## Key Files

- `codex/skills/ywc-worktrees/SKILL.md`
- `codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh`
- `codex/skills/ywc-worktrees/scripts/test-cleanup-worktree.sh`
- `codex/skills/ywc-worktrees/README*.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/references/worktree-run.md`
- `codex/skills/ywc-sequential-executor/references/checkpoint-resume.md`
- `codex/skills/ywc-sequential-executor/scripts/inspect-state.py`
- `codex/skills/ywc-sequential-executor/scripts/resume-state.py`
- `codex/skills/ywc-sequential-executor/scripts/test-worktree-state.py`
- `codex/skills/ywc-sequential-executor/evals/evals.json`
- `codex/skills/ywc-sequential-executor/README*.md`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`

## Notes

- This task intentionally spans several worktree-related skills because the behavior is one rollout and the contracts must align.
- Preserve safety checks in `cleanup-worktree.sh`: unsafe path and dirty worktree refusal must not regress.
- If eval schema does not accept the source case directly, add equivalent coverage and document why.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-worktrees/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/README*.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`

### Shared Surfaces

- Git worktree lifecycle contract
- Sequential executor checkpoint/resume state contract
- Finish-branch delivery command contract
- Parallel executor worktree behavior note

### Conflicts With

- `000004-010-infra-parallel-docker-hooks` - both tasks modify `codex/skills/ywc-parallel-executor/SKILL.md`

### Parallelizable After

- `000004-010-infra-parallel-docker-hooks`

### Task Verify

- `rg -n -- "--keep-branch" codex/skills/ywc-worktrees/SKILL.md codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh`
- `bash -n codex/skills/ywc-worktrees/scripts/*.sh`
- `python3 -m py_compile codex/skills/ywc-sequential-executor/scripts/inspect-state.py codex/skills/ywc-sequential-executor/scripts/resume-state.py codex/skills/ywc-sequential-executor/scripts/test-worktree-state.py`
- `rg -n -- "--worktree|worktree-run.md" codex/skills/ywc-sequential-executor`
- `rg -n -- "--worktree-path|Worktree-path mode|git -C <path>" codex/skills/ywc-finish-branch/SKILL.md`

## Out of Scope

- Changing release metadata
- Replacing `ywc-worktrees` lifecycle with inline cleanup inside executors
- Adding new custom agents
