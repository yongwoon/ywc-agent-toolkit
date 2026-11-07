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
- `gh pr checks --required`, no required checks — evidence (rung 4): installed `gh version 2.102.0 (2026-09-30)`; `gh pr checks --help` lists only `8: Checks pending` as an extra exit code. On this repo (`main` unprotected: `branches/main/protection/required_status_checks` → 404, `rules/branches/main` → `[]`), `gh pr checks 213 --required` printed `no required checks reported on the 'feature/improvement-20261105' branch` and exited 1. The message names the PR's **head** branch, not the base. The gh binary also carries `no checks reported on the '%s' branch` (no checks at all). Exit 1 is shared with real check failures, so SKILL.md tells the cases apart by that message. Fallback: `gh pr checks` without `--required`, result tagged `no required checks`; `Skipped (no CI checks)` when that run also reports no checks.
- Test stub: `oldsha`/`newsha` were not 40-hex values, so the new hex guard would have rejected them. Switched them to `a*40`/`b*40` first (32/32 green on unfixed code), then added `null` / 39-char cases — RED 4/4 subtests on unfixed code, GREEN 34/34 after the fix.
- Exit contract of `wait-dependabot-rebase.sh` unchanged (non-hex OLD_HEAD uses the existing exit-1 "head unreadable" path), so `claude-code/skills/CLAUDE.md` needs no edit.
- Review round 1: `no required checks reported` also appears when required checks have not registered yet (e.g. right after a rebase), so the 3a gate resolves it with `check-base-required-checks.sh`: exit 0 → pending, exit 1 with a non-empty `BASE=` → fall back to all checks, anything else → `Skipped (no required check confirmed)`. The gate is now an executable block (0 / 8 / other branching). `SequentialCiGateTest` pulls it out of SKILL.md and runs it against the stubbed gh. 8 snippet mutations were each caught. The conflict-path `--watch` wait spells out both commands (`--watch` never exits 8). Step 3 refusal wording now matches Stage 1.
- The script's exit 1 covers both "zero required checks" and a failed `gh api` lookup (e.g. 403 or rate limit), and both lead to the all-checks fallback. Server-side branch protection still refuses a merge that lacks required checks.
- `HEAD` is rejected explicitly in `check-base-required-checks.sh` (`refs/heads/HEAD` passes `check-ref-format`). `@` was already rejected by the allowlist, so it has a test case but no code change (the `HEAD` subtest was RED first).
