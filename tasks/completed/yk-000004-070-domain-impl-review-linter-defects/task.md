# yk-000004-070-domain-impl-review-linter-defects — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-impl-review/references/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Add the linter rule table**
  - [ ] Port the table from the snapshot `coderabbit-methodology.md`; keep the three constraints (installed only, changed files only, no config edits)
- [ ] **Create the appendix and entries**
  - [ ] Add `## Appendix — mined entries`, Table of contents entry, ID-rule paragraph, then A-005, A-006, A-007 as `###` headings
  - [ ] Add the 'A-001–A-004 not ported' line
- [ ] **Add cross-references**
  - [ ] One line in each of `devex-agent.md` and `security-agent.md` linking to the new material

## Acceptance Coverage
Covers: AC5

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -cE -- '^### A-00[567]' claude-code/skills/ywc-impl-review/references/recurring-defects.md | tr -d ' ')" = 3 ]`
- [ ] `grep -q 'zizmor' claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`
- [ ] `grep -q 'ruff check --select S110' claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`
- [ ] `grep -q 'Appendix' claude-code/skills/ywc-impl-review/references/recurring-defects.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` exits 0 (no mechanical regression)
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` — Phase A tasks do NOT commit the baseline file (parallel tasks would conflict on it; B3 records the before/after gate)

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
