# yw-000048-030-test-granularity-evals — Implementation Checklist

## Prerequisites
- [ ] `yw-000048-010-docs-granularity-contract` is completed and merged.
- [ ] Existing `evals/evals.json` schema and runner conventions are reviewed.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-task-generator/evals/evals.json`.
- [ ] Do not modify the generic contract runner or agent policy files unless a concrete limitation is reported.

## Stop Conditions
- [ ] Stop if the existing eval schema cannot represent one of the four required cases without runner changes.
- [ ] Stop if a fixture would need to assert an undocumented or contradictory source rule.
- [ ] Stop if JSON validation or the targeted runner fails for an unrelated pre-existing fixture; report the failure separately.

## Hardening Gate
- [ ] Classify as test/evaluation contract work.
- [ ] Establish RED-first evidence against the superseded thresholds or named existing coverage before finalizing fixtures.
- [ ] Record the fixture schema contract and runner consumer before editing.
- [ ] Mark Data Integrity and critical-surface review as N/A.

## Implementation Steps
- [ ] Append an accepted LLM vertical-slice fixture requiring one feature, exclusive Ownership, explicit Shared Surfaces, and the new size guideline.
- [ ] Append a rejected LLM cross-feature fixture that remains split despite fitting under the numeric limit.
- [ ] Append a human-mode fixture requiring category splitting across Database/API/UI concerns.
- [ ] Append an advisor-awareness fixture requiring the selected mode and exactly its matching guideline.
- [ ] Add assertions that ban superseded `~10/~300` and `~25/~800` guidance in the affected source contract.

## Task Verify
- [ ] `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `git diff --check`

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — JSON fixture task)
- [ ] unit tests pass (`bash scripts/run-codex-skill-contract-evals.sh`)
- [ ] integration tests pass (N/A — source-level contract evals)
- [ ] app builds without error (N/A — distribution validation is downstream)

## Implementation Notes

