# yk-000010-050-docs-metadata-followups

## Purpose
Three small metadata/tooling leftovers: the `ywc-impl-review` description is over the A15 80-word advisory cap, the Codex `ywc-skill-author` audit command uses a repo-relative script path, and `validate.sh` runs every security suite inside a function named `check_cc_support_dirs`.

## Scope
- `claude-code/skills/ywc-impl-review/SKILL.md` description: currently ~94 words; bring it to ≤80 words. Keep every trigger phrase and every `Do not use for` target that `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` relies on (grep the fixture for `ywc-impl-review` first); shorten prose, not routing terms.
- `codex/skills/ywc-skill-author/references/audit-workflow.md` (~line 12): `bash scripts/audit-skills.sh` → `bash "<skill-base-dir>/scripts/audit-skills.sh"` with the same defining sentence the Claude Code copy got in yk-000008-030. Confirm the Codex skill ships `scripts/audit-skills.sh`; if not, stop and report.
- `scripts/validate.sh`: move the test-suite runs (poll-pr-reviews, scan-secrets, merge-dependabot, security suites) out of `check_cc_support_dirs` into a new `run_script_test_suites` function called right after it. Behaviour and messages unchanged.
- Let the pre-commit hook regenerate `plugins/ywc-agent-toolkit` for the Codex change.

## Spec Reference

### Primary Sources
- Deferred findings in the Completion Reports of yk-000004..yk-000009 runs on `feature/improvement-20261106` (rulings ledger: yk-000004-020, yk-000005-040, yk-000005-050, yk-000006-010, yk-000009-010).
- `docs/review-learnings.md` (repository review rules)

### Summary
Follow-up items deferred by earlier runs on `feature/improvement-20261106`. Each Scope bullet names the file and the expected end state.

### Out of Scope (from findings)
- Anything not in Scope; other Phase 000010 tasks' items.

## Criticality
normal

## Dependencies

### Depends On
- (None)

### Depended By
- `yk-000010-060-test-reviewer-trigger-coverage`

## Key Files
- `claude-code/skills/ywc-impl-review/SKILL.md`
- `codex/skills/ywc-skill-author/references/audit-workflow.md`
- `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)
- `scripts/validate.sh`

## Parallel Execution Metadata

- Model Hint: sonnet

### Ownership
- `claude-code/skills/ywc-impl-review/SKILL.md`
- `codex/skills/ywc-skill-author/references/audit-workflow.md`
- `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)
- `scripts/validate.sh`

### Owned Interface
- (None — no public interface owned)

### Shared Surfaces
- `trigger-cases.json` (read only here; yk-000010-060 edits it)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `python3 -c "import re;t=open('claude-code/skills/ywc-impl-review/SKILL.md',encoding='utf-8').read().split('---')[1];d=re.search(r'description:(.*)',t,re.S).group(1);n=len(d.split());assert n<=80,n"`
- `[ "$(grep -c 'bash scripts/audit-skills.sh' codex/skills/ywc-skill-author/references/audit-workflow.md | tr -d ' ')" = 0 ]`
- `grep -q '^run_script_test_suites()' scripts/validate.sh`
- `bash -n scripts/validate.sh && shellcheck scripts/validate.sh`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last
- `python3 -c "import sys; bad=[p for p in sys.argv[1:] if open(p,encoding='utf-8').read().split('---',2)[2].count(chr(10))+1>500]; assert not bad, bad" claude-code/skills/ywc-impl-review/SKILL.md`

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
