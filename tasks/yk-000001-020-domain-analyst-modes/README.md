# yk-000001-020-domain-analyst-modes

## Purpose
Analyst caller and mode contract implements FR-2 and AC-2 of the approved Codex adoption specification.

## Scope
- Update the analyst TOML and all three callers atomically: debug_hypotheses, incident_five_whys, confidence_root_cause; missing/unknown/mismatched pairs return NEEDS_CONTEXT.
- Record minimal feedback catches/misses; rank 3–5 falsifiable debug candidates and change one variable per experiment. Preserve incident 5 Whys and confidence evidence for/against one cause.
- Stop after three failed fixes; permit a fourth debug attempt only with both evidence-linked Fix #4 signal and Next fix worth attempting fields.

## Spec Reference
### Primary Sources
- [docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md](../../docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md) — FR-2, AC-2, Global Constraints, Module Boundaries, immutable upstream provenance and Verification. (Repository-relative source path.)

### Summary
This task delivers three caller/mode pairs and bounded diagnostic feedback. It owns the FR-2 / AC-2 subset listed in Scope and test.md; the remaining clauses belong to sibling tasks. Consult the frozen merge SHA and bounded upstream paths in the specification before porting, and report drift instead of inventing behavior.

### Out of Scope (from spec)
Other subsets of FR-2 belong to the corresponding sibling task in dependency-graph.md. Catalog/plugin integration is owned by `yk-000002-010-infra-distribution`. Claude Code edits, runtime routing redesign, upstream history/version copying and real remote/cloud mutations are excluded.

## Criticality
critical — Sensitive command, permission, durable-write or cross-caller gate contracts require full review.

## Dependencies
### Depends On
- yk-000001-010-domain-model-hints

### Depended By
- yk-000001-030-domain-authoring-feedback
- yk-000002-010-infra-distribution

## Key Files
- `codex/agents/README.md`
- `codex/skills/ywc-debug-rootcause/`
- `codex/skills/ywc-incident-postmortem/`
- `codex/skills/ywc-confidence-gate/`
- `codex/agents/ywc-root-cause-analyst.toml`
- `codex/agents/evals/evals.json`
- `tests/fixtures/codex-issue69/upstream-adoption/analyst-modes.json`

## Notes
Mode: llm; language: en; initials: yk. Directory Ownership includes its subtree and new files. Source skills own all existing locales and evaluations. The contract runner already discovers `tests/fixtures/codex-issue69/*/*.json`; add the declared unique fixture without editing the shared runner. Source assertions and expected traces are not live runtime evidence.

Architecture contract_state: N/A — no architecture contract.

Size budget: approximately 35 files / 1,200 changed LOC; include locale/eval work in the estimate before implementation. Report a required split before expanding scope.

## Hardening Evidence
### Test Feedback Path
RED-first target: focused fixtures in the owned upstream-adoption namespace, wired into `tests/codex_issue69_contract_test.py`; remove the relevant clause as a negative control. Record baseline separately from final results.
### Interface Contract
Authority: specification Module Boundaries plus FR-2. Boundary: three caller/mode pairs and bounded diagnostic feedback. Consumers and predecessor contracts are listed under Dependencies. No callable signature is declared by the spec; do not synthesize one. On owner/input/output/status mismatch, return NEEDS_CONTEXT. The task-specific input and expected output/status cases are in test.md.

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
- `codex/agents/README.md`
- `codex/skills/ywc-debug-rootcause/`
- `codex/skills/ywc-incident-postmortem/`
- `codex/skills/ywc-confidence-gate/`
- `codex/agents/ywc-root-cause-analyst.toml`
- `codex/agents/evals/evals.json`
- `tests/fixtures/codex-issue69/upstream-adoption/analyst-modes.json`

### Shared Surfaces
- `codex/agents/README.md`
- `codex/agents/evals/evals.json`

### Conflicts With
- yk-000001-090-domain-infra-evidence
- yk-000002-010-infra-distribution

### Parallelizable After
- yk-000001-010-domain-model-hints

### Task Verify
- `git diff --check`
- `python3 tests/codex_issue69_contract_test.py`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/check-codex-agent-evals.sh`

## Out of Scope
Runtime model routing redesign, new libraries, DB migrations, unapproved upstream behaviors and implementation during task generation.
