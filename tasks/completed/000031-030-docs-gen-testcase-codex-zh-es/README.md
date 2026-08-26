# 000031-030-docs-gen-testcase-codex-zh-es

## Purpose

Codex `ywc-gen-testcase`가 testsheet prose language로 Simplified Chinese(`zh`)와 Spanish(`es`)를 지원하도록 확장합니다. YAML front matter keys, section numbers, template skeleton은 기존처럼 English로 유지합니다.

## Scope

- `codex/skills/ywc-gen-testcase/SKILL.md`의 `--lang <code>` table과 language detection/fallback guidance를 `ja,ko,en,zh,es`로 확장합니다.
- README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.
- Chinese/Spanish testsheet prose eval을 추가합니다.
- 필요 시 inline rule로 zh/es prose에서도 Technical terms를 English로 유지하도록 명시합니다.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#ywc-gen-testcase` — testsheet language 요구사항.
- `docs/ywc-plans/ywc-skills-zh-es-language-support.md#edge-cases` — machine-readable sections와 generated plugin diff edge cases.
- `codex/skills/ywc-gen-testcase/SKILL.md` — existing machine-surface English invariant.

### Summary

이 task는 testsheet의 human prose만 localize합니다. Summary, Goal, Steps, Expected, Notes, Edge Cases는 선택 language를 따르지만 YAML key, section number, template skeleton, file name, code snippet은 English 또는 기존 machine syntax를 유지합니다.

### Out of Scope (from spec)

- `references/language-policy.md` 신설.
- `claude-code/**` 변경.
- `ywc-project-docs` 변경.
- Plugin mirror 직접 수정.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000032-010-infra-codex-plugin-sync-validation` — final sync/validation.

## Key Files

- `codex/skills/ywc-gen-testcase/SKILL.md`
- `codex/skills/ywc-gen-testcase/README.md`
- `codex/skills/ywc-gen-testcase/README.en.md`
- `codex/skills/ywc-gen-testcase/README.ja.md`
- `codex/skills/ywc-gen-testcase/README.ko.md`
- `codex/skills/ywc-gen-testcase/README.zh.md`
- `codex/skills/ywc-gen-testcase/README.es.md`
- `codex/skills/ywc-gen-testcase/agents/openai.yaml`
- `codex/skills/ywc-gen-testcase/evals/evals.json`

## Notes

- `ja,ko,en` 기존 code convention을 유지하고 `zh,es`만 추가합니다.
- 이 skill은 testsheet output이므로 localized prose 외의 file/schema-like surfaces는 변경하지 않습니다.

## Hardening Evidence

### Test Feedback Path

- Named exception: docs-only / skill-definition maintenance. Eval JSON validation과 targeted grep으로 대체합니다.

### Interface Contract

- Contract: `ywc-gen-testcase --lang ja|ko|en|zh|es`
- Inputs: PR/task/range source and optional `--lang`.
- Outputs: localized human prose in generated testsheet markdown.
- Error model: unsupported language는 existing auto-detect/fallback behavior를 따릅니다.
- Impacted tests: `codex/skills/ywc-gen-testcase/evals/evals.json`

### Critical Surface Review

- Review requirement: N/A.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-gen-testcase/**`

### Shared Surfaces

- `codex/skills/ywc-gen-testcase/evals/evals.json`
- testsheet language contract
- `scripts/validate.sh` read-only validation gate

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-gen-testcase`
- `python3 -m json.tool codex/skills/ywc-gen-testcase/evals/evals.json >/dev/null`
- `rg -n "ja`,`ko`,`en|ja,ko,en|ja \\| ko \\| en" codex/skills/ywc-gen-testcase`
- `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Out of Scope

- Creating a new `references/language-policy.md`.
- Changing testsheet file naming or directory routing.
- Generated plugin mirror edits before `000032-010`.
