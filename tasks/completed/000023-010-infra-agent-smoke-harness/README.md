# 000023-010-infra-agent-smoke-harness

## Purpose

Create the deterministic local harness for Codex custom-agent smoke validation. This task establishes the fixture schema, validator script, and unit coverage without changing `score.py --mode mechanical` semantics or claiming A8 score movement.

## Scope

- Add `agent_smoke.py` under the internal Codex evaluator scripts.
- Define and validate the `agent-smoke-fixtures.json` contract, including explicit `output_path` and exact `Status: <expected_status>` checks.
- Extend `test_score.py` with validator coverage for passing and failing cases.
- Keep `score.py --mode mechanical` deterministic and partial; any smoke summary must be separate or opt-in.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-1-add-agent-smoke-fixture-files` — fixture shape and minimum case families.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-2-add-captured-output-evidence-contract` — captured output location and evidence metadata.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-3-implement-agent-smoke-validator` — validator behavior and failure conditions.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-4-extend-internal-evaluator-tests` — required test cases.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-5-preserve-mechanical-scorer-semantics` — mechanical scorer boundary.

### Summary
The spec requires a local-file smoke validator for Codex custom agents. The validator must parse fixture JSON, locate captured outputs from explicit `output_path` values, require exact status lines, and reject missing expected signals or present forbidden signals. It must not invoke Codex, models, networks, app runtimes, or external services.

### Out of Scope (from spec)
- Real fixture content and captured agent responses — handled by `000023-020-test-agent-smoke-evidence`.
- Skill `evals/evals.json` coverage — handled by `000023-030-test-skill-eval-fixtures`.
- Evaluation report and scoreboard changes — handled by `000024-010-docs-eval-report-scoreboard`.

## Dependencies

### Depends On
- (None) — root task for the new harness.

### Depended By
- `000023-020-test-agent-smoke-evidence` — needs the validator contract and command.
- `000024-010-docs-eval-report-scoreboard` — cites validator behavior and command results.

## Key Files
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py` — new deterministic validator.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py` — validator unit coverage.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` — only if an explicitly separate smoke summary hook is needed.
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/` — schema-adjacent fixture path assumptions.

## Notes

- Prefer Python standard library only.
- The validator should accept CLI flags matching the spec command: `--fixtures` and `--outputs`.
- Do not make A8 a mechanical score in this task. A8 remains judgment-only until a report cites fixture, output, command, exit code, and rubric decision.

## Parallel Execution Metadata

### Ownership
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` smoke-summary boundary only

### Shared Surfaces
- Internal evaluator CLI contract.
- Mechanical regression baseline semantics.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci`
- `bash scripts/validate.sh`

## Out of Scope

- Capturing or curating real custom-agent outputs.
- Editing `codex/agents/*.toml` behavior.
- Updating distributed Codex skills or generated plugin files.
