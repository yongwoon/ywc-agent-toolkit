# Codex Agentic Context Safety

> Status: Draft
> Scale: Large
> Created: 2026-08-12
> Author: Codex
> Spec Reference: PR #206의 Codex context-safety 제안 및 현재 Codex bundle 검토

## Global Constraints

- 변경 대상은 `codex/skills/` 및 `codex/agents/`뿐이다. Claude Code bundle은 이번 범위에 포함하지 않는다.
- Codex skill frontmatter는 `name`과 `description`만 포함한다. 변경한 skill은 Tier 1 README와 `agents/openai.yaml`을 함께 유지한다.
- `.ywc-run-state.json`과 worktree lifecycle state가 실행·정리의 유일한 authority다. 새 handoff는 이를 변경하거나 대체하지 않는다.
- 자동 실행은 사용자 입력을 기다리거나 임의 기본값을 만들지 않는다. 부족한 정보는 가장 작은 목록으로 `NEEDS_CONTEXT`를 반환한다.
- 실행 로그, handoff, subagent 결과에는 transcript, chain-of-thought, generated source, full diff, raw tool output을 기록하거나 전달하지 않는다.

## Purpose

`ywc-agentic`과 executor가 긴 multi-skill 실행 중에도 이전 대화 전체나 추측한 파일명을 authority로 사용하지 않게 한다. 모든 downstream 호출은 생산 skill이 확정한 artifact와 검증된 최소 상태만 사용하며, non-interactive 실행은 어떤 prompt surface도 사용자 대기 상태로 남기지 않는다.

## Scope

- `ywc-agentic`, `ywc-plan`, `ywc-spec-ready`, `ywc-task-generator`, `ywc-code-gen`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-team-assemble`의 orchestration contract를 갱신한다.
- 반환 artifact, plan scale, non-interactive 선택값을 위한 parseable result contract를 추가한다.
- executor transition용 비권한성 `.ywc-context-handoff.json`과 team Claim/Evidence payload 규칙을 정의한다.
- 결과·경로·no-prompt 경계를 검증하는 focused eval fixture를 추가한다.

## Out of Scope

- Claude Code skill/agent와의 동기화.
- runtime token counter, 외부 job queue, Batch API 또는 비용 최적화 backend.
- task/worktree lifecycle schema의 migration 및 cleanup authority 이전.
- 모든 skill의 일반 출력 형식 변경. 아래의 result block이 필요한 producer/consumer만 변경한다.

## Existing Constraints Touched

| Existing artifact | Verified behavior | Required interaction |
|---|---|---|
| `codex/skills/ywc-agentic/SKILL.md:88` | Full Mode가 caller-constructed `--output`과 Small `plan.md`를 전제한다. | artifact 결과를 파싱한 값만 후속 단계에 전달하도록 교체한다. |
| `codex/skills/ywc-plan/SKILL.md:199` | Small 기본 산출물은 `./plan.md`다. | agentic profile에서는 planner가 date-prefixed 경로를 소유하도록 별도 contract를 둔다. |
| `codex/skills/ywc-plan/SKILL.md:303` | `✅ Plan ready:`와 `✅ Spec drafted:` handoff를 이미 제공한다. | 사람이 읽는 handoff는 유지하되 machine authority는 아래 Result block 하나로 제한한다. |
| `codex/skills/ywc-sequential-executor/SKILL.md:148` | checkpoint가 재개 상태를 보존한다. | handoff는 checkpoint보다 낮은 우선순위의 재구성 cache다. |
| `codex/skills/ywc-parallel-executor/SKILL.md:140` | wave checkpoint가 병렬 재개 상태를 보존한다. | aggregate handoff만 기록하고 worker별 handoff authority를 만들지 않는다. |

## Acceptance Criteria

- [ ] **AC1 — Authoritative result:** producer가 하나의 complete Result block을 반환했을 때만 agentic이 Scale과 Artifact를 채택한다. 누락·중복·충돌·경로 검증 실패는 downstream 호출 없이 `BLOCKED`가 된다.
- [ ] **AC2 — Small artifact:** agentic Full Mode의 Small 계획은 `docs/ywc-plans/YYYYMMDD-small_<slug>.md`에 생성되고, 그 반환 경로가 code generation과 evaluation에 그대로 전달된다.
- [ ] **AC3 — Medium/Large artifact:** Medium/Large에서 initial plan은 scale과 candidate path만 결정한다. `ywc-spec-ready`가 `DONE`으로 반환한 artifact만 task generation, re-plan, evaluation의 final spec authority가 된다.
- [ ] **AC4 — No guessed path:** requested output, `plan.md`, basename 재구성, unlabelled prose path, raw response scan은 authority가 될 수 없다.
- [ ] **AC5 — Non-interactive closure:** `ywc-agentic --non-interactive`은 각 callee 직전에 모든 required deterministic input을 검사한다. 누락 시 정확한 agentic argument/config key를 포함한 `NEEDS_CONTEXT`를 반환하며 callee를 호출하지 않는다.
- [ ] **AC6 — Transition safety:** executor는 task/wave transition에 사용자 진행 메시지나 approval을 내보내지 않고, checkpoint/task source가 먼저인 compact handoff를 원자적으로 교체한다.
- [ ] **AC7 — Team isolation:** independent reviewer는 peer conclusion과 transcript를 받지 않는다. dependent role은 최대 세 개의 Claim과 그 evidence/artifact만 받는다.
- [ ] **AC8 — Privacy:** diagnostic·handoff·subagent payload fixture가 금지된 raw content field를 거부한다.
- [ ] **AC9 — Regression evidence:** 모든 affected skill의 eval, inventory, bundle validation, isolated install smoke가 통과한다.

## Functional Requirements

### FR-1: Parseable producer Result block

`ywc-plan`과 `ywc-spec-ready`는 사람이 읽는 handoff와 별도로 정확히 한 개의 다음 result block을 반환한다.

```text
## Result
Status: DONE
Scale: Small | Medium | Large
Artifact: <repository-relative regular Markdown file>
```

- `ywc-plan`만 `Scale`을 작성한다. `ywc-spec-ready`는 initial scale을 다시 판단하지 않고 `Status`와 `Artifact`만 작성한다.
- parser는 block 하나, field 하나씩만 허용한다. artifact는 repository root 기준으로 canonicalize하고, 상대 regular file이며 declared artifact root 안에 있는지 확인한다.
- producer 응답 원문은 저장하지 않는다. parse 실패 log에는 producer name, status, field name, candidate count, path digest, bounded reason만 저장한다.

### FR-2: Agentic-owned artifact profile

`ywc-plan`에 `--artifact-profile agentic`을 추가한다. 이 profile은 `--output`과 mutually exclusive다.

- Small: planner가 `docs/ywc-plans/YYYYMMDD-small_<slug>.md`를 생성한다.
- Medium/Large: planner가 `docs/ywc-plans/YYYYMMDD-<slug>.md`를 생성한다.
- `ywc-agentic` Full Mode는 `ywc-plan --non-interactive --artifact-profile agentic`을 호출한다. 따라서 agentic은 filename을 만들거나 `--output`으로 고정하지 않는다.
- `ywc-agentic`은 Result block의 paired Scale/Artifact만 한 단위로 파싱한다. Small artifact basename이 profile 규칙과 다르면 `BLOCKED`다.

### FR-3: One-authority orchestration flow

- Small: resolved plan artifact를 `ywc-code-gen --spec <artifact> --feature <original-goal> --skip-reuse-check`에 전달한다. task generator와 executor는 호출하지 않는다.
- Medium/Large: candidate artifact를 `ywc-spec-ready --spec <candidate>`에 전달한다. Ready Result의 `DONE` artifact만 task generator, re-plan, evaluation에 전달한다.
- 모든 invocation packet은 resolved artifact를 값으로 포함한다. run log만 보고 consumer가 artifact를 다시 찾는 방식은 금지한다.
- parseable callee status가 있으면 그대로 전파한다. status 자체가 없거나 Result block이 invalid이면 `BLOCKED`다.

### FR-4: Non-interactive public interface and preflight

`ywc-agentic`은 `--non-interactive`와 다음 forwarding argument를 문서화한다.

| Argument | Rule |
|---|---|
| `--mode` | Medium/Large task generation에서 필수이며 그대로 전달한다. |
| `--lang` | shared language chain으로 해소되지 않을 때만 필수이며 task generator에 전달한다. |
| `--suggestions apply|defer` | Medium/Large의 모든 `ywc-spec-ready` 호출에서 필요하며 그대로 전달한다. |
| `--resume-disposition resume|stop` | executor checkpoint가 존재할 때만 필수이며 선택된 executor에 전달한다. |

- `ywc-spec-ready`는 `--non-interactive --suggestions <apply|defer>`를 제공한다. Suggestion이 없으면 disposition을 요구하지 않는다. `apply`은 정확히 한 번만 amendment/re-validation하고 잔여 Suggestion은 `NEEDS_CONTEXT`로 끝낸다.
- sequential/parallel executor는 non-interactive resume, branch/worktree conflict, CI wait/timeout, external URL policy의 모든 prompt branch를 bounded terminal status로 바꾼다.
- sequential executor의 external URL policy는 `.codex/settings.local.json`의 `ywDevSequentialExecutor.externalSpecUrls`에서만 읽고 `deny|allow|allowlist` 외 값은 `NEEDS_CONTEXT`다. profile이 없는 경우 새 설정을 쓰거나 질문하지 않는다.

### FR-5: Context handoff wire contract

새 shared reference `codex/skills/references/context-handoff.md`는 다음 JSON object의 schema와 lifecycle만 소유한다.

- Required: `schema_version`, `executor`, `run_id`, `checkpoint_identity`, `current_unit`, `next_unit`, `aggregate_status`, `verified_commands`, `artifact_paths`, `unresolved_status`, `ownership_boundary`.
- `checkpoint_identity`는 task/wave id, checkpoint timestamp, base SHA, feature SHA 또는 per-worker SHA를 가진다.
- root run은 project root `.ywc-run-state.json` 옆에, sequential worktree run은 worktree state 옆에, parallel run은 root state 옆에 aggregate file 하나만 둔다.
- writer는 temporary sibling file을 fsync한 뒤 rename으로 교체한다. reader는 missing/malformed/stale/mismatched file을 폐기하고 checkpoint → current `README.md`/`task.md` 순서로 재구성한다.
- handoff는 completion, cleanup, worktree deletion을 변경하지 않는다.

### FR-6: Team Claim/Evidence contract

`references/subagent-status-actions.md`를 canonical source로 하며 optional `Claims` field를 추가한다.

- 최대 세 claim이며 각 항목은 statement와 `file:line` 또는 project-relative artifact evidence를 가져야 한다.
- `ywc-team-assemble` prompt template은 포함 scope, 제외 scope, artifact 목록, claims만 전달한다.
- independent reviewer에는 peer claim/conclusion/recommendation을 보내지 않는다. dependent role은 claims와 cited artifact만 읽을 수 있다.

### FR-7: Evaluation and release

Focused eval은 최소한 다음을 포함한다: paired result parser, date-prefixed Small artifact, Medium final spec authority, no guessed path, each missing non-interactive input, residual Suggestions, executor prompt closure, handoff fallback/location, Claim cap/isolation, prohibited log field rejection.

변경 skill의 README, `agents/openai.yaml`, `VERSION`, `CHANGELOG.md` 및 inventory를 동기화한다.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Determinism | authority가 되는 값은 labelled Result, checkpoint, task source 중 검증된 값뿐이다. |
| Backward compatibility | artifact profile이나 handoff가 없는 직접 skill 호출은 기존 behavior를 유지한다. |
| Privacy | raw response와 raw tool output은 run-local artifact에도 기록하지 않는다. |
| Availability | context pressure는 stop reason이 아니다. 실제 BLOCKED/NEEDS_CONTEXT만 중단한다. |

## Data Model

`.ywc-context-handoff.json`은 ignored run-local cache다. `.ywc-run-state.json`, task metadata, worktree state의 data model은 변경하지 않는다.

## API Contract

새/변경된 argument와 Result block은 FR-1, FR-2, FR-4를 따른다. 외부 network API 변경은 없다.

## Edge Cases

- missing/stale handoff: checkpoint와 current task source로 재구성하고 실행을 계속한다.
- conflicting Scale/Artifact results: downstream을 호출하지 않고 `BLOCKED`로 끝낸다.
- non-interactive worker가 `NEEDS_CONTEXT`를 반환: agentic은 user prompt를 열지 않고 status와 최소 missing evidence를 전파한다.
- resume state와 current invocation scope가 다름: `--resume-disposition` 없이는 `NEEDS_CONTEXT`다.
- Small planner가 profile 밖 artifact를 반환: `BLOCKED`; fallback filename을 만들지 않는다.

## Dependencies

- Existing `.ywc-run-state.json` checkpoint helpers and executor resume references.
- Existing `subagent-status-actions.md` status routing contract.
- Existing Codex skill validation and evaluation scripts.

## Open Questions

N/A — `--artifact-profile agentic`과 local-only handoff라는 boundary를 v1 decision으로 고정한다.

## Verification Plan

- `bash scripts/validate.sh`
- targeted `evals/evals.json` fixture validation for all eight affected skills
- `bash scripts/install.sh --list`
- `CODEX_HOME=<isolated-temp-dir> bash scripts/install.sh --codex ywc-agentic`
- structural checks: no agentic hard-coded `plan.md`, no caller-constructed artifact authority, no forbidden diagnostic fields, exactly one canonical Claim contract

## References

- `codex/skills/ywc-agentic/SKILL.md`
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `docs/ywc-plans/20260812-codex-architecture-invariants.md`

## Iteration 1 Amendments — Spec-readiness validation

These amendments prevail wherever they refine or replace an earlier requirement in this document.

### A. Outcome Oracle

| Element | Definition |
|---|---|
| Target | `ywc-agentic` and its eight named producer/consumer skills accept only verified, labelled artifacts and minimal checkpoint-derived context; they neither infer artifact paths nor leave a non-interactive run waiting for user input. |
| Quality threshold | Every focused eval listed in Amendment E passes; parser and handoff fixtures reject every malformed, duplicate, out-of-root, stale, mismatched, or privacy-violating input; `bash scripts/validate.sh` and isolated Codex installation pass. |
| Evidence required | The focused fixture results, `bash scripts/validate.sh`, `bash scripts/install.sh --list`, and `CODEX_HOME=<isolated-temp-dir> bash scripts/install.sh --codex ywc-agentic`, with the final inventory and documentation diff inspected. |
| Stop condition | Handoff to task generation is allowed only after all AC1–AC9 are demonstrably covered by the named fixtures/checks, no fixture accepts a prohibited fallback, and the changed bundle metadata is synchronized. Otherwise the work remains incomplete. |

### B. Result block schemas and consumer routing

FR-1 replaces its shared example with two producer-specific, success-only schemas. A producer must emit exactly one `## Result` block on `DONE`; terminal statuses use that skill's existing Completion Status report and are not a Result authority.

```text
# ywc-plan only
## Result
Status: DONE
Scale: Small | Medium | Large
Artifact: <repository-relative regular Markdown file>

# ywc-spec-ready only
## Result
Status: DONE
Artifact: <repository-relative regular Markdown file>
```

- The parser accepts exactly one block matching the invoked producer's schema, with one occurrence of each required field and no additional fields. It trims surrounding whitespace but does not recover fields from prose or a previous response.
- `ywc-agentic` consumes `ywc-plan`'s paired `Scale` and `Artifact`; it consumes only `Status` and `Artifact` from `ywc-spec-ready`. Thus AC1 means every required field for the producing skill, not that `ywc-spec-ready` supplies a Scale.
- Before dispatch, the consumer resolves `Artifact` against the repository root, rejects absolute and escaping paths, requires an existing regular Markdown file, and enforces the declared root: `docs/ywc-plans/` for `ywc-plan --artifact-profile agentic` and the original validated candidate's permitted spec root for `ywc-spec-ready`.
- Result parsing failure emits `BLOCKED` with producer name, failed field, candidate count, a digest of any candidate path, and a bounded reason. It stores neither response text nor raw tool output and invokes no downstream callee.
- A parseable non-`DONE` terminal status is propagated without attempting Result parsing. A missing terminal status remains `BLOCKED`.

### C. Non-interactive inputs and handoff validity

- `--mode` is restricted to the task-generator's documented modes; the agentic preflight reports `NEEDS_CONTEXT: --mode` before calling task generation when a Medium/Large invocation does not provide one.
- `--suggestions` is required only when `ywc-spec-ready` reports one or more Suggestions. `apply` permits one amendment/re-validation cycle; if Suggestions remain afterward, return `NEEDS_CONTEXT: --suggestions` with the remaining count and do not prompt. `defer` records the deferral and permits the `DONE` handoff.
- `--resume-disposition` is checked after locating the selected executor's authoritative checkpoint and before invoking it. A missing value returns `NEEDS_CONTEXT: --resume-disposition`; `stop` ends without executor invocation and does not alter checkpoint state.
- The external URL profile is valid only when `externalSpecUrls` is one of `deny`, `allow`, or `allowlist`; for `allowlist`, the same object must contain a non-empty list of canonical HTTPS origins. A missing profile or malformed value returns `NEEDS_CONTEXT` with `.codex/settings.local.json:ywDevSequentialExecutor.externalSpecUrls`.

### D. Context-handoff schema, location, and privacy boundary

`codex/skills/references/context-handoff.md` must define the following additional wire-level rules.

- Filename is `.ywc-context-handoff.json`. Its location is the directory containing the authoritative `.ywc-run-state.json`: repository root for root and parallel runs, and the sequential run worktree for a worktree run. Parallel execution writes exactly one aggregate file at root and no worker handoff file.
- The schema is closed: only the required fields from FR-5 and their documented nested keys are accepted. `schema_version` is the literal `1`; `executor` is `sequential` or `parallel`; `artifact_paths` are canonical repository-relative paths; `verified_commands` are command identifiers plus pass/fail status, never command output.
- `checkpoint_identity` must match the authoritative checkpoint's run id, current task/wave, timestamp, and applicable SHA(s). A file is stale or mismatched when any of those values differs; reader deletes/ignores it according to the existing run-local cleanup convention and reconstructs from checkpoint, then current `README.md`/`task.md`.
- Atomic replacement writes `<filename>.tmp` in the same directory, fsyncs the file, renames it over the destination, then fsyncs the parent directory where supported. Failed writes leave the prior valid handoff untouched and do not change checkpoint state.
- Reject recursively any unknown property and the names `transcript`, `chain_of_thought`, `generated_source`, `full_diff`, `raw_tool_output`, `raw_response`, or `tool_output`. Bound every string field to 512 characters, except a Claim statement (1,024) and an artifact path (4,096); rejection diagnostic names only the field and rule.

### E. Executable evaluation matrix and release scope

The implementation must add focused cases to each affected skill's existing `codex/skills/<skill>/evals/evals.json`; a shared parser/fixture may live under `codex/skills/references/` only when the cases cite it. Each case must state its input, expected terminal status, expected downstream-call count, and whether a handoff is accepted or rejected.

| Case | Expected assertion |
|---|---|
| Plan Result parser | accepts exactly one complete plan block; rejects duplicate/missing Scale or Artifact, unlabelled prose, outside-root and non-Markdown artifacts; downstream calls are zero on rejection. |
| Ready Result parser | accepts only Status/Artifact from one ready block; rejects a Scale field, a stale candidate path, non-`DONE` Result use, and any raw-response fallback. |
| Agentic artifact profile | Small result is date-prefixed in `docs/ywc-plans/`; Medium/Large use only the ready artifact after `DONE`; no requested output or reconstructed basename becomes authority. |
| Non-interactive preflight | independently omits `--mode`, unresolved `--lang`, required `--suggestions`, and checkpoint-bound `--resume-disposition`; each returns the named `NEEDS_CONTEXT` and calls no callee. |
| Suggestion closure | `apply` performs one amendment/re-validation; residual Suggestions return `NEEDS_CONTEXT`; `defer` records the deferral and allows handoff. |
| Executor closure | sequential and parallel fixtures cover resume, branch/worktree conflict, CI wait/timeout, and URL policy without emitting a user prompt. |
| Handoff recovery | validates root/worktree locations, one parallel aggregate file, atomic-write failure preservation, malformed/stale/mismatched discard, and checkpoint/task-source reconstruction. |
| Team/privacy | enforces three-Claim maximum with evidence; independent payload lacks peer claims/conclusions; dependent payload contains only claims and cited artifacts; every forbidden field is rejected. |

Release scope means the eight skills named in Scope, their Tier 1 READMEs, their `agents/openai.yaml` files, the repository's actual install inventory source, `VERSION`, and `CHANGELOG.md`. The implementation plan must identify the concrete inventory file discovered during implementation instead of assuming a filename.
