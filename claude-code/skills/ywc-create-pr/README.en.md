# Create PR

A Claude Code Skill that commits changes and creates a draft PR based on the repository's PR template.

## Overview

After work on a feature branch is complete, this Skill automates the flow from commit creation to draft PR creation.

### Key Features

- Automatically detects the base branch in the order `develop` → `main` → `master`
- Runs a security check for sensitive files such as `.env`, `*.key`, and `*.pem`
- Supports pre-push CI checks such as lint, format, typecheck, and test
- Runs a mandatory author self-review of the full diff before filing (catches scope creep, leftover debug output, and secrets)
- Applies `.github/pull_request_template.md` when available
- Creates every PR as a draft

## Usage

```text
/create-pr
/create-pr main
/create-pr --skip-ci-check
/create-pr main --skip-ci-check
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- Work is being done on a feature branch in a Git repository

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
