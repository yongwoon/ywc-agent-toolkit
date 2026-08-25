# 000078-010-docs-impl-review-bounded-payload-noninteractive

## Purpose

`ywc-impl-review`의 Phase 1 fan-out에 payload 상한을 명시하고, Return-payload contract directive를 verbatim 주입하며, Step 7의 사용자 응답 대기 지점을 억제하는 `--non-interactive` flag를 신설한다. 이 batch의 foundation task로, 나머지 caller task들이 소비할 flag 계약을 정의한다.

## Scope

- FR-1: Step 2 말미 문장을 Phase 1까지 포함하도록 확장, Step 3에 dispatch payload 제한 명시, `subagent-status-actions.md` §Return Payload Contract directive verbatim 인용, Integration `pattern source`에 reference 등재.
- FR-2: Arguments 표에 `--non-interactive` 1행 추가, Step 7을 interactive / non-interactive 2갈래로 분기, `Learning candidates (not promoted — non-interactive)` block schema 규정.
- FR-7(부분): `ywc-impl-review` README 6 locale에 신설 flag 반영.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-1-ywc-impl-review-phase-1-bounded-payload--return-payload-directive`
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-2-ywc-impl-review---non-interactive`
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#iteration-1-amendments` — Operative Sections 및 FR-1 rationale 수정본이 authoritative
- `claude-code/skills/references/subagent-status-actions.md` — §Return Payload Contract (인용 원본, 읽기 전용)

### Summary

Phase 1의 5-way fan-out에는 현재 payload 상한이 없어 부모가 읽은 spec 전문·diff 전문이 5개 subagent로 그대로 흘러갈 수 있다. Step 2의 "do not forward it wholesale to Phase 2" 문장을 Phase 1까지 확장하고, Step 3에서 각 subagent가 (a) 변경 파일 목록 + spec 파일 **경로**, (b) 자기 aspect의 `references/*-agent.md`, (c) 자기 aspect로 filter된 learnings 만 받도록 제한한다. 필요한 파일은 subagent가 스스로 Read한다. 동시에 Step 7의 learnings 승격 prompt가 unattended loop를 멈추는 문제를 `--non-interactive`로 닫되, write 경로는 열지 않고 report에만 후보를 기록한다. Iteration 1 Amendments에 따르면 이 repo에서 Return-payload contract directive를 실제로 주입하는 skill은 **0개**이며, FR-1이 최초 사례다. `ywc-code-gen`의 base-prompt 패턴(`prompts/implementer-base.md`)은 의도적으로 채택하지 않는다 — 1줄 directive를 위해 파일을 만드는 것은 need가 아닌 pattern 충족이다.

### Out of Scope (from spec)

- Phase 2의 기존 payload 규칙(`SKILL.md:95` Context payload)과 advisor budget(기본 5) — AC3에 의해 diff에 나타나면 안 된다.
- Step 0 loading 서술 — AC5에 의해 무변경.
- `--skip-learnings` 행(`SKILL.md:42`) 문구 — AC6에 의해 무변경. 조합 semantics는 신설 행과 Step 7 본문에만 기술한다.
- Step 3의 learnings aspect-scoping(`:72`) — 이미 "filtered to that aspect's category"이므로 무변경.
- 기존 36건의 `§3.5` citation drift 일괄 정정 — 선행 결함이며 범위 밖.
- caller 7곳의 flag 전파 — `000078-020` / `-030` / `-040`이 담당.

## Criticality

`normal` — skill의 prompt 문서만 수정하며 auth·payment·secret·PII 경로를 포함하지 않는다. `--non-interactive`는 사용자 확인을 억제하지만 write 권한을 확대하지 않는다 — learnings write 경로를 오히려 제거하는 방향이다 (spec §Critical Surfaces).

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000078-020-docs-sequential-executor-noninteractive` — `--non-interactive` flag의 의미 계약과 impl-review 호출 형태
- `000078-030-docs-parallel-executor-flag-compaction` — 동일
- `000078-040-docs-code-gen-agentic-propagation` — 동일
- `000079-010-infra-context-safety-validation` — AC1/AC2/AC3/AC4/AC5/AC6/AC8/AC15 검증 대상

## Key Files

- `claude-code/skills/ywc-impl-review/SKILL.md` — Step 2 확장, Step 3 payload 제한 + directive 주입, Arguments 표 flag 1행, Step 7 분기 + block schema, Integration pattern source 1건 추가
- `claude-code/skills/ywc-impl-review/README.md` — 한국어 기본, flag 설명 추가
- `claude-code/skills/ywc-impl-review/README.en.md` — 영어 원본
- `claude-code/skills/ywc-impl-review/README.ja.md`
- `claude-code/skills/ywc-impl-review/README.ko.md`
- `claude-code/skills/ywc-impl-review/README.zh.md`
- `claude-code/skills/ywc-impl-review/README.es.md`

## Notes

- **인용 anchor는 `§Return Payload Contract`(section 이름)로 적는다.** 본 repo의 `subagent-status-actions.md`에 `§3.5` 번호가 존재하지 않기 때문이다(headings: `## Status Responses` / `## Return Payload Contract` / `## BLOCKED Triage` / `## Aggregating Status`). 기존 36건의 `§3.5` 인용은 손대지 않는다.
- **`Occurrences in this review`는 단일 invocation 내 카운트다.** cross-invocation recurrence는 사람이 확인하는 Step 7 승격 flow가 확립하는 값이므로 non-interactive에는 데이터 출처가 없다. 두 Confirmed finding은 (a) 같은 aspect이고 (b) 같은 defect class일 때 같은 occurrence로 센다. aspect가 다르면 증상이 유사해도 병합하지 않는다. `<n>` = 1인 항목은 block에 싣지 않는다.
- block schema의 field 순서는 고정이다: `[<aspect>] Occurrences in this review: <n> — <finding 1-line summary> (severity: <값>) — would promote to <target file> as <learning type>`.
- `--non-interactive`는 `ywc-plan --non-interactive`(`ywc-plan/SKILL.md:17,99`)에서 **"질문을 열지 않는다"는 절반만** 재사용한다. FR-2는 어떤 default 값도 적용하지 않고 아무것도 write하지 않는다.
- README 6 locale은 상호 정합해야 한다 — `README.en.md`가 영어 원본, `README.md`가 한국어 기본. `translation-check.yml`은 informational 경고만 낸다.
- 본문 편집은 **영문**이다 (대상 파일이 전부 영문). 한국어는 `README.md` / `README.ko.md`에만 적용.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-impl-review/**`

### Shared Surfaces

- `--non-interactive` flag 의미 계약 — `000078-020` / `-030` / `-040`이 소비
- `claude-code/skills/references/subagent-status-actions.md` — **읽기 전용**. 이 task는 수정하지 않는다
- CI gates: `scripts/validate.sh`, `markdownlint.yml`, `score.py --ci`

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `grep -c "Return-payload contract" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 1 (현재 0)
- `grep -c "subagent-status-actions" claude-code/skills/ywc-impl-review/SKILL.md` — ≥ 2 (Step 3 + Integration, 현재 0)
- `git diff -- claude-code/skills/ywc-impl-review/SKILL.md` 에서 Step 0 서술 / `--skip-learnings` 행 / Phase 2 Context payload / advisor budget 이 나타나지 않음 (AC3/AC5/AC6)
- `ls claude-code/skills/ywc-impl-review/README*.md | wc -l` — 6, 전부 flag 언급

## Out of Scope

- 다른 skill / agent 파일의 어떤 수정도 포함하지 않는다.
- `claude-code/skills/references/**` 파일 수정 — 이 task는 참조·인용만 한다.
- 신규 shared reference 파일 생성 또는 `prompts/` 디렉터리 신설.
- `codex/**` 하위 모든 파일 (AC17).
- mechanical score baseline 재생성 — `000079-010`이 담당.
