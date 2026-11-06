# yk-000010-020-domain-merge-dependabot-hardening — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-merge-dependabot/**`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] C2 form: `scripts/check-base-required-checks.sh` (:11 comment, :36) and `SKILL.md` (:79) use `git check-ref-format --branch`; switch to `git check-ref-format "refs/heads/$base"` (the `ywc-worktrees --existing-branch` rule). Keep the allowlist order unchanged.
- [ ] `scripts/wait-dependabot-rebase.sh`: accept `OLD_HEAD` and `NEW_HEAD` only when they match `^[0-9a-f]{40}$`. A non-matching `OLD_HEAD` (empty, `null`) exits as "head unreadable" (never "rebased"); a non-matching `NEW_HEAD` keeps polling and ends `REBASED=0`. Tests first in `scripts/test_merge_dependabot_scripts.py` (stubbed `gh` returning `null` and a 39-char value) — RED before the fix.
- [ ] `gh pr checks --required` on a base with no required checks: confirm gh's behaviour from the installed gh (`gh pr checks --help`) or gh's source/changelog (do not guess). If it exits non-zero with a "no required checks" message, give that case its own result in SKILL.md (e.g. fall back to `gh pr checks` without `--required` and report `no required checks`) instead of `Failed (CI not passing)`. Record the evidence in Implementation Notes.
- [ ] The conflict/rebase path CI wait must also use `--required` (same gate as the main path).
- [ ] Prose: `SKILL.md` ~:57, ~:77 and `README*.md` ~:96 show `--auto` without `--match-head-commit`; make them match the pinned form. ~:241 attributes every refused queue call to a moved head; say it may also be another refusal reason.
- [ ] Re-locate every line number above first; they come from an earlier review and may have shifted.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- [ ] `[ "$(grep -rc 'check-ref-format --branch' claude-code/skills/ywc-merge-dependabot | awk -F: '{s+=$2} END{print s}')" = 0 ]`
- [ ] `grep -q '\[0-9a-f\]{40}' claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
