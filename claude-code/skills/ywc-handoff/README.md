# Handoff Skill (ywc-handoff)

> **사용자 호출 전용 Skill** — `/ywc-handoff` 로 직접 실행합니다. 모델이 자동으로 선택하지 않으며(`disable-model-invocation: true`), 다른 Skill 이 Skill tool 로 호출할 수 없습니다.

현재 대화를 새 Agent session 이 이어받을 수 있는 handoff 문서로 압축하는 Claude Code Skill 입니다. `mattpocock/skills` 의 `handoff` 를 기반으로 합니다.

## 개요

- Goal / State / Decisions / Dead ends / Next step / Waiting on user / References / Suggested skills 의 8개 섹션으로 작성
- State 의 각 thread 는 `gh pr view` / `git branch` 로 확인한 status tag 1개로 시작하며, 확인할 수 없으면 `[unverified]` 와 이유를 기록
- Waiting on user 에는 사용자만 내릴 수 있는 결정만 call / pick / evidence / risk 로 기록 (없으면 `N/A — nothing waits on the user`)
- Spec, plan, ADR, issue, commit, diff 등 이미 존재하는 산출물은 **복사하지 않고 경로·URL 로 참조**
- API key, password, token, 개인정보는 파일에 쓰기 **전에** `<REDACTED>` 로 치환 (본문, code block, log, URL, 파일명, task 이름 모두)
- 저장 위치는 OS 임시 Directory (`${TMPDIR:-/tmp}`) — canonical path 가 repository 밖일 때만 저장하며, `mktemp` 로 새 파일을 만들고 mode `0600` 을 확인

## 사용 방법

```text
/ywc-handoff
/ywc-handoff 다음 session 에서는 PR review 대응만 진행
```

## 옵션 Reference

- **호출**: `/ywc-handoff`
- **입력**: 다음 session 의 용도 (선택) — 지정하면 각 섹션을 그 용도에 맞춰 작성

Flag 없음.
