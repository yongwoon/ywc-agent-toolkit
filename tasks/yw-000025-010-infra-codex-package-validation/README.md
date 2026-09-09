# yw-000025-010-infra-codex-package-validation

## Purpose
Validate the completed async-monitoring source changes and regenerate the Codex marketplace package from source of truth.

## Scope
Run targeted JSON and contract checks, synchronize `plugins/ywc-agent-toolkit/skills/`, run repository validation, and inspect the generated diff. This task makes no source fixes.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#functional-requirements` — FR-5
- `docs/ywc-plans/20260909-codex-subagent-async-monitoring-and-review-output.md#verification` — required commands and diff inspection
- `codex/AGENTS.md#build-test-and-development-commands` — source/package workflow

### Summary
The Codex source tree must pass affected eval JSON checks and contract validation before synchronization. `bash scripts/sync-codex-plugin.sh` is the only package-generation path; the generated diff must contain only expected mirror changes and no agent TOML edits.

### Out of Scope (from spec)
- Any source-skill implementation fix — reopen the owning Phase 2 task if validation fails
- Manual edits to `plugins/ywc-agent-toolkit/skills/`
- Changes to `codex/agents/*.toml`, release metadata, or unrelated validation failures

## Criticality
normal

## Dependencies

### Depends On
- `yw-000024-010-domain-parallel-monitor-gate` — final parallel source/eval changes
- `yw-000024-020-domain-sequential-advisor-monitor` — final sequential source/eval changes
- `yw-000024-030-domain-review-monitor-output` — final review/status source/eval changes

### Depended By
- (None — final validation task)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` — generated mirror output only
- `scripts/sync-codex-plugin.sh` — generation command, not modified

## Notes
- If a check fails, report and reopen the owning source task; do not patch source or mirror here.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh` and `bash scripts/validate.sh`
- Named exception: generated-file-only task; source behavior is covered by predecessor tasks.

### Interface Contract
- (N/A — no new public or cross-task implementation surface)

### Critical Surface Review
- Review requirement: `N/A — validation-only`

### Data Integrity Hardening
- Trigger surface: N/A — generated-file-only validation
- Atomic / locking strategy: N/A
- Transaction boundary: N/A
- Idempotency guard: N/A
- Required tests: N/A

## Parallel Execution Metadata

### Ownership
- `plugins/ywc-agent-toolkit/skills/**` generated output only
- Validation command scope for the repository

### Shared Surfaces
- Source/package parity across `codex/skills/**` and `plugins/ywc-agent-toolkit/skills/**`
- Repository validation and eval runner

### Conflicts With
- All source-edit tasks; this task starts only after their merged baseline

### Parallelizable After
- `yw-000024-010-domain-parallel-monitor-gate`
- `yw-000024-020-domain-sequential-advisor-monitor`
- `yw-000024-030-domain-review-monitor-output`

### Task Verify
- `node -e 'JSON.parse(require("fs").readFileSync("codex/skills/ywc-parallel-executor/evals/evals.json", "utf8")); JSON.parse(require("fs").readFileSync("codex/skills/ywc-sequential-executor/evals/evals.json", "utf8")); JSON.parse(require("fs").readFileSync("codex/skills/ywc-impl-review/evals/evals.json", "utf8"))'`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `git diff --check`
- `git diff -- codex/skills plugins/ywc-agent-toolkit/skills codex/agents`

## Out of Scope
- Source fixes, manual mirror edits, unrelated package changes, and release/version updates.
