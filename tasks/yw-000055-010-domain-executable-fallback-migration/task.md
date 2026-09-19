# Implementation Task

## Prerequisites

- [ ] `yw-000054-010-infra-bundle-executable-resolver` is complete and its shared launcher block is available.
- [ ] Read the closed inventory in the specification and map all 20 sites before editing.

## Allowed Edit Scope

Edit only the eleven Codex caller files listed in the task README. Do not edit resolver implementation, tests, agents, or generated plugin output.

## Stop Conditions

- Stop if a caller needs a resolver behavior not defined by the canonical contract.
- Stop if preserving an invocation requires shell evaluation or changed arguments.
- Stop immediately if `mark-complete.sh` would mutate task or Git state before compactor resolution.

## Hardening Gate

- RED-first evidence: use the resolver contract and inventory mapping as the pre-edit feedback path; downstream regression tests are mandatory.
- Public surface: preserve each caller's current executable type, arguments, pipeline ordering, and exit-result semantics.
- Data Integrity: apply the `mark-complete.sh` resolve-before-mutation invariant and regression requirement.
- Critical surface: full review of every changed executable-selection site is required.

## Implementation Steps

- [ ] Replace fallback clauses in `ywc-code-gen`, `ywc-create-pr`, `ywc-finish-branch`, `ywc-handle-pr-reviews`, `ywc-onboard-repo`, `ywc-parallel-executor`, `ywc-release-pr-list`, `ywc-skill-author`, and `ywc-spec-writer` with the exact shared launcher block.
  - [ ] Resolve both executables before running the `ywc-spec-writer` pipeline.
  - [ ] Preserve `bash`, `python`, and `python3` invocation forms and all existing arguments.
- [ ] Migrate `codex/skills/scripts/mark-complete.sh` so compactor resolution completes before `mkdir`, move, staging, or commit.
- [ ] Migrate the two direct target-relative test-script commands in `ywc-task-generator/SKILL.md` and link every caller to the shared reference.

## Task Verify

- [ ] Run the repository complement search specified by the hardening spec and confirm all 20 sites are migrated or explicitly documented.
- [ ] `bash -n codex/skills/scripts/mark-complete.sh`
- [ ] `git diff --check`

## Verification

- [ ] `bash scripts/validate.sh`

