# ywc-design-renew

평범하거나 "LLM이 만든 듯한(AI slop)" Frontend 화면을 distinctive 한 디자인으로 리뉴얼하고, 동시에 AI-slop tell 을 점검하는 Codex Skill 입니다. 설치되어 있으면 `impeccable` skill 을 design engine 으로 위임하고, 없으면 자체 내장 ruleset 으로 동작하므로 어떤 project / runtime 에서도 작동합니다.

## 개요

LLM 이 생성한 화면은 동일한 template 으로 학습된 탓에 cyan-on-dark palette, gradient text, border-left stripe, Inter font, 균일한 card grid 같은 예측 가능한 시각적 cliché 로 수렴합니다. 이 Skill 은 그 "AI slop" 신호를 검출(check)하고 제거(renew)합니다.

- **renew mode (기본)**: 기존 화면을 받아 bold 한 aesthetic direction 으로 개선하고 before/after evidence 를 남깁니다.
- **check mode**: 편집 없이 AI-slop 점검만 수행하고 pass/fail gate 를 적용합니다.

핵심 판정 기준은 **AI Slop Test** 입니다 — "이 화면을 보여주며 'AI 가 만들었다'고 하면 즉시 믿겠는가?"

## 사전 준비물

- (선택) `impeccable` skill — 있으면 더 강력한 design engine 으로 위임, 없으면 자체 ruleset fallback. 설치되어 있지 않아도 이 Skill 은 자체 ruleset 으로 계속 진행합니다. `npx impeccable skills install` 을 사용할 수 있는 project 라면 설치 후 `impeccable init` 으로 project Design Context 를 1회 설정하면 아래 `PRODUCT.md` / `DESIGN.md` 가 생성되어 재질문이 생략됩니다.
- (선택) Live URL (local dev server) — before/after screenshot 용 Chrome DevTools MCP 탐색에 사용.
- (선택) `.impeccable.md` / `PRODUCT.md` / `DESIGN.md` — Design Context 가 이미 있으면 재질문 생략.

## 사용 시나리오

- "이 dashboard 디자인이 너무 평범해, LLM 이 만든 것 같아. 리뉴얼해줘."
- "배포 전에 이 화면이 AI slop 신호가 있는지 점검해줘."
- "Hero section 을 distinctive 하게 다시 디자인해줘."

## 사용 방법

```text
Use $ywc-design-renew to renew src/components/hero with --url http://localhost:3000.
Use $ywc-design-renew --mode check --target src/app/dashboard --fail-on critical.
```

또는 자연어로 호출:

> "이 화면 디자인이 LLM 이 한 것 같아. 리뉴얼 해줘."

## 입력

- **필수**: `--target` (리뉴얼/점검할 component·page·route) + Design Context (audience / use-cases / brand tone)
- **선택**: `--url` (live screenshot), `--mode check`, `--fail-on`, `--format html`

## 출력

- **renew**: 리뉴얼된 code + 리뉴얼 report (선택한 direction, 해소한 slop finding before→after, 변경 파일, 재검증 결과, before/after screenshot)
- **check**: 우선순위(Critical/High/Medium/Low) slop audit report + `--fail-on` gate 판정

## 관련 Skill

- `impeccable` — 설치 시 design engine 으로 위임 (craft / polish / audit)
- `ywc-ui-ux-review` — 리뉴얼 후 usability / IA / WCAG 축 검증 (이 Skill 은 미감/slop 축만 담당)
- `ywc-review-learnings` — 리뉴얼 중 확정된 디자인 선호를 project 별로 축적
