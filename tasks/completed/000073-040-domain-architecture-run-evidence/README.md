# 000073-040-domain-architecture-run-evidence

## Purpose
Implement the ignored, atomic architecture-invariant run-evidence artifact and its agentic diagnostic propagation under the final closed audit-result contract.

## Scope
Persist only completed audit results beside `.ywc-run-state.json`, reject raw/unknown fields recursively, and allow agentic flows to read the artifact as non-authoritative diagnostic evidence while checkpoint/task state remains authoritative.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-2-amendments--final-readiness-closure` — final invariant evidence and architect adapter
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-1-amendments--spec-readiness-validation` — run-evidence ownership and safety boundary

### Summary
The artifact is a closed version-1 audit result object containing only `version`, `aggregate_verdict`, and sorted `rule_results`. It is written only after a successful bounded audit, atomically replaced, ignored by version control, and never treated as authoritative task/checkpoint state. Raw command/output, transcript, source, generated source, chain of thought, full diff, and unknown keys are rejected recursively.

### Out of Scope (from spec)
- Verifier execution and registry fields — superseded by v1 validation-only scope.
- Changes to the closed context-handoff schema.
- Consumer packet routing — `000073-030`.

## Criticality
normal

## Dependencies

### Depends On
- `000073-010-domain-architecture-invariants-contract` — provides the closed audit-result schema and helper.

### Depended By
- `000074-010-infra-architecture-invariants-distribution` — validates the final evidence and agentic integration.

## Key Files
- `codex/skills/scripts/architecture-invariants.py` — atomic evidence write/read validation.
- `codex/skills/ywc-agentic/**` — diagnostic-only consumption boundary.
- `.gitignore` — ignored artifact entry.

## Notes
- Do not add verifier ID, command digest, exit code, raw output, or contract-state fields; Iteration 2 replaces those fields with the exact audit result object.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-agentic/**`
- Evidence-related functions in `codex/skills/scripts/architecture-invariants.py`
- `.gitignore` architecture-evidence entry

### Shared Surfaces
- `.ywc-run-state.json` adjacency and audit-result JSON shape.
- Helper write/read boundary.

### Conflicts With
- `000073-010-domain-architecture-invariants-contract` — helper contract must be stable.
- `000074-010-infra-architecture-invariants-distribution` — final validation must follow all source changes.

### Parallelizable After
- `000073-010-domain-architecture-invariants-contract`

### Task Verify
- `python3 tests/architecture_invariants_test.py`
- `rg -n 'raw_command|raw_command_output|transcript|chain_of_thought|generated_source|full_diff' codex/skills/scripts/architecture-invariants.py codex/skills/ywc-agentic`

## Hardening Evidence
- Test feedback path: closed-artifact, atomic-write, recursive forbidden-field, and no-authority-escalation fixtures.
- Interface contract: exact Section C audit-result object; no additional fields.
- Data Integrity Hardening: N/A — local diagnostic artifact only; atomic replacement is the required write strategy.
- Critical surface review: inspect ignored-path handling and ensure raw evidence never persists.

## Out of Scope
- Application database changes, subprocess execution, raw transcript storage, and changes to unrelated agentic checkpoint semantics.
