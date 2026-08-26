# Dispatch artifact: ywc-release-pr-list (original body, run 3)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: Step 1 of the procedure requires $ARGUMENTS to contain the target release PR number (a positive integer). The user's request describes the scenario (release PR, develop→main, merged PR list grouped by author) but does not supply an actual PR number. Per the explicit rule 'If no PR number is provided, stop and report the missing input,' the correct action is to halt before any gh/GitHub API work and ask the user for the release PR number, rather than guessing one or proceeding with a placeholder.

## Actions
- Read claude-code/skills/ywc-release-pr-list/SKILL.md (the full and only procedure followed)
- Announce skill invocation per the SKILL.md's mandated opening line
- Step 1: Attempt to read the target release PR number from $ARGUMENTS
- Step 1: Validate PR number is a positive integer
- Since no PR number was supplied in this request, stop before any GitHub API work and report the missing input back to the user
- (Deferred until PR number supplied) Step 2: ask the summary_mode yes/no question and wait
- (Deferred) Step 3: gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'
- (Deferred) Step 4: run scripts/extract-merged-prs.sh (or equivalent regex extraction) then gh pr view <n> --json state --jq .state per candidate to confirm MERGED
- (Deferred) Step 5: bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr...> for author/title/summary in one batched call
- (Deferred) Step 6: group entries by author alphabetically, sort PR numbers ascending within each group
- (Deferred) Step 7: gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt, write /tmp/pr_list_new.txt, run the provided python3 section-replacement script to produce /tmp/pr_body_updated.txt, then gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt
- (Deferred) Resolve {owner}/{repo} via gh repo view --json nameWithOwner --jq .nameWithOwner if needed

## Files touched
- claude-code/skills/ywc-release-pr-list/SKILL.md (read only)

## Gates enforced
- Step 1 input validation: PR number must be a positive integer present in $ARGUMENTS; missing input halts before any work
- Rationalization Defense table: no step may be skipped as an 'excuse', including not silently defaulting or guessing a PR number
- Step 2 opt-in summary_mode question must be asked exactly once and answered before GitHub API work begins (not yet reached)
- Author resolution must never be left blank; failures are retried via gh pr view, not silently skipped
- Only the ## PR LIST section of the target PR description may be modified; everything else preserved byte-for-byte
- No truncation of PR lists regardless of length
- gh availability/authentication check before proceeding is an implicit blocker condition

## Full narrative

I read claude-code/skills/ywc-release-pr-list/SKILL.md in full and treated it as the sole procedure. Here is exactly what I would do, step by step, if I were actually executing this request.

First, per the skill's required opening, I would announce: "I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR."

Then I move to Step 1 ("Identify the target PR"): the procedure requires reading the release PR number out of `$ARGUMENTS`, validating it's a positive integer, and explicitly says: "If no PR number is provided, stop and report the missing input." The request as given only restates the trigger scenario — "working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author" — it does not include an actual PR number (the example in the skill's own docs is something like `301`). Since no concrete number is present, I would stop right here, before touching `gh` at all, and ask the user directly for the target release PR number, e.g.: "Could you provide the release PR number (e.g., 301) for the PR whose description should receive the merged PR list?"

I would not guess a PR number, infer one from the current branch, or silently pick the most recent open PR — the Rationalization Defense table explicitly frames this class of shortcut as against the spirit of the skill (treating it as an audit artifact), and Step 1 has no fallback path other than asking.

If/when the user supplies a PR number (say `301`), the rest of the procedure I would carry out is:

1. Validate `301` is a positive integer.
2. Step 2 — ask exactly one question and wait: "Would you like to include a short summary of what each PR applied alongside the author? (yes / no)" and set `summary_mode` accordingly (defaulting to `false` with an explicit note only if the answer stays ambiguous after one re-ask). I would not re-prompt later.
3. Step 3 — run `gh pr view 301 --json commits --jq '.commits[].messageHeadline'` to collect commit headlines from the release PR.
4. Step 4 — extract merged PR numbers using only the two anchored patterns (`Merge pull request #(\d+)` and trailing `(#\d+)`), explicitly not matching arbitrary `#123` references like `fix #123`. I'd use `claude-code/skills/ywc-release-pr-list/scripts/extract-merged-prs.sh --exclude 301` for the pure-text extraction, then confirm each candidate is actually merged via `gh pr view <number> --json state --jq .state`, skipping any `OPEN`/non-merged/erroring numbers, deduping and sorting ascending, and excluding 301 itself.
5. Step 5 — fetch author/title/summary/state for all extracted numbers in one batched call: `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <n1> <n2> ...`, parse the NDJSON output, and build entries as `- #<N> @<author>` (classic) or `- #<N> @<author> — <summary>` (summary mode) depending on the answer from Step 2. Any `skipped:true` entries (not_merged or fetch_error) get reported, not fabricated.
6. Step 6 — group entries by author login, sort author groups alphabetically, and sort PR numbers ascending within each group.
7. Step 7 — save the current body via `gh pr view 301 --json body --jq '.body' > /tmp/pr_body_original.txt`, write the new list-only content to `/tmp/pr_list_new.txt`, run the provided `python3` script (verbatim, not a hand-rolled string replace) against those two files to produce `/tmp/pr_body_updated.txt` — which replaces only the `## PR LIST` section and leaves everything else byte-for-byte intact — and finally apply it with `gh pr edit 301 --body-file /tmp/pr_body_updated.txt`.

Throughout, I would resolve `{owner}/{repo}` dynamically via `gh repo view --json nameWithOwner --jq .nameWithOwner` only if needed for any of the above calls, and I would stop and report a blocker if `gh` turns out to be unavailable or unauthenticated, or if no merged PR numbers can be extracted from the commit headlines at all (rather than editing the PR with an empty or partial list).

But none of steps 2–7 happen yet in this actual turn, because the gating condition in Step 1 — a concrete PR number — was never satisfied. The correct and only action here is to stop and ask the user for that PR number before doing any `gh` work.</narrative>

