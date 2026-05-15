# ywc-spec-validate

사양 작성 완료 후, task-generator 실행 전에 사양 품질을 검증하는 Spec Reviewer Agent Skill 입니다.

## 사용 방법

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
```

## 검토 관점

| 관점             | 검토 내용                                                 |
| ---------------- | --------------------------------------------------------- |
| 완성도           | 필수 항목 누락 (Error Handling, Edge Case, Pagination 등) |
| 일관성           | 문서 간 용어/Format/데이터 구조 불일치                    |
| 실현 가능성      | 현재 Stack 으로 구현 가능한지                             |
| 기존 코드 정합성 | 현재 DB Schema, API Route 패턴과 충돌 여부                |

## 실행 Agent

### Phase 1 — 병렬 분석 (Sonnet × 4)

| Subagent | 담당 관점 |
|---|---|
| Completeness Subagent | 완성도 |
| Consistency Subagent | 일관성 |
| Feasibility Subagent | 실현 가능성 |
| Code Compatibility Subagent | 기존 코드 정합성 |

### Phase 2 — Advisor (Opus, 최대 2회)

모호한 Findings에 한해 Opus Advisor가 판단을 제공합니다.

## 출력 형식

Critical / Warning / Suggestion 심각도별 분류, 각 Issue 에 파일:행 참조 및 개선 제안

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
