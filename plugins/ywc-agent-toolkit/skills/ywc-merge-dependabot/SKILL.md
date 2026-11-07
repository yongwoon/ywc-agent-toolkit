---
name: ywc-merge-dependabot
description: >-
  (ywc) Use when the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs. Triggers: "merge dependabot", "dependabot PR", "dependency updates", "security updates merge", "디펜다봇 머지", "依存関係更新マージ". Do not use for non-Dependabot PRs, manual dependency upgrades, or for merging feature PRs (use ywc-create-pr or platform tools).
---

# Merge Dependabot Pull Requests

**Announce at start:** "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-lane scheduling) when requested."

Safely merge Dependabot PRs with CI verification, head-pinned merges, Dependabot rebase for conflicts, and clear reporting. Metadata prefers explicit invocation (`allow_implicit_invocation: false`); it is not a runtime enforcement guarantee.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "All ecosystems can run in parallel — fire all merges at once without grouping" | No. Within an ecosystem (e.g., multiple npm PRs all touching `package-lock.json`) the client must keep one active PR at a time. `parallel-auto` only fans out across non-overlapping ecosystems, not within one. |
| "Mixed-ecosystem PR (touches both `package.json` and `pom.xml`) is fine to auto-merge" | No. Mixed PRs go to a final sequential pass; `--auto` cannot guarantee ordering when a single PR crosses two parallel groups. |
| "Just enable `--auto` on every PR and walk away" | The polling loop and final summary are non-optional. Without them users have no audit trail of which PRs failed, why, or whether an ecosystem lane stalled. |
| "Repo doesn't have auto-merge enabled, fall through silently" | If `parallel-auto` is requested but `gh repo view --json autoMergeAllowed` returns `false`, fall back to sequential mode and tell the user — never pretend parallel scheduling is running. |
| "CI is green but lockfile shows different hash, merge anyway" | Lockfile mismatch indicates dirty working state. Stop and rebase the PR first. |
| "Major version bump looks safe, just merge" | Major bumps need explicit user confirmation. Default action: skip and report for human review. |
| "Conflicts with main, force-push my own resolution" | Use Dependabot's `@dependabot rebase` comment instead. Hand-resolved conflicts in dep PRs hide breaking changes. |
| "Security mode, but PR has no CVE link" | If `security` mode is requested and CVE/advisory is missing, skip the PR and report it. |
| "All passed, no need for a final summary" | Always emit a per-PR result table (merged / skipped / failed) at the end. |

**Violating the letter of these rules is violating the spirit.** Dependabot velocity is worthless if a bad merge silently breaks main.

## Context

- Repository: !`gh repo view --json nameWithOwner --jq .nameWithOwner`
- Default branch: !`gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

## Mode Selection

This skill supports two orthogonal flags inside `$ARGUMENTS`. Parse the argument string as a set of space-separated tokens.

**Scope flag** — controls which PRs are eligible:

| Token | Scope |
| --- | --- |
| `security` | Security-related Dependabot PRs only |
| _(token absent)_ | All Dependabot PRs |

**Execution flag** — controls how eligible PRs are processed:

| Token | Execution | When to use |
| --- | --- | --- |
| `parallel-auto` | Group eligible PRs by lockfile ecosystem; keep one active `gh pr merge --auto` PR per ecosystem lane; enqueue the next PR in that lane only after the previous PR reaches a terminal state; one final sequential pass clears the `mixed` bucket | Many PRs (≥ 5) across multiple ecosystems (npm + github-actions + python ...) where wall-clock CI wait is the bottleneck |
| _(token absent)_ | Sequential — one PR at a time, ascending PR number | Small batches, repos with strict branch protection, or environments where auto-merge is disabled |

Examples:

- `(empty)` → all PRs, sequential (default)
- `security` → security PRs only, sequential
- `parallel-auto` → all PRs, ecosystem-lane auto-merge
- `security parallel-auto` → security PRs only, ecosystem-lane auto-merge

Security-related PRs are identified by labels like `security`, PR title containing "security", or Dependabot's security advisory metadata. When in doubt about whether a PR is security-related, check the PR body for CVE references or GitHub Security Advisory links.

**Parallel-auto prerequisite:** before entering parallel-auto mode, verify the repository allows auto-merge:

```bash
gh repo view --json autoMergeAllowed --jq .autoMergeAllowed
```

If the value is `false`, announce the fallback ("Auto-merge is not enabled on this repository — falling back to sequential mode") and proceed as if `parallel-auto` were absent. Never silently skip scheduling and pretend the work is in progress.

## Task

### 1. List Dependabot PRs

Retrieve all open PRs created by Dependabot:

```bash
gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
```

If in **security-only mode**, filter to PRs that match any of:
- Have a `security` label
- Title or body contains "security advisory", "CVE-", "GHSA-", or "vulnerability"
- Created by `dependabot[bot]` with security update metadata in the body

Sort the resulting list by PR number ascending — processing order matters because earlier merges can affect later PRs.

### 2. Pre-Merge Checks

For each PR, run these checks **before** attempting to merge. If any check fails, skip the PR.

| Check | Skip condition | Skip label |
| --- | --- | --- |
| **Dockerfile FROM change** | PR modifies a `FROM` image version in any Dockerfile | `Skipped (Dockerfile)` |
| **Major version upgrade** | PR bumps a major version (e.g. 2.x → 3.x), which risks breaking changes | `Skipped (Major version upgrade)` |
| **CI failed** | A required CI check has failed | `Failed (CI not passing)` |
| **CI pending** | A required CI check is still pending | `Skipped (CI pending)`; in parallel-auto the PR instead stays in its lane for the Stage 1 lane start (`--auto`) |

### Dockerfile FROM detection

Fetch the diff successfully, then match changed `FROM` lines only inside Dockerfile hunks. A README or shell-file `FROM` line alone does not trigger the skip. Recognize `Dockerfile*` and `*.dockerfile` basenames in nested directories, added/deleted files and multi-stage builds; match the instruction case-insensitively. A failed diff query is unresolved, never a clean result. Unsupported quoted paths/parser failure also remain unresolved and block that PR's merge.

The following runnable recipe takes the already selected numeric PR as `$pr`. Exit 0 means skip for Dockerfile FROM change; 1 means a successful scan found none; any other exit is unresolved. Capture the exit explicitly rather than treating every nonzero as no match.

<!-- operational-safety:dockerfile-detector:start -->
```bash
patch=$(gh pr diff "$pr") || { printf '%s\n' 'UNRESOLVED: diff query failed' >&2; exit 2; }
printf '%s\n' "$patch" | awk '
  /^diff --git / { sawfile=1; docker=0; hunk=0; next }
  !hunk && (/^--- / || /^\+\+\+ /) {
    path=substr($0,5)
    if (path == "/dev/null") next
    if (path ~ /^"/) { bad=1; exit }
    sub(/^[ab]\//,"",path); sub(/\t.*$/,"",path)
    n=split(path,parts,"/")
    if (parts[n] ~ /^(Dockerfile.*|.*\.dockerfile)$/) docker=1
    next
  }
  /^@@ / { hunk=1; next }
  docker && hunk && /^[+-][[:space:]]*[Ff][Rr][Oo][Mm][[:space:]]/ { found=1 }
  NF { nonempty=1 }
  END { if (bad || (nonempty && !sawfile)) exit 2; exit !found }
'
```
<!-- operational-safety:dockerfile-detector:end -->

To detect major version bumps, compare the version numbers in the PR title (Dependabot titles typically follow the pattern "Bump X from A to B"). A major bump means the leftmost non-zero version segment changed.

### 2.5. Ecosystem Grouping (parallel-auto mode only)

Skip this step in sequential mode. In parallel-auto mode, classify the eligible PR list by lockfile ecosystem using the bundled script. Resolve the script path relative to this skill folder (the directory containing this `SKILL.md`), not relative to the target repository.

```bash
python3 /path/to/ywc-merge-dependabot/scripts/group-by-ecosystem.py {pr_numbers...}
```

Replace `/path/to/ywc-merge-dependabot` with the actual skill directory path.

The script returns single-line JSON of the shape `{"groups": {ecosystem: [pr...]}, "errors": [...]}`. Recognised ecosystems: `npm`, `github-actions`, `python`, `go`, `cargo`, `maven`, `gradle`, `docker`. PRs touching no recognised marker, or markers from two or more ecosystems, land in the `mixed` group.

The grouping serves two purposes:

1. **Audit trail** — the final summary records which ecosystem each PR belonged to and which ecosystem lanes ran concurrently.
2. **Mixed-bucket isolation** — `mixed` PRs are deliberately held back to a final sequential pass (Step 3b stage 3) so a single PR that crosses two parallel groups cannot race with itself.

Surface the grouping breakdown to the user before merging:

```
Ecosystem grouping (8 PRs eligible):
  - npm:            #201, #205, #207
  - github-actions: #203, #209
  - python:         #204, #208
  - mixed:          #211
```

### 3. Merge Process

Choose the flow based on the execution flag from Mode Selection. Both flows preserve the same safety contract — only the merge invocation and waiting strategy differ.

### One polling deadline across chunks

Set one run-wide deadline once at the start of Step 3 (`started_at + 1800` seconds). Every 3a rebase/CI wait, the parallel lane polling session and Stage 3 below share it; it is never reset per PR. Each polling chunk is bounded by the lesser of that deadline and its tool time budget. Never recompute the original 1800-second deadline on chunk resume; sleeps and API timeouts must fit the remaining total budget. A completion response received at or after the deadline cannot turn that wait into success.

Persist `deadline`, `active`, `lanes`, `status`, and `rebase_commented` (plus `rebase_intent`, below) together with the bound repository/invocation identity and pending PR head/CI run identity. For a sequential wait, `active` contains its one PR and `lanes` its pending queue. Acquire an exclusive per-repository/queue lock; a competing owner must stop before mutation. Save a complete snapshot by atomic replacement of a private state file under that serialized invocation owner after every chunk and before handoff; never evaluate state as shell source. Persistence failure is `BLOCKED`: retain the previous snapshot and stop subsequent merge/comment requests. Validate identity and state on resume; missing or malformed state returns `NEEDS_CONTEXT` without further merge/comment requests. An in-memory original deadline can reconstruct lost state only after reconciliation, never extend the budget.

Also persist `ci_wait[pr] = {head, restarts}` (the rebased head a 3a CI wait is on, and its restart count) and `stage3` (the list of PR numbers queued for Stage 3, kept beside `active` and `lanes`) in the same snapshot. An absent `ci_wait` or `stage3` key is empty, not malformed. The base-check result is never persisted: the check runs in the same block as its `--auto` call, every time. Persisted or remote values are compared in-process on parsed JSON, never interpolated into `--jq` or a shell string. On resume, first read `gh pr view {number} --json state,autoMergeRequest,headRefOid` and the Stage 1 step 1b `isInMergeQueue` value for every PR in `active`, `stage3` and `ci_wait`: a PR whose `state` is `MERGED` or `CLOSED` is recorded as terminal (`merged`, reported as `Merged`, or `closed`) and removed from those entries instead of being restarted. After those reads, advance each lane whose active PR was removed through the Stage 1 lane start block before polling: its pre-start read adopts a PR whose auto-merge is already enabled, or that is in the merge queue, as active (a start GitHub accepted before the crash), so that PR is polled and reported and the lane never stalls.

Only a successful rebase comment sets `rebase_commented[pr]`; persist that marker before another chunk. Because the process can end after GitHub accepts the comment but before the marker is saved, atomically persist a `rebase_intent[pr]` entry (with the pending PR head and a baseline of the PR's existing comment IDs) **before** sending the comment. On resume, an intent without a marker means the comment may already exist: list the PR's comments first and set the marker only if a matching `@dependabot rebase` comment whose ID is not in the baseline is found (an earlier run's comment never completes a new intent), and send only if none is. Reconcile an uncertain transport result against existing PR comments the same way before retrying, so an accepted comment is not duplicated. Reuse successful markers across retries. Rebase completion must be tied to the resulting head and its fresh CI run: stale green CI on the old head is not success.

At `now < deadline`, a nonempty queue may save state and resume; a chunk boundary is not terminal success or failure. At `now >= deadline`, incomplete work is failed, never successful. Mark started PRs that are still incomplete failed/stalled (never-started PRs are `Skipped (deadline reached)`), disable their pending auto-merge, and report a disable failure as auto-merge possibly still enabled. Stop subsequent merge or mixed-queue advancement after timeout. A PR whose state is read as `MERGED` or `CLOSED` at or after the deadline is recorded with its actual outcome (`merged`, reported as `Merged`, or `closed`) rather than left `active` as `lane-stalled`; the wait itself still counts as timed out, so the next PR in its lane is never started. Empty queues succeed only after verified completion before the deadline. These polling instructions and the lane illustration are source/expected-trace contracts; no live polling helper is provided.

#### 3a. Sequential Flow (default)

Process PRs one at a time in ascending PR number order. This is important because merging one PR can create conflicts in subsequent PRs.

For each PR that passes pre-merge checks, first read `gh pr view {number} --json mergeable --jq .mergeable`. `CONFLICTING` enters the conflict path below; any other value, `UNKNOWN` included, goes through the gate:

```bash
# Record the head CI will verify; anything but a 40-char hex SHA stops here
HEAD_SHA=$(gh pr view {number} --json headRefOid --jq .headRefOid) || HEAD_SHA=""
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "Skipped (head unreadable)"; exit 1; }

# Gate on the required checks: 0 = pass, 8 = pending, other non-zero = failed,
# except "no required checks reported" (resolved against the base branch below)
OUT=$(gh pr checks {number} --required 2>&1) && RC=0 || RC=$?
TAG=""
if [ "$RC" -ne 0 ] && [[ "$OUT" == *"no required checks reported"* ]]; then
  RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" 2>&1)" || { echo "BLOCKED: ${RESOLVER_LAUNCHER#BLOCKED: }" >&2; exit 3; }
  BASE_CHECK_SCRIPT="$(bash "$RESOLVER_LAUNCHER" "ywc-merge-dependabot/scripts/check-base-required-checks.sh" bash)" || { echo "BLOCKED: resolver failed ($?)" >&2; exit 3; }
  BASE_OUT=$(bash "$BASE_CHECK_SCRIPT" {number}) && BASE_RC=0 || BASE_RC=$?
  # Branch on the exit code before reading the last line CONFIRMED=<0|1> BASE=<…>
  case "$BASE_RC:${BASE_OUT##*$'\n'}" in
    0:*) echo "Skipped (CI pending)"; exit 1 ;;  # base requires checks; none registered yet
    1:"CONFIRMED=0 BASE="?*)                    # validated base, no required check: gate on every check
      TAG=" (no required checks)"
      OUT=$(gh pr checks {number} 2>&1) && RC=0 || RC=$? ;;
    3:*) echo "Skipped (required checks unconfirmed)"; exit 1 ;;  # lookup failed: never the fallback
    *) echo "Skipped (no required check confirmed)"; exit 1 ;;  # base unreadable or invalid, usage error
  esac
fi
case "$RC" in
  0) ;;
  8) echo "Skipped (CI pending)$TAG"; exit 1 ;;
  *) [[ "$OUT" == *"no checks reported"* ]] && { echo "Skipped (no CI checks)"; exit 1; }
     echo "Failed (CI not passing)$TAG"; exit 1 ;;
esac

# Attempt merge, pinned to the head CI verified
gh pr merge {number} --merge --match-head-commit "$HEAD_SHA" && echo "Merged$TAG"
```

Gate the merge on the exit status of `gh pr checks --required`, as the block does: exit 8 is `Skipped (CI pending)`, any other non-zero exit is `Failed (CI not passing)`, and a non-zero exit is never a merge. The exception is output containing `no required checks reported`, which gh prints both when the base has no required check and when required checks have not registered on the head yet; the block resolves it with `check-base-required-checks.sh`. Its exit 0 means `Skipped (CI pending)`. Exit 1 with a non-empty `BASE=` gates on every check and tags the result `(no required checks)`, where `no checks reported` is `Skipped (no CI checks)`. Exit 3 is `Skipped (required checks unconfirmed)`, never the all-checks fallback. Any other result, an empty `BASE=` or exit 2 included, is `Skipped (no required check confirmed)`. Shell state does not persist between tool calls, so substitute the literal recorded SHA when the merge runs in a separate call.

**Run blocked.** The two resolver lines resolve the bundled script through the shared Codex resolver; the resolver's stderr carries the `BLOCKED:` marker, which, not the exit code, tells it apart from the base check's exit 3. A resolver failure is `BLOCKED` for the whole run, never a per-PR result: make no further merge or `--auto` call and save the state snapshot. A PR that already has a terminal label (`Merged`, any `Failed (…)` or `Skipped (…)`, or `auto-merge-uncertain`) keeps its recorded terminal label; every other remaining PR is `Skipped (run blocked)`. In 3b, PRs already in `active` keep the auto-merge GitHub accepted, which is still gated by their confirmed required checks, and are reported as `Skipped (run blocked) — auto-merge still enabled` so the user can disable it.

**Refused merge.** Re-read `gh pr view {number} --json headRefOid,mergeable` and apply the same `^[0-9a-f]{40}$` check; an unreadable re-read is `Skipped (head unreadable)`. A moved head re-runs the Step 2 Dockerfile and major-version checks and the gate on it, at most 2 restarts per PR, then `Failed (head kept moving)`. An unchanged head reading `CONFLICTING` enters the conflict path; any other unchanged head is `Failed (merge refused)` with the error. Never retry unpinned.

**Conflict path.** The conflict path is entered only when `gh pr view {number} --json mergeable` reads `CONFLICTING`, in the read before the gate or in the re-read after a refused pinned merge. Never hand-resolve a Dependabot PR: a hand-merged lockfile can mask a breaking transitive bump. Use the `rebase_intent` → `@dependabot rebase` → chunked polling contract of One polling deadline across chunks above. The rebase is done when the polled `headRefOid` is 40-hex and differs from the recorded head, and `mergeable` is `MERGEABLE`; empty output, a failed query, `UNKNOWN` or any other value keeps polling. Then re-run the Step 2 checks on that `NEW_HEAD` and wait for its fresh CI inside the same run-wide deadline and chunks; this is not a second wait. Record `ci_wait[pr] = {head, restarts}` so the 2-restart cap holds across chunks. Each chunk runs the gate's check step on `NEW_HEAD`, with its sleep clamped to the remaining chunk and deadline budget:

- Exit 8, or `no required checks reported` with base-check exit 0, keeps waiting while `now < deadline`.
- Base-check exit 1 with a non-empty `BASE=` waits on every check by the same rule and tags the result `(no required checks)`.
- Exit 0 merges with `gh pr merge {number} --merge --match-head-commit "<NEW_HEAD>"` (the literal SHA), with the refused-merge rule above.
- Any other non-zero exit is `Failed (CI not passing)`.
- Base-check exit 1 with an empty `BASE=`, exit 2 or exit 3 maps as in the gate: `Skipped (no required check confirmed)` or `Skipped (required checks unconfirmed)`.
- `no checks reported` on the all-checks run keeps waiting, because a freshly rebased head may not have registered CI yet; still reported at the deadline, it is `Skipped (no CI checks)`, which takes precedence over `Failed (CI timeout)`.
- Otherwise, at `now >= deadline` the result is `Failed (CI timeout)`.

A moved head during the wait restarts it within the 2-restart cap. Polling exhaustion at the deadline, a still-conflicting head, or red CI skips the PR and surfaces it for human review.

After each successful merge, note it — the next PR in the queue may now have conflicts caused by this merge.

#### 3b. Parallel-Auto Flow

In parallel-auto mode the client uses GitHub auto-merge as a per-PR scheduler while preserving one active PR per ecosystem lane. GitHub auto-merge merges a PR when its requirements are met; it is not, by itself, an ecosystem-aware queue. If the repository's branch protection requires GitHub merge queue, `gh pr merge` may add eligible PRs to that queue, but the skill must still maintain ecosystem lanes and poll outcomes.

**Stage 1 — Start one non-mixed PR per ecosystem lane:**

For each non-empty ecosystem group, start only the first PR in that group with auto-merge, through this lane start block. The base check runs before every `--auto` call, including on resume:

```bash
# 1. Pre-start read; parse the JSON in-process. state MERGED/CLOSED → record it terminal.
#    A non-empty autoMergeRequest → already started (an earlier chunk or run): treat it as active.
#    headRefOid must match ^[0-9a-f]{40}$ (record it as <HEAD_SHA>); otherwise → stage3.
gh pr view {number} --json state,autoMergeRequest,headRefOid
# 1b. gh pr view has no isInMergeQueue field, so read it through GraphQL ({owner}/{repo} are
#     gh's own placeholders). true → GitHub already queued the PR (its autoMergeRequest may be
#     empty then): treat it as active. A failed read is treated like a failed step 1 read.
gh api graphql -F owner='{owner}' -F repo='{repo}' -F pr={number} -f query='query($owner:String!,$repo:String!,$pr:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){isInMergeQueue}}}' --jq .data.repository.pullRequest.isInMergeQueue
# 2. Confirm the base: only exit 0 may start the PR; any other exit → stage3, never --auto.
RESOLVER_LAUNCHER="$(bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/select-resolver-launcher.sh" 2>&1)" || { echo "BLOCKED: ${RESOLVER_LAUNCHER#BLOCKED: }" >&2; exit 3; }
BASE_CHECK_SCRIPT="$(bash "$RESOLVER_LAUNCHER" "ywc-merge-dependabot/scripts/check-base-required-checks.sh" bash)" || { echo "BLOCKED: resolver failed ($?)" >&2; exit 3; }
BASE_OUT=$(bash "$BASE_CHECK_SCRIPT" {number}) && BASE_RC=0 || BASE_RC=$?
[ "$BASE_RC" -eq 0 ] || { echo "stage3 (base not confirmed, exit $BASE_RC)"; exit 1; }
# 3. Compare in-process with the BASE= value of ${BASE_OUT##*$'\n'}; a difference re-runs step 2.
gh pr view {number} --json baseRefName
# 4. Start, pinned to the recorded head (the literal SHA).
gh pr merge {number} --auto --merge --match-head-commit "<HEAD_SHA>"
```

A run-wide `BLOCKED` from the resolver lines follows the Run blocked rule of 3a. Re-read `baseRefName` immediately before `--auto` (step 3). A base-check failure before any `--auto` call removes the PR from its lane and adds it to `stage3` directly, and the lane advances to its next PR. After any non-zero `--auto` result, re-read `state` and `autoMergeRequest` together (`gh pr view {number} --json state,autoMergeRequest`), plus `isInMergeQueue` with the step 1b read, before the PR leaves its lane; this does not try to tell a definite refusal from a transport failure. `--auto` can merge at once when no required check is pending, so a `MERGED` re-read persists `status[pr] = "merged"` (reported `Merged`) and a `CLOSED` re-read persists `status[pr] = "closed"`; either removes the PR from its lane, the lane advances, and the PR never enters `stage3`. An `OPEN` PR with `isInMergeQueue` true stays active in its lane: GitHub has queued it, and leaving the lane would let the next same-lockfile PR start while it can still merge. For an `OPEN` PR not in the merge queue, an empty `autoMergeRequest` removes the PR from its lane and adds it to `stage3`, and the lane advances. The PR "may already have auto-merge enabled" only when that re-read shows auto-merge enabled or fails (either read); the same holds when a resume read finds auto-merge enabled on a PR that is leaving its lane, or when the pre-start read fails. Such a PR moves to `stage3` only after `gh pr merge {number} --disable-auto` succeeds and a re-read shows `autoMergeRequest` empty and `isInMergeQueue` false. Otherwise persist `status[pr] = "auto-merge-uncertain"` and report it as `Failed (auto-merge possibly still enabled)`; it is never in `stage3`. An `auto-merge-uncertain` PR closes its lane: the lane's remaining PRs move to `stage3`, so two same-lockfile PRs never auto-merge concurrently. A resume retries `--disable-auto` once for each such PR; a retry that succeeds and re-reads an empty `autoMergeRequest` moves the PR to `stage3`.

If no PR's base is confirmed at Stage 1, announce "No required status checks confirmed on the base branch — falling back to sequential mode" and process every PR with 3a.

This sets the active PR to merge automatically as soon as its CI is green and the branch is up to date. Do not enable auto-merge for the remaining PRs in the same ecosystem yet; enabling all same-lockfile PRs at once can race because auto-merge is not ecosystem-aware. Different ecosystem lanes may have one active PR each. The pin only guards the start; heads Dependabot pushes later are guarded by the confirmed required checks, which GitHub evaluates on the head it merges.

**Stage 2 — Poll active lanes and advance them:**

Track each active PR's state until it reaches a terminal state. When an active PR merges, start the next PR from the same ecosystem lane with the Stage 1 lane start block (pre-start read, base check, `baseRefName` re-read, pinned `--auto`); a lane start never skips the base check, and a PR it moves to `stage3` lets the lane advance to its following PR in the same chunk. Use a single bounded loop (do not spin in tight retries). The following lane illustration omits state serialization and lane advancement; apply the complete chunk/state contract above, rather than executing it as a complete polling helper:

```bash
# Bounded by the run-wide deadline set once at the start of Step 3; poll every 60 seconds.
deadline=$RUN_DEADLINE  # the persisted run-wide value; never recomputed here
chunk_deadline=$(( $(date +%s) + 50 ))  # clamp to deadline; yield within tool budget
declare -A lanes
lanes[npm]="101 105 107"
lanes[github-actions]="203 209"
active=(101 203)   # first PR from each non-empty lane
declare -A status rebase_intent rebase_commented
while [ ${#active[@]} -gt 0 ] && [ "$(date +%s)" -lt "$deadline" ] && [ "$(date +%s)" -lt "$chunk_deadline" ]; do
  next=()
  for pr in "${active[@]}"; do
    pr_state=$(gh pr view "$pr" --json state --jq '.state' 2>/dev/null || echo UNKNOWN)
    merge_status=$(gh pr view "$pr" --json mergeStateStatus --jq '.mergeStateStatus' 2>/dev/null || echo UNKNOWN)
    if [ "$(date +%s)" -ge "$deadline" ]; then
      # Past the deadline: record the real terminal state, never start the next lane PR.
      case "$pr_state" in
        MERGED) status[$pr]="merged" ;;
        CLOSED) status[$pr]="closed" ;;
        *) next+=("$pr") ;;
      esac
      continue
    fi
    if [ "$pr_state" = "MERGED" ]; then
      status[$pr]="merged"
      # Remove this PR from active. Then run the Stage 1 lane start block for the
      # next unprocessed PR of the same ecosystem lane, if any, and append it to `next`.
    elif [ "$pr_state" = "CLOSED" ]; then
      status[$pr]="closed"
    elif [ "$merge_status" = "CONFLICTING" ] || [ "$merge_status" = "DIRTY" ]; then
      # Keep the active lane item — Dependabot or a maintainer may rebase before the deadline.
      next+=("$pr")
    else
      next+=("$pr")
    fi
  done
  active=("${next[@]}")
  # Bound each API call and clamp sleep to both remaining budgets.
  left=$(( deadline - $(date +%s) ))
  chunk_left=$(( chunk_deadline - $(date +%s) ))
  [ "$chunk_left" -lt "$left" ] && left=$chunk_left
  [ ${#active[@]} -gt 0 ] && [ "$left" -gt 0 ] && sleep $(( left < 60 ? left : 60 ))
done

# A chunk boundary saves all state, never marks failure by itself.
if [ "$(date +%s)" -ge "$deadline" ]; then
  for pr in "${active[@]}"; do
    status[$pr]="lane-stalled"
  done
fi
# Persist a complete snapshot per One polling deadline across chunks above.
```

PRs that reach `MERGED` are recorded as `Merged`. PRs whose status is `closed` (closed without merging, whether seen while polling, in a re-read, on resume or at the deadline) are recorded as `Skipped (closed without merge)`. PRs still in the `active` list after the deadline are recorded as `Failed (lane stalled)` so the user can investigate. `--disable-auto` does not remove a merge-queue entry, so a stalled PR whose step 1b read shows `isInMergeQueue` true is reported as `Failed (lane stalled) — still in merge queue` for the user to dequeue. Do not extend the deadline silently — if the lane genuinely needs more time, the user can rerun the skill.

**Stage 3 — Final sequential pass for the mixed bucket and unconfirmed-base PRs:**

After all active lanes have drained successfully before the deadline (not merely because a chunk returned; drained means `active` is empty and every lane's queue is empty), process the `mixed` group and the persisted `stage3` list (PRs whose base was not confirmed, whose `--auto` start failed with an empty `autoMergeRequest` re-read, or whose lane an `auto-merge-uncertain` PR closed) using the same logic as Sequential Flow (3a), under the run-wide deadline. Mixed PRs run last because earlier merges may have changed the conflict surface they would land in. PRs that 3a or Stage 3 has not reached before the deadline are `Skipped (deadline reached)`.

### 4. Final Summary

After processing all PRs, report results in this format:

```
## Dependabot Merge Results

Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2), mixed (1)

- ✅ Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- ✅ Merged    (npm)            : #125 Bump lodash from 4.17.20 to 4.17.21
- ✅ Merged    (github-actions) : #129 Bump actions/checkout from 4.1.1 to 4.2.0
- ⏭️ Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- ⏭️ Skipped   (Major version upgrade) : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 — CONFLICTING after 30 min
- ❌ Failed    (CI timeout)     : #135 Bump aws-sdk + boto3 (mixed) — rebased head CI still pending at the deadline

Total: 3 merged / 2 skipped / 2 failed
```

Include:
- Mode line — scope flag + execution flag, so the reader can reproduce the run
- Ecosystem group summary — only when parallel-auto was used; the count tells the reader how many ecosystem lanes ran concurrently
- Per-PR result — for parallel-auto, annotate each line with the ecosystem; for sequential, omit the annotation
- If a previous merge affected a subsequent PR, note which PR caused the issue
- Total counts: merged / skipped / failed
- Result labels beyond the example: `Skipped (closed without merge)`, `Failed (lane stalled) — still in merge queue`, `Skipped (CI pending)`, `Skipped (head unreadable)`, `Skipped (no required check confirmed)`, `Skipped (required checks unconfirmed)`, `Skipped (no CI checks)`, `Skipped (deadline reached)`, `Skipped (run blocked)`, `Skipped (run blocked) — auto-merge still enabled`, `Failed (CI not passing)`, `Failed (head kept moving)`, `Failed (merge refused)`, `Failed (CI timeout)`, `Failed (auto-merge possibly still enabled)`; a result gated on every check because the base has no required check carries the `(no required checks)` suffix

## Error Handling

| Error | Action |
| --- | --- |
| `gh` CLI not authenticated | Stop and ask user to run `gh auth login` |
| No Dependabot PRs found | Report "No Dependabot PRs found" and stop |
| Rate limit hit | Wait and retry, or stop and report progress so far |
| Branch protection prevents merge | Skip PR and note the protection rule in the report |

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- Never force-merge or bypass branch protection rules
- If the number of PRs is large (>20), ask the user for confirmation before proceeding. For batches of that size, also recommend `parallel-auto` mode if the eligible PRs span more than one ecosystem
- `parallel-auto` reduces wall-clock time by letting GitHub run the CI cycle for non-conflicting ecosystem lanes concurrently. It does not reduce the *per-PR* CI cost, the safety surface, or the conflict-resolution requirements — it only changes how active PRs are scheduled

## Integration

- **upstream**: None — this skill is triggered directly by the user or a scheduled workflow when Dependabot PRs accumulate
- **downstream**: `ywc-gen-testcase` (optional — run after merging dependency updates to verify the updated packages do not break existing test coverage)

## Output Format

Return the Dependabot merge report with:

```text
Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
Mode: <scope and execution mode>
Merged: <PR numbers>
Skipped: <PR numbers and reasons, using the Skipped (…) labels of Final Summary>
Failed: <PR numbers and reasons, using the Failed (…) labels of Final Summary>
Validation: <CI and branch-protection checks>
Next action: <manual follow-up or "none">
```

## Validation

Before finalizing, verify that branch protection was not bypassed, each PR result is categorized, CI status was checked after each merge lane, major or unsupported updates were skipped with reason, and failures include actionable blocker details.
