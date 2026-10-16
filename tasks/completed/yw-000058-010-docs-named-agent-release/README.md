# yw-000058-010-docs-named-agent-release

## Purpose
named subagent 가 완료 후 `idle` 로 남아 누적되는 문제를 막기 위해, async monitoring 계약에 release 절차를 추가하고 모든 concurrent batch dispatch 지점에 inline Release 단계와 이를 강제하는 test 를 둔다 (Phase A).

## Scope
- `subagent-async-monitoring.md` 에 `## On Every Signal`, 재조회 판단 표, 매 signal stall 점검, `## Releasing Completed Named Agents` 추가 (FR-A1~A4)
- 10 개 skill 12 곳에 단일 줄 `Action required` callout + `Release … TaskStop` (FR-A5), impl-review Step 6↔7 사이 독립 release 단계
- `tests/named_agent_release_test.py` 신규 + `scripts/validate.sh` 연결 (FR-A6)
- `claude-code/skills/CLAUDE.md` 소비자 목록 11 개로 갱신 (FR-A7), `ScheduleWakeup(` 미포함 (FR-A8)

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.md` — `## Scope` Phase A, `## Existing Constraints Touched`, FR-A1~FR-A8, AC-1/2/3/4/12(A2·A3)/13/15/18, FM-1/2/6
- `docs/ywc-plans/20261016-claude-upstream-issue69-port.spec-ready-log.md` — spec 수렴 이력 (ywc-spec-ready DONE)

### Summary
upstream #290/#294/#241/#252(일부) 를 이 저장소의 구버전 async monitoring 계약에 맞춰 적응 반영한다. upstream 의 `SendMessage` status-check 는 도입하지 않는다. callout 은 반드시 물리적 한 줄이며, 파일 내 모든 callout 줄마다 Release 가 있어야 test 를 통과한다. upstream diff 는 `gh pr diff <n> -R yongwoon/develop-with-llm` 의 `tools/claude-code/` 부분을 읽고 수동 반영한다.

### Out of Scope (from spec)
- #252 `audit-schedulewakeup.py` hook — 배포 대상 아님
- #294 `ywc-auth-implement/references/workflow-detail.md`, `ywc-team-assemble` — 이 저장소에 없음
- `ywc-skill-author` deletion test Release — Open Questions 6

## Criticality
`normal` — skill 문서 / 검증 script 변경이며 인증·결제·secret 등 security-sensitive surface 를 다루지 않음 (spec 에 Critical Surfaces 선언 없음)

## Dependencies

### Depends On
- (None — this is a root task)

### Depended By
- `yw-000059-010-docs-spec-plan-omission-checks` — Phase A 머지 base (spec-validate callout 이 들어간 SKILL.md)

## Key Files
- `claude-code/skills/references/subagent-async-monitoring.md` — 계약 확장
- `claude-code/skills/CLAUDE.md` — 소비자 목록
- `claude-code/skills/ywc-impl-review/SKILL.md` — `:73`, `:106` callout + Step 6↔7 release
- `claude-code/skills/ywc-spec-validate/SKILL.md` — `:77`, `:238` callout
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — `:219` callout (497 줄, 초과분은 `references/subagent-directives.md`)
- `claude-code/skills/ywc-{code-gen,product-review,security-audit,ui-ux-review,tech-research,iac-author,infra-review}/SKILL.md` — callout
- `tests/named_agent_release_test.py` — 신규 gate test
- `scripts/validate.sh` — `:842` 패턴으로 test 연결

## Notes
- ywc-tech-research 는 `--compare` 분기에만 callout. ywc-code-gen 은 RED-first 순서 (`:121`) 이후 세 layer 모두 terminal 이 된 뒤 release.
- infra-review callout 은 "같은 turn 에 batch 로 dispatch 된 경우" 로 한정.
- `.githooks/pre-commit` 이 `scripts/validate.sh` 변경 시 full validate 를 실행한다 — commit 시 시간 소요 예상.
- Codex 측 계획 (`docs/ywc-plans/20261016-codex-issue69-selective-port.md`) 도 `scripts/validate.sh` 를 수정할 수 있으므로 착수 전 main 최신화.
- FM-5 (anchor 불일치로 링크 깨짐) 는 AC-1 의 `validate.sh` 로 검출.

## Parallel Execution Metadata

- Model Hint: sonnet — M3 default (Ownership 에 `tests/*.py`, `scripts/validate.sh` 포함으로 M2 불일치, Depended By 1 개로 M1 불일치)

### Ownership
- `claude-code/skills/references/subagent-async-monitoring.md`
- `claude-code/skills/CLAUDE.md`
- `claude-code/skills/ywc-impl-review/SKILL.md`
- `claude-code/skills/ywc-spec-validate/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/subagent-directives.md`
- `claude-code/skills/ywc-code-gen/SKILL.md`
- `claude-code/skills/ywc-product-review/SKILL.md`
- `claude-code/skills/ywc-security-audit/SKILL.md`
- `claude-code/skills/ywc-ui-ux-review/SKILL.md`
- `claude-code/skills/ywc-tech-research/SKILL.md`
- `claude-code/skills/ywc-iac-author/SKILL.md`
- `claude-code/skills/ywc-infra-review/SKILL.md`
- `tests/named_agent_release_test.py`
- `scripts/validate.sh`

### Owned Interface
- callout 형식: `> **Action required**: Read [../references/subagent-async-monitoring.md](../references/subagent-async-monitoring.md) now — … **Release (mechanical gate — do not skip)**: … `TaskStop` …` (물리적 한 줄)
- `python3 tests/named_agent_release_test.py` — 위반 0 이면 exit 0, 위반 시 non-zero + 위반 파일 목록

### Shared Surfaces
- `scripts/validate.sh` (Codex 측 계획과 공유)
- `claude-code/skills/CLAUDE.md`

### Conflicts With
- (None identified — Phase 가 hard gate 로 직렬화됨)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 tests/named_agent_release_test.py` exit 0 (AC-2)
- `grep -l "Action required.*subagent-async-monitoring" claude-code/skills/*/SKILL.md` → 10 개, impl-review / spec-validate 는 `grep -c` 2 (AC-3)
- `grep -c "^## On Every Signal\|^## Releasing Completed Named Agents" claude-code/skills/references/subagent-async-monitoring.md` → 2 (AC-4)
- `grep -c "outstanding dispatch" claude-code/skills/references/subagent-async-monitoring.md` ≥1 (AC-12 FR-A2/A3)
- `sed -n '/^## Subagent Async Monitoring Contract/,/^## Bundled/p' claude-code/skills/CLAUDE.md | grep -c "ywc-iac-author\|ywc-infra-review\|ywc-sequential-executor"` ≥4 (AC-15)
- `grep -rn "ScheduleWakeup(" claude-code/skills/references/subagent-async-monitoring.md` 출력 없음 (AC-18)
- `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Out of Scope
- Codex (`codex/`) 측 동일 변경
- infra-optimize / product-review·security-audit Phase 2 advisor / parallel-executor 4c.5 Cleaner (no-change 로 기록됨)
