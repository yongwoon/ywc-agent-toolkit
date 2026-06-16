# ywc-tech-research

기술 조사 및 라이브러리 비교를 수행하는 Research Agent Skill 입니다.

## 사용 방법

```text
/ywc-tech-research "Hono 에서 Server-Sent Events 구현 방법"
```

## 사용 시나리오

| 상황            | 예시                                               |
| --------------- | -------------------------------------------------- |
| 사양 작성 전    | "Web Analytics SDK Privacy-preserving 방식 비교"   |
| 라이브러리 선택 | "PostgreSQL Partition Table 집계 성능 최적화 전략" |
| 구현 중 막힘    | "Rollup Tree-shaking Polyfill 문제 해결"           |

## 실행 Agent

- **Research Agent** (claude-sonnet-4-20250514)

## 출력 형식

- 요약 (1-2문장)
- 비교 분석 (Table)
- 권장 방안 및 근거
- 프로젝트 적용 시 고려사항
- 참고 자료

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
