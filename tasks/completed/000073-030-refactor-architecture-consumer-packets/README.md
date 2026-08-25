# 000073-030-refactor-architecture-consumer-packets

## Purpose
Propagate optional architecture-contract results through direct Codex consumers and the `ywc-architect` bounded output contract without reimplementing evaluation or changing no-manifest behavior.

## Scope
Update `ywc-code-gen`, `ywc-task-generator`, `ywc-impl-review`, and `ywc-architect` to accept paired manifest/evidence inputs, derive bounded changed paths, forward only sanitized invariant packets, and surface the required verdict/status semantics.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#iteration-2-amendments--final-readiness-closure` — consumer evidence interface and architect adapter
- `docs/ywc-plans/20260812-codex-architecture-invariants.md#functional-requirements` — consumer responsibilities and propagation constraints

### Summary
Consumers discover only the repository-root manifest unless an explicit repository-relative manifest is supplied. Evidence without a valid manifest is `NEEDS_CONTEXT`; a manifest without evidence preserves existing behavior. When both are valid, consumers call the shared helper and forward only contract state, affected IDs, result, and evidence path—not raw evidence contents.

### Out of Scope (from spec)
- Shared helper/schema implementation — `000073-010`.
- Foundational evaluator fixtures — `000073-020`.
- Agentic run-evidence artifact persistence — `000073-040`.
- Generated package synchronization — `000074-010`.

## Criticality
normal

## Dependencies

### Depends On
- `000073-010-domain-architecture-invariants-contract` — provides the shared resolver and packet contract.

### Depended By
- `000074-010-infra-architecture-invariants-distribution` — validates and packages the final consumer surfaces.

## Key Files
- `codex/skills/ywc-code-gen/SKILL.md` — bounded generation packet routing.
- `codex/skills/ywc-task-generator/SKILL.md` — component/rule metadata and verifier requirement routing.
- `codex/skills/ywc-impl-review/SKILL.md` — architecture finding source semantics.
- `codex/agents/ywc-architect.toml` — status and invariant verdict output contract.
- Corresponding `evals/evals.json` files — positive and no-evidence routing cases.

## Notes
- Keep existing direct skill behavior unchanged when no contract packet is present.
- `ywc-architect` must not discover manifests, run audits, or infer edges.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-code-gen/**`
- `codex/skills/ywc-task-generator/**`
- `codex/skills/ywc-impl-review/**`
- `codex/agents/ywc-architect.toml`

### Shared Surfaces
- Invariant packet fields and bounded evidence paths.
- Existing skill status/error channels and architect output vocabulary.

### Conflicts With
- `000073-020-test-architecture-invariants-evaluator` — final packet fixtures may extend the shared architecture eval inventory.
- `000074-010-infra-architecture-invariants-distribution` — generated package must not sync a partial source snapshot.

### Parallelizable After
- `000073-010-domain-architecture-invariants-contract`

### Task Verify
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/validate.sh`

## Hardening Evidence
- Test feedback path: consumer-specific positive, no-evidence, invalid-evidence, and violation cases in the affected eval inventories.
- Interface contract: Section C audit result plus the bounded packet fields in Iteration 2 D–E.
- Data Integrity Hardening: N/A — no application data schema.
- Critical surface review: verify no raw evidence content or command-like field reaches a worker or architect.

## Out of Scope
- Creating the architecture-invariant evaluator, changing unrelated routing, or adding process execution.
