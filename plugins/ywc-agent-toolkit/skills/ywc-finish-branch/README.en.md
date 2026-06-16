# ywc-finish-branch

A Codex Skill that delivers a Feature Branch to its Base Branch in a single call. It covers Mark-PR-ready, CI Wait + Bot Review Polling, Merge (PR or Local), Post-Merge Verification, Mark Task Complete, and Local Branch Cleanup.

## Overview

A single-responsibility extraction of the delivery logic that `ywc-sequential-executor` and `ywc-parallel-executor` previously inlined separately. Given one Feature Branch for one Task with passing verification, this Skill takes it the rest of the way to "done".

### Key features

- **Mode dispatch in one place**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Post-merge hard gate**: confirms the merge actually ran via `git log -1 --format="%s"`
- **Definition of Done enforced**: moves the task directory to `<tasks-dir>/completed/` with a verification gate
- **Bot review polling compatible**: `--bot-action sequential|parallel` matches the caller's CI strategy
- **Worktree-path mode**: `--worktree-path <path>` scopes delivery commands with `git -C <path>` for sequential run-level worktrees, while creation/removal stays with the caller

## Usage

### Default (PR-based)

```
/ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop
```

### Local Merge

```
/ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Range mode with deferred push

```
/ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### Worktree path mode

```
/ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
```

### Natural-language triggers

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## Mode comparison

| Mode | PR | CI wait | Merge | Mark Complete | Cleanup |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | yes (delegates to `ywc-create-pr`) | yes | `gh pr merge --delete-branch` | yes | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | yes | yes |
| `draft` | yes | no | no | no | no |
| `skip-ci-wait` | yes (mark ready) | no | no | no | no |
| `per-task-pr` | yes | no | no | no | no |

## Prerequisites

- `gh` CLI installed and authenticated (PR-based modes)
- Clean working tree
- Caller has already passed its verification gate (lint / typecheck / test)
- Pre-authorization configured in `Codex approval settings or the project-local policy file` (see `references/local-merge-permissions.md`)

## Tools used

`Bash`, `Read`, `Grep`, Task (delegates to `ywc-create-pr` / `ywc-handle-pr-reviews`)

## Integration

- **Upstream**: `ywc-sequential-executor` (replaces its Steps 5–8), `ywc-parallel-executor` (replaces the merge + mark-complete portion of Step 4e–4f)
- **Internal delegation**: `ywc-create-pr` (Step 2), `ywc-handle-pr-reviews` (Step 4 bot polling loop)
