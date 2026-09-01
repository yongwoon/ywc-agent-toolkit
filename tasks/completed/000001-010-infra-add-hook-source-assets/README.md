# 000001-010-infra-add-hook-source-assets

## Purpose

Hook 배포의 기반이 되는 static asset을 repository에 추가한다. 구체적으로는 7개 Hook Script를 `claude-code/hooks/`에 복사하고, install.sh가 참조할 `hooks-registry.json`을 정의하며, `claude-code/hooks/README.md`를 전면 업데이트한다.

이 태스크는 다음 태스크(`000002`)에서 install.sh가 hooks-registry.json을 파싱할 수 있도록, **포맷과 파일 경로를 먼저 확정**하는 Phase 1 foundation 역할을 한다.

## Scope

- 7개 Hook Script를 소스 경로에서 `claude-code/hooks/`로 복사
  - `block-dangerous-commands.py`
  - `check-claude-md-freshness.sh`
  - `cost-tracker.py`
  - `notify-permission.py`
  - `permission_request.py`
  - `protect-secrets.py`
  - `session_start.py`
- `claude-code/hooks/hooks-registry.json` 신규 작성 — Hook별 event, matcher, command 템플릿, 설명 정의
- `claude-code/hooks/README.md` 전면 업데이트 — 각 Hook 설명, 의존성, 설정 가이드

## Spec Reference

### Primary Sources
- `docs/ywc-plans/hooks-distribution.md#fr-1-레포지토리-구조` — Hook 파일 목록과 디렉토리 레이아웃
- `docs/ywc-plans/hooks-distribution.md#fr-2-hooks-registryjson-포맷` — registry JSON 포맷 전체 정의 (command_global / command_local 키명, 각 Hook의 event/matcher)

### Summary

소스 프로젝트(`develop-with-llm/setup-collection/default-project/.claude/hooks/`)의 Hook Script 7개를 이 repository의 `claude-code/hooks/`에 그대로 복사한다. 더불어 install.sh가 settings.json에 기록할 내용을 생성할 때 참조하는 메타데이터 파일 `hooks-registry.json`을 정의한다. registry의 `command_global`/`command_local` 키는 install.sh의 jq 쿼리에서 직접 참조되므로 이 태스크에서 포맷을 확정해야 한다.

### Out of Scope (from spec)

- `scripts/install.sh` 수정 — `000002-010-infra-implement-hook-installer`에서 처리
- root `README.md` 업데이트 — `000003-010-infra-update-toolkit-readme`에서 처리
- `settings.json`의 `permissions`(allow/deny) 블록 — Spec에서 명시적으로 제외
- Hook README 다국어 번역 — Spec Out of Scope

## Dependencies

### Depends On
- (None — 이 태스크는 Phase 1 root 태스크)

### Depended By
- `000002-010-infra-implement-hook-installer` — `hooks-registry.json`의 키 구조(command_global, command_local, event, matcher)를 install.sh jq 쿼리에서 직접 참조

## Key Files

| 파일 | 변경 유형 |
|------|-----------|
| `claude-code/hooks/block-dangerous-commands.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/check-claude-md-freshness.sh` | 신규 (소스에서 복사) |
| `claude-code/hooks/cost-tracker.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/notify-permission.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/permission_request.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/protect-secrets.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/session_start.py` | 신규 (소스에서 복사) |
| `claude-code/hooks/hooks-registry.json` | 신규 작성 |
| `claude-code/hooks/README.md` | 전면 업데이트 |

## Notes

- Hook Script는 파일 내용을 수정하지 않고 그대로 복사한다. Script 내부의 경로참조는 `$CLAUDE_PROJECT_DIR` 또는 `~/.claude/` prefix로 동작하도록 이미 설계되어 있음.
- `cost-tracker.py`는 `PostToolUse`와 `Stop` 두 event에 등록된다. registry의 해당 Hook 항목은 `events` 배열(`["PostToolUse", "Stop"]`)로 표현하고, install.sh에서 두 event에 각각 추가해야 한다. registry의 이 예외 구조를 Task 2 구현자가 명확히 인지할 수 있도록 README.md에도 명시한다.
- `check-claude-md-freshness.sh`는 `bash` 실행, 나머지 6개는 `uv run`으로 실행된다.

## Parallel Execution Metadata

### Ownership
- `claude-code/hooks/**`

### Shared Surfaces
- `claude-code/hooks/hooks-registry.json` — Task 2가 이 파일의 JSON 구조에 직접 의존

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — 선행 태스크 없음)

### Task Verify
- `find claude-code/hooks -name '*.py' -o -name '*.sh' | wc -l` → 7 이상
- `jq '.' claude-code/hooks/hooks-registry.json > /dev/null` → valid JSON
- `bash scripts/validate.sh`

## Out of Scope

- Hook Script 내용 수정 (버그 수정, 기능 추가 등)
- Script 실행 테스트 (uv, jq 의존성 설치 여부 확인은 install.sh 역할)
- settings.json 수정
- install.sh 수정
