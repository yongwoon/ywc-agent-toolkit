# 000004-010-infra-parallel-docker-hooks - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000003-010-infra-docker-isolate-package` is completed and merged.
- [ ] `codex/skills/ywc-docker-isolate/SKILL.md` documents audit, setup, and teardown modes.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-parallel-executor/SKILL.md` and `codex/skills/ywc-parallel-executor/README*.md`.
- [ ] Do not edit `codex/skills/ywc-worktrees/**` or `codex/skills/ywc-docker-isolate/**` in this task.

## Stop Conditions

- [ ] Stop if adding a hook requires replacing `ywc-worktrees --mode create`, `audit`, or `prune`.
- [ ] Stop if hook placement is ambiguous because current line numbers differ materially from the spec's cited behavior.
- [ ] Stop if source PR text introduces `tools/codex-skill` runtime paths.

## Implementation Steps

- [ ] Add pre-flight Docker audit.
  - [ ] Locate the point after selected task names are known and before worktree creation.
  - [ ] Document `ywc-docker-isolate --mode audit` with all selected task names.
  - [ ] Specify that non-empty stdout without `--prune` aborts with remediation guidance.
- [ ] Add post-create Docker setup.
  - [ ] Locate Step 4a after `ywc-worktrees --mode create` and mechanical path verification.
  - [ ] Use the resolved worktree path returned by `ywc-worktrees`.
  - [ ] Document failure reporting without replacing worktree creation.
- [ ] Add pre-prune Docker teardown.
  - [ ] Locate Step 4g before `ywc-worktrees --mode prune`.
  - [ ] Run teardown only for tasks whose Step 4e delivery completed.
  - [ ] Skip teardown for BLOCKED or preserved worktrees.
- [ ] Update parallel-executor README locale files if the Docker behavior is user-facing.
  - [ ] Mention Docker port isolation in Korean default README if needed.
  - [ ] Keep translated locale files aligned with the changed behavior.
- [ ] Verify delegation remains intact.
  - [ ] Confirm `ywc-worktrees --mode create` remains present.
  - [ ] Confirm `ywc-worktrees --mode audit` remains present.
  - [ ] Confirm `ywc-worktrees --mode prune` remains present.

## Task Verify

- [ ] `rg -n "ywc-docker-isolate --mode (audit|setup|teardown)" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n "ywc-worktrees --mode (create|audit|prune)" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n 'tools/codex-skill' codex/skills/ywc-parallel-executor/SKILL.md && exit 1 || true`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`
