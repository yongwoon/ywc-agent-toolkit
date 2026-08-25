# 000073-010-domain-architecture-invariants-contract

## Purpose
Create the validation-only `ywc-architecture-invariants` skill and the single shared standard-library contract resolver for optional architecture manifests and normalized audit evidence.

## Scope
Implement the closed v1 manifest/evidence schemas, repository-relative path/glob validation, draft/validate/audit mode contracts, deterministic mapping and verdict semantics, and the required Codex skill metadata and localized README files.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-2-amendments--final-readiness-closure` — operative v1 scope, schemas, modes, and result semantics
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-1-amendments--spec-readiness-validation` — consumer and evidence boundaries refined by Iteration 2

### Summary
V1 is validation-only and launches no child process from contract data. The helper must reject unknown fields, unsafe paths, invalid globs, ambiguous mappings, incomplete coverage, and executable/verifier fields. It must preserve no-manifest compatibility and expose deterministic `DONE`, `BLOCKED`, `N/A`, `MAINTAINED`, `VIOLATED`, and `NEEDS_CONTEXT` outcomes as defined by the operative amendments.

### Out of Scope (from spec)
- Verifier registry, subprocess execution, shell commands, argv, and network sandboxing — explicitly superseded for v1.
- Language-specific import-graph adapters and `ywc-agent-legibility-audit` D6.
- Mermaid diagrams as CI authority.

## Criticality
normal

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000073-020-test-architecture-invariants-evaluator` — consumes the contract and helper behavior.
- `000073-030-refactor-architecture-consumer-packets` — routes consumer packets through the shared helper.
- `000073-040-domain-architecture-run-evidence` — uses the finalized audit result schema.
- `000074-010-infra-architecture-invariants-distribution` — packages and validates the completed source surface.

## Key Files
- `codex/skills/ywc-architecture-invariants/SKILL.md` — new skill interface and behavior.
- `codex/skills/ywc-architecture-invariants/references/contracts.md` — normative closed JSON contracts.
- `codex/skills/scripts/architecture-invariants.py` — shared Python standard-library resolver/evaluator.
- `codex/skills/ywc-architecture-invariants/{README*.md,agents/openai.yaml,evals/evals.json}` — distribution metadata and contract eval inventory.

## Notes
- Do not add a runtime dependency or read `.codex/settings.local.json` in v1.
- Keep the helper API usable by direct consumers without duplicating schema or verdict logic.
- Approval was interactive for `docs/ywc-plans/20260812-codex-architecture-invariants.md`; invocation was `--mode llm`, language `en`, output `tasks/`.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-architecture-invariants/**`
- `codex/skills/scripts/architecture-invariants.py`

### Shared Surfaces
- Closed architecture manifest, evidence, and audit-result JSON contracts.
- Codex skill inventory and generated plugin source boundary.

### Conflicts With
- `000073-020-test-architecture-invariants-evaluator` — tests and evals must target the final contract.
- `000073-030-refactor-architecture-consumer-packets` — consumers must use the final helper interface.
- `000073-040-domain-architecture-run-evidence` — evidence persistence depends on the final result shape.

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 -m py_compile codex/skills/scripts/architecture-invariants.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Hardening Evidence
- Test feedback path: standard-library unit fixtures in `tests/architecture_invariants_test.py` (added by `000073-020`).
- Interface contract: `references/contracts.md` and the helper's closed input/output shapes.
- Data Integrity Hardening: N/A — no application data schema or persistence migration.
- Critical surface review: normal criticality; security constraints are covered by negative fixtures and static inspection.

## Out of Scope
- Consumer-specific packet wiring, agentic run-evidence persistence, generated plugin synchronization, and release metadata.
