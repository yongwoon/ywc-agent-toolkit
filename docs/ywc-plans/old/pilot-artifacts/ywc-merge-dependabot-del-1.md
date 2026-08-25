# Dispatch artifact: ywc-merge-dependabot (deleted body, run 1)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: deleted
**Refused/escalated**: False


## Actions
- Announce skill usage: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested."
- Run `gh repo view --json nameWithOwner --jq .nameWithOwner` to establish repo context
- Run `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name` to establish default branch
- Parse $ARGUMENTS for scope/execution tokens ('security', 'parallel-auto') — none present in this request, so default to scope=all Dependabot PRs, execution=sequential
- Run `gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100` to list all open Dependabot PRs
- Sort the returned PR list ascending by PR number
- If PR count > 20, pause and ask the user for confirmation before proceeding, and recommend parallel-auto if eligible PRs span more than one ecosystem
- If zero Dependabot PRs are found, report 'No Dependabot PRs found' and stop (no merge attempted)
- For each PR, run pre-merge checks: scan diff for Dockerfile FROM version changes (skip if found, label 'Skipped (Dockerfile)'); parse PR title pattern 'Bump X from A to B' to detect major version bump (skip if found, label 'Skipped (Major version upgrade)', pending explicit user confirmation)
- For each PR passing pre-checks, run `gh pr checks {number} --required` to verify CI status; skip with label 'Failed (CI not passing)' if not all green
- For each PR passing CI, run `gh pr merge {number} --merge` in ascending PR-number order (sequential flow), one at a time
- On merge conflict: first comment `@dependabot rebase` on the PR via `gh pr comment {number} --body "@dependabot rebase"` and wait for Dependabot to push a rebase
- If rebase does not clear the conflict: `gh pr checkout {number}`, resolve conflicts manually, `git add <resolved-files>` (explicit files only, no blanket add), `git commit -m "fix: resolve merge conflict for dependabot PR #{number}"`, `git push`, wait for CI to re-run, then `gh pr merge {number} --merge`
- If CI fails at any point (initial or post-conflict-resolution), skip the PR and record 'Failed (CI not passing)'
- After each successful merge, note it so downstream PRs can be checked for newly introduced conflicts caused by the prior merge
- Never use `parallel-auto` grouping script (scripts/group-by-ecosystem.py) since execution flag was not requested — sequential flow only
- Compile and emit the final per-PR result table: Merged / Skipped (Dockerfile) / Skipped (Major version) / Failed (CI not passing) / Failed (conflict unresolved), plus total counts
- Report the Mode line ('Mode: sequential (all PRs)') at the top of the summary for reproducibility
- If `gh` CLI is not authenticated at any point, stop immediately and ask the user to run `gh auth login` rather than proceeding
- If branch protection blocks a merge, skip that PR and note the specific protection rule in the final report rather than force-merging
- After the run, mention /ywc-gen-testcase as an optional downstream follow-up to verify updated packages don't break existing test coverage

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-merge-dependabot-24-24.md (read only, procedure source)

## Gates enforced
- gh CLI authentication check (stop + ask user if missing)
- No Dependabot PRs found → report and stop
- PR count > 20 → ask user confirmation before proceeding
- Dockerfile FROM change → mandatory skip, no override
- Major version bump → mandatory skip pending explicit user confirmation, never auto-merge
- CI required-checks must be green before any merge attempt
- Merge conflicts must go through @dependabot rebase first; manual resolution only as fallback, never force-push over branch protection
- Lockfile-hash mismatch on green CI → stop and rebase rather than merge (per Rationalization Defense table)
- Branch protection block → skip + report, never bypass
- Final per-PR summary table with totals is mandatory, not optional, even if all succeed

## Full narrative

Having read the ywc-merge-dependabot skill procedure in full, here is exactly how I would execute this request, since the user only asked generically to merge/batch-process/clean up accumulated Dependabot PRs without specifying a `security` or `parallel-auto` token.

**Step 0 — Announce and establish context.** I would open by stating the required announcement line, then run two read-only `gh` calls to anchor the session: `gh repo view --json nameWithOwner --jq .nameWithOwner` and `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`.

**Step 1 — Mode selection.** The user's phrasing contains no `security` or `parallel-auto` tokens, so per the Mode Selection table I default to scope = all Dependabot PRs, execution = sequential. I would not silently assume parallel-auto is wanted just because the phrase "batch-process" was used — that word alone isn't one of the defined tokens, and inventing a mode the user didn't ask for would violate the skill's explicit token-parsing contract. I keep this decision visible in the eventual summary line ("Mode: sequential (all PRs)").

**Step 2 — List PRs.** Run `gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100`, then sort the result ascending by PR number, since the skill is explicit that merge order matters (earlier merges can create conflicts in subsequent PRs).

Gate: if this call returns zero PRs, I stop immediately and report "No Dependabot PRs found" rather than proceeding further.

Gate: if the list exceeds 20 PRs, I pause and ask the user to confirm before continuing, and — per the Notes section — I would proactively recommend switching to `parallel-auto` if the eligible set spans more than one ecosystem (npm, github-actions, python, go, cargo, maven, gradle, docker), since that's explicitly the scenario the skill calls out for that recommendation. This is the one place a clarifying question is built into the procedure, and I would ask it rather than guess.

**Step 3 — Pre-merge checks (per PR, before any merge attempt).** For each PR remaining after scope filtering, I check, in order:
1. Does the diff touch a `FROM` line in any Dockerfile? If so, skip with label `Skipped (Dockerfile)`.
2. Does the PR title ("Bump X from A to B") indicate a major-version bump (leftmost non-zero segment changed)? If so, skip with label `Skipped (Major version upgrade)` — this is a hard skip-and-report, never an auto-merge, per the Rationalization Defense table ("Major version bump looks safe, just merge" is explicitly called out as an excuse to reject).
3. Run `gh pr checks {number} --required` — if required checks haven't all passed, skip with label `Failed (CI not passing)`.

**Step 4 — Sequential merge flow.** For each surviving PR, ascending by number: `gh pr checks {number} --required` (re-confirm), then `gh pr merge {number} --merge`.

If a merge conflict occurs, I do not hand-resolve first — I comment `@dependabot rebase` on the PR (`gh pr comment {number} --body "@dependabot rebase"`) and wait for the rebase to land. Only if that fails to clear the conflict do I fall back to: `gh pr checkout {number}`, resolve conflicts manually, `git add <resolved-files>` naming only the specific resolved files (never a blanket add), `git commit -m "fix: resolve merge conflict for dependabot PR #{number}"`, `git push`, wait for CI to re-run, then `gh pr merge {number} --merge`. If CI fails at any point in this sequence, I skip the PR and record `Failed (CI not passing)` rather than forcing it through.

After each successful merge I note it internally, because a merge can introduce new conflicts in the next queued PR — the final report needs to be able to say "PR #X's merge caused PR #Y's conflict" if that happens.

I explicitly would not invoke `scripts/group-by-ecosystem.py` or any ecosystem-grouping/auto-merge-queue logic (Step 2.5 / 3b), since those only apply when `parallel-auto` is the active execution flag, which it is not here.

**Step 5 — Final summary.** Regardless of how many PRs succeeded, I emit the mandatory per-PR result table (Merged / Skipped / Failed, with reasons) plus total counts, and a "Mode: sequential (all PRs)" header line. Per the Rationalization Defense table, skipping this summary "because everything passed" is explicitly called out as unacceptable, so I always produce it.

**Guardrails I would not cross under any circumstance:** never force-merge or bypass branch protection (if protection blocks a merge, skip + note the specific rule in the report); never auto-merge a major-version bump without explicit user confirmation; never treat a green-CI-but-lockfile-mismatch state as safe to merge (stop and rebase instead); if `gh` isn't authenticated, stop and ask the user to run `gh auth login` rather than attempting workarounds.

**Downstream note.** After merging, I would mention — not automatically invoke — `/ywc-gen-testcase` as an optional follow-up to verify the updated dependency versions don't break existing test coverage, consistent with the skill's declared downstream integration.

I would not refuse or escalate this request outright; the only conditional pause built into the procedure is the >20-PR confirmation gate and the parallel-auto fallback announcement if auto-merge isn't enabled on the repo — both of which I'd surface to the user in real time if triggered, rather than deciding silently on their behalf.</narrative>

