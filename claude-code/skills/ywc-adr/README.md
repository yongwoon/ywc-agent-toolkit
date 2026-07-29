# ywc-adr

Project의 Architecture Decision Record(ADR)를 관리하는 Skill입니다. 되돌리기 어렵고, 맥락 없이는 의아하며, 실제 trade-off의 결과인 아키텍처 결정을 `docs/adr/NNNN-<slug>.md` 파일 하나당 하나의 결정으로 기록합니다. `ywc-review-learnings` / `ywc-project-mission`과 같은 stateful-file family에 속하지만, 저장 형태는 다릅니다 — 누적되는 파일 하나가 아니라, 결정마다 별도의 immutable-ish 파일입니다.

`ywc-plan`의 Step 3.5(Architectural Advisor Gate)가 내리는 판단은 지금까지 해당 plan의 `architecture-verdict.md`에만 남고 사라졌습니다. 세 가지 기준(되돌리기 어려움 + 맥락 없이는 의아함 + 실제 trade-off)을 통과하는 결정이라면, 이 Skill이 그 판단을 `ADR-0007`처럼 안정적인 ID로 인용 가능한 기록으로 남깁니다.

## 지원 Mode

- **new** — 새 결정을 기록 (필요 시 기존 ADR을 supersede)
- **read** — Planning/Review를 위해 관련 ADR들을 요약해서 불러오기
- **list** — 전체 ADR 목록과 상태 표시
- **curate** — 후속 ADR 없이 맥락이 사라진 ADR을 Deprecated 처리

**Family와의 의도적인 차이점:** `docs/review-learnings.md`나 `docs/project-mission.md`와 달리, 이 Skill은 `@docs/adr/` 형태의 CLAUDE.md 자동 로드 안내를 출력하지 않습니다. 단일 파일은 매 세션에 미리 불러와도 비용이 적지만, ADR 디렉터리는 무한히 늘어나고 대부분 현재 요청과 무관하기 때문입니다. 대신 `read` mode로 필요할 때 `--target` 기준으로 필터링해서 불러옵니다.

## 사용 시나리오

- `ywc-plan` Step 3.5의 architecture verdict가 세 가지 기준을 통과했을 때, 그 판단을 durable ADR로 남기고 싶을 때
- 과거 결정을 뒤집는 새로운 결정을 내렸고, 왜 방향이 바뀌었는지 기록을 남기고 싶을 때 (supersede)
- 새 spec을 작성하기 전, 이미 확정된 아키텍처 결정과 모순되지 않는지 확인하고 싶을 때
- 더 이상 유효하지 않은 오래된 ADR을 정리하고 싶을 때

## 사용 방법

```bash
/ywc-adr
```

또는 자연어로 호출:

> "이 결정 ADR 로 남겨줘"
> "아키텍처 결정 기록해줘"
> "무슨 ADR 들이 있어?"
> "ADR-0004 는 이제 유효하지 않으니 정리해줘"

## 입력

- (선택) `--mode new|read|list|curate` — Mode 강제 지정 (생략 시 자동 감지)
- (선택) `--supersedes <ADR-NNNN>` — `new` mode에서 대체할 기존 ADR
- (선택) `--target <path|area>` — `read` mode에서 관련 범위로 필터링
- (선택) `--source plan|manual` — 결정의 출처 (기본 `manual`)
- (선택) `--output <디렉터리>` — ADR 디렉터리 경로 (기본: `docs/adr/`)
- (선택) `--dry-run` — 쓰기 없이 CHANGESET만 표시

## 출력

- `docs/adr/NNNN-<slug>.md` — Title / Status / Date / Provenance + Context / Decision / Alternatives Considered / Consequences 섹션을 갖춘 파일
- `new`/`curate` mode 시: 변경 내역을 명시하는 `ADR recorded` 확인 block 출력
- CLAUDE.md 자동 로드 안내는 출력하지 않음 (의도적 — 위 설명 참고)

## 출력 예시

```markdown
# ADR-0007: Deliver webhooks asynchronously via a queue

**Status:** Accepted
**Date:** 2026-07-29
**Provenance:** ywc-plan Step 3.5, plan docs/ywc-plans/webhook-delivery.md

## Context
...

## Decision
We will deliver webhooks through a durable queue, not inline in the request handler.

## Alternatives Considered
- Synchronous delivery with a timeout — rejected because ...
- Third-party delivery service — rejected because ...

## Consequences
...
```

## 관련 Skill

- `ywc-plan` — Step 3.5의 Architectural Advisor Gate가 이 Skill에 `new --source plan`을 opt-in으로 제안하고, Step 2가 `read` mode로 기존 ADR과 모순되지 않는지 확인
- `ywc-architect` — 이 Skill이 기록하는 trade-off 판단을 만들어내는 read-only advisor (자체적으로 저장하지 않음)
- `ywc-review-learnings` / `ywc-project-mission` — 동일한 stateful-file family (사용자 확인 후 쓰기, 파일 부재 시 무차단), 다른 도메인과 저장 형태
