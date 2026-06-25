# ywc-spec-validate

사양 작성 완료 후, task-generator 실행 전에 사양 품질을 검증하는 Spec Reviewer Agent Skill 입니다.

## 사용 방법

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md --tasks tasks/
```

> `--tasks <dir>` 를 함께 전달하면 task 생성 이후 spec ↔ tasks 정합(Cross-Artifact Analyze)까지 검증합니다 — 모든 requirement 가 task 로 covered 되는지, orphan task 가 없는지 확인.

## 검토 관점

| 관점             | 검토 내용                                                 |
| ---------------- | --------------------------------------------------------- |
| 완성도           | 필수 항목 누락 (Error Handling, Edge Case, Pagination 등) |
| 일관성           | 문서 간 용어/Format/데이터 구조 불일치                    |
| 실현 가능성      | 현재 Stack 으로 구현 가능한지                             |
| 기존 코드 정합성 | 현재 DB Schema, API Route 패턴과 충돌 여부                |
| 단순성           | 명시 Scope 가 아직 요구하지 않는 추상화·구성·일반성(과설계) 여부 — 실현 가능성 Pass 내에서 Warning 으로 표면화 |

## 실행 Agent

### Phase 1 — 병렬 분석 (Sonnet × 4)

| Subagent | 담당 관점 |
|---|---|
| Completeness Subagent | 완성도 |
| Consistency Subagent | 일관성 |
| Feasibility Subagent | 실현 가능성 |
| Code Compatibility Subagent | 기존 코드 정합성 |

### Phase 2 — Advisor (Opus, 최대 2회)

모호한 Findings에 한해 Opus Advisor가 판단을 제공합니다. `--advisor-budget <n>` 으로 호출당 escalation 횟수를 제어할 수 있으며, `--advisor-budget 0` 이면 escalation 을 비활성화하고 해당 Finding 을 일반 Suggestion 으로 보고합니다 (orchestrator 의 비용 가드용).

## 출력 형식

Critical / Warning / Suggestion 심각도별 분류, 각 Issue 에 파일:행 참조 및 개선 제안

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
