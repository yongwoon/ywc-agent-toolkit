# 000020-050-docs-agent-behavioral-evidence

## Purpose

Define a concrete A8 behavioral evidence path for Codex custom agents without prematurely editing agent TOML or evaluator harness code.

## Scope

- Add a lightweight evidence strategy under evaluator docs/references if useful.
- Cover Codex custom agents in `codex/agents/*.toml`.
- Define bounded prompt fixture shape for read-only reviewer-style agents.
- Record harness limitations and deferral rationale in the 2026-06-18 report if no current harness consumes agent fixtures.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-eval-quality-improvement-cycle.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-rubric.md`
- `codex/agents/*.toml`

### Summary

Implements AC5 and FR-5. This task creates an evidence strategy or records why A8 remains at 3 until a separate harness/spec exists.

### Out of Scope

- Changing agent role boundaries without evidence.
- Implementing a new agent smoke harness in this cycle.
- Requiring write access, app execution, network, or external services for fixtures.

## Dependencies

### Depends On

- `000020-010-docs-codex-eval-judgment-report`

### Depended By

- `000021-010-infra-codex-eval-sync-validation`

## Key Files

- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md`
- `docs/skill-agent-eval/codex/2026-06-18-full-sweep.md`
- `codex/agents/*.toml` (read-only unless the evidence strategy proves a narrow wording fix is necessary)

## Parallel Execution Metadata

- **Ownership:** Agent A8 evidence reference and A8 limitation notes in the 2026-06-18 report.
- **Shared Surfaces:** Internal evaluator documentation and Codex agent evidence semantics.
- **Conflicts With:** Any task editing the same report A8 section before `000020-010` merges.
- **Parallelizable After:** `000020-010-docs-codex-eval-judgment-report`
- **Task Verify:** See `task.md`.

## Notes

- Prefer a documented strategy over TOML edits if there is no executable harness to validate A8 behavior today.
