# ywc-plan

Rough idea를 구현 직전 상태(Small path 직접 실행 plan, 또는 Medium/Large path spec document)로 변환해주는 사전 planning Skill 입니다. Scale 을 자동 판정하여 적절한 downstream Skill 로 routing 합니다.

## 사용 시나리오

- 사용자가 "이 기능 어떻게 만들지 계획 세워줘" 라고 말할 때
- Spec 도 없고 task 도 없는 상태에서, 어디서부터 시작해야 할지 모를 때
- Small change 인지 Spec 까지 만들어야 하는 변경인지 판단이 필요할 때
- `ywc-task-generator` 실행 전에 input 이 될 spec 을 준비해야 할 때

## 사용 방법

```bash
/ywc-plan "<rough request>"
```

또는 자연어로 호출:

> "프로필 페이지에 알림 설정 추가하고 싶은데, 계획 세워줘"

## 입력

- 자연어 변경 요청 (rough idea, feature request, change description)

## 출력

규모에 따라 두 가지 중 하나:

| Scale | Output |
|---|---|
| Small | `./plan.md` — 직접 실행 가능한 단일 PR 계획서 |
| Medium / Large | `docs/ywc-plans/<slug>.md` — `ywc-spec-ready` 또는 수동 `ywc-spec-validate` -> `ywc-task-generator` 흐름이 소비할 spec 문서 |

각 path 별로 명시적인 handoff message 가 출력됩니다.

## 동작 흐름

1. **Clarify** — What / Why / Out of Scope / Done When 4가지 anchor 를 한 번에 질문
2. **Investigate** — `AGENTS.md` / `CODEX.md` / `CLAUDE.md`, `package.json`, `docs/architecture/` 등 핵심 file 만 read
3. **Assess Scale** — Small / Medium / Large 중 정확히 하나 선택 (모호하면 Medium default)
4. **Branch** — Small 이면 `plan.md`, Medium/Large 면 spec 문서 작성
5. **Handoff** — `ywc-spec-ready` 자동 수렴 shortcut 또는 수동 다음 단계 Skill 명시 (실행은 사용자가 결정)

## Safety Invariants

다음에 해당하면 자동으로 Medium 이상으로 escalate 됩니다:

- Database migration / schema 변경
- 새로운 library / framework 도입
- 외부에 노출되는 API contract 신설
- Authentication / authorization 로직 변경
- 2개 이상 module 에 걸친 cross-cutting 변경

## 관련 Skill

- `ywc-tech-research` — Technology 선택이 미정일 때 ywc-plan 보다 먼저
- `ywc-product-review` — Product / business framing 이 불명확할 때 ywc-plan 보다 먼저
- `ywc-spec-ready` — Medium/Large path 에서 사용자가 승인한 validate -> DONE 자동 수렴 shortcut
- `ywc-spec-validate` — Medium/Large path 의 다음 단계
- `ywc-task-generator` — Spec review 통과 후 task 분해
- `ywc-code-gen` — Small path 의 직접 실행 옵션
- `ywc-sequential-executor` / `ywc-parallel-executor` — Task 분해 후 실행

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
