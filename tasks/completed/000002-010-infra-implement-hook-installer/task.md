# 000002-010-infra-implement-hook-installer — Implementation Checklist

## Prerequisites
- [ ] `000001-010-infra-add-hook-source-assets` 완료(merge) 확인
- [ ] `claude-code/hooks/hooks-registry.json` 존재 및 유효성 확인: `jq '.' claude-code/hooks/hooks-registry.json`
- [ ] `jq` 설치 여부 확인: `which jq`

## Allowed Edit Scope
- [ ] `scripts/install.sh` 만 편집
- [ ] 이 범위 밖 편집이 필요한 경우 중단 후 보고

## Stop Conditions
- [ ] `hooks-registry.json`의 키 구조가 README.md 또는 Spec과 다른 경우 — Task 1 확인 후 보고
- [ ] 기존 `--cc`/`--codex`/`--all` 기능 로직 수정이 필요한 경우 — 이 태스크 범위가 아님, 중단
- [ ] settings.json 병합 로직이 `permissions` 블록을 수정하게 되는 경우 — Spec에서 금지, 중단

## Implementation Steps

- [ ] **의존성 사전 확인 함수 추가**
  - [ ] `check_deps()` 함수: `jq` 미설치 시 설치 안내 메시지 + `exit 1`
  - [ ] `uv` 미설치 시 경고 출력 (설치는 계속 진행)

- [ ] **`run_hook_install()` 함수 구현**
  - [ ] `hooks-registry.json`에서 Hook 이름 목록 읽기: `jq -r '.hooks | keys[]' hooks-registry.json`
  - [ ] Hook Script 파일을 대상 디렉토리(`~/.claude/hooks/` 또는 `./.claude/hooks/`)에 복사
  - [ ] `mkdir -p` 로 대상 디렉토리 자동 생성
  - [ ] Manifest 파일(`.ywc-agent-toolkit-hooks.manifest`)에 설치된 Hook 이름 기록
  - [ ] 선택 설치 시: 지정된 Hook만 복사, 없는 이름이면 오류 + 사용 가능 목록 출력

- [ ] **`merge_hook_settings()` 함수 구현**
  - [ ] 대상 `settings.json` 경로 결정 (global: `~/.claude/settings.json`, local: `./.claude/settings.json`)
  - [ ] settings.json 없을 경우 `{"hooks":{}}` 로 신규 생성
  - [ ] 수정 전 `.bak` 백업: `cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak"`
  - [ ] `registry.json`에서 각 Hook의 `command_global`/`command_local`과 `event`, `matcher` 읽기
  - [ ] jq 로 idempotent append:
    - 해당 event 키가 없으면 신규 생성
    - 동일 `command` 문자열이 이미 있으면 skip
    - 없으면 append
  - [ ] atomic write: `jq ... > /tmp/ywc-settings.tmp && mv /tmp/ywc-settings.tmp "$SETTINGS_FILE"`
  - [ ] `cost-tracker`의 multi-event(`PostToolUse`, `Stop`) 처리: 두 event에 각각 등록

- [ ] **CLI 파싱 확장**
  - [ ] `--hooks` 플래그 파싱 추가 (`MODE="hooks"`)
  - [ ] `--global` 플래그 파싱 (기본값)
  - [ ] `--local` 플래그 파싱
  - [ ] `case "$MODE"` 블록에 `hooks)` 분기 추가 → `run_hook_install` + `merge_hook_settings` 호출

- [ ] **`--list --hooks` 지원**
  - [ ] 기존 `--list` 분기에 `--hooks` 서브플래그 처리 추가
  - [ ] `hooks-registry.json`에서 Hook 이름 + description 출력

- [ ] **`usage()` 업데이트**
  - [ ] `--hooks [--global|--local] [hook-name...]` 예시 추가
  - [ ] `--list --hooks` 예시 추가

## Task Verify
- [ ] `bash scripts/install.sh --list --hooks` → 7개 Hook 목록 출력
- [ ] `bash scripts/install.sh --hooks --global` → 전체 global 설치 성공
- [ ] `jq '.hooks' ~/.claude/settings.json` → Hook 항목 존재 확인
- [ ] `bash scripts/install.sh --hooks --global cost-tracker` (재실행) → settings.json에 중복 항목 없음 (`jq '[.hooks.PostToolUse[].hooks[].command] | length'` 비교)
- [ ] `bash scripts/install.sh --hooks --global block-dangerous-commands cost-tracker` → 2개 선택 설치
- [ ] `bash scripts/install.sh --hooks --local session-start` → `./.claude/hooks/session_start.py` 존재 확인
- [ ] `shellcheck scripts/install.sh`
- [ ] `bash scripts/validate.sh`

## Verification
- [ ] `shellcheck scripts/install.sh` 통과
- [ ] `bash scripts/validate.sh` 통과
- [ ] build 없음 (shell-only project)
