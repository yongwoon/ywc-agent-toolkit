# Task: 000039-010-infra-validate-language-setup

## Prerequisites
- [ ] `000038-010-docs-ywc-setup-language-skill` 완료.
- [ ] `000038-020-docs-wire-doc-generator-consumers` 완료.
- [ ] `000038-030-docs-wire-git-artifact-consumers` 완료.

## Allowed Edit Scope
- (편집 없음) — 검증 전용. 결함은 원인 task 로 회귀 보고.

## Stop Conditions
- `validate.sh` 실패 시 이 task 에서 기능을 수정하지 말고 원인 build task 를 지목해 보고.

## Implementation Steps
- [ ] `bash scripts/validate.sh` 실행 → 통과 확인(새 skill frontmatter + README locale + shellcheck).
- [ ] `bash scripts/install.sh --list --cc` → `ywc-setup-language` 노출 확인.
- [ ] consumer 5종(`ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, `ywc-commit`) 모두 `language-resolution.md` 참조 확인.
- [ ] `claude-code/skills/CLAUDE.md` 에 `## Language Resolution` 섹션 + consumer list 존재 확인(AC12).
- [ ] 새 skill README Tier 2(`.zh`/`.es`) 존재 확인.

## Task Verify
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --cc | grep -q ywc-setup-language`
- [ ] `for s in ywc-task-generator ywc-spec-writer ywc-plan ywc-create-pr ywc-commit; do grep -q "language-resolution.md" claude-code/skills/$s/SKILL.md || echo "unwired: $s"; done`

## Verification
- [ ] `bash scripts/validate.sh` 최종 통과.
- [ ] markdownlint 대상(README) lint 통과.
