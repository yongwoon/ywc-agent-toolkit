# ywc-project-mission

Project의 durable한 Mission / North-Star, 측정 가능한 Success Criteria, Out-of-Scope non-goal을 `docs/project-mission.md`라는 commit 가능한 Markdown 파일로 영속화하는 Skill입니다. `ywc-review-learnings`와 동일한 stateful-file architecture(특정 runtime 비의존)를 따르며, `ywc-plan`이 새 request를 clarify하기 전에 이 파일을 불러와 모든 planning session을 동일한 north-star로 framing합니다.

핵심은 feature가 끝나면 폐기되는 일회성 plan과 달리, Mission은 어떤 단일 feature보다 오래 살아남는 *durable* 의도를 기록한다는 점입니다. 각 entry는 provenance와 date를 함께 남겨, 현재 commitment와 폐기된 방향을 구분할 수 있습니다.

## 지원 Mode

- **read** — Mission을 불러와 planning을 framing (보통 `ywc-plan`이 호출)
- **update** — 확인된 source에서 Mission / Success Criteria / non-goal을 포착·수정
- **list** — 현재 Mission 표시
- **curate** — stale하거나 superseded된 entry를 deprecate (hard-delete 금지)

## 사용 시나리오

- Brainstorm에서 정리된 Mission(What+Why)과 Success Criteria(Done When)를 Project 차원에서 영속화하고 싶을 때
- 매 planning마다 north-star를 다시 도출하지 않고, `ywc-plan`이 동일한 Mission으로 질문과 Acceptance Criteria를 framing하게 하고 싶을 때
- "이건 이 Project가 절대 하지 않는다"는 durable non-goal을 명시적으로 남기고 싶을 때
- LLM이 Project Mission을 자동으로 이해하도록 CLAUDE.md에 `@docs/project-mission.md` 참조를 추가하고 싶을 때

## 사용 방법

```bash
/ywc-project-mission
```

또는 자연어로 호출:

> "이 Project Mission 기억해둬"
> "Success Criteria 정리해줘"
> "현재 Project Mission 뭐였지?"

## 입력

- (선택) `--mode read|update|list|curate` — Mode 강제 지정 (생략 시 자동 감지)
- (선택) `--source brainstorm|plan` — update 시 Mission/criterion 출처 provenance (기본 `brainstorm`)
- (선택) `--output <경로>` — Mission 파일 경로 (기본: `docs/project-mission.md`)
- (선택) `--dry-run` — 쓰기 없이 CHANGESET만 표시

## 출력

- `docs/project-mission.md` — Mission / North-Star, Success Criteria Table(`ID | Criterion | Source | Added | Status`), Out of Scope, 자동 관리되는 Change Log
- update 시: ADD / MODIFY / DEPRECATE CHANGESET 확인 후 확정 entry만 기록, `Mission updated` 확인 block 출력
- 최초 파일 생성 시: CLAUDE.md에 `@docs/project-mission.md` 추가를 권장하는 활성화 안내를 1회 출력
- 동일 내용 재실행 시(idempotent): 빈 CHANGESET → 파일 쓰기 없음, date bump 없음

## 다른 Skill 과의 관계

- `ywc-brainstorm` — Step 6 Handoff에서 Mission(What+Why)과 Success Criteria(Done When)를 `update --source brainstorm`으로 영속화 제안 (opt-in)
- `ywc-plan` — Step 1에서 read mode로 Mission을 불러와 질문과 Acceptance Criteria를 framing
- `ywc-review-learnings` — 동일한 per-project stateful-file architecture (read/update/list/curate, 사용자 확인 후 쓰기), 다른 도메인 (durable 의도 vs review 선호)
- `ywc-ubiquitous-language` — 도메인 *어휘* 관리. 이 Skill은 도메인 *의도* 를 저장 (혼동 주의)
