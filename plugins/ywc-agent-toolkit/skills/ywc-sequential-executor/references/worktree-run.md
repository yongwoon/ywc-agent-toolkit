# Worktree Run - `ywc-sequential-executor --worktree`

`--worktree` is an execution-location flag, not a delivery mode. It wraps one
sequential invocation in a single run-level worktree while preserving the normal
task loop, verification, delivery, and dependency rules.

## Identity

Derive these names before task execution:

| Field | Rule |
|---|---|
| `run_slug` | `--group-name` when present; otherwise a sanitized explicit range; otherwise `auto-<timestamp>` for auto-detect. |
| `run_task_name` | `run-<run_slug>`, using only characters accepted by `ywc-worktrees`. |
| `integration_branch` | Non-aggregate trunk base: `integration/<run_task_name>`. Non-aggregate feature/integration base: reuse the supplied base branch. `--aggregate-pr`: use the aggregate work branch. |
| `start_point` | The real base branch or user-supplied `--base-branch` used to create the run worktree. |
| `$WT` | The first resolved path returned by `ywc-worktrees --mode create`. |

If the derived integration branch already exists and no resumable state ties it
to this invocation, return `NEEDS_CONTEXT`; never overwrite it.

## Creation

Non-resume `--worktree` runs perform this once before task resolution mutates
anything:

```bash
$ywc-worktrees --mode audit
$ywc-worktrees --mode create \
  --task-name <run_task_name> \
  --branch <integration_branch> \
  --base-branch <start_point>
```

Capture stdout as `$WT`, verify it appears in `git worktree list --porcelain`,
then initialize `$WT/.ywc-run-state.json`.

Dry-run mode must not create the worktree, branch, or state file. It prints the
planned `$WT`, `integration_branch`, `start_point`, and state path only.

## Redirection Rules

When `--worktree` is active, every mutating or verification action is scoped to
`$WT`.

- Git commands use `git -C "$WT" ...`.
- File edits target files under the absolute `$WT` path, never the main checkout.
- Verification commands run in one shell call as `cd "$WT" && <command>`.
- `ywc-finish-branch` is invoked from `$WT` or with an equivalent `git -C "$WT"`
  wrapper.
- `verify-transition.sh` runs after delivery against the integration branch state
  visible from `$WT`; do not validate against a stale main checkout.

Spec and task files may be read from the project root for planning, but any
implementation write belongs in `$WT`.

## Delivery Semantics

Delivery mode behavior is unchanged except for the target branch:

| Mode | Target in `--worktree` |
|---|---|
| normal PR | Per-task PR targets `integration_branch`; final integration-to-trunk PR is out of scope. |
| `--local-merge` | Per-task local merge targets `integration_branch`. |
| `--draft` | Draft PR targets `integration_branch`; task remains incomplete. |
| `--skip-ci-wait` | Ready/open PR targets `integration_branch`; task remains incomplete. |
| `--aggregate-pr` | `$WT` uses the aggregate work branch and the final work -> base PR lifecycle remains mandatory. |

## State And Resume

Root state remains the default when `--worktree` is absent. With `--worktree`,
write state to `$WT/.ywc-run-state.json` and include:

```json
{
  "worktree_mode": true,
  "worktree_path": "<absolute $WT path>",
  "integration_branch": "<branch>",
  "start_point": "<base or branch>",
  "run_task_name": "run-<slug>"
}
```

Resume Detection order:

1. Check project root `.ywc-run-state.json`.
2. If absent, enumerate `git worktree list --porcelain`.
3. Read each `<worktree>/.ywc-run-state.json`.
4. Apply executor, age, branch, completed-task, and intent-match validation.
5. If multiple candidates match, return `NEEDS_CONTEXT` with the candidate paths.

## Cleanup

For `DONE`:

1. Remove `$WT/.ywc-run-state.json`.
2. For non-aggregate modes, prune with branch preservation:
   ```bash
   $ywc-worktrees --mode prune \
     --task-name <run_task_name> \
     --branch <integration_branch> \
     --keep-branch
   ```
3. Verify `$WT` and git worktree metadata are gone, while `integration_branch`
   still exists.

For `--aggregate-pr`, prune only after the final work -> base PR is merged and
local base is synced. The local work branch may be deleted by the aggregate
cleanup path.

For `BLOCKED`, `NEEDS_CONTEXT`, or correctness-level `DONE_WITH_CONCERNS`,
preserve `$WT`, `$WT/.ywc-run-state.json`, `integration_branch`, and the current
feature branch. The Completion Report must include `$WT`, `integration_branch`,
and the resume command.
