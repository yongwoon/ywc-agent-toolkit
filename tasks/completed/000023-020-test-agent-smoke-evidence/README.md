# 000023-020-test-agent-smoke-evidence

## Purpose

Add concrete smoke fixtures and captured-output evidence for all seven Codex custom agents so A8 reporting has local, reviewable evidence.

## Scope

- Create `agent-smoke-fixtures.json` with happy-path, boundary-routing, missing-evidence, and read-only discipline cases.
- Add captured output files under `evals/agent-smoke-output/<agent>/<case>.md`.
- Ensure every captured output includes review metadata and exactly one agent response.
- Run the smoke validator and record the passing command for the final report task.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-1-add-agent-smoke-fixture-files` — required fixture coverage.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-2-add-captured-output-evidence-contract` — output path and metadata requirements.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#artifact-schema-agent-smoke-fixturesjson` — fixture schema rules.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md` — prior A8 evidence gap and smoke fixture guidance.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-rubric.md` — A8 evidence scoring interpretation.

### Summary
The fixture set must cover all seven Codex custom agents with bounded evidence packets and observable expected/forbidden signals. Captured outputs are saved manually after invoking the matching custom agent with the fixture prompt, but the validator itself remains local-file only. This task produces the evidence that the final evaluation report may cite for A8 rubric decisions.

### Out of Scope (from spec)
- Validator implementation — handled by `000023-010-infra-agent-smoke-harness`.
- A8 scoreboard movement — handled by `000024-010-docs-eval-report-scoreboard`.
- Live model benchmarking or automated remote execution — out of scope for the spec.

## Dependencies

### Depends On
- `000023-010-infra-agent-smoke-harness` — provides `agent_smoke.py`, schema enforcement, and validator tests.

### Depended By
- `000024-010-docs-eval-report-scoreboard` — needs fixture/output paths and passing validator result.

## Key Files
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-architect/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-security-engineer/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-root-cause-analyst/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-performance-engineer/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-typescript-reviewer/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-python-reviewer/*.md`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/ywc-go-reviewer/*.md`

## Notes

- Use bounded packets, not repository dumps.
- Captured output metadata should include fixture ID, agent name, capture date, and source commit or working-tree note.
- If a captured response fails the validator, do not weaken forbidden signals to pass; adjust the fixture only if the original expectation was objectively wrong.

## Parallel Execution Metadata

### Ownership
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/**`

### Shared Surfaces
- Agent A8 evidence contract.
- Internal evaluator fixture inventory.

### Conflicts With
- (None identified after `000023-010-infra-agent-smoke-harness` merges)

### Parallelizable After
- `000023-010-infra-agent-smoke-harness`

### Task Verify
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py --fixtures tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json --outputs tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `bash scripts/validate.sh`

## Out of Scope

- Editing custom-agent TOML definitions unless a fixture uncovers an explicit contract contradiction that blocks evidence capture.
- Automatically invoking remote agents from the validator.
- Moving scoreboard scores.
