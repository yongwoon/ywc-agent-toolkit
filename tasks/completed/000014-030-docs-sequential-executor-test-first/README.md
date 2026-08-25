# 000014-030-docs-sequential-executor-test-first

## Purpose

`ywc-sequential-executor` (Claude Code)에 함정 3/4/5 처방을 반영한다: Step 3.4 test-first 강화(behavior change는 failing test 먼저, bugfix는 실패하는 regression test 먼저, docs/config/mechanical 예외), headlights + trade-off framing, deep-module interface-first subsection, critical-path 감지 시 Step 4.5/5에서 `/ywc-impl-review` + `/ywc-security-audit` 자동 에스컬레이션, Rationalization Defense rows 추가 (FR-3, FR-5, AC4, AC5).

## Scope

- `SKILL.md` 편집(Rationalization rows, Step 3.4, interface-first subsection, Step 4.5/5 critical 에스컬레이션, Completion Report 필드)
- README locale set 갱신(md/en/ja/ko/es/zh)
- 모든 구조 편집은 `ywc-skill-author` 경유

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md` — FR-3, FR-5, AC4, AC5
- `claude-code/skills/references/tdd-deep-module-gray-box.md` — 000014-010 산출물

### Summary
이미 "tests required + TDD preferred"인 skill을 behavior change에 대해 test-first로 강화하고, critical-path task는 `--review` 미지정이어도 `/ywc-impl-review` + `/ywc-security-audit`를 강제한다. 일반 task는 gray-box(interface-level) 검증 유지.

### Out of Scope (from spec)
- code-gen / parallel-executor 편집은 별도 task 소관.
- 기존 branch/PR/CI/merge lifecycle 변경 없음(새 게이트 보고 목적 외).
- `codex/skills/**`, `plugins/**` 미수정.

## Dependencies

### Depends On
- `000014-010-docs-shared-tdd-boundary-contract` — 공유 reference 링크 대상

### Depended By
- `000015-010-infra-claude-executor-contract-validation` — validation/boundary 검증

## Key Files
- `claude-code/skills/ywc-sequential-executor/SKILL.md`
- `claude-code/skills/ywc-sequential-executor/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Notes
- 이 skill에는 `evals/` 디렉터리가 있으나 FR-3는 evals 변경을 요구하지 않는다(필요 시 별도). 본 task의 Ownership은 SKILL.md + README로 한정.
- critical-path 판정은 task의 Ownership(구현 전) 기준 — code-gen의 생성 후 판정과 시점이 다름(공유 reference에 명시).

## Out of Scope
- 다른 executor/generator 편집, codex/plugins 편집, lifecycle 재설계.

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/ywc-sequential-executor/SKILL.md`, `claude-code/skills/ywc-sequential-executor/README*.md`
- **Shared Surfaces:** 공유 reference(read-only link); README localization
- **Conflicts With:** (None identified) — 020/040과 disjoint 디렉터리
- **Parallelizable After:** `000014-010`
- **Task Verify:**
  - `rg -n "headlights|test-first|interface-first|ywc-security-audit|tdd-deep-module-gray-box" claude-code/skills/ywc-sequential-executor/SKILL.md`
