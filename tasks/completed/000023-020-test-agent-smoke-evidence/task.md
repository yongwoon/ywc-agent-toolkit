# Task: 000023-020-test-agent-smoke-evidence

## Prerequisites
- [ ] `000023-010-infra-agent-smoke-harness` is completed and merged.
- [ ] Read `tools/codex-internal/skills/ywc-codex-toolkit-eval/references/agent-behavioral-evidence.md`.
- [ ] Read all seven `codex/agents/*.toml` files to understand each custom agent's output contract.

## Allowed Edit Scope
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output/**`

## Stop Conditions
- [ ] Stop if the validator from `000023-010` is not available or its CLI differs from the spec command.
- [ ] Stop if a fixture requires full repository context, network access, or live app execution.
- [ ] Stop if a captured output cannot include the required metadata without altering the single-response evidence.
- [ ] Stop if a custom agent's TOML contract contradicts the fixture expectation; report the contradiction instead of weakening the validator.

## Implementation Steps

### Build the fixture inventory
- [ ] Create `tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json` with `schema: 1`.
- [ ] Add at least one happy-path fixture for each agent: `ywc-architect`, `ywc-security-engineer`, `ywc-root-cause-analyst`, `ywc-performance-engineer`, `ywc-typescript-reviewer`, `ywc-python-reviewer`, and `ywc-go-reviewer`.
- [ ] Add boundary-routing fixtures for architecture, security, performance, and one language reviewer.
- [ ] Add at least one missing-evidence fixture expecting `NEEDS_CONTEXT`.
- [ ] Add at least one read-only discipline fixture with forbidden signals for edits, test execution, app execution, network calls, and artifact creation.

### Capture agent outputs
- [ ] For each fixture, manually invoke the matching Codex custom agent with the bounded fixture prompt in a fresh session.
- [ ] Save exactly one response per fixture under `evals/agent-smoke-output/<agent>/<case>.md`.
- [ ] Include metadata in each output file: fixture ID, agent name, capture date, and source commit or working-tree note.
- [ ] Ensure every output contains the exact `Status: <expected_status>` line declared by the fixture.

### Validate the evidence
- [ ] Run `agent_smoke.py` with the fixture file and output directory from the spec command.
- [ ] Fix fixture/output mismatches only when the fixture expectation is objectively wrong or the output was copied incorrectly.
- [ ] Record the final passing command and output summary for `000024-010-docs-eval-report-scoreboard`.

## Task Verify
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py --fixtures tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-fixtures.json --outputs tools/codex-internal/skills/ywc-codex-toolkit-eval/evals/agent-smoke-output`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] Validator exits 0 for the committed fixture/output set.
- [ ] No captured output contains requests to edit files, run tools, call network, or create artifacts when forbidden by its fixture.
- [ ] `bash scripts/validate.sh` passes.
