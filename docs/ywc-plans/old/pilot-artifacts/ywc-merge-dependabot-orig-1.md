# Dispatch artifact: ywc-merge-dependabot (original body, run 1)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: original
**Refused/escalated**: False


## Actions
- gh repo view --json nameWithOwner --jq .nameWithOwner
- gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
- Parse $ARGUMENTS for scope/execution tokens (none found → default: all PRs, sequential)
- gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
- Sort resulting PR list ascending by PR number
- If PR count > 20, pause and ask user for confirmation before proceeding (and recommend parallel-auto if PRs span multiple ecosystems)
- For each PR: check for Dockerfile FROM image version changes; if present, skip and label 'Skipped (Dockerfile)'
- For each PR: parse title pattern 'Bump X from A to B' and compare leftmost non-zero version segment; if major bump, skip and label 'Skipped (Major version upgrade)'
- For each remaining PR: gh pr checks {number} --required; if not all passed, skip and label 'Failed (CI not passing)'
- For each PR passing all pre-merge checks, in ascending PR number order: gh pr merge {number} --merge
- On merge conflict: comment '@dependabot rebase' on the PR and wait for Dependabot to rebase
- If rebase does not clear the conflict: gh pr checkout {number}; resolve conflicts manually; git add <resolved-files> (explicit, not -A); git commit -m 'fix: resolve merge conflict for dependabot PR #{number}'; git push; wait for CI; gh pr merge {number} --merge
- If conflict cannot be resolved cleanly, skip the PR and record the failure
- If CI fails at any point (initial or after conflict resolution), skip the PR and record the failure
- After each successful merge, note it as a possible source of new conflicts in the next queued PR
- After all PRs processed, emit final summary: Mode line, per-PR result table (Merged/Skipped/Failed with reason), total counts merged/skipped/failed
- If gh CLI is not authenticated at any point, stop and ask the user to run gh auth login
- If no Dependabot PRs are found, report 'No Dependabot PRs found' and stop
- Never force-merge or bypass branch protection rules

## Files touched
- claude-code/skills/ywc-merge-dependabot/SKILL.md (read only — procedure source, not modified)

## Gates enforced
- Dockerfile FROM-change skip gate
- Major version bump skip gate (leftmost non-zero segment comparison)
- Required CI status gate before merge
- Merge conflict resolution order: @dependabot rebase first, manual resolution only as fallback
- Never force-push or hand-resolve conflicts as first resort
- Branch protection never bypassed
- gh CLI authentication check before proceeding
- No Dependabot PRs found → report and stop
- >20 eligible PRs → ask user for confirmation before proceeding
- Final per-PR summary table with merged/skipped/failed counts is non-optional

## Full narrative

Here is exactly what I would do to handle this request, following the ywc-merge-dependabot procedure step by step.

**Announcement.** I would open by stating: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."

**Context gathering.** I would run:
- `gh repo view --json nameWithOwner --jq .nameWithOwner`
- `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

to establish the repo and default branch for the report.

**Mode selection.** The user's request ("merge Dependabot PRs, batch-process dependency updates, clean up accumulated Dependabot PRs") contains no explicit `security` or `parallel-auto` tokens, so I would default to: scope = all open Dependabot PRs, execution = sequential (one PR at a time, ascending PR number). I would not silently assume parallel-auto even though "batch-process" sounds like it implies parallelism — the skill's mode grammar requires the literal token, so I'd only switch modes if the user explicitly asks for it, or later recommend it if the batch turns out large and multi-ecosystem.

**Step 1 — List PRs.** I would run:
```
gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
```
and sort the results by PR number ascending, since earlier merges can affect later PRs' merge state.

**Size check.** If the resulting list exceeds 20 PRs, I would pause and ask the user for explicit confirmation before proceeding, and if those PRs span more than one ecosystem (npm, github-actions, python, go, cargo, maven, gradle, docker) I would recommend switching to `parallel-auto` mode instead of continuing sequentially.

**Step 2 — Pre-merge checks (per PR, before touching anything).** For every candidate PR I would check, in order:
1. Does the diff modify a `FROM` image tag in any Dockerfile? If yes → skip, label `Skipped (Dockerfile)`.
2. Does the PR title ("Bump X from A to B") show a change in the leftmost non-zero version segment (major bump)? If yes → skip, label `Skipped (Major version upgrade)`, and surface it for human review rather than auto-merging.
3. `gh pr checks {number} --required` — if required checks have not all passed, skip and label `Failed (CI not passing)`.

I would not merge any PR that fails one of these gates, and I would not treat a "looks safe" major bump as an exception — the skill's Rationalization Defense table explicitly calls that out as a rule to enforce, not to talk myself out of.

**Step 3a — Sequential merge flow.** For each PR that clears all pre-merge checks, processed strictly in ascending PR-number order:
```
gh pr checks {number} --required
gh pr merge {number} --merge
```
If a merge conflict appears, I would first comment `@dependabot rebase` on the PR and wait for Dependabot's own rebase — I would not hand-resolve or force-push as a first resort. Only if that rebase fails to clear the conflict would I fall back to:
```
gh pr checkout {number}
# resolve conflicts by hand
git add <resolved-files>      # explicit paths, never -A
git commit -m "fix: resolve merge conflict for dependabot PR #{number}"
git push
# wait for CI, then:
gh pr merge {number} --merge
```
If CI fails at any point (initial pass or after conflict resolution), or the conflict cannot be cleanly resolved, I would skip that PR and record the failure rather than force it through. After every successful merge I would note it, since it can introduce new conflicts in the next queued PR — this is why sequential processing stays strictly ordered.

I would skip the ecosystem-grouping step (2.5) and the parallel-auto flow (3b) entirely in this default run, since no `parallel-auto` token was supplied.

**Step 4 — Final summary.** After the whole batch is processed I would emit a results table in the skill's required format: a Mode line (`sequential`, scope = all PRs), a per-PR line for every processed PR marked ✅ Merged / ⏭️ Skipped (with reason) / ❌ Failed (with reason), noting explicitly if an earlier merge caused a later PR's conflict, and a totals line (`Total: N merged / M skipped / K failed`). I would never omit this summary, even if every PR succeeded or every PR failed.

**Error handling I would apply throughout:**
- If `gh` is not authenticated, I would stop immediately and ask the user to run `gh auth login` rather than attempting workarounds.
- If no Dependabot PRs are found, I would report that and stop — no further action.
- If a rate limit is hit mid-run, I would wait and retry, or stop and report progress so far.
- If branch protection blocks a merge, I would skip that PR and note the specific protection rule in the final report rather than attempting to bypass it.

**What I would not do:** force-merge or bypass branch protection under any circumstance; auto-merge a major version bump without flagging it for human confirmation; hand-resolve a conflict before trying `@dependabot rebase`; merge a PR whose lockfile hash looks inconsistent with a green CI run (that would indicate dirty state, and I'd stop to investigate/rebase first); or fire off a `parallel-auto`-style fan-out when the request only implied "batch" without the explicit token and without first checking `gh repo view --json autoMergeAllowed` for the repository.

Given that the tools available to this skill are restricted to Bash and Read, all of the above would be executed via `gh` CLI and `git` commands plus targeted file checks (e.g., inspecting Dockerfile diffs) — no direct file edits outside of conflict resolution on a checked-out Dependabot branch, and no skill files or repository configuration would be modified.

I would not need to ask a clarifying question before starting this default run, since the absence of scope/execution tokens maps unambiguously to "all Dependabot PRs, sequential" per the skill's Mode Selection table — I would only escalate to a question if the initial PR count exceeded 20 (size confirmation) or if `gh` authentication was missing.
