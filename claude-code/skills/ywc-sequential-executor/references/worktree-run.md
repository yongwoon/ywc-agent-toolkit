# Run-level Worktree mode (`--worktree`)

This reference holds the full lifecycle for `ywc-sequential-executor --worktree`. The SKILL.md body keeps only the Arguments row, two Rationalization Defense rows, and a one-line pointer here; everything procedural lives in this file.

## What `--worktree` does

`--worktree` runs the **entire range inside one git worktree** that is isolated from the main checkout, so the user can keep working in the original clone while the range executes. The isolation is **run-level**, not task-level: a single worktree wraps the whole run, and tasks still execute strictly sequentially inside it (this is the opposite of `ywc-parallel-executor`, which creates one worktree *per task*). Sequential's "each task's correctness depends on the previous task's stable state" guarantee is unchanged.

`--worktree` is an **independent flag**, orthogonal to the four delivery modes (`normal-pr` / `--local-merge` / `--draft` / `--aggregate-pr`) and to `--review` — it is **not** a fifth member of the mutual-exclusion group. It changes only the working directory the Execution Cycle runs in; each delivery mode keeps its exact meaning.

When `--worktree` is **unset**, behavior is byte-identical to today: no worktree is created and `.ywc-run-state.json` stays at the repo root (AC6).

## `$WT` redirection contract (§A1)

This skill is an LLM-driven markdown prompt; it does **not** rely on a persistent shell `cd`. In `--worktree` mode the run worktree's absolute path is captured as `$WT` and injected explicitly into every operation:

- **Every git command** in Steps 2 / 5 / 6 (and the Step 1 validations) runs as `git -C "$WT" …` — e.g. `git -C "$WT" checkout -b feature/<task>`.
- **Every Edit/Write tool call** in Step 3 targets an absolute path under `$WT`.
- **Step 4 test / lint / build** runs as `cd "$WT" && <cmd>` **inside a single Bash call** — never assume `cd` persists between Bash calls.
- **`ywc-finish-branch` (Step 5)** is invoked with `--worktree-path "$WT"`, and **`verify-transition.sh` (Step 6)** is run against the integration branch (the worktree's checkout).

"The only thing that differs is the working directory" is **this** mechanism — it does not license a "the skill cds on its own" interpretation.

## Naming and identifiers (§A4)

- **slug** — `--group-name` value if given; otherwise the range sanitized (`..` → `-`, e.g. `000024-010..000024-020` → `000024-010-000024-020`); a single task uses its task-name.
- **run worktree task-name** — `run-<slug>`. It passes the `^[A-Za-z0-9_-]+$` allowlist (`ywc-worktrees` enforces this on `--task-name` because it forms a path component). Worktree path = `<resolved-root>/run-<slug>`.
- **integration branch** — when `--base-branch` is a trunk, a new branch `integration/run-<slug>` is created. The `^[A-Za-z0-9_-]+$` allowlist applies **only** to `--task-name`, never to `--branch`, so the `/` in `integration/run-<slug>` is a valid git ref.

### Trunk detection (§A7 W8)

`--base-branch` is treated as a **trunk** (→ create a new `integration/run-<slug>`) when it matches `^(develop|main|master)$` **or** equals the CLAUDE.md base-branch directive. Otherwise it is treated as an **existing integration/feature branch** and used directly as the worktree's checkout (the user's established `feature/<slug>-base` workflow).

## Lifecycle

### 1. Pre-flight audit (non-resume runs only, §A7 W2 / FR-2.1)

Before creating the worktree, run `ywc-worktrees --mode audit --expect run-<slug>` (or compare against the state file's `worktree_path`) so a **preserved BLOCKED worktree from a prior run is not mis-flagged as Leaked**. This mirrors parallel-executor's Pre-flight audit discipline.

### 2. Create + `$WT` capture (§A1 / §B4 AC18)

```bash
ywc-worktrees --mode create --task-name run-<slug> --branch <integration-branch> --base-branch <start-point>
```

`ywc-worktrees --mode create` prints the resolved worktree absolute path on stdout (`ywc-worktrees/SKILL.md:98` — "Print the resolved worktree path on stdout for the caller to capture"). Capture that **bare path** (no extra text) as `$WT` and use it for all subsequent operations. If create fails because the path already exists (`ywc-worktrees` exits 1), **surface the error and stop** — never overwrite (FR-2.3 / Edge Cases). If the integration branch is already checked out in main or another worktree, `git worktree add` fails loud — surface and stop (FR-3.3).

The worktree root itself is resolved by `ywc-worktrees`'s priority chain (`.worktrees/` > CLAUDE.md `worktree_root` > `--root` > `../` fallback); this skill adds **no** new root argument (FR-1.2).

### 3. State file relocation + 2-stage Resume Detection (§A2)

In `--worktree` mode `.ywc-run-state.json` lives at **`$WT/.ywc-run-state.json`** (absolute-path Write/Read/rm) and records `worktree_path: "$WT"`. Resume Detection searches in order:

1. `<project-root>/.ywc-run-state.json` — a non-worktree run.
2. If absent, enumerate `git worktree list --porcelain` roots and look for `.ywc-run-state.json` in each; a file whose `worktree_path` still exists is a preserved run offered as a resume candidate.

The **Intent-match guard** is unchanged — a new range that does not match the saved run's `range` must not silently resume.

### 4. Execution Cycle inside the worktree

Run the normal Step 1 → Step 5 cycle per task, applying the `$WT` redirection contract above. Specifics:

- **Step 2 branch creation** branches each `feature/<task>` from the **integration branch** (the worktree's checkout), via `git -C "$WT" checkout -b feature/<task>`. The integration branch plays the role the base branch plays in non-worktree mode (FR-3.2).
- **`--draft` chain-branching** (§A7 W7) is done inside the worktree: `git -C "$WT" checkout feature/<previous-task>` — every checkout targets `$WT`'s HEAD, preserving position-sensitivity.
- **Step 5 delivery** invokes `ywc-finish-branch --worktree-path "$WT"` with `--base-branch <integration-branch>`. For `--aggregate-pr`, the `work/<name>` branch is carved **inside** the worktree and the final `work → base` PR is created from inside it too (FR-4.2).

### 5. HEAD invariant (§B3 AC17)

At the moment Step 5 runs, the run worktree's HEAD is on the **integration branch**. `ywc-finish-branch` (via `--worktree-path`) creates/merges `feature/<task>` and checks out the integration branch *before* deleting `feature/<task>`, so the per-task branch is never the worktree's current checkout when it is deleted, and the integration/base branch is never a deletion target. This is why per-task `feature/<task>` deletion succeeds inside the worktree without `--keep-branch`. Observable: `git -C "$WT" rev-parse --abbrev-ref HEAD` returns the integration branch both immediately before and after each task's Step 5.

### 6. DONE-time prune (§A3) — delivery-mode branch handling

Run state cleanup **before** prune (the state file lives in the worktree that prune removes): `rm -f "$WT/.ywc-run-state.json"`. Then prune only when the run's final Completion Status is `DONE`:

- **non-aggregate** (`normal-pr` / `--local-merge` / `--draft`):
  ```bash
  ywc-worktrees --mode prune --task-name run-<slug> --branch integration/run-<slug> --keep-branch
  ```
  The worktree is removed but the integration branch is **preserved** (`--keep-branch`) for the user's final integration→trunk PR.
- **`--aggregate-pr`**:
  ```bash
  ywc-worktrees --mode prune --task-name run-<slug> --branch work/<name>
  ```
  No `--keep-branch`: `work/<name>` was already merged and deleted by the final PR, so the branch delete is idempotent (the prune script logs and continues on a missing branch, FR-6.3).

Pass the resolved root via `--root` on prune/audit to prevent mid-run root drift (§A8 S2).

### 7. Non-DONE preserve (§A7 W3)

If the final Completion Status is **not** `DONE` (`DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`), **do not prune** — preserve the worktree and name its path in the Completion Report so a later resume can re-enter it. `DONE_WITH_CONCERNS` is preserved, not pruned (only `DONE` prunes).

## Dry-run (§A8 S1)

With `--dry-run`, do not create anything. Call `ywc-worktrees --mode resolve` (read-only) to compute and display the worktree path and the integration branch that *would* be created, then exit. Store the resolved `$WT` in the plan output.

## Completion Report addendum (§A7 W9)

For a **non-aggregate** `--worktree` run, the Completion Report must state that the integration branch is **unmerged to trunk** and guide the follow-up: open the final `integration/run-<slug> → <trunk>` PR with `ywc-create-pr` (this is intentionally not automated — orthogonality with `--aggregate-pr`, which *does* auto-create its work→base PR).

## Known consequence: Docker inside a worktree

A Docker stack started inside the worktree can collide with the host's existing dev stack on host ports. This is **out of scope** here (the host-isolation follow-up owns it); tasks run strictly sequentially, so *parallel* port contention does not arise. Surfaced as a known consequence, not a feature.

## Edge cases (from spec)

- **worktree path already exists** → `ywc-worktrees --mode create` exits 1; surface + stop, never overwrite.
- **integration branch already checked out** → `git worktree add` fails loud; surface + stop.
- **`--base-branch` is a trunk** → create a new `integration/run-<slug>`; never check the trunk itself into the worktree.
- **run interrupted (BLOCKED / DONE_WITH_CONCERNS)** → worktree preserved, prune skipped, path reported; resume re-enters the worktree.
- **stale worktree from a prior interrupted run** → the Pre-flight audit detects and (for genuinely leaked, non-preserved trees) cleans it; unresolved in-progress work is surfaced + stop.
