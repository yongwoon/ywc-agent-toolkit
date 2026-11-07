# yk-000010-050-docs-metadata-followups — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-impl-review/SKILL.md`
  - `codex/skills/ywc-skill-author/references/audit-workflow.md`
  - `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` (generated)
  - `plugins/ywc-agent-toolkit/README.md` (generated)
  - `scripts/validate.sh`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `claude-code/skills/ywc-impl-review/SKILL.md` description: currently ~94 words; bring it to ≤80 words. Keep every trigger phrase and every `Do not use for` target that `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` relies on (grep the fixture for `ywc-impl-review` first); shorten prose, not routing terms.
- [ ] `codex/skills/ywc-skill-author/references/audit-workflow.md` (~line 12): `bash scripts/audit-skills.sh` → `bash "<skill-base-dir>/scripts/audit-skills.sh"` with the same defining sentence the Claude Code copy got in yk-000008-030. Confirm the Codex skill ships `scripts/audit-skills.sh`; if not, stop and report.
- [ ] `scripts/validate.sh`: move the test-suite runs (poll-pr-reviews, scan-secrets, merge-dependabot, security suites) out of `check_cc_support_dirs` into a new `run_script_test_suites` function called right after it. Behaviour and messages unchanged.
- [ ] Let the pre-commit hook regenerate `plugins/ywc-agent-toolkit` for the Codex change.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `python3 -c "import re;t=open('claude-code/skills/ywc-impl-review/SKILL.md',encoding='utf-8').read().split('---')[1];d=re.search(r'description:(.*)',t,re.S).group(1);n=len(d.split());assert n<=80,n"`
- [ ] `[ "$(grep -c 'bash scripts/audit-skills.sh' codex/skills/ywc-skill-author/references/audit-workflow.md | tr -d ' ')" = 0 ]`
- [ ] `grep -q '^run_script_test_suites()' scripts/validate.sh`
- [ ] `bash -n scripts/validate.sh && shellcheck scripts/validate.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- [ ] `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-impl-review/SKILL.md`

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
