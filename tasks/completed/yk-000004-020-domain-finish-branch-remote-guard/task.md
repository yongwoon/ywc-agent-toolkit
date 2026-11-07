# yk-000004-020-domain-finish-branch-remote-guard — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Locate the local deletion points**
  - [ ] Grep `ywc-finish-branch/SKILL.md` for `--delete-branch`, `push origin --delete`, `branch -d`; note Step 5 anchors
  - [ ] Read the snapshot `:369` paragraph and `:28` row
- [ ] **Insert the guard paragraph before any deletion**
  - [ ] Place 'Remote deletion guard' so the open-PR check is the first thing a reader meets in Step 5
  - [ ] Carry over the full rule set: allowed command, open-PR check with parse-empty requirement, failure statuses, `check-ref-format`, quoted variable
- [ ] **Add the strict 'merged' determination**
  - [ ] Include the `--state merged` query with `baseRefName` and `headRefOid` vs `git ls-remote` comparison and the ban on `git branch -r --merged HEAD`
- [ ] **Add Rationalization Defense row 1**
  - [ ] Insert the snapshot row at `:28`; keep the table format; do not add a stacked-PR `--base` check

## Acceptance Coverage
Covers: AC4

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -c 'gh pr list --head' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" -ge 2 ]`
- [ ] `[ "$(grep -c -- 'Remote deletion guard' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 1 ]`
- [ ] `grep -q 'check-ref-format' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -q 'headRefOid' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `python3 -c "t=open('claude-code/skills/ywc-finish-branch/SKILL.md',encoding='utf-8').read(); g=t.index('Remote deletion guard'); d=t.find('git push origin --delete'); assert d==-1 or g<d"` (guard text precedes any explicit deletion command)
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`
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
