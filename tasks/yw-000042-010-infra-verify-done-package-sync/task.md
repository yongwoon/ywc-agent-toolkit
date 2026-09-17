# yw-000042-010-infra-verify-done-package-sync — Implementation Checklist

## Prerequisites
- [ ] `yw-000041-010-docs-verify-done-ledger` is merged.
- [ ] Source checker tests and contract evals pass.

## Allowed Edit Scope
- [ ] Change generated `plugins/ywc-agent-toolkit/skills/ywc-verify-done/**` only through the sync script.

## Stop Conditions
- [ ] Stop on residual source/package diff, mode mismatch, failed temporary install, missing CLI mode, or validation error.
- [ ] Stop if any source edit is discovered after sync; return it to its owner.

## Hardening Gate
- [ ] Classify as generated-file-only distribution maintenance.
- [ ] Record predecessor test/eval evidence before sync.
- [ ] Consume the source-first package contract; Data Integrity Hardening is N/A.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` after confirming the source tree is final.
  - Confirm checker, reference, tests, SKILL, eval, six locales, and unchanged `agents/openai.yaml` are present in the mirror.
- [ ] Install into a temporary `CODEX_HOME` using the existing Codex install/list flow.
  - Invoke installed `gate-check.py --status`, bare, and `--reverify` against temporary ledgers and verify installed-path documentation.
- [ ] Run `bash scripts/validate.sh`, then inspect `git diff --stat` and `git diff --check` for generated-only scope.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`

## Verification
- [ ] Lint/typecheck/build: N/A — no repository application pipeline.
- [ ] Unit tests: predecessor `python3 codex/skills/ywc-verify-done/scripts/test_gate_check.py`.
- [ ] Integration: temporary installed three-mode CLI smoke test.

## Implementation Notes (optional)
