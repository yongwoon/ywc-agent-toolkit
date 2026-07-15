# 000062-010-docs-wayfinder-core — Implementation Checklist

## Prerequisites

- [ ] Phase 000061 complete and global validator passes.
- [ ] `ywc-skill-author` RED baseline for new skill is recorded.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-wayfinder/**`만 생성·편집한다.

## Stop Conditions

- [ ] tracker write, implementation default, 또는 여러 active ticket이 필요해지면 중단한다.
- [ ] required locale/UI asset을 완결할 수 없으면 partial bundle을 만들지 않는다.

## Implementation Steps

- [ ] required skill assets와 concise Codex-only frontmatter를 만든다.
  - Related AC/FR: AC1, AC2, AC7, FR-1.
- [ ] map/ticket template에 Destination, Fog, Local Status, evidence, next context와 route fields를 정의한다.
  - Related AC/FR: AC1, Amendment A.
- [ ] creation, resume, invalid ticket, one-active-ticket, terminal resolved/deferred/blocked fixture를 추가한다.
  - Related AC/FR: AC2, Amendment H.

## Task Verify

- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-wayfinder`
  - Expected Passing Signal: Frontmatter/Body/Filesystem checks pass.
  - Pre-change Failing Evidence / Exception: new skill baseline absent before task.
  - Contract/Test Evidence: validator output.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: Wayfinder fixture IDs/tokens pass.
  - Pre-change Failing Evidence / Exception: new contract.
  - Contract/Test Evidence: runner output.

## Verification

- [ ] `bash scripts/validate.sh` passes.
- [ ] temporary `CODEX_HOME` targeted install is deferred to `000063-010`.
