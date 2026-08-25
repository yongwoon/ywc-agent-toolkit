# 000012-020-docs-code-gen-contract-first

## Purpose
`ywc-code-gen` Codex skill 을 contract-first/test-first 구현 흐름으로 강화한다. 현재 존재하는 Gray Box 및 `--tdd` 옵션을 유지하되, Contract Snapshot 을 실제 절차로 끌어올리고 behavior-changing work 의 기본값을 TDD 로 만든다(FR-2, AC2, AC3, AC6, AC7).

## Scope
- `SKILL.md`에 shared reference 연결 및 Contract Snapshot 절차 추가
- `prompts/implementer-base.md`에 작업 시작 전 contract snapshot, failing test baseline, deep-module boundary 지침 추가
- backend/frontend/qa role reference 에 public contract 중심 테스트와 Critical Internals 보고를 반영
- eval trigger cases 에 contract-first/TDD/deep-module/gray-box 기대치를 추가 또는 갱신
- README locale 파일에 사용자-facing 옵션/동작 요약 갱신

## Spec Reference
### Primary Sources
- `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md` — FR-2, AC2, AC3, AC6, AC7
- `codex/skills/references/tdd-deep-module-gray-box.md` — 000012-010 산출물

### Summary
`ywc-code-gen`은 병렬 code generation의 entry point 이므로 각 worker 가 같은 contract snapshot 을 공유해야 한다. 구현 전 public contract 와 critical internals 를 명시하고, behavior-changing work 는 test-first 를 기본값으로 처리하도록 prompt 와 docs/evals 를 맞춘다.

### Out of Scope (from spec)
- Claude Code mirror 수정
- `ywc-sequential-executor`, `ywc-parallel-executor` 수정
- generated plugin package 직접 수정

## Dependencies
### Depends On
- `000012-010-docs-shared-tdd-boundary-contract`

### Depended By
- `000013-010-infra-codex-executor-contract-validation`

## Key Files
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

## Notes
- Existing `--tdd` option 을 제거하지 말고, option semantics 를 "strict TDD ritual" 쪽으로 명확히 한다.
- 기본 흐름은 "test-first unless exception"이고, `--tdd`는 더 엄격한 red/green/refactor enforcement 로 구분한다.
- README locale 은 구조와 핵심 의미를 맞추되 기계 번역보다 간결한 현지화 설명을 우선한다.

## Out of Scope
- sequential/parallel executor 파일 수정
- 새로운 custom agent 추가
- 실제 app/product 코드 생성

## Parallel Execution Metadata
- **Ownership:** `codex/skills/ywc-code-gen/**`
- **Shared Surfaces:** Codex code-generation worker prompt contract; shared TDD/deep-module/gray-box reference; Codex README localization surface
- **Conflicts With:** (None identified after `000012-010` merges)
- **Parallelizable After:** `000012-010-docs-shared-tdd-boundary-contract`
- **Task Verify:**
  - `rg -n "Contract Snapshot|TDD Mode|Changed Public Contracts|Critical Internals|tdd-deep-module-gray-box" codex/skills/ywc-code-gen`
  - `python3 -m json.tool codex/skills/ywc-code-gen/evals/evals.json >/dev/null`
  - `bash scripts/validate.sh`
