# yk-000004-010-domain-plan-auto-converge — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-plan/**`
  - `claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Read the snapshot and the local call sites**
  - [ ] Read `${TMPDIR:-/tmp}/ywc-issue69-snapshot/tools/claude-code/skills/ywc-plan/SKILL.md` Step 5, Step 4c, Arguments, Rationalization Defense
  - [ ] Read local `ywc-plan/SKILL.md:232-250` (Step 4c), `:335-345` (Step 5), `:381`, `:397`, and `ywc-agentic/SKILL.md:93-104`
- [ ] **Rewrite Step 5 and Arguments**
  - [ ] Replace the y/n question with an unconditional `/ywc-spec-ready --spec <path>` call for Medium/Large specs
  - [ ] Add `--no-converge` to the Arguments table; state that `--non-interactive` and `--no-converge` both skip the auto-run
  - [ ] State that a non-DONE Completion Report from the auto-run is surfaced verbatim, spec left drafted, no retry
- [ ] **Add Re-plan Mode step 7 (FR6)**
  - [ ] In Step 4c append step 7: print `✅ Spec amended: <path> (Iteration N)` and stop; add the 'Step 5 is never reached in Re-plan Mode' sentence at the top of Step 5
- [ ] **Remove duplicate claims**
  - [ ] Update Rationalization Defense (2 rows), Validation checklist (`:381`) and Integration (`:397`) to the new behavior; grep the file for 'ask', 'y/n', 'responds' to catch leftovers
- [ ] **Update the four Tier 1 READMEs**
  - [ ] In README.md (ko), README.en.md, README.ja.md, README.ko.md of `ywc-plan` change the option table and the `ywc-spec-ready` line (`:59`) from 'opt-in' to automatic with `--no-converge`
- [ ] **Add the auth-implement sentence**
  - [ ] In `ywc-auth-implement/SKILL.md` Step 3 add: pass the policy interview to `/ywc-plan --no-converge` (snapshot wording); do not touch other lines

## Acceptance Coverage
Covers: AC1, AC2, AC2b, AC2c (FR6, FR7)

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'ywc-spec-ready --spec' claude-code/skills/ywc-plan/SKILL.md`
- [ ] `[ "$(grep -c -- 'responds \*\*y\*\*' claude-code/skills/ywc-plan/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `[ "$(grep -c 'no-converge' claude-code/skills/ywc-plan/SKILL.md | tr -d ' ')" -ge 3 ]`
- [ ] `grep -q 'Spec amended' claude-code/skills/ywc-plan/SKILL.md`
- [ ] `[ "$(grep -c 'ywc-plan --no-converge' claude-code/skills/ywc-auth-implement/SKILL.md | tr -d ' ')" -ge 1 ]`
- [ ] `for f in README.md README.en.md README.ja.md README.ko.md; do [ "$(grep -c 'opt-in' claude-code/skills/ywc-plan/$f | tr -d ' ')" = 0 ] || exit 1; done`
- [ ] `[ "$(grep -c 'ywc-plan --non-interactive' claude-code/skills/ywc-agentic/SKILL.md | tr -d ' ')" = 1 ] && git diff --quiet -- claude-code/skills/ywc-agentic`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-auth-implement/SKILL.md`
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
