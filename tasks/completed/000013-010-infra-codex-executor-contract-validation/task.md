# 000013-010-infra-codex-executor-contract-validation — 구현 체크리스트

## Prerequisites
- [ ] `000012-010-docs-shared-tdd-boundary-contract` 완료
- [ ] `000012-020-docs-code-gen-contract-first` 완료
- [ ] `000012-030-docs-sequential-executor-test-first` 완료
- [ ] `000012-040-docs-parallel-executor-contract-gates` 완료

## Allowed Edit Scope
- `plugins/ywc-agent-toolkit/skills/**` (generated sync output only)
- 검증 실패가 generated output stale 이 아닌 source 문제일 경우 직접 수정하지 말고 owning task 로 반환

## Stop Conditions
- `claude-code/**` 변경이 감지되면 중단하고 보고
- `codex/skills/**` source 를 새로 고쳐야 해결되는 validation failure 가 나오면 해당 Phase 000012 task 로 되돌림
- Sync script 가 예상 외의 대량 unrelated 변경을 만들면 중단하고 diff 를 보고

## Implementation Steps
- [ ] `bash scripts/install.sh --list --codex` 실행
- [ ] `bash scripts/sync-codex-plugin.sh` 존재 여부와 repository convention 확인 후 필요한 경우 실행
- [ ] `bash scripts/validate.sh` 실행
- [ ] `git diff --name-only`로 변경 범위 확인
- [ ] `claude-code/**` 변경이 없는지 확인
- [ ] 최종 보고에 validation 결과와 generated plugin sync 여부를 기록

## Task Verify
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --name-only | rg '^claude-code/'` 결과 없음
- [ ] `git diff --name-only | rg '^codex/skills/(ywc-code-gen|ywc-sequential-executor|ywc-parallel-executor|references)/|^plugins/ywc-agent-toolkit/skills/'`

## Verification
- [ ] Final report 에 AC8 Codex-only, AC9 validation pass 여부 명시
