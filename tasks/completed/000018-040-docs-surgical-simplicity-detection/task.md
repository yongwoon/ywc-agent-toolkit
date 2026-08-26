# 000018-040-docs-surgical-simplicity-detection — Implementation Checklist

## Prerequisites

- [ ] `000018-010-docs-principles-foundation` 완료(merged)

## Allowed Edit Scope

- [ ] `ywc-impl-review/**`, 3개 언어 리뷰어 agent, `ywc-code-gen/**`만 편집
- [ ] Ownership 밖 편집 필요 시 중단·보고

## Stop Conditions

- [ ] impl-review 5-aspect 구조를 바꿔야 하면 중단(주입 1줄만)
- [ ] 언어 리뷰어에 탐지 본문을 중복 작성해야 하면 중단(포인터만)
- [ ] agent model/tool/출력 상태를 바꿔야 하면 중단

## Implementation Steps

- [ ] **FR-5 impl-review Step 3 주입** — Step 3 주입 블록(:66 인근)에 "추적 불가 hunk를 Surgical 발견으로 표면화(drive-by·churn·범위 외)" 1줄(generic + Tier-2 적용 명시)
- [ ] **FR-5 design-agent 하위절** — `references/design-agent.md`에 Surgical-Changes(시그니처 drive-by, 무관 public-surface) + Simplicity(요구 초과/더 적은 줄 표현) 하위절 추가
- [ ] **FR-5 언어 리뷰어 포인터** — go/python/typescript reviewer.md 각각에 "impl-review Step 3 주입 Surgical 체크를 자기 언어 diff에 적용(중복 본문 금지)" 1줄
- [ ] **FR-7 code-gen surgical/minimalism**
  - Verification Gate에 Diff scope 행(`git diff --stat`; 스펙 명명 파일만) + Output Summary 라인
  - Confidence Gate에 Minimalism 차원(≥70)
  - Rationalization "동작≠최소" 행
- [ ] **README 동기화(§A7)** — code-gen README.md/ko/en/ja

## Task Verify

- [ ] `rg -n "Architecture subagent|Design subagent|Devex subagent|Security subagent|QA subagent" claude-code/skills/ywc-impl-review/SKILL.md` (5개)
- [ ] `rg -ni "surgical|simplicity" claude-code/skills/ywc-impl-review/references/design-agent.md`
- [ ] `rg -n "Step 3|drive-by|Surgical" claude-code/agents/ywc-go-reviewer.md claude-code/agents/ywc-python-reviewer.md claude-code/agents/ywc-typescript-reviewer.md`
- [ ] `rg -n "Minimalism|Diff scope" claude-code/skills/ywc-code-gen/SKILL.md`
- [ ] code-gen README 4종 반영

## Verification

- [ ] `bash scripts/validate.sh` exit 0
- [ ] `bash scripts/install.sh --list --cc-agents` exit 0(agent 편집 후)
- [ ] markdownlint 통과
