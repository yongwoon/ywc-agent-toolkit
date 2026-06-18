# ywc-code-gen

여러 Layer 에 걸친 코드를 동시에 생성하는 Skill 입니다. Backend + Frontend + QA Agent 를 병렬로 실행합니다.

## 사용 방법

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "area exposure heatmap"
```

## 실행 Agent

| Agent | 생성물 |
|-------|--------|
| Backend Agent (sonnet) | API Route, Service, DB Migration |
| Frontend Agent (sonnet) | UI Component, Query Hook, State 관리 |
| QA Agent (sonnet) | Unit Test, Integration Test, E2E Scenario |

## Contract / TDD baseline

Worker 실행 전에 Backend, Frontend, QA 가 같은 public contract 를 보도록 Contract Snapshot 을 준비합니다. 동작 변경이 있는 생성은 기본적으로 test-first 로 진행하며, `--tdd`는 더 엄격한 RED/GREEN/REFACTOR checkpoint commit 모드입니다.

## sequential-executor 와의 관계

- **sequential-executor**: 순차 실행 (의존성이 있는 작업에 적합)
- **/ywc-code-gen**: 독립 Layer 병렬 생성 (SDK/API/Web 동시 필요 시)
- 보완적으로 사용

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
