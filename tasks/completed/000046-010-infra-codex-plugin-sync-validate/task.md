# task: 000046-010-infra-codex-plugin-sync-validate

## Prerequisites
- [ ] `000045-010`~`000045-050` 전부 완료(모든 스킬·에이전트 저작 완료)

## Allowed Edit Scope
`plugins/ywc-agent-toolkit/**`, `.codex-plugin/plugin.json` (스크립트 생성물). 스킬 원본은 수정하지 않음.

## Stop Conditions
- validate.sh가 스킬/에이전트 내용 오류를 보고하면 중단하고 해당 스킬 태스크로 회부.

## Implementation Steps
- [ ] `bash scripts/sync-codex-plugin.sh` 실행하여 `plugins/ywc-agent-toolkit/` 미러 + `.codex-plugin/plugin.json` 재생성
- [ ] `bash scripts/validate.sh` 실행, 실패 항목 해소(단, 원본 스킬 결함은 선행 태스크로 회부)
- [ ] markdownlint(CI 설정 준수) 로컬 확인
- [ ] `bash scripts/install.sh --list --cc` / `--codex`로 신규 스킬 5종 노출 확인

## Task Verify
- [ ] `bash scripts/validate.sh` exit 0
- [ ] `bash scripts/install.sh --list --cc | grep -E 'ywc-iac-author|ywc-infra-design|ywc-infra-review|ywc-infra-optimize'`

## Verification
- [ ] `bash scripts/validate.sh` exit 0
- [ ] markdownlint 통과
