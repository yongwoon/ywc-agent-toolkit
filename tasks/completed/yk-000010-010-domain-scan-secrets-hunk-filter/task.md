# yk-000010-010-domain-scan-secrets-hunk-filter — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh`
  - `claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
  - `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`
  - `codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
  - `plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/**` (generated)
  - `plugins/ywc-agent-toolkit/README.md` (generated)
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] Tests first in both `test-scan-secrets.sh` copies (keep them byte-identical): a staged file and a committed file whose added line is `++key=AKIA…` (assemble the key at runtime, as the existing cases do) → exit 1. Confirm both are RED against the current script.
- [ ] Replace the `ADDED_LINES` filter (`claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` ~line 136, same line in the Codex copy) with a hunk-aware filter: treat `+++ ` / `--- ` as headers only before the first `@@` of each file section (after a `diff --git` line), and take every `+` line inside a hunk as added content. `awk` is enough; no new dependency.
- [ ] Keep the existing 27 cases green; confirm by mutation that reverting to `grep -v '^+++'` turns the new cases red.
- [ ] Apply the same change to `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`; let the pre-commit hook regenerate `plugins/ywc-agent-toolkit` (never hand-edit it).
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `bash claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `bash codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `cmp claude-code/skills/ywc-create-pr/scripts/test-scan-secrets.sh codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `cmp codex/skills/ywc-create-pr/scripts/scan-secrets.sh plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/scan-secrets.sh`
- [ ] `[ "$(grep -c "grep -v '^+++'" claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh | tr -d ' ')" = 0 ]`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000010 Wave 1 tasks do NOT commit the baseline file; yk-000010-060 stages it last

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
