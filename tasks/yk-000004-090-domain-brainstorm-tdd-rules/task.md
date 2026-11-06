# yk-000004-090-domain-brainstorm-tdd-rules — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-brainstorm/SKILL.md`
  - `claude-code/skills/ywc-tdd-ritual/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Brainstorm rules**
  - [ ] Port the two question-ordering rules into `ywc-brainstorm/SKILL.md`
- [ ] **tdd-ritual SKILL.md**
  - [ ] Add the horizontal-slicing row, the seam catches/misses line, and the ~50-line setup row to the Rationalization Defense table
- [ ] **Align the two references**
  - [ ] Edit `test-shape-cookbook.md:77` and `red-green-checklist.md:18` as listed in Scope

## Acceptance Coverage
Covers: AC7b

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/references/test-shape-cookbook.md`
- [ ] `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/references/red-green-checklist.md`
- [ ] `[ "$(grep -c -- '~10 lines' claude-code/skills/ywc-tdd-ritual/references/red-green-checklist.md | tr -d ' ')" = 0 ]`
- [ ] `grep -q '~50 lines' claude-code/skills/ywc-tdd-ritual/SKILL.md`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-brainstorm/SKILL.md claude-code/skills/ywc-tdd-ritual/SKILL.md`
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

- `ywc-tdd-ritual/SKILL.md` already had a verbose "test setup is so big" row (200-line wording), so the ~50-line threshold replaced that number in place instead of adding a duplicate row. Row now reads: "Unit test setup over ~50 lines signals the design is wrong. Listen to the test: …".
- Added the horizontal-slicing row (verbatim from the snapshot) and extended the "Write the seam first" bullet with the catches/misses line.
- `ywc-brainstorm/SKILL.md` Step 3, added after "If the initial request already answers one of these…":
  - "**Facts are your job; decisions are the user's.** Before asking, check whether the answer lives in the environment …"
  - "**Ask from the frontier.** Pick the next question only from those whose prerequisite decisions are already settled. …"
