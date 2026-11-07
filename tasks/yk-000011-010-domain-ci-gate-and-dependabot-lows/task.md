# yk-000011-010-domain-ci-gate-and-dependabot-lows — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `scripts/validate.sh`
  - `claude-code/skills/ywc-merge-dependabot/**`
  - `claude-code/skills/CLAUDE.md` (check-base-required-checks.sh row only)
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `scripts/validate.sh`: run `python3 .claude/skills/ywc-toolkit-eval/scripts/test_score.py` (it is currently only checked for existence, ~:662/:690) inside `run_script_test_suites`, with the same error-reporting pattern as the other suites (tail of output on failure). Confirm it fails when a new item drops below the coverage minimum: in a scratch copy of the fixture (`mktemp -d`), remove one exempt reviewer's collision cases and show the suite failing.
- [ ] `scripts/validate.sh`: declare `dependabot_out` `local` (review-050 Low).
- [ ] `claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`: distinguish "lookup failed" (gh api error, rate limit, 403, unparseable output) from "base has zero required checks". Add exit 3 = unresolved (nothing confirmed, nothing denied), keep 0/1/2 meanings. Tests first in `test_merge_dependabot_scripts.py` with a stubbed `gh api` failure — RED before.
- [ ] `claude-code/skills/ywc-merge-dependabot/SKILL.md` (3a gate ~:184 and conflict path ~:226, plus Mode Selection ~:82): exit 3 → `Skipped (required checks unconfirmed)`, never the all-checks fallback and never `--auto`. Update the extracted-block tests (`SequentialCiGateTest`) to cover exit 3.
- [ ] `claude-code/skills/ywc-merge-dependabot/scripts/wait-dependabot-rebase.sh` (~:50): accept only `MERGEABLE` = `MERGEABLE` (allowlist) instead of rejecting `CONFLICTING`/`UNKNOWN`; test first with a stubbed unexpected value.
- [ ] `claude-code/skills/CLAUDE.md` scripts table, `check-base-required-checks.sh` row (~:366): replace `check-ref-format --branch` with the `refs/heads/` form and the `HEAD` rejection, and add exit 3. Edit only that row.
- [ ] Re-locate every line number first; they come from the yk-000010 reviews.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 claude-code/skills/ywc-merge-dependabot/scripts/test_merge_dependabot_scripts.py`
- [ ] `grep -q 'test_score.py' scripts/validate.sh && grep -q 'python3 .*test_score.py' scripts/validate.sh`
- [ ] `grep -q 'local dependabot_out' scripts/validate.sh`
- [ ] `grep -q 'exit 3' claude-code/skills/ywc-merge-dependabot/scripts/check-base-required-checks.sh`
- [ ] `[ "$(grep -c 'check-ref-format --branch' claude-code/skills/CLAUDE.md | tr -d ' ')" = 0 ]`
- [ ] `bash -n scripts/validate.sh && shellcheck scripts/validate.sh claude-code/skills/ywc-merge-dependabot/scripts/*.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit if it changed
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-merge-dependabot/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
