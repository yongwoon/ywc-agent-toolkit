# Dispatch artifact: ywc-release-pr-list (deleted body, run 1)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The request describes the general task (generate a merged PR list grouped by author for a release PR) but does not supply the target release PR number required by $ARGUMENTS. Per Step 1 of the procedure ('If no PR number is provided, stop and report the missing input'), I would halt before doing any work and ask the user to provide the release PR number (e.g. 301) rather than guessing or proceeding against an unspecified PR.

## Actions
- Announce: "I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR."
- Check $ARGUMENTS for a target release PR number per Step 1
- Detect that no PR number was supplied in the request
- Stop before any GitHub API calls and ask the user for the release PR number (e.g. 301)
- (Once a PR number is supplied) validate it is a positive integer; if invalid, stop and report the invalid input
- Ask the single required clarifying question at Step 2: whether to include a per-PR summary alongside the author (yes/no), and wait for the answer before doing any GitHub API work
- Persist summary_mode in memory for the rest of the run without re-prompting
- Run: gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline' to collect commit headlines from the release PR
- Extract merged PR numbers only via 'Merge pull request #(\d+)' and trailing '(#\d+)' patterns, excluding bare '#123' issue-style references
- For each extracted number, run: gh pr view <number> --json state --jq .state to confirm MERGED state; drop any OPEN, CLOSED-not-merged, or erroring numbers
- De-duplicate, sort ascending, and exclude the release PR's own number if present
- If no merged PR numbers can be extracted, stop before editing anything and report what was found in the commit headlines
- Run: bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-number-1> <pr-number-2> ... to fetch author/title/summary/skip status for all extracted PR numbers in one call
- Parse the NDJSON output; for entries with skipped:true, record the reason (not_merged or fetch_error) for the final report instead of guessing
- Build list entries as '- #<PR_NUMBER> @<AUTHOR>' (classic mode) or '- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>' (summary mode) using only the script's derived summary, never fabricating one
- Group entries by author login (alphabetical) and sort PR numbers ascending within each author group
- Run: gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt to snapshot the current PR description
- Write the newly built PR list block (entries only, no heading) to /tmp/pr_list_new.txt
- Run the provided python3 heredoc script against /tmp/pr_body_original.txt and /tmp/pr_list_new.txt to produce /tmp/pr_body_updated.txt, replacing only the '## PR LIST' section (or appending one if absent) and leaving all other content byte-for-byte intact
- Run: gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt to apply the updated description
- Resolve {owner}/{repo} dynamically via gh repo view --json nameWithOwner --jq .nameWithOwner if needed for context
- If gh is unavailable or unauthenticated at any point, stop immediately and report the blocker rather than improvising
- Produce a final report noting: summary_mode chosen (or defaulted), any skipped/unresolvable PR numbers with reasons, and any entries that fell back to classic format due to missing summary material

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-release-pr-list-27-27.md (read only, procedure source)
- /tmp/pr_body_original.txt (would create, scratch)
- /tmp/pr_list_new.txt (would create, scratch)
- /tmp/pr_body_updated.txt (would create, scratch)
- claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh (would invoke, not edit)

## Gates enforced
- Step 1 gate: PR number must be present and a positive integer in $ARGUMENTS, else stop and report missing/invalid input
- Step 2 gate: must ask the single summary-mode question before any GitHub API work and wait for the answer; never silently enable summary_mode; never re-prompt mid-run once set
- PR-number extraction gate: only 'Merge pull request #(\d+)' and trailing '(#\d+)' patterns count as merged-PR references; bare '#123' style issue/cross-references are excluded
- Merge-state verification gate: every extracted number must be confirmed MERGED via gh pr view --json state before inclusion; OPEN/CLOSED-not-merged/error results are skipped and reported, never guessed
- No-extractable-PRs gate: if extraction yields nothing, stop before editing and report the raw findings
- Author resolution gate: never guess or leave an author blank; unresolved PRs are reported explicitly instead of written with incomplete data
- No-fabrication gate: summaries must derive from the script's title/body-based logic; if no usable line exists, that single entry falls back to classic format and is flagged in the final report, never invented
- Description-preservation gate: the update must touch only the '## PR LIST' section via the provided Python replace script — never hand-construct or rewrite the full body, never reorder/delete other sections
- Anti-truncation gate: long PR lists are written in full, never abbreviated with '... and more'
- Tooling-availability gate: if gh is unavailable/unauthenticated, stop and report the blocker rather than proceeding with partial data

## Full narrative

I would begin by announcing that I'm using the ywc-release-pr-list procedure to compile the merged PR list for the release PR, as the procedure requires that announcement at the start.

Next, per Step 1 ("Identify the target PR"), I would look for the release PR number in the arguments the user supplied. The user's message describes the general scenario — working on a release PR such as develop→main and wanting the merged PR list grouped by author — but does not actually give me a concrete PR number (nothing like "301" or a URL pointing at a specific PR). The procedure is explicit here: "If no PR number is provided, stop and report the missing input." So at this point I would not run any `gh` commands, not touch any files, and not proceed further. I would stop and ask the user directly for the release PR number, e.g.: "Could you provide the release PR number you'd like me to compile the merged PR list for (for example, 301)?"

I would not attempt to infer the PR number from `git branch --show-current` or `git log --oneline -5` context, since the procedure's context block only supplies situational awareness, not a substitute for the required `$ARGUMENTS` input, and the validation rule is unambiguous about halting on missing input.

Assuming the user then supplies a valid PR number, here is exactly how I would carry the rest of the procedure forward, concretely:

1. Validate the number is a positive integer; if not, stop and report the invalid input instead of attempting a lookup.
2. Ask the user exactly one question before any GitHub API work: whether they want a short per-PR summary alongside the author (yes/no), and wait for their reply. An affirmative answer sets `summary_mode = true`; a negative sets it `false`; an ambiguous answer triggers exactly one re-ask, after which an unresolved response defaults to `summary_mode = false` with an explicit note of that default in my final report. Once set, I would not re-prompt for this later in the run.
3. Run `gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'` to pull the release PR's commit headlines.
4. Extract merged PR numbers using only the two sanctioned patterns — `Merge pull request #(\d+)` for merge commits and trailing `(#\d+)` for squash merges — explicitly excluding stray `#123`-style issue or cross references appearing mid-message (e.g. "fix #123"). For every extracted number I would run `gh pr view <number> --json state --jq .state` to confirm it is actually `MERGED`, dropping (and noting) any that come back `OPEN`, `CLOSED` (unmerged), or error out. I'd then de-duplicate, sort ascending, and drop the release PR's own number if it appears in its own history.
5. If that extraction yields nothing, I would stop before touching the PR description and report exactly what commit headlines were found, rather than guessing or inventing a list.
6. For the surviving PR numbers, I would run the bundled script in one call: `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-number-1> <pr-number-2> ...`, parse its NDJSON output, and use `author` (classic mode) or `author` + `summary` (summary mode) per entry. Any line with `skipped:true` (reason `not_merged: ...` or `fetch_error`) would be excluded from the list and called out in my final report rather than left blank or guessed.
7. I would format each entry as `- #<PR_NUMBER> @<AUTHOR>` in classic mode, or `- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>` in summary mode — using only the script-derived summary text, never fabricating a summary; any entry where no usable summary material exists would fall back to the classic single-line format for that entry and get flagged in my report.
8. I would group entries by author login alphabetically, and within each author group sort PR numbers ascending.
9. To update the PR description safely, I would first snapshot the existing body with `gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt`, write the newly built list block (entries only) to `/tmp/pr_list_new.txt`, then run the provided `python3` heredoc script against those two files to produce `/tmp/pr_body_updated.txt` — this script replaces only the `## PR LIST` section (matching from that heading through to the next `## ` heading or end of file) and appends a new `## PR LIST` section only if none exists, leaving every other section byte-for-byte untouched. I would deliberately not hand-construct the new body string myself, since the procedure explicitly forbids that to avoid accidentally clobbering unrelated sections.
10. Finally, I would apply the update with `gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt`.

Throughout, if `gh` turned out to be unavailable or unauthenticated at any step, I would stop immediately and report that blocker rather than trying to work around it (for example, by trying to scrape data some other way). I would also resolve `{owner}/{repo}` dynamically via `gh repo view --json nameWithOwner --jq .nameWithOwner` if I needed repository context for any of the above calls, rather than assuming or hardcoding a repository name.

At the end of a successful run, I would produce a final report noting: which `summary_mode` was used (and whether it was a default rather than an explicit user choice), any PR numbers that were skipped along with their reasons (not merged, fetch error, or missing commit-header pattern), and any entries that fell back from summary to classic format because no usable summary text was available — consistent with the procedure's instruction never to fabricate data and never to truncate long lists.

But all of that is contingent on the user first supplying the release PR number, which the current request does not include. So, as things stand, my next concrete action would be to ask that one clarifying question and wait, rather than run any `gh`, `git`, or script commands.</narrative>
</StructuredOutput>


