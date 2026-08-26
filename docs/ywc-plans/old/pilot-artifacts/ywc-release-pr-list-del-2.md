# Dispatch artifact: ywc-release-pr-list (deleted body, run 2)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The user's request did not include the target release PR number, which the procedure requires as a hard precondition (Step 1: validate a positive integer PR number is present; if none is provided, stop and report the missing input) before any GitHub API work, including the mandatory summary-mode question, can begin.

## Actions
- Announce skill usage: 'I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR.'
- Validate that $ARGUMENTS contains a positive integer PR number
- Since no PR number was supplied in the request, stop before any GitHub calls and ask the user for the target release PR number (e.g. 301)
- (Once PR number is supplied) Run: gh repo view --json nameWithOwner --jq .nameWithOwner to resolve {owner}/{repo}
- (Once PR number is supplied) Ask the user exactly one yes/no question: 'Would you like to include a short summary of what each PR applied alongside the author? (yes / no)' and wait for the reply before doing any GitHub API work; store summary_mode and do not re-prompt later
- Run: gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline' to collect commit headlines from the release PR
- Parse headlines with the two allowed patterns only: 'Merge pull request #(\d+)' and trailing '(#\d+)'; explicitly ignore mid-sentence '#123' references (issue refs / cross-references)
- For each extracted number, run gh pr view <number> --json state --jq .state to confirm MERGED; drop any OPEN, CLOSED-not-merged, or erroring numbers; dedupe; sort ascending; exclude the release PR's own number
- Run: bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-number-1> <pr-number-2> ... to fetch author/title/summary/skip-reason for all extracted PR numbers in one call, and parse the NDJSON output
- Report to the user any entries with skipped:true (not_merged or fetch_error) rather than silently dropping them
- Build list entries: classic mode '- #<PR_NUMBER> @<AUTHOR>' or summary mode '- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>' per the earlier answer; for any PR where no usable summary can be derived, fall back to classic format for that entry only and note it in the final report
- Group entries by author login, sort author groups alphabetically, sort PR numbers ascending within each group
- Run: gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt
- Write the newly built PR-list entries (no heading) to /tmp/pr_list_new.txt
- Run the provided python3 heredoc script against /tmp/pr_body_original.txt and /tmp/pr_list_new.txt to produce /tmp/pr_body_updated.txt, replacing only the '## PR LIST' section (or appending it if absent) and leaving all other body content byte-for-byte untouched
- Run: gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt to publish the updated description
- Do not manually reconstruct the PR body string by hand — only the python script output is used for the edit
- Give a final report summarizing: total merged PRs included, author groups, any skipped/unresolvable PR numbers, any commit headlines whose PR numbers were skipped, whether summary_mode defaulted due to an ambiguous answer, and any entries that fell back to classic format despite summary_mode being on

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-release-pr-list-27-27.md (read only, as instructed)
- claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh (executed, not edited)
- /tmp/pr_body_original.txt (created)
- /tmp/pr_list_new.txt (created)
- /tmp/pr_body_updated.txt (created)

## Gates enforced
- PR number validation (positive integer, must be present) before any work
- Single required yes/no prompt for summary_mode, asked before any GitHub API calls, never re-prompted mid-run
- Commit-headline PR-number extraction restricted to the two reliable regex patterns only — no arbitrary '#123' matches
- Merged-state verification via gh pr view --json state for every extracted PR number before inclusion
- No truncation of long PR lists
- No fabrication of authors or summaries — unresolved/ambiguous entries are reported, not guessed
- PR description edit restricted to the '## PR LIST' section only, verified via the byte-preserving python script rather than manual string construction
- Stop-and-report gates for: missing/invalid PR number, gh unavailable/unauthenticated, and zero extractable merged PR numbers

## Full narrative

I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR.

Before I can do anything else, I need the target release PR number (e.g. 301) — the procedure requires validating that a positive integer PR number is present before touching GitHub in any way, and your message didn't include one. Could you provide the release PR number (the develop→main PR whose description should get the merged-PR list)?

Once you give me that number, here is exactly what I'll do:

1. Resolve the repo with `gh repo view --json nameWithOwner --jq .nameWithOwner`.
2. Ask you one question and wait for your answer before doing any further API work: "Would you like to include a short summary of what each PR applied alongside the author? (yes / no)" — I will not proceed with GitHub calls until you answer, and I won't re-ask later in the run.
3. Pull the release PR's commit headlines: `gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'`.
4. Extract merged PR numbers using only the two reliable patterns — `Merge pull request #(\d+)` and trailing `(#\d+)` — deliberately ignoring stray `#123` references that are issue mentions or cross-references, not merges. Each surviving number gets checked with `gh pr view <number> --json state --jq .state`; anything not `MERGED` is dropped. I'll dedupe, sort ascending, and drop the release PR's own number if present.
5. Fetch author/title/summary/merge-state for all surviving numbers in one call: `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <numbers...>`, parsing the NDJSON output. Any line with `skipped:true` gets flagged in my final report rather than silently dropped.
6. Build entries — classic `- #<PR_NUMBER> @<AUTHOR>` or, if you opted into summaries, `- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>`. If a PR has no usable title/body to derive a summary from, I fall back to classic format for that single entry and call it out at the end rather than inventing text.
7. Group entries by author login (alphabetical), and sort PR numbers ascending within each author's group.
8. Save the current PR body with `gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt`, write the new entries to `/tmp/pr_list_new.txt`, then run the provided python3 script against both files to produce `/tmp/pr_body_updated.txt` — this replaces only the `## PR LIST` section (or appends one if it doesn't exist yet) and leaves every other part of the description untouched, byte-for-byte. I will not hand-assemble the body text myself.
9. Publish the update with `gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt`.
10. Close out with a report: which PRs were included and how they were grouped, any PR numbers found in commit headlines but skipped (not merged, fetch error, or excluded as non-PR references), whether summary_mode defaulted because your answer was ambiguous, and any entries that fell back to classic format despite summary mode being on.

Along the way I will stop and report rather than proceed if: `gh` is unavailable or unauthenticated, no merged PR numbers can be extracted from the commit headlines at all, or any commit headline's PR number can't be resolved even after retrying the `gh pr view` lookup — in none of these cases would I guess, leave fields blank, or truncate the list, since this description doubles as an audit record of who contributed what to the release.
