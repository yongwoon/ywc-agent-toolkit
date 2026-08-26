# 000012-010-docs-shared-tdd-boundary-contract — 구현 체크리스트

## Prerequisites
- [ ] `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md`의 FR-1, AC1, AC4, AC6, AC7 확인
- [ ] `codex/skills/references/readable-code.md`, `codex/skills/references/principles.md`, `codex/skills/references/confidence-gate.md`가 존재하는지 확인

## Allowed Edit Scope
- `codex/skills/references/tdd-deep-module-gray-box.md`

## Stop Conditions
- Claude Code 경로(`claude-code/**`)를 수정해야 할 것 같으면 중단하고 보고
- `plugins/ywc-agent-toolkit/skills/**`를 직접 수정해야 할 것 같으면 중단하고 000013로 넘김
- Reference 가 특정 스킬 전용 prompt 로 변질되면 중단하고 공통 규칙으로 축소

## Implementation Steps
- [ ] `codex/skills/references/tdd-deep-module-gray-box.md`를 생성
- [ ] "Contract Snapshot" 섹션 추가: Changed Public Contracts, Critical Internals, Cross-Module Impact 항목 정의
- [ ] "TDD Baseline" 섹션 추가: behavior-changing work 는 failing test 또는 existing failing assertion 확인 후 구현하도록 명시
- [ ] "Allowed Exceptions" 섹션 추가: docs-only, mechanical rename, no practical test harness, explicit user override
- [ ] "Deep Module Boundary" 섹션 추가: public behavior 중심 테스트, internal churn 최소화, module boundary protection
- [ ] "Gray Box Reporting" 섹션 추가: 내부 구현을 읽되 최종 검증/보고는 contract 중심으로 정리
- [ ] 기존 reference 와의 관계를 짧게 명시하고 중복되는 일반 원칙은 링크/참조 수준으로 유지

## Task Verify
- [ ] `test -f codex/skills/references/tdd-deep-module-gray-box.md`
- [ ] `rg -n "Contract Snapshot|TDD Baseline|Allowed Exceptions|Deep Module|Gray Box|Critical Internals|Changed Public Contracts" codex/skills/references/tdd-deep-module-gray-box.md`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `git diff --name-only`에 `claude-code/` 경로가 없음
