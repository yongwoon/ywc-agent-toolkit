# ywc-sequential-executor

This document introduces the Codex `ywc-sequential-executor` workflow. The authoritative trigger conditions, anti-triggers, execution steps, and output format are defined in [SKILL.md](./SKILL.md).

## Localized Versions

- [한국어](./README.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)

## When To Use

- The user uses one of the skill's trigger phrases or an equivalent natural-language request.
- Codex needs the skill-specific workflow and validation criteria before acting.
- Another `ywc-*` skill references this skill as an upstream or downstream step.

## Usage

```bash
$ywc-sequential-executor
```

Follow the Arguments or Workflow sections in [SKILL.md](./SKILL.md) for supported options and modes.

### Key Modes

- `--aggregate-pr`: runs each task on its own feature branch, local-merges each result into one work branch, and delivers the range through one final work -> base PR.
- `--group-name <name>`: pins the aggregate work branch to `work/<name>`. It is valid only with `--aggregate-pr`.
- `--worktree`: runs the whole sequential invocation inside one run worktree outside the main checkout. It is not a delivery mode and can combine with other mode flags.
- Stale `.ywc-run-state.json` guard: when the saved run-state does not match the newly requested explicit range, the executor does not auto-resume. It asks whether to resume the saved run-state or delete it and start the new run.

```bash
$ywc-sequential-executor 001010..003020 --aggregate-pr --group-name billing-rollout
```

```bash
$ywc-sequential-executor 001010..003020 --worktree --pr-lang ko
```

## Output

This skill follows the report, artifact, and status format defined in [SKILL.md](./SKILL.md). If the skill emits Completion Status, preserve the meanings of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, and `NEEDS_CONTEXT`.
