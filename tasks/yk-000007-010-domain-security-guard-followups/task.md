# yk-000007-010-domain-security-guard-followups — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Working tree is clean and on a `feature/<task-name>` branch created from `feature/improvement-20261106` (or its successor)
- [ ] Read `claude-code/skills/ywc-worktrees/SKILL.md` Step 2 (`--existing-branch` bullet) for the C2 branch-name rule

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `scripts/validate.sh`
  - `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
  - `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
  - `claude-code/skills/references/pr-conflict-resolution.md`
  - `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if any of the three security tests fails once wired (fix belongs to its owning skill, not this task)
- [ ] Stop if `scan-secrets.sh` callers depend on exit 0 for an unresolvable base (grep callers in `claude-code/skills/` first)
- [ ] Stop if required changes spill outside Ownership

## Implementation Steps
- [ ] **Wire tests (M1)**
  - [ ] Add three missing/failed blocks to `scripts/validate.sh` next to the scan-secrets block
- [ ] **scan-secrets fail-closed (M2), test first**
  - [ ] Add the four `--committed` cases to `test-scan-secrets.sh` (temp repo); confirm unknown-base case fails RED
  - [ ] Add allowlist + `rev-parse --verify` guard and drop `|| true` on the committed diff; exit 2 on failure
- [ ] **finish-branch guard (M4)**
  - [ ] Prepend the C2 allowlist order to the Step 5 Remote deletion guard sentence
- [ ] **pr-conflict-resolution (M5)**
  - [ ] Add the C2 validation sentence and `BLOCKED: invalid base branch name` before the Update Branch From Base snippet; quote the branch variable
- [ ] **Final gate**
  - [ ] Run `bash scripts/validate.sh` and `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`; stage the baseline

## Acceptance Coverage
Covers: final-review M1, M2, M4, M5; closes the yk-000004-050 deferral (missing exit 0 / exit 1 cases)

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'resolve-pr-head-test.sh' scripts/validate.sh`
- [ ] `grep -q 'test_handoff_safety.py' scripts/validate.sh`
- [ ] `grep -q 'test_retro_safety.py' scripts/validate.sh`
- [ ] `grep -q 'rev-parse --verify' claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- [ ] `grep -q -- '--committed' claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `grep -qF '^[A-Za-z0-9._/-]+$' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF '^[A-Za-z0-9._/-]+$' claude-code/skills/references/pr-conflict-resolution.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] Stage the auto-updated `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` in the same commit
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`, includes shellcheck on `scripts/`)
- [ ] typecheck: N/A
- [ ] unit tests: `test-scan-secrets.sh` plus the three newly wired suites via `scripts/validate.sh`
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
