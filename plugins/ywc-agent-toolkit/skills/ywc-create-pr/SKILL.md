---
name: ywc-create-pr
description: (ywc) Use when the user wants to open a pull request and says "create a PR", "open a PR", "submit code for review", "push and create PR", "PR 만들어줘", "풀리퀘 작성", "プルリク作成", or is wrapping up a feature branch. Do not use for committing only without PR creation, or for handling existing PR review comments (use ywc-handle-pr-reviews).
---

# Create PR

**Announce at start:** "I'm using the ywc-create-pr skill to commit and open a pull request."

Commit changes and create a draft PR following the PR template.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "User said 'create PR' — they obviously want it merged too" | Default is **draft** PR. Mark ready/merge only when explicitly asked. |
| "CI check is slow, just push and let CI run remotely" | Local CI catches failures before review delay. Skip only with `--skip-ci-check`. |
| "Force push will resolve the rejection faster" | Non-fast-forward = teammate work or rebase needed. Force only with explicit user approval. |
| "The PR template is generic, my custom body is better" | If `.github/pull_request_template.md` exists, follow it. Templates encode team norms. |
| "Secret scan flagged a value but it's just a test fixture" | Stop and confirm with the user before bypassing the scan. Better to over-confirm than leak. |
| "Base branch is obvious from history" | Auto-detect order is develop → main → master. Show the chosen base before proceeding. |
| "The hook is just being pedantic, `CLAUDE_MD_CHECK=skip git push` will fix it" | Inline `VAR=value git push` does NOT reach the hook subprocess — the hook runs before the command executes. Use `export VAR=value && git push` in a single Bash call instead, or instruct the user to run `! VAR=value git push` in their terminal. |
| "CI passed locally, so remote CI will pass too" | Remote CI may use different OS runners, Node versions, or environment secrets unavailable locally. Always verify remote CI after pushing — local and remote diverge more often than expected. |
| "CI is slow — let the reviewer catch failures" | CI failures signal a broken branch to every reviewer. Fix them immediately after PR creation so the PR stays reviewable and avoids a second round-trip after the reviewer waits for another push. |
| "CI is green, so the PR is ready to merge" | CI status and merge-readiness are independent gates. A green PR can still be `CONFLICTING` against the base if the base advanced. Check `gh pr view --json mergeable,mergeStateStatus` before declaring the PR done — a `CONFLICTING`/`BEHIND`/`BLOCKED` PR blocks every reviewer just like a CI failure. |
| "The PR conflicts with base — I'll rebase the feature branch to fix it" | Rebasing rewrites commit SHAs and orphans existing PR review threads. Merge the base *into* the feature branch instead (`git merge --no-ff origin/<base>`); it preserves SHAs and review history. See `../references/pr-conflict-resolution.md`. |
| "The UL update adds noise before every PR" | The update is a diff-driven incremental review, not a full re-extraction. If no new domain terms appeared in the branch, the skill produces no changes. Skipping it lets the glossary drift from the codebase with every PR that introduces new vocabulary. |

**Violating the letter of these rules is violating the spirit.** If you find yourself rephrasing a rule to make an exception, stop and ask the user.

## Context

- Changed files: !`git status --short`
- Current branch: !`git branch --show-current`

## Task

Follow the steps below to commit and create a PR.

### 0. Language and Title Initialization

1. **Title**: Check `$ARGUMENTS` for `--title "<value>"`. If present, store it as the PR title — it will be used verbatim in Step 7 (skip self-generated title).
2. **Language**: Check `$ARGUMENTS` for a language hint (e.g., `--lang ja`, `--lang en`, `--language korean`). If not specified and no `--title` was provided, use the `AskUserQuestion` tool to ask: "What language should the PR title and description be written in?" with options English / Japanese / Korean — then **immediately continue to Step 0.5 in the same turn**; do not end the turn or wait for further input after receiving the answer. If `--title` was provided, infer the language from its content or default to English — do not prompt.
3. Apply the chosen language consistently when writing the PR description in Step 7.
4. **Post-CI check**: Check `$ARGUMENTS` for `--skip-post-ci-check`. If present, skip Step 8 (Remote CI & Bot Review). This flag is passed by `ywc-finish-branch`, which handles CI verification independently in its own Step 4.
5. **Ubiquitous Language update**: Check `$ARGUMENTS` for `--skip-ubiquitous-update`. Store the flag — it controls Step 0.5.

### 0.5. Ubiquitous Language Update (optional)

**Skip this step if `--skip-ubiquitous-update` is present in `$ARGUMENTS`.** This flag is passed by `ywc-finish-branch`, which runs the update in its own Step 1.5 before delegating PR creation to this skill.

Check whether `docs/ubiquitous-language.md` exists in the project root:

```bash
test -f docs/ubiquitous-language.md
```

- **Exists**: Invoke `ywc-ubiquitous-language --mode update`. Any changes to `docs/ubiquitous-language.md` will be picked up and committed by Step 4.
- **Not exists**: Skip silently — the project has not yet established a ubiquitous language document.

### 1. Determine Base Branch

- If a base branch is specified in `$ARGUMENTS`, use it
- Otherwise, auto-detect the default base branch in the following priority order:
  1. `develop` — if it exists locally or in remote (`git rev-parse --verify develop 2>/dev/null || git rev-parse --verify origin/develop 2>/dev/null`)
  2. `main` — if it exists locally or in remote
  3. `master` — fallback
- Store the determined base branch and use it consistently throughout all subsequent steps
- Show the determined base branch to the user: "Base branch: `<branch>`"

### 2. Pre-flight Checks

Before proceeding, verify the environment is ready:

- Confirm `gh` CLI is installed and authenticated (`gh auth status`). If not, stop and tell the user how to set it up
- Check if a PR already exists for this branch (`gh pr list --head <current-branch> --state open`). If one exists, show the URL and ask the user whether to update it or create a new one
  - **If update**: Skip PR creation (Step 7), but do **not** skip Step 8. Commit and push changes, optionally update the PR description with `gh pr edit <number> --body-file -`, then proceed to Step 8 (Remote CI & Bot Review Check). Updating a PR can break CI exactly like creating one — the verification must run on the update path too, not only on the new-PR path (unless `--skip-post-ci-check` was passed by an upstream caller).
  - **If new**: Continue with the full workflow
- Verify the current branch is not the base branch itself — refuse to create a PR from main/develop/master to itself

### 3. Security Check

Run the bundled secret scan script:

```bash
# Phase 1+2: dangerous file names + staged/unstaged diff content
SECRET_SCRIPT="codex/skills/ywc-create-pr/scripts/scan-secrets.sh"
[ -f "$SECRET_SCRIPT" ] || SECRET_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/ywc-create-pr/scripts/scan-secrets.sh"
bash "$SECRET_SCRIPT" --staged

# Phase 3: all commits on this branch vs base (secrets already committed)
bash "$SECRET_SCRIPT" --committed <base-branch>
```

Exit 0 = clean — proceed. Exit 1 = secrets or dangerous files found — the script prints matches to stdout.

If either scan returns exit 1, warn the user and show the script output. Do not include flagged files in the commit unless the user explicitly confirms. For committed secrets (second scan), require explicit confirmation before proceeding to PR creation.

### 4. Commit Uncommitted Changes

- Check uncommitted changes with `git status` and `git diff`
- If there are uncommitted changes, delegate to `ywc-commit` with `--skip-ubiquitous-update`:
  - **Why the flag**: Step 0.5 of this skill already invoked `ywc-ubiquitous-language --mode update` (unless this skill itself was called with `--skip-ubiquitous-update` by an upstream caller like `ywc-finish-branch`). Without the flag, `ywc-commit`'s own Step 0.5 would run the update a second time. The flag must always be passed in this delegation — even when this skill's Step 0.5 was skipped, because the upstream caller is the one responsible for the UL update in that scenario.
  - `ywc-commit` classifies every changed file as IN / UNKNOWN / OUT relative to the current session, splits logically distinct changes into separate commits, and learns the project's commit message style from `git log`
  - It will confirm with the user before staging any UNKNOWN or OUT files — do not skip that confirmation
  - Follow the repository's observed co-author trailer convention; do not force-add a trailer if the repository does not already use one
- If there are no uncommitted changes: skip this step

### 5. CI Check (Pre-push Validation)

Run the same lint, format, typecheck, and test checks locally that CI will execute. The goal is to catch failures before pushing, since CI failures delay PR review.

**Skip this step if `--skip-ci-check` is present in `$ARGUMENTS`.**

#### 5-1. Detect CI Check Commands

Run the bundled detector first — it emits candidate commands from each source plus the package manager, so you do not re-derive the same greps each run:

```bash
CI_DETECT_SCRIPT="codex/skills/ywc-create-pr/scripts/detect-ci-commands.sh"
[ -f "$CI_DETECT_SCRIPT" ] || CI_DETECT_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/ywc-create-pr/scripts/detect-ci-commands.sh"
bash "$CI_DETECT_SCRIPT" [repo-dir]
```

It is best-effort; reconcile its output against the priority order below (workflows are authoritative, then CLAUDE.md, then package.json, then Makefile):

1. **`.github/workflows/*.yml`** — Read CI workflow files and extract active check commands
   - Look for `run:` fields containing `lint`, `format`, `typecheck`, `type-check`, `test`, `check`
   - Exclude deployment-related jobs/steps (deploy, release, publish, docker build)
   - Prioritize workflows with `on: pull_request` or `on: push` triggers
2. **`CLAUDE.md`** — Search the project root CLAUDE.md (or parent directory) for lint, format, typecheck, and test commands
3. **`package.json` scripts** — Use scripts whose keys match `lint`, `format`, `typecheck`, `type-check`, or `test`
4. **`Makefile`** — Use targets named `lint`, `format`, `check`, or `test`

If no commands are detected, skip this step and inform the user of the reason.

#### 5-2. Detect Execution Environment

- If CLAUDE.md specifies a `docker exec <container>` prefix, apply it to all commands
- Determine the package manager (`pnpm`, `npm`, `yarn`, etc.) from the lock file

#### 5-3. Run Checks

- Execute all detected check commands in sequence (recommended order: lint → format → typecheck → test)
- Record the pass/fail result of each command
- Continue running remaining commands even if one fails — report all results together at the end

#### 5-4. Report Results and Next Steps

- If all checks pass, proceed to the next step (Push)
- If any check fails:
  - Summarize which checks failed and what the errors were
  - Present the user with two options:
    1. **Fix and retry** — Resolve the issues, then re-commit and re-run checks
    2. **Skip and proceed** — Ignore the check failures and continue to Push & PR creation

### 6. Push to Remote

- Check if the current branch is already up-to-date with the remote (`git status -sb` — look for `ahead` count). If the branch is already pushed and there are no new local commits, skip the push
- Push to remote with `git push -u origin HEAD`
- If push fails due to a **PreToolUse hook error** (error message contains "hook error" or "Blocked:"):
  1. Read the full hook error message — it usually states exactly what is required or how to bypass
  2. Look for a bypass env var hint (e.g., `CLAUDE_MD_CHECK=skip`, `SKIP_CHECK=true`). If found:
     - Retry with `export <BYPASS_VAR>=<value> && git push -u origin HEAD` in a single Bash call
     - **Why**: `VAR=value git push` sets the variable only for the git process, not for the hook subprocess that runs before it. Exporting in the same shell command makes the variable available to the hook
  3. If the hook requires a content action (e.g., "update CLAUDE.md before pushing"):
     - Evaluate whether the requirement genuinely applies to the changed files
     - If yes: fulfill the requirement (e.g., update CLAUDE.md), then retry the push normally
     - If no (e.g., changes are test fixtures or QA docs with no documentation impact): use the bypass approach in step 2
  4. If the bypass attempt also fails or no bypass is indicated, instruct the user to run this in their terminal:
     ```
     ! export <BYPASS_VAR>=<value> && git push origin HEAD
     ```
     Explain: the `!` prefix runs the command directly in the user's shell session, where the exported variable reaches the hook subprocess. Continue to Step 7 once the user confirms the push succeeded
- If push fails due to **remote changes** (non-fast-forward):
  - Suggest `git pull --rebase origin <current-branch>` to the user (rebase against the same feature branch, not the base branch)
  - Do not force-push without explicit user approval

### 7. Create PR

- Check if `.github/pull_request_template.md` exists
  - **If exists**: Read the template and create the PR description following its structure
  - **If not exists**: Create a PR description with the following default structure:

    ```markdown
    ## Summary

    [1-3 bullet points summarizing the changes]

    ## Changes

    [List of specific changes made]

    ## Test Plan

    [How to verify the changes]
    ```

- Write each section based on all commits from the base branch (`git log <base-branch>..HEAD`)
- Review the full diff (`git diff <base-branch>...HEAD`) to ensure the description accurately reflects the changes
- **PR title**: if `--title` was provided in Step 0, use it verbatim. Otherwise, generate a title from the commit history in the language chosen in Step 0.
- Write all description content in the language chosen in Step 0
- If there are no UI changes, write "N/A" in the screenshot section (if the template has one)
- Create a **draft** PR with `gh pr create --draft --base <base-branch> --title "<title>" --body-file - <<'EOF'`
- Always specify `--title` and `--body-file -` (or `--body`) explicitly to avoid interactive prompts

### 8. Remote CI & Bot Review Check

**Skip this step entirely if `--skip-post-ci-check` is present in `$ARGUMENTS`.** This step runs only when `ywc-create-pr` is invoked directly by the user — `ywc-finish-branch` passes `--skip-post-ci-check` and handles CI + bot review in its own Step 4.

After the PR is created **or updated** (the Step 2 update path also lands here), retrieve the PR number and verify that remote CI passes and no automated reviewers have flagged issues.

```bash
PR_NUMBER=$(gh pr view --json number --jq .number)
```

#### 8-1. Wait for CI to Complete

```bash
gh pr checks $PR_NUMBER --watch
# exit 0 = all checks passed; exit 1 = one or more checks failed
```

If no CI checks are configured for this repository (command returns immediately with no output), skip to Step 8-3. If `--skip-ci-check` is present in `$ARGUMENTS`, skip to Step 8-3.

#### 8-2. CI Failure Fix Loop (up to 2 attempts)

If `gh pr checks` exits 1, at least one check failed. Apply fixes in the loop below — at most **2 attempts**:

1. **Get failure details:**
   ```bash
   # List failed run IDs for the current branch
   gh run list --branch $(git branch --show-current) \
     --json databaseId,name,conclusion \
     --jq '.[] | select(.conclusion == "failure")'
   # View logs for the most recent failed run
   gh run view <run-id> --log-failed
   ```

2. **Categorize and fix by failure type:**

   | Failure type | Fix action |
   |---|---|
   | Lint / format | Run the project's auto-fix command (`eslint --fix`, `prettier --write`, `ruff --fix`, `biome check --apply`), commit the changes |
   | Type errors | Read compiler output, fix type mismatches in affected files, commit |
   | Test failures | Analyze failing test output, fix the implementation (never disable or weaken tests), commit |
   | Build errors | Read compiler/bundler output, fix compilation or import errors, commit |

3. **Push the fixes** and re-run `gh pr checks $PR_NUMBER --watch` to re-verify.

4. After **2 failed fix attempts**, report the failing check name(s) with the last 30 log lines, leave the PR as draft for manual intervention, and note the CI failure in the Completion Report.

#### 8-3. Bot Review Polling

> **Action required**: Read [`codex/skills/references/pr-bot-polling.md`](../references/pr-bot-polling.md) before proceeding. The canonical polling procedure and parameters are defined there.

```bash
bash "${CODEX_HOME:-$HOME/.codex}/skills/scripts/poll-pr-reviews.sh" "$PR_NUMBER"
# exit 0 → BOT_COUNT > 0 (bot reviews posted)
# exit 1 → BOT_COUNT == 0 (no bot reviews within polling window)
```

- **BOT_COUNT > 0**: Invoke `ywc-handle-pr-reviews` to address all comments, then re-run the polling script to catch any follow-up comments. If code fixes were pushed, re-run `gh pr checks $PR_NUMBER --watch` (one additional fix attempt allowed).
- **BOT_COUNT == 0**: No bot reviews — proceed to Step 8-4.

#### 8-4. Merge-Readiness (Conflict) Check

> **Action required**: Read [`../references/pr-conflict-resolution.md`](../references/pr-conflict-resolution.md) before proceeding. The `mergeable` / `mergeStateStatus` semantics, the merge-not-rebase rule, and the surface-vs-auto-resolve boundary are defined there.

CI passing does not mean the PR is mergeable — the base branch may have advanced and now conflict. After CI and bot review settle, check the merge state:

```bash
gh pr view $PR_NUMBER --json mergeable,mergeStateStatus --jq '{mergeable, mergeStateStatus}'
```

- `MERGEABLE` / `CLEAN` → the PR is review-ready; proceed to Completion Report.
- `BEHIND` → the branch is merely out of date (no textual conflict). Follow **Update Branch From Base** for the fast catch-up, push, and re-verify CI.
- `CONFLICTING` / `DIRTY` → follow **Update Branch From Base** in the reference. If the merge auto-resolves (branch was merely behind), push and re-verify CI. If it reports real textual conflicts, surface the conflicting files and PR URL to the user and note the conflict in the Completion Report — do not auto-resolve or force-push.
- `BLOCKED` → a required check or review gate is missing — **not** a conflict. Do not run the base-merge procedure; report which required check or review is outstanding so it can be resolved.
- `UNKNOWN` → poll briefly per the reference, then re-read.

Because this skill creates a **draft** PR by default and does not merge, a conflicting result is reported (not a hard stop) unless the user asked to take the PR further — but the branch should still be brought up to date so reviewers see a mergeable PR.

### 9. Completion Report

Display:

- The created PR URL (clickable)
- Summary: number of commits, files changed, insertions/deletions
- Base branch used

## Notes

- Follow any additional instructions in `$ARGUMENTS`
- Never force-push or amend published commits without explicit user approval
- If any step fails, explain what went wrong and suggest the fix rather than silently retrying

## Output Format

Return a PR creation report:

```text
Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
PR: <URL or "not created">
Base branch: <detected or requested base>
Commits: <commits created or "already committed">
Validation: <local checks, sensitive-file scan, and CI/bot status>
Next action: <merge/review instruction or blocker>
```

## Validation

Before finalizing, verify that sensitive files were not committed without confirmation, staged files were explicit, base branch selection is reported, `gh` authentication was checked, and CI or bot-review handling follows the selected mode.
