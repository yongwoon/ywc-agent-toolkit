# Existing branch creation

Ported from `yongwoon/develop-with-llm` #347, frozen merge
`76200680f059d34d295b3f01da527c29ea782dc2`,
`tools/codex-skill/skills/ywc-worktrees/SKILL.md`.

The provider creates a new worktree only; it never reuses an existing target path.
The PR consumer owns clean registered `in-place` / `reused` selection. Preserve the
existing root resolution, mandatory pre-create audit, ignore guard, and cleanup/audit
classifications. No helper path from the upstream installation is copied.

Require `--branch` to equal the literal `--existing-branch` value. Reject a leading
`-`, `..`, non-allowlisted characters, or failed `git check-ref-format --branch`
before branch-specific commands. Exactly one of base/existing is required.
A checked-out branch, dirty matching worktree, locked/prunable record or missing
registered path is `BLOCKED`; report which state was observed and preserve it.
A caller may select a clean registered worktree separately, but must never use
`--force`, reset, rebase, another remote, or a replacement branch as a fallback.

The recipe below runs only after repository/root/audit preflight and after the
parent of `RESOLVED_PATH` has been canonicalized. `EXISTING_BRANCH`, `BRANCH`,
`RESOLVED_PATH`, and optional `BASE_BRANCH` are parsed argv data, not shell source.
Capture its status/output. Every failure stops creation; stderr from Git remains
verbatim. An exit-2 remote lookup without an exact head is absence; other nonzero
lookup/fetch results are transport failures, never absence.

<!-- pr-worktrees:existing-branch:start -->
```bash
set -uo pipefail
if [ -n "${BASE_BRANCH:-}" ] || [ -z "${EXISTING_BRANCH:-}" ] || [ "${BRANCH:-}" != "$EXISTING_BRANCH" ]; then
  printf '%s\n' 'NEEDS_CONTEXT: require equal existing/branch and no base flag' >&2; exit 1
fi
case "$EXISTING_BRANCH" in ''|-*|*..*|*[!A-Za-z0-9._/-]*)
  printf '%s\n' 'NEEDS_CONTEXT: invalid existing branch' >&2; exit 1;; esac
git check-ref-format --branch "$EXISTING_BRANCH" >/dev/null || { printf '%s\n' 'NEEDS_CONTEXT: invalid ref' >&2; exit 1; }
if [ -e "$RESOLVED_PATH" ] || [ -L "$RESOLVED_PATH" ]; then
  printf '%s\n' 'BLOCKED: target path exists' >&2; exit 1
fi
records=$(git worktree list --porcelain) || { printf '%s\n' 'BLOCKED: worktree query failed' >&2; exit 1; }
record=$(printf '%s\n' "$records" | awk -v ref="refs/heads/$EXISTING_BRANCH" 'BEGIN { RS=""; FS="\n" } { for(i=1;i<=NF;i++) if($i=="branch " ref) { print; break } }')
if [ -n "$record" ]; then
  matched_path=$(printf '%s\n' "$record" | sed -n 's/^worktree //p')
  case "$matched_path" in *"'"*|*'"'*|*'$'*|*'`'*|*'\'*|*$'\r'*|*$'\n'*)
    printf '%s\n' 'BLOCKED: unsafe registered path' >&2; exit 1;; esac
  if printf '%s\n' "$record" | grep -Eq '^locked( |$)'; then
    printf '%s\n' 'BLOCKED: matching worktree locked' >&2
  elif [ ! -d "$matched_path" ] || printf '%s\n' "$record" | grep -Eq '^prunable( |$)'; then
    printf '%s\n' 'BLOCKED: matching worktree missing or prunable' >&2
  else
    dirty=$(git -C "$matched_path" status --porcelain --untracked-files=all) || { printf '%s\n' 'BLOCKED: status query failed' >&2; exit 1; }
    if [ -n "$dirty" ]; then printf '%s\n' 'BLOCKED: matching worktree dirty' >&2
    else printf '%s\n' 'BLOCKED: existing branch checked out' >&2; fi
  fi
  exit 1
fi
git rev-parse --verify --quiet "refs/heads/$EXISTING_BRANCH^{commit}" >/dev/null
local_status=$?
if [ "$local_status" -eq 0 ]; then
  git worktree add "$RESOLVED_PATH" "$EXISTING_BRANCH" || { printf '%s\n' 'BLOCKED: local worktree add failed' >&2; exit 1; }
elif [ "$local_status" -eq 1 ]; then
  remote_rows=$(git ls-remote --exit-code --heads origin "refs/heads/$EXISTING_BRANCH")
  lookup_status=$?
  exact_count=$(printf '%s\n' "$remote_rows" | awk -v ref="refs/heads/$EXISTING_BRANCH" 'NF==2 && $2==ref && $1 ~ /^[0-9a-f]+$/ && (length($1)==40 || length($1)==64) { n++ } END { print n+0 }')
  row_count=$(printf '%s\n' "$remote_rows" | awk 'NF { n++ } END { print n+0 }')
  if [ "$lookup_status" -eq 2 ] && [ "$exact_count" -eq 0 ]; then
    printf '%s\n' 'NEEDS_CONTEXT: branch absent locally and on origin' >&2; exit 1
  elif [ "$lookup_status" -ne 0 ]; then
    printf '%s\n' 'BLOCKED: remote lookup failed' >&2; exit 1
  elif [ "$exact_count" -ne 1 ] || [ "$row_count" -ne 1 ]; then
    printf '%s\n' 'NEEDS_CONTEXT: ambiguous exact remote ref' >&2; exit 1
  fi
  git fetch --no-tags origin "+refs/heads/$EXISTING_BRANCH:refs/remotes/origin/$EXISTING_BRANCH" || { printf '%s\n' 'BLOCKED: exact fetch failed' >&2; exit 1; }
  git worktree add --track -b "$EXISTING_BRANCH" "$RESOLVED_PATH" "refs/remotes/origin/$EXISTING_BRANCH" || { printf '%s\n' 'BLOCKED: tracking worktree add failed' >&2; exit 1; }
else
  printf '%s\n' 'BLOCKED: local ref query failed' >&2; exit 1
fi
printf 'DONE: %s\n' "$RESOLVED_PATH"
```
<!-- pr-worktrees:existing-branch:end -->

After success, independently read `git worktree list --porcelain` and require
exact path + `refs/heads/$EXISTING_BRANCH` registration, canonical root, matching
branch and clean status. A failed post-create verification is `BLOCKED` with its
already-created path/branch reported; do not claim partial success or auto-prune.
