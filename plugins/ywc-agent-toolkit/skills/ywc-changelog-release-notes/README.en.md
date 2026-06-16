# ywc-changelog-release-notes

A skill for generating CHANGELOG.md entries and user-facing release notes
from git history, merged PRs, or ywc-release-pr-list output.
Produces both a technical CHANGELOG (Keep a Changelog format) and a
plain-language user-facing release summary as separate documents.

## Core concept: two distinct outputs

This skill produces **two documents with different purposes**.

| | CHANGELOG.md | Release Notes |
|---|---|---|
| Audience | Developers, maintainers | End users, customers |
| Includes | All changes, CVEs, PR numbers | User-visible changes only |
| Tone | Technical, concise | Plain language, benefit-oriented |
| refactor/chore | Included | Omitted |

## Usage scenarios

### Case 1: Before tagging a new release (most common)

```
/ywc-changelog-release-notes --both --version 1.2.0
```

Generates both a developer-facing CHANGELOG.md entry and a user-facing Release Notes document in one pass.
Use this when you need content for the GitHub Release page.

### Case 2: Updating CHANGELOG.md only

```
/ywc-changelog-release-notes --changelog
```

Use for internal projects with no external users, where only a developer-facing change history is needed.
Run this before creating a `git tag`.

### Case 3: Writing a customer announcement or Slack post

```
/ywc-changelog-release-notes --release
```

Use when writing user-facing announcements such as "v1.3.0 is now live."
Technical details are filtered out automatically and reframed from the user's perspective.

### Case 4: Preview before modifying files

```
/ywc-changelog-release-notes --dry-run
```

Use to see what would be written to `CHANGELOG.md` before actually modifying the file.
Review the output, then re-run without `--dry-run` if it looks correct.

### Case 5: Combining with `ywc-release-pr-list`

When a PR list has already been prepared, feed it as input to this skill.

```
/ywc-release-pr-list > pr-list.md
/ywc-changelog-release-notes --both --pr-list pr-list.md --version 1.2.0
```

`ywc-release-pr-list` lists PRs in a table; this skill **formats** them as readable, categorized CHANGELOG entries.

## All flags

```
/ywc-changelog-release-notes --changelog              # CHANGELOG.md entry only
/ywc-changelog-release-notes --release                # User-facing release notes only
/ywc-changelog-release-notes --both --version 1.2.0  # Generate both documents
/ywc-changelog-release-notes --from v1.1.0 --to HEAD # Specific range
/ywc-changelog-release-notes --dry-run               # Print to stdout, no file changes
```

## Typical release flow

```
1. ywc-release-pr-list          → Compile the PR list for this release
2. ywc-changelog-release-notes  → Generate CHANGELOG + Release Notes
3. ywc-commit                   → Commit the updated CHANGELOG.md
4. ywc-create-pr                → Create the release PR
5. git tag -a v1.2.0 -m "..."   → Tag the release (skill suggests the command)
```

## Related skills

- `ywc-release-pr-list` — Generate the PR list to feed into `--pr-list`
- `ywc-commit` — Commit the updated CHANGELOG.md
- `ywc-create-pr` — Create the release PR
- `ywc-incident-postmortem` — Postmortem for incidents that drove a patch release
