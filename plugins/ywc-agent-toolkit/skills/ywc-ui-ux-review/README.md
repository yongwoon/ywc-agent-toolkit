# UI/UX Review - Hybrid Code & Live UI Auditor

자신의 Project를 정적 Code 분석과 Live UI 탐색을 결합하여 UI/UX 관점에서 점검하고, 우선순위별 Markdown report를 생성하는 Codex Skill입니다.

## 개요

"우리 Project의 UX, 어디부터 손봐야 하는가?"라는 질문에 evidence 기반으로 답하기 위한 Skill입니다. Code 정적 분석과 available browser tooling를 활용한 Live UI 탐색을 함께 수행하며, 모든 finding은 권위 있는 heuristic(Nielsen 10 / WCAG 2.2 AA / Material 3 / Apple HIG / Internal Design System)에 근거를 둡니다.

### 주요 특징

- **Hybrid Review**: Code 정적 분석 + Live UI 탐색 결합
- **중점 영역**: Information Architecture, Visual Design
- **Multi-Heuristic**: Nielsen 10, WCAG 2.2 AA, Material 3, Apple HIG, Internal Design System
- **우선순위 기반 출력**: Critical / High / Medium / Low 4단계 분류
- **Evidence 기반**: 모든 finding에 file:line 또는 screen:selector + heuristic citation 부착
- **Token 효율**: available browser tooling의 accessibility tree snapshot 우선 사용

## 사용 방법

### 기본 사용

자연어 Trigger 문구를 입력합니다.

```text
UI/UX review 해줘. 대상은 http://localhost:3000 의 dashboard 화면이야.
```

```text
이 project의 navigation과 typography를 점검해줘. usability audit으로.
```

### 사전 준비

- **Live URL**: 실행 중인 dev server 또는 staging URL (필수 권장)
- **Scope 명시**: 점검 대상 page와 주요 user journey
- **Internal Design System** (있는 경우): tokens 위치, component library 위치

Live URL이 없으면 code-only review로 자동 전환되며, 그 사실은 report에 명시됩니다.

## Workflow

| Phase | 단계 | 사용 Tool |
| --- | --- | --- |
| 1 | Scope & Context 확인 | (대화) |
| 2 | Code Reconnaissance | `Read`, `Grep`, `Glob` |
| 3 | Live UI Exploration | available browser tooling |
| 4 | Per-Domain Review (IA → Visual) | `references/*-checklist.md` |
| 5 | Severity Triage | `references/severity-rubric.md` |
| 6 | Report Generation | `assets/report-template.md` |

## Output 예시

생성되는 report는 다음 구조를 가집니다.

```markdown
# UI/UX Review — Dashboard

## Executive Summary
| Tier | Count |
|---|---|
| 🔴 Critical | 2 |
| 🟠 High | 5 |
| 🟡 Medium | 9 |
| 🟢 Low | 4 |

### Top 3 Systemic Patterns
1. Color token이 정의되지 않아 hex literal이 23회 산재
2. ...

## 🔴 Critical
### C-01 · Body text contrast fails WCAG SC 1.4.3
- Location: `src/components/Card.tsx:42`
- Heuristic: WCAG SC 1.4.3 (Contrast Minimum)
- Observed: foreground #8a8a8a on #ffffff = 3.2:1
- Expected: ≥ 4.5:1
- Recommendation:
  ```css
  /* Replace literal with token */
  color: var(--color-text-primary);
  ```
```

기본 저장 경로는 `claudedocs/ui-ux-review-{YYYY-MM-DD}.md` 입니다.

## Skill 파일 구조

```
ywc-ui-ux-review/
├── SKILL.md                              # Skill 정의 (Trigger, Workflow)
├── README.md                             # 이 파일 (한국어 primary)
├── README.en.md                          # English summary
├── README.ja.md                          # Japanese summary
├── README.ko.md                          # Korean summary
├── references/
│   ├── ia-checklist.md                   # Information Architecture checklist
│   ├── visual-design-checklist.md        # Visual Design checklist
│   ├── heuristics-combined.md            # Nielsen + WCAG + Platform + Design System
│   └── severity-rubric.md                # Critical/High/Medium/Low 판정 기준
└── assets/
    └── report-template.md                # 우선순위별 report template
```

### Reference 파일 사용 시점

| Reference | Phase | 용도 |
| --- | --- | --- |
| `ia-checklist.md` | Phase 4 | Information Architecture 점검 |
| `visual-design-checklist.md` | Phase 4 | Visual Design 점검 |
| `heuristics-combined.md` | Phase 4 | 모든 finding에 citation 부착 |
| `severity-rubric.md` | Phase 5 | 4단계 severity 분류 |

## Live UI 도구 선택

본 Skill은 **available browser tooling**를 우선 사용합니다.

| 작업 | 권장 Tool |
| --- | --- |
| Accessibility tree snapshot | `browser accessibility or DOM snapshot tool` |
| Screenshot 수집 | `browser screenshot tool` |
| Responsive 검증 | `browser resize tool` |
| 자동 accessibility scoring | `browser audit tool` |
| Computed style / contrast 계산 | `browser script evaluation tool` |
| Console error 수집 | `browser console inspection tool` |

복잡한 multi-step interaction이 필요한 경우에 한해 Playwright MCP를 보조적으로 사용합니다.

## 확장 방법

### 평가 Framework 추가

`references/heuristics-combined.md`에 새 framework section을 추가합니다. 예: GOV.UK Design System, ISO 9241-110.

### Domain 영역 추가

예: "Form UX"를 별도 영역으로 분리하는 경우:

1. `references/form-checklist.md` 작성
2. `SKILL.md` Phase 4의 영역 순서에 추가
3. Severity Rubric은 공통이므로 수정 불필요

### Internal Design System 연계

Project별 design token 위치가 다르므로 처음 사용 시 user에게 token 위치를 확인하고 review에 반영합니다. 자주 review하는 project가 정해지면 별도 reference 파일로 등록할 수 있습니다.

## 한계

- **실제 user testing의 대체 불가**: 본 Skill은 heuristic 기반 expert review이며, real user 검증과는 보완 관계입니다.
- **주관적 미적 평가 배제**: "예쁘다 / 안 예쁘다" 판단은 하지 않으며, 모든 평가는 heuristic에 anchor됩니다.
- **자동 수정 미수행**: Review만 수행하며 실제 code 수정은 별도 task로 분리합니다.

## 관련 문서

- [Codex Skills Guide](../../README.md)
- [ywc-project-scaffold](../ywc-project-scaffold/README.md) - 다른 Skill 작성 예시
- [WCAG 2.2 (W3C)](https://www.w3.org/TR/WCAG22/)
- [Nielsen 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean (Summary)](./README.ko.md)
