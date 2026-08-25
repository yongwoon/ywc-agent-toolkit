# 000031-020-docs-task-generator-codex-zh-es — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`에서 `ywc-task-generator` section을 읽습니다.
- [ ] 현재 `codex/skills/ywc-task-generator/SKILL.md`의 language contract를 확인합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-task-generator/**` 안에서만 수정합니다.
- [ ] generated plugin mirror와 `claude-code/**`는 수정하지 않습니다.

## Stop Conditions

- [ ] `--lang` 확장이 granularity, numbering, dependency graph semantics를 바꾸어야 한다면 중단합니다.
- [ ] `README.zh.md` / `README.es.md` required validation 정책 변경이 필요하면 중단합니다.
- [ ] task output template의 YAML/Markdown machine structure를 localize해야 한다고 판단되면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. Eval fixture와 validation으로 대체합니다.
- [ ] Interface contract를 `--lang` option 및 language-policy reference에 명시합니다.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-task-generator/SKILL.md`의 Arguments table을 확장합니다.
  - [ ] `korean|japanese|english`에 `chinese|spanish`를 추가합니다.
  - [ ] `zh|es` code aliases를 accepted values로 문서화합니다.
  - [ ] Step 4 prompt에 Chinese/Spanish 선택지를 추가합니다.
- [ ] `references/language-policy.md`를 갱신합니다.
  - [ ] Supported languages에 Chinese/Spanish를 추가합니다.
  - [ ] Chinese (Simplified)와 Spanish writing rules를 추가합니다.
  - [ ] Technical terms 유지 예시를 포함합니다.
- [ ] README locale set을 갱신합니다.
  - [ ] `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`
  - [ ] Codex syntax는 `$ywc-task-generator`로 유지합니다.
- [ ] `agents/openai.yaml`에서 supported language summary가 stale하지 않도록 수정합니다.
- [ ] `evals/evals.json`에 Chinese와 Spanish task generation cases를 추가합니다.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-task-generator`
- [ ] `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
- [ ] `rg -n "korean \\| japanese \\| english|korean/japanese/english" codex/skills/ywc-task-generator` 결과를 확인하고 3-language-only wording을 갱신합니다.
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 `codex/skills/ywc-task-generator/**`에만 있는지 확인합니다.
