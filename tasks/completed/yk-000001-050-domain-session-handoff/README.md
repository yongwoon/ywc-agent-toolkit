# yk-000001-050-domain-session-handoff

## Purpose
Safe session handoff implements FR-4 and AC-4 of the approved Codex adoption specification.

## Scope
- Port frozen #345 handoff with Goal/State/Decisions/Dead ends/Next step/References/Suggested skills; use reasoned N/A, artifact path references and redaction.
- Require canonical temp containment, slug <=48 characters (empty=session), exclusive creation, symlink/overwrite refusal, owner-only permissions and collision retry; unverifiable paths must not be written.
- Add Tier 1 locales, metadata and evaluations; set explicit invocation preference for handoff, retro and setup without claiming runtime enforcement.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-4, AC-4, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers handoff sections, safe artifact writes and invocation metadata. It owns the FR-4 / AC-4 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-4 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
critical — Sensitive command, permission, durable-write or cross-caller gate contracts require full review.

## Dependencies
### Depends On
- yk-000001-040-domain-session-retro

### Depended By
- yk-000002-010-infra-distribution

## Key Files
- `codex/skills/ywc-handoff/`
- `codex/skills/ywc-setup/`
- `tests/fixtures/codex-issue69/upstream-adoption/session-handoff.json`
- `codex/skills/ywc-retro/agents/openai.yaml`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-4. Boundary: handoff sections, safe artifact writes and invocation metadata. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

### Critical Surface Review
Require ywc-impl-review or full manual implementation review before DONE.
### Data Integrity Hardening
- Trigger surface: permission, retryable commands or durable writes described by this task; apply codex/skills/references/data-integrity-hardening.md where triggered.
- Atomic / locking strategy: preserve existing guards; document all-or-nothing boundaries before changing write instructions.
- Transaction boundary: task-specific operation; no partial-success claim after required-command failure.
- Idempotency guard: refuse duplicate/unsafe side effects; N/A for pure source assertions.
- Required tests: refusal, failure injection and duplicate/retry paths for triggered operations; N/A for pure documentation.

## Parallel Execution Metadata
- Model Hint: `advanced` — Sensitive state and cross-skill reasoning.
### Ownership
- `codex/skills/ywc-handoff/`
- `codex/skills/ywc-setup/`
- `tests/fixtures/codex-issue69/upstream-adoption/session-handoff.json`
- `codex/skills/ywc-retro/agents/openai.yaml`

### Shared Surfaces
- `codex/skills/ywc-retro/agents/openai.yaml`

### Conflicts With
- yk-000001-040-domain-session-retro

### Parallelizable After
- yk-000001-040-domain-session-retro

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
