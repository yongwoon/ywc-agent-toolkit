# 000045-020-docs-iac-author-skill

## Purpose
실장 오케스트레이터 `ywc-iac-author` 스킬을 저작한다. 설계 입력→Terraform 모듈 작성→plan→blast-radius 요약. ywc-cloud-engineer로 fan-out.

## Scope
- `claude-code/skills/ywc-iac-author/SKILL.md` + `README.md`/`README.en.md`/`README.ja.md`/`README.ko.md`
- `codex/skills/ywc-iac-author/SKILL.md`(frontmatter는 name+description만) + Tier1 README 4종 + `agents/openai.yaml`
- 공유 references 링크(providers/iac-tools/lenses)

## Spec Reference
### Primary Sources
- `docs/ywc-plans/infra-skill-suite-design.md` §2.2 (ywc-iac-author)
### Summary
Terraform 단일 고정(§7), 프로바이더 4종은 공유 references 링크. description은 KR/EN/JP 트리거 + "Do not use for" anti-trigger(§5 매트릭스) 포함.
### Out of Scope (from spec)
§5 anti-trigger 매트릭스에 명시된 인접 스킬 영역.

## Criticality
normal

## Dependencies
- **Depends On**: `000044-010`(dispatch 워커), `000044-020`(공유 refs)
- **Depended By**: `000046-010-infra-codex-plugin-sync-validate`

## Key Files
- `claude-code/skills/ywc-iac-author/SKILL.md` 및 README 4종
- `codex/skills/ywc-iac-author/SKILL.md`, `codex/skills/ywc-iac-author/agents/openai.yaml` 및 README 4종

## Notes
- Codex SKILL.md는 `category|phase|requires|advisor_budget|allowed tools` frontmatter 금지(validate.sh:88).
- 다른 스킬을 `@skill-name`으로 force-load 금지 — 이름으로만 참조.

## Out of Scope
- 공유 references 저작(044-020). 본 태스크는 링크만.

## Parallel Execution Metadata
- **Ownership**: `claude-code/skills/ywc-iac-author/**`, `codex/skills/ywc-iac-author/**`
- **Shared Surfaces**: `codex/skills/references/`, `.codex-plugin/plugin.json`(패키징 태스크가 재생성)
- **Conflicts With**: (None identified)
- **Parallelizable After**: `000044-010`(dispatch 워커), `000044-020`(공유 refs)
- **Task Verify**: `test -f claude-code/skills/ywc-iac-author/SKILL.md && test -f codex/skills/ywc-iac-author/agents/openai.yaml && bash scripts/validate.sh`
