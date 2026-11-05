# yk-000005-030-refactor-skill-script-paths — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `yk-000005-020-domain-user-invoked-skills` is completed (merged)
- [ ] Working tree is clean and on a `feature/<task-name>` branch
- [ ] Read the full spec sections cited in README `Spec Reference`

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-create-pr/SKILL.md`
  - `claude-code/skills/ywc-docker-isolate/SKILL.md`
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
  - `claude-code/skills/ywc-handle-pr-reviews/SKILL.md`
  - `claude-code/skills/ywc-mine-review-history/SKILL.md`
  - `claude-code/skills/ywc-parallel-executor/**`
  - `claude-code/skills/ywc-release-pr-list/SKILL.md`
  - `claude-code/skills/ywc-sequential-executor/**`
  - `claude-code/skills/ywc-skill-author/SKILL.md`
  - `claude-code/skills/ywc-spec-writer/SKILL.md`
  - `claude-code/skills/ywc-task-generator/**`
  - `claude-code/skills/ywc-verify-done/**`
  - `claude-code/skills/CLAUDE.md` (pair table only)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if a shared contract or schema must change beyond the declared Scope
- [ ] Stop if another in-flight task already owns the surface this task now needs to edit
- [ ] Stop (report `BLOCKED`) if a required snapshot file is `BLOCKED` in the MANIFEST — never reconstruct upstream text from memory
- [ ] Stop if a snapshot hunk names a skill/feature that does not exist locally and the intent cannot be mapped (FR3); drop the sentence and note it instead of inventing a target

## Implementation Steps
- [ ] **Enumerate with the AC10 grep**
  - [ ] Save the hit list; it must match the 39 / 15 and 6 / 2 counts in Scope (report drift)
- [ ] **Substitute SKILL.md call sites**
  - [ ] Apply `"${CLAUDE_SKILL_DIR}/scripts/x"` / `"${CLAUDE_SKILL_DIR}/../ywc-x/scripts/y"` to each SKILL.md hit; preserve quoting and surrounding text
- [ ] **Substitute references and templates**
  - [ ] Apply `"<skill-base-dir>/…"` with its one-sentence definition on first use in each file; fix the six `<path-to-skill>` hits
- [ ] **Verify targets exist and the table is current**
  - [ ] Run the AC11 existence one-liner
  - [ ] Re-run the cross-skill grep and update the B1 pair table if it changed

## Acceptance Coverage
Covers: AC10, AC11

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -rnE '(tools/)?claude-code/skills/ywc-[a-z-]+/scripts/' --include='*.md' --include='*.template' claude-code/skills | grep -v 'claude-code/skills/CLAUDE.md' | wc -l | tr -d ' ')" = 0 ]`
- [ ] `[ "$(grep -rn '<path-to-skill>' claude-code/skills | wc -l | tr -d ' ')" = 0 ]`
- [ ] AC11 existence check: for each substituted `${CLAUDE_SKILL_DIR}` / `<skill-base-dir>` path, replace the placeholder with the skill directory and `test -f` it (one-liner recorded in Implementation Notes)
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-finish-branch/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-spec-writer/SKILL.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-verify-done/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A (no typecheck in this repository)
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] markdownlint passes for every changed `README*.md` (same config as `.github/workflows/markdownlint.yml`)
- [ ] build: N/A (documentation/prompt repository)

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
