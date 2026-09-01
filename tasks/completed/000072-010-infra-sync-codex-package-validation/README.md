# 000072-010-infra-sync-codex-package-validation

## Purpose
Synchronize the generated Codex marketplace package and prove the complete gap-closure batch is distributable.

## Scope
Run the repository's sync, structural validation, Codex listing, disposable targeted installation, and final source/generated diff checks. Fix only generated output or validation issues caused by the preceding source tasks.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#verification-plan` — required validation evidence
- `codex/AGENTS.md` — source-of-truth and generated-package rules

### Summary
`codex/skills/` is authoritative and `plugins/ywc-agent-toolkit/skills/` is generated. This terminal task synchronizes the package, runs `scripts/validate.sh`, confirms the install listing, installs only `ywc-implement` into a disposable `CODEX_HOME`, and inspects that generated output matches source expectations.

### Out of Scope (from spec)
- Any new source behavior or wording — completed by the predecessor tasks.
- Installation script, CI, Claude bundle, or unrelated package changes — excluded by the spec.

## Dependencies

### Depends On
- `000071-010-refactor-direct-lane-handoffs` — all source changes must be complete before sync.

### Depended By
- (None — terminal validation task)

## Key Files
- `plugins/ywc-agent-toolkit/skills/**` — generated marketplace output.
- `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json` — generated manifest copy if changed by sync.

## Notes
Never hand-edit generated marketplace files. Use a disposable directory for targeted installation and preserve unrelated user configuration.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: `bash scripts/validate.sh`, `bash scripts/install.sh --list --codex`, and targeted install.

### Interface Contract
- Contract: generated package mirrors `codex/skills/` and exposes `ywc-implement` through Codex installation discovery.
- Inputs: completed source skill directories.
- Outputs: synchronized package and successful targeted install.
- Error model: any sync, validation, listing, or install failure blocks completion.

### Critical Surface Review
- Review requirement: full final diff inspection and repository validation.

### Data Integrity Hardening
- Trigger surface: N/A — generated packaging and read-only validation.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `plugins/ywc-agent-toolkit/**` generated output only.
- Disposable validation/install directories under a task-local temporary path.

### Shared Surfaces
- Entire Codex skill package and plugin manifest.

### Conflicts With
- All preceding source tasks — sync must run after their merge.

### Parallelizable After
- `000071-010-refactor-direct-lane-handoffs`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`
- `tmp_codex_home="$(mktemp -d)"; CODEX_HOME="$tmp_codex_home" bash scripts/install.sh --codex ywc-implement; test -f "$tmp_codex_home/skills/ywc-implement/SKILL.md"`

## Out of Scope
Do not manually modify source skills, install scripts, CI, or unrelated generated assets.
