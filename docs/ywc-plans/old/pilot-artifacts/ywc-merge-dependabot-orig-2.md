# Dispatch artifact: ywc-merge-dependabot (original body, run 2)

**Key**: claude-code/skills/ywc-merge-dependabot/SKILL.md:24-24
**Scenario**: I need help with the following: the user wants to merge Dependabot PRs, batch-process dependency updates, or clean up accumulated Dependabot PRs.
**Variant**: original
**Refused/escalated**: False


## Actions
- Read claude-code/skills/ywc-merge-dependabot/SKILL.md (procedure)
- Announce skill usage per the mandated announce line
- Run gh repo view --json nameWithOwner --jq .nameWithOwner
- Run gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
- Parse $ARGUMENTS for scope token (security) and execution token (parallel-auto); none present -> default: all PRs, sequential
- Run gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100
- Sort resulting PR list ascending by PR number
- If PR count > 20, stop and ask user for confirmation before proceeding (and suggest parallel-auto if multi-ecosystem)
- For each PR: check Dockerfile FROM change (skip if match)
- For each PR: run scripts/detect-major-bump.py --title <title> (or infer from 'Bump X from A to B') to gate major version bumps (skip + report, no auto-merge)
- For each PR: run gh pr checks {number} --required to confirm CI is green (skip if not passing)
- For each eligible PR (ascending order): run gh pr merge {number} --merge
- On merge conflict: comment '@dependabot rebase' on the PR first, wait for Dependabot
- If rebase does not clear conflict: gh pr checkout {number}; resolve conflicts; git add <resolved-files>; git commit -m 'fix: resolve merge conflict for dependabot PR #{number}'; git push; wait for CI; gh pr merge {number} --merge
- If conflict cannot be resolved cleanly or CI fails post-resolution, skip PR and record failure reason
- After each merge, note whether it could affect conflict surface of subsequent queued PRs
- Compile Final Summary per the skill's required table format (Mode line, per-PR result, totals merged/skipped/failed)
- On gh CLI auth failure: stop and ask user to run gh auth login (do not proceed)
- On zero Dependabot PRs found: report 'No Dependabot PRs found' and stop
- On rate limit hit: wait and retry, or stop and report partial progress
- On branch protection blocking merge: skip PR, note the protection rule in report, never force-merge or bypass
- After completion, mention /ywc-gen-testcase as an optional downstream follow-up to verify updated packages

## Files touched
- claude-code/skills/ywc-merge-dependabot/SKILL.md (read only, procedure source)
- claude-code/skills/ywc-merge-dependabot/scripts/detect-major-bump.py (invoked, not modified)
- claude-code/skills/ywc-merge-dependabot/scripts/group-by-ecosystem.py (only if parallel-auto were selected; not used in this default-mode run)

## Gates enforced
- Dockerfile FROM change skip gate
- Major version upgrade skip gate (requires explicit user confirmation, default action = skip and report)
- CI status must-pass gate before any merge attempt
- gh CLI authentication gate (stop and ask, do not proceed)
- >20 PR batch-size confirmation gate before proceeding
- Branch protection respected — never force-merge or bypass
- Merge-conflict resolution order gate (@dependabot rebase first, manual resolution only as fallback, skip if unresolved)
- Security-mode CVE/advisory presence gate (only relevant if 'security' token were passed)
- Final per-PR summary table mandatory (merged/skipped/failed), never omitted

## Full narrative

Here is exactly what I would do, step by step, under the ywc-merge-dependabot procedure, given the user's request to merge Dependabot PRs / batch-process dependency updates / clean up accumulated Dependabot PRs (no explicit mode flags supplied).

**1. Announce and gather context**
I would open by stating: "I'm using the ywc-merge-dependabot skill to merge Dependabot PRs with CI verification — sequential by default, or parallel-auto (ecosystem-grouped queue) when requested." Then run:
- `gh repo view --json nameWithOwner --jq .nameWithOwner`
- `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`

**2. Resolve mode**
The user's phrasing contains no `security` or `parallel-auto` tokens, so per the Mode Selection table this defaults to: scope = all Dependabot PRs, execution = sequential (one PR at a time, ascending PR number). I would not stop to ask a clarifying question here, since the skill defines an explicit default for the empty-argument case — asking would be unnecessary friction. I would, however, surface the resolved mode to the user in my final report so they can see what ran.

**3. List Dependabot PRs (Step 1)**
- `gh pr list --author "app/dependabot" --state open --json number,title,labels,body --limit 100`
- Sort the returned list ascending by PR number (processing order matters — earlier merges can create conflicts in later PRs).
- If the list is empty: report "No Dependabot PRs found" and stop — no further action.
- If the list has more than 20 entries: stop and ask the user for explicit confirmation before proceeding, and if the eligible set spans more than one ecosystem, recommend switching to `parallel-auto` mode instead.

**4. Pre-merge checks per PR (Step 2)**
For each PR, before attempting any merge:
- Check whether the PR touches a `FROM` line in any Dockerfile → if so, skip with label `Skipped (Dockerfile)`.
- Determine if it's a major version bump. I would invoke the bundled deterministic script rather than eyeballing the title: `python3 <skill-dir>/scripts/detect-major-bump.py --title "<PR title>"`, resolving `<skill-dir>` relative to the skill folder itself (not the target repo). If the script returns `major_bump: true`, skip with label `Skipped (Major version upgrade)` and flag it for explicit human confirmation — I would never auto-merge a major bump. If it returns `null` (undecidable), I'd fall back to manual inspection of the "Bump X from A to B" title pattern.
- Check CI status: `gh pr checks {number} --required`. If required checks have not all passed, skip with label `Failed (CI not passing)`.

**5. Skip ecosystem grouping (Step 2.5)**
Since this is sequential mode (no `parallel-auto` token), I would skip the `group-by-ecosystem.py` classification step entirely — it only applies to parallel-auto.

**6. Sequential merge flow (Step 3a)**
For each PR that passed all pre-merge checks, in ascending PR-number order:
- `gh pr checks {number} --required` (re-confirm just before merge)
- `gh pr merge {number} --merge`

If a merge conflict occurs, I would resolve it in the mandated order — never jump straight to manual resolution:
1. First comment `@dependabot rebase` on the PR and wait for Dependabot to push a rebase.
2. Only if that fails to clear the conflict, fall back to:
   - `gh pr checkout {number}`
   - resolve conflicts manually
   - `git add <resolved-files>` (explicitly staged, never a blanket `git add -A`)
   - `git commit -m "fix: resolve merge conflict for dependabot PR #{number}"`
   - `git push`
   - wait for CI to re-run, then `gh pr merge {number} --merge`
   - if the conflict cannot be resolved cleanly, skip the PR and record the failure.

If CI fails at any point (initial check, or after conflict resolution), I would skip that PR and record the failure rather than force it through. After every successful merge I would note it internally, since it can introduce conflicts into the next queued PR — this is the "note the merge, watch for downstream conflicts" discipline the skill calls out.

Throughout, I would never force-merge, never bypass branch protection, and never hand-resolve a conflict as the first move — only as the documented fallback after a failed Dependabot rebase attempt.

**7. Error handling gates**
- If `gh` is not authenticated, I would stop immediately and ask the user to run `gh auth login` — I would not attempt any workaround.
- If a GitHub rate limit is hit mid-run, I would either wait and retry or stop and report progress so far, rather than silently dropping remaining PRs.
- If branch protection blocks a merge, I would skip that PR, note the specific protection rule in the final report, and move on — never bypass it.

**8. Final summary (Step 4)**
Regardless of outcome, I would always emit a per-PR result table in the mandated format, e.g.:

```
## Dependabot Merge Results

Mode: sequential (all PRs)

- ✅ Merged    : #123 Bump axios from 1.6.0 to 1.7.2
- ⏭️ Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- ⏭️ Skipped   (Major version)  : #130 Bump webpack from 4.46.0 to 5.90.0
- ❌ Failed    (CI not passing) : #132 Bump express from 4.18.0 to 4.19.2

Total: 1 merged / 2 skipped / 1 failed
```

I would never omit this summary even if every PR succeeded — "all passed, no summary needed" is explicitly called out in the skill as a disallowed shortcut.

**9. Downstream follow-up**
After the run, I would mention `/ywc-gen-testcase` as an optional next step to verify the newly merged dependency versions don't break existing test coverage — this is the skill's documented downstream integration, not something I'd invoke automatically.

**Points where I would stop or escalate rather than proceed silently:**
- `gh` unauthenticated → hard stop, ask user to authenticate.
- Zero Dependabot PRs → report and stop.
- Batch of >20 PRs → stop and ask for explicit confirmation before merging anything.
- Any major version bump → never auto-merge; always skip and surface for human review.
- Any PR requested under `security` scope lacking a CVE/advisory reference → skip and report (not applicable here since no `security` token was given, but I'd apply it if the user later asked for security-only mode).
- Genuine unresolved merge conflicts after the Dependabot-rebase attempt → skip that specific PR rather than force a resolution.

I do not have live repository access in this session, so none of the `gh`/`git` commands above were actually executed — this is the precise sequence I would run, in order, with the exact skip/escalate conditions I would honor, if I were operating against a real repository under this procedure.
