# 000035-010-docs-impl-review-integrity-catalog

## Purpose

`ywc-impl-review`(claude-code)가 Race Condition, Partial Write, Idempotency 누락을 recurring defect로 직접 잡을 수 있도록 review catalog와 worker surface를 보강한다. 특히 "로컬/순차 테스트 통과는 concurrency 안전성의 증거가 아니다"라는 scan cue를 명시한다.

## Scope

- `claude-code/skills/ywc-impl-review/references/recurring-defects.md` §1(line 37 Data-layer integrity)에 write-consistency 하위 항목 + scan cue + severity 가이드 추가 (FR-1)
- `claude-code/skills/ywc-impl-review/SKILL.md` line 184 recurring defects catalog summary에 세 결함 클래스명 추가 (FR-2)
- `claude-code/skills/ywc-impl-review/README*.md` (6 locale) mirror 갱신

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-1-extend-implementation-review-recurring-defects-write-consistency-subsection` — catalog에 추가할 defect class·scan cue·severity 기준
- `docs/ywc-plans/claude-code-data-integrity-skill-hardening.md#fr-2-wire-the-new-review-class-into-ywc-impl-review` — `SKILL.md` summary 갱신 범위
- `/Users/yongwoon/Desktop/yongwoon/source/active_others/develop-with-llm/docs/studies/research/race-condition-partial-write-idempotency.md` — 원본 연구 문서

### Summary

상세 지식은 `recurring-defects.md`에 두고 `SKILL.md`에는 짧은 routing summary만 남긴다. 핵심 defect는 application-level read → modify → write, transaction 없는 multi-step write, in-memory idempotency다. durable idempotency는 §4 "Idempotency must be durable"(line 155)를 **restate하지 않고 cross-reference**한다. Severity는 oversell/double-charge/lost ledger/duplicate provisioning blast radius에 맞춰 정한다.

### Out of Scope (from spec)

- `ywc-spec-validate`, `ywc-task-generator` 지침 변경 → `000035-020-docs-spec-task-integrity-guidance`
- executor 지침 변경 → `000035-030-docs-executor-integrity-gates`
- validation/README consistency 최종 게이트 → `000036-010-infra-claude-integrity-validation`
- Codex skill 및 실제 application code 구현 → spec Out of Scope

## Criticality

`normal` — 편집 대상 Ownership(`claude-code/skills/ywc-impl-review/**`)은 보안 키워드(auth/payment/token 등) 경로가 아니다. 다만 이 guidance는 payment/order/data 경로의 review 품질을 바꾸므로 batch 종료 후 `000036-010`에서 review-behavior 회귀를 확인한다 (Notes 참조).

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000035-020-docs-spec-task-integrity-guidance` — 동일한 write-consistency 용어·severity 기준을 downstream spec/task guidance에 재사용
- `000035-030-docs-executor-integrity-gates` — executor가 Task Verify gate로 취급할 defect class 명칭 공유
- `000036-010-infra-claude-integrity-validation` — 최종 validation/README consistency 대상

## Key Files

- `claude-code/skills/ywc-impl-review/references/recurring-defects.md` — primary defect catalog (§1 확장)
- `claude-code/skills/ywc-impl-review/SKILL.md` — recurring real-world defects catalog summary (line 184)
- `claude-code/skills/ywc-impl-review/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.zh.md` / `README.es.md`

## Notes

- 연구 문서를 통째로 붙여넣지 말 것. progressive disclosure — 구체 check는 `recurring-defects.md`, `SKILL.md`는 요약만.
- 기존 용어 재사용: recurring defects, Phase 1, Critical/High/Medium/Low/Info, QA axis, durable idempotency. "QA High" 같은 복합 tier를 만들지 말 것 (QA는 axis, severity는 별도 필드).
- durable idempotency는 §4 line 155를 한 줄 pointer로 연결 — 같은 파일 내 문구 중복 금지.
- README mirror는 SKILL.md의 user-facing 변경(요약 문장에 새 defect class 등장)이 있을 때만 갱신. Tier 2(zh/es)는 이미 shipping되므로 유지.

## Out of Scope

- `codex/skills/**` 및 `plugins/ywc-agent-toolkit/skills/**` 편집 금지.
- 새 script·dependency·validation command 추가 금지.
- `ywc-spec-validate` / `ywc-task-generator` / executor / `ywc-agentic` 편집 금지.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-impl-review/**`

### Shared Surfaces

- Claude Code review semantics: recurring real-world defects catalog
- README locale mirror set for `ywc-impl-review`

### Conflicts With

- `claude-code/skills/ywc-impl-review/**`를 편집하는 모든 task (현 batch에는 없음)

### Parallelizable After

- (Root task — 선행 불필요)

### Task Verify

- `rg -n "concurrent write|read . modify . write|transaction boundary|partial write|durable idempotency|local test|concurrency-safe" claude-code/skills/ywc-impl-review` — 새 항목·scan cue가 실제로 들어갔는지 확인 (≥1 hit in recurring-defects.md AND SKILL.md summary)
- `rg -n "QA High" claude-code/skills/ywc-impl-review` — 존재하지 않아야 함 (exit 1 기대: 복합 tier 미생성)
- `bash scripts/install.sh --list --cc` — 스킬이 여전히 나열되는지
