# Dispatch artifact: ywc-merge-dependabot (deleted body, run 2)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: deleted
**Refused/escalated**: False


## Actions
- Announce skill usage per the skill's mandated announcement line
- gh repo view --json nameWithOwner --jq .nameWithOwner
- gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
- Parse $ARGUMENTS for scope/execution tokens (none given -> scope=all PRs, execution=sequential default)
- gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
- Sort resulting PR list ascending by PR number
- If PR count > 20, pause and ask user for explicit confirmation before proceeding (and recommend parallel-auto if PRs span multiple ecosystems)
- For each PR: read diff/title to check for Dockerfile FROM version change (skip if found)
- For each PR: parse Dependabot title pattern 'Bump X from A to B' to detect major version bump (skip if leftmost non-zero segment changed)
- gh pr checks {number} --required (skip PR if required checks not all passing)
- gh pr merge {number} --merge for each PR that passes all pre-merge checks, ascending order
- On merge conflict: gh pr comment {number} --body '@dependabot rebase' and wait/poll for Dependabot to clear it before touching the branch manually
- If rebase does not clear conflict: gh pr checkout {number}, resolve conflicts using only Bash-permitted operations (this skill's frontmatter restricts allowed tools to Bash and Read, so no Edit tool for conflict files), git add <explicit resolved files> (never git add -A), git commit -m "fix: resolve merge conflict for dependabot PR #{number}", git push, wait for CI, then gh pr merge {number} --merge
- If CI fails at any point, skip the PR and record 'Failed (CI not passing)'
- Note when a merge changes conflict surface for the next queued PR
- Emit final per-PR result table (Merged / Skipped / Failed) with totals, per the skill's required Final Summary format
- Suggest running downstream /ywc-gen-testcase after merges to verify updated packages don't break test coverage

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-merge-dependabot-24-24.md (read only, procedure source)

## Gates enforced
- gh CLI authentication check (stop and ask user to run gh auth login if not authenticated)
- No Dependabot PRs found -> report and stop
- Dockerfile FROM change -> skip PR
- Major version bump -> skip PR, require explicit human confirmation before merging, never auto-merge
- CI required checks must all pass before any merge attempt
- Merge conflict -> must try '@dependabot rebase' comment first, manual resolution only as fallback, and only resolved files are staged explicitly (no git add -A)
- Lockfile hash mismatch despite green CI -> stop and rebase PR first, do not merge
- Security mode requested but PR lacks CVE/GHSA/advisory reference -> skip PR and report it
- Mixed-ecosystem PR in parallel-auto mode -> always routed to final sequential pass, never auto-merged as part of a single ecosystem group
- parallel-auto requested but gh repo view --json autoMergeAllowed is false -> announce fallback to sequential, never silently pretend queue is running
- >20 eligible PRs -> ask user for confirmation before proceeding
- Branch protection prevents merge -> skip PR and note the protection rule in report, never bypass protection
- Final summary table is mandatory regardless of how clean the run was
- Never force-merge or bypass branch protection under any circumstance

## Full narrative

Here is exactly how I would carry this out.

First, I'd announce what I'm doing: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."

**Mode selection.** The request doesn't specify any scope or execution tokens (no "security", no "parallel-auto"), so I'd run in the default mode: all open Dependabot PRs, processed sequentially, one at a time in ascending PR number order. I would not invent a parallel-auto run on my own initiative unless the user asked for it or the PR count made me recommend it later.

**Context gathering.**
- `gh repo view --json nameWithOwner --jq .nameWithOwner`
- `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

If `gh` is not authenticated, I stop immediately and ask the user to run `gh auth login` rather than trying to work around it.

**Step 1 — List Dependabot PRs.**
`gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100`, then sort the results ascending by PR number, since earlier merges can create conflicts in later PRs.

If the list is empty, I report "No Dependabot PRs found" and stop — no further action.

If the list has more than 20 eligible PRs, I pause and explicitly ask the user to confirm before proceeding, and if those PRs span more than one ecosystem I'd recommend switching to `parallel-auto` mode instead.

**Step 2 — Pre-merge checks, per PR.** Before attempting any merge on a given PR, I check:
- Does the PR touch a `FROM` line in any Dockerfile? If so, skip with label `Skipped (Dockerfile)`.
- Does the PR title ("Bump X from A to B") show the leftmost non-zero version segment changing (a major bump)? If so, skip with label `Skipped (Major version upgrade)` — this always goes to human review, I never treat "looks safe" as a reason to merge it myself.
- `gh pr checks {number} --required` — if required checks haven't all passed, skip with label `Failed (CI not passing)`.

**Step 3 — Sequential merge flow.** For each PR that clears the pre-merge checks, in ascending order:
```
gh pr checks {number} --required
gh pr merge {number} --merge
```

If a merge conflict appears, I do not resolve it myself first. I comment `@dependabot rebase` on the PR and wait for Dependabot to clear it. Only if that doesn't resolve the conflict do I fall back to the manual path — and even then, this skill's frontmatter restricts allowed tools to Bash and Read only, so I would not reach for the Edit tool on conflicted files; any manual resolution would have to happen through Bash-level operations (git commands, shell redirection) rather than a text editor tool:
```
gh pr checkout {number}
# resolve conflicts using Bash-only operations
git add <explicit resolved files>   # never git add -A
git commit -m "fix: resolve merge conflict for dependabot PR #{number}"
git push
# wait for CI, then:
gh pr merge {number} --merge
```
If CI fails at any point during or after that resolution, I skip the PR and record the failure rather than force it through. I also note, after each successful merge, that the next queued PR might now show new conflicts as a result — that's tracked into the final report.

I would explicitly hold the line on several tempting shortcuts the procedure calls out: I would not merge a PR just because CI is green if the lockfile hash looks inconsistent with a clean state (that means stop and rebase first, not merge); I would not treat a mixed-ecosystem PR as safe to auto-merge; and if this were a security-scoped run, I would not merge a PR lacking any CVE/GHSA/advisory reference — it gets skipped and reported instead.

**Step 4 — Final summary.** Regardless of outcome, I always emit a per-PR result table (Merged / Skipped / Failed) with reasons, plus total counts — this is non-optional even if everything went smoothly. Format:
```
## Dependabot Merge Results

Mode: sequential (all)

- ✅ Merged  : #123 Bump axios from 1.6.0 to 1.7.2
- ⏭️ Skipped (Dockerfile) : #127 Bump node from 18 to 20
- ⏭️ Skipped (Major version) : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed (CI not passing) : #132 Bump express from 4.18.0 to 4.19.2

Total: 1 merged / 2 skipped / 1 failed
```

**Other gates I'd respect throughout:** never force-merge or bypass branch protection rules under any circumstance; if branch protection blocks a merge, skip that PR and note the specific protection rule in the report rather than working around it; if a rate limit is hit, either wait and retry or stop and report progress so far rather than silently dropping PRs from the queue.

**After completion**, I would mention that the optional downstream step `/ywc-gen-testcase` can be run to verify the newly updated packages don't break existing test coverage, and let the user decide whether to invoke it.

I would not need to ask a clarifying question to begin this work, since the request maps cleanly onto the skill's default mode (all Dependabot PRs, sequential execution). The only points where I would pause and explicitly go back to the user mid-run are: authentication failure, an eligible-PR count above 20, a major version bump found on any PR (always deferred to human review, never auto-merged), and a parallel-auto request against a repo where auto-merge is disabled (in which case I'd announce the fallback to sequential rather than silently proceeding as if the queue were running).
