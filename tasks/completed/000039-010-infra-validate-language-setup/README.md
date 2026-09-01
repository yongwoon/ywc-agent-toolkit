# 000039-010-infra-validate-language-setup

## Purpose

언어 setup 기능 전체를 CI 기준으로 검증한다. 새 `ywc-setup-language` skill 구조/README locale set, `--list` 노출, consumer wiring 을 확인하고 `scripts/validate.sh` 를 통과시킨다.

## Scope

- **포함**: `bash scripts/validate.sh` 실행 및 통과; 새 skill 이 Tier 1 README locale set + frontmatter 검증 통과; `install.sh --list --cc` 에 노출; consumer 5종이 `language-resolution.md` 를 참조하는지 최종 확인.
- 파일 편집은 없음(검증 전용). 결함 발견 시 해당 task 로 회귀 보고.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/ywc-language-setup.md` — AC11, AC12, NFR1, FR8.

### Summary
AC11: `bash scripts/validate.sh` 가 새 skill 을 통과시킨다(frontmatter + `.md`/`.en`/`.ja`/`.ko` Tier 1 + 생성 Tier 2). 이 task 는 모든 산출물이 CI 기준을 만족하는지 확인하는 최종 gate 이며, 결함은 원인 task 로 회귀시킨다.

### Out of Scope (from spec)
- 기능 구현(선행 task 담당). 이 task 는 검증만.

## Criticality
`normal`.

## Dependencies

### Depends On
- `000038-010-docs-ywc-setup-language-skill` — 검증 대상 skill 존재.
- `000038-020-docs-wire-doc-generator-consumers` — consumer wiring 확인.
- `000038-030-docs-wire-git-artifact-consumers` — consumer wiring 확인.

### Depended By
- (없음) — 최종 task.

## Key Files
- (편집 없음) — 검증 전용. 대상: `claude-code/skills/ywc-setup-language/**`, consumer 5종 SKILL.md, `claude-code/skills/references/language-resolution.md`.

## Notes
- 파일을 편집하지 않으므로 다른 어떤 task 와도 병렬 편집 충돌 없음. 단, 선행 build task 가 모두 merge 된 뒤 실행해야 의미가 있다(hard gate).
- validate.sh 실패 시 원인을 해당 build task 로 회귀 — 이 task 안에서 기능을 고치지 않는다.

## Out of Scope
- 기능/문서 수정.

## Parallel Execution Metadata
- **Ownership**: (편집 없음) — 검증 전용.
- **Shared Surfaces**: 없음.
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000038-010`, `000038-020`, `000038-030` 모두 완료.
- **Task Verify**:
  - `bash scripts/validate.sh`
  - `bash scripts/install.sh --list --cc | grep -q ywc-setup-language`
  - `for s in ywc-task-generator ywc-spec-writer ywc-plan ywc-create-pr ywc-commit; do grep -q "language-resolution.md" claude-code/skills/$s/SKILL.md || echo "unwired: $s"; done`
  - `grep -q "## Language Resolution" claude-code/skills/CLAUDE.md`
