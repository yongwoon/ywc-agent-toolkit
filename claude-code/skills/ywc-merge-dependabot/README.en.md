# Merge Dependabot Skill

A Claude Code Skill for safely batch-merging Pull Requests created by Dependabot.

## Overview

This Skill detects Dependabot PRs, applies pre-merge safety checks, and processes them in ascending PR-number order.

### Key Features

- Batch-detects and merges Dependabot PRs
- Supports a security-only merge mode
- Checks Dockerfile base image changes, major-version upgrades, and CI status before merge
- Attempts conflict resolution when possible
- **Parallel-auto mode**: groups PRs by lockfile ecosystem and delegates serialization to GitHub's auto-merge queue, reducing wall-clock time for large batches
- Generates a summary report at the end

## Usage

```text
/ywc-merge-dependabot                          # all PRs, sequential
/ywc-merge-dependabot security                 # security PRs only, sequential
/ywc-merge-dependabot parallel-auto            # all PRs, ecosystem-grouped auto-merge
/ywc-merge-dependabot security parallel-auto   # security PRs only, ecosystem-grouped auto-merge
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
