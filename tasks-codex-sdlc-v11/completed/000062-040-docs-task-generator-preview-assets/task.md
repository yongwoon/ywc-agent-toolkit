# 000062-040-docs-task-generator-preview-assets — Implementation Checklist

## Prerequisites

- [ ] `000062-030` core preview contract merged.

## Allowed Edit Scope

- [ ] task-generator README/UI/eval/template/reference assets only.

## Stop Conditions

- [ ] template schema deviates from core canonical fields or removes explicit approval evidence이면 중단한다.

## Implementation Steps

- [ ] README/templates/dependency graph에 preview artifact, digest, approval 및 wide-refactor metadata fields를 추가한다.
  - Related AC/FR: AC3, AC9, Amendment L.
- [ ] eval fixtures를 add/update한다.
  - valid preview-only consume, stale/missing/custom path, bypass, spec/path/symlink/collision cases를 포함한다.
  - Related AC/FR: AC3, AC4, Amendments H/M/N.
- [ ] UI wording과 required local documentation을 contract에 맞춘다.
  - Related AC/FR: AC7.

## Task Verify

- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: all preview/refactor fixture IDs and tokens pass.
  - Pre-change Failing Evidence / Exception: fixtures absent.
  - Contract/Test Evidence: runner output.
- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-task-generator`
  - Expected Passing Signal: skill assets valid.
  - Pre-change Failing Evidence / Exception: N/A.
  - Contract/Test Evidence: validator output.

## Verification

- [ ] `bash scripts/validate.sh` passes.
