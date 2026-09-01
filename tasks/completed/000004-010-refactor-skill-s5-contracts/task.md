# 000004-010-refactor-skill-s5-contracts — Implementation Checklist

## Prerequisites
- [ ] Confirm this is a root task and no predecessor task is required
- [ ] Read `docs/ywc-plans/codex-toolkit-eval-improvements.md`
- [ ] Read `docs/ywc-plans/codex-toolkit-eval-improvements.validation.md`

## Allowed Edit Scope
- [ ] Stay within the Codex skill directories listed in `README.md`
- [ ] If changes are needed outside those directories, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a target skill would exceed the 500-line body guideline without moving examples into `evals/evals.json`
- [ ] Stop if an added eval fixture would be empty, generic, or not tied to observable skill behavior
- [ ] Stop if any Codex `SKILL.md` frontmatter gains fields other than `name` and `description`

## Implementation Steps

- [ ] **Map current S5 signals**
  - [ ] For each target skill, identify which of the four S5 scorer buckets already exists
  - [ ] Record any skill that already has `scripts/` so `evals/` is not incorrectly counted as a new distinct bucket

- [ ] **Patch P0 skills**
  - [ ] Add `## Output Format`, `## Validation`, `Status:` report contract, and realistic eval fixture for `ywc-product-review`
  - [ ] Add output path/report contract, pre-creation validation checklist, status states, and eval fixture for `ywc-project-docs`
  - [ ] Add scaffold report contract, validation checklist, status states, and eval fixture for `ywc-project-scaffold`
  - [ ] Convert `ywc-team-assemble` `## Output` to `## Output Format`, then add validation gate, status states, and eval fixture

- [ ] **Patch P1 skills**
  - [ ] Add explicit validation criteria and eval fixture where needed for `ywc-changelog-release-notes`
  - [ ] Ensure `ywc-create-pr` includes `Status:` and validation while preserving existing eval fixture
  - [ ] Apply Iteration 1 requirements to `ywc-gen-testcase`: `## Output Format` plus `## Validation`, with concise body changes
  - [ ] Add output format, validation, and eval fixture for `ywc-handle-pr-reviews`
  - [ ] Add validation checklist and eval fixture for `ywc-incident-postmortem`
  - [ ] Add output format/status and eval fixture for `ywc-merge-dependabot`
  - [ ] Add output format/status, validation, and eval fixture for `ywc-release-pr-list`
  - [ ] Add validation checklist and eval fixture for `ywc-ui-ux-review`
  - [ ] Apply Iteration 1 requirements to `ywc-worktrees`: `## Output Format`, `## Validation`, and `Status:` result shape

- [ ] **Validate contract quality**
  - [ ] Ensure every new `evals/evals.json` uses matching `skill_name`
  - [ ] Include at least three realistic prompts where feasible
  - [ ] Include expected behavior and concrete anti-behavior

## Task Verify
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --format markdown --target all`
- [ ] Confirm all target skills from FR-1 now show S5 >= 3
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] validation passes (`bash scripts/validate.sh`)
- [ ] mechanical score command shows no target S5 below 3
- [ ] no project build command exists beyond repository validation
