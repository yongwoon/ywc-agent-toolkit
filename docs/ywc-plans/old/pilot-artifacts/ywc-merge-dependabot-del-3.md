# Dispatch artifact: ywc-merge-dependabot (deleted body, run 3)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: deleted
**Refused/escalated**: False


## Actions
- Read docs/ywc-plans/pilot-artifacts/variant-ywc-merge-dependabot-24-24.md (the only instructions used)
- Announce: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."
- Parse $ARGUMENTS for scope/execution tokens; none supplied by the user's phrasing, so default to scope=all PRs, execution=sequential
- Run: gh repo view --json nameWithOwner --jq .nameWithOwner
- Run: gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
- Run: gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
- Sort resulting PR list ascending by PR number
- If PR count is 0: report 'No Dependabot PRs found' and stop
- If PR count > 20: pause and ask the user for confirmation before proceeding, and recommend parallel-auto if PRs span more than one ecosystem
- For each PR ascending: inspect diff/files (e.g. gh pr view {number} --json files, gh pr diff {number}) to check for a Dockerfile FROM version change -> skip with label 'Skipped (Dockerfile)' if found
- For each PR: parse the Dependabot title pattern 'Bump X from A to B' and compare the leftmost non-zero version segment -> skip with label 'Skipped (Major version upgrade)' on a major bump, flagged for human review, never auto-merged
- For each PR: run gh pr checks {number} --required -> skip with label 'Failed (CI not passing)' if required checks are not all green
- For each PR passing all pre-merge checks: run gh pr checks {number} --required then gh pr merge {number} --merge
- On merge conflict: comment '@dependabot rebase' on the PR and wait for Dependabot to clear it before any manual fallback
- If rebase does not clear conflict: gh pr checkout {number}; resolve conflicts; git add <only the resolved files>; git commit -m "fix: resolve merge conflict for dependabot PR #{number}"; git push; wait for CI; gh pr merge {number} --merge
- If CI still fails after conflict resolution or at any point: skip PR and record 'Failed (CI not passing)'
- After each successful merge, note it in-progress since it may create conflicts in later queued PRs
- Skip ecosystem-grouping step (2.5) entirely since execution flag is sequential, not parallel-auto
- After processing all PRs, emit the final summary in the mandated format: mode line, per-PR result table (merged/skipped/failed, with reasons), and total counts
- Check for gh CLI authentication issues, rate limiting, and branch-protection merge blocks per the Error Handling table, stopping or skipping as specified
- Mention optional downstream step: /ywc-gen-testcase after merges to verify updated packages don't break existing test coverage
- Never force-merge, never bypass branch protection, never silently fall back or silently extend any wait/deadline

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-merge-dependabot-24-24.md

## Gates enforced
- Dockerfile FROM change -> skip
- Major version bump -> skip and require explicit human confirmation before any merge, never auto-merge
- CI required-checks must be green before merge
- Merge conflicts resolved via @dependabot rebase first, manual resolution only as fallback with explicit staged files and a labeled commit message
- CI must re-pass after any manual conflict resolution before merging
- >20 eligible PRs requires user confirmation before proceeding
- gh CLI must be authenticated or the run stops and asks the user to run gh auth login
- Branch protection blocking a merge is recorded, never bypassed
- Final per-PR result summary with merged/skipped/failed totals is mandatory, never omitted
- No silent fallback: if parallel-auto were requested but unsupported it must be announced, not silently downgraded (not triggered here since default sequential mode was used)

## Full narrative

Having read the procedure at docs/ywc-plans/pilot-artifacts/variant-ywc-merge-dependabot-24-24.md in full, here is exactly what I would do to handle "merge Dependabot PRs / batch-process dependency updates / clean up accumulated Dependabot PRs," treating that file as the sole authority for how to act.

**Opening announcement.** Before doing anything else I would state: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested." — this is a required announcement in the procedure, not optional framing.

**Mode selection.** The user's phrasing doesn't include either of the two recognized tokens (`security` for scope, `parallel-auto` for execution). Per the procedure's Mode Selection table, absence of these tokens maps to scope=all PRs and execution=sequential (one PR at a time, ascending PR number). I would proceed under that default rather than guessing the user wants parallel-auto just because they said "batch-process" — the skill defines the token vocabulary explicitly and I'd follow it literally. I would state this chosen mode in my response so the user can correct me if they actually wanted `security` or `parallel-auto`.

**Context gathering.** I'd run:
- `gh repo view --json nameWithOwner --jq .nameWithOwner`
- `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

**Step 1 — List PRs.** I'd run:
`gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100`
then sort the results by PR number ascending, since the procedure calls this out as load-bearing (earlier merges can affect later PRs).

If that call returns zero PRs, per the Error Handling table I would report "No Dependabot PRs found" and stop — no further action.

If the count exceeds 20, the Notes section requires me to pause and ask the user for confirmation before proceeding, and to recommend `parallel-auto` if the eligible PRs span more than one ecosystem. I would not silently barrel through a 20+ PR batch.

**Step 2 — Pre-merge checks, per PR, in ascending order.** For each candidate PR I would:
- Inspect its changed files/diff (e.g. `gh pr view {number} --json files`, `gh pr diff {number}`) to detect a `FROM` image version change in any Dockerfile → if found, skip with label `Skipped (Dockerfile)`.
- Parse the PR title against the Dependabot pattern "Bump X from A to B" and compare the leftmost non-zero version segment → if it's a major bump, skip with label `Skipped (Major version upgrade)` and flag it for human review. Per the Rationalization Defense table this is non-negotiable — a major bump "looking safe" is explicitly called out as not a valid reason to merge it anyway.
- Run `gh pr checks {number} --required` → if required checks haven't all passed, skip with label `Failed (CI not passing)`.

I'd skip step 2.5 (ecosystem grouping) entirely — it is explicitly scoped to parallel-auto mode only, and sequential mode is what applies here.

**Step 3a — Sequential merge flow.** For each PR that survives the pre-merge checks, in ascending order:
```
gh pr checks {number} --required
gh pr merge {number} --merge
```
If a merge conflict occurs, I would first comment `@dependabot rebase` on the PR and wait for Dependabot to clear it — per both the main flow and the Rationalization Defense table, hand-resolving conflicts in a dependency PR is explicitly discouraged because it can hide breaking changes, so this is the required first move, not an optional courtesy. Only if that rebase fails to clear the conflict would I fall back to:
```
gh pr checkout {number}
# resolve conflicts
git add <only the resolved files>
git commit -m "fix: resolve merge conflict for dependabot PR #{number}"
git push
# wait for CI, then merge
gh pr merge {number} --merge
```
If CI fails at any point in this fallback, I'd skip the PR and record `Failed (CI not passing)` rather than force it through. After each successful merge I would note that subsequent PRs may now show new conflicts as a consequence, since the procedure is explicit that sequential ordering exists precisely because earlier merges can destabilize later ones.

**Step 4 — Final summary.** After the queue is exhausted I would emit the required report format: a mode line (scope + execution flag, so the run is reproducible), a per-PR result line for every processed PR (merged / skipped-with-reason / failed-with-reason), and total counts of merged/skipped/failed. I would not omit this even if every PR merged cleanly — the procedure calls this non-optional.

**Error handling gates applied throughout:** if `gh` isn't authenticated, I stop and ask the user to run `gh auth login` rather than attempting workarounds. If rate limits are hit, I either wait and retry or stop and report progress so far. If branch protection blocks a merge, I skip that PR and note the specific protection rule in the report — I would never force-merge or bypass protection rules under any circumstance, per the Notes section.

**What I would not do:** I would not silently assume `parallel-auto` just because the request mentions "batch-process" — that word alone isn't one of the two recognized tokens, so I'd stick to sequential and flag the assumption. I would not auto-merge any major version bump. I would not hand-resolve a conflict before trying `@dependabot rebase` first. And I would not skip the final summary table under any outcome.

**Downstream note.** After merging, I would mention — as an optional next step, not something I'd run automatically — that `/ywc-gen-testcase` can be used afterward to verify the newly updated packages don't break existing test coverage, since the procedure lists that as the documented downstream integration point.

I would not refuse or escalate this request; it falls squarely within what the procedure is designed to handle. The only conditional pause built into the flow is the >20-PR confirmation gate and the implicit gate on major-version bumps requiring human sign-off before merge — both of which I would honor if and when they actually trigger during the run.
