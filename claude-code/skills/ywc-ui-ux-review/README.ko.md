# UI/UX Review - Hybrid Code & Live UI Auditor

정적 Code 분석과 Chrome DevTools MCP 기반 Live UI 탐색을 결합하여 Project를 UI/UX 관점에서 점검하고, 우선순위별 Markdown report를 생성하는 Claude Code Skill입니다.

## 개요

"어디부터 UX를 손봐야 하는가?"에 evidence 기반으로 답하는 Skill입니다. 모든 finding은 권위 있는 heuristic(Nielsen 10 / WCAG 2.2 AA / Material 3 / Apple HIG / Internal Design System)에 근거합니다.

### 주요 기능

- Hybrid Review: 정적 Code 분석 + Live UI 탐색
- 중점 영역: Information Architecture, Visual Design
- Phase 4 병렬 Subagent: IA Reviewer와 Visual Design Reviewer 동시 실행 (각 Sonnet), Phase 4b에서 병합
- Critical / High / Medium / Low 4단계 출력
- 모든 finding에 location과 heuristic citation 부착
- Chrome DevTools MCP의 accessibility tree snapshot 사용으로 Token 효율 확보

## 사용 방법

```text
http://localhost:3000 의 dashboard UI/UX review 해줘.
```

```text
Settings flow의 usability와 Information Architecture를 audit 해줘.
```

자연어 Trigger는 [SKILL.md](./SKILL.md)에 정의되어 있습니다.

## Reference

- Domain checklist와 heuristic citation은 [`references/`](./references)에 있습니다
- Report template은 [`assets/`](./assets)에 있습니다
- Workflow와 Trigger는 [SKILL.md](./SKILL.md)에 있습니다

## Live UI Tooling

본 Skill은 inspection 중심 작업에 Chrome DevTools MCP를 우선 사용합니다 (accessibility tree snapshot, Lighthouse audit, computed style, screenshot 등). Multi-step interaction 자동화가 필요한 경우에 한해 Playwright MCP를 보조적으로 사용합니다.

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Japanese](./README.ja.md)
