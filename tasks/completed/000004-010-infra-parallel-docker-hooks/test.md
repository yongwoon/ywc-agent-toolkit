# 000004-010-infra-parallel-docker-hooks - Manual Test Plan

## Preconditions

- [ ] `000003-010-infra-docker-isolate-package` is merged.
- [ ] `codex/skills/ywc-parallel-executor/SKILL.md` has been updated.

## Test Scenarios

### Scenario 1: audit hook runs before worktree creation

**Steps:**
1. Inspect `codex/skills/ywc-parallel-executor/SKILL.md`.
2. Locate selected task resolution, pre-flight checks, and Step 4a.
3. Confirm `ywc-docker-isolate --mode audit` appears before worktree creation.

**Expected Result:**
- Audit is documented before any worktree is created.
- Existing `ywc-worktrees --mode audit` behavior remains present.

### Scenario 2: setup uses resolved worktree path

**Steps:**
1. Inspect Step 4a in `codex/skills/ywc-parallel-executor/SKILL.md`.
2. Confirm Docker setup runs after resolved worktree path capture.

**Expected Result:**
- Setup uses the path returned by `ywc-worktrees`, not a guessed path.

### Scenario 3: teardown is successful-task scoped

**Steps:**
1. Inspect Step 4g in `codex/skills/ywc-parallel-executor/SKILL.md`.
2. Confirm teardown is run before prune only for delivered tasks.

**Expected Result:**
- BLOCKED or preserved worktrees skip teardown.
- Teardown failure is reported without rolling back a delivered task.
