# ywc-onboard-repo (한국어)

기존 / 처음 보는 Repository 진입 시 4-Phase (Reconnaissance → Architecture → Conventions → Generate) 로 Onboarding Guide 와 Starter AGENTS.md 를 생성하는 Skill 입니다. 신규 Repository 생성 (scaffolding) 이 아니며, `ywc-project-scaffold` 의 inverse direction 입니다. Reconnaissance 는 Glob + Grep 만 사용하여 token cost 를 통제합니다.

## Localized Versions

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)

## 사용 시나리오

- 사용자가 "onboard me", "이 repo 처음이야", "이 codebase 이해하게 해줘" 라고 말할 때
- 새 Project 에 Codex 를 처음 설정할 때 (Starter AGENTS.md 생성)
- Subagent runner 가 implementation 위임 전에 AGENTS.md 를 필요로 할 때

## 사용 방법

```bash
$ywc-onboard-repo --scope apps/web/
```

또는 자연어로:

> "이 repo onboard 해줘"
> "AGENTS.md 만들어줘"

## Iron Law

1. **Reconnaissance 는 Glob + Grep 만 사용** — Read 는 ambiguous signal 발생 시에만
2. **Code 에서 검증된 convention 이 config 보다 우선**
3. **기존 AGENTS.md 는 enhancement 만**, overwrite 금지

## 입력

- (선택) `--scope <dir>` — Monorepo 의 특정 workspace 만 reconnaissance
- (선택) `--guide-only` — Onboarding Guide 만 emit, AGENTS.md skip
- (선택) `--agents-md-only` — AGENTS.md 만 생성, Guide skip
- (선택) `--enhance` — 기존 AGENTS.md 가 없어도 enhancement path 강제

## 출력

- **Output A**: Onboarding Guide (Conversation 에 Markdown 으로 print) — Tech Stack, Architecture, Key Entry Points, Directory Map, Request Lifecycle, Conventions, Common Tasks, Where to Look, Detection Confidence
- **Output B**: Starter AGENTS.md (repo root 에 write) — 기존 file 있으면 `## Detected Conventions (<YYYY-MM-DD>)` section 만 추가

## 관련 Skill

- `ywc-project-scaffold` — inverse direction (신규 repo 생성). 같은 session 에서 둘 다 호출 금지
- `ywc-refactor-clean` — reconnaissance 가 dead-code accumulation 을 감지하면 follow-up PR 로 routing
- `ywc-impl-review` — 작성된 Onboarding Guide 가 cold review 의 anchor 가 됨
- `ywc-plan` — Phase 2 의 Request Lifecycle 이 plan Step 2 의 architectural anchor
- `ywc-verify-done` — 최종 "Wrote AGENTS.md" claim 의 vocabulary 규칙 제공
