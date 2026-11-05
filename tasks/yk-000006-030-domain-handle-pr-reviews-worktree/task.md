# yk-000006-030-domain-handle-pr-reviews-worktree — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000006-020-domain-worktrees-existing-branch` is completed (merged)
- [ ] `${TMPDIR:-/tmp}/ywc-issue69-snapshot/MANIFEST.md` exists and lists every upstream path this task consumes (if the snapshot directory was cleaned, re-run `yk-000003-010-config-upstream-snapshot` first)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-handle-pr-reviews/**`
  - `claude-code/skills/ywc-skill-author/references/cross-skill-graph.md`
  - `claude-code/skills/CLAUDE.md` (pair table row)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Add Arguments and Step 1.5**
  - [ ] Create the `## Arguments` section with `--worktree`
  - [ ] Write the PR-number regex check, head-branch validation (C2 rules), fork-PR and non-OPEN `BLOCKED` rules
- [ ] **Specify worktree handling**
  - [ ] Define in-place / created / reuse outcomes, clean-tree requirement, remote refresh and cwd re-check
  - [ ] Delegate creation to `ywc-worktrees --mode create --existing-branch --task-name pr-<N>`; `BLOCKED` when the skill is absent
- [ ] **Fix Step 9 and add defenses**
  - [ ] Require `--keep-branch` in the prune advice
  - [ ] Add the two Rationalization Defense rows
- [ ] **Update references and READMEs**
  - [ ] Add the handle-pr-reviews→worktrees edge to `cross-skill-graph.md` and the `claude-code/skills/CLAUDE.md` pair table
  - [ ] Update README.md (ko), README.en.md, README.ja.md, README.ko.md of `ywc-handle-pr-reviews`
- [ ] **Final full gate (AC17)**
  - [ ] Run `bash scripts/validate.sh` and `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`; stage the baseline

## Acceptance Coverage
Covers: AC16b, AC17

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'Step 1.5' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- [ ] `grep -q 'isCrossRepository' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- [ ] `grep -qF '^[0-9]+$' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- [ ] `grep -q -- '--keep-branch' claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
- [ ] `[ "$(grep -c 'git worktree add' claude-code/skills/ywc-handle-pr-reviews/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-handle-pr-reviews/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
