# ywc-implement

승인된 단일 specification 또는 ticket을 직접 구현하는 Codex Skill입니다.

`--spec <repo-relative-path>` 또는 `--ticket <reference>` 중 하나만 허용하며, 승인 증거와 acceptance criteria가 없으면 `NEEDS_CONTEXT`를 반환합니다.

Clean baseline과 feature branch를 기록하고 기존 패턴을 확인합니다. 동작 변경은 TDD, focused check, 전체 검증, `ywc-impl-review`를 거친 후 conventional commit을 생성합니다. PR과 force-push는 만들지 않습니다.
