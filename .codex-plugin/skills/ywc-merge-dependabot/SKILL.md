---
name: ywc-merge-dependabot
description: >-
  (ywc) Use when the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs. Triggers: "merge dependabot", "dependabot PR", "dependency updates", "security updates merge", "디펜다봇 머지", "依存関係更新マージ". Do not use for non-Dependabot PRs, manual dependency upgrades, or for merging feature PRs (use ywc-create-pr or platform tools).
---

# Merge Dependabot Pull Requests

**Announce at start:** "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-lane scheduling) when requested."

Safely merge Dependabot PRs with CI verification, conflict resolution, and clear reporting.

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
| **CI status** | Required CI checks have not all passed | `Failed (CI not passing)` |

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

#### 3a. Sequential Flow (default)

Process PRs one at a time in ascending PR number order. This is important because merging one PR can create conflicts in subsequent PRs.

For each PR that passes pre-merge checks:

```bash
# Check CI status
gh pr checks {number} --required

# Attempt merge
gh pr merge {number} --merge
```

**If a merge conflict occurs:**

1. Check out the PR branch and attempt to resolve the conflict
2. Push the resolved branch
3. Wait for CI to re-run and pass
4. Merge if CI passes
5. If the conflict cannot be resolved cleanly, skip the PR

```bash
gh pr checkout {number}
# resolve conflicts
git add <resolved-files>  # stage only the conflict-resolved files explicitly
git commit -m "fix: resolve merge conflict for dependabot PR #{number}"
git push
# wait for CI, then merge
gh pr merge {number} --merge
```

**If CI fails** after conflict resolution or at any point, skip the PR and record the failure.

After each successful merge, note it — the next PR in the queue may now have conflicts caused by this merge.

#### 3b. Parallel-Auto Flow

In parallel-auto mode the client uses GitHub auto-merge as a per-PR scheduler while preserving one active PR per ecosystem lane. GitHub auto-merge merges a PR when its requirements are met; it is not, by itself, an ecosystem-aware queue. If the repository's branch protection requires GitHub merge queue, `gh pr merge` may add eligible PRs to that queue, but the skill must still maintain ecosystem lanes and poll outcomes.

**Stage 1 — Start one non-mixed PR per ecosystem lane:**

For each non-empty ecosystem group, start only the first PR in that group with auto-merge:

```bash
gh pr merge {number} --auto --merge
```

This sets the active PR to merge automatically as soon as its CI is green and the branch is up to date. Do not enable auto-merge for the remaining PRs in the same ecosystem yet; enabling all same-lockfile PRs at once can race because auto-merge is not ecosystem-aware. Different ecosystem lanes may have one active PR each.

**Stage 2 — Poll active lanes and advance them:**

Track each active PR's state until it reaches a terminal state. When an active PR merges, start the next PR from the same ecosystem lane. Use a single bounded loop (do not spin in tight retries):

```bash
# Wait up to 30 minutes total, polling every 60 seconds.
deadline=$(( $(date +%s) + 1800 ))
declare -A lanes
lanes[npm]="101 105 107"
lanes[github-actions]="203 209"
active=(101 203)   # first PR from each non-empty lane
declare -A status
while [ ${#active[@]} -gt 0 ] && [ "$(date +%s)" -lt "$deadline" ]; do
  next=()
  for pr in "${active[@]}"; do
    pr_state=$(gh pr view "$pr" --json state --jq '.state' 2>/dev/null || echo UNKNOWN)
    merge_status=$(gh pr view "$pr" --json mergeStateStatus --jq '.mergeStateStatus' 2>/dev/null || echo UNKNOWN)
    if [ "$pr_state" = "MERGED" ]; then
      status[$pr]="merged"
      # Remove this PR from active. Then start the next unprocessed PR from
      # the same ecosystem lane, if any, and append that PR number to `next`.
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
  [ ${#active[@]} -gt 0 ] && sleep 60
done

# Any PR still in `active` after the loop is recorded as lane-stalled.
for pr in "${active[@]}"; do
  status[$pr]="lane-stalled"
done
```

PRs that reach `MERGED` are recorded as `Merged`. PRs still in the `active` list after the deadline are recorded as `Failed (lane stalled)` so the user can investigate. Do not extend the deadline silently — if the lane genuinely needs more time, the user can rerun the skill.

**Stage 3 — Final sequential pass for the mixed bucket:**

After all active lanes have drained (Stage 2 returned), process the `mixed` group using the same logic as Sequential Flow (3a). Mixed PRs run last because earlier merges may have changed the conflict surface they would land in.

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
- ⏭️ Skipped   (Major version)  : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 — CONFLICTING after 30 min
- ❌ Failed    (mixed pass)     : #135 Bump aws-sdk + boto3 — manual conflict resolution required

Total: 3 merged / 2 skipped / 2 failed
```

Include:
- Mode line — scope flag + execution flag, so the reader can reproduce the run
- Ecosystem group summary — only when parallel-auto was used; the count tells the reader how many ecosystem lanes ran concurrently
- Per-PR result — for parallel-auto, annotate each line with the ecosystem; for sequential, omit the annotation
- If a previous merge affected a subsequent PR, note which PR caused the issue
- Total counts: merged / skipped / failed

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
- **downstream**: /ywc-gen-testcase (optional — run after merging dependency updates to verify the updated packages do not break existing test coverage)
