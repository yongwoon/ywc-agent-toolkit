# Implementation Task — 000062-010-infra-auth-implement-distribution-validation

## Prerequisites

- [ ] `000061-010-domain-auth-implement-skill` is merged.
- [ ] `000061-020-test-auth-implement-routing-evals` is merged.
- [ ] `000061-030-docs-auth-implement-catalogs` is merged.
- [ ] Working tree contains the complete Phase 000061 source state.

## Allowed Edit Scope

Run `bash scripts/sync-codex-plugin.sh`; it alone may change generated `plugins/ywc-agent-toolkit/**`. Do not hand-edit plugin output or source files.

## Stop Conditions

- [ ] Source skill contract/eval/catalog validation fails; return the failing command and error to the source-task owner.
- [ ] Sync script is unavailable or generates a path outside `plugins/ywc-agent-toolkit/**`.
- [ ] Disposable install lacks `SKILL.md` or `agents/openai.yaml`.

## Hardening Gate

- [ ] Run source JSON, description, and contract checks before package synchronization.
- [ ] Verify the source-to-plugin package interface and disposable installation after synchronization.
- [ ] Complete full review of auth-skill distribution results; Data Integrity is N/A except deterministic sync idempotency.

## Implementation Steps

- [ ] Run targeted source checks: parse eval JSON, run description cap checks and the contract-eval runner.
- [ ] Test installation into a disposable `CODEX_HOME` and assert installed `SKILL.md` and `agents/openai.yaml`.
- [ ] Generate the plugin package through `bash scripts/sync-codex-plugin.sh`; inspect output without direct edits.
- [ ] Run `bash scripts/validate.sh` and `git diff --check`; report exact command results.

## Task Verify

- [ ] Run every command listed in the README Task Verify block.
- [ ] `test -f plugins/ywc-agent-toolkit/skills/ywc-auth-implement/SKILL.md`
- [ ] `test -f plugins/ywc-agent-toolkit/skills/ywc-auth-implement/agents/openai.yaml`

## Verification

- [ ] `bash scripts/validate.sh` passes.
- [ ] `git diff --check` passes.
