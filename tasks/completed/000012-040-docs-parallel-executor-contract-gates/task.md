# 000012-040-docs-parallel-executor-contract-gates — 구현 체크리스트

## Prerequisites
- [ ] `000012-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md`의 FR-4, AC3, AC5, AC6, AC7 확인

## Allowed Edit Scope
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/evals/evals.json`
- `codex/skills/ywc-parallel-executor/README.md`
- `codex/skills/ywc-parallel-executor/README.en.md`
- `codex/skills/ywc-parallel-executor/README.ja.md`
- `codex/skills/ywc-parallel-executor/README.ko.md`
- `codex/skills/ywc-parallel-executor/agents/openai.yaml` (metadata check only)

## Stop Conditions
- Parallel scheduling 의 기존 ownership/isolation 안전장치를 약화해야 할 것 같으면 중단
- Worker payload 가 너무 길어져 실제 subagent 지시로 쓰기 어렵다면 중단하고 checklist 를 축약
- Generated plugin package 를 직접 고쳐야 할 것 같으면 중단하고 000013로 넘김

## Implementation Steps
- [ ] `SKILL.md`에 shared reference 링크 또는 요약 추가
- [ ] worker dispatch payload 에 Changed Public Contracts, Critical Internals, Cross-Module Impact 항목 추가
- [ ] behavior-changing task 는 worker 가 failing test 또는 existing failing assertion 을 먼저 확인하도록 명시
- [ ] Worker completion evidence 에 tests authored, tests executed, TDD exceptions 를 포함
- [ ] Parallel conflict detection 에 shared public contract 변경 가능성을 Shared Surfaces signal 로 추가
- [ ] Wave aggregation/final report 에 per-task contract evidence 를 모으는 항목 추가
- [ ] Deep module guidance 추가: internal-only tests 로 module boundary 를 깨지 않도록 경고
- [ ] `evals/evals.json`에 worker-level contract gate 와 aggregation evidence 를 검증하는 case 반영
- [ ] README 4종에 parallel contract gates 와 test evidence reporting 을 사용자 관점으로 요약

## Task Verify
- [ ] `rg -n "shared contract|Contract|failing test|authored|Critical Internals|TDD Exceptions|tdd-deep-module-gray-box" codex/skills/ywc-parallel-executor`
- [ ] `python3 -m json.tool codex/skills/ywc-parallel-executor/evals/evals.json >/dev/null`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `git diff --name-only`에 `claude-code/` 경로가 없음
