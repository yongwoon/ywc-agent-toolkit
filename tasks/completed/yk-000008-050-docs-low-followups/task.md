# yk-000008-050-docs-low-followups — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-sequential-executor/references/worktree-run.md`
  - `CLAUDE.md`
  - `claude-code/skills/ywc-worktrees/SKILL.md` (Integration section)
  - `claude-code/skills/ywc-parallel-executor/SKILL.md` (Pre-flight item 5)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `claude-code/skills/ywc-sequential-executor/references/worktree-run.md` (~line 46): `ywc-worktrees/SKILL.md:98` → cite the step by name ("Step 2 item 5") instead of a line number, so it does not drift again.
- [ ] Root `CLAUDE.md` (~line 7): Codex skill count 51 → the actual count (`ls -d codex/skills/ywc-*/ | wc -l`, 54 at `7d4c6976`); re-check the Claude Code skill and both agent counts at the same time.
- [ ] `claude-code/skills/ywc-worktrees/SKILL.md` `## Integration` upstream list: add `ywc-handle-pr-reviews` (`--worktree`: `--mode create --existing-branch`, Step 9 `--mode prune --keep-branch`).
- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md` Pre-flight item 5: add a resolution rule for a worktree whose basename is `pr-<N>`: it belongs to `ywc-handle-pr-reviews`, so never delete it or its branch; stop and ask the user to finish or prune it via `ywc-handle-pr-reviews` (prune with `--keep-branch`) before the run. No change to `audit-worktrees.sh`.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `[ "$(grep -c 'SKILL.md:98' claude-code/skills/ywc-sequential-executor/references/worktree-run.md | tr -d ' ')" = 0 ]`
- [ ] `n=$(ls -d codex/skills/ywc-*/ | wc -l | tr -d ' '); grep -q "Codex\*\* ($n skills" CLAUDE.md`
- [ ] `grep -q 'ywc-handle-pr-reviews' claude-code/skills/ywc-worktrees/SKILL.md`
- [ ] `grep -q 'pr-<N>' claude-code/skills/ywc-parallel-executor/SKILL.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-worktrees/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
