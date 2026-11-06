# yk-000008-010-domain-security-doc-followups

## Purpose
Close the documentation and quoting gaps left after yk-000007-010 made `scan-secrets.sh --committed` fail closed and allowlisted remote-controlled branch names.

## Scope
- `claude-code/skills/ywc-create-pr/SKILL.md` Step 3 (~line 112): the exit 2 meaning must also cover "`--committed` base is invalid or does not resolve to a local commit", and say a base that exists only as `origin/<base>` needs a local ref (or pass `origin/<base>`).
- `claude-code/skills/CLAUDE.md` Bundled Execution Scripts table, `scan-secrets.sh` row (~line 351): same exit 2 wording.
- `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 `--mode local-merge` block (~lines 223-228): hold `<base-branch>` and `feature/<task-name>` in variables validated by the Step 5 Remote deletion guard rule and quote every use (`git pull origin "$BASE"`, `git merge --no-ff "$BRANCH"`, `git push origin "$BASE"`, `git branch -d "$BRANCH"`).
- `claude-code/skills/references/pr-conflict-resolution.md` Update Branch From Base snippet: quote `feature/<task-name>` the same way (it is local, but keep one quoting style).

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
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/CLAUDE.md` (scan-secrets row only)
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/references/pr-conflict-resolution.md`

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/CLAUDE.md` (scan-secrets row only)
- `claude-code/skills/ywc-finish-branch/SKILL.md`
- `claude-code/skills/references/pr-conflict-resolution.md`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- claude-code/skills/CLAUDE.md (also read by other tasks; this task edits only the scan-secrets row)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `grep -q 'does not resolve' claude-code/skills/ywc-create-pr/SKILL.md`
- `grep -n 'scan-secrets.sh' claude-code/skills/CLAUDE.md | grep -q 'resolv'`
- `grep -qF 'git push origin "$BASE"' claude-code/skills/ywc-finish-branch/SKILL.md`
- `[ "$(grep -c 'git push origin <base-branch>' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-finish-branch/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
