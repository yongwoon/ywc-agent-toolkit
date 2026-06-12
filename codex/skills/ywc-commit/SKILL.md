---
name: ywc-commit
description: >-
  (ywc) Use when the user says "commit", "커밋", "커밋 해줘", "commit push",
  "push", "지금까지 한 작업 커밋", "コミットして", "プッシュして", or any phrase
  indicating intent to stage, commit, or push current work. Do not use for PR
  creation (use ywc-create-pr), handling PR review feedback (use
  ywc-handle-pr-reviews), code review (use ywc-impl-review), or making code
  changes.
---

# Commit Skill

**Announce at start:** "I'm using the ywc-commit skill to stage and commit the current work."

Use this skill when the user wants to commit (and optionally push) work-in-progress changes to the repository.

Keep the workflow disciplined and conservative. Only stage files that are clearly part of the current conversation's work.

## Rationalization Defense

When tempted to skip a rule, check this table first:

| Excuse | Reality |
|---|---|
| "These extra files probably belong here" | If you cannot point to a moment in this session when they were touched, they are OUT. Ask. |
| "git add . is faster" | Faster ≠ correct. Stage by explicit path every time. |
| "Hook failure is just noise, --no-verify is fine" | Hooks exist for a reason. Fix the cause or report it. |
| "User said push, so amend + force push is implied" | Push intent ≠ rewrite-history intent. Force only when explicitly asked. |
| "This is just main, one direct commit is OK" | Direct commits to main are almost always wrong. Confirm first. |
| "The summary message captures both refactor and feature" | Two purposes = two commits. Always. |
| "I will write a co-author trailer because this looks like a AI-assisted project" | Only if the repo's recent commits already use one. Do not fabricate convention. |
| "The UL update adds noise to a small commit, skip it" | If `docs/ubiquitous-language.md` exists, the project has committed to keeping its glossary synchronized with code. A commit that introduces a new domain term without updating the glossary silently degrades every downstream LLM prompt that reads the file. Skip only when the caller already ran the update (signaled by `--skip-ubiquitous-update`) or the file does not exist. |
| "ywc-create-pr already runs UL update, mine would duplicate" | Correct — that is exactly why callers must pass `--skip-ubiquitous-update` when delegating. Without the flag, ywc-commit will re-run the update. Read `$ARGUMENTS` in Step 0 before deciding. |

**Violating the letter of these rules is violating the spirit.** If you find yourself rephrasing a rule to make an exception, stop and ask the user.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--skip-ubiquitous-update` | flag | off | Skip Step 0.5 (Ubiquitous Language Update). Passed by callers that have already run `ywc-ubiquitous-language` themselves (e.g., `ywc-create-pr`, `ywc-finish-branch`) to prevent double invocation. |

All other behavior is controlled by the user's natural-language request (e.g., "push", "커밋만", "authentication 관련만"). The skill does not introduce extra flags beyond what is needed for delegation safety — keeping the surface minimal so direct users do not have to remember syntax.

## Core Rules (Never Violate)

1. **Only commit files relevant to the current session.** Stage only files that were created, modified, or explicitly discussed during this conversation. Do not include files changed by other processes, leftover from a previous session, or of unknown origin. When in doubt, ask the user.
2. **Split logically distinct changes into separate commits.** One commit, one purpose.
3. **Only push if the user explicitly requests it.** Push intent is expressed by words like "push", "푸쉬", "올려줘", or similar.
4. **Never use `--no-verify`.** Pre-commit and pre-push hooks must pass. If a hook fails, fix the root cause or report it to the user.
5. **Confirm before committing directly to `main` or `master`.** This is almost always a mistake.
6. **Never use `git add .` or `git add -A`.** Always stage files by explicit path.
7. **Never commit secrets or build artifacts.** Skip `.env*`, `*.log`, `dist/`, `build/`, `node_modules/`, `.DS_Store`, and large binaries unless the user explicitly added them. Report any such files found.
8. **Do not add tool-specific co-author trailers by default.** Follow the repository's observed commit conventions. Add an AI co-author trailer only when the repository already requires one or the user explicitly asks for it.

## Workflow

### Step 0 — Parse arguments

Inspect `$ARGUMENTS` for the flags listed in the [Arguments](#arguments) table. Store the parsed values for use in later steps:

- `--skip-ubiquitous-update` → if present, skip Step 0.5 entirely.

The skill remains fully usable without any flag — direct invocations (`/ywc-commit`, "커밋 해줘") proceed with all defaults.

### Step 0.5 — Ubiquitous Language Update (optional)

**Skip this step if `--skip-ubiquitous-update` is present in `$ARGUMENTS`.** Callers that already invoked `ywc-ubiquitous-language` (e.g., `ywc-create-pr` Step 0.5, `ywc-finish-branch` Step 1.5) pass this flag to avoid duplicate work.

Check whether the project has established a ubiquitous language document:

```bash
test -f docs/ubiquitous-language.md
```

- **Exists**: Invoke `ywc-ubiquitous-language --mode update`. Any resulting changes to `docs/ubiquitous-language.md` flow naturally into Step 2 (Classify changed files) as IN, since the file was modified during this session.
- **Not exists**: Skip silently — the project has not yet adopted a ubiquitous language document. Do not prompt the user to create one; that is the job of `ywc-ubiquitous-language` itself when invoked directly.

**Rationale**: Domain vocabulary drift is hard to detect after the fact. Catching it at the commit boundary keeps the glossary aligned with the codebase incrementally, rather than as a separate "vocabulary cleanup" effort later. The check is cheap when the file is absent (one `test -f`) and bounded when present (the skill's `update` mode produces no diff when nothing changed).

### Step 1 — Assess current state

```bash
git status --short
git diff --stat
git log --oneline -15   # learn the project's commit style
git branch --show-current
```

- Check whether the working branch is `main` or `master`. If so, apply Rule 5.
- Read the last 15–30 commit messages to learn the project's exact type/scope/message conventions before drafting any messages.

### Step 2 — Classify changed files (Rule 1)

Classify every changed file into one of three categories:

| Category | Action |
|---|---|
| **IN** — created, modified, or discussed during this session | Stage for commit |
| **UNKNOWN** — unclear when or why it changed | Ask the user before staging |
| **OUT** — clearly unrelated to this session's work (other features, IDE files, local config) | Exclude. Inform the user: "These files looked unrelated and were excluded." |

If any file is UNKNOWN or OUT, show the user the classification table and get explicit approval before staging anything. **Do not skip this step.**

### Step 3 — Split into logical commits (Rule 2)

Group the IN files by logical unit and plan the commit sequence. Examples:

- Refactor + new feature → **2 commits** (refactor first, then feat)
- Bug fix + its tests → **1 commit** (same context)
- Bug fix + unrelated typo fix → **2 commits**
- UI change + extracted utility discovered along the way → **2 commits** (refactor first)

Use `git add -p` for hunk-level staging when a single file contains changes that belong to different logical units.

Show the user the planned commits (files + draft message for each) and get approval before proceeding. Approval can be skipped if there are only 1–2 files with a clearly single-purpose change.

### Step 4 — Write commit messages

Read `git log --oneline -30` and match the project's **exact** style.

**General format**

```
<type>(<scope>): <summary>

<body — only when needed>
```

**Types** — use only what this repository already uses. Common types:

- `feat` — new feature
- `fix` — bug fix
- `refactor` — internal restructuring with no behaviour change
- `perf` — performance improvement
- `chore` — build, config, or tooling changes
- `docs` — documentation only
- `test` — test changes only

If the repository uses additional types (e.g., `enhance`, `skill`, `ci`), adopt them.

**Scope** — derive from the project's git log pattern. Common patterns:

- Package name (`web`, `api`, `cli`)
- Module or domain name (`auth`, `dashboard`, `payment`)
- Omit scope when the change spans multiple areas
- For skill files (e.g., `.codex/skills/`), use the skill name as scope

**Summary rules**

- Noun phrase or verb phrase — match the project's style exactly
- No trailing period
- 72 characters max on the first line

**Body rules**

- Omit for simple single-purpose changes
- Use bullet points (`- `) when bundling multiple items into one commit
- Briefly state "why" when the reason is not self-evident from the summary

**Co-author trailer**

- Do not add a co-author trailer by default.
- If the repository's recent commits consistently include an AI co-author trailer, follow that exact convention.
- If the user explicitly requests a co-author trailer and the repository has no convention, use `Co-Authored-By: Codex <noreply@openai.com>`.
- Never fabricate a different provider's identity unless the repository's existing commit history explicitly uses it.

### Step 5 — Stage and commit

```bash
# Stage only relevant files by explicit path
git add <path1> <path2> ...
# Or stage by hunk when one file has mixed changes
git add -p <path>

# Verify staged diff before committing
git diff --cached --stat

# Commit using heredoc to safely handle multi-line messages
git commit -m "$(cat <<'EOF'
<type>(<scope>): <summary>

<body>
EOF
)"
```

Repeat for each logical commit. After each commit, run `git status` to review remaining changes before proceeding to the next.

### Step 6 — Verify result

```bash
git log --oneline -<N>   # N = number of commits just created
git status               # confirm working tree is as expected
```

Report immediately if any commits are missing or if unexpected changes remain.

### Step 7 — Push (only when explicitly requested)

Push only when the user's message contains clear push intent:

```bash
git push
```

- Use `git push -u origin <branch>` if no upstream is set.
- Use `--force` or `--force-with-lease` **only when the user explicitly requests it**. If a default push is rejected as non-fast-forward, explain the situation and present the options.
- After pushing, report the current branch and latest commit hash in one line.

## Report Format

After all commits are done, report concisely:

```
✅ N commit(s) created [+ pushed]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
Excluded files: <list if any, omit if none>
```

## Common Mistakes (Never Do These)

- ❌ `git add .` — stages unrelated files silently
- ❌ Bundling different changes under a vague message like "update work" or "작업 내용 반영"
- ❌ Committing `.env`, lock files, or build artifacts without asking
- ❌ Referencing conversation context in messages ("as requested", "per discussion")
- ❌ Including changes from a previous session or unrelated working tree modifications
- ❌ Pushing without an explicit push request from the user
- ❌ Bypassing hooks with `--no-verify`
- ❌ Skipping Step 0.5 when `docs/ubiquitous-language.md` exists and no `--skip-ubiquitous-update` flag was passed
- ❌ Running Step 0.5 a second time when the caller already passed `--skip-ubiquitous-update`

## Example Invocations

- `/ywc-commit`
- `커밋 해줘`
- `commit and push`
- `지금까지 한 작업 커밋푸쉬 ㄱㄱ`
- `authentication 관련 파일만 commit해줘`
- `/ywc-commit --skip-ubiquitous-update` (delegated invocation from another skill that already ran the UL update)

## Validation Scenarios

1. **Normal case** — session-relevant files staged into one or more logical commits following the project's commit style.
2. **Multi-commit split** — refactor and feature changes separated into two ordered commits.
3. **UNKNOWN file found** — user is shown the classification table and asked to confirm before any staging occurs.
4. **Push requested** — commits created first, then pushed; force-push is never used unless explicitly asked.
5. **Hook failure** — `--no-verify` is never used; root cause is reported to the user.
6. **UL document present, direct invocation** — Step 0.5 runs `ywc-ubiquitous-language --mode update`; any resulting `docs/ubiquitous-language.md` changes are classified as IN in Step 2 and folded into the appropriate logical commit (typically the same commit as the domain-code change that introduced the new term).
7. **UL document present, delegated invocation** — Caller passes `--skip-ubiquitous-update`; Step 0.5 is skipped; no double invocation occurs.
8. **UL document absent** — Step 0.5 silently skips after `test -f`; user is not prompted to create the file.
