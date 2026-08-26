# 000012-020-docs-code-gen-contract-first — 구현 체크리스트

## Prerequisites
- [ ] `000012-010-docs-shared-tdd-boundary-contract` 완료 및 reference 존재 확인
- [ ] `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md`의 FR-2, AC2, AC3, AC6, AC7 확인

## Allowed Edit Scope
- `codex/skills/ywc-code-gen/SKILL.md`
- `codex/skills/ywc-code-gen/prompts/implementer-base.md`
- `codex/skills/ywc-code-gen/references/backend-agent.md`
- `codex/skills/ywc-code-gen/references/frontend-agent.md`
- `codex/skills/ywc-code-gen/references/qa-agent.md`
- `codex/skills/ywc-code-gen/evals/evals.json`
- `codex/skills/ywc-code-gen/README.md`
- `codex/skills/ywc-code-gen/README.en.md`
- `codex/skills/ywc-code-gen/README.ja.md`
- `codex/skills/ywc-code-gen/README.ko.md`
- `codex/skills/ywc-code-gen/agents/openai.yaml` (metadata check only)

## Stop Conditions
- Claude Code skill mirror 를 수정해야 할 것 같으면 중단
- `plugins/ywc-agent-toolkit/skills/**` 직접 수정 필요성이 보이면 중단하고 000013로 넘김
- `--tdd` option 을 삭제하거나 기존 invocation contract 를 깨야 할 것 같으면 중단

## Implementation Steps
- [ ] `SKILL.md`에 `codex/skills/references/tdd-deep-module-gray-box.md` 참조 추가
- [ ] 작업 시작 절차에 Contract Snapshot 작성 단계를 추가: Changed Public Contracts, Critical Internals, Cross-Module Impact
- [ ] behavior-changing work 의 기본값을 failing test 또는 existing failing assertion 확인 후 구현으로 명시
- [ ] `--tdd`는 strict red/green/refactor enforcement 로 설명을 좁혀 기본 test-first baseline 과 구분
- [ ] `prompts/implementer-base.md`에 worker payload 가 Contract Snapshot 을 받거나 생성하도록 지시 추가
- [ ] backend/frontend reference 에 public contract 중심 테스트와 deep module boundary 보호 문구 추가
- [ ] qa reference 에 changed public contracts, critical internals, gray-box coverage 검토 문구 추가
- [ ] `evals/evals.json`에 contract-first/test-first/deep-module/gray-box 기대치를 검증하는 trigger case 또는 rubric 문구 반영
- [ ] README 4종에 contract-first/test-first baseline 과 `--tdd`의 strict 의미를 간결히 반영

## Task Verify
- [ ] `rg -n "Contract Snapshot|TDD Mode|Changed Public Contracts|Critical Internals|tdd-deep-module-gray-box" codex/skills/ywc-code-gen`
- [ ] `python3 -m json.tool codex/skills/ywc-code-gen/evals/evals.json >/dev/null`

## Verification
- [ ] `bash scripts/validate.sh` 통과
- [ ] `git diff --name-only`에 `claude-code/` 경로가 없음
