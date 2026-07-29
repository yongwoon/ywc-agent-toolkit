# ywc-code-gen

여러 Layer 에 걸친 코드를 동시에 생성하는 Skill 입니다. Backend + Frontend + QA Agent 를 병렬로 실행합니다.

## 사용 방법

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "area exposure heatmap"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## 실행 Agent

| Agent | 생성물 |
|-------|--------|
| Backend Agent (sonnet) | API Route, Service, DB Migration |
| Frontend Agent (sonnet) | UI Component, Query Hook, State 관리 |
| QA Agent (sonnet) | Unit Test, Integration Test, E2E Scenario |

## Contract / TDD baseline

Worker 실행 전에 Backend, Frontend, QA 가 같은 public contract 를 보도록 Contract Snapshot 을 준비합니다. 동작 변경이 있는 생성은 기본적으로 test-first 로 진행하며, `--tdd`는 더 엄격한 RED/GREEN/REFACTOR checkpoint commit 모드입니다.
최종 report 는 최종 생성 코드 형상에 실질적으로 영향을 주는 non-obvious decision 에 한해 `Implementation Notes` 를 남기고, routine 한 boilerplate 설명은 제외합니다.

## 선택적 구현 리뷰

`--review`를 사용하면 생성 결과가 검증과 Confidence Gate를 통과한 뒤 `ywc-impl-review`를 실행합니다. review-only commit 없이 staged, unstaged, untracked, 삭제된 생성 변경을 검토합니다(`--tdd`는 checkpoint 마다 commit 하여 working tree를 비우므로, 이때 review 대상은 `--git-range <pre-generation-sha>..HEAD`로 전환됩니다). 시작 전 working tree는 깨끗해야 하며, Critical/High 이슈는 한 번 수정 후 재검토하고 남은 우려는 결과에 그대로 남깁니다.

**`--review` 없이도**, 생성 파일이 critical path(auth, payment, crypto, PII, external input)에 해당하면 `ywc-impl-review`와 `ywc-security-audit`를 강제 실행합니다(`ywc-sequential-executor`와 동일한 계약). **두 review 모두의** Critical/High finding이 1회 fix cycle 대상이며, 어느 한쪽이라도 `BLOCKED`/`NEEDS_CONTEXT`를 반환하면 성공으로 보고하지 않고 그대로 전파합니다. 이 Skill은 merge 권한이 없으므로 gate는 blocking이 아니라 advisory입니다 — 잔존 finding은 상태를 `DONE_WITH_CONCERNS`로 낮출 뿐 생성 코드를 폐기하지 않습니다.

## sequential-executor 와의 관계

- **sequential-executor**: 순차 실행 (의존성이 있는 작업에 적합)
- **/ywc-code-gen**: 독립 Layer 병렬 생성 (SDK/API/Web 동시 필요 시)
- **ywc-implement**: 승인된 단일 spec 또는 ticket의 직접 구현
- 보완적으로 사용

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
