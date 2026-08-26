# 000031-050-docs-executor-pr-lang-zh-es — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`의 executor와 `ywc-agentic` sections를 읽습니다.
- [ ] `000031-040`의 output이 아직 없어도 pass-through contract를 spec 기준으로 유지합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-sequential-executor/**`
- [ ] `codex/skills/ywc-parallel-executor/**`
- [ ] `codex/skills/ywc-agentic/**`

## Stop Conditions

- [ ] `--pr-lang` pass-through를 구현하려다 executor merge/CI/bot behavior를 바꿔야 한다면 중단합니다.
- [ ] `ywc-agentic`이 명시되지 않은 task language를 추정해서 강제로 넘겨야 하는 요구로 해석되면 중단합니다.
- [ ] `claude-code/**` 또는 plugin mirror 직접 수정이 필요하면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance.
- [ ] Named exception: runtime code 없음. Eval fixture와 grep 검증으로 대체합니다.
- [ ] Interface contract `--pr-lang` pass-through를 각 skill에 기록합니다.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-sequential-executor/SKILL.md`와 references를 갱신합니다.
  - [ ] `--pr-lang en|ja|ko|zh|es`를 문서화합니다.
  - [ ] auto-detection examples에 Chinese/Spanish를 추가합니다.
  - [ ] downstream call examples가 `--pr-lang <pr-lang>`를 unchanged로 넘기도록 확인합니다.
- [ ] `codex/skills/ywc-parallel-executor/SKILL.md`와 `references/aggregate-pr.md`를 갱신합니다.
  - [ ] draft/aggregate PR path에서 `--pr-lang zh/es` pass-through를 명시합니다.
- [ ] `codex/skills/ywc-agentic/SKILL.md`를 갱신합니다.
  - [ ] `--pr-lang en|ja|ko|zh|es`를 문서화합니다.
  - [ ] explicit task/spec language request가 있을 때만 `ywc-task-generator`로 `--lang`을 넘긴다는 기존 behavior를 보존합니다.
- [ ] 세 skill의 README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.

## Task Verify

- [ ] `python3 -m json.tool codex/skills/ywc-sequential-executor/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-parallel-executor/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-agentic/evals/evals.json >/dev/null`
- [ ] `rg -n "zh|es|Chinese|Spanish|--pr-lang" codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor codex/skills/ywc-agentic`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 allowed scope 안에만 있는지 확인합니다.
