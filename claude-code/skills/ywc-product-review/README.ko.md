# Product Review Skill

## 개요

**ywc-product-review** Skill은 진행 중인 프로젝트를 5가지 비즈니스·서비스 관점에서 분석하여 우선순위가 정해진 개선 Feedback을 제공하는 Claude Code Skill입니다.

코드베이스와 문서(README, 기획서, Spec)를 모두 분석하여, 기술적인 코드 품질이 아닌 **사용자 가치·성장·리스크·시장 관점**에서의 개선점을 도출합니다.

**주요 기능:**

- 5가지 비즈니스 관점에서 프로젝트 분석
- 코드베이스 + 문서 통합 분석
- 🔴 High / 🟡 Medium / 🟢 Low 우선순위 Report 자동 생성
- 즉시 실행 가능한 개선 제안 포함
- Executive Summary로 핵심 인사이트 요약

**사용 대상:**

- 서비스 개선 방향을 찾고 있는 Product Manager 및 개발자
- 비즈니스 관점에서 프로젝트를 점검하고 싶은 팀
- "다음에 무엇을 만들어야 할까?"에 대한 답을 구하는 팀

---

## 사용 방법

### Skill 호출

Claude Code에서 다음과 같이 호출합니다:

```
# 전체 분석 (5가지 관점 모두)
/ywc-product-review

# 특정 관점만 분석
/ywc-product-review user-value growth

# 문서를 명시적으로 지정
/ywc-product-review @README.md @docs/spec.md
```

또는 자연어로:

```
User: 이 프로젝트를 비즈니스 관점에서 리뷰해줘
User: 서비스 개선 포인트를 찾아줘
User: 우리 제품에서 성장을 위해 개선해야 할 부분이 뭐야?
User: 사용자 가치 관점에서 부족한 점을 분석해줘
```

### 전제 조건

- 분석 대상 프로젝트의 코드베이스가 현재 Directory에 있거나
- README, 기획서 등의 문서를 참조할 수 있는 상태

---

## 분석 관점

### 5가지 핵심 관점

| 관점 태그 | 분석 내용 | Reference 파일 |
|---|---|---|
| `[User Value]` | Job-to-be-Done, Value Proposition, 충족되지 않은 요구 | `references/user-value.md` |
| `[UX Flow]` | Onboarding, 이탈 포인트, 핵심 사용자 Journey | `references/ux-flow.md` |
| `[Growth]` | Retention, Viral Loop, Activation, Engagement | `references/growth.md` |
| `[Risk]` | 사용자 Pain Point, Churn 요인, 미해결 문제 | `references/risk.md` |
| `[Market]` | Feature 우선순위, 시장 트렌드, 경쟁사 Gap | `references/market-timing.md` |

### 분석 흐름

```
Context 수집 (README + 코드베이스)
    ↓
Phase 1: 5가지 관점 Subagent 병렬 실행 (각 Sonnet)
├── User Value  ├── UX Flow  ├── Growth  ├── Risk  └── Market
    ↓
Phase 2: Opus Advisor (크로스 관점 충돌 시, 최대 2회)
    ↓
우선순위 분류 (High / Medium / Low)
    ↓
Report 생성 + Executive Summary
```

---

## 출력 Report 형식

분석 완료 후 다음 형식으로 결과를 출력합니다:

```markdown
## Product Review Report: [Project Name]

**Analysis Date**: [날짜]
**Perspectives Reviewed**: User Value · UX Flow · Growth · Risk · Market Timing

---

### 🔴 High Priority — 즉시 개선 권장

| # | Perspective   | Problem        | Evidence        | Suggestion      |
|---|---------------|----------------|-----------------|-----------------|
| 1 | [User Value]  | [문제 설명]     | [코드/문서 근거] | [개선 제안]      |

---

### 🟡 Medium Priority — 단기 Roadmap 검토

...

---

### 🟢 Low Priority — 중장기 고려

...

---

### Executive Summary

- **가장 큰 기회**: [최고 임팩트 개선점]
- **즉시 해결해야 할 과제**: [가장 긴급한 문제]
- **중장기 방향성**: [서비스의 다음 단계 방향]
```

---

## 파일 구조

```
ywc-product-review/
├── SKILL.md                        # Skill 정의 및 Workflow
├── README.md                       # 이 파일 (한국어 Guide)
├── README.en.md                    # English Guide
├── README.ja.md                    # 日本語 Guide
├── README.ko.md                    # 한국어 Guide (동일)
└── references/
    ├── user-value.md               # 사용자 가치 체크리스트
    ├── ux-flow.md                  # UX Flow 체크리스트
    ├── growth.md                   # Growth Mechanics 체크리스트
    ├── risk.md                     # Risk & Pain Points 체크리스트
    ├── market-timing.md            # Market Timing 체크리스트
    └── report-template.md          # Report 출력 Template
```

---

## 사용 예시

### Example 1: 전체 관점 분석

```
User: 이 프로젝트를 비즈니스 관점에서 리뷰해줘

Claude: 프로젝트 구조와 README를 확인합니다.

[코드베이스 및 문서 분석 수행]

Phase 1: 5개 Subagent 병렬 실행 중...
[User Value Subagent] Job-to-be-Done 명확성 검토 중
[UX Flow Subagent] Onboarding 및 핵심 Flow 분석 중
[Growth Subagent] Retention 및 Viral 메커니즘 검토 중
[Risk Subagent] 미해결 Pain Point 탐색 중
[Market Subagent] 경쟁사 Gap 및 타이밍 분석 중
Phase 2: Opus Advisor로 크로스 관점 충돌 검토 중...

## Product Review Report: My Project

### 🔴 High Priority

| # | Perspective | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | [UX Flow] | Onboarding이 5단계 이상 필요 | README의 Quick Start가 복잡함 | 핵심 가치를 2단계 이내로 경험할 수 있도록 간소화 |
| 2 | [Growth] | Retention 메커니즘 없음 | 재방문 유도 기능 없음 | 주간 Summary 알림 또는 진행 상황 Dashboard 추가 |

...

### Executive Summary
- **가장 큰 기회**: Onboarding 간소화로 Activation Rate 향상
- **즉시 해결해야 할 과제**: 재방문 유도 메커니즘 부재
- **중장기 방향성**: Network Effect가 있는 협업 기능 도입
```

### Example 2: 특정 관점만 분석

```
User: Growth 관점에서만 분석해줘

Claude: Growth Mechanics 관점으로 분석합니다.

[references/growth.md 로드 및 적용]

## Product Review Report: My Project
**Perspectives Reviewed**: Growth

### 🔴 High Priority
...
```

---

## Best Practices

### 1. 문서와 코드를 함께 제공

코드베이스만 있는 경우보다 README, 기획서, 사용자 인터뷰 자료를 함께 제공하면 더 깊은 분석이 가능합니다:

```
User: @README.md @docs/product-spec.md 이 파일들을 바탕으로 Product Review를 해줘
```

### 2. 반복 활용으로 진화 추적

기능 추가나 개선 후 다시 실행하여 개선 전후를 비교할 수 있습니다.

### 3. Executive Summary를 Roadmap 입력으로 활용

High Priority 항목을 Sprint 또는 Milestone의 입력으로 직접 활용하세요.

---

## 관련 문서

### 프로젝트 내부 참조

- [UI/UX Review Skill](../ywc-ui-ux-review/README.md) — UI/UX 관점 상세 리뷰 (시각 디자인, Information Architecture)

### 외부 참조

- [Jobs-to-be-Done Theory](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) — Clayton Christensen
- [Hooked: How to Build Habit-Forming Products](https://www.nirandfar.com/hooked/) — Nir Eyal

---

## 버전 정보

- **마지막 업데이트**: 2026-04-25
- **Skill Version**: 1.0
- **호환 환경**: Claude Code

---

## License

이 Skill은 `develop-with-llm` 프로젝트의 일부로, 학습 및 참고 목적으로 제공됩니다.
