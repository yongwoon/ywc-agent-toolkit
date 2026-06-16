---
name: ywc-release-pr-list
version: 1.0.0
description: (ywc) Use when working on a release PR (e.g., develop→main) and the user wants to generate the merged PR list grouped by author. Triggers: "release PR list", "릴리즈 PR 정리", "릴리스 PR 리스트", "release pr 정리", "リリースPR一覧", "ywc-release-pr-list", or any request to build a release-PR description from merged PR numbers. Do not use for normal feature PR creation (use ywc-create-pr), handling PR review comments (use ywc-handle-pr-reviews), or CHANGELOG / release-note generation from git history or merged PRs (use ywc-changelog-release-notes).
category: release
phase: release
requires: []
advisor_budget: 0
allowed tools: Bash, Read, Glob, Grep
---

# Release PR List

**Announce at start:** "I'm using the ywc-release-pr-list skill to compile the merged PR list for the release PR."

Generate the PR list for a release PR and update the PR description.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Some commit headlines lack PR numbers, skip those" | Stop and report missing PR numbers. They likely indicate squashed-without-link or direct pushes that need attention. |
| "Author resolution failed for one PR, leave it blank" | Always retry author lookup via `gh pr view <num> --json author`. Blank author breaks grouping. |
| "Author summaries make the list verbose, skip them" | Summary inclusion is interactively asked at the start. Honor that user choice exactly. |
| "Updating the target PR description requires force, skip on conflict" | Use `gh pr edit --body-file -`. If concurrent edit detected, fetch latest and re-apply, do not overwrite. |
| "Group by date instead of author for variety" | Author grouping is the spec. Date grouping defeats the goal of attribution. |
| "Release PR has 100+ PRs, truncate with '... and more'" | Never truncate. Long lists are fine; missing entries break audit trail. |

**Violating the letter of these rules is violating the spirit.** Release PR descriptions are an audit artifact.

## Context

- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Inputs

- `$ARGUMENTS` must contain the target release PR number
- Example: `301`

## Task

Follow the steps below.

### 1. Identify the target PR

- Read the PR number from `$ARGUMENTS`
- Validate that the PR number is a positive integer
- If the PR number is not valid, stop and report the invalid input
- If no PR number is provided, stop and report the missing input

### 2. Ask whether to include a per-PR summary

Before doing any GitHub API work, ask the user exactly one question and wait for a response:

> Would you like to include a short summary of what each PR applied alongside the author? (yes / no)

- On `yes`, `y`, or equivalent affirmative: set `summary_mode = true`
- On `no`, `n`, or equivalent negative: set `summary_mode = false`
- On ambiguous response: ask once more. If still unclear, default to `summary_mode = false` and explicitly note the default in the final report.

Persist `summary_mode` in memory for the remaining steps. Do not re-prompt later.

### 3. Collect commit headlines from the release PR

Run:

```bash
gh pr view <PR_NUMBER> --json commits --jq '.commits[].messageHeadline'
```

### 4. Extract merged PR numbers

- Extract PR numbers from commit headlines using these reliable patterns:
  - `Merge pull request #(\d+)` — standard merge commit format
  - Trailing `(#\d+)` — squash merge format (e.g., `feat: add login (#123)`)
- Do NOT extract `#<number>` from arbitrary positions (e.g., `fix #123` is an Issue reference, `see #456` is a cross-reference — these are not merged PRs)
- After extraction, validate each number with `gh pr view <number> --json state --jq .state` to confirm it is a merged PR. Skip any that return `OPEN`, `CLOSED` (not merged), or error
- Remove duplicates
- Sort PR numbers in ascending order
- Exclude the release PR number itself if it appears

### 5. Resolve author (and summary when enabled) for each PR

Fetch author, title, summary, and MERGED state for all extracted PR numbers in one script call:

```bash
bash claude-code/skills/ywc-release-pr-list/scripts/fetch-pr-metadata.sh \
  <pr-number-1> <pr-number-2> ...
# exit 0 → NDJSON on stdout (one JSON object per line); exit 2 → usage error
```

Each output line is one of:
- `{"number":123,"author":"alice","title":"feat: add login","summary":"Add login flow","skipped":false}` — merged PR; use `author` for grouping and `summary` for summary mode
- `{"number":124,"skipped":true,"reason":"not_merged: OPEN"}` — PR is not merged; skip it
- `{"number":125,"skipped":true,"reason":"fetch_error"}` — could not fetch; report in final report

The script applies the summary derivation rules (strip conventional commit prefixes, truncate at 80 chars, fall back to first non-empty body line for vague titles) regardless of `summary_mode`. In classic mode, ignore the `summary` field and use only `author`.

Build entries in this format:

- Classic mode: `- #<PR_NUMBER> @<AUTHOR>`
- Summary mode: `- #<PR_NUMBER> @<AUTHOR> — <SUMMARY>`

### 6. Group and sort the list

- Group entries by author login
- Sort author groups alphabetically
- Sort PR numbers ascending within each author group

### 7. Update the release PR description

First, save the current PR description and the new PR list to temporary files:

```bash
gh pr view <PR_NUMBER> --json body --jq '.body' > /tmp/pr_body_original.txt
```

Write the new PR LIST content (entries only, no heading) to `/tmp/pr_list_new.txt`.

Classic mode example (`summary_mode = false`):

```markdown
- #123 @alice
- #145 @alice
- #130 @bob
```

Summary mode example (`summary_mode = true`):

```markdown
- #123 @alice — Add OAuth login flow with Google provider
- #145 @alice — Fix pagination off-by-one on user list
- #130 @bob — Refactor database connection pool for reuse
```

Then run this script to produce the updated body. This script replaces ONLY the `## PR LIST` section and preserves everything else byte-for-byte:

```bash
python3 - /tmp/pr_body_original.txt /tmp/pr_list_new.txt /tmp/pr_body_updated.txt <<'PYEOF'
import sys, re

original = open(sys.argv[1], "r").read()
new_list = open(sys.argv[2], "r").read().strip()

section = f"## PR LIST\n\n{new_list}\n"

# Pattern: match from "## PR LIST" to the next "## " heading or end of string
pattern = r"(## PR LIST)\s*\n[\s\S]*?(?=\n## |\Z)"

if re.search(pattern, original):
    updated = re.sub(pattern, section, original, count=1)
else:
    # No existing PR LIST section — append at end
    updated = original.rstrip() + "\n\n" + section + "\n"

open(sys.argv[3], "w").write(updated)
PYEOF
```

Finally, update the PR description from the file:

```bash
gh pr edit <PR_NUMBER> --body-file /tmp/pr_body_updated.txt
```

**Important**: Do NOT construct the full body string manually. Always use the Python script above to ensure only the `## PR LIST` section is modified.

## Decision Rules

- Resolve `{owner}/{repo}` dynamically: `gh repo view --json nameWithOwner --jq .nameWithOwner`
- If `gh` is unavailable or unauthenticated, stop and report the blocker.
- If no merged PR numbers can be extracted, stop before editing and report what was found in the commit headlines.
- **Preserve existing description**: Never modify, reorder, or delete any content outside the `## PR LIST` section. Maintain the original section order.
- **Update only PR LIST**: If a `## PR LIST` section already exists, replace only that section with the new PR list. Leave everything else intact.
- Do not guess authors. If a PR cannot be resolved, report it clearly instead of writing incomplete data.
- **Summary mode is opt-in**: Always ask the user once at step 2 before performing the work. Never enable `summary_mode` silently and never re-prompt mid-run.
- **Do not fabricate summaries**: A summary must be derived from the PR title or body. If neither yields a usable line, fall back to classic format for that single entry and list the affected PR numbers in the final report.

## Example Invocations

- `Use $release-pr-list 301 to update the release PR description.`
- `Use $release-pr-list 301 and keep the existing sections untouched except for PR LIST.`
- `Use $release-pr-list 301 — I'll choose whether to add per-PR summaries when prompted.`
