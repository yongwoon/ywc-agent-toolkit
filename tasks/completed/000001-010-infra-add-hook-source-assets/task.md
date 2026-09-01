# 000001-010-infra-add-hook-source-assets — Implementation Checklist

## Prerequisites
- [ ] `docs/ywc-plans/hooks-distribution.md` 존재 확인
- [ ] 소스 경로 접근 가능 확인: `/Users/yongwoon/Desktop/yongwoon/source/active_others/develop-with-llm/setup-collection/default-project/.claude/hooks/`
- [ ] (Root task — 선행 태스크 없음)

## Allowed Edit Scope
- [ ] `claude-code/hooks/**` 내에서만 편집
- [ ] 이 범위 밖 편집이 필요한 경우 중단 후 보고

## Stop Conditions
- [ ] 소스 Hook Script가 7개 미만인 경우 — Spec 확인 후 보고
- [ ] `hooks-registry.json` 포맷 변경이 필요한 경우 — Task 2 구현자와 먼저 합의
- [ ] `scripts/install.sh` 수정이 필요하다고 판단되는 경우 — 이 태스크의 범위가 아님, 중단

## Implementation Steps

- [ ] **Hook Script 7개 복사**
  - [ ] `block-dangerous-commands.py` 복사
  - [ ] `check-claude-md-freshness.sh` 복사 후 실행 권한 확인 (`chmod +x`)
  - [ ] `cost-tracker.py` 복사
  - [ ] `notify-permission.py` 복사
  - [ ] `permission_request.py` 복사
  - [ ] `protect-secrets.py` 복사
  - [ ] `session_start.py` 복사

- [ ] **`claude-code/hooks/hooks-registry.json` 작성**
  - [ ] `docs/ywc-plans/hooks-distribution.md#fr-2` 의 JSON 구조를 기반으로 작성
  - [ ] 각 Hook 항목에 `event`(또는 `events`), `matcher`, `command_global`, `command_local`, `description` 포함
  - [ ] `cost-tracker`는 `"events": ["PostToolUse", "Stop"]` 배열로 표현
  - [ ] `jq '.' claude-code/hooks/hooks-registry.json` 으로 유효성 확인

- [ ] **`claude-code/hooks/README.md` 전면 업데이트**
  - [ ] 상단에 Hook 목록 테이블 작성 (파일명, Event, Matcher, 역할)
  - [ ] 각 Hook별 Overview, 동작 흐름, 의존성(`uv`, `jq`, `git` 등) 섹션 추가
  - [ ] `cost-tracker`의 multi-event 등록 방식 (`PostToolUse` + `Stop`) 명시
  - [ ] `notify-permission.py`의 `CCH_SLA_WEBHOOK` 환경변수 설정 안내 포함

## Task Verify
- [ ] `find claude-code/hooks -maxdepth 1 \( -name '*.py' -o -name '*.sh' \) | wc -l` → `7`
- [ ] `jq '.' claude-code/hooks/hooks-registry.json > /dev/null && echo OK`
- [ ] `jq '.hooks | keys | length' claude-code/hooks/hooks-registry.json` → `7`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] lint 통과 — 이 프로젝트는 shellcheck / markdownlint 사용 (`bash scripts/validate.sh`)
- [ ] `markdownlint claude-code/hooks/README.md` (또는 `bash scripts/validate.sh` 내 포함 여부 확인)
- [ ] build 없음 (shell/python/markdown only project)
