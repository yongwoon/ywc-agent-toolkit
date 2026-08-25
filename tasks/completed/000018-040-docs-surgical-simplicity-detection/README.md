# 000018-040-docs-surgical-simplicity-detection

## Purpose

리뷰·생성 표면에 Karpathy 원칙 3(외과적 변경 탐지)과 원칙 2(과복잡 탐지)를 심는다. impl-review가 drive-by/범위 외 diff를 횡단 탐지하고(언어 리뷰어 포함), code-gen이 diff-scope·Minimalism을 검증한다.

## Scope

- FR-5: `ywc-impl-review/SKILL.md` Step 3 주입에 "요청/스펙으로 추적되지 않는 변경 hunk(drive-by·churn·범위 외) Surgical 표면화" 1줄(generic + Tier-2 언어 리뷰어 모두 적용); `references/design-agent.md`에 Surgical/Simplicity 하위절; go/python/typescript 리뷰어 agent에 1줄 포인터.
- FR-7: `ywc-code-gen/SKILL.md`에 Verification Gate diff-scope 행 + Output Summary 라인 + Confidence Gate Minimalism 차원 + "동작≠최소" Rationalization 행.
- code-gen README locale set 동기화(§A7 — Output Summary 가시 변경).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §FR-5, §FR-7
- `docs/ywc-plans/claude-code-karpathy-guideline-integration.md` §Iteration 1 Amendments §A4(5-aspect rg 가드), §A8(agents 경로), §A9(용어)
- `claude-code/skills/ywc-impl-review/SKILL.md:60-66,74-77` — Step 3 주입 / Tier-2 dispatch
- `claude-code/skills/ywc-impl-review/references/design-agent.md` — Surgical 절 부재(추가 대상)
- `claude-code/agents/ywc-go-reviewer.md`, `ywc-python-reviewer.md`, `ywc-typescript-reviewer.md` — 1줄 포인터
- `claude-code/skills/ywc-code-gen/SKILL.md` — Verification/Confidence Gate

### Summary

drive-by 탐지 본문의 단일 소스는 impl-review Step 3 주입이며, 3개 언어 리뷰어 agent는 이를 받는다는 1줄 포인터만 갖는다(중복 본문 금지). design-agent는 Architecture/Devex 절을 미러링한 Surgical/Simplicity 하위절을 얻는다. code-gen은 banned-but-not-verified였던 surgical을 git diff로 검증한다.

### Out of Scope (from spec)

- impl-review 5-aspect 구조 변경 — 주입 1줄만(§A4 rg로 보존 검증)
- agent model/tool/출력 상태 변경

## Dependencies

### Depends On

- `000018-010-docs-principles-foundation` — Surgical/Simplicity 표준 원칙 이름

### Depended By

- `000019-010-infra-karpathy-validation` — 최종 검증(AC6/AC8/AC12)

## Key Files

- `claude-code/skills/ywc-impl-review/SKILL.md` — Step 3 주입 1줄
- `claude-code/skills/ywc-impl-review/references/design-agent.md` — Surgical/Simplicity 하위절
- `claude-code/agents/ywc-go-reviewer.md`, `ywc-python-reviewer.md`, `ywc-typescript-reviewer.md` — 포인터 1줄
- `claude-code/skills/ywc-code-gen/SKILL.md` — diff-scope/Minimalism/Rationalization
- `claude-code/skills/ywc-code-gen/README.md`/`README.ko.md`/`README.en.md`/`README.ja.md`

## Notes

- §A8: agent 편집은 **소스 경로** `claude-code/agents/*.md` 기준(설치 경로 tools/claude-code/agents/ 아님).
- impl-review는 reference/agent 변경이라 자체 README 동기화 불필요; code-gen만 README 동기화(Output Summary 변경).
- §A4: 편집 후 5-aspect 이름 + Step 3 주입 블록 온전성 rg로 확인(AC12).

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-impl-review/**`
- `claude-code/agents/ywc-go-reviewer.md`
- `claude-code/agents/ywc-python-reviewer.md`
- `claude-code/agents/ywc-typescript-reviewer.md`
- `claude-code/skills/ywc-code-gen/**`

### Shared Surfaces

- `공유 SoT: principles.md` (읽기 전용 인용)

### Conflicts With

- (None identified)

### Parallelizable After

- `000018-010-docs-principles-foundation`

### Task Verify

- `rg -n "Architecture subagent|Design subagent|Devex subagent|Security subagent|QA subagent" claude-code/skills/ywc-impl-review/SKILL.md` (5개 모두)
- `rg -ni "surgical|drive-by|trace" claude-code/skills/ywc-impl-review/references/design-agent.md`
- `rg -n "drive-by|Surgical|Step 3" claude-code/agents/ywc-go-reviewer.md claude-code/agents/ywc-python-reviewer.md claude-code/agents/ywc-typescript-reviewer.md`
- `rg -n "Minimalism|Diff scope|동작" claude-code/skills/ywc-code-gen/SKILL.md`
- `bash scripts/validate.sh`

## Out of Scope

- 언어 리뷰어에 drive-by 탐지 본문 중복 작성(포인터만)
- impl-review aspect 추가/제거
