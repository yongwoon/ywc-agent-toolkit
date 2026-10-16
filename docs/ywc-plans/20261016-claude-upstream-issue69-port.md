# Spec: develop-with-llm issue #69 Claude Code 반영분 포팅

- Source: <https://github.com/yongwoon/develop-with-llm/issues/69>
- Target: `claude-code/` (Claude Code 전용. `codex/`, `plugins/` 는 대상 외 — Codex 측은 `20261016-codex-issue69-selective-port.md` 가 별도 담당)
- Baseline revision: `614096d3` (`1.38.0`)
- Scale: **Large** (5 phase, 20+ skill 파일, 1 신규 test) — phase 별 1 PR 로 분할 진행
- Upstream 변경 출처: `gh pr diff <n> -R yongwoon/develop-with-llm` 중 `tools/claude-code/` 경로만 사용 (경로는 `tools/claude-code/` → `claude-code/` 로 치환). `git apply` 가 아닌 diff 를 읽고 수동 반영

## Global Constraints

`CLAUDE.md` (repo root) 에서 그대로 인용:

- "Every skill directory must contain: `SKILL.md` with `name:` and `description:` YAML frontmatter; `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md` (Tier 1, CI-enforced)"
- "The `description:` field drives activation — it must include trigger phrases users will type AND explicit "Do not use for..." anti-triggers to prevent false matches against sibling skills."
- "Keep SKILL.md under ~500 lines; extract long sections to `references/`."
- "Do not reference other skills with `@skill-name` (force-load) — it consumes excessive context. Reference by skill name only."
- Commit types: `feat`, `fix`, `docs`, `i18n`, `ci`, `chore`

Workspace `CLAUDE.md`: "Documentation: Korean", "Code (variables, functions, comments): English".

## Purpose

develop-with-llm 에서 2026-08~10 에 머지된 skill 개선 중, 이 저장소의 Claude Code skill 에 아직 없고 실제 운용상 효과가 있는 변경만 선별 반영한다. 특히 named subagent 가 완료 후에도 `idle` 로 남아 누적되는 문제(#290/#294)를 우선 해결한다.

## Scope

| Phase | Upstream PR | 반영 내용 |
|---|---|---|
| A | #290, #294, #241, #252(일부) | async monitoring 계약에 On Every Signal / ListAgents 재조회 생략 조건 / 매 signal stall 점검 / Releasing Completed Named Agents 추가. fan-out skill 에 `Action required` callout + inline `Release … TaskStop` 추가. 누락 검출 test 추가 |
| B | #257, #268, #266(spec-ready 부분) | spec-validate UI/Interaction Omission Check, ywc-plan `## Failure Modes`·`reuse`·prior-art seam, task-generator Spec coverage / Interface consistency / Right-Sizing, spec-ready Suggestion 자동 1회 pass |
| C | #258, #260(Impact 부분), #262 | create-pr Impact 섹션, gen-testcase Impact 시나리오 소스, impl-review SDK 예외 계층 검증 |
| D | #251 | ywc-project-scaffold `references/javascript.md` Fastify Small/Medium/Large |
| E | #263(description), #288(Claude 측, 적응), #282(Baseline 부분) | skill/agent trigger 경계 문구, Model Hint routing, command-bearing AC 의 Baseline |

## Out of Scope

- #240 (optimization batch, shared script 구조 상이) — issue 의 "Periodic Execution: script 분리" 검토와 함께 별도 진행
- #267, #279 (Codex 전용), #283 (screenshot / `pr-assets` 호스팅 필요), #237 (Postpone)
- #289 `ywc-task-executor`, #293 `ywc-docker-compose` 신규 skill — Open Questions 참조
- #260 의 Security lens 부분 (#259 `security-qa-lenses.md` 선행 필요) — Open Questions 참조
- #295: claude-code 변경이 bug-report 경로 1줄뿐이며 해당 문서가 이 저장소에 없음 → 반영 대상 없음
- #266 의 ywc-task-generator 부분: 이 저장소 task-generator 에는 preview 승인 단계 자체가 없음 (`claude-code/skills/ywc-task-generator/SKILL.md:296` Step 9 = Directory and File Generation) → 반영 대상 없음
- #252 의 `audit-schedulewakeup.py` hook: upstream repo 개발 세션용 `.claude/hooks/` 이며 `scripts/install.sh` 배포 대상이 아님
- #282 의 criticality / SCS profile / initializer / AC `Covers` 인용 / spec-ready regression repair
- #288 의 Escalation Ladder (`subagent-status-actions.md`), CI workflow 변경
- #294 의 `ywc-auth-implement/references/workflow-detail.md` (이 저장소에 파일 없음), `ywc-team-assemble` (skill 없음)
- #260 의 `ywc-gen-testcase/evals/evals.json` 변경 전체 (Security lens 전제)
- #282 의 `references/criticality.md`, `ywc-code-gen/references/qa-agent.md`, `ywc-impl-review/references/qa-agent.md`, `ywc-parallel-executor/references/rationalization-defense.md`
- `codex/`, `plugins/ywc-agent-toolkit/` 측 동기화 (`plugins/` 는 `scripts/sync-codex-plugin.sh` 로 `codex/skills` 에서만 생성됨)
- upstream 이 README 를 바꾸지 않은 skill 의 README 개편
- README Tier 2 (`README.zh.md` / `README.es.md`) 동기화 — `translation-check` 는 경고만 내며 merge 를 막지 않음. Tier 1 (md / en / ja / ko) 만 FR-E6 에서 갱신

## Existing Constraints Touched

| Site | 현재 동작 | Interaction |
|---|---|---|
| `claude-code/skills/references/subagent-async-monitoring.md:9-13` Full-Roster Reconciliation | roster listing capability 또는 자체 checklist 로 대조. 재조회 빈도 규정 없음 | extend (#241 재조회 판단 표) |
| `claude-code/skills/references/subagent-async-monitoring.md:29-31` Bounded Escalation | hard threshold 도달 시 BLOCKED 취급. `SendMessage` status-check 단계 없음 | extend (매 signal 마다 모든 outstanding dispatch 경과시간 점검만 추가. upstream 의 `SendMessage` 단계는 이 저장소 계약에 없으므로 도입하지 않음) |
| `claude-code/skills/references/subagent-async-monitoring.md` 전체 | `## On Every Signal`, `## Releasing Completed Named Agents` 없음 | extend |
| `claude-code/skills/ywc-impl-review/SKILL.md:73` | Step 3 Phase 1 5-way 병렬 dispatch, 계약을 prose 로 인용 (`Apply [...]`), `Action required` callout 아님 | extend → callout + Release |
| `claude-code/skills/ywc-impl-review/SKILL.md:106` | Step 4.5 Independent Verification Pass — finding 별 Sonnet verifier 동시 dispatch (최대 20), 계약을 prose 로 인용. verifier 실패 처리는 `:114` | extend → callout + Release |
| `claude-code/skills/ywc-impl-review/SKILL.md:117`, `:122`, `:124` | Step 5 Phase 2 advisor (순차로 기술), Step 6 Merge and Output Report, Step 7 Capture Learnings | Release 단계는 Step 6 과 Step 7 사이에 둔다 (Phase 1 lane + Step 4.5 verifier 모두 대상) |
| `claude-code/skills/ywc-spec-validate/SKILL.md:238` | Council voice 별 Opus subagent 를 독립 spawn (anti-anchoring, 결과 독립 수집) | extend → callout + Release |
| `claude-code/skills/ywc-iac-author/SKILL.md:70` | Step 3 Terraform module 별 `ywc-cloud-engineer` dispatch, "concurrent module dispatches" 명시 | extend → callout + Release |
| `claude-code/skills/ywc-infra-review/SKILL.md:55` | Steps 2–4 security / cost / reliability lens 3 subagent fan-out ("this skill dispatches three subagents") | extend → callout + Release (같은 turn 에 dispatch 될 때 batch) |
| `claude-code/skills/ywc-product-review/SKILL.md:89`, `claude-code/skills/ywc-security-audit/SKILL.md:68` | Phase 2 advisor: "for each surviving candidate" 후보별 bounded Opus 호출, 동시 실행 기술 없음 | no change needed — 단일 bounded advisor dispatch 계열 |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:245` | 4c.5 Cleaner — 각 task worker 내부에서 per-task 로 dispatch | no change needed — orchestrator batch 가 아니라 task worker 내부 단일 dispatch |
| `claude-code/skills/ywc-infra-optimize/SKILL.md:67`, `:85` | Step 1 / Step 3 순차 단일 dispatch | no change needed |
| `claude-code/skills/ywc-code-gen/SKILL.md:149` | Phase 2 Design Advisor — 후보별 bounded Opus 호출 | no change needed — 단일 bounded advisor dispatch 계열 |
| `claude-code/skills/ywc-skill-author/SKILL.md:213` | deletion test "Dispatch 3 + 3, blind" (6 subagent) | no change needed (이번 범위 외) — upstream #294 대상에 없던 skill-authoring 전용 pilot 이며 blind contrast 절차 변경은 별도 검토. 후속 후보로 Open Questions 6 에 기록 |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:219` | `4b-monitor (mechanical gate)` 문장으로 인용, Release 없음 | extend → callout + Release |
| `claude-code/skills/ywc-sequential-executor/SKILL.md:40`, `:214` | 단일 bounded Opus dispatch 로 인용 (batch 아님) | comply — no change needed |
| `claude-code/skills/ywc-code-gen/SKILL.md:119-126` | Backend/Frontend/QA subagent dispatch, 계약 인용 없음 | extend → callout + Release |
| `claude-code/skills/ywc-product-review/SKILL.md:64` | 5 perspective 병렬, 인용 없음 | extend |
| `claude-code/skills/ywc-security-audit/SKILL.md:46` | 3 OWASP subagent 병렬, 인용 없음 | extend |
| `claude-code/skills/ywc-spec-validate/SKILL.md:77` | 4 dimension 병렬, 인용 없음 | extend |
| `claude-code/skills/ywc-ui-ux-review/SKILL.md:84` | 2 subagent 병렬, 인용 없음 | extend |
| `claude-code/skills/ywc-tech-research/SKILL.md:89` | `--compare` option 별 병렬, 인용 없음 | extend |
| `claude-code/skills/ywc-auth-implement/SKILL.md:63-111` | Backend/Frontend/Doc dispatch 를 순서대로 기술, 병렬 명시 없음. `references/workflow-detail.md` 부재 | no change needed (upstream 은 2-way batch 였으나 이 저장소는 batch 로 기술되어 있지 않음) |
| `ywc-team-assemble` | 이 저장소에 없음 | no change needed |
| `claude-code/skills/CLAUDE.md:300-303` (prose 소비자 설명), `:322-323` (`Consumers:` 줄) | 소비자 = parallel-executor, sequential-executor, impl-review | extend — callout skill 10 개 + `ywc-sequential-executor` = 11 개로 갱신 |
| `scripts/validate.sh:842` | `python3 tests/codex_executable_resolution_test.py \|\| ERRORS=$((ERRORS + 1))` 형태로 test 연결 | reuse (같은 패턴으로 신규 test 연결) |
| `scripts/validate.sh:752` `check_loop_only_tool_calls` | `claude-code/skills/**/*.md` 의 `ScheduleWakeup(` 호출 문법을 거부 | comply — 신규 문구에 `ScheduleWakeup(` 를 쓰지 않는다 (금지 대상으로 도구명을 prose 로 언급하는 것은 허용) |
| `claude-code/skills/ywc-parallel-executor/SKILL.md` (497 줄), `:416` Step 5 Completion Report | Completion Report 는 SKILL.md 본문에 있음. `references/completion-report.md` 는 없음 | extend — Model Hint 표기는 Step 5 에 1 줄 pointer, 상세는 `references/model-routing.md`. 초과분은 `references/subagent-directives.md` 로 이동 |
| `claude-code/skills/ywc-task-generator/SKILL.md` (463 줄), `references/parallel-execution-metadata.md` | `## Parallel Execution Metadata` 규칙의 상세 reference. task-generator 에는 Completion Status (`DONE_WITH_CONCERNS`) 개념이 없음 | extend — Model Hint 할당 규칙 상세는 `references/parallel-execution-metadata.md` 에 두고 SKILL.md 는 pointer 만 |
| `claude-code/skills/ywc-spec-ready/SKILL.md:40`, `:85-95`, `:153` | Suggestion 잔존 시 사용자에게 y/n 질문 (`:153` Common Mistakes 의 "Auto-applying Suggestions" 항목 포함) | override (#266) — 세 곳 모두 정합화 |
| `claude-code/skills/ywc-plan/SKILL.md:273-283` Pass B, `references/spec-template.md:81` AC seam | `Failure Modes` 0건, Pass B 에 Baseline 행 없음 | extend (#268, #282) |
| `claude-code/skills/ywc-task-generator/SKILL.md:398-400` Step 11 Final Validation | Spec coverage / Interface consistency 항목 없음 (upstream 은 Step 12, 이 저장소는 Step 11) | extend — step 번호는 이 저장소 기준 유지 |
| `claude-code/skills/ywc-task-generator/references/README.md.template:39`, `:53`, `:66` | `Depended By` / `Parallel Execution Metadata` / `Owned Interface` 존재, `Criticality` 없음. `## Parallel Execution Metadata` 바로 아래는 bullet 이 아니라 `### Ownership` | extend (#288 Model Hint 를 `### Ownership` 앞의 단독 줄로 추가) |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:163`, `:191` | Agent Hint 로 `subagent_type` override | extend (Model Hint 는 `model` 파라미터이며 Agent Hint 와 독립) |
| `claude-code/skills/ywc-create-pr/SKILL.md:193` 6.5 Self-Review, `:243` 7 Create PR, `:264` diff 재조회 문구 | Impact 섹션 없음 | extend (#258) |
| `claude-code/skills/ywc-gen-testcase/SKILL.md:96`, `:195` | Impact 블록 미참조 | extend (#260 Impact 부분) |
| `claude-code/skills/ywc-impl-review/references/devex-agent.md:32` §3, `references/coderabbit-methodology.md:59` §4 | SDK 예외 계층 검증 없음 | extend (#262) |
| `claude-code/skills/ywc-project-scaffold/references/javascript.md:483` Express.js | Fastify 없음 | extend (#251) |

## Acceptance Criteria

Seam: 각 phase 의 검증 경계는 `bash scripts/validate.sh` 와 대상 파일 grep 이다. Prior art: `tests/codex_executable_resolution_test.py` (stdlib-only 회귀 test, `scripts/validate.sh:842` 에서 호출).

- [ ] AC-1 (전 phase): When `bash scripts/validate.sh` 를 각 phase branch 에서 실행하면, exit 0 으로 종료한다. Baseline: `0 — All checks passed.`
- [ ] AC-2 (A): When `python3 tests/named_agent_release_test.py` 를 실행하면, (a) `claude-code/skills/*/SKILL.md` 에서 `Action required` callout 으로 `subagent-async-monitoring.md` 를 인용하는 **모든 callout 줄 각각**이 같은 줄에 `Release … TaskStop` 을 포함하는지 검사해 위반 0 건으로 exit 0, (b) 내장 synthetic case (callout 만 있음 → 실패, 같은 줄 release → 통과, 다른 줄 release → 실패, callout 2 개 중 1 개만 release → 실패, prose 인용 → 대상 외) 가 모두 기대대로 판정된다. Baseline: unrunnable — 신규 파일
- [ ] AC-3 (A): When `grep -l "Action required.*subagent-async-monitoring" claude-code/skills/*/SKILL.md` 를 실행하면, ywc-impl-review / ywc-parallel-executor / ywc-code-gen / ywc-product-review / ywc-security-audit / ywc-spec-validate / ywc-ui-ux-review / ywc-tech-research / ywc-iac-author / ywc-infra-review 10 개가 출력되고, `grep -c` 로 ywc-impl-review 와 ywc-spec-validate 는 각각 2 줄이다. Baseline: `1 — no output` (callout 형태 인용 0 건)
- [ ] AC-4 (A): When `grep -c "^## On Every Signal\|^## Releasing Completed Named Agents" claude-code/skills/references/subagent-async-monitoring.md` 를 실행하면 `2` 가 출력된다. Baseline: `1 — 0`
- [ ] AC-5 (B): When `grep -c "Failure Modes" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md` 를 실행하면 두 파일 모두 ≥1 이다. Baseline: `1 — 두 파일 모두 0`
- [ ] AC-6 (B): When `grep -n "ask the user" claude-code/skills/ywc-spec-ready/SKILL.md` 를 실행하면 Suggestion pass 관련 질문 문구가 출력되지 않는다 (자동 1회 pass 로 대체). Baseline: `0 — :40, :87, :153 에 질문/advisory 문구 존재`
- [ ] AC-7 (B): When `test -f claude-code/skills/ywc-spec-validate/references/ui-qa-lenses.md` 를 실행하면 exit 0 이고, SKILL.md 가 상대경로 `references/ui-qa-lenses.md` 로 링크한다. Baseline: `1 — 파일 없음`
- [ ] AC-8 (C): When `grep -n "Impact" claude-code/skills/ywc-create-pr/SKILL.md claude-code/skills/ywc-gen-testcase/SKILL.md` 를 실행하면 create-pr Step 7 의 5 언어 heading 표와 gen-testcase 시나리오 소스 1번에 Impact 가 나타난다. Baseline: `1 — 두 파일 모두 0 hit`
- [ ] AC-9 (D): When `grep -c "^### Fastify" claude-code/skills/ywc-project-scaffold/references/javascript.md` 를 실행하면 `3` 이 출력되고 TOC 에 링크가 추가된다. Baseline: `1 — 0`
- [ ] AC-10 (E): When `grep -c "Model Hint" claude-code/skills/references/model-routing.md claude-code/skills/ywc-task-generator/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md` 를 실행하면 각각 ≥1 이다. Baseline: `2 — model-routing.md 없음`
- [ ] AC-11 (E): When `grep -n "Baseline:" claude-code/skills/ywc-plan/SKILL.md claude-code/skills/ywc-plan/references/spec-template.md claude-code/skills/ywc-spec-validate/SKILL.md` 를 실행하면 Pass B 행, Validation checklist, template AC 형식, spec-validate Feasibility 에 각각 나타난다. Baseline: `1 — 0 hit`
- [ ] AC-12 (A/B/C/E 보조): When 다음 grep 을 실행하면 각각 ≥1 hit 이다 — (FR-A2/A3) `grep -c "outstanding dispatch" claude-code/skills/references/subagent-async-monitoring.md`, (FR-B3) `grep -c "Spec coverage\|Interface consistency" claude-code/skills/ywc-task-generator/SKILL.md`, (FR-C3) `grep -c "exception hierarchy\|exception taxonomy" claude-code/skills/ywc-impl-review/references/devex-agent.md claude-code/skills/ywc-impl-review/references/coderabbit-methodology.md`, (FR-E1) `grep -c "manual verification testsheet" claude-code/agents/ywc-qa-engineer.md`. 여러 파일을 받는 `grep -c` 는 파일별 count 가 각각 ≥1 이어야 한다. Baseline: `1 — 네 명령 모두 0 hit`
- [ ] AC-13 (전 phase): When `wc -l` 을 각 phase 에서 수정한 모든 `claude-code/skills/*/SKILL.md` 에 실행하면 각 파일이 500 줄 이하이다. Baseline: `0 — parallel-executor 497, task-generator 463, create-pr 414, gen-testcase 397, plan 396, code-gen 346, spec-validate 313, impl-review 280, tech-research 174, spec-ready 162, iac-author 157, ui-ux-review 156, security-audit 143, infra-review 136, product-review 119 (모두 ≤500; 미수정 대상인 sequential-executor 는 501)`
- [ ] AC-14 (B): When `grep -c "exactly one suggestion-focused" claude-code/skills/ywc-spec-ready/SKILL.md` 를 실행하면 ≥1 이다 (FR-B4 의 자동 1회 pass 문구 존재 확인). Baseline: `1 — 0`
- [ ] AC-15 (A): When `sed -n '/^## Subagent Async Monitoring Contract/,/^## Bundled/p' claude-code/skills/CLAUDE.md | grep -c "ywc-iac-author\|ywc-infra-review\|ywc-sequential-executor"` 를 실행하면 ≥4 이다 (현재 sequential-executor 2 줄 + iac-author + infra-review). Baseline: `0 — 2 (sequential-executor 2 줄만)`
- [ ] AC-16 (E): When `grep -c "CLAUDE_CODE_SUBAGENT_MODEL" claude-code/skills/references/model-routing.md` 와 `grep -c "Model Hint" claude-code/skills/ywc-task-generator/references/README.md.template claude-code/skills/ywc-task-generator/references/parallel-execution-metadata.md` 를 실행하면 각 파일 ≥1 이다 (FR-E2 Version floor, FR-E3). Baseline: `2 — model-routing.md 없음; template/metadata 0`
- [ ] AC-17 (E): When `grep -c "Model Hint" claude-code/skills/ywc-parallel-executor/README.md claude-code/skills/ywc-parallel-executor/README.en.md claude-code/skills/ywc-parallel-executor/README.ja.md claude-code/skills/ywc-parallel-executor/README.ko.md` 와 같은 명령을 `ywc-task-generator` 에 실행하면 각 파일 ≥1 이다 (FR-E6). 그리고 `grep -c "repo-wide" claude-code/agents/ywc-refactor-cleaner.md`, `grep -c "spec-verification" claude-code/skills/ywc-code-gen/SKILL.md`, `grep -c "AI-generated" claude-code/skills/ywc-ui-ux-review/SKILL.md`, `grep -c "ROI" claude-code/skills/ywc-tech-research/SKILL.md`, `grep -c "ad-hoc threat-model" claude-code/skills/ywc-security-audit/SKILL.md` 가 각각 ≥1 이다 (FR-E1). Baseline: `1 — README 8 파일 모두 0, description grep 5 개 모두 0`
- [ ] AC-18 (A): When `grep -rn "ScheduleWakeup(" claude-code/skills/references/subagent-async-monitoring.md` 를 실행하면 출력이 없다 (FR-A8; 전체 검사는 AC-1 의 `validate.sh:752`). Baseline: `1 — no output` (현 상태도 통과 — 신규 문구 추가 후의 회귀 방지용)

## Functional Requirements

### Phase A — async monitoring / named agent release

- FR-A1 (AC-4): `subagent-async-monitoring.md` 에 `## On Every Signal` (Reconciliation → Bounded Escalation → 미해결 시 turn 종료 → batch 해소 후 Release 순서) 추가. 이 계약이 "2개 이상 동시 dispatch 하고 같은 session 이 완료를 기다리는 모든 batch" 에 적용된다는 범위 문단 추가 (#252).
- FR-A2: Full-Roster Reconciliation 에 #241 의 재조회 판단 표 추가 (terminal status 를 명시한 알림 → 재조회 불요 / 모호한 알림·batch 완료 시점 → 1회 재조회 / 매 알림 재조회 → anti-pattern).
- FR-A3: Bounded Escalation 에 "재조회 여부와 무관하게 매 signal 마다 모든 outstanding dispatch 의 경과시간을 점검" 추가.
- FR-A4: `## Releasing Completed Named Agents` 추가 (#290 본문 기반: 완료 후 `idle` 은 정상이며 escalation 대상 아님, batch 완료 + 결과 소비 후 name 별 `TaskStop(task_id=<name>)`, 현재 batch 한정, 조기 release 금지, 이미 종료된 agent 의 `TaskStop` 실패는 무시, `shutdown_request` 는 사용자 요청 시만, session 종료 직전이면 생략 가능, 출처 URL).
- FR-A5 (AC-3): 10 개 skill 의 concurrent batch dispatch 지점 12 곳 (impl-review `:73` Step 3 / `:106` Step 4.5, spec-validate `:77` Phase 1 / `:238` Council, parallel-executor `:219`, code-gen `:119`, product-review `:64`, security-audit `:46`, ui-ux-review `:84`, tech-research `:89`, iac-author `:70`, infra-review `:55`) 에 `> **Action required**: Read [../references/subagent-async-monitoring.md](../references/subagent-async-monitoring.md) now — …` callout 을 두고, **같은 물리적 한 줄**에 `**Release (mechanical gate — do not skip)**: … TaskStop …` 문장을 포함 (줄바꿈 금지). 기존 prose 인용 (`:73`, `:106`, `:219`) 은 callout 으로 대체. ywc-impl-review 는 Step 6 (Merge and Output Report) 과 Step 7 (Capture Learnings) 사이에 독립 release 단계를 추가해, Step 4.5 verifier 실패 처리 (`:114`) 와 Step 6 report 조립이 끝난 뒤 Phase 1 lane 과 Step 4.5 verifier 를 모두 release (#294 적응).
- FR-A6 (AC-2): `tests/named_agent_release_test.py` 신규 (stdlib only, `re.search` 사용). 실제 트리에서 callout 줄마다 Release 를 요구 + synthetic case 자가검증. `scripts/validate.sh` 에 `python3 tests/named_agent_release_test.py || ERRORS=$((ERRORS + 1))` 로 연결 (`:842` 패턴 재사용).
- FR-A7 (AC-15): `claude-code/skills/CLAUDE.md:300-303` 의 소비자 설명과 `:322-323` 의 `Consumers:` 줄을 callout skill 10 개 + `ywc-sequential-executor` (단일 bounded dispatch 소비자) 로 갱신.
- FR-A8 (AC-18): Phase A 의 모든 신규 문구는 `ScheduleWakeup(` 호출 문법을 포함하지 않는다 (`scripts/validate.sh:752`). `## On Every Signal` / `## Releasing Completed Named Agents` 는 기존 `## Waiting for Completion` 의 "turn 종료로 대기, polling 금지" 와 모순되지 않게 쓴다.

### Phase B — spec / plan

- FR-B1 (AC-7): `ywc-spec-validate/references/ui-qa-lenses.md` 신규 (10 lens 표), SKILL.md 에 UI/Interaction Omission Check 단계, Review Dimensions 매핑, rationalization 행 추가 (#257). upstream 의 Step 3.65 번호는 이 저장소 step 체계에 맞춘다.
- FR-B2 (AC-5): ywc-plan `must include` 목록, Pass A 행, Validation checklist 에 Failure Modes 추가. spec-template 에 `## Failure Modes` (FM-n 표, critical gap 규칙) + worked example 1행, Existing Constraints Touched interaction 에 `reuse`, AC seam 에 prior-art test 인용 요구 (#268).
- FR-B3 (AC-12): ywc-task-generator Final Validation (Step 11, `:398`) 에 Spec coverage / Interface consistency 항목, Principle 에 Right-Sizing 규칙 추가 (#268). 이 skill 에는 `DONE_WITH_CONCERNS` 상태 개념과 `references/output-and-validation.md` 가 없으므로, 미매핑 spec 항목은 Step 11 결과 요약에 `Unmapped spec items: <id 목록>` 으로 보고한다 (상태 체계 신설은 하지 않음).
- FR-B4 (AC-6): ywc-spec-ready Step 4 Handoff (`:85-95`), rationalization 행 (`:40`), Common Mistakes (`:153`) 를 "Suggestion 잔존 시 자동 1회 amendment pass → 재검증 → 결과와 무관하게 handoff" 로 변경 (#266).

### Phase C — PR / review

- FR-C1 (AC-8): ywc-create-pr 에 rationalization 행 (diff 재조회 금지), `:264` 를 "Step 6.5 에서 읽은 diff 재사용" 으로 변경, Step 7 에 optional Impact 섹션 (behavior change 판정, 5 언어 heading 표, template, diff 근거 한정) 추가 (#258).
- FR-C2: ywc-gen-testcase `:96` 에 Impact 블록 lift, `:195` 시나리오 소스에 Impact Before/After 추가 (#260 Impact 부분만). Security lens 문장과 eval case 6 은 제외.
- FR-C3: impl-review `devex-agent.md` §3 와 `coderabbit-methodology.md` §4 에 SDK 예외 계층 verify-before-surface 문단 추가 (#262).

### Phase D — scaffold

- FR-D1 (AC-9): `javascript.md` Express.js 뒤에 Fastify Small / Medium / Large 섹션과 Key Points, TOC 링크 추가 (#251 claude-code 판 기준).

### Phase E — trigger 경계 / model routing / Baseline

- FR-E1 (AC-12, AC-17): #263 의 description 변경을 이 저장소에 존재하는 대상에만 적용: `ywc-code-gen`, `ywc-security-audit`, `ywc-tech-research`, `ywc-ui-ux-review` SKILL.md description, `agents/ywc-qa-engineer.md`, `agents/ywc-refactor-cleaner.md` description, `ywc-product-review` verify-before-surface 문장. 추가하는 경계 문구의 식별 token: refactor-cleaner `repo-wide`, code-gen `spec-verification`, ui-ux-review `AI-generated`, tech-research `ROI`, security-audit `ad-hoc threat-model`, qa-engineer `manual verification testsheet`. skill description 은 `claude-code/skills/ywc-skill-author/SKILL.md:48` A15 ("`description` SHOULD be ≤80 words", CI 미강제 권고) 를 목표로 하되, 이미 80 단어를 넘는 description (ui-ux-review 86 단어) 은 이번 변경으로 늘어나는 단어 수만큼 기존 문구를 줄여 순증가 0 을 목표로 한다. agent description (`claude-code/agents/*.md`) 은 A15 적용 대상이 아니다.
- FR-E2 (AC-10, AC-16): `claude-code/skills/references/model-routing.md` 신규. M1 은 이 저장소에 Criticality 개념이 없으므로 "`Depended By` 의 task bullet ≥2 이고 `Owned Interface` 에 `(None` 으로 시작하지 않는 bullet 이 ≥1 → `opus`" 로 적응. M2 (문서/설정 전용 → `haiku`), M3 (`sonnet`) 는 upstream 대로. upstream 의 Version floor 문단 (`CLAUDE_CODE_SUBAGENT_MODEL` 이 구버전 Claude Code 에서 hint 를 덮어씀, 이는 오류가 아님) 과 effective model source 라벨 (`hint` / `frontmatter` / `env` / `default`) 을 포함. Escalation 관련 문단과 `escalated` 라벨은 제외.
- FR-E3 (AC-16): task-generator `references/README.md.template` 의 `## Parallel Execution Metadata` 바로 아래, `### Ownership` 앞에 단독 줄 `- Model Hint: <haiku|sonnet|opus> — <rule>` 을 추가. 할당 규칙 상세는 `references/parallel-execution-metadata.md` 에 추가하고, SKILL.md 에는 할당 단계 pointer 1 줄과 Step 11 Final Validation 항목 1 줄만 추가.
- FR-E4 (AC-10): parallel-executor Step 1 (`:156-163`) TaskInfo 파싱 목록에 Model Hint 추가, Step 3 (`:191`) Agent Hint override 다음에 Model Hint 처리 규칙 1 줄, Step 4b (`:211`) implementer dispatch 에서 `model` 전달 (Agent Hint 의 `subagent_type` override 와 독립), Step 5 Completion Report (`:416`) 에 task 별 `<model> (<source>)` 표기 1 줄. 규칙 상세는 `references/model-routing.md` 를 pointer 로 참조.
- FR-E5 (AC-11): #282 의 Baseline 부분만 반영: ywc-plan Pass B 행 + Validation 항목, spec-template AC 형식 (`Baseline: <exit> — <output>`), spec-validate Feasibility 의 Baseline 확인 (plain read command allowlist 로만 재실행, 부재 시 `missing-ac-baseline` Suggestion).
- FR-E6 (AC-17): upstream 이 README 를 바꾼 skill (parallel-executor, task-generator) 은 Tier 1 README (md / en / ja / ko) 를 함께 갱신. Tier 2 (zh / es) 는 Out of Scope.

## Non-Functional Requirements

- 각 수정 SKILL.md 는 500 줄 이하 유지 (AC-13). 초과 시 분리 대상: `ywc-parallel-executor` → `references/subagent-directives.md` (Step 4b 의 기존 dispatch 지시 문단), `ywc-task-generator` → `references/parallel-execution-metadata.md`, 그 외 skill → 해당 skill 의 기존 `references/` 파일.
- 신규 test 는 stdlib only, 외부 네트워크 불요.
- 각 phase PR 은 앞선 phase 가 머지된 base 위에서 작성한다. phase 간 파일 겹침이 있으므로 (Dependencies 참조) 개별 revert 는 역순 (E → A) 으로만 안전하다.

## Failure Modes

| ID | New path | Realistic failure | Covered by (AC / test / error handling) | User-visible? |
|---|---|---|---|---|
| `FM-1` | FR-A5 Release step | batch 결과 소비 전에 `TaskStop` → 결과 재요청 `SendMessage` 불가 | FR-A4 "조기 release 금지" + impl-review 독립 release 단계 (Step 6 과 Step 7 사이, Step 4.5 실패 처리 이후) | clear error (SendMessage 실패) |
| `FM-2` | FR-A6 test | 새 fan-out skill 이 callout 없이 prose 로만 계약을 인용 → gate 우회 | FR-A1 범위 문단이 batch dispatch 시 callout 사용을 요구. test 는 prose 인용을 단일 dispatch 로 간주 (의도된 한계) | silent — 수용, Open Questions 5 |
| `FM-3` | FR-E2 Model Hint | 사용자 환경의 `CLAUDE_CODE_SUBAGENT_MODEL` 이 hint 를 덮어씀 (구버전 Claude Code) | model-routing.md Version floor 문단 (FR-E2, AC-16) + parallel-executor Step 5 의 `<model> (<source>)` 표기 (FR-E4) | clear (report 에 source 표시) |
| `FM-4` | FR-B4 spec-ready | 자동 Suggestion pass 가 새 Critical 을 유발 | 1회 pass 후 재검증, handoff report 에 잔존 findings 표시 | clear |
| `FM-5` | 전 phase | upstream 문구의 Step 번호 / heading anchor 가 이 저장소와 불일치 → 깨진 링크 | AC-1 (`validate.sh`) + markdownlint CI | clear (CI 실패) |
| `FM-6` | FR-A5 callout | callout 이 두 줄로 줄바꿈되어 test regex 가 Release 를 인식하지 못함 | FR-A5 "같은 물리적 한 줄" 규칙 + AC-2 test 가 실패로 검출 | clear (CI 실패) |

## Edge Cases

- ywc-tech-research 는 `--compare` 미지정 시 단일 dispatch → callout 은 `--compare` 분기에만 둔다.
- ywc-code-gen 은 default 에서 QA subagent 를 먼저 dispatch 하는 RED-first 순서가 있음 (`:121`) → Release 는 세 layer 모두 terminal 이 된 뒤.
- 한 SKILL.md 에 해당 callout 이 여러 개면 (impl-review, spec-validate), **모든 callout 줄 각각**에 Release 가 있어야 통과 (upstream gate 의 "어느 한 줄" 규칙보다 엄격하게 적응 — Step 4.5 같은 두 번째 batch 의 누락을 잡기 위함).
- ywc-infra-review 의 lens 3 개가 서로 다른 turn 에 순차 dispatch 되는 경우에도 callout 의 Release 는 "batch 로 dispatch 된 경우" 에만 적용된다고 명시.

## Dependencies

- 진행 순서는 **A → B → C → D → E 필수** (각 phase 는 앞 phase 머지 후 착수).
- 파일 겹침:
  - A ↔ B: `ywc-spec-validate/SKILL.md` (A: callout, B: UI Omission Check)
  - A ↔ E: `ywc-parallel-executor/SKILL.md`, `ywc-code-gen/SKILL.md`, `ywc-security-audit/SKILL.md`, `ywc-tech-research/SKILL.md`, `ywc-ui-ux-review/SKILL.md`, `ywc-product-review/SKILL.md`
  - B ↔ E: `ywc-plan/SKILL.md`, `ywc-plan/references/spec-template.md`, `ywc-spec-validate/SKILL.md`, `ywc-task-generator/SKILL.md`
- Phase C 의 FR-C2 는 FR-C1 의 Impact 섹션을 전제 → 같은 PR.
- `scripts/validate.sh` 는 Codex 측 계획 (`20261016-codex-issue69-selective-port.md`) 도 수정할 수 있으므로, Phase A PR 작성 시 main 최신화 후 충돌 여부를 확인.

## Open Questions

1. #260 Security lens 부분 반영을 위해 PR #259 (`security-qa-lenses.md`) 를 범위에 추가할지 — 미결정, 현재 Out of Scope.
2. #289 `ywc-task-executor`, #293 `ywc-docker-compose` 신규 skill 반영 여부 — 미결정, 현재 Out of Scope.
3. #251 / #257 신규 파일 본문은 upstream 을 기준으로 하되, 이 저장소의 heading / Step 번호와 대조 후 조정 (구현 단계에서 확인).
4. #288 M1 을 Criticality 없이 적응하는 안 — Criticality 개념 도입 전까지의 잠정 규칙으로 둔다.
5. FM-2 의 prose 인용 우회를 test 로 막을지 (예: "in parallel" + 계약 미인용 SKILL.md 검출) — 오탐 위험으로 이번 범위에서는 제외.
6. `ywc-skill-author` deletion test (`SKILL.md:213`, 3 + 3 blind dispatch) 에도 Release 단계를 둘지 — 이번 범위 외, 후속 후보.

## References

- 이전 반영 PR: #193, #195, #196, #197, #198, #199, #200
- `docs/ywc-plans/20260925-small_install-and-agent-regression-gates.md` (validate.sh test 연결 선례)
- `docs/ywc-plans/20261016-codex-issue69-selective-port.md` (Codex 측 대응 계획)

## Amendment Log

### Iteration 1 — 2026-10-16

**Driven by**: DONE_WITH_CONCERNS, gate not re-scored (no design change), 6/11/6 findings
**Signatures**: `completeness:fr-b3-nonexistent-output-and-validation`, `completeness:fr-e4-nonexistent-completion-report`, `codecompat:impl-review-step45-verifier-fanout-omitted`, `codecompat:spec-validate-council-omitted`, `codecompat:iac-author-module-fanout-omitted`, `codecompat:infra-review-lens-fanout-omitted`

> Phase 2 advisor 후보 2 건 (Step 4.5 / Council 포함 여부, product-review·security-audit advisor) 은 repo 원문으로 판정: 원문이 동시 dispatch 를 명시한 곳만 포함하고, 후보별 bounded advisor 는 단일 dispatch 계열로 제외.

| Section edited | What changed | Why |
|---|---|---|
| `## Out of Scope` | 미반영 upstream 파일 (#294 workflow-detail, team-assemble, #260 evals, #282 reference 4 종), plugins 생성 경로, README Tier 2 처리 명시 | n/a — additive |
| `## Existing Constraints Touched` | impl-review `:106`/`:117-124`, spec-validate `:238`, iac-author `:70`, infra-review `:55` 를 extend 로 추가, product-review `:89`·security-audit `:68`·parallel-executor `:245`·infra-optimize 를 no-change 로 기록, CLAUDE.md 인용 `:300-303`/`:322-323` 로 정정, `validate.sh:752`, 줄 수와 실제 Completion Report 위치, template 구조 추가 | "`claude-code/skills/CLAUDE.md:303`, `:320` … extend (8 개 skill 로 갱신)" |
| `## Acceptance Criteria` | AC-2 를 callout 줄마다 Release 요구로 강화, AC-3 을 10 개 skill 로 확장, AC-12 다중 파일 count 규칙, AC-13~16 (줄 수, spec-ready 긍정 문구, CLAUDE.md 소비자, Model Hint/Version floor) 추가 | "ywc-impl-review / … / ywc-tech-research 8 개가 출력된다" |
| `## Functional Requirements` | FR-A5 대상 12 곳·한 줄 규칙·impl-review release 위치 (Step 6↔7), FR-A6 `re.search`, FR-A7 11 개 소비자, FR-A8 신설, FR-B3 Step 11 보고로 재지정, FR-E2 Version floor·M1 판정식, FR-E3 template 위치·metadata reference, FR-E4 실제 Step 3/5 위치, FR-E6 Tier 1 한정 | "`references/completion-report.md` 에 effective model 표기" |
| `## Non-Functional Requirements` | 500 줄 초과 시 분리 대상 파일 명시, revert 독립성 서술을 역순 revert 로 정정 | "phase 간 파일 의존은 B → E 의 ywc-plan / spec-template 뿐" |
| `## Failure Modes` | FM-1 release 시점 정정, FM-3 근거를 FR-E2/E4 로 연결, FM-6 (callout 줄바꿈) 추가 | "impl-review 독립 release 단계 (Step 6 이후)" |
| `## Edge Cases` | 복수 callout 규칙을 "모든 callout 줄" 로 변경, infra-review 순차 dispatch 경우 명시 | "적어도 하나의 callout 줄에 Release 가 있으면 통과" |
| `## Dependencies` | A→B→C→D→E 필수화, A↔B / A↔E / B↔E 파일 겹침, Codex 측 validate.sh 충돌 확인 추가 | "그 외 phase 는 서로 독립" |

### Iteration 2 — 2026-10-16

**Driven by**: DONE (Critical 0) — apply-suggestions pass, gate not re-scored (no design change), 0/4/3 findings
**Signatures**: `codecompat:fr-e4-taskinfo-step-misplaced`, `completeness:skill-author-dispatch-3plus3-unrecorded`, `feasibility:fr-e1-description-cap-unsourced`, `completeness:fr-e1-e6-a8-ac-gaps`, `completeness:code-gen-advisor-unrecorded`, `consistency:ac13-baseline-incomplete`, `consistency:fm-order`

> Suggestion pass 에 같은 iteration 의 Warning 4 건도 함께 반영 (모두 1~2 줄 정정, W1 은 실제 인용 오류).

| Section edited | What changed | Why |
|---|---|---|
| `## Functional Requirements` | FR-E4 위치를 Step 1 `:156-163` / Step 3 `:191` / Step 4b `:211` 로 정정, FR-E1 의 80 단어 근거를 `ywc-skill-author/SKILL.md:48` A15 로 명시 | "parallel-executor Step 3 (`:181`) TaskInfo 파싱에 Model Hint 추가" |
| `## Existing Constraints Touched` | `ywc-code-gen/SKILL.md:149` advisor, `ywc-skill-author/SKILL.md:213` 3 + 3 blind dispatch 를 no-change 행으로 추가 | n/a — additive |
| `## Acceptance Criteria` | AC-13 Baseline 에 수정 대상 전체 줄 수 기재, AC-17 (README Tier 1 / description 경계) · AC-18 (`ScheduleWakeup(` 부재) 추가 | n/a — additive |
| `## Failure Modes` | FM-6 행을 FM-5 뒤로 이동 | n/a — 순서 정리 |
| `## Open Questions` | 6 번 (skill-author deletion test Release) 추가 | n/a — additive |

### Iteration 3 — 2026-10-16

**Driven by**: DONE (Critical 0) — repair-suggestion-regression pass, gate not re-scored (no design change), 0/1/4 pass-introduced findings
**Signatures**: `feasibility:fr-e1-a15-80word-unachievable`, `consistency:fr-ac-tag-missing`, `consistency:ac-order`, `completeness:ac17-tokens-undefined-in-fr`, `completeness:ac18-vacuous-baseline`

| Section edited | What changed | Why |
|---|---|---|
| `## Functional Requirements` | FR-E1 에 식별 token 6 개 명시, A15 는 skill 만 대상·80 단어 초과 description 은 순증가 0 목표·agent 제외로 정정, FR-A8 / FR-E1 / FR-E6 에 AC 태그 추가 | "description 은 … A15 … 를 따른다 (CI 미강제 권고)" |
| `## Acceptance Criteria` | AC-17 / AC-18 을 AC-16 뒤로 이동, AC-18 Baseline 에 회귀 방지 용도 명시 | n/a — 순서·주석 정리 |
