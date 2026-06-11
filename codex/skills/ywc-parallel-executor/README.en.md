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

## Delivery Modes

| Mode | Behavior |
|---|---|
| `--local-merge` | Locally merges each task into the base branch and pushes immediately. No PR is created. |
| `--draft` | Accumulates task changes through local merges, then creates one aggregate draft PR at the end. |
| `--per-task-pr` | For each task, creates a PR, waits for CI, handles bot reviews, refreshes against the latest base, merges the PR, syncs base, and marks the task complete. |

In `--per-task-pr`, an earlier task in the same wave may advance the base branch. Before merging, the executor checks whether the PR branch contains the latest base; if not, it merges the base into the worktree branch, pushes, and re-verifies CI. A base-refresh conflict is reported as `BLOCKED`, and the PR is not merged using CI results from an older head SHA.

## Output

This skill follows the report, artifact, and status format defined in [SKILL.md](./SKILL.md). If the skill emits Completion Status, preserve the meanings of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, and `NEEDS_CONTEXT`.
