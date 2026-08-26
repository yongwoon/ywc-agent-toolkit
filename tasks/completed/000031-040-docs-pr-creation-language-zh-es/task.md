# 000031-040-docs-pr-creation-language-zh-es — Implementation Checklist

## Prerequisites

- [ ] `docs/ywc-plans/ywc-skills-zh-es-language-support.md`의 `ywc-create-pr`와 `ywc-finish-branch` sections를 읽습니다.
- [ ] `codex/skills/ywc-finish-branch/scripts/build-pr-title.py`를 읽고 script edit 필요 여부를 판단합니다.

## Allowed Edit Scope

- [ ] `codex/skills/ywc-create-pr/**`
- [ ] `codex/skills/ywc-finish-branch/**`
- [ ] 다른 executor skill은 수정하지 않습니다.

## Stop Conditions

- [ ] PR title translation이 branch name, task ID, file path, command를 번역해야 하는 형태로 해석되면 중단합니다.
- [ ] `--title` verbatim behavior가 깨질 것 같으면 중단합니다.
- [ ] `build-pr-title.py` 변경이 필요하지만 current examples/contract만으로 검증할 수 없으면 중단합니다.

## Hardening Gate

- [ ] Classify this task: docs-only / skill-definition maintenance, plus optional script-touch if needed.
- [ ] Script를 바꾸면 최소 smoke command를 기록합니다.
- [ ] Interface contract: PR title/body language only, machine identifiers untranslated.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] `codex/skills/ywc-create-pr/SKILL.md`를 갱신합니다.
  - [ ] language prompt를 English/Japanese/Korean/Chinese/Spanish로 확장합니다.
  - [ ] `--lang zh`, `--lang es`, `--language chinese`, `--language spanish`를 accepted hint로 문서화합니다.
  - [ ] PR title/body prose만 번역하고 machine identifiers는 유지한다는 rule을 추가합니다.
- [ ] `codex/skills/ywc-finish-branch/SKILL.md`를 갱신합니다.
  - [ ] `--pr-lang en|ja|ko|zh|es`를 명시합니다.
  - [ ] `[<TASK_NUMBER>] <translated-slug>` examples에 Chinese/Spanish를 추가합니다.
  - [ ] `ywc-create-pr --lang <pr-lang>` pass-through를 그대로 유지합니다.
- [ ] 두 skill의 README locale set, `agents/openai.yaml`, `evals/evals.json`을 갱신합니다.
- [ ] `build-pr-title.py`는 필요한 경우에만 수정하고 smoke test를 추가로 실행합니다.

## Task Verify

- [ ] `python3 -m json.tool codex/skills/ywc-create-pr/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-finish-branch/evals/evals.json >/dev/null`
- [ ] `rg -n "Chinese|Spanish|zh|es|中文|Español" codex/skills/ywc-create-pr codex/skills/ywc-finish-branch`
- [ ] If `build-pr-title.py` changed: `python3 codex/skills/ywc-finish-branch/scripts/build-pr-title.py 000001-010-db-create-users --format title`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`

## Verification

- [ ] Full repository validation은 `000032-010`에서 수행합니다.
- [ ] 이 task 완료 시점의 diff가 allowed scope 안에만 있는지 확인합니다.
