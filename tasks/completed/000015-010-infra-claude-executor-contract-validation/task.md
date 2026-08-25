# 000015-010-infra-claude-executor-contract-validation — 구현 체크리스트

## Prerequisites
- [ ] Phase 000014의 4개 task(`-010`/`-020`/`-030`/`-040`) 모두 완료/머지 확인
- [ ] `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`의 FR-6, AC7/AC8/AC9 확인

## Allowed Edit Scope
- 검증 전용 — 소스 편집 없음
- 검증 실패 보정이 필요한 경우에 한해 해당 skill 디렉터리 내 최소 수정(범위를 초과하면 중단하고 해당 task로 회신)

## Stop Conditions
- `validate.sh`가 `plugins/` drift를 보고하면 직접 수정하지 말고 surface 후 중단(별도 결정)
- 보정이 단순 검증 통과를 넘어 기능 변경으로 번지면 중단
- `codex/skills/**` 수정이 필요해 보이면 중단

## Implementation Steps
- [ ] `bash scripts/install.sh --list --cc` 실행, claude-code skill 목록 정상 출력 확인
- [ ] `bash scripts/validate.sh` 실행, exit 0 확인(실패 시 원인별 최소 보정 후 재실행)
- [ ] `README*.md` markdownlint 통과 확인(`.github/workflows/markdownlint.yml` 기준)
- [ ] claude-code-only 경계 확인: `git diff --name-only`에 `codex/`·`plugins/` 경로가 없음
- [ ] shared reference 링크가 3개 skill에서 실제로 참조되는지 확인(AC1/AC4 산출물 점검)
- [ ] 검증 결과를 Completion Report로 요약(통과/실패 항목, 보정 내역)

## Task Verify
- [ ] `bash scripts/install.sh --list --cc`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --name-only | grep -E '^(codex|plugins)/' && exit 1 || echo "OK: claude-code-only"`
- [ ] `rg -l "tdd-deep-module-gray-box" claude-code/skills/ywc-code-gen claude-code/skills/ywc-sequential-executor claude-code/skills/ywc-parallel-executor`

## Verification
- [ ] 위 Task Verify 전 항목 통과
- [ ] Completion Report에 claude-code-only 경계 확인 결과 포함
