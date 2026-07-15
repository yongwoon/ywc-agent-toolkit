# ywc-wayfinder

대형이거나 불확실한 변경을 여러 session에 걸쳐 탐색할 때 쓰는 discovery Skill 입니다. 로컬 Markdown map 하나와 정확히 하나의 active ticket만 유지하고, 구현 대신 다음 routing 을 결정합니다.

## 사용 시나리오

- ordinary planning 으로 바로 들어가기엔 unresolved decision 이 너무 많을 때
- 여러 session 에 걸쳐 discovery 를 이어가야 할 때
- 외부 tracker write 없이 repo 안의 deterministic handoff 가 필요할 때

## 핵심 계약

- canonical map 경로: `docs/ywc-plans/<slug>-wayfinder.md`
- active ticket 는 항상 하나만 허용
- terminal resolved 상태는 `DONE` 이고 map 을 다시 쓰지 않음
- terminal deferred / blocked 상태는 `NEEDS_CONTEXT` 이고 map 을 다시 쓰지 않음
