# ywc-impl-review

구현 완료 후 PR 작성 전에 사양 적합성을 종합 검증하는 Skill 입니다. Phase 1 에서 5개 Agent (Architecture / Design / Devex / Security / QA — Sonnet 4개, Haiku 1개) 를 병렬로 실행하고, 애매한 finding 은 Phase 2 Opus Advisor 로 확대합니다.

## 사용 방법

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
```

`--working-tree`는 commit 없이 staged, unstaged, untracked source 변경을 검토합니다. `--code`, `--git-range`와 함께 사용하지 마세요.

## 실행 Agent

| Agent                  | 검증 내용                                                        |
| ---------------------- | ----------------------------------------------------------------- |
| Architecture (sonnet) | Module 경계, Layering, Dependency 방향, 구조적 사양 적합성        |
| Design (sonnet)       | API/Interface 설계, Naming, Signature, Error Model, Contract 사양 적합성 |
| Devex (sonnet)        | 가독성, Error Message, Logging, Documentation, Debuggability      |
| Security (sonnet)     | OWASP Top 10 분석                                                  |
| QA (haiku)            | Test Coverage 격차, 누락된 Test Case                               |

Phase 2 (opus) — 위 5개 Agent 중 애매한 finding 만 선별하여 확대 검토합니다 (Budget: 기본 5회, `--advisor-budget` 로 조정 가능, 공유).

## 출력 형식

통합 Report — Aggregator 가 Phase 1 finding 과 Phase 2 Advisor 판정을 병합하여 심각도별 분류 및 수정 우선순위 제공. 각 finding 은 `[P1]`/`[P2]` marker 로 Phase 1/Phase 2 출처를 표시합니다.

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
- [Chinese](./README.zh.md)
- [Spanish](./README.es.md)
