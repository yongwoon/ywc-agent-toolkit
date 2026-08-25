# 000004-020-infra-worktree-rollout - Manual Test Plan

## Preconditions

- [ ] `000004-010-infra-parallel-docker-hooks` is merged.
- [ ] Worktree-related skill files have been updated.

## Test Scenarios

### Scenario 1: keep-branch is contract-level and script-level

**Steps:**
1. Run `rg -n -- "--keep-branch" codex/skills/ywc-worktrees/SKILL.md codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh`.
2. Inspect the cleanup script path safety and dirty worktree checks.

**Expected Result:**
- Both skill contract and cleanup script contain `--keep-branch`.
- Existing safety checks remain present.

### Scenario 2: sequential worktree state is explicit

**Steps:**
1. Run `rg -n -- "--worktree|worktree-run.md|--state-file" codex/skills/ywc-sequential-executor`.
2. Inspect `resume-state.py` behavior for multiple preserved worktree state files.

**Expected Result:**
- Worktree mode is documented across SKILL, README, reference, and scripts.
- Multiple state files return `NEEDS_CONTEXT` rather than guessing.

### Scenario 3: finish-branch supports path-scoped delivery

**Steps:**
1. Run `rg -n -- "--worktree-path|Worktree-path mode|git -C <path>" codex/skills/ywc-finish-branch/SKILL.md`.
2. Inspect merge, post-merge verification, Mark Task Complete, and cleanup sections.

**Expected Result:**
- `--worktree-path` mode is documented with path-scoped command guidance.
