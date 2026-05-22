---
name: ywc-worktrees
description: >-
  (ywc) Use when creating, auditing, pruning, or resolving the worktree
  location for an isolated workspace — primarily as a delegated callable
  from `ywc-parallel-executor` (per-task worktree creation in Step 4 and
  audit in Pre-flight) and `ywc-finish-branch` (post-merge prune in the
  cleanup step), but also available standalone for one-off worktree
  operations. Triggers: "worktree 생성", "worktree audit", "worktree 정리",
  "worktree prune", "ywc-worktrees", "ywc worktrees", "worktree 경로 결정",
  "worktree 위치 확정", "git worktree 정리", "ワークツリー作成",
  "ワークツリー監査", "create worktree", "audit worktrees", "prune worktrees".
  Do not use for branch creation alone (use `git checkout -b` directly via
  the caller), branch deletion alone (use `git branch -d` via the caller),
  PR creation (`ywc-create-pr`), CI / merge / Mark-Complete delivery
  (`ywc-finish-branch`), task-level orchestration
  (`ywc-sequential-executor` / `ywc-parallel-executor`), or any non-git
  workspace isolation pattern (e.g. Docker volumes).
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
| `--task-name` | `<task-name>` | `--task-name 000001-010-db-create-users` | The task this worktree belongs to. Required for `create` and `prune`; optional for `audit`. |
| `--branch` | `<branch-name>` | `--branch feature/000001-010-db-create-users` | The branch to associate with the worktree. Required for `create`; optional for `prune` (defaults to `feature/<task-name>`). |
| `--base-branch` | `<branch-name>` | `--base-branch develop` | The starting point for the new branch. Required for `create` (no default). |
| `--root` | `<path>` | `--root .worktrees` | Fallback worktree root when the project has neither `.worktrees/` nor `CLAUDE.md` `worktree_root`. Project-level configuration wins over this value. |
| `--expect` | `<task1,task2,...>` | `--expect 000001-010,000001-020` | (Audit only) Comma-separated list of task names that should currently have a worktree. Any extra or missing worktree fails the audit. |
| `--force` | flag | | (Prune only) Pass `--force` to `git worktree remove` even if the worktree is dirty. Use only when the caller has confirmed the worktree's contents are disposable. |

## Modes

| Mode | Reads | Writes | Use case |
|---|---|---|---|
| `resolve` | `.worktrees/` presence, CLAUDE.md `worktree_root`, `--root` | nothing | Caller wants to know where a worktree would land before committing to create. Returns the resolved path on stdout. |
| `create` | resolved root + `--task-name` + `--branch` + `--base-branch` | `git worktree add` | Per-task worktree creation. Called by `ywc-parallel-executor` Step 4 for each in-wave task. |
| `audit` | resolved root contents + `--expect` (optional) | nothing (read-only) | Pre-flight or wave-end audit. Reports stale, leaked, or unexpected worktrees. |
| `prune` | resolved root + `--task-name` + optional `--branch` | `git worktree remove` + local branch delete + `git worktree prune` | Post-merge cleanup. Called by `ywc-finish-branch` Step 5/8 and `ywc-parallel-executor` Step 4g. |

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
3. Run `git worktree add <resolved-path> -b <branch> <base-branch>`.
4. Verify the worktree was registered: `git worktree list --porcelain | grep <resolved-path>` returns a row.
5. Print the resolved worktree path on stdout for the caller to capture.
6. Exit 0 on success.

Error handling: if `git worktree add` fails (locked, branch already exists elsewhere, etc.), surface the exact git error and exit 1. Never retry; the caller decides whether the failure is recoverable.

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
   - Deletes the local branch with `git branch -d <branch>` (default `feature/<task-name>`) after the worktree is released.
   - Runs `git worktree prune` to clear any stale metadata.
   - Verifies the path is gone, the metadata row is removed, and the local branch no longer exists.
3. Exit 0 if cleanup verified; exit 1 with details on stdout if any step failed.

The script refuses to operate on dirty worktrees unless `--force` is set — this is the discipline that catches accidental deletion of work in progress.

## Integration

- **upstream** — `ywc-parallel-executor` (Pre-flight `--mode audit`, Step 4 per-task `--mode create`, Step 4g `--mode prune`); `ywc-finish-branch` (Step 5/8 cleanup `--mode prune` when called from a parallel-executor context).
- **downstream** — none; this skill is a leaf operation. Callers consume its exit code and stdout.
- **bundled scripts** — `scripts/audit-worktrees.sh` (audit), `scripts/cleanup-worktree.sh` (prune + local branch deletion). These are centralized here so callers do not keep divergent worktree audit or cleanup logic.

## Design Source

Adapted from the superpowers `using-git-worktrees` skill. The priority resolution chain (`.worktrees/` > CLAUDE.md > `--root` > fallback) and the four-mode interface (`create` / `audit` / `prune` / `resolve`) follow that pattern. This project's self-contained runtime policy means the superpowers skill is **not** dispatched at runtime — it is a design reference for the pattern shape only, and this file is the project-owned implementation.

## Notes

This skill is the single source for worktree lifecycle. Callers must not re-implement worktree creation or pruning inline; doing so fragments the priority resolution chain and the audit / prune discipline. If a caller needs a worktree operation not covered by the four modes, extend this skill rather than work around it.
