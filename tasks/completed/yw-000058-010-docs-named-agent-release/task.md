# yw-000058-010-docs-named-agent-release — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] (Root task — no prerequisite)
- [ ] `main` 최신화 후 feature branch 생성 (`feature/<task-name>`)

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if a dependency task is not actually merged or its output contract is missing
- [ ] Stop if required changes spill into another task's Ownership
- [ ] Stop if the upstream diff hunk referenced in a step no longer matches this repo's section/step numbering in a way the spec did not anticipate
- [ ] Stop if a touched SKILL.md would exceed 500 lines and the designated `references/` split target cannot absorb it

## Implementation Steps
- [ ] 계약 확장 — `subagent-async-monitoring.md`
  - [ ] 적용 범위 문단 + `## On Every Signal` (Reconciliation → Bounded Escalation → 미해결 시 turn 종료 → batch 해소 후 Release) 추가 (FR-A1, upstream `cc-252`)
  - [ ] Full-Roster Reconciliation 에 재조회 판단 표 추가, Bounded Escalation 에 "매 signal 마다 모든 outstanding dispatch 경과시간 점검" 추가 (FR-A2/A3, upstream `cc-241`; `SendMessage` 단계 제외)
  - [ ] `## Releasing Completed Named Agents` 추가 (FR-A4, upstream `cc-290`). `## Waiting for Completion` 과 모순 금지, `ScheduleWakeup(` 문법 미사용 (FR-A8)
- [ ] callout + Release — 12 dispatch 지점
  - [ ] impl-review `:73`, `:106` / spec-validate `:77`, `:238` / parallel-executor `:219` / code-gen `:119` / product-review `:64` / security-audit `:46` / ui-ux-review `:84` / tech-research `:89` / iac-author `:70` / infra-review `:55` 에 단일 줄 callout (기존 prose 인용은 대체)
  - [ ] impl-review 에 Step 6 과 Step 7 사이 독립 release 단계 — Phase 1 lane + Step 4.5 verifier 모두 대상, Step 4.5 실패 처리 (`:114`) 이후 (FM-1)
  - [ ] parallel-executor 가 500 줄을 넘으면 Step 4b 기존 dispatch 지시 문단을 `references/subagent-directives.md` 로 이동
- [ ] gate test — `tests/named_agent_release_test.py`
  - [ ] stdlib only, `re.search` 로 `Action required.*subagent-async-monitoring\.md` 줄을 찾고 각 줄에 `Release.*TaskStop` 요구 (FM-6)
  - [ ] synthetic case: callout 만 → 실패 / 같은 줄 release → 통과 / 다른 줄 release → 실패 / callout 2 개 중 1 개만 → 실패 / prose 인용 → 대상 외 (FM-2 한계는 docstring 에 기록)
  - [ ] `scripts/validate.sh` 의 `:842` 근처에 `python3 tests/named_agent_release_test.py || ERRORS=$((ERRORS + 1))` 추가
- [ ] 소비자 목록 — `claude-code/skills/CLAUDE.md`
  - [ ] `:300-303` 설명과 `:322-323` `Consumers:` 줄을 callout skill 10 개 + `ywc-sequential-executor` 로 갱신 (FR-A7)

## Acceptance Coverage
Covers: AC-1, AC-2, AC-3, AC-4, AC-12 (FR-A2/A3 부분), AC-13, AC-15, AC-18

## Task Verify
- [ ] `python3 tests/named_agent_release_test.py` exit 0 (AC-2)
- [ ] `grep -l "Action required.*subagent-async-monitoring" claude-code/skills/*/SKILL.md` → 10 개, impl-review / spec-validate 는 `grep -c` 2 (AC-3)
- [ ] `grep -c "^## On Every Signal\|^## Releasing Completed Named Agents" claude-code/skills/references/subagent-async-monitoring.md` → 2 (AC-4)
- [ ] `grep -c "outstanding dispatch" claude-code/skills/references/subagent-async-monitoring.md` ≥1 (AC-12 FR-A2/A3)
- [ ] `sed -n '/^## Subagent Async Monitoring Contract/,/^## Bundled/p' claude-code/skills/CLAUDE.md | grep -c "ywc-iac-author\|ywc-infra-review\|ywc-sequential-executor"` ≥4 (AC-15)
- [ ] `grep -rn "ScheduleWakeup(" claude-code/skills/references/subagent-async-monitoring.md` 출력 없음 (AC-18)
- [ ] `bash scripts/validate.sh` 가 `All checks passed.` / exit 0 (AC-1)
- [ ] 수정한 모든 `claude-code/skills/*/SKILL.md` 에 `wc -l` → 각 500 줄 이하 (AC-13)

## Verification
- [ ] `bash scripts/validate.sh` passes (skill structure, README locale set, shellcheck, link and loop-only-tool checks)
- [ ] `npx markdownlint-cli2@0.22.1` on any changed `README*.md` passes (CI markdownlint scope)
- [ ] No `ScheduleWakeup(` call syntax introduced under `claude-code/skills/` (`scripts/validate.sh:752`)

## Implementation Notes (optional)

