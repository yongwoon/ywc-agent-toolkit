# Dispatch artifact: ywc-release-pr-list (original body, run 2)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The procedure's Step 1 (\"Identify the target PR\") explicitly requires: \"If no PR number is provided, stop and report the missing input.\" The user's message describes the scenario (release PR, develop→main, merged PR list grouped by author) but does not supply an actual PR number in $ARGUMENTS, so per the skill I must halt before any gh/API work and ask for it rather than guessing or picking the most recent release PR.

## Actions
- Read claude-code/skills/ywc-release-pr-list/SKILL.md in full (only action taken)
- Would announce: "I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR."
- Would check $ARGUMENTS for a target release PR number
- Since no PR number was supplied in the request, would stop at Step 1 and ask the user for the release PR number (e.g., 301) rather than proceeding

## Files touched
- claude-code/skills/ywc-release-pr-list/SKILL.md (read only)

## Gates enforced
- Step 1 input validation gate (PR number must be a positive integer; missing input halts the workflow before any GitHub API calls)

## Full narrative

I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR.

Here is exactly how I would carry this out under the procedure in claude-code/skills/ywc-release-pr-list/SKILL.md.

**Step 1 — Identify the target PR.** The skill requires the target release PR number to come from `$ARGUMENTS` (e.g., `301`), validated as a positive integer. The request as given only describes the situation ("working on a release PR, develop→main, generate merged PR list grouped by author") without an actual PR number. Per the Decision Rules and Step 1, this is a hard stop condition: "If no PR number is provided, stop and report the missing input." So at this point I would not run any `gh` commands at all — I would pause and ask you directly: "Which release PR number should I compile the merged PR list for (e.g., 301)?"

Assuming you then supplied a number, here is exactly what I would do next, in order:

**Step 2 — Ask about summaries.** Before touching the GitHub API, I would ask exactly one question and wait: "Would you like to include a short summary of what each PR applied alongside the author? (yes / no)" I would set `summary_mode` based on your answer (re-asking once if ambiguous, defaulting to `false` with an explicit note if still unclear), and would not re-prompt for this later.

**Step 3 — Collect commit headlines.** I would run:
`gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'`

**Step 4 — Extract merged PR numbers.** I would either run the bundled helper `bash claude-code/skills/ywc-release-pr-list/scripts/extract-merged-prs.sh --exclude <PR_NUMBER>` or manually apply only the two anchored patterns (`Merge pull request #(\d+)` and trailing `(#\d+)` squash format) against the headlines — explicitly not matching stray `#123` references like `fix #123` or `see #456`. I would then validate each extracted number with `gh pr view <number> --json state --jq .state`, discarding anything that isn't a merged state, dedupe, sort ascending, and exclude the release PR's own number if present.

**Step 5 — Resolve author/summary per PR.** I would run the bundled script in one call:
`bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-1> <pr-2> ...`
and parse the NDJSON output, using `author` (classic mode) or `author` + `summary` (summary mode) for each non-skipped entry, and collecting `skipped` entries (with `reason`) to report at the end rather than silently dropping them.

**Step 6 — Group and sort.** I would group entries by author login, sort author groups alphabetically, and sort PR numbers ascending within each group.

**Step 7 — Update the release PR description.** I would:
1. Save the current body: `gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt`
2. Write the newly built entries-only list to `/tmp/pr_list_new.txt` (classic format `- #123 @alice` or summary format `- #123 @alice — <summary>` depending on the earlier answer).
3. Run the exact Python snippet embedded in the skill (via `python3 - /tmp/pr_body_original.txt /tmp/pr_list_new.txt /tmp/pr_body_updated.txt <<'PYEOF' ... PYEOF`) that replaces only the `## PR LIST` section (matching from `## PR LIST` to the next `## ` heading or end of string) and preserves everything else byte-for-byte, appending a new `## PR LIST` section at the end if none exists yet.
4. Apply the update: `gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt`

I would explicitly avoid constructing the full PR body string by hand — the skill flags that as a violation since it risks clobbering unrelated sections.

Throughout, I would also resolve `{owner}/{repo}` dynamically via `gh repo view --json nameWithOwner --jq .nameWithOwner` if needed, and I would treat several conditions as hard stops rather than working around them: `gh` unavailable/unauthenticated, zero extractable merged PR numbers, or an author that fails to resolve even after retrying `gh pr view <num> --json author` (I would report it rather than leave a blank or fabricate one). I would not truncate long lists, would not switch to date-based grouping, and would only include per-PR summaries if you opted in at Step 2.

Since none of this can begin without the release PR number, my actual next action is to ask you for it before making any `gh` calls.
