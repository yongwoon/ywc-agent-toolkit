# 000031-010-docs-spec-writer-codex-zh-es — Implementation Checklist

## Prerequisites

- [ ] Base branch에 기존 `000030-*` Claude task 변경이 있더라도 이 task와 Ownership이 겹치지 않는지 확인합니다.
- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`를 읽고 Codex-only boundary를 확인합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-spec-writer/**` 안에서만 수정합니다.
- [ ] `claude-code/**` 또는 `plugins/ywc-agent-toolkit/skills/**` 수정이 필요해 보이면 중단하고 보고합니다.

## Stop Conditions

- [ ] `Codex SKILL.md` frontmatter에 `version`, `category`, `requires` 같은 Claude-only field가 필요해 보이면 중단합니다.
- [ ] `--lang zh/es` 추가가 기존 default `ko` 변경을 요구하면 중단합니다.
- [ ] `README.zh.md` / `README.es.md`를 validation required set으로 만들 필요가 생기면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] RED-first 대신 named exception을 기록합니다: behavior는 skill instruction/eval로 검증합니다.
- [ ] Interface contract `--lang ko|ja|en|zh|es`를 README와 eval에 반영합니다.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-spec-writer/SKILL.md`에서 `Supports Korean, Japanese, and English output` 및 `--lang ko|ja|en` 표현을 `ko|ja|en|zh|es`로 확장합니다.
  - [ ] `description` trigger에 Chinese/Spanish request 예시를 추가합니다.
  - [ ] language resolution/default section은 default `ko`를 유지합니다.
  - [ ] validation checklist에서 language match 항목을 5-language contract로 갱신합니다.
- [ ] `codex/skills/ywc-spec-writer/references/language-policy.md`에 Chinese (Simplified)와 Spanish policy를 추가합니다.
  - [ ] Body prose rule을 각 language로 명시합니다.
  - [ ] Technical terms는 English로 유지한다는 예시를 포함합니다.
  - [ ] User story / requirements prose 형식이 기존 ko/ja/en section과 일관되도록 합니다.
- [ ] `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`의 language option과 examples를 갱신합니다.
- [ ] `agents/openai.yaml`의 short/default prompt가 supported languages를 언급한다면 zh/es를 포함합니다.
- [ ] `evals/evals.json`에 `--lang zh`와 `--lang es` fixture를 추가하고 expected output에 prose language와 technical-term policy를 포함합니다.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-spec-writer`
- [ ] `python3 -m json.tool codex/skills/ywc-spec-writer/evals/evals.json >/dev/null`
- [ ] `rg -n "zh|es|Chinese|Spanish|中文|Español" codex/skills/ywc-spec-writer/SKILL.md codex/skills/ywc-spec-writer/references/language-policy.md codex/skills/ywc-spec-writer/evals/evals.json`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 `codex/skills/ywc-spec-writer/**`에만 있는지 확인합니다.
