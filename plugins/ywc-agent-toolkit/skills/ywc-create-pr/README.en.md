# Create PR

A Codex Skill that commits changes and creates a draft PR based on the repository's PR template.

## Overview

After work on a feature branch is complete, this Skill automates the flow from commit creation to draft PR creation.

### Key Features

- Automatically detects the base branch in the order `develop` → `main` → `master`
- Runs a security check for sensitive files such as `.env`, `*.key`, and `*.pem`
- Supports pre-push CI checks such as lint, format, typecheck, and test
- Applies `.github/pull_request_template.md` when available
- Creates every PR as a draft
- Supports PR title/body prose in `en`, `ja`, `ko`, `zh`, or `es` via `--lang` / `--language`, while keeping task IDs, branch names, file paths, commands, labels, and explicit `--title` values unchanged
- Cites related design background by checking the branch's task `## Spec Reference` first, then best-effort fuzzy matching under `docs/ywc-plans/`

## Usage

```text
$ywc-create-pr
$ywc-create-pr main
$ywc-create-pr --skip-ci-check
$ywc-create-pr main --skip-ci-check
$ywc-create-pr --lang zh
$ywc-create-pr --language spanish
$ywc-create-pr --plan-doc docs/ywc-plans/20260814-small_example.md
$ywc-create-pr --no-plan-ref
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- Work is being done on a feature branch in a Git repository

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
- [Chinese (Simplified)](./README.zh.md)
- [Spanish](./README.es.md)
