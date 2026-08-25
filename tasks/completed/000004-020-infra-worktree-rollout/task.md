# 000004-020-infra-worktree-rollout - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000004-010-infra-parallel-docker-hooks` is completed and merged.
- [ ] Current `ywc-worktrees` create/audit/prune delegation remains present in `ywc-parallel-executor`.

## Allowed Edit Scope

- [ ] Stay within declared Ownership in `README.md`.
- [ ] Do not edit `codex/skills/ywc-docker-isolate/**`, `codex/skills/ywc-spec-ready/**`, or `.codex-plugin/**`.
- [ ] If source PR requires changes outside worktree-related skills, stop and report.

## Stop Conditions

- [ ] Stop if cleanup changes weaken unsafe path or dirty worktree refusal behavior.
- [ ] Stop if sequential resume behavior would guess between multiple preserved state files.
- [ ] Stop if implementing `--worktree-path` requires changing `ywc-create-pr` or unrelated delivery skills.

## Implementation Steps

- [ ] Extend `ywc-worktrees`.
  - [ ] Add `--keep-branch` to `codex/skills/ywc-worktrees/SKILL.md`.
  - [ ] Update prune-mode output contract, validation checklist, and common mistakes text.
  - [ ] Add `--keep-branch` parsing and branch-preservation verification to `scripts/cleanup-worktree.sh`.
  - [ ] Add or port `scripts/test-cleanup-worktree.sh` regression coverage.
- [ ] Add sequential run-level worktree behavior.
  - [ ] Add `--worktree` argument and dry-run output fields in `codex/skills/ywc-sequential-executor/SKILL.md`.
  - [ ] Add pre-flight worktree setup pointer and `$WT`-scoped execution guidance.
  - [ ] Add completion report fields for worktree mode.
  - [ ] Add `references/worktree-run.md`.
  - [ ] Update `references/checkpoint-resume.md` for root-state and worktree-state behavior.
- [ ] Update sequential state scripts.
  - [ ] Add `--state-file` support to `scripts/inspect-state.py`.
  - [ ] Update `scripts/resume-state.py` to discover preserved worktree state files.
  - [ ] Ensure multiple preserved state files return `NEEDS_CONTEXT` instead of guessing.
  - [ ] Add `scripts/test-worktree-state.py`.
- [ ] Extend finish-branch for worktree delivery.
  - [ ] Add `--worktree-path <path>` argument documentation.
  - [ ] Add a `Worktree-path mode` section.
  - [ ] Document `git -C <path>` notes for relevant merge, verification, and cleanup steps.
- [ ] Update worktree-related docs and evals.
  - [ ] Update README locale files for `ywc-worktrees`, `ywc-sequential-executor`, and `ywc-finish-branch`.
  - [ ] Add or port the worktree-mode eval case in `codex/skills/ywc-sequential-executor/evals/evals.json` if schema-compatible.
  - [ ] Add the PR #129 sequential-vs-parallel worktree granularity note to `ywc-parallel-executor/SKILL.md`.

## Task Verify

- [ ] `rg -n -- "--keep-branch" codex/skills/ywc-worktrees/SKILL.md codex/skills/ywc-worktrees/scripts/cleanup-worktree.sh`
- [ ] `bash -n codex/skills/ywc-worktrees/scripts/*.sh`
- [ ] `python3 -m py_compile codex/skills/ywc-sequential-executor/scripts/inspect-state.py codex/skills/ywc-sequential-executor/scripts/resume-state.py codex/skills/ywc-sequential-executor/scripts/test-worktree-state.py`
- [ ] `rg -n -- "--worktree|worktree-run.md" codex/skills/ywc-sequential-executor`
- [ ] `rg -n -- "--worktree-path|Worktree-path mode|git -C <path>" codex/skills/ywc-finish-branch/SKILL.md`

## Verification

- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`
