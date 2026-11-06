# yk-000010-040-domain-finish-branch-guard-review — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Run a focused security review of `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 Remote deletion guard (~line 215) and every block that deletes a branch or relies on the "merged" judgement (Steps 5 and 8). Lenses: open-PR check failure modes, `gh pr list` result parsing, `headRefOid` vs `ls-remote` tip comparison, fork PRs (same head name, different owner), and multiple PRs for one head.
- [ ] yk-000009-010 already moved the guard to the C2 `refs/heads/` form and quoted `BASE`/`BRANCH`; do not redo those. List each remaining Medium+ finding in Implementation Notes with file:line, then fix it in place.
- [ ] If none of the four can be reproduced, record that as a Ruling with the review evidence; do not invent changes.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'Remote deletion guard' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -qF 'git check-ref-format "refs/heads/$branch"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-finish-branch/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
