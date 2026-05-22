# ywc-brainstorm

구현 착수 전, 사용자의 rough idea 를 명확한 design 으로 전환하는 Socratic dialogue skill 입니다.

## 무엇을 하나요

다음 Hard Gate 를 강제합니다.

> **NO IMPLEMENTATION SKILL, SPEC DRAFTING, OR CODE WRITING UNTIL A DESIGN IS PRESENTED AND THE USER HAS APPROVED IT.**

6단계 dialogue workflow:

1. **Step 1 — Explore project context** — 영향 area 의 `CLAUDE.md`, `docs/`, 최근 commit 을 미리 읽어 stale assumption 방지
2. **Step 2 — Detect "too big for one design"** — 여러 subsystem 이 섞여 있으면 STOP 하고 decomposition 협의
3. **Step 3 — Ask clarifying questions one at a time** — What / Why / Out of Scope / Done When 4개 anchor 를 한 번에 한 질문씩 surface
4. **Step 4 — Propose 2–3 approaches with trade-offs** — 추천 1안 + 대안 1~2안, 각각의 trade-off 명시
5. **Step 5 — Present the design and get approval** — section 별 confirm, 마지막에 명시적 handoff 승인
6. **Step 6 — Handoff to ywc-plan** — 4개 anchor 와 chosen approach 를 `ywc-plan` 에게 명시적 input 으로 전달

이 skill 은 절대로 `ywc-code-gen`, `ywc-spec-writer`, `ywc-task-generator`, executor 로 직접 분기하지 않습니다 — terminal state 는 항상 `ywc-plan` 호출입니다.

## 언제 trigger 되나요

- 사용자가 "아이디어", "구상", "어떻게 만들지", "brainstorm", "ブレスト" 등을 언급할 때
- 의도가 명확하지 않거나 implementation 방식이 여러 가지 가능한 경우
- 요구사항이 여러 subsystem 에 걸쳐 있는 경우
- `ywc-plan` 이 Step 1 에서 의도가 불명확하다고 판단해 위임할 때

## 언제 사용하지 않나요

- 요구가 이미 file path · acceptance criteria 까지 구체적인 경우 → `ywc-plan` 직접
- 기존 spec 의 quality validation → `ywc-spec-validate`
- Library / framework 선택 → `ywc-tech-research` 먼저
- Implementation 진행 중 질문 → `ywc-code-gen`

## 참고

상세 workflow · Rationalization Defense 는 [SKILL.md](./SKILL.md) 를 참조합니다. 원본 process discipline 은 `superpowers:brainstorming` 에서 차용하되 ywc 의 handoff 흐름 (→ ywc-plan) 에 맞게 조정했습니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)
