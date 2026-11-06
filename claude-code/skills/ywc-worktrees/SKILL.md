---
name: ywc-worktrees
description: >-
  (ywc) Use when creating, auditing, pruning, or resolving the worktree
  location for an isolated workspace — delegated from `ywc-parallel-executor`
  (creation, Pre-flight audit) and `ywc-finish-branch` (post-merge prune),
  standalone for one-off use. Triggers: "worktree 생성", "worktree 정리",
  "worktree 위치 확정", "ワークツリー作成", "ワークツリー監査", "create worktree",
  "audit worktrees", "prune worktrees", "ywc-worktrees". Do not use for
  branch creation/deletion alone (use `git checkout -b` / `git branch -d`),
  PR creation (`ywc-create-pr`), CI/merge/Mark-Complete delivery
  (`ywc-finish-branch`), task-level orchestration (`ywc-sequential-executor`
  / `ywc-parallel-executor`), or non-git workspace isolation (e.g. Docker
  volumes).
---

# ywc-worktrees

**Announce at start:** "I'm using the ywc-worktrees skill to manage the git worktree lifecycle for an isolated workspace."

Single source of truth for git worktree priority resolution, creation,
audit, and pruning. Extracted from `ywc-parallel-executor` so the same
discipline is callable from any skill that needs worktree isolation
(parallel-executor's per-task worktrees, finish-branch's post-merge
cleanup, ad-hoc developer use). Pattern inspiration: superpowers
`using-git-worktrees` skill, adapted to this project's self-contained
runtime policy — referenced for design intent only, never dispatched at
runtime.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Worktree location does not matter — drop it next to the repo" | Worktree path is a contract. Callers and audit tooling expect `.worktrees/<task-name>` or the project's documented `worktree_root`. Inventing a sibling path breaks every downstream cleanup that scans the documented location. |
| "`git worktree prune` is enough — skip the audit step" | `prune` removes only stale metadata for worktrees whose directories are gone. It does **not** report worktrees whose directories still exist but were never claimed by any task. Audit catches both classes; prune alone hides drift. |
| "If a worktree path already exists, just reuse it" | A pre-existing path means either a prior run did not clean up (drift) or another task is currently using it (collision). Reuse silently corrupts whichever party is touching the path. Always treat existing paths as an error, not a hint. |
| "The caller passed `--mode create` so the resolution step is decided — skip the audit" | Pre-flight audit is mandatory before any new worktree creation. Stale metadata from a previous run causes the new `git worktree add` to fail with a confusing "already registered" error; the audit + prune catches this before the user-visible failure. |
| "Worktree priority is overhead — the caller knows where it wants to go" | The priority chain (`.worktrees/` > CLAUDE.md `worktree_root` > `--root` fallback) exists so that a project can pin a worktree location once (in its CLAUDE.md) and have every skill respect it. Callers that bypass the chain silently fragment worktree locations across the project. |

**Violating the letter of these rules is violating the spirit.** A stale worktree from yesterday's run is the most common cause of "the new run is broken for no reason" in parallel-executor.

## Arguments

| Parameter | Format | Example | Description |
|---|---|---|---|
| `--mode` | `<mode>` | `--mode create` | One of `create`, `audit`, `prune`, `resolve`. See [Modes](#modes). |
| `--task-name` | `<task-name>` | `--task-name yk-000001-010-db-create-users` | The task this worktree belongs to. Required for `create` and `prune`; optional for `audit`. |
| `--branch` | `<branch-name>` | `--branch feature/yk-000001-010-db-create-users` | The branch to associate with the worktree. Required for `create`; optional for `prune` (defaults to `feature/<task-name>`). |
| `--base-branch` | `<branch-name>` | `--base-branch develop` | The starting point for the new branch. Required for `create` unless `--existing-branch` is set (no default). Mutually exclusive with `--existing-branch`. |
| `--existing-branch` | flag | | (Create only) Check out the branch named by `--branch` instead of creating a new one: a local branch as-is, or a branch that exists only on `origin` as a new tracking branch. Replaces `--base-branch`; passing both is a usage error. |
| `--root` | `<path>` | `--root .worktrees` | Fallback worktree root when the project has neither `.worktrees/` nor `CLAUDE.md` `worktree_root`. Project-level configuration wins over this value. |
| `--expect` | `<task1,task2,...>` | `--expect yk-000001-010,yk-000001-020` | (Audit only) Comma-separated list of task names that should currently have a worktree. Any extra or missing worktree fails the audit. |
| `--force` | flag | | (Prune only) Pass `--force` to `git worktree remove` even if the worktree is dirty. Use only when the caller has confirmed the worktree's contents are disposable. |
| `--keep-branch` | flag | | (Prune only) Remove the worktree and prune stale metadata, but **skip** the local branch deletion (`git branch -d`) and its verification. Same semantics as `ywc-finish-branch --keep-branch`: use when the branch must survive the worktree teardown (e.g. an integration branch a caller will later raise a trunk PR from). |

**Task and branch names are used verbatim**, so an `[INITIALS]` segment passes through unchanged: `yk-000001-010-db-create-users` and the legacy unprefixed `000001-010-db-create-users` are both valid `--task-name` values, and `feature/yk-000001-010-db-create-users` is a valid git ref requiring no special handling.

## Modes

| Mode | Reads | Writes | Use case |
|---|---|---|---|
| `resolve` | `.worktrees/` presence, CLAUDE.md `worktree_root`, `--root` | nothing | Caller wants to know where a worktree would land before committing to create. Returns the resolved path on stdout. |
| `create` | resolved root + `--task-name` + `--branch` + (`--base-branch` or `--existing-branch`) | `git worktree add` | Per-task worktree creation. Called by `ywc-parallel-executor` Step 4 for each in-wave task. |
| `audit` | resolved root contents + `--expect` (optional) | nothing (read-only) | Pre-flight or wave-end audit. Reports stale, leaked, or unexpected worktrees. |
| `prune` | resolved root + `--task-name` + optional `--branch` + optional `--keep-branch` | `git worktree remove` + local branch delete (skipped when `--keep-branch`) + `git worktree prune` | Post-merge cleanup. Called by `ywc-finish-branch` Step 5/8 and `ywc-parallel-executor` Step 4g. `--keep-branch` preserves the branch (e.g. `ywc-sequential-executor --worktree` non-aggregate teardown). |

Modes are mutually exclusive — `--mode` takes exactly one value. The caller chooses the mode based on the lifecycle stage; this skill does not infer.

## Priority Resolution

The worktree root is resolved by walking the following chain in order; the first match wins:

1. **`.worktrees/` directory present in repo root** — if the directory exists (even empty), it is the worktree root. This is the recommended pattern: a project commits an empty `.worktrees/.gitkeep` to make the location explicit and discoverable.
2. **CLAUDE.md `worktree_root` directive** — if `CLAUDE.md` contains a line matching `worktree_root: <path>`, that path is the root. Allows projects to pin a location outside the repo (e.g., a sibling `../<repo>-worktrees/`) without requiring an in-repo directory.
3. **`--root <path>` fallback** — used only when neither `.worktrees/` nor `CLAUDE.md` declares a project-level root. This lets callers pass an explicit location without overriding project policy.
4. **Project-relative `../` fallback** — if none of the above match, fall back to `../worktree-<task-name>` (the legacy parallel-executor convention). A warning is logged: the project should adopt `.worktrees/` or the CLAUDE.md directive to make this explicit.

The resolved path is recorded in the caller's payload and re-derived (not stored) on every invocation, so a mid-run change to CLAUDE.md or `.worktrees/` presence takes effect on the next call.

## Execution

### `--mode resolve`

1. Walk the priority chain above.
2. Print the resolved root path to stdout.
3. Exit 0 on success; exit 1 if `--root` was provided but is not a writable directory.

No side effects. Safe to call from `--dry-run` paths in upstream skills.

### `--mode create`

1. Run `--mode resolve` internally to get the worktree root.
2. Verify the target path `<root>/<task-name>` does not already exist. If it does, exit 1 with a descriptive error — never overwrite.
3. Add the worktree. `--base-branch` and `--existing-branch` are mutually exclusive: passing both exits 1 with a `mutually exclusive` usage error, and passing neither is also a usage error (exit 1). This procedure is prose, so a usage error exits 1, unlike the bundled scripts' exit 2 convention.
   - Without `--existing-branch`: run `git worktree add <resolved-path> -b <branch> <base-branch>`.
   - With `--existing-branch`, validate `<branch>` first, in this order. (1) Without interpolating it into any shell command (hold it in a variable or check it in-process; never line-oriented `grep -E`, where `$` matches per line), it must match `^[A-Za-z0-9._/-]+$` over the whole string, must not start with `-`, and must not contain `..`. (2) Only after (1) passes, `git check-ref-format "refs/heads/<branch>"` must succeed — it is itself a shell call. On any failure exit 1 with `invalid branch name` **before** running `ls-remote`, `fetch`, or `worktree add`. The allowlist is the shell-metacharacter boundary (a double-quoted `$(…)` or backtick still executes when the caller pastes `<branch>` literally), so branch names that git accepts but that contain `+`, `@`, `#`, or `~` are rejected on purpose. Then quote every branch argument:
     1. `git show-ref --verify --quiet "refs/heads/<branch>"` succeeds (local branch) → `git worktree add "<resolved-path>" "<branch>"`.
     2. Otherwise run `git ls-remote --exit-code origin "refs/heads/<branch>"` (the full ref avoids tail matches such as `x/<branch>`). Exit 2 → exit 1 with `branch <branch> not found locally or on origin`. Any other non-zero exit (network, authentication) → print git's stderr as-is and exit 1; never report it as "not found".
     3. If the branch exists on `origin`, run `git fetch origin "+refs/heads/<branch>:refs/remotes/origin/<branch>"` (the explicit refspec also works in single-branch clones). On failure print git's stderr and exit 1. Then run `git worktree add --track -b "<branch>" "<resolved-path>" "refs/remotes/origin/<branch>"` (the full ref avoids a same-named local tag).
4. Verify the worktree was registered: `git worktree list --porcelain | grep <resolved-path>` returns a row.
5. Print the resolved worktree path on stdout for the caller to capture.
6. Exit 0 on success.

Error handling: if `git worktree add` fails (locked, branch already exists elsewhere, etc.), surface the exact git error and exit 1. This includes `--existing-branch` when the branch is already checked out in another worktree — deciding whether to reuse that worktree is the caller's job. Never retry; the caller decides whether the failure is recoverable.

### `--mode audit`

1. Run `--mode resolve` to get the worktree root.
2. Run the bundled `scripts/audit-worktrees.sh` against the resolved root. The script reports:
   - **Clean** — no stale metadata, no unexpected worktrees, every `--expect` task has a worktree.
   - **Drift** — `git worktree list` rows whose directories no longer exist (stale metadata) OR directories under the root whose paths are not in `git worktree list`. Both cases fail the audit.
   - **Missing** — when `--expect` is provided, tasks in the expect list that do not have a worktree. Fails the audit.
   - **Leaked** — when `--expect` is provided, worktrees that exist but are not in the expect list. Fails the audit (a previous task was not cleaned up).
3. Exit 0 if clean; exit 1 with the categorized findings on stdout if not.

### `--mode prune`

1. Run `--mode resolve` to get the worktree root.
2. Run the bundled `scripts/cleanup-worktree.sh` against the resolved task worktree path. The script:
   - Verifies the path is under the resolved root (refuses to operate on paths outside).
   - Runs `git worktree remove <path>` (or `--force` if `--force` was passed).
   - Deletes the local branch with `git branch -d <branch>` (default `feature/<task-name>`) after the worktree is released — **unless `--keep-branch` is set**, in which case the branch deletion and its verification are skipped. The branch name is treated as a git ref (it may legitimately contain `/`, e.g. `integration/run-<slug>` or `work/<name>`); only `--task-name`, which forms a path component, is allowlisted to `^[A-Za-z0-9_-]+$`.
   - If the target branch does not exist (e.g. an `--aggregate-pr` integration branch already merged and deleted by its final PR), the deletion step is idempotent — it logs and continues rather than failing.
   - Runs `git worktree prune` to clear any stale metadata.
   - Verifies the path is gone, the metadata row is removed, and (when `--keep-branch` is not set) the local branch no longer exists.
3. Exit 0 if cleanup verified; exit 1 with details on stdout if any step failed.

The script refuses to operate on dirty worktrees unless `--force` is set — this is the discipline that catches accidental deletion of work in progress.

## Integration

- **upstream** — `ywc-parallel-executor` (Pre-flight `--mode audit`, Step 4 per-task `--mode create`, Step 4g `--mode prune`); `ywc-finish-branch` (Step 5/8 cleanup `--mode prune` when called from a parallel-executor context).
- **downstream** — none; this skill is a leaf operation. Callers consume its exit code and stdout.
- **bundled scripts** — `scripts/audit-worktrees.sh` (audit), `scripts/cleanup-worktree.sh` (prune + local branch deletion). Both moved here from `ywc-parallel-executor/scripts/` via `git mv`, preserving history.

## Design Source

Adapted from the superpowers `using-git-worktrees` skill. The priority resolution chain (`.worktrees/` > CLAUDE.md > `--root` > fallback) and the four-mode interface (`create` / `audit` / `prune` / `resolve`) follow that pattern. This project's self-contained runtime policy means the superpowers skill is **not** dispatched at runtime — it is a design reference for the pattern shape only, and this file is the project-owned implementation.

## Notes

This skill is the single source for worktree lifecycle. Callers must not re-implement worktree creation or pruning inline; doing so fragments the priority resolution chain and the audit / prune discipline. If a caller needs a worktree operation not covered by the four modes, extend this skill rather than work around it.
