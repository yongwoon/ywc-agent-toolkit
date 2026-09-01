# Task: 000038-030-docs-wire-git-artifact-consumers

## Prerequisites
- [ ] `000037-010-docs-language-resolution-reference` 완료(`references/language-resolution.md` 존재).

## Allowed Edit Scope
- `claude-code/skills/ywc-create-pr/SKILL.md`
- `claude-code/skills/ywc-commit/SKILL.md`
- 그 외 파일 편집 금지.

## Stop Conditions
- create-pr 의 `--title` verbatim 우선(EC4) 을 깨지 않고 resolution 을 넣을 수 없으면 중단하고 보고.
- commit 위임 chain 에서 이중 해석/이중 prompt 위험이 보이면 중단하고 보고(EC7).

## Implementation Steps
- [ ] `ywc-create-pr/SKILL.md`(Step 0, :52) — `AskUserQuestion` 이전에 `> **Action required**: Read [../references/language-resolution.md]` 로 resolution 수행:
  - [ ] 정책 resolve 되면 그 언어로 제목·본문 작성, 언어 prompt **skip**(AC6).
  - [ ] resolve 안 되면 현행처럼 prompt 하되 옵션을 `ko|ja|en|es|zh` 로 확대(AC10 보존 + 누락 언어 추가).
  - [ ] `--title` 제공 시 제목 verbatim, 정책은 본문 언어만 지배(EC4).
  - [ ] 제목의 `[task-id]`/conventional prefix 는 영어 유지.
- [ ] `ywc-commit/SKILL.md` — message 설명부 언어 해석 step 추가:
  - [ ] `> **Action required**: Read [../references/language-resolution.md]` 로 resolved 언어에 설명부 작성(AC7).
  - [ ] `type:` prefix(`feat:`/`fix:` 등)·whitelist 기술용어는 영어 유지.
  - [ ] read-only·멱등이라 위임 chain(finish-branch→create-pr→commit)에서도 동일 언어 해석, 추가 prompt 없음(EC7).

## Task Verify
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-create-pr/SKILL.md`
- [ ] `grep -q "language-resolution.md" claude-code/skills/ywc-commit/SKILL.md`
- [ ] 수동: create-pr 옵션이 5개 언어로 확대됐는지, 정책 존재 시 prompt skip 문구가 있는지 확인.

## Verification
- [ ] `bash scripts/validate.sh` 통과.
- [ ] 수동: commit 설명부는 resolved 언어, `type:` prefix 는 영어라는 규칙이 문서상 명확한지 확인(AC7).
