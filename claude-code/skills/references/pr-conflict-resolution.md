# PR Conflict & Merge-Readiness Resolution — Shared Reference

Used by `ywc-create-pr`, `ywc-handle-pr-reviews`, `ywc-finish-branch`, and
`ywc-parallel-executor` (`--per-task-pr`) to detect and resolve the two distinct
ways a PR becomes unmergeable. The detection commands, the merge-not-rebase rule,
and the surface-vs-auto-resolve boundary are identical across all callers; only
the *entry point* differs (after PR creation, after review fixes, before merge,
or per-task in a wave).

## Two Distinct Conflict Situations

Do not confuse these — they have different causes and different fixes.

| Situation | Cause | Symptom | Fix |
|---|---|---|---|
| **Feature-branch push rejection** | The **remote feature branch** advanced (a teammate pushed, or a prior push you did not pull) | `git push` rejected as `non-fast-forward` | `git pull --rebase origin <feature-branch>` (rebase onto the *same* branch is safe here — you own those commits), then re-push. Never force-push without explicit user approval. |
| **PR-vs-base conflict** | The **base branch** advanced and now textually conflicts with the PR | `gh pr view --json mergeable` returns `CONFLICTING`; `gh pr merge` fails | Merge base into the feature branch (procedure below). This is the common gap — CI can be green while the PR is unmergeable. |

A PR that **passed CI** can still be **unmergeable** against the base. CI status
and merge-readiness are two independent gates. Checking only CI and then calling
`gh pr merge` is the most common reason a "green" PR fails to merge.

## Merge-Readiness Check

Query GitHub's computed merge state. Run this after creating/updating a PR, after
pushing review fixes, and immediately before any merge attempt:

```bash
gh pr view <pr-number> --json mergeable,mergeStateStatus \
  --jq '{mergeable, mergeStateStatus}'
```

| `mergeable` | Meaning | Action |
|---|---|---|
| `MERGEABLE` | No conflict with base | Proceed (still honor `mergeStateStatus` below) |
| `CONFLICTING` | Textual conflict with base | Run [Update Branch From Base](#update-branch-from-base) |
| `UNKNOWN` | GitHub is still computing the merge | Poll briefly, then re-read — see [UNKNOWN handling](#unknown-handling) |

`mergeStateStatus` refines the merge gate even when `mergeable` is `MERGEABLE`:

| `mergeStateStatus` | Meaning | Action |
|---|---|---|
| `CLEAN` | Ready to merge | Proceed to merge |
| `BEHIND` | Branch is out of date; branch protection requires up-to-date before merge | Update branch from base (no conflict — fast catch-up), then re-verify CI |
| `BLOCKED` | A required check or review is missing (not a conflict) | Resolve the missing gate (CI, required review) — do not treat as a conflict |
| `DIRTY` | Conflict present | Run [Update Branch From Base](#update-branch-from-base) |
| `UNKNOWN` | Still computing | Poll briefly (see below) |

### UNKNOWN handling

GitHub computes mergeability asynchronously. Right after a push, `mergeable` is
often `UNKNOWN` for a few seconds. Poll in a **single Bash call** using the
`until` pattern (a standalone `sleep N && gh ...` is blocked by Claude Code's
PreToolUse hook):

```bash
# Run this ENTIRE block as a SINGLE Bash call.
MERGEABLE=UNKNOWN
TRIES=0
until [ "$MERGEABLE" != "UNKNOWN" ] || [ "$TRIES" -ge 5 ]; do
  sleep 5
  MERGEABLE=$(gh pr view <pr-number> --json mergeable --jq .mergeable)
  TRIES=$((TRIES + 1))
done
echo "mergeable=$MERGEABLE"
```

If it is still `UNKNOWN` after the window, treat it as `CONFLICTING` and run the
update procedure — updating against an up-to-date base is harmless when there is
in fact no conflict (the merge becomes a fast no-op).

## Update Branch From Base

When the PR conflicts with (or is behind) the base, bring the base into the
feature branch by **merging**, not rebasing:

```bash
git fetch origin <base-branch>
git checkout feature/<task-name>          # skip if the branch is in a worktree — use git -C <worktree>
git merge --no-ff origin/<base-branch> -m "Merge origin/<base-branch> into feature/<task-name>"
```

**Why merge, not rebase:** rebasing rewrites the feature branch's commit SHAs,
which **orphans every existing PR review thread** (GitHub anchors comments to
SHAs) and forces a `--force` push. Merging preserves SHAs and review history and
needs only a normal push. This mirrors the `git merge --no-ff` philosophy used at
the final base merge.

### Outcome A — merge succeeds (no real conflict)

The branch was merely out of date. Push and re-verify CI:

```bash
git push origin feature/<task-name>
```

The new merge commit triggers a fresh CI run. **Re-verify CI** before merging —
the previous green result is stale. Treat the update + CI re-gate as one unit;
the merge gate is only satisfied when `mergeable == MERGEABLE` **and** CI is green
on the new head SHA.

### Outcome B — merge reports conflicts (real textual conflict)

These need human judgment. **Do not auto-resolve, do not force-push, do not
`git merge --abort`** — an abort discards the working state the user needs to
inspect the conflict.

1. List the conflicting files: `git diff --name-only --diff-filter=U`.
2. Surface to the user: the PR URL, the base branch, the conflicting file list,
   and a one-line description of why the base advanced (e.g. "a sibling task
   merged into `<base>` first").
3. Stop with status `BLOCKED`. The feature branch and the in-progress merge are
   left intact so the user can resolve manually.

Real textual conflicts are a **1-attempt** situation: surface immediately. Do not
loop. This is the conflict analogue of the CI fix loop's "design decision →
BLOCKED" exit — a conflict that git cannot auto-merge requires a human to choose
the correct resolution.

## Attempt Budget Summary

| Conflict type | Auto-resolve? | Budget |
|---|---|---|
| `BEHIND` / out-of-date, no textual conflict | Yes — merge base in, push, re-verify CI | Up to 2 update+CI cycles (matches the CI fix-loop budget) |
| `CONFLICTING` with real textual conflict | No — surface to user | 1 (surface immediately, `BLOCKED`) |
| Feature-branch push rejection (non-fast-forward) | `git pull --rebase` on the feature branch only | 1 retry, then surface if it still fails |

## Worktree Note (parallel executor)

When the feature branch lives in a worktree (`ywc-parallel-executor`), run the
update from the worktree with `git -C ../worktree-<task-name> merge ...` and
`git -C ../worktree-<task-name> push ...` rather than `git checkout`. The main
checkout stays on the base branch. This is exactly the branch-refresh step the
`--per-task-pr` flow already performs; this reference is its canonical definition.
