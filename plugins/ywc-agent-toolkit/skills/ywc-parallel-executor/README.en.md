# ywc-parallel-executor

This document introduces the Codex `ywc-parallel-executor` workflow. The authoritative trigger conditions, anti-triggers, execution steps, and output format are defined in [SKILL.md](./SKILL.md).

## Localized Versions

- [한국어](./README.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)
- [Español](./README.es.md)
- [中文](./README.zh.md)

## When To Use

- The user uses one of the skill's trigger phrases or an equivalent natural-language request.
- Codex needs the skill-specific workflow and validation criteria before acting.
- Another `ywc-*` skill references this skill as an upstream or downstream step.

## Usage

```bash
$ywc-parallel-executor
```

Follow the Arguments or Workflow sections in [SKILL.md](./SKILL.md) for supported options and modes.

## Docker Isolation

For task worktrees that use Docker Compose, the executor delegates port isolation to `ywc-docker-isolate`: it audits selected task stacks before creating worktrees, sets up deterministic per-task ports after each worktree is verified, and tears down successful task stacks before pruning worktrees. BLOCKED or preserved worktrees keep their Docker state for recovery.

## Contract Gates

Wave planning treats shared public contracts as Shared Surfaces, not just file paths. Worker payloads require Changed Public Contracts, Critical Internals, Cross-Module Impact, and test evidence; behavior-changing tasks without authored/executed tests must provide an explicit TDD exception or remain blocked/with concerns.

## Delivery Modes

| Mode | Behavior |
|---|---|
| `--local-merge` | Locally merges each task into the base branch and pushes immediately. No PR is created. |
| `--draft` | Accumulates task changes through local merges, then creates one aggregate draft PR at the end. |
| `--per-task-pr` | For each task, creates a PR, waits for CI, handles bot reviews, refreshes against the latest base, merges the PR, syncs base, and marks the task complete. |
| `--aggregate-pr` | Groups the whole invocation into one aggregate branch and PR, then completes ready → CI → bot review → merge. |

In `--per-task-pr`, an earlier task in the same wave may advance the base branch. Before merging, the executor checks whether the PR branch contains the latest base; if not, it merges the base into the worktree branch, pushes, and re-verifies CI. A base-refresh conflict is reported as `BLOCKED`, and the PR is not merged using CI results from an older head SHA.

## Group Execution

Use `--aggregate-pr --group-name <name>` when many tasks should be delivered as one group-level PR. To run multiple groups concurrently, use one independent clone per group rather than worktrees. The canonical procedure and concurrency rules live in [references/aggregate-pr.md](./references/aggregate-pr.md).

## Output

This skill follows the report, artifact, and status format defined in [SKILL.md](./SKILL.md). If the skill emits Completion Status, preserve the meanings of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, and `NEEDS_CONTEXT`.
