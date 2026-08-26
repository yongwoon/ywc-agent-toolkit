# 000074-010-infra-architecture-invariants-distribution

## Purpose
Synchronize the generated Codex plugin package and complete release, inventory, install, and repository validation for the architecture-invariants feature.

## Scope
Run the final source/package consistency checks, update only release metadata or validation inventory required by the implemented feature, and perform isolated Codex installation smoke validation.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-2-amendments--final-readiness-closure` — allowed generated-package and validation scope
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#verification-plan` — required final commands and isolated install smoke

### Summary
This hard-gate task runs after all source, fixture, consumer, and evidence tasks are merged. The generated `plugins/ywc-agent-toolkit` package must be synchronized from `codex/skills`, and validation must prove metadata completeness, contract eval coverage, no leaked executable fields, and isolated installation of the new skill.

### Out of Scope (from spec)
- New feature behavior or contract changes — handled by Phase `000073` tasks.
- Claude Code bundle changes.
- Verifier execution or registry distribution.

## Criticality
normal

## Dependencies

### Depends On
- `000073-010-domain-architecture-invariants-contract` — source skill/helper are complete.
- `000073-020-test-architecture-invariants-evaluator` — foundational fixtures and eval inventory are complete.
- `000073-030-refactor-architecture-consumer-packets` — consumers and architect contract are complete.
- `000073-040-domain-architecture-run-evidence` — local evidence and agentic boundaries are complete.

### Depended By
- (None — terminal validation task)

## Key Files
- `plugins/ywc-agent-toolkit/**` — generated Codex package output.
- Release metadata/inventory files discovered by validation — only if required.
- `scripts/validate.sh` — only narrowly scoped inventory/check updates if required.

## Notes
- Use `bash scripts/sync-codex-plugin.sh`; do not hand-edit generated plugin files.
- Use a disposable `CODEX_HOME` for install smoke and do not touch the user’s real skill directory.

## Parallel Execution Metadata

### Ownership
- `plugins/ywc-agent-toolkit/**`
- Feature-specific release metadata and validation inventory entries
- `scripts/validate.sh` only for required architecture-invariants inventory checks

### Shared Surfaces
- Generated Codex plugin package.
- Repository-wide validation and install inventory.

### Conflicts With
- All Phase `000073` tasks — generated output must reflect the complete merged source tree.

### Parallelizable After
- `000073-010-domain-architecture-invariants-contract`
- `000073-020-test-architecture-invariants-evaluator`
- `000073-030-refactor-architecture-consumer-packets`
- `000073-040-domain-architecture-run-evidence`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list`
- `isolated_codex_home=$(mktemp -d) && CODEX_HOME="$isolated_codex_home" bash scripts/install.sh --codex ywc-architecture-invariants`

## Hardening Evidence
- Test feedback path: full repository validation, contract evals, and isolated install smoke.
- Interface contract: generated package must match `codex/skills` source exactly.
- Data Integrity Hardening: N/A — generated distribution and metadata only.
- Critical surface review: inspect final diff for forbidden executable fields, raw evidence leakage, and accidental user-home writes.

## Out of Scope
- Implementing or redesigning the evaluator, consumer packets, evidence artifact, or unrelated validation rules.
