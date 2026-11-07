# yk-000004-040-domain-create-pr-features-api — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-create-pr/SKILL.md`
  - `claude-code/skills/ywc-create-pr/references/pr-body-features-api.md`
  - `claude-code/skills/ywc-create-pr/README*.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Create the reference from the snapshot**
  - [ ] Copy only the feature-list and API-table content; keep it English; check no dangling `ywc-*` names (FR3)
  - [ ] Rewrite the Placement rule's 'Review Guide last' to 'after Design Background'
- [ ] **Wire it into SKILL.md**
  - [ ] Replace `:257` with the feature-list instruction and an 'Action required: Read references/pr-body-features-api.md' line
  - [ ] Confirm the Design Background section (`:266-314`) ordering still reads correctly
- [ ] **Update READMEs**
  - [ ] Add one sentence to README.md (ko), README.en.md, README.ja.md, README.ko.md of `ywc-create-pr`

## Acceptance Coverage
Covers: AC6

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `test -f claude-code/skills/ywc-create-pr/references/pr-body-features-api.md`
- [ ] `grep -q 'pr-body-features-api' claude-code/skills/ywc-create-pr/SKILL.md`
- [ ] `[ "$(grep -c -- '\[List of specific changes made\]' claude-code/skills/ywc-create-pr/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md`
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
