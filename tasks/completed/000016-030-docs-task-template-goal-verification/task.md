# 000016-030-docs-task-template-goal-verification — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000016-010-docs-principles-guideline-gap` is completed (merged).

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-task-generator/references/task.md.template`.
- [ ] Stay within `codex/skills/ywc-task-generator/evals/evals.json` if adding objective eval coverage.
- [ ] If the task requires edits outside Ownership, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if the template change requires rewriting task generator workflow sections outside the reference template.
- [ ] Stop if the new template becomes a long tutorial rather than a concise checklist.
- [ ] Stop if eval changes require global eval runner modifications.

## Implementation Steps
- [ ] Update `Implementation Steps` placeholders in `task.md.template` to require target file/module, related AC/FR, contract/behavior change, and verification command/evidence.
  - Related AC/FR: AC4, FR-3
  - Contract / Behavior Change: generated tasks expose traceability from step to spec outcome.
  - Verification Command / Evidence: `rg -n "Related AC/FR|Contract / Behavior Change|Verification Command / Evidence" codex/skills/ywc-task-generator/references/task.md.template`
- [ ] Update `Task Verify` placeholders to include task-specific command, expected passing signal, pre-change failing evidence or exception, and contract/test evidence.
  - Related AC/FR: AC5, FR-3
  - Contract / Behavior Change: generated tasks make verification evidence explicit before implementation can be marked done.
  - Verification Command / Evidence: `rg -n "Pre-change Failing Evidence|Exception|contract/test evidence|expected passing" codex/skills/ywc-task-generator/references/task.md.template`
- [ ] Add concise guidance that a task is not ready when steps cannot be traced to a spec outcome.
  - Related AC/FR: AC4, FR-3
  - Contract / Behavior Change: task generator refuses untraceable implementation steps.
  - Verification Command / Evidence: `rg -n "not ready|spec outcome|AC/FR" codex/skills/ywc-task-generator/references/task.md.template`
- [ ] Inspect `codex/skills/ywc-task-generator/evals/evals.json` and add an objective regression case if supported.
  - Related AC/FR: AC9, FR-6
  - Contract / Behavior Change: mechanical eval catches task output missing AC/FR and verification evidence.
  - Verification Command / Evidence: `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-task-generator --format json`

## Task Verify
- [ ] Run `rg -n "Related AC/FR|Contract / Behavior Change|Verification Command / Evidence|Pre-change Failing Evidence|Exception" codex/skills/ywc-task-generator/references/task.md.template`.
- [ ] Run `python tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --root . --skill ywc-task-generator --format json`.

## Verification
- [ ] Targeted grep checks pass.
- [ ] Skill eval score command completes or its failure is reported with cause.
- [ ] Full repository validation is deferred to `000017-010-infra-codex-karpathy-validation`.
