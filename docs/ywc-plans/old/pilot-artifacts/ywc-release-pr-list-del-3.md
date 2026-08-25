# Dispatch artifact: ywc-release-pr-list (deleted body, run 3)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The procedure's Step 1 requires a target release PR number to be present in the input, and explicitly instructs: 'If no PR number is provided, stop and report the missing input.' The user's request describes the general scenario (compiling a merged PR list grouped by author for a release PR) but does not supply an actual PR number, so per the procedure I would halt before doing any GitHub API work and ask the user to provide the release PR number (e.g., 301) rather than guessing or defaulting to the current branch's PR.

## Actions
- Announce skill start: 'I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR.'
- Check $ARGUMENTS for a release PR number per Step 1 of the procedure
- Detect that no PR number was supplied in the request
- Stop before any GitHub API work and report the missing input, asking the user to supply the target release PR number (e.g., 301)
- (Conditional, only after a valid PR number is supplied) Ask exactly one question: whether to include a per-PR summary alongside each author, and wait for yes/no before proceeding; on ambiguous answer, ask once more, then default to summary_mode=false if still unclear and note the default in the final report
- (Conditional) Run `gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'` to collect commit headlines from the release PR
- (Conditional) Extract merged PR numbers using only the 'Merge pull request #(\d+)' and trailing '(#\d+)' patterns, explicitly excluding arbitrary '#<number>' references like 'fix #123' or 'see #456'
- (Conditional) Validate each extracted number with `gh pr view <number> --json state --jq .state`, skipping any that are OPEN, CLOSED-not-merged, or error out; dedupe, sort ascending, and exclude the release PR's own number
- (Conditional) Run `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-numbers...>` to fetch author/title/summary/state for all extracted PRs in one call, treating exit 2 as usage error and per-line 'skipped' entries as unresolved/not-merged
- (Conditional) Build entries as `- #<PR_NUMBER> @<AUTHOR>` (classic) or `- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>` (summary mode), never fabricating a summary — fall back to classic format for any single entry lacking a usable title/body line and note it in the final report
- (Conditional) Group entries by author login, sort author groups alphabetically, sort PR numbers ascending within each group
- (Conditional) Run `gh pr view <PR_NUMBER> --json body --jq '.body'` and save to /tmp/pr_body_original.txt
- (Conditional) Write the new PR list entries (no heading) to /tmp/pr_list_new.txt
- (Conditional) Run the provided python3 script against the original body and new list to regenerate /tmp/pr_body_updated.txt, replacing only the '## PR LIST' section and preserving all other content byte-for-byte
- (Conditional) Run `gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt` to publish the updated description
- (Conditional) Resolve {owner}/{repo} via `gh repo view --json nameWithOwner --jq .nameWithOwner` as needed
- (Conditional) If `gh` is unavailable/unauthenticated, or if no merged PR numbers can be extracted, stop before editing and report the blocker/findings instead of proceeding

## Files touched
- /tmp/pr_body_original.txt (would be created via gh pr view redirect)
- /tmp/pr_list_new.txt (would be written with the new PR LIST entries)
- /tmp/pr_body_updated.txt (would be produced by the python3 merge script)
- claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh (would be invoked, not edited)

## Gates enforced
- Step 1 validation: release PR number must be present and a positive integer; missing/invalid input halts the workflow before any other action
- Step 2 opt-in gate: summary_mode must be explicitly asked and confirmed once, never assumed or silently enabled, never re-prompted mid-run
- Step 4 extraction discipline: only 'Merge pull request #(\d+)' and trailing '(#\d+)' patterns count as merged-PR references; arbitrary '#N' mentions are excluded
- Step 4 merge-state verification: each extracted number re-validated via gh pr view --json state before inclusion
- Step 5 author-resolution gate: no blank/guessed authors; unresolved PRs are reported, not silently dropped
- Step 5 no-fabrication gate: summaries must derive from real title/body content; unusable ones fall back to classic format for that entry and get flagged in the final report
- Rationalization Defense table: no skipping missing PR numbers, no leaving blank authors, no switching to date-based grouping, no truncating long lists
- Decision Rules: gh availability/auth check — stop and report if gh is unavailable or unauthenticated
- Decision Rules: if no merged PR numbers extractable, stop before editing and report findings
- Description-preservation gate: only the '## PR LIST' section may be modified; all other content and order must remain byte-for-byte intact, enforced via the dedicated python3 replace script rather than manual string construction

## Full narrative

Here is exactly how I would proceed under the ywc-release-pr-list procedure.

First, I would announce that I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR, then move to Step 1: identify the target PR. The procedure requires the target release PR number to come from `$ARGUMENTS`, validated as a positive integer, and states plainly: "If no PR number is provided, stop and report the missing input." The user's message describes the scenario in general terms (a develop→main release PR, wanting a merged PR list grouped by author) but does not actually supply a PR number.

Because of that, I would stop right here rather than guessing which PR is meant (e.g., by assuming it's whatever PR is open on the current branch) or silently proceeding with a placeholder. I would report back to the user that a target release PR number is required and ask them to supply it — for example: "Could you provide the release PR number this applies to (e.g., 301)?" I would not run any `gh` commands, touch any files, or take any other action until that number is given, since every subsequent step in the procedure (commit collection, PR-number extraction, author resolution, description rewrite) is keyed off that PR number.

If the user then supplied a valid PR number, I would continue exactly as specified:

- Step 2: Before any GitHub API calls, I would ask the user exactly one question — "Would you like to include a short summary of what each PR applied alongside the author? (yes / no)" — and wait for a response. A clear yes/y sets `summary_mode = true`; a clear no/n sets it `false`; an ambiguous answer gets one follow-up ask, after which I'd default to `false` and explicitly flag that default in my final report. I would not re-ask this later.

- Step 3: I would run `gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'` to pull the release PR's commit headlines.

- Step 4: I would extract merged-PR numbers using only two patterns — `Merge pull request #(\d+)` and a trailing `(#\d+)` from squash-merge headlines — explicitly declining to treat stray `#123` references like `fix #123` or `see #456` as merged PRs. For every extracted number I would confirm merged status with `gh pr view <number> --json state --jq .state`, discarding anything `OPEN`, `CLOSED` (not merged), or erroring. I'd dedupe, sort ascending, and drop the release PR's own number if present.

- Step 5: I would fetch author/title/summary/state for all remaining numbers in a single call to `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-number-1> <pr-number-2> ...`, treating exit code 2 as a usage error and parsing NDJSON output, skipping entries marked `"skipped":true` while noting the reason (e.g., `not_merged`, `fetch_error`) for the final report. I would never guess an author for an unresolved PR — I'd report it instead. Entries would be built as `- #<N> @<author>` in classic mode, or `- #<N> @<author> — <summary>` in summary mode, with the rule that summaries are never fabricated; if neither title nor body yields a usable line, that single entry falls back to classic format and gets flagged.

- Step 6: I would group entries by author login, sort author groups alphabetically, and sort PR numbers ascending within each group.

- Step 7: I would save the current description via `gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt`, write the newly built list (entries only, no heading) to `/tmp/pr_list_new.txt`, then run the provided python3 script (invoked exactly as given in the procedure, taking the original body file, the new list file, and an output path as positional args) to regenerate `/tmp/pr_body_updated.txt` — this script replaces only the `## PR LIST` section via regex and leaves everything else byte-for-byte untouched, appending a new `## PR LIST` section at the end only if none exists. I would not hand-construct the merged body string myself, per the procedure's explicit warning. Finally I would run `gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt` to publish the update.

Throughout, I would resolve `{owner}/{repo}` dynamically via `gh repo view --json nameWithOwner --jq .nameWithOwner` if needed, and I would halt and report a blocker rather than proceed if `gh` turned out to be unavailable or unauthenticated, or if Step 4 yielded zero extractable merged-PR numbers.

But none of that runs yet — the very first gate in the procedure (a valid release PR number) is not satisfied by the request as given, so my concrete next action is to ask the user for that PR number and wait.
