# yk-000006-020-domain-worktrees-existing-branch — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000006-010-domain-agent-description-alignment` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-worktrees/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Add the flag to Arguments and Modes**
  - [ ] Document `--existing-branch`, the `--base-branch` conditional requirement and the mutual exclusion with exit 1
- [ ] **Specify checkout behavior**
  - [ ] Local branch → checkout; origin-only → create tracking branch; never `-b` in this path
- [ ] **Add validation and error handling**
  - [ ] Insert the four-part branch check before `ls-remote`/`fetch`/`worktree add`; add the `invalid branch name` error row
- [ ] **Update READMEs**
  - [ ] Document the flag in README.md (ko), README.en.md, README.ja.md, README.ko.md of `ywc-worktrees`

## Acceptance Coverage
Covers: AC16

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -c -- '--existing-branch' claude-code/skills/ywc-worktrees/SKILL.md | tr -d ' ')" -ge 3 ]`
- [ ] `grep -q 'check-ref-format' claude-code/skills/ywc-worktrees/SKILL.md`
- [ ] `grep -q 'invalid branch name' claude-code/skills/ywc-worktrees/SKILL.md`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-worktrees/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
