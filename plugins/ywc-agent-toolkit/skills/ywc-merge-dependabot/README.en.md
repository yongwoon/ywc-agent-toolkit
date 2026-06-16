# Merge Dependabot Skill (Codex)

## Overview

This skill safely batch-merges Pull Requests created by Dependabot.
It can be used from both Claude Code and Codex CLI.

## Features

- Merge all Dependabot PRs or only security-related PRs
- Run pre-merge safety checks for Dockerfile `FROM` changes, major version upgrades, and CI status
- Attempt merge-conflict resolution and wait for CI reruns
- Process PRs sequentially by ascending PR number by default
- **Parallel-auto mode**: group PRs into lockfile ecosystem lanes and keep one active auto-merge PR per lane to reduce wall-clock time for large batches
- Emit a final summary report

## Usage

### Claude Code

```text
/ywc-merge-dependabot                          # all PRs, sequential
/ywc-merge-dependabot security                 # security PRs only, sequential
/ywc-merge-dependabot parallel-auto            # all PRs, ecosystem-lane auto-merge
/ywc-merge-dependabot security parallel-auto   # security PRs only, ecosystem-lane auto-merge
```

### Codex CLI

```text
Use $ywc-merge-dependabot to merge all open Dependabot pull requests.
Use $ywc-merge-dependabot security to merge only security-related Dependabot PRs.
Use $ywc-merge-dependabot parallel-auto to merge a large batch via ecosystem-lane auto-merge scheduling.
Use $ywc-merge-dependabot security parallel-auto to combine the security scope with the parallel-auto execution flag.
```

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Merge permission for the target repository
- For `parallel-auto`: repository "Allow auto-merge" enabled. If disabled, the skill falls back to sequential mode.

## Modes

This skill supports two orthogonal flags.

**Scope flag** — target PRs:

| Token | Scope |
| --- | --- |
| `security` | Security-related Dependabot PRs only |
| _(none)_ | All Dependabot PRs |

**Execution flag** — processing strategy:

| Token | Execution | When to use |
| --- | --- | --- |
| `parallel-auto` | Ecosystem lanes + one active auto-merge PR per lane | Five or more PRs spread across multiple ecosystems |
| _(none)_ | Sequential by ascending PR number | Small batches or strict branch protection environments |

## Skip Conditions

| Condition | Reason |
| --- | --- |
| Dockerfile `FROM` change | Container base image changes need manual review |
| Major version upgrade | Breaking change risk |
| CI not passing | Prevents merging failed builds/tests |

## Result Format

```text
Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2)

- Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- Skipped   (Major version)  : #130 Bump webpack from 4.x to 5.x
- Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 - CONFLICTING after 30 min
```

Sequential mode still prints the `Mode` line, but omits the `Ecosystem groups` header and per-PR ecosystem annotations.

## File Structure

```text
ywc-merge-dependabot/
├── README.md
├── README.en.md / README.ja.md / README.ko.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── group-by-ecosystem.py
```

## Related Skills

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — create PRs
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — handle PR review comments
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — generate release PR lists
