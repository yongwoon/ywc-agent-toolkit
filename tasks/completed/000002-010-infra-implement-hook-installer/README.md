# 000002-010-infra-implement-hook-installer

## Purpose

`scripts/install.sh`에 Hook 설치 기능을 전부 구현한다. 사용자가 `--hooks [--global|--local] [hook-name...]` 인터페이스로 Hook Script를 설치하고, 대상 settings.json에 Hook 항목을 idempotent하게 병합할 수 있게 한다.

## Scope

- `run_hook_install()` 함수 — Hook Script 파일 복사, manifest 기록
- `merge_hook_settings()` 함수 — jq 기반 settings.json atomic 병합 (idempotency 포함)
- CLI 파싱 확장 — `--hooks`, `--global`, `--local` 플래그
- `--list --hooks` 지원
- `usage()` 함수 업데이트
- 의존성 사전 확인 — `jq` 미설치 시 오류 출력, `uv` 미설치 시 경고

## Spec Reference

### Primary Sources
- `docs/ywc-plans/hooks-distribution.md#fr-3-installsh-cli-확장` — CLI 인터페이스 전체 정의
- `docs/ywc-plans/hooks-distribution.md#fr-4-settingsjson-병합-로직` — 4단계 병합 규칙, atomic rename, 백업
- `docs/ywc-plans/hooks-distribution.md#fr-5-파일-설치-경로` — global/local 경로 테이블
- `docs/ywc-plans/hooks-distribution.md#fr-6-manifest` — manifest 파일명, 위치, 내용 포맷
- `docs/ywc-plans/hooks-distribution.md#non-functional-requirements` — jq/uv 의존성 처리, idempotency, atomic write
- `docs/ywc-plans/hooks-distribution.md#edge-cases` — 8개 edge case 처리 목록

### Summary

`scripts/install.sh`의 기존 skill 설치 구조(`run_cc_install`, `prune_orphans`, `write_manifest`)를 참고하여, Hook 설치에 특화된 함수를 추가한다. 핵심 난점은 settings.json 병합: 기존 Hook 항목을 보존하면서 신규 항목만 append하는 idempotent 로직을 jq로 구현해야 한다. global 설치 시 command에는 `~/.claude/hooks/<hook>` (절대 경로), local 설치 시 `$CLAUDE_PROJECT_DIR/.claude/hooks/<hook>` (환경변수 참조)를 사용한다.

### Out of Scope (from spec)

- Hook Script 파일 자체 수정 — `000001-010-infra-add-hook-source-assets`에서 처리 완료
- root README.md 업데이트 — `000003-010-infra-update-toolkit-readme`에서 처리
- `settings.json`의 `permissions`(allow/deny) 병합 — Spec에서 명시적으로 제외
- `--hooks --all` (global + local 동시 설치) — Spec Out of Scope

## Dependencies

### Depends On
- `000001-010-infra-add-hook-source-assets` — `claude-code/hooks/hooks-registry.json`의 포맷(command_global, command_local, event, matcher 키)이 확정되어야 install.sh의 jq 쿼리를 작성할 수 있음

### Depended By
- `000003-010-infra-update-toolkit-readme` — 실제 동작하는 CLI 인터페이스(`--hooks`, `--global`, `--local`, `--list --hooks`)가 확정되어야 README에 정확한 사용 예시를 작성할 수 있음

## Key Files

| 파일 | 변경 유형 |
|------|-----------|
| `scripts/install.sh` | 수정 (함수 추가, CLI 파싱 확장) |

## Notes

- **jq 병합 핵심 로직**: `jq --arg cmd "..." '.hooks.PreToolUse += [{"matcher": "Bash", "hooks": [{"type":"command","command":$cmd}]}]'` 패턴을 사용하되, `any(.hooks[]; .command == $cmd)` 로 중복 체크 후 append 여부를 결정한다.
- **cost-tracker의 multi-event 처리**: `hooks-registry.json`에서 `events` 배열(`["PostToolUse", "Stop"]`)을 가진 Hook은 반복문으로 각 event에 개별 등록한다.
- **atomic write**: `jq ... > /tmp/settings.tmp && mv /tmp/settings.tmp "$SETTINGS_FILE"` 패턴으로 write 중 crash로 인한 파일 손상을 방지한다.
- **settings.json 백업**: 수정 전 `cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak"` 실행. 병합 실패 시 rollback.
- **기존 `run_cc_install`과의 공존**: `--cc`/`--codex`/`--all` 기존 플래그는 변경 없이 유지. `--hooks` 전용 분기를 별도 `case` 블록으로 추가한다.

## Parallel Execution Metadata

### Ownership
- `scripts/install.sh`

### Shared Surfaces
- `scripts/install.sh` CLI interface — Task 3의 README 작성이 이 인터페이스에 의존

### Conflicts With
- (None identified)

### Parallelizable After
- `000001-010-infra-add-hook-source-assets`

### Task Verify
- `bash scripts/install.sh --list --hooks` — Hook 목록 출력
- `bash scripts/install.sh --hooks --global` — 전체 global 설치
- `bash scripts/install.sh --hooks --global cost-tracker` — 선택 설치
- `jq '.' ~/.claude/settings.json` — 병합 후 유효한 JSON
- `bash scripts/install.sh --hooks --global cost-tracker` (재실행) → settings.json에 중복 항목 없음
- `shellcheck scripts/install.sh`
- `bash scripts/validate.sh`

## Out of Scope

- Hook Script 파일 내용 수정
- Python/uv 자동 설치 (경고만 출력)
- `--hooks --local` 이후 현재 프로젝트의 `.claude/settings.json` 존재 여부 UI — 자동 생성으로 처리
