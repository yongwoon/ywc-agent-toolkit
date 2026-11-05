# PR worktree identity and preservation

Ported from `yongwoon/develop-with-llm` #347, frozen merge
`76200680f059d34d295b3f01da527c29ea782dc2`,
`tools/codex-skill/skills/ywc-handle-pr-reviews/SKILL.md`.

## Selection contract

1. Bind the invoking repository once as `REPOSITORY=owner/repo`, require `origin`
   to name that repository, and pin explicit positive `PR_NUMBER`. Use the bound
   repository in every `gh` command (`--repo` or full repository API path).
   Unverifiable repository ownership is `NEEDS_CONTEXT` before mutation.
2. Query the pinned number for `number,url,state,isCrossRepository,headRefName`.
   Require matching number, open state and `isCrossRepository=false`; closed,
   fork/foreign or mismatched metadata is `BLOCKED`. Pin `H=headRefName` once.
   Treat metadata as data: require `^[A-Za-z0-9._/-]+$`, reject leading `-` and
   `..`, then require `git check-ref-format "refs/heads/$H"`. Quote all values;
   never interpolate them into generated shell source or use `eval`.
3. Read `git worktree list --porcelain`, capturing canonical invoking path and
   main path as literal `MAIN` data. A bare repository is `BLOCKED`. Reject a path with
   quotes, dollar sign, backtick, backslash, CR or LF before using it in commands.
   Match only an exact `branch refs/heads/$H` record; locked/prunable/missing
   records are `BLOCKED` with a specific path and recovery hint.
4. The matching current registered path is `in-place`; another matching clean
   canonical registered path is `reused`. If the current branch is `H` without
   matching registration, stop rather than duplicate. Do not trust printed paths.
5. Only with no matching record, re-enter and verify the canonical main path,
   then call `ywc-worktrees --mode create --task-name "pr-$PR_NUMBER" --branch
   "$H" --existing-branch "$H"`. Require `Status: DONE`, re-read registration
   and derive the exact head record independently; set state `created`. Any
   required provider failure is terminal: do not retry, create a replacement,
   or silently change to a newly discovered worktree.
6. Canonicalize `WT_PATH`, require matching registration, root and branch `H`,
   and require `git status --porcelain --untracked-files=all` to be empty before
   refresh. Dirty state is `BLOCKED`; exact fetch and fast-forward only are allowed.
   Local-ahead/diverged history is `BLOCKED`; never reset/rebase or use a main
   checkout fallback. Preserve the selected state and already-created artifacts.
7. Any later PR metadata response with a changed number/head/repository/open
   state returns `BLOCKED`; do not replace pinned PR_NUMBER/H mid-invocation.

## Refresh recipe

Execute only after the selection/argument checks above. Inputs are parsed literal
`WT_PATH` and `H`; capture diagnostics and exit status. This is an executable
source recipe, not an installed dispatcher or a live agent trace.

<!-- pr-worktrees:refresh:start -->
```bash
set -euo pipefail
verify_identity() {
  [ "$(pwd -P)" = "$WT_PATH" ] &&
  [ "$(git -C "$WT_PATH" rev-parse --show-toplevel)" = "$WT_PATH" ] &&
  [ "$(git -C "$WT_PATH" branch --show-current)" = "$H" ] || return 1
  git -C "$WT_PATH" worktree list --porcelain | awk -v path="$WT_PATH" -v ref="refs/heads/$H" '
    BEGIN { RS=""; FS="\n" } { p=""; b=""; for(i=1;i<=NF;i++) { if($i=="worktree " path) p=1; if($i=="branch " ref) b=1 } if(p && b) { found=1; for(i=1;i<=NF;i++) if($i ~ /^(locked|prunable)( |$)/) bad=1 } } END { exit (!found || bad) }'
}
cd "$WT_PATH" || { printf '%s\n' 'BLOCKED: worktree entry failed' >&2; exit 1; }
verify_identity || { printf '%s\n' 'BLOCKED: worktree identity mismatch' >&2; exit 1; }
dirty=$(git status --porcelain --untracked-files=all) || { printf '%s\n' 'BLOCKED: status query failed' >&2; exit 1; }
[ -z "$dirty" ] || { printf '%s\n' 'BLOCKED: worktree dirty' >&2; exit 1; }
git fetch --no-tags origin "+refs/heads/$H:refs/remotes/origin/$H" || { printf '%s\n' 'BLOCKED: exact fetch failed' >&2; exit 1; }
ahead=$(git rev-list --count "refs/remotes/origin/$H..HEAD") || { printf '%s\n' 'BLOCKED: ancestry query failed' >&2; exit 1; }
[ "$ahead" = 0 ] || { printf '%s\n' 'BLOCKED: local-ahead or diverged history' >&2; exit 1; }
git merge --ff-only "refs/remotes/origin/$H" || { printf '%s\n' 'BLOCKED: fast-forward failed' >&2; exit 1; }
verify_identity || { printf '%s\n' 'BLOCKED: worktree identity changed' >&2; exit 1; }
dirty=$(git status --porcelain --untracked-files=all) || { printf '%s\n' 'BLOCKED: final status query failed' >&2; exit 1; }
[ -z "$dirty" ] || { printf '%s\n' 'BLOCKED: final worktree dirty' >&2; exit 1; }
printf '%s\n' 'DONE: exact head refreshed'
```
<!-- pr-worktrees:refresh:end -->

## Invocation-wide operation guard

After selection, `WT_PATH`, `H`, repository, PR number and state are fixed. Before
every review file read/edit, PR API operation, commit, push, retry, CI check/wait
or merge-readiness check, confirm `pwd -P == WT_PATH`, canonical repository root
`== WT_PATH`, and current branch `== H`. Keep one invocation-wide cwd re-entry
budget: on the first mismatch consume it, re-enter `WT_PATH` once and recheck all
three conditions. Any second mismatch or failed identity check is `BLOCKED`
before that operation. Never mutate from the main checkout as fallback.

Before every PR API write (reply, comment) and every push, also re-query the
pinned PR with `gh pr view "$PR_NUMBER" --repo "$REPOSITORY" --json
number,state,headRefName,isCrossRepository` and require the pinned number,
`OPEN`, `headRefName == H` and `isCrossRepository=false`. A PR closed or
re-pointed mid-run is `BLOCKED` before that write; local path and branch checks
alone cannot detect it.

A failed required command stops later edits, commits, API writes, pushes and
retries. Report the failed gate and every completed commit/push; preserve worktree
and branch. Successful review feedback may follow the existing bounded retry
policy, but a transport/identity/required CI failure never enters that retry.
Only created worktrees get branch-preserving prune guidance in a separate
invocation from the saved, verified canonical MAIN and same resolved root/path;
reused/in-place worktrees are never automatically removed. Retained review worktrees remain
subject to unchanged Drift/Missing/Leaked audit classifications.
