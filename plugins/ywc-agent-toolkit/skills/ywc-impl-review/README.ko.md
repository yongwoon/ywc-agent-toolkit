# ywc-impl-review

구현 완료 후 PR 작성 전에 사양 적합성을 종합 검증하는 Skill 입니다. 3개 Agent (Reviewer + Security + QA) 를 병렬로 실행합니다.

## 사용 방법

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
```

## 실행 Agent

| Agent                 | 검증 내용                                        |
| --------------------- | ------------------------------------------------ |
| Reviewer Agent (opus) | 사양 대비 구현 누락/차이, 코드 품질, 패턴 일관성 |
| Security Agent (opus) | OWASP Top 10, 인증/인가 누락, Input Validation   |
| QA Agent (sonnet)     | Test Coverage 분석, 누락 Test Case 제안          |

## 출력 형식

통합 Report — 3개 Agent 결과를 Aggregator 가 병합하여 심각도별 분류 및 수정 우선순위 제공

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
