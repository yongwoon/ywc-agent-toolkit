# yk-000008-020-domain-codex-scan-secrets-guard — Implementation Checklist

## Prerequisites
- [ ] Working tree is clean and on a `feature/<task-name>` branch

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`:
  - `codex/skills/ywc-create-pr/**`
  - `plugins/ywc-agent-toolkit/skills/ywc-create-pr/**` (generated)
  - `scripts/validate.sh`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if required changes spill outside Ownership
- [ ] Stop if a Scope bullet's premise (line, text, count) no longer matches the file; report instead of guessing

## Implementation Steps
- [ ] `codex/skills/ywc-create-pr/scripts/scan-secrets.sh`: apply the same changes as `claude-code/skills/ywc-create-pr/scripts/scan-secrets.sh` (commits c0985a92, c205fa41): `shift $(( $# >= 2 ? 2 : 1 ))`, in-process allowlist, `rev-parse --verify "${BASE}^{commit}"`, checked diff, exit 2. First confirm the Codex script has the same not-a-work-tree guard; port it too if missing.
- [ ] Add `codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh` (copy of the Claude Code test incl. the `git` shim), and wire it into `scripts/validate.sh` next to the Claude Code scan-secrets block.
- [ ] Regenerate `plugins/ywc-agent-toolkit` via the repository pre-commit hook (do not hand-edit the plugin copy); `scripts/validate.sh` fails on a stale plugin package.
- [ ] `codex/skills/ywc-create-pr/SKILL.md`: if it states the exit-code table, add the exit 2 case.
- [ ] Run the Task Verify commands

## Acceptance Coverage
Covers: the Scope bullets above

<!-- Write portable commands: see references/execution-convention.md#task-verify-portability -->
## Task Verify
- [ ] `grep -q 'rev-parse --verify' codex/skills/ywc-create-pr/scripts/scan-secrets.sh`
- [ ] `bash codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh`
- [ ] `grep -q 'codex/skills/ywc-create-pr/scripts/test-scan-secrets.sh' scripts/validate.sh`
- [ ] `cmp codex/skills/ywc-create-pr/scripts/scan-secrets.sh plugins/ywc-agent-toolkit/skills/ywc-create-pr/scripts/scan-secrets.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- [ ] `git checkout -- .claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`  — Phase 000008 parallel tasks do NOT commit the baseline file; yk-000008-040 stages it last

## Verification
- [ ] lint/structure passes (`bash scripts/validate.sh`)
- [ ] typecheck: N/A
- [ ] unit tests: covered by `scripts/validate.sh` plus the task-specific commands above
- [ ] build: N/A

## Implementation Notes (optional)

<!-- Starts empty at generation time. -->
