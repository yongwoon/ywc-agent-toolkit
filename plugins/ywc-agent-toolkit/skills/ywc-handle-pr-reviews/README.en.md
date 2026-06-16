# Handle PR Reviews

A Codex Skill that checks PR review comments, applies fixes where appropriate, and replies to each thread.

## Overview

This Skill automates the repetitive work after a PR review arrives. Clear change requests are fixed directly, while ambiguous or debatable comments are surfaced for user judgment.

### Key Features

- Classifies comments into fix requests, debatable feedback, questions, and already-handled items
- Groups comments by file and handles related fixes together
- Matches the reply language to the reviewer's language
- Skips comments that were already handled or already answered

## Usage

```text
/handle-pr-reviews
/handle-pr-reviews 123
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- The command runs on a branch that already has a PR

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
