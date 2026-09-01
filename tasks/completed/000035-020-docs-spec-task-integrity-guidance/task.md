# Task: 000035-020-docs-spec-task-integrity-guidance

## Prerequisites

- [ ] `000035-010-docs-impl-review-integrity-catalog` 병합 완료 (write-consistency 용어·severity 기준 canonical source 확정)

## Allowed Edit Scope

- `claude-code/skills/ywc-spec-validate/**` 와 `claude-code/skills/ywc-task-generator/**` 만 편집한다.

## Stop Conditions

- spec-validate SKILL.md line 80 Step 4 Completeness worker row를 찾지 못하면 멈추고 보고한다.
- task-generator SKILL.md Task Verify 규칙(line 327/383) 또는 task.md.template `## Task Verify`(line 24)를 찾지 못하면 멈추고 보고한다.
- 지침이 impl-review 5-tier severity를 spec-validate에 끌어와야만 표현되면 멈추고 보고한다 (어휘 혼선 방지).

## Implementation Steps

- [ ] `claude-code/skills/ywc-spec-validate/SKILL.md` line 80 Step 4 fan-out 표의 Completeness worker Focus 컬럼을 확장한다: duplicate-sensitive write flow를 정의한 spec에 대해 (a) concurrent request 동작, (b) 복수 DB write의 transaction/consistency boundary, (c) 중복 client retry/double-click 처리, (d) stock/balance/quota 소진 또는 lock/version 불일치 시 failure response/status 가 명시됐는지 점검. 누락 시 Completeness finding(Critical: double charge/oversell/lost ledger/duplicate provisioning 유발 가능 / 그 외 Warning).
- [ ] line 113 "Review Dimensions" 표는 **변경하지 않는다** (generic 유지 — Step 4 Focus가 단일 operative source).
- [ ] spec-validate Rationalization Defense 표에 row 1개 추가: "spec에 코드가 아직 없으니 concurrency는 구현 단계 문제" → "duplicate-sensitive write의 concurrency/transaction/idempotency 요구 누락은 Completeness Critical — spec 단계에서 잡는다."
- [ ] `claude-code/skills/ywc-task-generator/SKILL.md` Task Verify 규칙(line 327 Core Elements, line 383 Quality checklist) 근처에 규칙 추가: task가 duplicate-sensitive write flow를 다루면 그 task.md Task Verify가 concurrent write 동작·partial failure rollback·idempotent retry 를 포함해야 하고, spec이 특정 메커니즘(atomic conditional update / row lock / optimistic lock / idempotency key)을 요구하면 task는 선택 메커니즘과 기대 관찰 결과를 명시해야 한다.
- [ ] task-generator Rationalization Defense 표에 row 1개 추가: "duplicate-sensitive write지만 project-wide build로 검증 충분" → "green build는 THIS task의 concurrency invariant를 증명 못 함 — atomicity/idempotency assertion을 명시."
- [ ] `claude-code/skills/ywc-task-generator/references/task.md.template` line 24 `## Task Verify` 섹션에 간결한 note 추가: 해당 시(stock/balance/order/payment/provisioning/quota write) concurrent request·rollback·idempotency retry 검증 포함.
- [ ] 두 스킬의 README 6 locale 중 user-facing 요약(review dimension/Task Verify 설명)이 바뀐 부분만 mirror. 바뀐 게 없으면 확인 후 기록.

## Task Verify

- [ ] `rg -n "duplicate-sensitive|concurrent request|transaction|idempoten|lock/version" claude-code/skills/ywc-spec-validate/SKILL.md` — Completeness Focus + Rationalization Defense hit
- [ ] `rg -n "Review Dimensions" claude-code/skills/ywc-spec-validate/SKILL.md` 이후 표가 generic으로 유지됐는지 육안 확인 (concurrency 항목 미추가)
- [ ] `rg -n "concurrent|rollback|idempoten|atomic" claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-task-generator/references/task.md.template` — 규칙·template note hit
- [ ] spec-validate 지침이 Critical/Warning/Suggestion 어휘만 쓰는지 육안 확인 (impl-review "High" 미유입)

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] 변경 README markdownlint 0 error (`npx --yes markdownlint-cli2 "claude-code/skills/ywc-spec-validate/README*.md" "claude-code/skills/ywc-task-generator/README*.md"`)
