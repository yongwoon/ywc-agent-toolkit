# 000031-030-docs-gen-testcase-codex-zh-es — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`의 `ywc-gen-testcase` section을 읽습니다.
- [ ] `codex/skills/ywc-gen-testcase/SKILL.md`의 machine-surface English invariant를 확인합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-gen-testcase/**` 안에서만 수정합니다.
- [ ] `references/language-policy.md`를 새로 만들지 않습니다.

## Stop Conditions

- [ ] zh/es support가 YAML front matter key나 template skeleton 번역을 요구하는 방향으로 흐르면 중단합니다.
- [ ] `--lang` 외의 source parsing behavior가 바뀌어야 한다면 중단합니다.
- [ ] `claude-code/**` 또는 plugin mirror 직접 수정이 필요하면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. Eval fixture와 validation으로 대체합니다.
- [ ] Interface contract `--lang ja|ko|en|zh|es`를 기록합니다.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-gen-testcase/SKILL.md`에서 `--lang <code>` row를 `ja,ko,en,zh,es`로 확장합니다.
- [ ] auto-detect fallback / detected language reporting 문구에 Chinese와 Spanish를 추가합니다.
- [ ] "YAML front matter keys, section numbers, template skeleton stay English" invariant가 zh/es에도 적용되도록 문구를 확장합니다.
- [ ] zh/es prose에서도 Technical terms는 English로 유지한다는 inline rule을 추가합니다.
- [ ] README locale set에서 supported-language wording과 examples를 갱신합니다.
- [ ] `agents/openai.yaml` metadata가 supported language를 언급한다면 `zh/es`를 포함합니다.
- [ ] `evals/evals.json`에 Chinese와 Spanish testsheet prose fixture를 추가합니다.

## Task Verify

- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-gen-testcase`
- [ ] `python3 -m json.tool codex/skills/ywc-gen-testcase/evals/evals.json >/dev/null`
- [ ] `rg -n "zh|es|Chinese|Spanish|中文|Español" codex/skills/ywc-gen-testcase/SKILL.md codex/skills/ywc-gen-testcase/evals/evals.json`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 `codex/skills/ywc-gen-testcase/**`에만 있는지 확인합니다.
