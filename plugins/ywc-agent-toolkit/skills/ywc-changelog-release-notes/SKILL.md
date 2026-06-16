---
name: ywc-changelog-release-notes
description: >-
  (ywc) Use when generating CHANGELOG.md entries or user-facing release notes
  from git history, merged PRs, or ywc-release-pr-list output after completing a
  release or sprint. Triggers: "changelog 작성", "릴리즈 노트 생성", "release
  notes", "변경 이력 업데이트", "CHANGELOG 업데이트", "릴리스 노트",
  "リリースノート作成", "変更履歴", "changelog", "what changed in this release",
  "今回の変更". Do not use for listing merged PRs as an attribution table (use
  ywc-release-pr-list), committing release-note changes (use ywc-commit),
  creating the release PR (use ywc-create-pr), or incident analysis after a
  release fix (use ywc-incident-postmortem).
---


**Announce at start:** "I'm using the ywc-changelog-release-notes skill to generate CHANGELOG entries and release notes."

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "git log is good enough for release notes" | Raw commits are too technical for users and inconsistently formatted even for developers. |
| "My project is too small for a CHANGELOG" | Even small projects benefit from structured history when debugging regressions or onboarding users. |
| "I'll write it manually — it's faster" | Manual writing misses commits, inconsistently categorizes, and skips security entries. |
| "ywc-release-pr-list already covers this" | ywc-release-pr-list *lists* PRs in a table; this skill *formats* them as readable, categorized changelog entries. |
| "Release notes and CHANGELOG are the same thing" | Technical CHANGELOG targets developers (breaking changes, API diffs); release notes target users (features in plain language). |
| "Keep a Changelog format is too rigid" | The format is a starting template. Categories prevent omitting security entries and ensure consistent grouping. |
| "I can just tag and push without notes" | Undocumented releases create support burden. Users ask what changed; a changelog prevents repetitive questions. |

## Arguments

| Flag | Description |
|---|---|
| `--changelog` | Generate CHANGELOG.md entry in Keep a Changelog format (default) |
| `--release` | Generate user-facing release notes in plain language |
| `--both` | Generate both CHANGELOG entry and user-facing release notes |
| `--from <tag>` | Start diff from this git tag (default: last tag from `git describe`) |
| `--to <ref>` | End diff at this ref (default: HEAD) |
| `--version <v>` | Set the release version string (e.g., `1.2.0`) |
| `--pr-list <file>` | Read PR list from ywc-release-pr-list output instead of git log |
| `--dry-run` | Print to stdout only — do not modify CHANGELOG.md |

## Dynamic Context

```bash
# Last tag to determine version range
git describe --tags --abbrev=0 2>/dev/null || echo "(no tags yet)"

# Commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null)..HEAD --oneline 2>/dev/null | head -30

# Merged PRs if gh CLI is available
gh pr list --state merged --limit 30 --json number,title,mergedAt,labels 2>/dev/null | head -c 3000
```

## Workflow

**Step 1 — Detect version range**
Determine `from` (last tag or `--from`) and `to` (HEAD or `--to`). If `--version` is not provided, use AskUserQuestion to ask for it, then **immediately continue to Step 2 in the same turn** — do not end the turn or wait for further input after receiving the answer.

**Step 2 — Parse commits**
Group by conventional commit type: `feat` → Added, `fix` → Fixed, `refactor`/`chore` → internal (omit from user notes), `security` → Security, `BREAKING CHANGE` → Changed.

**Step 3 — Enrich from PRs**
If gh CLI is available or `--pr-list` is provided, use PR titles and labels for richer descriptions than raw commit messages.

**Step 4 — Generate CHANGELOG entry**
Keep a Changelog format: Added / Changed / Deprecated / Removed / Fixed / Security. Prepend to CHANGELOG.md (or `--dry-run` to stdout).

**Step 5 — Generate release notes (if --release or --both)**
Plain language summary: remove technical jargon, omit internal refactors and dependency bumps, frame features from user perspective.

**Step 6 — Suggest git tag command**
Output: `git tag -a v1.2.0 -m "Release v1.2.0"` for the developer to run.

## Output Format

### CHANGELOG.md entry (Keep a Changelog)

```markdown
## [1.2.0] - 2026-05-01

### Added
- User profile photo upload

### Fixed
- Login redirect loop after password reset (#42)

### Security
- Upgraded dependency X to address CVE-YYYY-XXXXX
```

### User-facing release notes

```markdown
# What's new in v1.2.0

**Profile photos**: You can now upload a photo from Settings → Profile.

**Bug fixes**: Fixed an issue where users were sent back to the login page
after resetting their password.
```

See [references/changelog-format.md](references/changelog-format.md) for the full Keep a Changelog spec and category definitions.
See [references/release-notes-format.md](references/release-notes-format.md) for user-facing writing guidelines and examples.

## Integration

- **After `ywc-release-pr-list`**: Feed the PR table output via `--pr-list` for richer, PR-linked descriptions.
- **Before `ywc-create-pr`**: Include the CHANGELOG.md update as part of the release PR.
- **After `ywc-commit`**: Run this skill to document the batch of changes before tagging.
- **After `ywc-incident-postmortem`**: If an incident led to a patch release, key action items inform the Security or Fixed entry.

## Banned Output Patterns

| Pattern | Problem | Replace with |
|---|---|---|
| "Various bug fixes and improvements" | Meaningless to users | List each specific fix |
| Commit hashes in user-facing notes | Users don't use git | PR numbers or feature names |
| Internal code names or module paths | Users don't know internal structure | User-visible feature names |
| Security entries only in user notes | Developers need CVE details | CVE reference in CHANGELOG; plain summary in release notes |
| Refactor/chore entries in user notes | Not relevant to users | Omit from release notes; include only in CHANGELOG |

## Validation

Before finalizing, report the release-note result with:

```text
Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
Artifacts: <CHANGELOG entry path and/or release notes path>
Sources: <commits, PR list, tags, or incident documents used>
Validation: <banned patterns checked and category placement verified>
Next action: <release handoff or "none">
```

Verify that every entry maps to a concrete source, user-facing notes omit irrelevant internal refactors, developer changelog entries keep required technical/security references, and banned generic wording is absent.
