# yw-000049-010-infra-granularity-distribution

## Purpose
Synchronize the validated Codex task-generator source into the generated marketplace package and run the complete distribution quality gate.

## Scope
Run the standard source-first plugin synchronization, inspect the generated task-generator mirror, verify no superseded thresholds remain in affected source or generated surfaces, and run diff, repository validation, and Codex contract evaluations.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260918-codex-task-generator-granularity-expansion.md#FR-5`
- `scripts/sync-codex-plugin.sh`
- `scripts/validate.sh`
- `scripts/run-codex-skill-contract-evals.sh`

### Summary
The generated marketplace package is derived from `codex/skills`; source changes must be synchronized before inspecting or validating the mirror. Completion requires source/mirror agreement, no affected old thresholds, passing contract evals, clean diff checks, and passing repository validation.

### Out of Scope (from spec)
- Any source contract, README, or eval edits — handled by Phase `yw-000048` tasks.
- Hand-authored changes directly in `plugins/ywc-agent-toolkit/skills/**`.
- Changes to `codex/agents/*.toml` or generic validation scripts.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000048-010-docs-granularity-contract` — finalized source instructions.
- `yw-000048-020-docs-granularity-readmes` — finalized public documentation.
- `yw-000048-030-test-granularity-evals` — finalized regression fixtures.

### Depended By
- (None — final task in this batch)

## Key Files
- `scripts/sync-codex-plugin.sh` — source-to-mirror synchronization command.
- `plugins/ywc-agent-toolkit/skills/ywc-task-generator/**` — generated mirror to inspect.

## Notes
- Run synchronization before reviewing the generated diff.
- If the mirror differs after sync, stop and report rather than hand-editing it.

## Hardening Evidence
### Test Feedback Path
- Named exception: generated-only distribution task; source contract evals, diff checks, sync inspection, and full validation provide replacement verification.

### Interface Contract
- Contract: source-to-marketplace skill mirror.
- Owner task: `yw-000049-010-infra-granularity-distribution`.
- Canonical signature: `codex/skills/**` source -> synchronized `plugins/ywc-agent-toolkit/skills/**` distribution copy.
- Consumers: marketplace installs and downstream validation.
- Implementation opacity: generated consumers trust the sync output; no hand-authored divergence is permitted.
- Mismatch action: `NEEDS_CONTEXT`.

### Critical Surface Review
- Review requirement: N/A — generated distribution and validation task.

### Data Integrity Hardening
- Trigger surface: N/A — generated-file task.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata
### Ownership
- `plugins/ywc-agent-toolkit/skills/ywc-task-generator/**` generated mirror during synchronization and inspection.
- Validation command outputs and no source files beyond sync-generated content.

### Shared Surfaces
- Generated marketplace package.
- Repository validation and contract-eval gates.

### Conflicts With
- All Phase `yw-000048` tasks — distribution must run after their merge.

### Parallelizable After
- `yw-000048-010-docs-granularity-contract`
- `yw-000048-020-docs-granularity-readmes`
- `yw-000048-030-test-granularity-evals`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `git diff --check`
- `bash scripts/validate.sh`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
- Source edits, direct generated-mirror edits, unrelated package changes, and runner changes.
