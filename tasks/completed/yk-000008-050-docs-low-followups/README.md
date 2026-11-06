# yk-000008-050-docs-low-followups

## Purpose
Fix the Low findings from the Issue 69 port final review: a stale line reference, a stale skill count, a missing caller entry, and the parallel pre-flight treating a `ywc-handle-pr-reviews` `pr-<N>` worktree as a leaked task worktree.

## Scope
- `claude-code/skills/ywc-sequential-executor/references/worktree-run.md` (~line 46): `ywc-worktrees/SKILL.md:98` → cite the step by name ("Step 2 item 5") instead of a line number, so it does not drift again.
- Root `CLAUDE.md` (~line 7): Codex skill count 51 → the actual count (`ls -d codex/skills/ywc-*/ | wc -l`, 54 at `7d4c6976`); re-check the Claude Code skill and both agent counts at the same time.
- `claude-code/skills/ywc-worktrees/SKILL.md` `## Integration` upstream list: add `ywc-handle-pr-reviews` (`--worktree`: `--mode create --existing-branch`, Step 9 `--mode prune --keep-branch`).
- `claude-code/skills/ywc-parallel-executor/SKILL.md` Pre-flight item 5: add a resolution rule for a worktree whose basename is `pr-<N>`: it belongs to `ywc-handle-pr-reviews`, so never delete it or its branch; stop and ask the user to finish or prune it via `ywc-handle-pr-reviews` (prune with `--keep-branch`) before the run. No change to `audit-worktrees.sh`.

## Spec Reference

### Primary Sources
- Issue 69 port final review (Lows, M3, M6) and the yk-000007-010 review (Lows), recorded in those runs' Completion Reports.
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000008 tasks' items.

## Criticality
normal

## Dependencies

### Depends On
- (None)

### Depended By
- `yk-000008-040-test-trigger-cases-grounding`

## Key Files
- `claude-code/skills/ywc-sequential-executor/references/worktree-run.md`
- `CLAUDE.md`
- `claude-code/skills/ywc-worktrees/SKILL.md` (Integration section)
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (Pre-flight item 5)

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `claude-code/skills/ywc-sequential-executor/references/worktree-run.md`
- `CLAUDE.md`
- `claude-code/skills/ywc-worktrees/SKILL.md` (Integration section)
- `claude-code/skills/ywc-parallel-executor/SKILL.md` (Pre-flight item 5)

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- ywc-worktrees caller list

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `[ "$(grep -c 'SKILL.md:98' claude-code/skills/ywc-sequential-executor/references/worktree-run.md | tr -d ' ')" = 0 ]`
- `n=$(ls -d codex/skills/ywc-*/ | wc -l | tr -d ' '); grep -q "Codex\*\* ($n skills" CLAUDE.md`
- `grep -q 'ywc-handle-pr-reviews' claude-code/skills/ywc-worktrees/SKILL.md`
- `grep -q 'pr-<N>' claude-code/skills/ywc-parallel-executor/SKILL.md`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-worktrees/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
