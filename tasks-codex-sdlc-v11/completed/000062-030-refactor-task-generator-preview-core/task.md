# 000062-030-refactor-task-generator-preview-core — Implementation Checklist

## Prerequisites

- [ ] Phase 000061 complete.
- [ ] Existing `tasks/000060-*` content is treated as reference only; do not copy Claude-only paths or depend on that batch.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-task-generator/SKILL.md` core command/workflow sections and direct core reference only.

## Stop Conditions

- [ ] a write can occur without matching `--spec` and approved persisted preview이면 중단한다.
- [ ] path validation follows symlinks outside allowed roots, or SKILL body exceeds 500 lines이면 중단한다.

## Implementation Steps

- [ ] argument/identity contract을 정의한다.
  - `--spec`, `--preview-only`, `--preview-path`, `--approve-preview`, `--non-interactive`의 allowed combinations와 safe roots를 명시한다.
  - Related AC/FR: AC3, AC4, Amendments B/M/N.
- [ ] two-phase preview semantics을 정의한다.
  - preview-only는 canonical preview만 write; approved call은 re-decompose하지 않고 matching digest/revision만 consume한다.
  - Related AC/FR: AC3, AC4, Amendment H.
- [ ] wide-refactor row fields와 digest invalidation을 명시한다.
  - Refactor Phase, Batch ID, Depends On 변화가 approval invalidation을 유발한다.
  - Related AC/FR: AC9, Amendment L.

## Task Verify

- [ ] `wc -l codex/skills/ywc-task-generator/SKILL.md`
  - Expected Passing Signal: <=500 lines.
  - Pre-change Failing Evidence / Exception: preview contract absent.
  - Contract/Test Evidence: line count and reference link check.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: core preview contract tokens/IDs pass once assets task lands; otherwise record deferred dependency.
  - Pre-change Failing Evidence / Exception: new contract.
  - Contract/Test Evidence: runner output.

## Verification

- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-task-generator` passes.
