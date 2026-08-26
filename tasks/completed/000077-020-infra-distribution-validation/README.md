# 000077-020-infra-distribution-validation

## Purpose
Synchronize distributable metadata and prove the context-safety change passes repository and isolated-install gates.

## Scope
Update affected Tier 1/Tier 2 READMEs, `agents/openai.yaml`, actual inventory metadata, `VERSION`, `CHANGELOG.md`, generated plugin output, and run final validation.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#fr-7-evaluation-and-release`
- `docs/ywc-plans/20260812-codex-agentic-context-safety.md#e-executable-evaluation-matrix-and-release-scope`
- `codex/AGENTS.md#build-test-and-development-commands`
### Summary
Release scope covers eight affected skills, their localized documentation and OpenAI metadata, the discovered inventory source, version/changelog metadata, and generated plugin output. Validation includes repository checks, install listing, and isolated installation smoke after all behavior and eval changes land.
### Out of Scope (from spec)
- New production behavior or eval cases — handled by earlier tasks.
- Claude Code synchronization.

## Criticality
normal

## Dependencies
### Depends On
- `000077-010-test-context-safety-evaluation-matrix` — provides the final eval inventory and passing matrix.
### Depended By
- (None — final gate)

## Key Files
- Affected `codex/skills/*/README*.md` and `agents/openai.yaml`
- `VERSION`, `CHANGELOG.md`
- Actual inventory file discovered during implementation
- `plugins/ywc-agent-toolkit/skills/*` generated mirror

## Notes
`codex/skills/` is the source of truth; use `bash scripts/sync-codex-plugin.sh` for generated plugin output. Do not assume an inventory filename before discovering it.

## Hardening Evidence
### Test Feedback Path
- Existing coverage: `bash scripts/validate.sh`, `bash scripts/install.sh --list --codex`, and isolated install smoke.
### Interface Contract
- Contract: distributable Codex skill bundle metadata and inventory.
- Inputs: finalized source skills/evals and release metadata.
- Outputs: synchronized source/plugin bundle and passing validation.
- Error model: validation failure blocks completion.
- Impacted tests: repository validation and install smoke.
### Critical Surface Review
- Review requirement: N/A — distribution/documentation gate; behavior was reviewed upstream.
### Data Integrity Hardening
- Trigger surface: N/A — metadata/generated files.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: isolated installation smoke.

## Parallel Execution Metadata
### Ownership
- Affected skill metadata files, `VERSION`, `CHANGELOG.md`, discovered inventory source, and generated plugin mirror.
### Shared Surfaces
- Bundle inventory, source/plugin parity, version metadata.
### Conflicts With
- (None identified)
### Parallelizable After
- `000077-010-test-context-safety-evaluation-matrix`
### Task Verify
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`
- `CODEX_HOME=$(mktemp -d) bash scripts/install.sh --codex ywc-agentic`

## Out of Scope
- Any `claude-code/**` changes.
- New behavior or test coverage.
