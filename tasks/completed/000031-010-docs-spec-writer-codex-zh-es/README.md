# 000031-010-docs-spec-writer-codex-zh-es

## Purpose

Codex `ywc-spec-writer`가 기존 `ko|ja|en` 외에 Simplified Chinese(`zh`)와 Spanish(`es`) spec 출력을 지원하도록 확장합니다. `ywc-project-docs`의 5-language 지원을 기준으로 삼되, 이 skill의 기존 `ko` default와 spec-writing workflow는 유지합니다.

## Scope

- `codex/skills/ywc-spec-writer/SKILL.md`의 `--lang` 계약을 `ko|ja|en|zh|es`로 확장합니다.
- `codex/skills/ywc-spec-writer/references/language-policy.md`에 Chinese (Simplified)와 Spanish writing policy를 추가합니다.
- `README*.md`, `agents/openai.yaml`, `evals/evals.json`의 supported-language wording과 예시를 갱신합니다.
- `--lang zh`와 `--lang es` Codex eval fixture를 추가합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#fr-2-update-content-output-skills` — `ywc-spec-writer`의 Codex source 변경 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#fr-1-establish-a-canonical-language-code-policy` — language code와 alias 정책.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#out-of-scope` — `claude-code/**`, `ywc-project-docs`, 새 translation infrastructure 제외.

### Summary

이 task는 Codex `ywc-spec-writer` 하나만 담당합니다. Spec body prose는 선택한 language를 따르고, command, file path, code block, JSON/YAML key, Technical terms는 English를 유지합니다. 기존 default인 Korean(`ko`)은 변경하지 않습니다.

### Out of Scope (from spec)

- `claude-code/**` 변경 — 전체 spec의 Out of Scope.
- `codex/skills/ywc-project-docs/**` 변경 — reference implementation이므로 제외.
- Codex plugin mirror 직접 수정 — `000032-010-infra-codex-plugin-sync-validation`에서 sync로 생성.
- Workflow PR language skills — `000031-040`, `000031-050`, `000031-060`에서 처리.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — source 변경 후 plugin sync와 full validation을 수행합니다.

## Key Files

- `codex/skills/ywc-spec-writer/SKILL.md` — `--lang` contract, description, validation checklist.
- `codex/skills/ywc-spec-writer/references/language-policy.md` — zh/es language policy.
- `codex/skills/ywc-spec-writer/README.md`
- `codex/skills/ywc-spec-writer/README.en.md`
- `codex/skills/ywc-spec-writer/README.ja.md`
- `codex/skills/ywc-spec-writer/README.ko.md`
- `codex/skills/ywc-spec-writer/README.zh.md`
- `codex/skills/ywc-spec-writer/README.es.md`
- `codex/skills/ywc-spec-writer/agents/openai.yaml`
- `codex/skills/ywc-spec-writer/evals/evals.json`

## Notes

- 기존 `ko` code convention을 유지합니다. `kr`로 바꾸지 않습니다.
- `Codex SKILL.md` frontmatter는 `name`과 `description`만 유지해야 합니다.
- README locale prose는 각 locale로 작성하되 Technical terms는 English로 유지합니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs/skill-definition maintenance입니다. 대신 targeted grep, JSON validation, skill validation, full repository validation으로 검증합니다.

### Interface Contract

- Contract: `ywc-spec-writer --lang ko|ja|en|zh|es`
- Inputs: spec-writing invocation with optional `--lang`.
- Outputs: localized `docs/specification/` markdown.
- Error model: unsupported/ambiguous language는 기존 clarification/default behavior를 따릅니다.
- Impacted tests: `codex/skills/ywc-spec-writer/evals/evals.json`

### Critical Surface Review

- Review requirement: N/A — auth, permission, billing, data migration, data deletion, security surface 없음.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-spec-writer/**`

### Shared Surfaces

- `codex/skills/ywc-spec-writer/evals/evals.json`
- `agents/openai.yaml` metadata surface
- `scripts/validate.sh` read-only validation gate

### Conflicts With

- (None identified) — sibling tasks own disjoint skill directories.

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-spec-writer`
- `python3 -m json.tool codex/skills/ywc-spec-writer/evals/evals.json >/dev/null`
- `rg -n "ko\\|ja\\|en|Korean, Japanese, and English|Supports Korean, Japanese, and English" codex/skills/ywc-spec-writer`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- `codex/skills/ywc-task-generator/**`, `codex/skills/ywc-gen-testcase/**`, PR workflow skills.
- `plugins/ywc-agent-toolkit/skills/**` generated mirror edits.
- `README.zh.md` / `README.es.md` mandatory validation rule changes.
