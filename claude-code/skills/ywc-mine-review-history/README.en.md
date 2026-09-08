# Mine Review History

A Claude Code Skill that batch-mines bot review comments (CodeRabbit / Codex Review / Claude Review) across many already-merged PRs and surfaces recurring defect classes as candidate durable learnings.

## Overview

Two existing Skills capture review knowledge: `ywc-review-learnings --mode update --source pr` harvests a single PR on demand, and `ywc-incident-postmortem` captures a single incident. Neither covers a **batch/retrospective sweep** of PR history that predates either Skill's adoption — that gap is what this Skill closes.

The Skill fetches bot comments across a bounded window of merged PRs, classifies each accept-vs-dismiss using the same rule `ywc-review-learnings` already applies, clusters classified comments into defect classes, and offers classes recurring across `--min-recurrence` (default 3) distinct PRs to `ywc-review-learnings --mode update --source pr` as promotion candidates. It never writes `docs/review-learnings.md` directly — every promotion goes through that Skill's own confirmation gate.

### Key Features

- Bounded scope selection (`--limit` and/or `--since`) — no unbounded default scan
- Reuses the existing `--source pr` accept/dismiss classification rule at batch scale
- Counts recurrence by **distinct PR**, not raw comment count
- Recurrence-gated promotion (`--min-recurrence`, default 3) — below-threshold classes are reported, never silently dropped
- Full report surface every run: PRs scanned, comments fetched/classified, defect classes found vs. promoted

## Usage

```text
/ywc-mine-review-history --limit 50
/ywc-mine-review-history --since 2026-01-01
/ywc-mine-review-history --limit 50 --min-recurrence 4
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## Prerequisites

- `gh` CLI is installed and authenticated
- At least one of `--limit` or `--since` is supplied

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
