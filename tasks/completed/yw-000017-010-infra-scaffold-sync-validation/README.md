# yw-000017-010-infra-scaffold-sync-validation

## Purpose
Regenerate the Codex marketplace package from source and prove the complete PR #220 port satisfies repository validation.

## Scope
Run source-focused checks, sync with `scripts/sync-codex-plugin.sh`, verify generated parity and required terms, then run the repository validation gates.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#fr6--codex-contract-coverage-and-packaging` — packaging boundary
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#verification` — required commands
- `docs/ywc-plans/20260902-codex-project-scaffold-pr220-port.md#ac11` — sync and validation acceptance criterion

### Summary
The Codex source tree is authoritative. This task regenerates `plugins/ywc-agent-toolkit/skills/` only through the sync script, checks the generated plugin contains the source changes, and runs JSON, install-list, Markdown, and repository validation gates.

### Out of Scope (from spec)
- Any source behavior or reference edits — handled by Phase 000015 tasks.
- Eval fixture edits — handled by `yw-000016-010-test-scaffold-contract-evals`.
- Manual edits to generated plugin files.

## Dependencies
### Depends On
- `yw-000016-010-test-scaffold-contract-evals` — complete source change set and fixtures.

### Depended By
- (None — final task in this generated set)

## Key Files
- `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/**` — generated output updated by sync script.
- `codex/skills/ywc-project-scaffold/**` — source inspected, not edited by this task.

## Notes
Review the generated diff after sync. If validation fails because of a source issue, report it to the owning task rather than hand-editing the package.

## Parallel Execution Metadata
### Ownership
- `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/**` (generated output only through the sync script)
- Validation command scope for `codex/skills/ywc-project-scaffold/**` and repository scripts.

### Shared Surfaces
- Entire generated Codex marketplace package and repository validation status.

### Conflicts With
- `(None identified)`

### Parallelizable After
- `yw-000016-010-test-scaffold-contract-evals`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`

## Out of Scope
Do not manually repair generated files, modify Claude Code content, or change unrelated source files to silence validation.
