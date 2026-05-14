---
name: ywc-handle-pr-reviews
description: (ywc) Use when handling PR review feedback, addressing code review comments, or responding to GitHub PR review threads. Triggers: "handle PR reviews", "address review comments", "respond to PR comments", "리뷰 대응", "리뷰 코멘트 처리", "レビュー対応". Do not use for creating a new PR (use ywc-create-pr), performing a code review yourself (use ywc-impl-review), or for changes outside an open PR context.
---

# Handle PR Review Comments

**Announce at start:** "I'm using the ywc-handle-pr-reviews skill to address review comments and reply to each thread."

Review PR comments, fix issues where needed, and reply to each comment.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "This comment is just opinion, no fix needed" | Even disagreement requires a reply explaining why. Silent skip looks like neglect. |
| "I'll batch all replies after fixing everything" | Reply per thread as fixes land. Reviewers track which threads are resolved. |
| "Push without reply, the diff speaks for itself" | Reviewers cannot tell intent from diff alone. Always pair fix with reply. |
| "Resolving the thread without reply is fine" | Resolving without reply implies the reviewer's concern was wrong. Always state how it was addressed. |
| "Conflict in suggestions, pick one and move on" | Surface the conflict to the user. Do not silently choose between reviewer A and reviewer B. |
| "PR not found for this branch, scan recent PRs" | Stop and ask. Acting on a wrong PR overwrites unrelated reviewer threads. |
| "All review comments are addressed — CI is a separate concern" | Fixes to source code (refactors, new imports, logic changes) can break CI. Always re-verify CI after pushing review fixes. A PR with all comments addressed but failing CI is still blocked from merging. |

**Violating the letter of these rules is violating the spirit.** Code review is a conversation, not a checklist.

## Context

- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`

## Task

Follow the steps below to handle PR review comments.

### 1. Identify PR Number

- If a PR number is specified in `$ARGUMENTS`, use it
- Otherwise, identify the current branch's PR with `gh pr view --json number`
- If no PR exists for the current branch, stop and notify the user rather than proceeding blindly

Resolve `{owner}/{repo}` dynamically at this stage — it's used throughout the workflow:

```bash
gh repo view --json nameWithOwner --jq .nameWithOwner
```

### 2. Retrieve and Filter Comments

Retrieve all PR review comments and filter out those that don't need action. This prevents duplicate work and keeps the process focused on genuinely unresolved feedback.

```bash
bash codex/skills/ywc-handle-pr-reviews/scripts/fetch-unresolved-comments.sh \
  {owner}/{repo} {pr_number}
# exit 0 → JSON array of unresolved threads on stdout (may be [])
# exit 1 → gh CLI error (not authenticated or PR not found)
```

The script fetches paginated comments, groups them into threads, and applies the skip conditions automatically: threads containing `<!-- <review_comment_addressed> -->` are dropped, and threads where your reply is newer than the latest reviewer comment are dropped. The output JSON array contains only actionable threads — each element has `id`, `body`, `path`, `line`, `user`, `created_at`, and `thread_comment_count`. If the array is `[]`, skip to Step 7 and report "no unresolved comments".

### 3. Group and Analyze Comments

Before fixing anything, group all remaining comments by file. Processing file-by-file is more efficient — you read each file once, apply all related fixes together, and create one coherent commit per file instead of jumping back and forth.

**Processing strategy:**

1. Collect all unresolved comments and group by target file path
2. For each file, read the file once and analyze all related comments together
3. Apply fixes for that file and commit as a unit
4. Move to the next file

### 4. Classify and Fix Comments

For each comment, classify it into one of four categories:

| Category                                                                                                   | Action                                                                                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Approval / Acknowledgment** (tagged `review_comment_addressed`)                                          | Skip — already resolved                                                                                                                                                                 |
| **Clear code change request** (the fix is straightforward and unambiguous)                                 | Apply the fix                                                                                                                                                                           |
| **Controversial or ambiguous change request** (disagreement, architectural concern, or trade-off involved) | Do NOT auto-fix. Present the comment to the user with context, explain the trade-off, and ask for a decision. Reviewer feedback deserves thoughtful consideration, not blind acceptance |
| **Question only** (no code change implied)                                                                 | Reply with an explanation — no fix needed                                                                                                                                               |

**Security guardrails (never auto-apply, always defer to user):**

- Removal of authentication, authorization, or security middleware
- Addition of `eval()`, `exec()`, or dynamic code execution
- Disabling RLS, bypassing tenant isolation, or weakening input validation
- Hardcoded credentials or secrets

**When applying fixes:**

- Read the target file and identify the exact problem area referenced by the comment
- Apply the minimal fix that addresses the reviewer's concern
- If the comment references outdated code (the file has changed since the review), check whether the concern still applies to the current code. If it does, fix the current version. If not, reply explaining the code has already changed

**Commit rules:**

- One commit per file (group all fixes for the same file into a single commit)
- Use commit message format: `fix: summary of the fix`
- Push to remote after all commits are ready — pushing once at the end is cleaner than pushing after each commit

### 5. Reply to Comments

Reply to every processed comment so the reviewer knows their feedback was addressed. Use the thread reply API to keep conversations organized:

```bash
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments/{in_reply_to_id}/replies -F body=@- <<'REPLY_BODY'
...
REPLY_BODY
```

**Reply language:** Match the language of the original comment. If the reviewer wrote in Korean, reply in Korean. If in English, reply in English.

**Reply format by category:**

- **Fixed:**
  ```markdown
  Fixed: [commit-hash](https://github.com/{owner}/{repo}/pull/{pr}/commits/{full_sha})
  Description of what was changed and why
  ```
- **Deferred to user:** `This requires a decision — I've flagged it for the PR author.`
- **No fix needed:** Reply explaining the reasoning (e.g., intentional design choice, already handled elsewhere)
- **Outdated comment:** `This code has been updated since the review. The concern no longer applies because [reason].`

### 6. Error Handling

Things can go wrong during the process. Handle these gracefully:

| Error                                 | How to handle                                                                           |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| `gh pr view` fails (no PR for branch) | Stop and tell the user. Don't guess the PR number                                       |
| Push fails due to conflict            | Stop, notify the user, and show the conflicting files. Don't force-push or auto-resolve |
| Comment reply API returns 403/404     | Log the error, skip that reply, and report it in the final summary                      |
| Referenced file no longer exists      | Reply to the comment explaining the file was removed, and skip the fix                  |

### 6.5 CI Re-verification After Fixes

**Skip this step if no code commits were pushed in Step 4** (e.g., only reply comments with no code changes were made).

After all review-comment fixes are pushed, verify that the applied changes did not introduce CI regressions.

```bash
PR_NUMBER=$(gh pr view --json number --jq .number)
gh pr checks $PR_NUMBER
```

- **All checks pass**: proceed to Step 7.
- **Any check fails**:
  1. Get failure logs:
     ```bash
     gh run list --branch $(git branch --show-current) \
       --json databaseId,conclusion \
       --jq '.[] | select(.conclusion == "failure") | .databaseId' | head -1
     gh run view <run-id> --log-failed
     ```
  2. Categorize and fix:
     | Failure type | Fix action |
     |---|---|
     | Lint / format | Run the project's auto-fix command, commit, push |
     | Type / test / build | Analyze output, fix implementation, commit, push |
  3. Re-check CI after each push. Up to **2 fix attempts**.
  4. If CI still fails after 2 attempts: record the failing check names in Step 7's summary and set the overall outcome to `DONE_WITH_CONCERNS` (not `DONE`).

### 7. Final Summary

Report the results so the user has a clear picture of what happened:

- Total comments processed vs skipped
- List of applied fixes with file paths and commit hashes
- Any comments deferred to the user (with links)
- Any errors encountered during the process

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- When in doubt about a reviewer's intent, ask the user rather than guessing — misinterpreting feedback wastes more time than a quick clarification

## Integration

- **upstream**: ywc-create-pr (a PR must exist before review comments can be handled); ywc-sequential-executor / ywc-parallel-executor (executors that generate the PRs being reviewed)
- **downstream**: None — this skill closes the PR review loop; subsequent work is driven by the reviewer's approval or further comments
