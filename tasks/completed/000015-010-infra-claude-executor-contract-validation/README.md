# 000015-010-infra-claude-executor-contract-validation

## Purpose

Phase 000014의 모든 변경(shared reference + 3개 skill + README locale)이 끝난 뒤, claude-code 전용 경계와 저장소 검증을 수행한다: `ywc-skill-author` 규칙 적합성, `bash scripts/validate.sh` 통과, `bash scripts/install.sh --list --cc` 동작, `README*.md` markdownlint, 그리고 diff에 `codex/`·`plugins/` 경로가 없음 확인 (FR-6, AC7, AC8, AC9).

## Scope

- 저장소 검증 실행 및 결과 보고
- claude-code-only boundary 확인(`git diff --name-only`)
- 검증 실패 시 최소 수정(검증을 통과시키기 위한 수정에 한함)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md` — FR-6, AC7, AC8, AC9

### Summary
이 task는 hard gate다. Phase 000014의 4개 task가 모두 머지된 뒤에만 의미가 있다. 검증은 install scan + `validate.sh` + markdownlint이며, claude-code-only 경계를 명시적으로 확인한다. claude-code 변경은 codex sync가 불필요하나, `validate.sh`가 plugin drift를 보고하면 직접 수정하지 않고 별도 결정으로 surface한다.

### Out of Scope (from spec)
- 새 기능 추가, skill 내용 재설계.
- `plugins/**` 직접 편집(생성물).

## Dependencies

### Depends On
- `000014-010-docs-shared-tdd-boundary-contract` — shared reference 존재/링크
- `000014-020-docs-code-gen-red-gate-deep-module` — code-gen 변경
- `000014-030-docs-sequential-executor-test-first` — sequential 변경
- `000014-040-docs-parallel-executor-contract-gates` — parallel 변경

### Depended By
- (없음) — 배치의 최종 검증 task

## Key Files
- (편집 없음 — 검증 전용) 필요 시 검증 실패 보정 한정

## Notes
- AC8(`ywc-skill-author` 경유)은 diff만으로 검증이 어려운 process AC다. 산출물 적합성(frontmatter, Rationalization rows, reference link)이 `validate.sh`를 통과하는지를 관측 가능한 proxy로 사용한다(spec-validate Suggestion 반영).

## Out of Scope
- skill 내용 변경, codex/plugins 편집.

## Parallel Execution Metadata
- **Ownership:** (검증 전용 — 소스 편집 없음; 보정이 필요하면 해당 skill의 Ownership을 재확인)
- **Shared Surfaces:** 저장소 전체 validation
- **Conflicts With:** Phase 000014 전 task(완료 후에만 실행)
- **Parallelizable After:** `000014-010`, `000014-020`, `000014-030`, `000014-040` (전부 머지)
- **Task Verify:**
  - `bash scripts/install.sh --list --cc`
  - `bash scripts/validate.sh`
  - `git diff --name-only | grep -E '^(codex|plugins)/' && exit 1 || echo "OK: claude-code-only"`
