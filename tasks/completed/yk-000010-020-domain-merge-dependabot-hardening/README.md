# yk-000010-020-domain-merge-dependabot-hardening

## Purpose
Close the yk-000005-040 re-review Medium/Lows and the yk-000009-010 Low in `ywc-merge-dependabot`: remote-controlled values and `gh pr checks --required` edge cases. All are fail-safe today, but one mislabels or blocks valid merges.

## Scope
- C2 form: `scripts/check-base-required-checks.sh` (:11 comment, :36) and `SKILL.md` (:79) use `git check-ref-format --branch`; switch to `git check-ref-format "refs/heads/$base"` (the `ywc-worktrees --existing-branch` rule). Keep the allowlist order unchanged.
- `scripts/wait-dependabot-rebase.sh`: accept `OLD_HEAD` and `NEW_HEAD` only when they match `^[0-9a-f]{40}$`. A non-matching `OLD_HEAD` (empty, `null`) exits as "head unreadable" (never "rebased"); a non-matching `NEW_HEAD` keeps polling and ends `REBASED=0`. Tests first in `scripts/test_merge_dependabot_scripts.py` (stubbed `gh` returning `null` and a 39-char value) — RED before the fix.
- `gh pr checks --required` on a base with no required checks: confirm gh's behaviour from the installed gh (`gh pr checks --help`) or gh's source/changelog (do not guess). If it exits non-zero with a "no required checks" message, give that case its own result in SKILL.md (e.g. fall back to `gh pr checks` without `--required` and report `no required checks`) instead of `Failed (CI not passing)`. Record the evidence in Implementation Notes.
- The conflict/rebase path CI wait must also use `--required` (same gate as the main path).
- Prose: `SKILL.md` ~:57, ~:77 and `README*.md` ~:96 show `--auto` without `--match-head-commit`; make them match the pinned form. ~:241 attributes every refused queue call to a moved head; say it may also be another refusal reason.
- Re-locate every line number above first; they come from an earlier review and may have shifted.

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
- `claude-code/skills/ywc-merge-dependabot/**`

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-merge-dependabot/**`

### Owned Interface
- `wait-dependabot-rebase.sh` last-line contract `REBASED=<0|1> ATTEMPTS=<n> NEW_HEAD=<sha>`

### Shared Surfaces
- C2 branch-name rule (`ywc-worktrees`)
- `claude-code/skills/CLAUDE.md` scripts table (read only; edit only if the exit contract changes — then stop and report)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- `[ "$(grep -rc 'check-ref-format --branch' claude-code/skills/ywc-merge-dependabot | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- `grep -q '\[0-9a-f\]{40}' claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
