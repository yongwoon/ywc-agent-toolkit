# yk-000006-010-domain-agent-description-alignment — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000005-050-domain-handoff-retro-skills` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/agents/ywc-go-reviewer.md`
  - `claude-code/agents/ywc-python-reviewer.md`
  - `claude-code/agents/ywc-typescript-reviewer.md`
  - `claude-code/agents/ywc-qa-engineer.md`
  - `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Update the three reviewer descriptions**
  - [ ] Add the defect-class phrase, remove natural-language triggers, add the `ywc-impl-review` anti-trigger to each agent
- [ ] **Verify impl-review and update qa-engineer**
  - [ ] Confirm the three per-language triggers exist in `ywc-impl-review` description (no edit)
  - [ ] Apply the qa-engineer wording changes
- [ ] **Review trigger fixtures**
  - [ ] List cases by the grep in Scope; switch affected positives to `ywc-impl-review`; run the schema test

## Acceptance Coverage
Covers: AC15

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `for a in ywc-go-reviewer ywc-python-reviewer ywc-typescript-reviewer; do grep -q 'user-typed code review request' claude-code/agents/$a.md || exit 1; done`
- [ ] `grep -q 'While authoring tests' claude-code/agents/ywc-qa-engineer.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/test_fixture_schema.py`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
