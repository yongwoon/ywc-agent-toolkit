# 000012-030-docs-sequential-executor-test-first — 구현 체크리스트

## Prerequisites
- [ ] `000012-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md`의 FR-3, AC3, AC4, AC6, AC7 확인

## Allowed Edit Scope
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/evals/evals.json`
- `codex/skills/ywc-sequential-executor/README.md`
- `codex/skills/ywc-sequential-executor/README.en.md`
- `codex/skills/ywc-sequential-executor/README.ja.md`
- `codex/skills/ywc-sequential-executor/README.ko.md`
- `codex/skills/ywc-sequential-executor/agents/openai.yaml` (metadata check only)

## Stop Conditions
- Parallel executor 또는 code-gen 파일까지 수정해야 해결될 것 같으면 중단하고 dependency graph 확인
- User task 의 기존 verification contract 를 약화해야 할 것 같으면 중단
- TDD 예외가 무제한 허용처럼 읽히면 중단하고 예외 조건을 좁힘

## Implementation Steps
- [ ] `SKILL.md`에 shared reference 링크 또는 요약 추가
- [ ] task 실행 전 changed public contracts / critical internals / cross-module impact 확인 단계를 추가
- [ ] behavior-changing implementation step 은 failing test 작성 또는 existing failing assertion 확인을 먼저 수행하도록 명시
- [ ] docs-only, mechanical, no practical harness, explicit user override 예외와 예외 보고 형식 추가
- [ ] Deep module guidance 추가: public behavior 중심 테스트, 내부 구조 고정 테스트 남발 금지
- [ ] Final report 또는 verification report 형식에 Changed Public Contracts, Critical Internals, TDD Exceptions 항목 추가
- [ ] `evals/evals.json`에 sequential executor 가 test-first/contract report 를 요구하는지 검증하는 case 반영
- [ ] README 4종에 test-first baseline 과 gray-box reporting 을 사용자 관점으로 요약

## Task Verify
- [ ] `rg -n "failing test|contract test|Changed Public Contracts|Critical Internals|TDD Exceptions|tdd-deep-module-gray-box" codex/skills/ywc-sequential-executor`
- [ ] `python3 -m json.tool codex/skills/ywc-sequential-executor/evals/evals.json >/dev/null`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `git diff --name-only`에 `claude-code/` 경로가 없음
