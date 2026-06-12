# Release PR List

A Codex Skill that extracts the PRs included in a release PR, groups them by author, and updates the PR description.

## Overview

When creating a release PR such as `develop` → `main`, this Skill extracts PR numbers from commit headlines, looks up their authors, and rewrites the `## PR LIST` section.

### Key Features

- Extracts PR numbers from `#<number>` patterns in commit headlines
- Groups PRs by author login and sorts them alphabetically
- On each run, asks the user whether to append a one-line summary of what each PR applied; only when confirmed does it derive a concise summary from the PR title
- Preserves the existing description except for the `## PR LIST` section
- Remains idempotent when run multiple times

## Usage

```text
/release-pr-list 301
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- The release PR has already been created

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
