# yk-000010-040-domain-finish-branch-guard-review

## Purpose
yk-000004-020 ported the upstream Remote deletion guard verbatim; its review left four Mediums "inherited from the upstream text" that were never itemized in the run record. Re-derive them on the current text and fix what is still open.

## Scope
- Run a focused security review of `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 Remote deletion guard (~line 215) and every block that deletes a branch or relies on the "merged" judgement (Steps 5 and 8). Lenses: open-PR check failure modes, `gh pr list` result parsing, `headRefOid` vs `ls-remote` tip comparison, fork PRs (same head name, different owner), and multiple PRs for one head.
- yk-000009-010 already moved the guard to the C2 `refs/heads/` form and quoted `BASE`/`BRANCH`; do not redo those. List each remaining Medium+ finding in Implementation Notes with file:line, then fix it in place.
- If none of the four can be reproduced, record that as a Ruling with the review evidence; do not invent changes.

## Spec Reference

### Primary Sources
- Deferred findings in the Completion Reports of yk-000004..yk-000009 runs on `feature/improvement-20261106` (rulings ledger: yk-000004-020, yk-000005-040, yk-000005-050, yk-000006-010, yk-000009-010).
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000010 tasks' items.

## Criticality
critical — secret detection, remote-controlled values reaching shell/gh, or remote branch deletion.

## Dependencies

### Depends On
- (None)

### Depended By
- `yk-000010-060-test-reviewer-trigger-coverage`

## Key Files
- `claude-code/skills/ywc-finish-branch/SKILL.md`

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-finish-branch/SKILL.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- C2 branch-name rule (`ywc-worktrees`)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `grep -q 'Remote deletion guard' claude-code/skills/ywc-finish-branch/SKILL.md`
- `grep -qF 'git check-ref-format "refs/heads/$branch"' claude-code/skills/ywc-finish-branch/SKILL.md`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
