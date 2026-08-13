# 000081-010-infra-eval-rescore-report

## Purpose
Run the completed offline evaluator suite and document evidence-backed S5 deltas.

## Scope
- Run targeted fixture tests, full mocked runner, inventory, repository validation, and mechanical scoring.
- Review score movement against the stated thresholds and document evidence or a concrete evidence-model limitation.
- Update the Codex evaluation report and scoreboard only after reviewing the delta.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#acceptance-criteria` — AC7 and AC8 define the final gates.
- `docs/ywc-plans/20260812-codex-evaluation-s5-hardening.md#outcome-oracle` — required evidence and stop condition.
- `docs/skill-agent-eval/codex/2026-08-12-full-sweep.md` — baseline S5 findings and report structure.

### Summary
This hard-gate task consumes all three fixture tasks and produces the next offline evidence pass. It must preserve the mechanical baseline unless explicitly reviewed, and it must report per-dimension evidence rather than claiming score movement without verification. The task stops after one complete offline fixture-and-score pass.

### Out of Scope (from spec)
- Fixture implementation — handled by `000080-010-test-architecture-invariant-fixtures`, `000080-020-test-iac-design-safety-fixtures`, and `000080-030-test-infra-routing-fixtures`.
- Live adapters, cloud credentials, Terraform execution, S8 watch items, and unapproved `history.mechanical.json` changes — out of scope.

## Criticality
normal

## Dependencies

### Depends On
- `000080-010-test-architecture-invariant-fixtures` — provides architecture evidence and targeted test results.
- `000080-020-test-iac-design-safety-fixtures` — provides IaC/design evidence and targeted test results.
- `000080-030-test-infra-routing-fixtures` — provides optimization/review evidence and targeted test results.

### Depended By
- (None — final task in this batch.)

## Key Files
- `docs/skill-agent-eval/codex/2026-08-12-full-sweep.md` — append/update evidence-backed judgment details as appropriate.
- `docs/skill-agent-eval/codex/scoreboard.md` — update affected rows after delta review.
- `.codex/skills/ywc-codex-toolkit-eval/evals/history.mechanical.json` — read-only by default; never update without explicit baseline review.

## Notes
- Preserve unrelated user changes already present in the report and scoreboard.
- If AC8 cannot be proven by the fixture model, record the concrete limitation instead of weakening assertions.
- Do not add live adapters or update the mechanical history baseline in the default path.

## Hardening Evidence

### Test Feedback Path
- Existing coverage: all targeted Python tests, fake mocked runner, `bash scripts/validate.sh`, and mechanical scorer/CI output.
- Named exception: report-only task; no production behavior changes. Replacement verification is the complete command set listed in `Task Verify`.

### Interface Contract
- Contract: score/report evidence handoff from fixture outputs to Codex report/scoreboard rows.
- Inputs: fixture test output, inventory output, scorer output, and prior report baseline.
- Outputs: evidence-backed report rows and threshold/limitation statement.
- Error model: stop on failed required gate; do not publish a passing score claim.
- Impacted tests: full evaluator command set.

### Critical Surface Review
- Review requirement: N/A — report-only task with no runtime behavior change.

### Data Integrity Hardening
- Trigger surface: N/A — report and read-only verification work.
- Atomic / locking strategy: N/A.
- Transaction boundary: N/A.
- Idempotency guard: N/A.
- Required tests: N/A.

## Parallel Execution Metadata

### Ownership
- `docs/skill-agent-eval/codex/2026-08-12-full-sweep.md`
- `docs/skill-agent-eval/codex/scoreboard.md`
- Read-only access to `.codex/skills/ywc-codex-toolkit-eval/**` during verification.

### Shared Surfaces
- Codex evaluation report and scoreboard.
- Mechanical scorer output and `history.mechanical.json` baseline.

### Conflicts With
- Any task modifying `docs/skill-agent-eval/codex/**` or `history.mechanical.json`.

### Parallelizable After
- `000080-010-test-architecture-invariant-fixtures`
- `000080-020-test-iac-design-safety-fixtures`
- `000080-030-test-infra-routing-fixtures`

### Task Verify
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --only skills --json`
- `bash scripts/run-codex-skill-contract-evals.sh`
- `bash scripts/validate.sh`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --format markdown`
- `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target all --ci`

## Out of Scope
- Mechanical baseline update, live evaluation, infrastructure execution, or S8 remediation.
