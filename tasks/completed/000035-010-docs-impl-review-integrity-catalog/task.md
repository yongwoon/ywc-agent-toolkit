# Task: 000035-010-docs-impl-review-integrity-catalog

## Prerequisites

- [ ] (None — root task; no predecessor to verify)

## Allowed Edit Scope

- `claude-code/skills/ywc-impl-review/**` 만 편집한다. 다른 스킬 디렉토리·`codex/**`·`plugins/**`는 건드리지 않는다.

## Stop Conditions

- `recurring-defects.md` §1 또는 §4의 기존 구조가 spec이 가정한 line(37 / 155)과 다르면 멈추고 보고한다.
- SKILL.md line 184 "Recurring real-world defects catalog" 요약 문장을 찾지 못하면 멈추고 보고한다.
- 변경이 6개 README locale의 mirror 범위를 넘어 다른 스킬을 건드려야 하면 멈추고 보고한다.

## Implementation Steps

- [ ] `claude-code/skills/ywc-impl-review/references/recurring-defects.md` §1(line 37 "## 1. Data-layer access-boundary & integrity") 하단에 write-consistency 하위 항목을 추가한다:
  - [ ] **Concurrent write safety**: stock·balance·credits·quota·seats·counter 등 공유 가변값에 application-level `read → modify → write` 금지. 로직 복잡도에 따라 atomic conditional update(+ affected-row check) / row lock / optimistic version check.
  - [ ] **Transaction boundary**: stock 차감 + order 생성, balance 차감 + ledger 기록 등 multi-step logical write는 all-or-nothing (mid-flow 실패 시 rollback).
  - [ ] **Durable idempotency (cross-reference)**: §4 "Idempotency must be durable"(line 155)를 한 줄 pointer로 연결. 문구 restate 금지.
  - [ ] **Scan cue**: "로컬/순차 테스트 green은 concurrency 안전성의 증거가 아니다 — 공유 가변값 write에 atomicity 메커니즘이 없으면 finding으로 표면화."
- [ ] 같은 위치에 severity 가이드 추가: oversell/double-charge/cross-ledger → Critical; money/order/provisioning transaction 누락 → High 또는 Critical(blast radius); duplicate-sensitive in-memory idempotency → High; 해당 코드의 concurrency test 부재 → QA axis High (다른 integration test가 입증하지 않는 한). "QA High" 복합 tier를 만들지 말 것.
- [ ] 필요 시 §1 TOC/헤더를 최소 변경한다 (spec Open Question: §1 하단 bullet 추가가 기본).
- [ ] `claude-code/skills/ywc-impl-review/SKILL.md` line 184 "Recurring real-world defects catalog" 요약 문장에 세 클래스명을 추가한다: race condition / concurrent write safety, transaction boundary / partial write prevention, durable idempotency for retryable side effects. 상세 설명은 넣지 않는다.
- [ ] SKILL.md 변경이 user-facing 요약을 바꾸므로 `README.md`(ko), `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md` 중 해당 요약을 mirror하는 부분을 갱신한다 (mirror하지 않으면 변경 불필요 — 확인 후 기록).

## Task Verify

- [ ] `rg -n "concurrent write|read . modify . write|transaction boundary|partial write|durable idempotency|local test|concurrency-safe" claude-code/skills/ywc-impl-review/references/recurring-defects.md` — 새 항목·scan cue hit
- [ ] `rg -n "race condition|concurrent write safety|transaction boundary|durable idempotency" claude-code/skills/ywc-impl-review/SKILL.md` — 요약 문장 hit
- [ ] `rg -n "QA High" claude-code/skills/ywc-impl-review` — hit 없어야 함 (복합 tier 미생성)
- [ ] durable idempotency 항목이 §1에서 §4를 pointer로 참조하고 문구를 restate하지 않았는지 육안 확인

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] 변경된 README에 대해 markdownlint 0 error (`npx --yes markdownlint-cli2 "claude-code/skills/ywc-impl-review/README*.md"`)
