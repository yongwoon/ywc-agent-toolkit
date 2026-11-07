# Retrospective Skill (ywc-retro)

> **사용자 호출 전용 Skill** — `/ywc-retro` 로 직접 실행합니다. 모델이 자동으로 선택하지 않으며(`disable-model-invocation: true`), 다른 Skill 이 Skill tool 로 호출할 수 없습니다.
>
> **Agent 의존성** — lens 와 synthesizer 는 read-only `ywc-retro-lens` Agent (Read / Grep / Glob 만) 에서 실행됩니다. `bash scripts/install.sh --cc-agents ywc-retro-lens` 로 설치하며, 설치되지 않은 경우 single pass 로 fallback 합니다.

Coding session 을 회고하여, 다음 실행부터 Agent 가 더 잘 일하도록 **환경**(navigation pointer, automated check, coding standard, steering file, tooling, 정보 접근)을 개선할 후보를 심각도 (High / Medium / Low) 순으로 제안하는 Claude Code Skill 입니다. `mattpocock/skills` 의 `retro` 를 기반으로 합니다.

## 개요

- Session 의 primary source(대화, tool call)를 직접 읽고 근거를 인용
- 7개 범주로 후보 수집: Navigation / Automated checks / Coding standards / Steering files / Tool economy / No-ops / Information access
- 후보는 3개 lens subagent (judgment / tooling / divergent, `sonnet`) 가 병렬로 수집하고, clean context 의 synthesizer (`opus`) 가 기각 사유와 함께 걸러냄 — 회고 대상인 parent session 의 self-review bias 를 피하기 위함이며, 실행마다 subagent 4회 비용이 듦
- **기계적 위반은 규칙이 아니라 check 로**: 고정 패턴·금지 API·import 형태 위반은 lint rule, pre-commit hook, CI job 으로 제안하고, 판단이 필요한 것만 문서화된 standard 로 제안
- pre-commit hook 도 CI 도 없는 repo 는 그 자체를 finding 으로 보고
- 결과를 보여주기 전에 credential·token·개인정보를 `<REDACTED>` 로 치환
- 제안만 하고 적용하지 않음 — 채택 여부는 사용자가 결정

## 사용 방법

```text
/ywc-retro
/ywc-retro 어제 ywc-agentic 실행했던 session
```

## 옵션 Reference

- **호출**: `/ywc-retro`
- **입력**: 대상 session (생략 시 현재 session)

Flag 없음.

## 관련 Skill

- `ywc-skill-author` — Skill 지시가 원인인 후보의 후속 처리, 그리고 회고가 참조하는 Writing Levers 의 출처
- `ywc-review-learnings` — Project 단위 review 선호를 축적
- `ywc-incident-postmortem` — Production 장애 회고 (이 Skill 은 Agent session 회고)
