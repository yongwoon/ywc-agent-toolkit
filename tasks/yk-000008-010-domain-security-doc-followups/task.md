# yk-000008-010-domain-security-doc-followups — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-create-pr/SKILL.md`
  - `claude-code/skills/CLAUDE.md` (scan-secrets row only)
  - `claude-code/skills/ywc-finish-branch/SKILL.md`
  - `claude-code/skills/references/pr-conflict-resolution.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `claude-code/skills/ywc-create-pr/SKILL.md` Step 3 (~line 112): the exit 2 meaning must also cover "`--committed` base is invalid or does not resolve to a local commit", and say a base that exists only as `origin/<base>` needs a local ref (or pass `origin/<base>`).
- [ ] `claude-code/skills/CLAUDE.md` Bundled Execution Scripts table, `scan-secrets.sh` row (~line 351): same exit 2 wording.
- [ ] `claude-code/skills/ywc-finish-branch/SKILL.md` Step 5 `--mode local-merge` block (~lines 223-228): hold `<base-branch>` and `feature/<task-name>` in variables validated by the Step 5 Remote deletion guard rule and quote every use (`git pull origin "$BASE"`, `git merge --no-ff "$BRANCH"`, `git push origin "$BASE"`, `git branch -d "$BRANCH"`).
- [ ] `claude-code/skills/references/pr-conflict-resolution.md` Update Branch From Base snippet: quote `feature/<task-name>` the same way (it is local, but keep one quoting style).
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'does not resolve' claude-code/skills/ywc-create-pr/SKILL.md`
- [ ] `grep -n 'scan-secrets.sh' claude-code/skills/CLAUDE.md | grep -q 'resolv'`
- [ ] `grep -qF 'git push origin "$BASE"' claude-code/skills/ywc-finish-branch/SKILL.md`
- [ ] `[ "$(grep -c 'git push origin <base-branch>' claude-code/skills/ywc-finish-branch/SKILL.md | tr -d ' ')" = 0 ]`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-finish-branch/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
