# Dispatch artifact: ywc-merge-dependabot (original body, run 3)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: original
**Refused/escalated**: False


## Actions
- Announce skill usage banner
- gh repo view --json nameWithOwner --jq .nameWithOwner
- gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
- Parse $ARGUMENTS tokens (none found) -> scope=all PRs, execution=sequential (default)
- gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
- Sort resulting PR list by PR number ascending
- For each PR: check for Dockerfile FROM version change in the diff
- For each PR: compare version numbers in title (leftmost non-zero segment) to detect major bump
- gh pr checks {number} --required for each PR
- If PR count > 20, pause and ask user for confirmation before proceeding, and recommend parallel-auto if eligible PRs span multiple ecosystems
- For each eligible PR ascending: gh pr checks {number} --required then gh pr merge {number} --merge
- On merge conflict: comment '@dependabot rebase' on the PR and wait
- If rebase does not clear conflict: gh pr checkout {number}
- Manually resolve conflicting files
- git add <explicit resolved files>
- git commit -m "fix: resolve merge conflict for dependabot PR #{number}"
- git push
- Wait for CI, then gh pr merge {number} --merge
- Skip PR and record failure if CI fails at any point
- Note after each successful merge that subsequent PRs may now have new conflicts
- Emit final per-PR result table (merged/skipped/failed) with mode line and totals
- Optionally recommend /ywc-gen-testcase as downstream follow-up

## Files touched
- claude-code/skills/ywc-merge-dependabot/SKILL.md (read only, as instructed)

## Gates enforced
- Dockerfile FROM change -> skip (Skipped (Dockerfile))
- Major version upgrade -> skip (Skipped (Major version upgrade)), requires explicit user confirmation to override
- CI required checks must pass before merge attempt
- Merge conflict resolution order: @dependabot rebase first, manual checkout/resolve only as fallback
- Never force-merge or bypass branch protection rules
- If Dockerfile/manual conflict cannot be resolved cleanly, skip and record
- Batch size >20 PRs requires explicit user confirmation before proceeding
- gh CLI must be authenticated, else stop and ask user to run gh auth login
- No Dependabot PRs found -> report and stop, no further action
- Rate limit hit -> wait/retry or stop and report progress so far
- Branch protection blocking merge -> skip PR and note the protection rule in report
- Final summary is mandatory: per-PR result table + total counts (merged/skipped/failed)

## Full narrative

Here is exactly what I would do, step by step, under the ywc-merge-dependabot procedure, given a request to merge Dependabot PRs / batch-process dependency updates / clean up accumulated Dependabot PRs with no explicit mode flags supplied.

**Announcement.** I would first state: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."

**Context gathering (Bash).**
- `gh repo view --json nameWithOwner --jq .nameWithOwner`
- `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

**Mode selection.** Since the request contains no `security` or `parallel-auto` tokens, I would resolve scope = all Dependabot PRs, execution = sequential (the default, one PR at a time, ascending PR number). I would not silently assume parallel-auto even if many PRs turn out to exist — that flag has to be explicitly requested or explicitly recommended to the user after I see the count.

**Step 1 — List Dependabot PRs.**
- `gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100`
- Sort by PR number ascending, since earlier merges can create conflicts in later PRs.
- If the list is empty, per Error Handling I would report "No Dependabot PRs found" and stop — no further action.
- If the list has more than 20 PRs, I would pause and explicitly ask the user for confirmation before proceeding, and additionally recommend parallel-auto mode if the eligible PRs span more than one ecosystem (npm + github-actions + python, etc.).

**Step 2 — Pre-merge checks, per PR, before any merge attempt.**
For each PR I would check, in order:
1. Whether the PR modifies a `FROM` image version in any Dockerfile — if so, skip with label `Skipped (Dockerfile)`.
2. Whether the PR is a major version bump (leftmost non-zero version segment changed, e.g. 2.x → 3.x), inferred from the Dependabot title pattern "Bump X from A to B" — if so, skip with label `Skipped (Major version upgrade)` and do NOT merge without explicit user confirmation.
3. `gh pr checks {number} --required` — if required checks have not all passed, skip with label `Failed (CI not passing)`.

**Step 2.5 — skipped**, since this batch is sequential mode, not parallel-auto (that step only applies when ecosystem grouping via `scripts/group-by-ecosystem.py` is needed).

**Step 3a — Sequential merge flow**, for each PR that passed pre-merge checks, ascending PR number:
```
gh pr checks {number} --required
gh pr merge {number} --merge
```
If a merge conflict occurs, I would resolve it in this strict order:
1. Comment `@dependabot rebase` on the PR and wait for Dependabot to push a rebase.
2. Only if that does not clear the conflict, fall back to manual resolution:
   - `gh pr checkout {number}`
   - resolve the conflicting files by hand
   - `git add <resolved-files>` (staging only the explicitly resolved files, never a blanket `git add -A`)
   - `git commit -m "fix: resolve merge conflict for dependabot PR #{number}"`
   - `git push`
   - wait for CI to re-run, then `gh pr merge {number} --merge` if it passes
   - if the conflict cannot be resolved cleanly, skip the PR and record it as failed

If CI fails at any point (before or after conflict resolution), I would skip the PR and record the failure rather than force it through. After each successful merge I would note it internally, since the next PR in the queue may now have new conflicts caused by that merge — this affects how I interpret subsequent pre-merge checks.

At no point would I force-merge, bypass branch protection, or silently fall through on a failed check.

**Step 4 — Final summary.** After processing the full queue, I would emit a report in this shape:
```
## Dependabot Merge Results

Mode: sequential (all PRs)

- ✅ Merged    : #123 Bump axios from 1.6.0 to 1.7.2
- ⏭️ Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- ⏭️ Skipped   (Major version)  : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed    (CI not passing) : #132 Bump express from 4.18.0 to 4.19.2

Total: 1 merged / 2 skipped / 1 failed
```
including the mode line, per-PR results, any note about a merge that affected a subsequent PR's conflict state, and total counts.

**Error handling I would apply throughout:**
- `gh` not authenticated → stop immediately and ask the user to run `gh auth login`.
- No Dependabot PRs found → report and stop.
- Rate limit hit → wait and retry, or stop and report progress so far.
- Branch protection prevents a merge → skip that PR and note the specific protection rule in the final report.

**What I would explicitly refuse to do:** merge a major-version-bump PR without explicit user confirmation; hand-resolve a merge conflict by force-pushing my own resolution before trying `@dependabot rebase` first; merge a PR whose required CI checks have not passed, even if the lockfile "looks fine"; or skip emitting the final per-PR summary table.

**Downstream follow-up.** Once merging is complete, I would mention that `/ywc-gen-testcase` is available as an optional next step to verify the newly updated packages don't break existing test coverage — but I would not invoke it automatically, since it is listed as optional downstream, not a required continuation.

I would not need to ask a clarifying question up front for this generic request, since the skill's default (all PRs, sequential) is well-defined; the only point at which I would proactively pause for user input is if the eligible PR count exceeds 20, or if a major-version bump is encountered (skip-and-report, not merge-and-ask).
