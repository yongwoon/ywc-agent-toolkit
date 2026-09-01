# 000033-030-docs-executor-integrity-gates - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000033-010-docs-impl-review-integrity-catalog` is completed or its terminology/severity wording is available.
- [ ] Existing executor Task Verify failure handling has been read in both target SKILL files.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/ywc-sequential-executor/**` and `codex/skills/ywc-parallel-executor/**`.
- [ ] If task-generator wording needs changes, stop; that belongs to `000033-020-docs-spec-task-integrity-guidance`.

## Stop Conditions

- [ ] Stop if the proposed wording would weaken existing CI/merge/Task Verify gates.
- [ ] Stop if changes require altering branch lifecycle, PR lifecycle, or worktree lifecycle.
- [ ] Stop if README locale updates require broad translation regeneration beyond mirror maintenance.

## Hardening Gate

- [ ] Classify this task: docs-only executor behavior guidance.
- [ ] Record named exception: no executable behavior; replacement verification is targeted `rg` plus final validation.
- [ ] Record interface contract: executor must run generated data-integrity Task Verify gates before delivery.
- [ ] Require full review before DONE because this affects delivery gates for critical write tasks.

## Implementation Steps

- [ ] Update `codex/skills/ywc-sequential-executor/SKILL.md`.
  - [ ] In implementation or verification guidance, state that concurrency, transaction rollback, and idempotency Task Verify entries are mandatory for DB/API write tasks.
  - [ ] State that lint/typecheck/build alone cannot replace those task-specific checks.
  - [ ] Preserve existing failure handling: failed Task Verify blocks delivery after allowed fix attempts.
- [ ] Update `codex/skills/ywc-parallel-executor/SKILL.md`.
  - [ ] Add equivalent directive to per-task worker prompt or Task Verify section.
  - [ ] Ensure wave execution still treats failed Task Verify as task-level failure before delivery.
  - [ ] Preserve existing worktree and wave lifecycle rules.
- [ ] Review README mirrors for both executor skills.
  - [ ] Update only if README mirrors Task Verify behavior details.
  - [ ] Record no-change rationale if README remains high-level.

## Task Verify

- [ ] `rg -n "concurrency|concurrent|rollback|idempotency|Task Verify" codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`
- [ ] `bash scripts/install.sh --list --codex`

## Verification

- [ ] repository validation deferred to `000034-010-infra-codex-integrity-validation`
- [ ] generated plugin sync deferred to `000034-010-infra-codex-integrity-validation`
