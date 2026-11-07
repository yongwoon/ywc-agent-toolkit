# yk-000010-010-domain-scan-secrets-hunk-filter

## Purpose
`scan-secrets.sh` drops every added line whose content starts with `++` (the diff line then starts with `+++`), because `grep '^+' | grep -v '^+++'` cannot tell a file header from content. A secret on such a line is reported clean.

## Scope
- Tests first in both `test-scan-secrets.sh` copies (keep them byte-identical): a staged file and a committed file whose added line is `++key=AKIA…` (assemble the key at runtime, as the existing cases do) → exit 1. Confirm both are RED against the current script.
- Replace the `ADDED_LINES` filter (`claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` ~line 136, same line in the Codex copy) with a hunk-aware filter: treat `+++ ` / `--- ` as headers only before the first `@@` of each file section (after a `diff --git` line), and take every `+` line inside a hunk as added content. `awk` is enough; no new dependency.
- Keep the existing 27 cases green; confirm by mutation that reverting to `grep -v '^+++'` turns the new cases red.
- Apply the same change to `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`; let the pre-commit hook regenerate `plugins/ywc-agent-toolkit` (never hand-edit it).

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
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)

## Parallel Execution Metadata

- Model Hint: opus — M1 (Criticality: critical)

### Ownership
- `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/**` (generated)
- `plugins/ywc-agent-toolkit/README.md` (generated)

### Owned Interface
- `scan-secrets.sh` exit contract (0 clean / 1 secret / 2 nothing scanned)

### Shared Surfaces
- (None)

### Conflicts With
- (None)

### Parallelizable After
- (None)

### Task Verify
- `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `bash codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `cmp claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- `cmp codex/skills/ywc-create-pr/scripts/scan-secrets.sh plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/scan-secrets.sh`
- `[ "$(grep -c "grep -v '^+++'" claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh | tr -d ' ')" = 0 ]`
- `bash scripts/validate.sh`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last

## Out of Scope
Anything not listed in Scope. Codex files only where Ownership names them.
