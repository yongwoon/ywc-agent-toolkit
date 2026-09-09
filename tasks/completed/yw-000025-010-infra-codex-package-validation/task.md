# yw-000025-010-infra-codex-package-validation — Implementation Checklist

## Prerequisites
- [ ] `yw-000024-010-domain-parallel-monitor-gate` is completed and merged
- [ ] `yw-000024-020-domain-sequential-advisor-monitor` is completed and merged
- [ ] `yw-000024-030-domain-review-monitor-output` is completed and merged

## Allowed Edit Scope
- [ ] Run validation and synchronization commands only
- [ ] Generated writes may target `plugins/ywc-agent-toolkit/skills/**`; do not edit source or agent TOMLs

## Stop Conditions
- [ ] Stop and reopen the owning source task if any targeted eval or validation fails
- [ ] Stop if synchronization produces unexpected non-mirror files
- [ ] Stop if the generated diff includes manual edits or `codex/agents/**` changes

## Hardening Gate
- [ ] Classify as generated-file-only validation
- [ ] Use predecessor test evidence; do not invent a failing test for this task
- [ ] Confirm no new interface, data-integrity, or critical-surface change is introduced

## Implementation Steps
- [ ] Parse the three affected `evals/evals.json` files and run `bash scripts/run-codex-skill-contract-evals.sh`.
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root.
- [ ] Run `bash scripts/validate.sh` and `git diff --check`.
- [ ] Inspect `git diff -- codex/skills plugins/ywc-agent-toolkit/skills codex/agents` and confirm only expected source/package parity changes are present; report unexpected changes without fixing them here.

## Task Verify
- [ ] `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-parallel-executor/evals/evals.json", "utf8")); JSON.parse(require("fs").readFileSync("codex/skills/ywc-sequential-executor/evals/evals.json", "utf8")); JSON.parse(require("fs").readFileSync("codex/skills/ywc-impl-review/evals/evals.json", "utf8"))'`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --check`

## Verification
- [ ] All targeted checks pass
- [ ] Source/package diff inspection confirms generated-only mirror changes

## Implementation Notes (optional)
