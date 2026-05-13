# Commit Skill (ywc-commit)

A Claude Code Skill that safely stages, commits, and optionally pushes changes from the current session.

## Overview

This Skill handles the following automatically:

- Selects only session-relevant files to stage
- Splits logically distinct changes into separate commits
- Learns the project's commit style (type/scope/message) from `git log` and applies it consistently
- Reports a concise summary of all commits created

## Usage

Request in natural language or with a slash command:

```text
/ywc-commit
```

```text
commit and push
```

```text
commit only the authentication-related files
```

Korean phrases are also recognized: `커밋 해줘`, `커밋푸쉬 ㄱㄱ`, `지금까지 한 작업 커밋`.

## Core Rules

| Rule | Detail |
| --- | --- |
| Stage only session-relevant files | Only files created, modified, or discussed during this conversation |
| Split commits by logical unit | One commit = one purpose |
| Push only when explicitly requested | Triggered by "push", "푸쉬", "올려줘", or equivalent |
| `--no-verify` is forbidden | Fix hook failures or report them — never bypass |
| `git add .` is forbidden | Always stage files by explicit path |
| Confirm before committing to main/master | Almost always a mistake — ask first |
| Exclude secrets and build artifacts | Skip `.env*`, `dist/`, `build/` unless intentionally added |
| No tool-specific co-author trailer by default | Include one only when repository convention or the user explicitly asks for it |

## Workflow

```text
Step 0: Parse arguments
  └─ Handle flags passed by caller skills (e.g., --skip-ubiquitous-update)

Step 0.5: Ubiquitous Language Update (conditionally auto-ON)
  └─ If docs/ubiquitous-language.md exists → invoke ywc-ubiquitous-language --mode update
  └─ If file is absent → silent skip
  └─ If --skip-ubiquitous-update flag is set → skip (prevents double invocation)

Step 1: Assess current state
  └─ git status, git diff, git log (learn style), check branch

Step 2: Classify changed files
  └─ IN (session-relevant) / UNKNOWN (unclear origin) / OUT (unrelated)
  └─ docs/ubiquitous-language.md updated in Step 0.5 is classified as IN
  └─ Show classification table to user and get approval if any UNKNOWN/OUT found

Step 3: Split into logical commits
  └─ Plan separate commits for logically distinct changes
  └─ Use git add -p for hunk-level staging when needed
  └─ Show planned commits (files + draft messages) to user for approval

Step 4: Write commit messages
  └─ Learn project style from git log and apply it exactly
  └─ Include a co-author trailer only when repository convention or the user asks for it

Step 5: Stage & Commit
  └─ Stage by explicit path → verify diff → commit with heredoc

Step 6: Verify result
  └─ Check git log and git status for missing commits or unexpected changes

Step 7: Push (only when requested)
  └─ Default push; use -u flag if no upstream is set
  └─ Force-push only when explicitly requested
```

## Arguments

| Flag | Default | Behavior |
| --- | --- | --- |
| `--skip-ubiquitous-update` | off | Skips Step 0.5 (Ubiquitous Language update). Pass this when a caller skill (e.g., `ywc-create-pr`, `ywc-finish-branch`) has already run the update, to prevent a duplicate invocation. |

No flags are needed when invoking directly via `/ywc-commit`.

## Commit Message Format

Matches the project's existing `git log` style. General format:

```text
<type>(<scope>): <summary>

<body — only when needed>
```

**Common types** (use only what this repository already uses):
`feat`, `fix`, `refactor`, `perf`, `chore`, `docs`, `test`

**Scope**: derived from `git log` patterns (package name, module name, etc.). Omit when the change spans multiple areas.

Do not add a `Co-Authored-By` trailer by default. Add one only when recent commit history consistently uses an AI co-author trailer or the user explicitly requests it. If there is no repository convention and the user asks for one, use `Co-Authored-By: Claude <noreply@anthropic.com>`.

## Report Format

After all commits are done:

```text
✅ N commit(s) created [+ pushed]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
Excluded files: <list if any, omit if none>
```

## Error Handling

| Situation | Behavior |
| --- | --- |
| UNKNOWN file found | Show classification table to user and wait for approval |
| Hook failure | Never use `--no-verify`; report root cause and stop |
| Direct commit to main/master | Ask user for confirmation first |
| Non-fast-forward push rejected | Explain the situation and present options; force-push only on explicit request |
| Secret or artifact file found | Inform user and exclude from commit |

## Integration

This Skill integrates with:

- **ywc-ubiquitous-language** — Called in Step 0.5 with `--mode update` to sync the domain glossary before committing
- **ywc-create-pr** — Step 4 of `ywc-create-pr` delegates to this skill with `--skip-ubiquitous-update` after running the UL update itself
- **ywc-finish-branch** — Invoked indirectly via `ywc-create-pr` during branch lifecycle completion
- **ywc-sequential-executor** — May reference this skill during the commit phase of task execution

## Example Prompts

```text
/ywc-commit
commit and push
commit only the authentication-related files
/ywc-commit --skip-ubiquitous-update  # when delegated from a caller skill
```
