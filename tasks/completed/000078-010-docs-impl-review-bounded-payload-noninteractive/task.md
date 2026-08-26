# 000078-010-docs-impl-review-bounded-payload-noninteractive — Implementation Checklist

## Prerequisites

- [ ] (None — root task)
- [ ] `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md` 및 `## Iteration 1 Amendments` 를 읽었다 (Amendments가 authoritative)
- [ ] `claude-code/skills/references/subagent-status-actions.md` §Return Payload Contract 의 directive 1줄 원문을 확인했다

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-impl-review/**` 안에서만 편집한다
- [ ] Ownership 밖 편집이 필요하면 중단하고 보고한다

## Stop Conditions

- [ ] `subagent-status-actions.md` §Return Payload Contract 의 directive 1줄을 특정할 수 없으면 중단
- [ ] Step 2 / Step 3 / Step 7 / Integration 의 실제 line 위치가 spec의 `file:line`과 크게 어긋나면 중단하고 보고
- [ ] 변경이 `references/**` 또는 다른 skill 디렉터리로 번지면 중단
- [ ] `--skip-learnings` 행 문구를 수정해야만 semantics가 성립한다고 판단되면 중단 (AC6 위반)

## Implementation Steps

- [ ] **FR-1a — Step 2 payload 경계 확장** (`SKILL.md:63` 부근)
  - [ ] "This context stays with the parent; do not forward it wholesale to Phase 2." 문장을 **Phase 1도 포함**하도록 확장한다
  - [ ] 부모가 읽은 spec/코드 전문은 부모 context에 남고 subagent에는 경로와 범위만 전달함을 명시한다
- [ ] **FR-1b — Step 3 dispatch payload 제한** (`SKILL.md:72-76` 부근)
  - [ ] 각 subagent가 받는 것을 3항목으로 한정해 명시: (a) 변경 파일 목록 + spec 파일 **경로**, (b) 자기 aspect의 `references/*-agent.md`, (c) 자기 aspect로 filter된 learnings
  - [ ] 필요한 파일은 subagent가 **스스로 Read** 한다고 명시한다
  - [ ] 다른 subagent의 결과 / 전체 project context / 다른 aspect의 rubric 은 전달하지 않는다고 명시한다
  - [ ] `:72` 의 기존 "filtered to that aspect's category" 문구는 그대로 둔다 (이미 aspect-scoped)
- [ ] **FR-1c — Return-payload contract directive verbatim 주입**
  - [ ] `../references/subagent-status-actions.md` §Return Payload Contract 의 directive 1줄을 **문자 그대로** 인용해 각 subagent prompt에 주입하도록 Step 3에 규정한다
  - [ ] Confirmed findings 와 Advisor candidates 의 **본문은 파일로 쓰고 path만 반환**, 부모는 report 조립 시 읽도록 `:74-76` 의 inline 반환 규정을 조정한다
  - [ ] Phase 2 escalation용 bounded snippet(≤100줄)은 candidate 파일 **안에** 두고, 부모는 budget 통과 항목에 대해서만 읽는다고 명시한다
  - [ ] 인용 anchor는 `§Return Payload Contract` 로 표기한다 (`§3.5` 금지)
- [ ] **FR-1d — Integration 등재** (`SKILL.md:240` 부근)
  - [ ] `pattern source` 목록에 `subagent-status-actions.md` 1건을 추가한다 (기존 `advisor-pattern.md` / `coderabbit-methodology.md` 유지)
- [ ] **FR-2a — Arguments 표에 flag 추가**
  - [ ] `--non-interactive` 1행 추가. 의미: Step 7의 사용자 확인 prompt를 열지 않음. Step 0 loading / Phase 1 / Phase 2 / report 생성은 무변경
  - [ ] default가 interactive(opt-in flag)임을 명시한다 (AC8)
  - [ ] `--skip-learnings` 와 **직교**함을 이 행에 기술한다. `:42` 행 문구는 수정하지 않는다
- [ ] **FR-2b — Step 7 2갈래 분기** (`SKILL.md:101` 부근)
  - [ ] Interactive(기본): 현행 문구를 그대로 유지한다
  - [ ] Non-interactive: offer를 생략하고 후보를 report block에 기록한 뒤 종료한다
  - [ ] `docs/review-learnings.md` / `references/recurring-defects.md` 에 대한 write 는 **어느 mode에서도 발생하지 않음**을 명시한다
  - [ ] 두 flag 동시 지정 시 Step 0·Step 7 모두 skip 되며 block을 출력하지 않음을 기술한다 (수집 근거 없음)
- [ ] **FR-2c — block schema 규정**
  - [ ] `### Learning candidates (not promoted — non-interactive)` block 형식을 코드블록으로 명시한다
  - [ ] field 순서 고정: `[<aspect>] Occurrences in this review: <n> — <finding 1-line summary> (severity: <값>) — would promote to <target file> as <learning type>`
  - [ ] `<aspect>` 는 Architecture / Design / Devex / Security / QA 중 하나로 한정한다
  - [ ] `Occurrences in this review` 가 **단일 invocation 내 카운트**이며 cross-invocation recurrence가 아님을 명시한다
  - [ ] 같은 occurrence 판정 기준(같은 aspect + 같은 defect class, 조립자의 분류 판단)과 `<n>` = 1 항목 제외 규칙을 기술한다
  - [ ] 해당 항목이 0건일 때 `(none)` 을 출력하고 block 자체는 생략하지 않음을 명시한다 (Auditability NFR)
- [ ] **FR-7(부분) — README 6 locale 갱신**
  - [ ] `README.en.md` 에 영어 원본으로 flag 설명을 추가한다
  - [ ] `README.md` / `README.ko.md` 에 한국어로 반영한다 (technical term은 English 유지)
  - [ ] `README.ja.md` / `README.zh.md` / `README.es.md` 에 각 언어로 반영한다
  - [ ] 6개 파일이 동일한 flag semantics를 서술하는지 대조한다 (AC15)

## Task Verify

- [ ] `grep -c "Return-payload contract" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 1
- [ ] `grep -c "subagent-status-actions" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 2
- [ ] `grep -c "Learning candidates (not promoted — non-interactive)" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 1
- [ ] `grep -n -- "--non-interactive" claude-code/skills/ywc-impl-review/README*.md` — 6개 파일 전부 hit
- [ ] `git diff -- claude-code/skills/ywc-impl-review/SKILL.md | grep -c "skip-learnings"` — `:42` 행이 변경 hunk에 없음을 육안 확인 (AC6)
- [ ] `git diff -- claude-code/skills/ywc-impl-review/SKILL.md` 에 Phase 2 Context payload / advisor budget / Step 0 서술이 없음을 육안 확인 (AC3/AC5)

## Verification

- [ ] `bash scripts/validate.sh` 통과 (skill 구조 + README locale 필수 파일)
- [ ] markdownlint 통과 — `.github/workflows/markdownlint.yml` 의 실제 invocation 형태를 재현한다 (로컬에서 임의 버전 pin + 다른 config 사용 금지)
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --format json` 으로 read-only 확인 (baseline 재생성은 `000079-010` 소관)
- [ ] `git diff --name-only | grep -c '^codex/'` — 0 (AC17)
- [ ] 수동 transcript 확인 — `test.md` 참조

## Implementation Notes
