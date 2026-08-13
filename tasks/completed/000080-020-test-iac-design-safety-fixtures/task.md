# 000080-020-test-iac-design-safety-fixtures — Implementation Checklist

## Prerequisites
- [ ] Confirm this task owns only the IaC-author and infra-design fixture subtrees.
- [ ] Confirm no concurrent task is editing shared evaluator framework files.

## Allowed Edit Scope
- [ ] Stay within the two declared fixture subtrees and named owning skill files for evidence-driven fixes.
- [ ] Stop before changing shared validator, runner, or verifier code.

## Stop Conditions
- [ ] Stop if a required assertion needs arbitrary command execution, live credentials, network access, or Terraform apply.
- [ ] Stop if the existing fixture schema cannot represent the behavior safely.
- [ ] Stop if a shared evaluator change is required and ownership cannot be serialized.

## Hardening Gate
- [ ] Classify this as critical infrastructure-safety contract coverage.
- [ ] Add failing target-specific assertions before any skill contract edit.
- [ ] Record the fixture schema contract, expected statuses/artifacts, and no-apply boundary.
- [ ] Data Integrity Hardening: N/A — read-only fixture/evaluator work.
- [ ] Require full implementation review or `ywc-impl-review` before completion.

## Implementation Steps
- [ ] Inspect both target `SKILL.md` files and existing fixture manifests before adding cases.
- [ ] Add an IaC-author missing-design case asserting clarification/`NEEDS_CONTEXT`.
- [ ] Add an IaC-author successful-path case asserting validate/plan and review handoff without apply.
- [ ] Add an infra-design case asserting `infra-design.md`/handoff evidence and no Terraform authoring in the same pass.
- [ ] Use only contained files and supported checks; declare target skills and dependencies explicitly.
- [ ] Apply a smallest owning-skill correction only if the fixture proves a real contract defect.

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

