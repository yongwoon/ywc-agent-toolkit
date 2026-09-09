# yw-000022-010-infra-impl-review-package-validation — Implementation Checklist

## Prerequisites

- [ ] `yw-000021-010-domain-impl-review-verification-contract` is completed and merged.
- [ ] `yw-000021-020-test-impl-review-verification-evals` is completed and merged.
- [ ] `yw-000021-030-docs-impl-review-localized-flow` is completed and merged.

## Allowed Edit Scope

- [ ] Allow only generated changes under `plugins/ywc-agent-toolkit/skills/ywc-impl-review/**` created by `bash scripts/sync-codex-plugin.sh`.
- [ ] Do not hand-edit generated files or modify authoritative sources, scripts, or custom-agent TOML files.

## Stop Conditions

- [ ] Stop if source changes are incomplete, unmerged, or fail the targeted source checks.
- [ ] Stop if synchronization changes a package path outside the declared generated skill directory.
- [ ] Stop if source/package parity, validation, or the no-agent-change check fails.

## Hardening Gate

- [ ] Classify this task as generated-file-only and infrastructure validation.
- [ ] Use the named existing checks before and after synchronization.
- [ ] Consume the Source-to-marketplace generated package parity contract; return `NEEDS_CONTEXT` on a source, destination, or consumer mismatch.
- [ ] Data Integrity Hardening is N/A because the sync is a deterministic generated-file operation.
- [ ] Critical surface review is N/A because this task changes no application behavior.

## Implementation Steps

- [ ] Validate the final source inputs.
  - [ ] Run `jq empty codex/skills/ywc-impl-review/evals/evals.json`.
  - [ ] Run `bash scripts/run-codex-skill-contract-evals.sh` and stop on failure.
- [ ] Generate the marketplace mirror.
  - [ ] Run `bash scripts/sync-codex-plugin.sh` only after all Phase 21 source edits are present.
  - [ ] Inspect the generated diff and keep it limited to `plugins/ywc-agent-toolkit/skills/ywc-impl-review/**`.
- [ ] Prove final integrity.
  - [ ] Run `diff -qr codex/skills/ywc-impl-review plugins/ywc-agent-toolkit/skills/ywc-impl-review`.
  - [ ] Run `bash scripts/validate.sh` and inspect `git diff -- codex/agents/*.toml` for an empty result.

## Task Verify

- [ ] `jq empty codex/skills/ywc-impl-review/evals/evals.json`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `diff -qr codex/skills/ywc-impl-review plugins/ywc-agent-toolkit/skills/ywc-impl-review`
- [ ] `bash scripts/validate.sh`
- [ ] `test -z "$(git diff -- codex/agents/*.toml)"`

## Verification

- [ ] Eval JSON and structural contract-eval runner pass.
- [ ] Source and generated package are identical.
- [ ] Repository structural validation passes.
- [ ] No custom-agent TOML file changed.

## Implementation Notes (optional)

