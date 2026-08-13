# 000080-030-test-infra-routing-fixtures — Implementation Checklist

## Prerequisites
- [ ] Confirm this task owns only the optimization and review fixture subtrees.
- [ ] Confirm no concurrent task is editing shared evaluator framework files.

## Allowed Edit Scope
- [ ] Stay within the two fixture subtrees and named owning skill files for evidence-driven fixes.
- [ ] Stop before changing shared validator, runner, or verifier code.

## Stop Conditions
- [ ] Stop if the required behavior needs live infrastructure, credentials, arbitrary execution, or network access.
- [ ] Stop if the V2 schema cannot safely express a classification, routing, lens, or BLOCK assertion.
- [ ] Stop if shared evaluator changes are required without serialized ownership.

## Hardening Gate
- [ ] Classify this as critical infrastructure-safety contract coverage.
- [ ] Add failing classification/lens assertions before any skill contract edit.
- [ ] Record the routing and review interface contract, including expected BLOCK behavior.
- [ ] Data Integrity Hardening: N/A — read-only fixture/evaluator work.
- [ ] Require full implementation review or `ywc-impl-review` before completion.

## Implementation Steps
- [ ] Inspect both target `SKILL.md` files and existing optimize/review fixture patterns.
- [ ] Add SAFE, CAUTION, and DANGER optimization cases with explicit routing to `ywc-iac-author`.
- [ ] Assert every optimization case does not auto-execute remediation or apply changes.
- [ ] Add a review case requiring security, cost, and reliability lenses.
- [ ] Add a Critical/High review case asserting an explicit BLOCK recommendation.
- [ ] Apply a smallest owning-skill correction only if fixture evidence proves a real contract defect.

## Task Verify
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_fixture_validator.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/test_runner.py`
- [ ] `python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked`

## Verification
- [ ] Structure validation passes (`bash scripts/validate.sh`)
- [ ] Typecheck: N/A — no project typecheck command
- [ ] Targeted Python tests pass
- [ ] Live integration tests: N/A — explicitly out of scope
- [ ] Build: N/A — no application build

## Implementation Notes

