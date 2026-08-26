# 000014-010-docs-shared-tdd-boundary-contract

## Purpose

Claude Code 3개 executor/generator skill이 공유할 단일 reference `claude-code/skills/references/tdd-deep-module-gray-box.md`를 신설한다. Matt Pocock 함정 3(TDD/headlights), 함정 4(deep module/interface-first), 함정 5(gray box + critical-module 예외)의 operational contract를 한곳에 담아, 세 skill이 중복 prose 없이 참조하도록 한다 (FR-1, AC1, AC4 일부, AC6/AC7의 reporting contract 근거).

## Scope

- 신규 reference 파일 작성: `claude-code/skills/references/tdd-deep-module-gray-box.md`
- 6개 섹션 구성: When This Applies / Feedback Loop(headlights) / Deep Module Boundary / Gray Box + Critical-Module Exception(canonical critical-path list 포함) / Allowed Exceptions / Reporting Contract
- 기존 shared reference(`readable-code.md`, `principles.md`, `confidence-gate.md`, `subagent-status-actions.md`) 인용 링크 포함

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md` — FR-1, AC1, AC4, AC6, AC7
- `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm/docs/studies/llm/MATT_POCOCK_AI_CODING_PITFALLS.md` — 함정 3/4/5 원문

### Summary
세 skill이 각자 Pocock 개념을 재설명하지 않도록, TDD RED-first loop, deep-module interface-first, gray-box review + critical-module 예외를 하나의 reference로 통합한다. critical-path canonical list(auth/payment/crypto/PII/external-input 등)와 `CLAUDE.md`의 `critical_paths` override 가능성을 명시한다.

### Out of Scope (from spec)
- 개별 skill의 SKILL.md/README 편집은 후속 task(000014-020/030/040)에서 수행한다.
- codex root(`codex/skills/**`) 파일은 건드리지 않는다(별도 codex batch 소관).

## Dependencies

### Depends On
- (root) — 선행 task 없음

### Depended By
- `000014-020-docs-code-gen-red-gate-deep-module` — 이 reference를 link
- `000014-030-docs-sequential-executor-test-first` — 이 reference를 link
- `000014-040-docs-parallel-executor-contract-gates` — 이 reference를 link
- `000015-010-infra-claude-executor-contract-validation` — reference 존재/링크를 검증

## Key Files
- `claude-code/skills/references/tdd-deep-module-gray-box.md` (신규)

## Notes
- codex sibling `codex/skills/references/tdd-deep-module-gray-box.md`와 동일 파일명이나, claude-code root는 독립 유지된다(자동 sync 없음). 내용은 claude-code 맥락(named subagent, `ywc-security-audit` routing)에 맞춘다.
- `readable-code.md` §G anti-dogma guardrail을 인용해 speculative interface 강요를 방지한다.

## Out of Scope
- skill body 편집, README locale 편집, validation 실행.

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/references/tdd-deep-module-gray-box.md`
- **Shared Surfaces:** 후속 3개 skill task가 이 파일을 read-only로 link함(생성 후 안정)
- **Conflicts With:** (None identified)
- **Parallelizable After:** (root)
- **Task Verify:**
  - `test -f claude-code/skills/references/tdd-deep-module-gray-box.md`
  - `rg -n "Critical-Module Exception|Deep Module|headlights|Reporting Contract" claude-code/skills/references/tdd-deep-module-gray-box.md`
