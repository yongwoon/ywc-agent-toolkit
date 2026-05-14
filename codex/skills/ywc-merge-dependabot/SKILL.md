---
name: ywc-merge-dependabot
description: (ywc) Use when the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs. Triggers: "merge dependabot", "dependabot PR", "dependency updates", "security updates merge", "디펜다봇 머지", "依存関係更新マージ". Do not use for non-Dependabot PRs, manual dependency upgrades, or for merging feature PRs (use ywc-create-pr or platform tools).
---

# Merge Dependabot Pull Requests

**Announce at start:** "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs sequentially with CI verification."

Safely merge Dependabot PRs with CI verification, conflict resolution, and clear reporting.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Multiple Dependabot PRs, batch-merge them in parallel" | Sequential only. Parallel merges race on the same package-lock and produce conflicts. |
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

This skill supports two modes based on `$ARGUMENTS`:

| Argument contains | Mode | Behavior |
| --- | --- | --- |
| `security` | Security-only | Merge only security-related Dependabot PRs |
| _(anything else or empty)_ | All | Merge all Dependabot PRs |

Security-related PRs are identified by labels like `security`, PR title containing "security", or Dependabot's security advisory metadata. When in doubt about whether a PR is security-related, check the PR body for CVE references or GitHub Security Advisory links.

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

### 3. Merge Process

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

### 4. Final Summary

After processing all PRs, report results in this format:

```
## Dependabot Merge Results

- ✅ Merged: #123 Bump axios from 1.6.0 to 1.7.2
- ✅ Merged: #125 Bump lodash from 4.17.20 to 4.17.21
- ⏭️ Skipped (Dockerfile): #127 Bump node from 18 to 20
- ⏭️ Skipped (Major version upgrade): #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed: #132 Bump express from 4.18.0 to 4.19.2 — conflict caused by #125 merge, could not resolve
```

Include:
- Processing order (ascending by PR number)
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
- If the number of PRs is large (>20), ask the user for confirmation before proceeding

## Integration

- **upstream**: None — this skill is triggered directly by the user or a scheduled workflow when Dependabot PRs accumulate
- **downstream**: /ywc-gen-testcase (optional — run after merging dependency updates to verify the updated packages do not break existing test coverage)
