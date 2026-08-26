# yw-000002-020-consumer-legacy-compatibility — Implementation Checklist

## Prerequisites
- [ ] `yw-000001-030-parser-prefixed-task-ids` is completed and merged.
- [ ] `yw-000002-010-task-generator-initials-allocation` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within the executor, finish-branch, and shared task-generator reference/documentation paths listed in `README.md`.

## Stop Conditions
- [ ] Stop if an existing task directory or legacy dependency reference would need renaming.
- [ ] Stop if a consumer requires parser behavior outside the predecessor task’s contract.
- [ ] Stop if changes spill into `claude-code/**`.

## Hardening Gate
- [ ] Record existing executor/finish-branch coverage or targeted contract scans before edits.
- [ ] Record the cross-skill task ID grammar contract.
- [ ] Mark Data Integrity Hardening N/A for documentation/consumer compatibility edits.

## Implementation Steps
- [ ] Update sequential executor range-selection and completion-move documentation/examples to accept prefixed and legacy forms.
- [ ] Update parallel executor wave/range parsing contracts and examples without changing worktree lifecycle semantics.
- [ ] Update finish-branch task-number/PR-title and completion-flow references to preserve both formats.
- [ ] Update task-generator dependency-graph and execution-convention templates with prefixed examples and legacy-transition notes.
- [ ] Add or adjust eval expectations for mixed prefixed/legacy dependencies and ranges.

## Task Verify
- [ ] Run focused sequential/parallel executor contract evals.
- [ ] Run finish-branch parser and completion-flow checks.
- [ ] `rg -n '\[PHASE\]-\[SEQUENCE\]|000001-010|yw-000001-010' codex/skills/ywc-task-generator codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor codex/skills/ywc-finish-branch`
- [ ] Confirm no `claude-code/**` files changed.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Markdown/Bash skill tooling)
- [ ] unit tests pass (focused executor/finish-branch fixtures)
- [ ] integration tests pass (N/A — no external integration)
- [ ] app builds without error (N/A — documentation/tooling repository)
