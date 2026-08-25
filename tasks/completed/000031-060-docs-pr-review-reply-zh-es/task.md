# 000031-060-docs-pr-review-reply-zh-es — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`의 `ywc-handle-pr-reviews` section을 읽습니다.
- [ ] 기존 `Reply language` rule을 확인합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-handle-pr-reviews/**` 안에서만 수정합니다.

## Stop Conditions

- [ ] PR artifact fetch script나 merge-readiness logic 변경이 필요해 보이면 중단합니다.
- [ ] Reply language rule이 original comment matching이 아니라 fixed enum enforcement로 바뀌려 하면 중단합니다.
- [ ] `claude-code/**` 또는 plugin mirror 직접 수정이 필요하면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. Eval fixture와 grep 검증으로 대체합니다.
- [ ] Interface contract: original comment language matching, machine text unchanged.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-handle-pr-reviews/SKILL.md`의 `Reply language` section을 갱신합니다.
  - [ ] Korean/English examples에 Japanese/Chinese/Spanish를 추가합니다.
  - [ ] code suggestions, command output, file path, API name, quoted reviewer text는 번역하지 않는다고 명시합니다.
- [ ] README locale set에서 reply language guidance가 stale하면 갱신합니다.
- [ ] `agents/openai.yaml`이 reply language를 언급한다면 examples를 확장합니다.
- [ ] `evals/evals.json`에 Chinese 또는 Spanish reviewer comment에 같은 language로 reply해야 한다는 fixture를 추가합니다.

## Task Verify

- [ ] `python3 -m json.tool codex/skills/ywc-handle-pr-reviews/evals/evals.json >/dev/null`
- [ ] `rg -n "Reply language|Chinese|Spanish|中文|Español" codex/skills/ywc-handle-pr-reviews`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 `codex/skills/ywc-handle-pr-reviews/**`에만 있는지 확인합니다.
