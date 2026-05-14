# Merge Dependabot Skill

A Codex Skill for safely batch-merging Pull Requests created by Dependabot.

## Overview

This Skill detects Dependabot PRs, applies pre-merge safety checks, and processes them in ascending PR-number order.

### Key Features

- Batch-detects and merges Dependabot PRs
- Supports a security-only merge mode
- Checks Dockerfile base image changes, major-version upgrades, and CI status before merge
- Attempts conflict resolution when possible
- Generates a summary report at the end

## Usage

```text
/merge-dependabot
/merge-dependabot security
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- The user has merge permission on the repository
- Dependabot PRs already exist in the repository

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
