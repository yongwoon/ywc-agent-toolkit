# Dispatch artifact: ywc-release-pr-list (original body, run 1)

**Key**: claude-code/skills/ywc-release-pr-list/SKILL.md:27-27
**Scenario**: I need help with the following: working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The skill's Step 1 requires the target release PR number to be supplied via $ARGUMENTS, and the user's request ('working on a release PR (e.g., develop→main) and wants to generate the merged PR list grouped by author') does not include a PR number. Per the Task procedure ('If no PR number is provided, stop and report the missing input'), the correct action is to stop before doing any GitHub API work and ask the user to supply the target release PR number, rather than guessing or proceeding on an assumed PR.

## Actions
- Read claude-code/skills/ywc-release-pr-list/SKILL.md in full (only action taken)
- Determine $ARGUMENTS contains no release PR number
- Stop before any gh/API work and ask the user for the target release PR number
- (contingent, once PR number supplied) ask the required yes/no summary_mode question and wait
- (contingent) run: gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'
- (contingent) extract merged PR numbers via scripts/extract-merged-prs.sh --exclude <PR_NUMBER> (anchored 'Merge pull request #(\d+)' and trailing '(#\d+)' patterns only)
- (contingent) validate each extracted number with gh pr view <n> --json state --jq .state, drop non-MERGED
- (contingent) run bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <numbers...> to get NDJSON author/title/summary/skipped
- (contingent) group entries by author (alphabetical), sort PR numbers ascending within each group, build '- #N @author' or '- #N @author — summary' lines per summary_mode
- (contingent) gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt
- (contingent) write new list to /tmp/pr_list_new.txt
- (contingent) run the provided python3 heredoc script to produce /tmp/pr_body_updated.txt, replacing only the '## PR LIST' section
- (contingent) gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt
- (contingent) resolve {owner}/{repo} via gh repo view --json nameWithOwner --jq .nameWithOwner if needed
- Report final result including any skipped/unresolved PR numbers

## Files touched
- claude-code/skills/ywc-release-pr-list/SKILL.md (read only)
- /tmp/pr_body_original.txt (would create, contingent)
- /tmp/pr_list_new.txt (would create, contingent)
- /tmp/pr_body_updated.txt (would create, contingent)

## Gates enforced
- Step 1 input validation: PR number must be present and a positive integer, else stop and report missing input
- Step 2 mandatory single question + wait for summary_mode before any GitHub API work, no re-prompt later
- Step 4 anchored-pattern-only PR extraction (rejects arbitrary '#123' issue/cross references) plus per-number merged-state validation via gh pr view --json state
- Step 5 author resolution must not be left blank; retry via gh pr view --json author rather than guessing
- Step 7 PR body edit must go through the python script that touches only the '## PR LIST' section, never a manually reconstructed full body
- Rationalization Defense table: no truncating long lists, no skipping missing PR-number reports, no date-grouping substitution, honor user's exact summary_mode choice
- Decision Rules: stop and report if gh is unavailable/unauthenticated, or if no merged PR numbers can be extracted, before making any edit

## Full narrative

I would apply the ywc-release-pr-list skill's procedure exactly as written, and the very first gate stops me before any real work begins.

**Step 1 — Identify the target PR.** The skill's Task section says: "Read the PR number from $ARGUMENTS... If no PR number is provided, stop and report the missing input." The user's request only describes the general scenario (release PR, develop→main, merged PR list grouped by author) — it does not include a concrete PR number such as `301`. Per the skill's own contract, I would not guess at a PR number, infer it from `git log`, or try to find "the" open release PR myself. I would stop immediately and ask the user directly:

> "Could you provide the target release PR number (e.g., 301) so I can compile its merged PR list?"

This is a hard stop, not a soft suggestion — the skill explicitly enumerates "no PR number provided" as a stop-and-report condition, distinct from "invalid PR number" (non-positive-integer), which is also a stop condition.

Assuming the user then supplies a valid PR number (e.g., `301`), here is exactly what I would do next, in order:

1. **Announce the skill**: state "I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR."

2. **Step 2 — Ask about summaries.** Before touching `gh` at all, I would ask exactly one question and wait: "Would you like to include a short summary of what each PR applied alongside the author? (yes / no)". A `yes`/`y` sets `summary_mode = true`; `no`/`n` sets it `false`. If the answer is ambiguous I ask once more, and if still unclear I default to `summary_mode = false` and note that default explicitly in my final report. I would not re-prompt for this later in the run.

3. **Step 3 — Collect commit headlines.** Run:
   `gh pr view 301 --json commits --jq '.commits[].messageHeadline'`

4. **Step 4 — Extract merged PR numbers.** Rather than eyeballing the headlines, I would run the bundled deterministic extractor:
   `bash claude-code/skills/ywc-release-pr-list/scripts/extract-merged-prs.sh --exclude 301`
   which applies only the two anchored patterns (`Merge pull request #(\d+)` and trailing `(#\d+)`), rejecting stray references like `fix #123` or `see #456`, then dedups and sorts ascending. For each surviving number I would additionally confirm merged state with `gh pr view <n> --json state --jq .state`, dropping anything that returns `OPEN`, non-merged `CLOSED`, or an error.

5. **Step 5 — Resolve author/summary per PR.** In one batch call:
   `bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh <pr-1> <pr-2> ...`
   parsing the NDJSON output — using `author` (and `summary` only if `summary_mode` is true) for each non-skipped entry, and recording any `skipped: true` entries (with `reason`, e.g. `not_merged: OPEN` or `fetch_error`) to surface in my final report rather than silently dropping them or leaving authors blank.

6. **Step 6 — Group and sort.** Group resolved entries by author login, sort author groups alphabetically, and sort PR numbers ascending within each group. Build lines as `- #<N> @<author>` (classic) or `- #<N> @<author> — <summary>` (summary mode).

7. **Step 7 — Update the release PR description.**
   - `gh pr view 301 --json body --jq '.body' > /tmp/pr_body_original.txt`
   - Write the newly built list (entries only) to `/tmp/pr_list_new.txt`
   - Run the provided `python3` heredoc script against those two files, producing `/tmp/pr_body_updated.txt`, which replaces only the `## PR LIST` section (matched via the `(## PR LIST)\s*\n[\s\S]*?(?=\n## |\Z)` pattern) and appends a fresh `## PR LIST` section if none exists — never touching any other part of the body.
   - `gh pr edit 301 --body-file /tmp/pr_body_updated.txt`

   I would explicitly avoid hand-constructing the full PR body string myself, since the skill flags that as a rationalization trap ("Updating the target PR description requires force, skip on conflict" — instead I'd re-fetch and re-apply via the script rather than force-overwriting on any concurrent-edit conflict).

Throughout, I would honor the skill's Decision Rules: resolve `{owner}/{repo}` dynamically via `gh repo view --json nameWithOwner --jq .nameWithOwner` if needed; stop and report if `gh` is unavailable/unauthenticated; stop before editing anything if zero merged PR numbers can be extracted; never truncate a long list; never fabricate an author or a summary (falling back to classic format for any single entry whose summary can't be derived, and listing those numbers in my final report); and preserve every other section of the existing PR description byte-for-byte.

Since none of this can begin without the release PR number, my actual next move right now is only the clarifying question above — I have not run any `gh` command, read any other file, or made any edit.
