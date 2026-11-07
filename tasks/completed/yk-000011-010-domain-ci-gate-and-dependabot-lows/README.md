# yk-000011-010-domain-ci-gate-and-dependabot-lows

## Purpose
Close the yk-000010 deferred findings: the trigger-coverage pin in `test_score.py` is never run by `validate.sh`/CI, and three `ywc-merge-dependabot` Lows (a failed base lookup reaches the all-checks fallback, a deny-list mergeable check, a stale `--branch` row in the scripts table).

## Scope
- `scripts/validate.sh`: run `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` (it is currently only checked for existence, ~:662/:690) inside `run_script_test_suites`, with the same error-reporting pattern as the other suites (tail of output on failure). Confirm it fails when a new item drops below the coverage minimum: in a scratch copy of the fixture (`mktemp -d`), remove one exempt reviewer's collision cases and show the suite failing.
- `scripts/validate.sh`: declare `dependabot_out` `local` (review-050 Low).
- `claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`: distinguish "lookup failed" (gh api error, rate limit, 403, unparseable output) from "base has zero required checks". Add exit 3 = unresolved (nothing confirmed, nothing denied), keep 0/1/2 meanings. Tests first in `test_merge_dependabot_scripts.py` with a stubbed `gh api` failure — RED before.
- `claude-code/skills/ywc-merge-dependabot/SKILL.md` (3a gate ~:184 and conflict path ~:226, plus Mode Selection ~:82): exit 3 → `Skipped (required checks unconfirmed)`, never the all-checks fallback and never `--auto`. Update the extracted-block tests (`SequentialCiGateTest`) to cover exit 3.
- `claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh` (~:50): accept only `MERGEABLE` = `MERGEABLE` (allowlist) instead of rejecting `CONFLICTING`/`UNKNOWN`; test first with a stubbed unexpected value.
- `claude-code/skills/CLAUDE.md` scripts table, `check-base-required-checks.sh` row (~:366): replace `check-ref-format --branch` with the `refs/heads/` form and the `HEAD` rejection, and add exit 3. Edit only that row.
- Re-locate every line number first; they come from the yk-000010 reviews.

## Spec Reference

### Primary Sources
- Deferred findings in the yk-000010 Completion Report on `feature/improvement-20261106` (rulings ledger: yk-000010-020, yk-000010-060; review-050 Low).
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; the `ywc-mine-review-history` coverage gap (needs a real user prompt); the scan-secrets `--cc ' +x'` and untracked-content gaps; a frontmatter `dispatch-only` key (left to the next plan).

## Criticality
critical — secret detection, remote-controlled values reaching shell/gh, or remote branch deletion.

## Dependencies

### Depends On
- (None)

### Depended By
- (None)

## Key Files
- `scripts/validate.sh`
- `claude-code/skills/ywc-merge-dependabot/**`
- `claude-code/skills/CLAUDE.md` (check-base-required-checks.sh row only)
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `scripts/validate.sh`
- `claude-code/skills/ywc-merge-dependabot/**`
- `claude-code/skills/CLAUDE.md` (check-base-required-checks.sh row only)
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`

### Owned Interface
- `check-base-required-checks.sh` exit contract (0 confirmed / 1 zero required checks or invalid base / 2 usage / 3 unresolved)

### Shared Surfaces
- `.claude/skills/ywc-toolkit-eval/scripts/test_score.py` (run only; do not edit)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- `grep -q 'test_score.py' scripts/validate.sh && grep -q 'python3 .*test_score.py' scripts/validate.sh`
- `grep -q 'local dependabot_out' scripts/validate.sh`
- `grep -q 'exit 3' claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`
- `[ "$(grep -c 'check-ref-format --branch' claude-code/skills/CLAUDE.md | tr -d ' ')" = 0 ]`
- `bash -n scripts/validate.sh && shellcheck scripts/validate.sh claude-code/skills/ywc-merge-dependabot/scripts/*.sh`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit if it changed
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
