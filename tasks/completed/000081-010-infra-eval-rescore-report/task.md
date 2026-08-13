# 000081-010-infra-eval-rescore-report — Implementation Checklist

## Prerequisites
- [ ] `000080-010-test-architecture-invariant-fixtures` is merged and its targeted checks pass.
- [ ] `000080-020-test-iac-design-safety-fixtures` is merged and its targeted checks pass.
- [ ] `000080-030-test-infra-routing-fixtures` is merged and its targeted checks pass.

## Allowed Edit Scope
- [ ] Modify only the Codex evaluation report and scoreboard in the declared Ownership.
- [ ] Treat evaluator source, fixtures, and mechanical history as read-only during this task.

## Stop Conditions
- [ ] Stop if any required targeted test, mocked runner, validator, inventory gate, repository validation, or scorer CI command fails.
- [ ] Stop if score movement cannot be tied to fixture or contract evidence.
- [ ] Stop if updating `history.mechanical.json` appears necessary without explicit baseline review.
- [ ] Stop after one complete offline fixture-and-score pass; do not expand into live evaluation.

## Hardening Gate
- [ ] Classify this as report-only verification and documentation work.
- [ ] Use existing test/scorer evidence; no production edits are permitted.
- [ ] Record the report/scoreboard evidence handoff contract and any unmet AC8 limitation.
- [ ] Data Integrity Hardening: N/A — read-only verification and report work.
- [ ] Critical-surface review: N/A — no runtime or safety implementation changes.

## Implementation Steps
- [ ] Run all prerequisite targeted fixture tests and confirm their outputs are attributable to the three predecessor tasks.
- [ ] Run the fake mocked suite, inventory gate, contract-eval script, and `scripts/validate.sh`.
- [ ] Run mechanical scoring in markdown and CI modes without `--update-baseline`.
- [ ] Compare S5 rows for all five named skills against `docs/skill-agent-eval/codex/2026-08-12-full-sweep.md`.
- [ ] Update the report and scoreboard with file/line-backed evidence, threshold results, or a concrete evidence-model limitation.
- [ ] Re-read the diff and confirm no mechanical baseline, live adapter, credential, or S8 changes were introduced.

## Task Verify
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --only skills --json`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --format markdown`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --ci`

## Verification
- [ ] Lint/structure passes (`bash scripts/validate.sh`)
- [ ] Typecheck: N/A — no project typecheck command
- [ ] Unit/evaluator tests pass (commands above)
- [ ] Integration tests: N/A — live evaluation is deferred
- [ ] Build: N/A — no application build

## Implementation Notes

