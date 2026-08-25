# Claude Code Agentic Context Safety (ywc-agent-toolkit)

> Status: Draft
> Scale: Medium
> Created: 2026-08-12
> Author: ywc-plan
> Upstream source: `yongwoon/develop-with-llm` PR #206 — `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md`
> Sibling spec (codex root, Out of Scope here): [`20260812-codex-agentic-context-safety.md`](./20260812-codex-agentic-context-safety.md)
> Branch policy: 현재 branch(`feature/improve-skills-20260724`) 유지. 신규 branch 생성 없음.

## Purpose

Unattended loop(`ywc-agentic` → executor → `ywc-impl-review`)에 사용자 응답을 기다리는 지점이 두 곳 실재하며, 두 곳 모두 이미 문서화된 default가 있음에도 prompt를 연다. 또한 `ywc-impl-review`의 Phase 1 5-way fan-out에는 payload 상한이 없어, 부모가 읽은 spec 전문·diff 전문이 5개 subagent에 그대로 흘러갈 수 있다.

이 change set은 새 mechanism을 도입하지 않는다. 기존 flag pattern(`ywc-plan --non-interactive`), 기존 shared contract(`claude-code/skills/references/subagent-status-actions.md` §Return Payload Contract), 기존 compaction 문형(`ywc-sequential-executor` / `ywc-agentic`)을 재사용해 gap만 닫는다.

Upstream spec은 `develop-with-llm` repo의 `tools/claude-code/...` 기준이며, 본 repo는 `claude-code/...`다. 아래 **Existing Constraints Touched**의 `file:line`은 전부 본 repo에서 직접 확인한 값이다.

## Global Constraints

- 신규 문서는 한국어 기본, technical term은 English 유지 (`CLAUDE.md` §Language Conventions). 다만 편집 대상(`claude-code/skills/*/SKILL.md`, `claude-code/agents/*.md`)은 전부 영문이므로 **본문 편집은 영문**으로 한다.
- `claude-code/`와 `codex/`는 독립 관리한다. 한쪽 변경은 다른 쪽으로 자동 전파되지 않는다 (`CLAUDE.md` §Repository Structure).
- 모든 skill은 `SKILL.md` + `README.md` / `README.en.md` / `README.ja.md` / `README.ko.md`를 갖춰야 하며 `scripts/validate.sh:47`이 CI에서 강제한다. 대상 2개 skill은 `README.zh.md` / `README.es.md`도 보유하므로 함께 갱신한다.
- Agent frontmatter는 `name:` / `description:`을 반드시 포함한다 (`scripts/validate.sh:524,529`).
- Mechanical score baseline gate가 CI에 있다 — `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`가 점수 하락 시 실패하며, 정당한 변경은 baseline 재생성 후 commit해야 한다 (`.github/workflows/validate.yml:32-37`).
- Commit type은 `feat` / `fix` / `docs` / `i18n` / `ci` / `chore` (`CLAUDE.md` §Commit Conventions). PR title은 Conventional Commits를 따른다 (`pr-title-lint.yml`).
- 새 shared abstraction은 실제로 공통 책임을 줄일 때만 추가한다 — 추측성 generality 금지 (`claude-code/skills/references/readable-code.md` §G).

## Scope

- `ywc-impl-review` Phase 1 dispatch에 bounded payload 규칙 명시 + Return-payload contract directive verbatim 주입 (FR-1).
- `ywc-impl-review`에 `--non-interactive` flag 신설 — Step 7의 승격 prompt만 억제 (FR-2).
- `ywc-impl-review`를 **자동으로** 호출하는 **7개 지점**에 그 flag 전파 (FR-3).
- `ywc-sequential-executor`에 `--non-interactive` flag 신설 — External URL Policy 질문을 문서화된 `deny` default로 대체, 영속화하지 않음 (FR-4). `ywc-agentic` Step 5가 sequential 선택 시 forward.
- `ywc-refactor-cleaner` agent의 `Write` 사용 범위를 Mission / Boundaries / Anti-patterns에 명문화 (FR-5). `tools:` 행은 무변경.
- `ywc-parallel-executor`에 compaction 문단 신설 (FR-6).
- 신설 flag 2개는 사용자 노출 argument이므로 해당 2개 skill의 README 6 locale 갱신 (FR-7).

## Out of Scope

- `codex/` 아래 **모든 파일**. Root Independence상 자동 sync 대상이 아니며, 동일 취지의 codex 반영은 sibling spec `20260812-codex-agentic-context-safety.md`가 담당한다.
- Architecture invariants(upstream sibling spec `20260812-claude-code-architecture-invariants.md`) — 별도 검토 대상.
- **`§3.5` citation drift 일괄 정정.** 본 repo의 `claude-code/skills/references/subagent-status-actions.md`에는 `§3.5`라는 번호가 존재하지 않는다(headings: `## Status Responses` / `## Return Payload Contract` / `## BLOCKED Triage` / `## Aggregating Status`). 그럼에도 repo 전체에 `§3.5` 인용이 **36건** 있다. 이는 선행 결함이며 이번 요청 범위 밖이므로 **기존 36건은 손대지 않는다**. FR-1이 신규로 추가하는 인용만 section 이름(`§Return Payload Contract`)으로 정확히 적는다.
- `ywc-spec-validate` / `ywc-task-generator`의 동일 gap(둘 다 `subagent-status-actions` 참조 0건) — 같은 class이나 이번 요청이 요구하지 않으므로 아래 표에 기록만 한다.
- `ywc-sequential-executor:155` / `ywc-agentic:208`의 기존 compaction 문단에 chars/4 크기 신호 병기 — upstream FR-6이 근거로 삼은 `ywc-agent-legibility-audit` skill이 본 repo에 **존재하지 않으므로**(51개 skill 중 부재) 재사용할 표기 관례가 없다. 새 heuristic을 발명하지 않는다.
- 신규 shared reference 파일 생성. 기존 `subagent-status-actions.md` / `advisor-pattern.md`가 동일 보장을 제공한다.
- `.ywc-run-state.json` schema 변경, checkpoint/resume mechanics 변경.
- `ywc-parallel-executor`의 delivery-mode 선택 질문 — 유일한 unattended caller인 `ywc-agentic`이 Step 5에서 mode를 항상 명시 전달하므로 hang 경로가 성립하지 않는다.

## Existing Constraints Touched

모든 `file:line`은 `claude-code/` 이하 상대경로이며 본 repo에서 직접 확인했다.

| Existing artifact | Verified behavior | Interaction |
|---|---|---|
| `skills/ywc-impl-review/SKILL.md:42` `--skip-learnings` | 단일 flag가 Step 0 loading과 Step 7 capture를 **동시에** skip한다. prompt만 억제할 수단이 없다 | 그대로 유지. `--non-interactive`를 **직교 flag**로 신설해 Step 7만 억제 (FR-2) |
| `skills/ywc-impl-review/SKILL.md:54` Step 0 | `ywc-review-learnings --mode read`로 loading. "If the file is absent, proceed with an empty set — never block" | `--non-interactive`에서도 **무변경** — loading은 사용자 입력을 요구하지 않는다 |
| `skills/ywc-impl-review/SKILL.md:101` Step 7 | "offer to promote durable lessons … do not write learnings without the user-confirmation CHANGESET" — **사용자 응답 대기 지점** | `--non-interactive`일 때 offer를 열지 않고 후보를 report에만 기록. CHANGESET 없는 write 금지 invariant는 강화됨 (FR-2) |
| `skills/ywc-impl-review/SKILL.md:63` Step 2 말미 | "This context stays with the parent; do not forward it wholesale to **Phase 2**." — Phase 1 5-way fan-out에는 상한이 없는 것으로 읽힌다 | Phase 1도 포함하도록 확장 (FR-1) |
| `skills/ywc-impl-review/SKILL.md:72` Step 3 learnings 주입 | 이미 **"filtered to that aspect's category"** — aspect-scoped다 | **변경 없음.** upstream spec도 동일 결론 |
| `skills/ywc-impl-review/SKILL.md:74-76` Step 3 return artifacts | subagent가 Confirmed findings와 Advisor candidates(≤100줄 snippet)를 **inline 반환**하도록 규정. `subagent-status-actions` 참조 **0건** | Return-payload contract directive를 verbatim 주입하고, 본문은 파일로 쓰고 path만 반환하도록 조정 (FR-1) |
| `skills/references/subagent-status-actions.md:37` | "Why this contract exists" 목록에 **`ywc-impl-review`를 명시**한다 | 이 요구를 이행한다 |
| `skills/references/subagent-status-actions.md:39-41` | "every fan-out skill must inject the following directive **verbatim**" + directive 본문 1줄 | FR-1이 이 1줄을 그대로 인용 |
| `skills/references/subagent-status-actions.md` headings | `§3.5`라는 번호는 **존재하지 않는다** | 신규 인용은 `§Return Payload Contract`로 표기. 기존 36건은 Out of Scope |
| `skills/ywc-impl-review/SKILL.md:240` Integration | `pattern source`에 `advisor-pattern.md` / `coderabbit-methodology.md`만 등재 | `subagent-status-actions.md` 1건 추가 (FR-1) |
| `skills/ywc-spec-validate/SKILL.md`, `skills/ywc-task-generator/SKILL.md` | 두 skill도 `subagent-status-actions` 참조 0건 (grep: code-gen 2 / parallel 4 / sequential 4 / impl-review 0 / spec-validate 0 / task-generator 0) | **no change needed** — 동일 class이나 범위 밖 |
| `skills/ywc-sequential-executor/SKILL.md:119` External URL Policy | "If missing, ask the user **once** to choose `deny` (default), `allow`, or `allowlist`, then persist" — **유일한 Pre-flight 질문** | `--non-interactive`일 때 질문 없이 `deny` 적용, **persist하지 않음** (FR-4) |
| `skills/ywc-sequential-executor/references/external-url-policy.md` | `deny`가 문서화된 default이며 URL을 skip하고 skip 목록을 log한다 | 이 default를 그대로 채택. 새 default를 발명하지 않는다 |
| `skills/ywc-sequential-executor/SKILL.md:196` Allowed Stop Reasons | `flag conflict detected (Pre-flight)` 포함 | Non-interactive 경로는 stop을 **제거**하므로 목록 무변경 |
| `skills/ywc-sequential-executor/SKILL.md:337` Step 4.5 | `--review` 시 `/ywc-impl-review` 호출 (flag 없음) | `--non-interactive` 부착 (FR-3) |
| `skills/ywc-sequential-executor/SKILL.md:341` critical-path 강제 | "**regardless of whether `--review` was passed**" — `/ywc-impl-review` **및** `/ywc-security-audit` 강제 호출 | `--non-interactive` 부착 (FR-3). **upstream spec이 누락한 지점** |
| `skills/ywc-parallel-executor/SKILL.md:264` Step 4d | `/ywc-impl-review --spec <task-spec-path> --git-range <base-branch>..feature/<task-name>` | `--non-interactive` 부착 (FR-3) |
| `skills/ywc-parallel-executor/SKILL.md:257` critical-path 강제 | "regardless of `--review`" 강제 호출 | `--non-interactive` 부착 (FR-3). **upstream spec 누락 지점** |
| `skills/ywc-code-gen/SKILL.md:197` **Step 8** | `--review` 시 `/ywc-impl-review --spec <spec-path> --working-tree`. upstream spec의 "Step 7.5"는 본 repo에 없다 | `--non-interactive` 부착 (FR-3) |
| `skills/ywc-code-gen/SKILL.md:198` critical-path 강제 | "forced, **even without `--review`**" | `--non-interactive` 부착 (FR-3). **upstream spec 누락 지점** |
| `skills/ywc-agentic/SKILL.md:156` Step 6 | `ywc-impl-review --spec docs/ywc-plans/agentic-<slug>-iter1.md --git-range <pre-iter-sha>..HEAD` | `--non-interactive` 부착 (FR-3) |
| `skills/ywc-agentic/SKILL.md:148` Step 5 | executor를 **`--review` 없이** 호출하도록 명시 (Step 6이 review를 소유) | sequential 선택 시 `--non-interactive` forward (FR-4). `--review` 무부착 규칙은 무변경 |
| `skills/references/non-stop-execution.md` (executor 필수 선독) | 범위 실행 중 사용자 확인을 금지하고 허용 stop을 열거 | 이 변경은 stop 지점을 **줄이기만** 하므로 충돌 없음. 파일 무수정 |
| `skills/ywc-sequential-executor/SKILL.md:155` | Compaction 문단 **존재** (`.ywc-run-state.json` source of truth, ~30+ tasks trigger) | **no change needed.** 문형을 FR-6이 재사용 |
| `skills/ywc-agentic/SKILL.md:208` | Compaction 문단 **존재** (iteration 6 onward) | **no change needed** |
| `skills/ywc-parallel-executor/SKILL.md:142` Checkpoint and Resume | `.ywc-run-state.json`을 durable record로 규정하나 **compaction 문단 부재** (grep 확인). fan-out 폭이 가장 넓은 skill | 이 section 직후에 문단 신설 (FR-6) |
| `agents/ywc-refactor-cleaner.md:19` | `tools: [Read, Write, Edit, Bash, Grep, Glob]` | grant **유지**. 사용 범위만 제한 (FR-5) |
| `agents/ywc-refactor-cleaner.md:29` Mission | "surgical removal via the `Edit` tool with no adjacent re-formatting" — 삭제는 Edit 전용 | `Write`가 삭제 경로에 쓰이지 않음을 명문화 |
| `agents/ywc-refactor-cleaner.md:118-128` Anti-patterns | "Write the commit list + per-item evidence to a file under the parent's artifact directory" | **grant를 제거할 수 없는 근거.** 파일 산출이 계약 요구사항 |
| `agents/ywc-refactor-cleaner.md:45` Boundaries | "Will NOT" 8개 존재. `Write` 관련 항목만 **부재** | 항목 1개 추가 (FR-5) |
| `skills/ywc-plan/SKILL.md:17,99` | `--non-interactive`가 이미 확립된 flag 이름·의미(질문 금지 + 문서화된 default 적용) | 신설 flag 2개가 이 vocabulary를 재사용 |
| `scripts/validate.sh:47` | 각 skill에 `README.md` / `.en` / `.ja` / `.ko` 필수 | FR-7이 이를 충족 |
| `.github/workflows/validate.yml:32-37` | `score.py --ci`가 mechanical score 하락 시 실패 | Verification Plan에 baseline 재생성 절차 포함 |

## Acceptance Criteria

- [ ] **AC1 — Phase 1 bounded payload**: `ywc-impl-review` Step 2의 "do not forward it wholesale to Phase 2" 문장이 **Phase 1도 포함**하도록 확장되고, Step 3에 dispatch payload 제한(변경 파일 목록 + spec 파일 **경로** + 해당 aspect의 `references/*-agent.md` + 그 aspect로 filter된 learnings 만 전달, 나머지는 subagent가 스스로 Read)이 명시된다. 관측: 해당 두 문장이 `SKILL.md`에 존재.
- [ ] **AC2 — directive verbatim 주입**: Step 3이 `../references/subagent-status-actions.md` §Return Payload Contract의 directive 1줄을 **문자 그대로** 인용해 각 subagent prompt에 주입하도록 규정하고, Confirmed findings / Advisor candidates 본문은 파일로 쓰고 path만 반환하도록 조정한다. 관측: `grep -c "Return-payload contract" skills/ywc-impl-review/SKILL.md` ≥ 1 **그리고** `grep -c "subagent-status-actions" skills/ywc-impl-review/SKILL.md` ≥ 2 (Step 3 + Integration). 현재 각각 0.
- [ ] **AC3 — Phase 2 무변경**: Phase 2의 기존 payload 규칙(`SKILL.md:95` "Context payload")과 advisor budget(기본 5)이 diff에 나타나지 않는다.
- [ ] **AC4 — impl-review non-interactive Step 7**: `--non-interactive`로 실행하면 Step 7이 승격 여부를 묻지 않고 종료하며, report에 `Learning candidates (not promoted — non-interactive)` block이 존재한다. 관측: transcript에 `AskUserQuestion` 0회, report에 해당 block 존재.
- [ ] **AC5 — Step 0 loading 보존**: `--non-interactive`만 준 실행과 flag 없는 실행이 learnings 주입 여부에서 동일하다. 관측: Step 0 서술이 diff에 나타나지 않는다.
- [ ] **AC6 — `--skip-learnings` 직교성**: `--skip-learnings` 행(`SKILL.md:42`) 문구가 diff에 나타나지 않는다. 두 flag 동시 지정 시 Step 0·Step 7 모두 skip되며, 그 조합 semantics는 신설 `--non-interactive` 행과 Step 7 본문에만 기술된다.
- [ ] **AC7 — caller 7곳 전파**: 아래 7개 지점 전부가 `--non-interactive`를 포함한다.
  - `ywc-sequential-executor` `:337`(`--review`), `:341`(강제)
  - `ywc-parallel-executor` `:264`(`--review`), `:257`(강제)
  - `ywc-code-gen` `:197`(`--review`), `:198`(강제)
  - `ywc-agentic` `:156`
- [ ] **AC8 — 사용자 직접 호출 불변**: 사용자가 `/ywc-impl-review`를 직접 타이핑하면 flag가 없으므로 기존 interactive 동작 그대로다. 관측: Arguments 표에서 flag가 opt-in으로 문서화되고 default가 interactive임이 명시된다.
- [ ] **AC9 — external URL non-interactive default**: `taskExecutor.externalSpecUrls`가 **없는** 상태에서 `ywc-sequential-executor --non-interactive`를 실행하면 질문 없이 `deny`를 적용하고 Completion Report에 `External URL policy: deny (assumed — non-interactive, not persisted)`를 출력한다. 관측: 실행 후 `.claude/settings.local.json`에 `taskExecutor` key가 **생성되지 않음**.
- [ ] **AC10 — external URL 기존 경로 불변**: key가 이미 있으면 mode와 무관하게 silently 사용하고, `--non-interactive` 없이 key가 없으면 기존대로 1회 질문 후 persist한다. 관측: `SKILL.md:119`의 기존 두 분기 문장이 삭제되지 않고 세 번째 분기만 추가된다.
- [ ] **AC11 — agentic forward**: `ywc-agentic` Step 5가 sequential executor 선택 시 `--non-interactive`를 전달하고, parallel 선택 시에는 전달하지 않으며, 기존 "`--review` 없이 호출" 규칙(`:148`)이 유지된다.
- [ ] **AC12 — refactor-cleaner Write 범위**: Boundaries "Will NOT" 목록에 다음 취지의 항목이 존재한다 — "does NOT use `Write` for production source or any file outside the parent's artifact directory; if such a need arises, return `DONE_WITH_CONCERNS` to the parent instead." (`DONE_WITH_CONCERNS` 단어 필수). Mission이 evidence artifact를 `Write`의 유일한 용도로 명시하고, Anti-patterns에 "삭제 대신 `Write`로 파일 통째 재작성" 행이 추가된다. frontmatter `tools:` 행(`:19`)은 **무변경**.
- [ ] **AC13 — agent 6 section 유지**: `ywc-refactor-cleaner.md`의 Mission / Triggers / Boundaries / Success Criteria / Return Contract / Anti-patterns 6개 section의 존재와 순서가 유지되고, Return Contract는 inline 재정의 없이 참조만 유지한다.
- [ ] **AC14 — parallel compaction 문단**: `ywc-parallel-executor/SKILL.md`에 `.ywc-run-state.json` + 완료 task artifact를 source of truth로 삼는 compaction 문단이 존재하고, 완료 wave당 1줄 digest 규율과 advisory 성격이 명시되며, **새 stop condition을 도입하지 않는다**. 관측: `grep -ci "compaction" skills/ywc-parallel-executor/SKILL.md` ≥ 1 (현재 0).
- [ ] **AC15 — README locale 갱신**: `ywc-impl-review`와 `ywc-sequential-executor` 각각의 `README.md` / `.en` / `.ja` / `.ko` / `.zh` / `.es` 6개 파일에 신설 flag가 반영된다.
- [ ] **AC16 — CI gate 통과**: `bash scripts/validate.sh` exit 0, `npx markdownlint-cli2` 통과, `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 통과(필요 시 baseline diff archive 후 재생성 커밋).
- [ ] **AC17 — codex root 무변경**: diff에 `codex/` 경로가 **0건** 등장한다. 관측: `git diff --name-only main...HEAD | grep -c '^codex/'` 가 `0`.

## Functional Requirements

### FR-1: `ywc-impl-review` Phase 1 bounded payload + return-payload directive

`skills/ywc-impl-review/SKILL.md`의 Step 2 · Step 3 · Integration을 수정한다.

- Step 2(`:63`) 말미 문장을 **Phase 1도 포함**하도록 확장한다. 부모가 읽은 spec/코드 전문은 부모 context에 남고, subagent에는 경로와 범위만 전달한다.
- Step 3에 dispatch payload 제한을 명시한다. 각 subagent는 (a) 변경 파일 목록 + spec 파일 **경로**, (b) 자기 aspect의 `references/*-agent.md`, (c) 자기 aspect로 filter된 learnings 만 받고, **필요한 파일은 스스로 Read**한다. 다른 subagent의 결과·전체 project context·다른 aspect의 rubric은 전달하지 않는다.
- Step 3에 `../references/subagent-status-actions.md` §Return Payload Contract의 directive를 **verbatim 인용**해 각 subagent prompt에 주입하도록 규정한다. Confirmed findings와 Advisor candidates의 본문은 파일로 쓰고, 부모는 report 조립 시 읽는다. Phase 2 escalation용 bounded snippet(≤100줄)은 candidate 파일 안에 두고, 부모는 budget 통과 항목에 대해서만 읽는다.
- Integration(`:240`)의 `pattern source`에 `subagent-status-actions.md`를 추가한다.
- Phase 2의 기존 payload 규칙과 advisor budget은 **변경하지 않는다**.
- 인용 anchor는 `§Return Payload Contract`(section 이름)로 적는다 — 본 repo의 reference에 `§3.5` 번호가 없기 때문이다. 기존 36건의 `§3.5` 인용은 손대지 않는다(Out of Scope).

### FR-2: `ywc-impl-review --non-interactive`

Arguments 표에 flag 1행을 추가한다.

- 의미: **Step 7의 사용자 확인 prompt를 열지 않는다.** Step 0(loading), Phase 1, Phase 2, report 생성은 전부 무변경.
- Step 7 서술을 두 갈래로 나눈다.
  - Interactive(기본): 현행 문구 유지.
  - Non-interactive: offer를 생략하고 후보를 report의 `Learning candidates (not promoted — non-interactive)` block에 기록한 뒤 종료.
- block schema (report 표면):

  ```text
  ### Learning candidates (not promoted — non-interactive)
  - [Architecture] Occurrences in this review: 3 — <finding 1-line summary> (severity: High) — would promote to docs/review-learnings.md as DO-NOT
  - [Security] Occurrences in this review: 2 — <finding 1-line summary> (severity: Medium) — would promote to references/recurring-defects.md as cross-project
  (none)   <- 해당 항목이 없을 때
  ```

  - field 순서 고정: `[<aspect>] Occurrences in this review: <n> — <finding 1-line summary> (severity: <값>) — would promote to <target file> as <learning type>`.
  - `<aspect>`는 Phase 1의 5축(Architecture / Design / Devex / Security / QA) 중 하나.
  - **`Occurrences in this review`는 단일 invocation 내 카운트다.** cross-invocation recurrence는 사람이 확인하는 Step 7 승격 flow가 확립하는 값이므로 non-interactive에는 데이터 출처가 없다. 두 Confirmed finding은 (a) 같은 aspect이고 (b) report 조립 단계의 판단으로 같은 defect class일 때 같은 occurrence로 센다 — `references/*-agent.md`에 controlled-vocabulary tag가 없으므로 이는 조립자의 분류 판단이며, tag 도입은 범위 밖이다. aspect가 다르면 증상이 유사해도 병합하지 않는다. `<n>` = 1인 항목은 block에 싣지 않는다(block의 목적이 run 내 **반복** pattern 표면화이므로).
- `docs/review-learnings.md`와 `references/recurring-defects.md`에 대한 **write는 어느 mode에서도 발생하지 않는다** — CHANGESET 확인 없는 write 금지 invariant는 강화되기만 한다.
- `--skip-learnings`와 직교한다. 조합 semantics는 신설 행과 Step 7 본문에만 기술하고, `:42` 행 문구는 수정하지 않는다.
- flag 이름은 `ywc-plan --non-interactive`(`skills/ywc-plan/SKILL.md:17,99`)에서 **"질문을 열지 않는다"는 절반만** 재사용한다. FR-2는 어떤 default 값도 적용하지 않고 아무것도 write하지 않는다는 점에서 ywc-plan의 "문서화된 default 적용" 절반과는 다르다.

### FR-3: 자동 호출 caller 7곳의 flag 전파

`ywc-impl-review`를 **자동으로** 호출하는 7개 지점이 `--non-interactive`를 항상 전달한다.

| Caller | 위치 | 현재 호출 | 조치 |
|---|---|---|---|
| `ywc-sequential-executor` | `:337` Step 4.5 (`--review`) | `/ywc-impl-review` (flag 없음) | 문장 내 명령을 `/ywc-impl-review --non-interactive`로 |
| `ywc-sequential-executor` | `:341` critical-path 강제 | `/ywc-impl-review` **and** `/ywc-security-audit` | impl-review 호출에만 flag 부착 |
| `ywc-parallel-executor` | `:264` Step 4d 코드블록 | `/ywc-impl-review --spec … --git-range …` | 코드블록 끝에 `--non-interactive` 리터럴 추가 |
| `ywc-parallel-executor` | `:257` critical-path 강제 | `/ywc-impl-review` **and** `/ywc-security-audit` | impl-review 호출에만 flag 부착 |
| `ywc-code-gen` | `:197` Step 8 (`--review`) | `/ywc-impl-review --spec <spec-path> --working-tree` | 표 셀에 `--non-interactive` 추가 |
| `ywc-code-gen` | `:198` critical-path 강제 | `/ywc-impl-review --spec <spec-path> --working-tree` **and** `/ywc-security-audit` | impl-review 호출에만 flag 부착 |
| `ywc-agentic` | `:156` Step 6 코드블록 | `ywc-impl-review --spec … --git-range <pre-iter-sha>..HEAD` | 코드블록 끝에 `--non-interactive` 리터럴 추가 |

- 조건 분기를 두지 않는다: 7곳 모두 loop step으로서의 자동 호출이며, executor의 Non-Stop Execution Principle과 `ywc-agentic`의 자율 loop 계약이 이미 이 지점의 prompt를 금지한다. flag 부착은 기존 규칙의 **집행**이다.
- `/ywc-security-audit` 호출에는 flag를 부착하지 않는다 — 그 skill에 해당 flag가 없으며 이번 범위 밖이다.
- 각 caller의 status routing 문단(`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`)은 변경하지 않는다.

### FR-4: `ywc-sequential-executor --non-interactive` (External URL Policy)

Arguments 표에 flag를 추가하고 External URL Policy(`:119`)를 3분기로 만든다.

- key가 **있으면**: mode와 무관하게 기존대로 silently 사용.
- **없고** `--non-interactive`가 **없으면**: 기존대로 1회 질문 후 persist.
- **없고** `--non-interactive`가 **있으면**: 질문 없이 문서화된 `deny` default를 적용한다. **파일에 persist하지 않는다** — 가정은 이번 run 한정이며, 사용자가 나중에 interactive 실행에서 진짜 결정을 내릴 수 있어야 한다. Completion Report에 `External URL policy: deny (assumed — non-interactive, not persisted)`를 기록하고, Step 1b에서 skip된 URL 목록을 기존 `deny` 동작대로 log한다.
- key가 **존재하지만** `allow` / `deny` / `allowlist` 중 어느 것도 아닌 값일 때: **key 부재와 동일하게 취급하되 이번 run 한정**이며, malformed 값을 강제 변환하거나 persist하지 않는다. 두 mode 모두 Completion Report에 `External URL policy: malformed value "<value>" — treated as absent for this run`을 기록한다. interactive 분기가 재질문할 때는 기존 값이 무효라 교체됨을 먼저 알린 뒤 묻는다. 이는 `external-url-policy.md`에 없는 **신규 규칙**이며, 이 spec이 도입한다.
- Allowed Stop Reasons(`:196`)는 변경하지 않는다 — 이 변경은 stop을 제거하기만 한다.
- `ywc-agentic` Step 5가 **sequential** 선택 시 `--non-interactive`를 함께 전달한다. `--review`를 부착하지 않는 기존 규칙(`:148`)은 유지한다. `ywc-parallel-executor`는 이 flag를 갖지 않는다.
- `--dry-run`과 조합 시 flag는 계획 출력에 한 줄로 반영되고 별도 동작 변화는 없다.

### FR-5: `ywc-refactor-cleaner`의 `Write` 사용 범위 명문화

`agents/ywc-refactor-cleaner.md`를 수정한다. **frontmatter `tools:` 행(`:19`)은 변경하지 않는다.**

- 근거: Anti-patterns(`:128`)가 evidence 파일 산출을 요구하므로 `Write` grant 제거는 계약 위반이다. grant 제거안은 검토 후 기각한다.
- Mission에 한 문장 추가: 삭제는 `Edit` 전용이며, `Write`의 유일한 정당 용도는 parent artifact directory 아래의 per-item evidence 파일이다.
- Boundaries "Will NOT"에 항목 1개 추가 (AC12의 문구, `DONE_WITH_CONCERNS` 포함).
- Anti-patterns 표에 행 1개 추가: "삭제 대신 `Write`로 파일을 통째로 재작성" — bisect 대상 오염 + Mission의 Edit-only 규정 위반, 대체 행동은 `Edit` 기반 surgical 삭제.
- `permissionMode`는 추가하지 않는다 (Coder tier에는 부적합).
- 6개 필수 section의 순서·존재를 유지한다.

### FR-6: `ywc-parallel-executor` compaction 문단 신설

`skills/ywc-parallel-executor/SKILL.md`의 Checkpoint and Resume section(`:142-144`) 직후에 문단을 신설한다.

- `.ywc-run-state.json`과 각 task의 `tasks/completed/<id>/` artifact를 source of truth로 삼고, 완료 wave당 1줄 digest만 작업 context에 유지하며 세부는 필요 시 재독한다.
- `ywc-sequential-executor:155`의 문형을 재사용한다 — 새 mechanism을 만들지 않는다.
- **advisory**이며 새 stop condition을 도입하지 않음을 문장에 명시한다.
- chars/4 크기 신호는 넣지 않는다 (Out of Scope 참조).

### FR-7: README locale 갱신

신설 flag 2개는 사용자 노출 argument이므로 아래 12개 파일을 갱신한다.

- `skills/ywc-impl-review/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md` — `--non-interactive` 설명 추가
- `skills/ywc-sequential-executor/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md` — `--non-interactive` 설명 추가 및 External URL 관련 기존 문구(`README.md:115` 등)와의 정합

`README.md`는 한국어, `README.en.md`는 영어 원본, 나머지는 해당 언어. 번역 정합은 `translation-check.yml`(informational)이 경고한다.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Backward compatibility | 신설 flag 2개는 모두 opt-in. flag 없이 실행하면 현재 동작이 그대로 유지되며 `--skip-learnings` 문구와 `.ywc-run-state.json` schema는 변경되지 않는다 |
| Determinism | non-interactive 경로가 적용하는 default는 이미 문서에 존재하는 값(`deny`)뿐이다. 새 default를 발명하지 않는다 |
| Automation safety | 자동화 run은 사용자 입력을 기다리지 않는다. 필수 입력 부재 시의 정지는 기존 `BLOCKED` / `NEEDS_CONTEXT` 경로를 그대로 사용한다 |
| Context safety | Phase 1·Phase 2 dispatch 모두 bounded payload를 전달하며 transcript·full diff·chain-of-thought는 전달하지 않는다 |
| Scope discipline | 새 shared reference 파일을 만들지 않는다. 기존 `subagent-status-actions.md` / `advisor-pattern.md` / 기존 compaction 문형을 재사용한다 |
| Auditability | non-interactive에서 억제된 상호작용(learnings 승격 후보, external URL 가정)은 전부 report에 흔적을 남긴다. 조용한 억제는 허용하지 않는다 |
| Root independence | `codex/` 아래 어떤 파일도 추가·수정하지 않는다 (AC17) |
| Verification/Testability | 이 change set은 prompt 문서 수정이므로 자동 테스트 harness가 없다. **실행**: `--non-interactive` 실행 1회씩(impl-review, sequential-executor)의 transcript를 확인한다. **확인 대상**: `AskUserQuestion` 호출 0회, `Learning candidates (not promoted — non-interactive)` block 존재, `External URL policy: deny (assumed …)` 로그 존재를 육안 확인한다. 구조적 항목(AC1/AC2/AC7/AC12/AC14/AC17)은 grep으로 기계 확인한다 |

## Critical Surfaces

N/A — no critical surface. 이 change set은 skill/agent의 prompt 문서만 수정하며 auth·payment·secret·PII 코드 경로를 포함하지 않는다. `--non-interactive`는 사용자 확인을 억제하지만 **write 권한을 확대하지 않는다** — FR-2는 learnings write 경로를 제거하는 방향이고, FR-4는 더 제한적인 default(`deny`)를 적용하며 결정을 영속화하지 않는다. FR-5는 오히려 `Write` 사용 범위를 좁힌다.

## Data Model

N/A — no data model change. `.claude/settings.local.json`은 FR-4에서 **읽기만** 하며 non-interactive 경로는 쓰지 않는다. `.ywc-run-state.json` schema는 무변경.

## API Contract

External API 변경 없음. 신설 CLI flag 2개는 skill argument 표에 문서화되는 사용자 인터페이스다.

| Skill | Flag | Type | Default | Description |
|---|---|---|---|---|
| `ywc-impl-review` | `--non-interactive` | flag | 미설정 = interactive | Step 7의 learnings 승격 prompt를 열지 않고, 후보를 report의 `Learning candidates (not promoted — non-interactive)` block에 기록한다. Step 0 loading은 영향받지 않는다 |
| `ywc-sequential-executor` | `--non-interactive` | flag | 미설정 = interactive | Pre-flight의 External URL Policy 질문을 열지 않고 문서화된 `deny` default를 이번 run 한정으로 적용한다(영속화하지 않음) |

## Edge Cases

- **`--non-interactive` + `--skip-learnings` 동시 지정**: Step 0과 Step 7 모두 skip. `--skip-learnings`가 상위 개념이며 충돌이 아니다. report에는 loading skip 사실만 기록하고 `Learning candidates (not promoted — non-interactive)` block은 출력하지 않는다(수집 근거가 없으므로).
- **`--non-interactive` 실행에서 해당 finding이 0건**: block을 `(none)`으로 출력한다. block 자체를 생략하지 않는다 — Auditability NFR 때문.
- **`docs/review-learnings.md`가 존재하되 entry 0건**: 파일 부재 case와 report 표면상 동일하게 취급한다 — loaded 건수 `0`, "Applicable Review Learnings" block은 빈 상태로 생성.
- **`ywc-review-learnings`가 `BLOCKED` 반환**: 기존 Step 0 규칙("파일 부재 시 empty set, 절대 block하지 않는다")을 그대로 적용한다. non-interactive라고 review 자체를 중단하지 않는다.
- **`--non-interactive` sequential run에서 `externalSpecUrls`가 `allowlist`인데 allowlist가 비어 있음**: 기존 파일 값이 존재하므로 그 값을 사용한다(빈 allowlist = 전부 skip). default로 덮어쓰지 않는다.
- **`deny` 적용 결과 task의 Primary Sources가 전부 external URL**: Step 1b 기존 규칙대로 Summary와 project-relative path로 진행하고 skip 목록을 log한다. `--non-interactive` 때문에 새로 `BLOCKED` 처리하지 않는다.
- **사용자가 `/ywc-impl-review --non-interactive`를 직접 타이핑**: 정상 동작. 자동 caller 전용 flag가 아니며 CI에서의 수동 사용도 지원한다.
- **`Criticality: critical` task가 unattended agentic run 안에서 impl-review를 강제 실행**: FR-3에 의해 `--non-interactive`가 부착되므로 Step 7이 loop를 멈추지 않는다. 이것이 이 spec이 닫는 **주된 hang 경로**다 — `ywc-agentic` → executor(`--review` 미지정) → critical task → forced impl-review → Step 7 prompt.
- **`ywc-refactor-cleaner`가 evidence 파일을 쓸 artifact directory를 parent가 지정하지 않음**: 기존 `NEEDS_CONTEXT` 경로로 반환한다. `Write` 범위 제한 때문에 임의 경로를 고르지 않는다.
- **`--dry-run` + `--non-interactive` (sequential)**: 계획만 출력하고 아무 파일도 쓰지 않는다. External URL 가정은 계획 출력에 한 줄로 표시된다.
- **mechanical score baseline 하락**: `score.py --ci` 실패 시 diff를 archive한 뒤 baseline을 재생성해 같은 PR에 commit한다.

## Dependencies

- 기존 `claude-code/skills/references/subagent-status-actions.md` §Return Payload Contract — FR-1이 참조·주입.
- 기존 `claude-code/skills/references/advisor-pattern.md` — FR-1이 Phase 1 규칙을 이 문서와 정합하게 맞춘다.
- 기존 `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md` — FR-4의 `deny` default 출처.
- 기존 `claude-code/skills/ywc-plan/SKILL.md:17,99` — `--non-interactive` vocabulary 출처.
- CI: `scripts/validate.sh`, `markdownlint.yml`, `.claude/skills/ywc-toolkit-eval/scripts/score.py --ci`, `pr-title-lint.yml`.
- 외부 library 의존 없음. Database 없음.

## Open Questions

N/A — none identified. 신설 flag 2개는 프로젝트에 이미 존재하는 `--non-interactive` semantics를 재사용하고, 적용되는 default는 기존 문서에 명시된 값(`deny`)이며, 새 persistent state나 schema를 도입하지 않는다.

## Implementation Phases

1. **impl-review 계약 강화** — FR-1(bounded payload + directive 주입 + Integration 등재), FR-2(flag + Step 7 분기 + block schema).
2. **caller 전파** — FR-3의 7개 지점.
3. **sequential non-interactive** — FR-4(flag + 3분기 + malformed 분기 + Completion Report 라인) 및 `ywc-agentic` Step 5 forward.
4. **agent / compaction** — FR-5(refactor-cleaner), FR-6(parallel compaction 문단).
5. **문서 및 gate** — FR-7(README 12개), validate / markdownlint / score baseline.

## Verification Plan

```bash
bash scripts/validate.sh
npx markdownlint-cli2@0.22.1 "claude-code/skills/*/README*.md"
python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci   # 실패 시 diff archive 후 --update-baseline

# 구조적 AC 기계 확인
grep -c "Return-payload contract"  claude-code/skills/ywc-impl-review/SKILL.md        # AC2 >= 1
grep -c "subagent-status-actions"  claude-code/skills/ywc-impl-review/SKILL.md        # AC2 >= 2
grep -rn -- "--non-interactive" claude-code/skills/ywc-sequential-executor/SKILL.md \
  claude-code/skills/ywc-parallel-executor/SKILL.md \
  claude-code/skills/ywc-code-gen/SKILL.md \
  claude-code/skills/ywc-agentic/SKILL.md                                             # AC7: impl-review 호출 7건 + seq flag 행 + agentic forward
grep -ci "compaction" claude-code/skills/ywc-parallel-executor/SKILL.md               # AC14 >= 1
grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md               # AC12 증가 확인
git diff --name-only main...HEAD | grep -c '^codex/'                                  # AC17 = 0
```

수동 transcript 확인 2건 (NFR Verification/Testability): `ywc-impl-review --non-interactive` 1회, `ywc-sequential-executor --non-interactive` 1회.

## Traceability

| AC | FR | Phase | Verification evidence |
|---|---|---|---|
| AC1, AC2, AC3 | FR-1 | 1 | grep 2건 + Step 2/3 문장 diff |
| AC4, AC5, AC6, AC8 | FR-2 | 1 | Arguments 표 diff + Step 7 분기 + transcript 1회 |
| AC7 | FR-3 | 2 | 7개 지점 grep |
| AC9, AC10, AC11 | FR-4 | 3 | 3분기 diff + `settings.local.json` key 부재 확인 + transcript 1회 |
| AC12, AC13 | FR-5 | 4 | Boundaries / Mission / Anti-patterns diff + 6 section 순서 확인 |
| AC14 | FR-6 | 4 | compaction grep |
| AC15 | FR-7 | 5 | 12개 README diff |
| AC16 | 전체 | 5 | validate.sh / markdownlint / score.py 전부 exit 0 |
| AC17 | 전체 | 1–5 | `git diff --name-only` grep = 0 |

## Confidence Gate

Aggregate: **92 / 100 — PROCEED** (weakest: Architecture compliance 88)

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | 6개 편집 표면과 codex root 제외가 명시적이며, 각 접붙임 지점이 본 repo `file:line`으로 고정됨 |
| Architecture compliance | 88 | 기존 flag pattern / shared reference / 기존 section에 전부 접붙임. 유일한 판단 지점은 신규 인용 anchor를 `§3.5`(sibling 36건과 일관)가 아니라 `§Return Payload Contract`(실제로 존재하는 이름)로 택한 것 |
| Evidence quality | 94 | upstream spec의 line 인용을 그대로 쓰지 않고 6개 대상 파일 + reference + validator + CI workflow를 직접 확인. upstream이 누락한 critical-path 강제 호출 3곳을 grep으로 발견 |
| Reuse verified | 95 | 새 파일·새 status set·새 heuristic 없음. `ywc-plan` flag vocabulary, `external-url-policy.md` default, sequential compaction 문형을 재사용 |
| Root cause identified | 90 | 근본 원인은 "unattended caller가 interactive default를 상속한다"이며, 7개 호출 지점 전부에 flag를 부착해 caller 측에서 닫는다 |

## References

- Upstream: `yongwoon/develop-with-llm` PR #206 — `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md`
- Sibling (codex root): [`20260812-codex-agentic-context-safety.md`](./20260812-codex-agentic-context-safety.md)
- `claude-code/skills/references/subagent-status-actions.md`
- `claude-code/skills/references/advisor-pattern.md`
- `claude-code/skills/references/non-stop-execution.md`
- `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md`
- `claude-code/skills/ywc-plan/SKILL.md` (`--non-interactive` 1차 출처)
- `scripts/validate.sh`, `.github/workflows/validate.yml`

---

## Iteration 1 Amendments

> Source: `ywc-spec-validate` iteration 1 — Critical: 1, Warning: 3, Suggestion: 2.
> Note on provenance: iteration 1's Phase 1 4-dimension fan-out returned no payload (4/4 subagents ended with an empty body, after two re-requests). The findings below were produced by direct grep / file verification instead. This is recorded because the finding set is therefore single-reviewer, not fan-out-corroborated.

### Operative Sections

Where this section differs from the original text above, **this section is authoritative**: **AC7**, **AC15**, the **Verification Plan** markdownlint line, the **Existing Constraints** row for the `subagent-status-actions` grep counts, the **FR-1** rationale clause, the **Out of Scope** skill-count clause, and the **FR-4** flag-orthogonality clause. All other original content is unchanged.

### Critical fix — AC7 observation method

**AC7 (amended).** The original observation method ("`grep -rn -- "--non-interactive"` across the four caller files") cannot detect FR-3's absence: three `--non-interactive` occurrences already exist before this change set (`ywc-agentic/SKILL.md:95,97,262`, all of them `ywc-plan` invocations), and FR-4 adds two more that are not impl-review call sites (the `ywc-sequential-executor` Arguments row and its External URL Policy branch). A bare flag count therefore conflates at least three distinct populations.

Replace the observation method with a call-site-scoped grep plus an explicit expected count:

```bash
# expected: exactly 7 lines (FR-3's seven auto-invocation sites)
grep -rnE "ywc-impl-review[^|]*--non-interactive" \
  claude-code/skills/ywc-sequential-executor/SKILL.md \
  claude-code/skills/ywc-parallel-executor/SKILL.md \
  claude-code/skills/ywc-code-gen/SKILL.md \
  claude-code/skills/ywc-agentic/SKILL.md | wc -l

# guard: the three pre-existing ywc-plan occurrences must remain untouched
grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md   # expected: unchanged (1)
```

The `[^|]*` bound keeps the match inside a single table cell so a Markdown table row cannot join an `ywc-impl-review` mention in one column to a `--non-interactive` mention in another.

### Warning fixes

- **Existing Constraints row (amended) — `subagent-status-actions` grep counts.** The original row presents the counts (code-gen 2 / parallel 4 / sequential 4 / impl-review 0 / spec-validate 0 / task-generator 0) in a way that reads as "the other skills already honor the injection contract." Verified against the files, every one of those citations is a **status-routing** reference (`ywc-code-gen/SKILL.md:130,134`, `ywc-parallel-executor/SKILL.md:232,236,267,340`, `ywc-sequential-executor/SKILL.md:155,345,383,387`); **no skill in this repo currently injects the Return-payload contract directive into a subagent prompt.** The row's meaning is corrected to: the counts measure *status-routing adoption only*, and the injection contract at `subagent-status-actions.md:39-41` is currently honored by zero skills.
- **FR-1 rationale (amended).** FR-1 is therefore the **first** directive injection in this repo, not the enforcement of an existing practice. The nearest precedent is `ywc-code-gen/SKILL.md:128` item (v), which centralizes the status protocol and return-artifact format in a bundled base prompt (`prompts/implementer-base.md`) rather than quoting it inline. FR-1 deliberately does **not** adopt that pattern: `ywc-impl-review` has no `prompts/` directory, creating one for a single one-line directive would add a file to satisfy a pattern rather than a need, and `subagent-status-actions.md:39` explicitly mandates verbatim injection. Inline verbatim quoting is the smaller diff and the compliant one. If a second directive later needs sharing across impl-review's five lanes, revisit the base-prompt pattern then.
- **Verification Plan (amended) — markdownlint line.** Replace `npx markdownlint-cli2@0.22.1 "claude-code/skills/*/README*.md"` with the repo's actual CI invocation shape (`.github/workflows/markdownlint.yml:19` runs `npx markdownlint-cli2 --config /tmp/ml.json …`, unpinned, with a generated config). A locally pinned version plus a different config applies different rules than CI, producing both false passes and false failures. The authoritative check is the workflow itself; locally, reproduce the workflow's config-and-glob invocation rather than inventing one.
- **Out of Scope (amended) — skill count.** "51개 skill 중 부재" is corrected to "**48개 `ywc-*` skill** 중 부재". `claude-code/skills/` holds 51 directory entries, of which 48 are `ywc-*` skills; the remaining three are `CLAUDE.md`, the catalog `README*` set, and `references/`. The substantive claim (`ywc-agent-legibility-audit` is absent) is unchanged and re-verified.

### Suggestion fixes

- **FR-4 (amended) — flag orthogonality.** `ywc-sequential-executor/SKILL.md:64` defines a closed mutual-exclusion group of four delivery modes (`--local-merge`, `--draft`, `--skip-ci-wait`, `--aggregate-pr`). FR-4 adds: `--non-interactive` is **orthogonal** to that group — exactly like `--worktree` (`:64`, "not a fifth member") — and must not be added to it. It combines with every delivery mode and with `--review` / `--dry-run` / `--worktree`. Consequently the Pre-flight flag-conflict check and the `flag conflict detected (Pre-flight)` Allowed Stop Reason (`:196`) remain unchanged.
- **AC15 (amended).** Add: the six locale files per skill stay mutually consistent, with `README.en.md` as the English source and `README.md` as the Korean default; `translation-check.yml` warns (informational, non-blocking) when a `README.md` change lands without matching translation updates. AC15 passes only when all six files describe the same flag semantics.

### Self-Consistency Re-check (ywc-plan Step 4b.5, whole spec)

- **Pass A (cross-section)**: the amended AC7 now quotes the exact grep FR-3's edits produce, and the amended AC15 matches FR-7's file list (12 files, 2 skills × 6 locales). The FR-4 orthogonality clause is consistent with AC9/AC10, neither of which asserts any flag-conflict behavior. No new AC is required — each amendment tightens an existing one.
- **Pass B (claim↔reality)**: every corrected claim was verified directly against the repo in this iteration — the three pre-existing `--non-interactive` sites, the 10 status-routing citations, `markdownlint.yml:19`, the 48/51 directory split, and `SKILL.md:64`'s "not a fifth member" wording. The one claim this amendment *withdraws* (that sibling skills already honor the injection contract) was the only unverified inference in the original draft.
- **Pass C (schema)**: N/A — no Data Model change.

Amended items (Iteration 1): AC7 (Critical — observation method), Existing Constraints `subagent-status-actions` row, FR-1 rationale clause, Verification Plan markdownlint line, Out of Scope skill count, FR-4 flag-orthogonality clause, AC15 translation-consistency clause. No Data Model, API Contract, or Critical Surfaces change.
