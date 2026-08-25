# 000014-040-docs-parallel-executor-contract-gates

## Purpose

`ywc-parallel-executor` (Claude Code)에 함정 3/4/5 처방을 반영한다: Rationalization Defense에 TDD/headlights row + deep-module row 추가, Step 4b worker payload에 interface-first directive + test-first-where-feasible directive 추가, Step 4d/4e에서 critical-path task에 대해 `/ywc-impl-review` + `/ywc-security-audit` 자동 에스컬레이션, Completion Report에 per-wave changed contracts + critical-module 노트 추가 (FR-4, FR-5, AC4, AC5).

## Scope

- `SKILL.md` 편집(Rationalization rows, Step 4b worker directives, Step 4d/4e critical 에스컬레이션, Completion Report 필드)
- README locale set 갱신(md/en/ja/ko/es/zh)
- 모든 구조 편집은 `ywc-skill-author` 경유

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md` — FR-4, FR-5, AC4, AC5
- `claude-code/skills/references/tdd-deep-module-gray-box.md` — 000014-010 산출물

### Summary
worker payload에 interface-first + test-first directive를 주입하고, 동일 wave에서 공유 public surface를 다루는 task는 dispatch 전 contract를 정의(또는 직렬화)한다. critical-path task는 4d review + `/ywc-security-audit`를 4e delivery 전 강제한다. 일반 task는 gray-box 검증 유지.

### Out of Scope (from spec)
- code-gen / sequential-executor 편집은 별도 task 소관.
- wave/worktree/Docker/merge lifecycle 변경 없음(새 게이트 보고 목적 외).
- `codex/skills/**`, `plugins/**` 미수정.

## Dependencies

### Depends On
- `000014-010-docs-shared-tdd-boundary-contract` — 공유 reference 링크 대상

### Depended By
- `000015-010-infra-claude-executor-contract-validation` — validation/boundary 검증

## Key Files
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/README.md` / `README.en.md` / `README.ja.md` / `README.ko.md` / `README.es.md` / `README.zh.md`

## Notes
- worker payload directive는 기존 verbatim directive(Question-First / Completeness / Simplicity+Surgical) 형식과 일관되게 추가한다.
- critical-path 판정은 task Ownership(구현 전) 기준 — 공유 reference에 명시된 시점 규칙 따름.

## Out of Scope
- 다른 executor/generator 편집, codex/plugins 편집, wave/worktree 재설계.

## Parallel Execution Metadata
- **Ownership:** `claude-code/skills/ywc-parallel-executor/SKILL.md`, `claude-code/skills/ywc-parallel-executor/README*.md`
- **Shared Surfaces:** 공유 reference(read-only link); worker payload directive 형식; README localization
- **Conflicts With:** (None identified) — 020/030과 disjoint 디렉터리
- **Parallelizable After:** `000014-010`
- **Task Verify:**
  - `rg -n "interface-first|test-first|headlights|ywc-security-audit|tdd-deep-module-gray-box" claude-code/skills/ywc-parallel-executor/SKILL.md`
