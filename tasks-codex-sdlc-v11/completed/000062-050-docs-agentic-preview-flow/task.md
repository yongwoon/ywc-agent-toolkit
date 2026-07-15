# 000062-050-docs-agentic-preview-flow — Implementation Checklist

## Prerequisites

- [ ] `000062-040` preview command/output contract merged.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-agentic/**` only.

## Stop Conditions

- [ ] second call re-decomposes or does not repeat matching spec/task context이면 중단한다.
- [ ] interactive request can bypass human approval이면 중단한다.

## Implementation Steps

- [ ] Medium/Large Task Phase의 first preview-only call을 fixed project-relative `--spec`과 함께 정의한다.
  - Related AC/FR: AC4, Amendment N.
- [ ] returned preview path/revision/digest를 검증하고 UTC run log에 append한 뒤 matching approved call을 정의한다.
  - Related AC/FR: AC4, Amendment H.
- [ ] normal propagation, stale/missing/mismatch/direct bypass fixture를 추가한다.
  - Related AC/FR: AC4, Amendment H.

## Task Verify

- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: standard Task Phase forwards `--spec` and valid two-call fixture passes.
  - Pre-change Failing Evidence / Exception: old one-call behavior.
  - Contract/Test Evidence: runner output.
- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-agentic`
  - Expected Passing Signal: validator exit 0.
  - Pre-change Failing Evidence / Exception: N/A.
  - Contract/Test Evidence: validator output.

## Verification

- [ ] `bash scripts/validate.sh` passes.
