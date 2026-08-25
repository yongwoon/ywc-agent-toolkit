# 000018-010-docs-principles-foundation

## Purpose

공유 SoT `claude-code/skills/references/principles.md`에 Karpathy 4대 규율을 명명하는 운영 하위절을 추가한다. 이후 모든 per-skill 편집이 인용할 수 있는 표준 원칙 이름(Assumption & Ambiguity Discipline, Goal-Driven Execution)을 확립하는 foundation 태스크다.

## Scope

- FR-1: `principles.md`에 Assumption & Ambiguity Discipline, Goal-Driven Execution 절 추가.
- Simplicity는 `readable-code.md`, test-first는 `tdd-deep-module-gray-box.md`를 명시적으로 가리키도록 연결.
- §A9: 'Simplicity First' 한 기둥이 spec-validate에서는 Simplicity, code-gen에서는 Minimalism, 한국어로는 과설계로 불린다는 명명 정합 노트 1줄.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-1 — 추가할 두 절의 내용
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §Iteration 1 Amendments §A9 — 용어 명명 정합 노트
- `claude-code/skills/references/principles.md:15,28,54,66` — 기존 §2 계층/§3 Evidence/§5 Scope/§6 Failure (보존 대상)
- `docs/ywc-plans/codex-karpathy-guideline-integration.md` FR-1 — 선례(미러링 대상)

### Summary

기존 principles.md의 §2 Principle Hierarchy(Safety/Evidence/Scope/Reuse/Clarity/Efficiency)를 대체하지 않고, 짧은 운영 하위절 2개를 추가한다. 새 텍스트는 기존 스타일(짧은 절·직접 규칙·외부 산문 복붙 금지)을 따른다. Simplicity/Surgical/test-first는 각각 readable-code.md / tdd-deep-module-gray-box.md를 가리켜 중복을 피한다.

### Out of Scope (from spec)

- readable-code.md / tdd-deep-module-gray-box.md 본문 수정 — 가리키기만 하고 새 §는 추가하지 않음
- per-skill SKILL.md 편집 — 후속 Phase 000018 태스크가 담당

## Dependencies

### Depends On

- (None — 루트 태스크)

### Depended By

- `000018-020-docs-planning-discipline` — 표준 원칙 이름 인용
- `000018-030-docs-task-generator-goal-evals` — Goal-Driven Execution 원칙 인용
- `000018-040-docs-surgical-simplicity-detection` — Simplicity/Surgical 원칙 인용
- `000018-050-docs-execution-discipline` — Goal-Driven/Surgical 원칙 인용
- `000019-010-infra-karpathy-validation` — 최종 검증

## Key Files

- `claude-code/skills/references/principles.md` — 두 운영 하위절 + §A9 용어 노트 추가

## Notes

- principles.md는 reference이며 README locale set이 없다 → README 동기화 불필요(spec §A7).
- §5 Clarity가 이미 readable-code.md를 가리키는 기존 링크를 활용한다.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/references/principles.md`

### Shared Surfaces

- `공유 SoT: principles.md` — Phase 000018의 다른 태스크가 이 파일을 *읽고 인용*하지만 *편집*하지 않음(이 태스크 전용 편집)

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `rg -n "Assumption|Goal-Driven|NEEDS_CONTEXT|readable-code|tdd-deep-module" claude-code/skills/references/principles.md` — 모든 토큰 반환
- `bash scripts/validate.sh`

## Out of Scope

- 4개 차원 외 다른 principles.md 절의 재작성
- 새 karpathy-* skill 생성
