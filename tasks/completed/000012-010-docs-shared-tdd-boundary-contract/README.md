# 000012-010-docs-shared-tdd-boundary-contract

## Purpose
Codex executor 계열 스킬이 공통으로 참조할 TDD, deep module, gray-box contract reference 를 추가한다. 이 reference 는 Matt Pocock pitfalls 3/4/5 대응을 한 곳에 고정하여 세 스킬의 지침이 서로 엇갈리지 않게 한다(FR-1, AC1, AC4, AC6, AC7).

## Scope
- `codex/skills/references/tdd-deep-module-gray-box.md` 신규 작성
- test-first 기본값, 허용 예외, 예외 보고 형식 정의
- deep module 기준: public contract 집중, internal churn 방지, module boundary 보호
- gray-box 기준: Critical Internals 정의, changed public contracts 보고, cross-module impact 기록
- 기존 reference 인 `readable-code.md`, `principles.md`, `confidence-gate.md`와 충돌하지 않도록 연결 문맥 정리

## Spec Reference
### Primary Sources
- `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md` — FR-1, AC1, AC4, AC6, AC7

### Summary
세 대상 스킬이 반복해서 써야 하는 contract-first/test-first/deep-module/gray-box 용어를 shared reference 로 고정한다. 이 작업은 후속 skill 업데이트의 선행 조건이며, 후속 작업은 이 reference 를 링크하거나 그 핵심 규칙을 요약해야 한다.

### Out of Scope (from spec)
- Claude Code skill 수정
- `plugins/ywc-agent-toolkit/skills/**` 직접 hand-edit
- 실제 product code 또는 test code 구현

## Dependencies
### Depends On
- (없음) — Batch 4 root task

### Depended By
- `000012-020-docs-code-gen-contract-first`
- `000012-030-docs-sequential-executor-test-first`
- `000012-040-docs-parallel-executor-contract-gates`
- `000013-010-infra-codex-executor-contract-validation`

## Key Files
- `codex/skills/references/tdd-deep-module-gray-box.md`

## Notes
- Reference 는 executor prompt 에 그대로 인용 가능한 짧은 checklist 중심으로 작성한다.
- "항상 테스트 작성" 같은 절대 규칙 대신 behavior-changing work 의 baseline 을 test-first 로 두고, docs-only/mechanical/no-test-harness 예외를 명시한다.
- Internal inspection 은 허용하되, 테스트와 보고는 public behavior / stable boundary 중심으로 유도한다.

## Out of Scope
- 세 대상 스킬의 `SKILL.md`, README, eval 수정(후속 task 소관)
- generated plugin sync(000013 소관)

## Parallel Execution Metadata
- **Ownership:** `codex/skills/references/tdd-deep-module-gray-box.md`
- **Shared Surfaces:** Codex shared reference contract for TDD / deep module / gray-box guidance
- **Conflicts With:** (None identified)
- **Parallelizable After:** (없음 — 즉시 실행 가능)
- **Task Verify:**
  - `test -f codex/skills/references/tdd-deep-module-gray-box.md`
  - `rg -n "TDD|Deep Module|Gray Box|Critical Internals|Changed Public Contracts" codex/skills/references/tdd-deep-module-gray-box.md`
  - `bash scripts/validate.sh`
