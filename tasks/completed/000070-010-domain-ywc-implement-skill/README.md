# 000070-010-domain-ywc-implement-skill

## Purpose
Create the direct Codex implementation lane for exactly one approved specification or ticket.

## Scope
Add `codex/skills/ywc-implement/` with its `SKILL.md`, Tier 1 READMEs, `agents/openai.yaml`, and focused eval fixture. Encode approval evidence, clean baseline and feature-branch handling, TDD/focused checks, full verification, mandatory review, one bounded correction cycle, and conventional commit rules.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#iteration-2-amendments` — authoritative direct-lane approval and review protocol
- `docs/ywc-plans/codex-sdlc-v11-gap-closure.md#acceptance-criteria` — required behavior and distribution checks

### Summary
The new skill handles one approved `--spec` or resolvable approved `--ticket`. It must reject vague ideas, task ranges, broad generation, missing approval evidence, and missing acceptance criteria before editing. The workflow must protect user work, complete verification and `ywc-impl-review`, and prevent delivery after blocked or unresolved Critical/High findings.

### Out of Scope (from spec)
- Multi-layer generation — handled by `ywc-code-gen`.
- Generated task lifecycle — handled by `ywc-sequential-executor` and `ywc-parallel-executor`.
- Prototype, research, Claude bundle, installation scripts, and CI changes — excluded by the spec.

## Dependencies

### Depends On
- (None — root task)

### Depended By
- `000070-020-refactor-impl-review-merge-base` — consumes the direct lane's review-routing contract.
- `000071-010-refactor-direct-lane-handoffs` — documents the completed direct-lane boundary.

## Key Files
- `codex/skills/ywc-implement/SKILL.md` — new skill contract.
- `codex/skills/ywc-implement/README*.md` — Tier 1 documentation.
- `codex/skills/ywc-implement/agents/openai.yaml` — Codex UI metadata.
- `codex/skills/ywc-implement/evals/evals.json` — trigger and boundary coverage.

## Notes
Keep `SKILL.md` below 500 lines and reuse existing `ywc-tdd-ritual`, `ywc-impl-review`, and `ywc-verify-done` contracts. Do not add helper scripts or dependencies unless an existing deterministic command cannot express the workflow.

## Hardening Evidence

### Test Feedback Path
- RED-first target: `codex/skills/ywc-implement/evals/evals.json` before final skill wording.
- Existing coverage: `bash scripts/run-codex-skill-contract-evals.sh`.

### Interface Contract
- Contract: `ywc-implement` invocation and completion report.
- Inputs: exactly one approved `--spec <repo-relative-path>` or resolved approved `--ticket <reference>`.
- Outputs: changed files, verification commands with exit status, review status, commit SHA when delivered, and unresolved concerns.
- Error model: `NEEDS_CONTEXT` for invalid input/baseline/review target; `BLOCKED` or `DONE_WITH_CONCERNS` prevents delivery as specified.

### Critical Surface Review
- Review requirement: `ywc-impl-review` must run before delivery; no PR, force-push, or published-commit amendment.

### Data Integrity Hardening
- Trigger surface: N/A — workflow documentation and generated metadata only.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-implement/**`

### Shared Surfaces
- Codex skill descriptions and `agents/openai.yaml` metadata.
- Direct-lane routing text in adjacent skills.

### Conflicts With
- `000071-010-refactor-direct-lane-handoffs` — may edit overlapping routing descriptions.

### Parallelizable After
- `(Root task — no predecessor required)`

### Task Verify
- `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-implement`
- `bash scripts/run-codex-skill-contract-evals.sh`

## Out of Scope
Do not modify existing implementation, executor, installation, CI, or generated marketplace files in this task.
