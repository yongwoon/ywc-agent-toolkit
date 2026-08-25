# Task: 000023-010-infra-agent-smoke-harness

## Prerequisites
- [ ] Read `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md` sections FR-1 through FR-5.
- [ ] Confirm no existing `agent_smoke.py` script already exists under the internal evaluator.

## Allowed Edit Scope
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py` only for a separately labeled smoke summary hook if necessary

## Stop Conditions
- [ ] Stop if implementing the validator requires non-standard-library Python dependencies.
- [ ] Stop if A8 would need to become a `score.py --mode mechanical` axis to complete this task.
- [ ] Stop if fixture path validation cannot prevent `..` escape from `evals/agent-smoke-output/`.
- [ ] Stop if existing `test_score.py` structure makes validator tests too large for the file; report a split-test proposal before adding a second command.

## Implementation Steps

### Add the local validator
- [ ] Create `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/agent_smoke.py`.
- [ ] Implement CLI flags `--fixtures` and `--outputs`, both accepting project-relative or absolute paths.
- [ ] Parse fixture JSON with required top-level `schema` and `fixtures` fields.
- [ ] Validate each fixture requires `id`, `agent`, `output_path`, `intent`, `evidence_packet`, `expected_status`, `expected_signals`, and `forbidden_signals`.
- [ ] Reject duplicate fixture IDs and unknown `agent` values by comparing against `codex/agents/*.toml` stems.

### Enforce output evidence rules
- [ ] Resolve `output_path` relative to `tools/codex-internal/skills/ywc-codex-toolkit-eval/`.
- [ ] Reject absolute `output_path`, `..` traversal, and paths outside `evals/agent-smoke-output/`.
- [ ] Treat missing captured output files as failures.
- [ ] Require the exact line `Status: <expected_status>` in each captured output.
- [ ] Require every `expected_signals` entry to appear in the captured output.
- [ ] Require every `forbidden_signals` entry to be absent from the captured output.

### Preserve scorer boundaries
- [ ] Leave `score.py --mode mechanical` behavior unchanged unless adding an explicitly separate smoke field.
- [ ] If `score.py` is touched, label any smoke result separately from A8 and keep A8 judgment-only.
- [ ] Print a concise per-agent/case summary and exit non-zero on any failure.

### Add tests in `test_score.py`
- [ ] Add temporary fixture/output helper data for a passing case.
- [ ] Add tests for missing output, missing expected signal, present forbidden signal, unknown agent name, and duplicate fixture ID.
- [ ] Ensure tests run through `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`.

## Task Verify
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] No project lint command exists beyond `bash scripts/validate.sh`; validate.sh passes.
- [ ] Unit tests pass through `test_score.py`.
- [ ] Internal mechanical regression gate remains green.
