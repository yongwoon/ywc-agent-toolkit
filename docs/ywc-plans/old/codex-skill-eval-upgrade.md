# Spec: Codex Skill Eval 고도화

> Status: Draft (implementation-ready plan)
> Scale: Medium (평가 스키마·실행기·CI·두 저장소 경계를 함께 변경)
>
> **Operative Sections:** `## Iteration 1 Amendments` is authoritative for the evaluator location, isolation model, deterministic verifier model, result lifecycle, migration, and rollout. Sections marked `⚠️ SUPERSEDED` remain historical context only.
>
> ⚠️ SUPERSEDED by Iteration 1 — evaluator location is replaced below.
> Target evaluator: `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm/.codex/skills/evaluate-codex-skills-agents`
> Target bundle: `codex/skills/`, `codex/agents/`
> Created: 2026-07-22

## Purpose

`evaluate-codex-skills-agents`를 단순 구조 점검 도구에서, Codex 스킬과 custom agent의 실제 결과 품질·안전 경계·비용을 재현 가능하게 측정하는 평가 체계로 확장한다. 현재 evaluator의 하드코딩된 `tools/codex-skill/...` 경로와 단일 README 정책을 제거하여 이 저장소의 `codex/...` 번들을 정확히 평가할 수 있어야 한다.

## Scope

- 평가 대상 루트와 README/metadata 정책을 프로필 기반 설정으로 분리한다.
- 스킬 eval fixture 스키마를 정상/비활성화/경계 사례와 결정적 검증으로 표준화한다.
- 격리 workspace에서 실행하는 low-cost deterministic runner와, 필요한 경우에만 쓰는 LLM judge 단계를 구현한다.
- 고위험 또는 capability 보완형 스킬에 한해 반복 with/without ablation을 실행·기록하는 expensive suite를 구현한다.
- SKILL.md 품질 linter를 경고 중심으로 추가하고, 기존 `scripts/validate.sh`와 evaluator의 테스트를 CI 단계별로 연결한다.

## Out of Scope

- 이번 변경에서 48개 스킬 모두에 10~20개 실행 케이스를 일괄 작성하거나 전부 실행하지 않는다.
- 모델 공급자·Codex 런타임을 새로 만들거나 production credential을 이용하지 않는다.
- 평가 결과만 근거로 스킬을 자동 삭제·은퇴하지 않는다. retire는 사람 승인과 ablation evidence가 필요하다.
- `plugins/ywc-agent-toolkit/skills/` 생성 산출물을 수동 수정하지 않는다.

## Existing Constraints Touched

| 위치 | 확인된 사실 | 계획상 처리 |
|---|---|---|
| evaluator `SKILL.md`, `inventory_gate.py`, `score.py` | `tools/codex-skill/skills`와 단일 README 정책을 전제 | profile 설정으로 교체하고 legacy profile은 호환성 테스트로 보존 |
| `codex/AGENTS.md` | source of truth는 `codex/skills/`, plugin은 동기화 산출물 | evaluator가 source만 평가하고 bundle validation을 재사용 |
| `scripts/run-codex-skill-contract-evals.sh` | 현재는 JSON shape와 일부 토큰만 검증 | v2 schema validator와 runner 결과 검증으로 확장 |
| `codex/skills/*/evals/evals.json` | 44개 스킬이 fixture를 보유, 4개는 미보유 | 위험 기반 migration: 누락 4개와 고위험 샘플부터 보강 |
| `codex/agents/*.toml` | 구조 검증은 가능하지만 행동 fixture가 없음 | agent fixture/runner schema를 별도 도입 |

## Acceptance Criteria

1. `--repo-root <ywc-agent-toolkit>`와 `--profile ywc-agent-toolkit`으로 실행하면 정확히 `codex/skills`와 `codex/agents`만 inventory/score 대상이 된다.
2. profile은 required locale README, `agents/openai.yaml`, source/plugin sync 정책을 선언하며 코드에 정책을 하드코딩하지 않는다.
3. v2 fixture는 `id`, `prompt`, `language`, `category`, `should_trigger`, `expected_checks`를 검증한다. `category`는 최소 `happy_path`, `negative`, `boundary`를 지원한다.
4. fixture validator는 각 스킬의 정상 사례 1개와 non-use/boundary 사례 1개 이상을 보고하고, 누락은 quality backlog 신호로 낸다. 기존 fixture는 migration 완료 전 읽기 전용 호환 모드로 통과한다.
5. deterministic runner는 매 case마다 새 temporary workspace를 사용하고, command exit code·파일/JSON 경로·regex를 LLM 호출 없이 채점한다. 실패 artifact와 실행 metadata를 보존한다.
6. LLM judge는 deterministic check로 판정하지 못한 항목만 평가하며, rubric version·model·prompt version·판정 근거를 JSON 결과에 기록한다.
7. ablation suite는 선택된 case에 대해 with/without을 동일 fixture와 격리 환경에서 3회 이상 실행하고, pass rate·차이·비용을 보고한다. 일반 PR CI에서는 실행하지 않는다.
8. linter는 500줄 초과, 중복/무의미 지시문 후보, 비명령형 안내문 후보를 **warning**으로 보고한다. no-op/문체만으로 CI 실패를 만들지 않는다.
9. `ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review`에 최소 정상 1개와 경계/거부 1개의 v2 fixture를 추가한다.
10. evaluator 단위 테스트, fixture validator, targeted deterministic sample, `bash scripts/validate.sh`가 모두 성공한다.

## Functional Requirements and Execution Plan

### Phase 1 — 평가 대상 profile과 경로 정합성

> ⚠️ SUPERSEDED by Iteration 1 — local evaluator ownership and direct target roots are replaced below.

1. evaluator에 `profiles/` 또는 단일 versioned config를 추가한다.
2. `ywc-agent-toolkit` profile에 skill root=`codex/skills`, agent root=`codex/agents`, locale README set, openai metadata 규칙, repository validation command를 선언한다.
3. `inventory_gate.py`, `score.py`, agent fixture validator 및 tests가 config를 주입받도록 바꾼다. `tools/codex-skill` 문자열을 assertion fixture 외에는 제거한다.
4. evaluator 문서의 boundary·command matrix·report target을 실제 profile/CLI 문법으로 갱신한다.

### Phase 2 — fixture v2와 결정적 채점

> ⚠️ SUPERSEDED by Iteration 1 — arbitrary fixture `command` checks are replaced by verifier registry rules below.

1. JSON Schema 또는 stdlib validator로 v2 case shape를 정의한다.
2. `expected_checks`에 다음 check type을 제공한다: `exit_code`, `stdout_regex`, `stderr_regex`, `file_exists`, `file_regex`, `json_path_equals`, `command`.
3. 기존 `expected_behavior`, `anti_behavior`, `expectations`은 judge rubric input으로 정규화하되, migration 동안 제거하지 않는다.
4. fixture별 언어와 category 분포, `should_trigger=false` 비율, deterministic check 보유율을 mechanical score signal로 표시한다.

### Phase 3 — 격리 실행 runner와 judge adapter

> ⚠️ SUPERSEDED by Iteration 1 — the best-effort isolation and adapter contract are replaced below.

1. case마다 `mktemp` 기반 workspace를 만들고 fixture 파일만 복사한다. 이전 run의 artifacts, 대화/trace, worktree 변경을 읽지 못하게 한다.
2. runner adapter는 Codex invocation을 추상화한다. 로컬 CLI가 없거나 credentials가 없으면 `SKIPPED_UNAVAILABLE`로 기록하며 pass로 바꾸지 않는다.
3. deterministic checks를 먼저 실행하고, unresolved check만 LLM judge input으로 보낸다.
4. 실행 결과 schema에 run id, profile, case id, seed/attempt, duration, token/cost(available할 때), workspace artifact path, deterministic/judge verdict를 기록한다.

### Phase 4 — 반복·ablation과 retire evidence

> ⚠️ SUPERSEDED by Iteration 1 — trial and retirement decision rules are replaced below.

1. `--suite expensive` 또는 동등한 명시 플래그에서만 with/without을 활성화한다.
2. 동일 case/fixture/model 설정으로 3회 기본 trial을 실행하며, case별 pass rate와 95% 신뢰구간 또는 표본 수 부족 표시를 낸다.
3. retire 후보는 without 성능이 사전 정의된 non-inferiority margin 내에 있고 비용 절감이 확인될 때만 `CANDIDATE_FOR_REVIEW`로 표시한다.
4. fixture는 스킬 은퇴 후에도 regression suite에 남긴다.

### Phase 5 — lint, migration, CI 운영

> ⚠️ SUPERSEDED by Iteration 1 — result lifecycle, migration, and local CI ownership are replaced below.

1. linter rule은 heuristic ID, 근거 line, suppress annotation을 제공한다. mandatory policy 위반과 stylistic warning을 분리한다.
2. 누락된 4개 infra/IAc skill에 v2 cases를 추가하고, Docker/infra 관련 case는 실제 host mutation 없이 mocked fixture 또는 dry-run 계약으로 만든다.
3. CI를 세 계층으로 분리한다: PR fast(structure/schema/lint), scheduled deterministic runner, manually dispatched expensive ablation/judge.
4. report template에 outcome pass rate, trigger precision/recall, boundary safety, judge coverage, cost, ablation delta, unavailable/skipped count를 추가한다.

## Test Strategy

| Layer | Command / evidence | Pass condition |
|---|---|---|
| Evaluator unit tests | `test_inventory_gate.py`, `test_score.py`, agent fixture tests | profile injection과 legacy compatibility를 포함해 성공 |
| Fixture schema | v1 compatibility + v2 valid/invalid fixture tests | invalid field/category/check type이 실패 |
| Isolation | two consecutive runs with sentinel artifact | second run이 first-run sentinel을 관측하지 못함 |
| Deterministic sample | safe, fixture-backed skills 2~3개 | expected checks와 artifact retention이 일치 |
| Judge adapter | fake judge response + rubric version assertion | unresolved 항목만 judge로 전달 |
| Ablation | fake/recorded adapter 3 trials | with/without aggregation·비용·불확실성 표기 정확 |
| Bundle regression | `bash scripts/validate.sh` | exit 0, plugin sync drift 없음 |

## Rollout and Dependencies

1. Phase 1과 evaluator test 변경을 먼저 독립 PR로 제출한다. 이 단계가 완료되기 전에는 현재 evaluator를 `./codex` 품질의 근거로 사용하지 않는다.
2. Phase 2와 v1 compatibility를 다음 PR로 도입하고, 4개 누락 스킬 및 고위험 대표 스킬만 v2로 migrate한다.
3. Phase 3 deterministic runner는 local/manual mode로 검증한 뒤 scheduled CI에 연결한다.
4. Phase 4 judge/ablation은 비용 상한, 허용 모델, artifact 보존 기간을 결정한 뒤 opt-in suite로만 활성화한다.

## Risks and Mitigations

- **Runner가 스킬 activation 자체를 완전히 관측하지 못함**: `should_trigger`는 단일 성공 기준이 아니라 precision/recall 진단 지표로 보고하고, outcome을 최종 판정으로 유지한다.
- **No-op/명령형 linter 오탐**: 초기에는 warning-only, suppression에는 이유를 요구한다.
- **비결정성으로 인한 잘못된 retire 결론**: 3회 이상 trial, confidence 표시, 사람 승인 없이는 retire 불가.
- **실제 Docker/GitHub 등 외부 상태 변경**: mock/dry-run fixture를 우선하고, isolated runner에는 credential/production 접근을 주지 않는다.
- **두 저장소의 정책 drift**: profile config의 version과 fixture/profile compatibility test를 CI에 둔다.

## Open Questions

- expensive suite의 실행 모델, case당 비용 상한, artifact 보존 기간을 누가 정하는가?
- 실제 Codex CLI trace를 runner가 안정적으로 수집할 수 있는가? 불가능하면 runner의 1차 범위를 fixture-backed command workflow로 한정한다.
- evaluator가 `develop-with-llm` 내부 bundle도 계속 기본 대상으로 유지할지, 아니면 `ywc-agent-toolkit` profile을 기본값으로 바꿀지 결정이 필요하다. 권장안은 **기존 기본값 유지 + 명시적 `ywc-agent-toolkit` profile**이다.

## Confidence Gate

Confidence: 84/100 — REVIEW

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 92 | 목표, 비목표, 단계와 AC가 명확함. |
| Architecture compliance | 88 | 기존 inventory/score/tests 구조를 확장하고 profile로 경로 정책을 분리함. |
| Evidence quality | 88 | evaluator의 실제 하드코딩 경로와 bundle의 fixture/validation 상태를 확인함. |
| Reuse verified | 78 | 기존 contract evaluator와 fixture 형식을 재사용 가능하지만 Codex CLI trace API는 미확인. |
| Root cause identified | 74 | 실행형 outcome evidence 부재와 profile drift는 확인했으나 runner adapter의 실제 런타임 표면은 검증 전. |

Weakest dimension: Root cause identified (74)

What would raise it: Phase 1 이후 sandbox에서 Codex CLI 1회 실행을 수행해 activation/trace/artifact 수집 가능 여부를 확인하고, 그 결과로 adapter contract를 확정한다.

## Handoff

이 spec은 `ywc-spec-validate`로 검토한 후 `ywc-task-generator`로 Phase 1~5 task로 분해한다. 구현은 profile 정합성(Phase 1)을 완료한 뒤에만 시작한다.

## Iteration 1 Amendments

### Resolved Decisions

- **Evaluator ownership:** the only evaluator in scope is this repository's local-only `.codex/skills/ywc-codex-toolkit-eval`. The previously named `develop-with-llm` path is not part of this work.
- **Isolation:** use temporary `CODEX_HOME` best-effort isolation. This isolates installed skills and user configuration but is **not** a host-filesystem security boundary; this suite must not claim container/VM-grade non-observability.
- **Deterministic commands:** fixtures never contain arbitrary shell commands. They request evaluator-owned `verifier_id` entries only.

### Revised Acceptance Criteria

1. The evaluator continues to enumerate only `codex/skills/<directory-with-SKILL.md>` and `codex/agents/*.toml`; shared `codex/skills/references` and `codex/skills/scripts` are excluded.
2. The evaluator stays under `.codex/skills/ywc-codex-toolkit-eval` and remains excluded from `codex/skills`, `.codex-plugin/skills`, and `plugins/ywc-agent-toolkit/skills`.
3. V2 skill fixtures have an explicit `schema: 2` and case fields `id`, `prompt`, `language`, `category`, `should_trigger`, and `expected_checks`. `category` is exactly one of `happy_path`, `negative`, or `boundary`.
4. V2 agent fixtures extend the existing evaluator-owned `evals/agent-smoke-fixtures.json`; they declare the target TOML agent, isolated input/evidence packet, expected status, expected/forbidden signals, and fixture-local output path. One representative agent migration test is required before scheduled execution is enabled.
5. `expected_checks` initially supports `stdout_regex`, `stderr_regex`, `file_exists`, `file_regex`, `json_path_equals`, and `verifier`. Fixture fields never execute a shell command or specify an executable path.
6. A `verifier` check names a registry entry owned and reviewed with the evaluator code. Each entry defines an `argv` array, runner-owned cwd, timeout, allowed environment, expected exit code, and optional output regex. Shell interpreters, inherited credentials, and network access are disabled by default.
7. Every live case uses a fresh temporary workspace and temporary `CODEX_HOME` containing only the selected target skill and explicitly declared skill dependencies. It invokes the supported Codex CLI with ephemeral mode and ignores user config/rules. The run report records the CLI version, command arguments, target/dependency set, and attempt; it does not record a controllable seed unless the selected CLI version supports one.
8. The isolation test proves only that an earlier evaluator run's temporary `CODEX_HOME`, workspace, and run artifacts are absent from the next run. It must not assert host-filesystem invisibility.
9. Every run returns exactly one of `PASS`, `FAIL`, `SKIPPED_UNAVAILABLE`, `ERROR`, or `INCONCLUSIVE`. `SKIPPED_UNAVAILABLE` and `ERROR` are never quality passes and never update a baseline; scheduled workflow marks them as infrastructure-unavailable rather than silently green.
10. The runner writes a capped, redacted result record under a gitignored evaluator artifact root. Successful workspaces are deleted immediately; failed workspaces are retained only with explicit `--retain-failed-artifacts`, capped at 10 MB per run and pruned after seven days. Raw credentials and unbounded model transcripts are never persisted.
11. The existing v1 fixture shape remains read-only compatible. New fixtures and edits to an existing fixture use v2. V1 support may be removed only when the evaluator reports zero remaining v1 fixtures and a reviewed baseline change approves the removal.
12. Trigger precision/recall is reported only when the adapter exposes an activation/selection signal. Otherwise the run reports `activation_observability: unavailable`, omits precision/recall, and evaluates the final outcome only.
13. The four currently uncovered skills (`ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review`) receive at least one v2 happy-path and one v2 negative/boundary fixture.
14. Retire evidence is descriptive unless both arms complete six paired trials on the same cases and model/CLI metadata. A skill becomes only `CANDIDATE_FOR_REVIEW` when the without-skill arm has no more than one additional failed trial, cost evidence is complete for both arms, and a human approves retirement. Otherwise the result is `INCONCLUSIVE`.

### Revised Implementation Plan

1. **Local baseline and discovery:** update `.codex/skills/ywc-codex-toolkit-eval` only. Keep its existing `codex/skills` and `codex/agents` target roots, make discovery require `SKILL.md`, and add regression tests excluding shared directories.
2. **Schema and verifier registry:** add a v2 fixture validator and a small evaluator-owned verifier registry. Begin with a minimal allowlisted verifier set such as `bundle.validate`; add domain-specific verifiers as code-reviewed changes, never as fixture shell text.
3. **Runner spike before live suite:** implement and test the temporary workspace/`CODEX_HOME` adapter before migrating fixtures. Pin a supported Codex CLI version or range, parse its structured final-output event with a documented text fallback, and define timeout/cancel and unavailable/error behavior.
4. **Artifacts and metrics:** implement the status enum, redaction/retention policy, v1/v2 migration report, activation-observability field, and result aggregation before enabling any scheduled run.
5. **Migration and CI:** migrate the four uncovered skills and one existing agent smoke fixture. Keep PR CI to structure/schema/lint and deterministic mocked verifier tests; run live deterministic evaluation only on schedule or manual dispatch. The expensive paired ablation suite remains manual-only.

### Revised Test Strategy

| Layer | Evidence | Pass condition |
|---|---|---|
| Discovery | temporary repo containing a real skill plus `references/` and `scripts/` | only the real `SKILL.md` directory is enumerated |
| V2 validator | valid/invalid skill and agent fixtures | unsupported category, v1/v2 ambiguity, path traversal, and free-form command fail |
| Verifier registry | fake registry entry and rejected shell-like fixture value | only registry-owned argv executes with fixed cwd/timeout/env |
| Best-effort isolation | two consecutive fake-adapter runs | no prior workspace, temporary `CODEX_HOME`, or artifact is copied into the next run |
| Adapter spike | supported CLI fixture plus unavailable CLI fixture | final output parsing, timeout, `SKIPPED_UNAVAILABLE`, and CLI metadata are correct |
| Results | oversized/redaction/retention fixtures | status aggregation and retention policy are enforced |
| Ablation | six paired fake-adapter trials | candidate versus inconclusive rule and complete-cost requirement are correct |
| Bundle regression | `bash scripts/validate.sh` | exit 0 and no evaluator distribution leak |

### Revised Rollout

1. Land local discovery, schema, registry, and fake-adapter tests first; no live Codex execution yet.
2. Land the adapter spike, artifact policy, and status aggregation; manually validate one safe skill.
3. Migrate the four missing skill fixtures and one agent smoke fixture; enable scheduled live deterministic runs only after their results are reproducible.
4. Enable manual-only paired ablation after six-trial aggregation and cost metadata work; retirement remains a human decision.

### Revised Confidence Gate

Confidence: 91/100 — PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 94 | Local evaluator ownership, target roots, and non-goals are explicit. |
| Architecture compliance | 93 | Extends the existing local evaluator, agent smoke fixture, and bundle validation boundaries. |
| Evidence quality | 91 | Current evaluator paths, fixture coverage, discovery layout, and validation behavior were checked. |
| Reuse verified | 89 | Existing `agent_smoke.py`, `score.py`, and contract evaluation support the registry and fixture migration path. |
| Root cause identified | 88 | Path mismatch, missing outcome runner, and unsafe fixture-command ambiguity are converted into explicit contracts. |

### Step 4b.5 Re-check

- **Pass A — cross-section consistency:** revised acceptance criteria, plan, test strategy, rollout, and confidence gate all use the local evaluator, best-effort isolation, and registry-only verifier model. ✓
- **Pass B — claim-to-reality:** evaluator locality, `codex/skills` shared-directory layout, four missing skill fixtures, and existing agent smoke fixture were verified in the repository. ✓
- **Pass C — schema:** no database or API data model applies. Fixture schema invariants are covered by the revised validator acceptance criteria. ✓

## Iteration 2 Amendments

### Authentication and Network Boundary

- A temporary `CODEX_HOME` is mandatory for every live run and must not copy a developer's persistent `CODEX_HOME` or configuration.
- The runner accepts one explicit **credential-provider handoff** chosen by its deployment: `unavailable`, `injected_ci_secret`, or `ephemeral_session_material`. The adapter spike must prove the selected handoff works with the pinned Codex CLI. Credentials are process-only, excluded from command metadata and artifacts, and deleted with the run environment.
- When no provider is configured, the runner returns `SKIPPED_UNAVAILABLE`; it must never fall back to the developer's normal `CODEX_HOME`.
- “Network disabled by default” applies to model-generated tools and verifier processes. Live model API egress is an explicit CI/job-level allowlist exception; the Codex CLI alone is not claimed to enforce it. A deployment unable to enforce that boundary runs live suites manually only and records the limitation.

### Workspace and Verifier Contract

1. Every V2 live case declares an evaluator-validated workspace manifest:
   - `target_skill` and `skill_dependencies`: installed skill identifiers, resolved only from the repository's `codex/skills/<name>` directories;
   - `fixture_files`: allowlisted repository-relative source paths copied into the temporary workspace;
   - `output_paths`: workspace-relative paths the agent may create or modify;
   - `evidence_packet`: JSON input delivered to the adapter; and
   - `verifier_ids`: registry entries permitted for the case.
2. The runner rejects absolute paths, `..` traversal, symlinks escaping the fixture root, unknown dependencies, or outputs outside `output_paths`. A missing declared dependency produces `ERROR`, not an implicit global-skill lookup.
3. Every registry verifier declares exactly one mode:
   - `fixture_workspace`: runs against the copied temporary workspace; or
   - `source_checkout_readonly`: runs an allowlisted read-only validation command from the repository checkout.
   `bundle.validate` is `source_checkout_readonly`; it is not run in a selected-skill-only fixture workspace. The registry owns the mode, argv, cwd, timeout, and expected result.

### Scheduled Workflow and Artifact Operations

- Add `.github/workflows/codex-skill-evals.yml`, owned by this repository, with `workflow_dispatch` and a weekly schedule. Its inputs select `mocked` or `live` suite; `live` is disabled unless a credential provider and API-egress policy are configured.
- The workflow writes a machine-readable summary to `docs/skill-agent-eval/codex/runs/<run-id>/summary.json` and a human report beside it. Run artifacts are gitignored; only an intentionally reviewed report/scoreboard may be committed separately.
- Exit policy: `PASS` exits 0; `FAIL` exits 1; `ERROR` exits 2; `SKIPPED_UNAVAILABLE` exits 3 and emits an infrastructure alert; `INCONCLUSIVE` exits 0 only for the manual ablation suite and is never treated as a retire decision. PR fast CI invokes mocked/schema checks only and cannot produce live-suite statuses.
- A workflow cleanup step deletes retained failed-run directories older than seven days and enforces the 10 MB cap before upload. It never uploads credentials, raw environment dumps, or unbounded transcripts.

### Revised Acceptance Criteria

15. The adapter spike includes a temporary-`CODEX_HOME` authentication test with the selected credential-provider handoff and a no-provider test that returns `SKIPPED_UNAVAILABLE` without reading the developer's `CODEX_HOME`.
16. V2 live fixture validation enforces the workspace manifest, declared target/dependency installation, verifier mode, and allowed output boundaries.
17. The scheduled workflow, its suite gating, artifact locations, cleanup, and status-specific exit codes are tested with fake adapters before any live credential is configured.

### Revised Confidence Gate

Confidence: 92/100 — PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | Workspace, verifier, credential, and CI ownership contracts are explicit. |
| Architecture compliance | 93 | Uses local evaluator and existing bundle CI without distributing the evaluator. |
| Evidence quality | 92 | Temporary `CODEX_HOME` authentication and CLI option behavior were directly checked. |
| Reuse verified | 90 | Existing local evaluator and validation workflow provide the extension points. |
| Root cause identified | 89 | Authentication, API egress, and full-checkout verifier constraints are captured. |

### Step 4b.5 Re-check

- **Pass A — cross-section consistency:** local evaluator, best-effort isolation, credential handoff, registry-only verifiers, and manual expensive suite are consistent across acceptance criteria, implementation, and CI. ✓
- **Pass B — claim-to-reality:** the Codex CLI's temporary-`CODEX_HOME` auth behavior, config-ignore semantics, ephemeral mode, sandbox modes, JSON output, and checkout validation requirement were checked. ✓
- **Pass C — schema:** workspace manifest and result status rules are explicitly validated; no database/API schema applies. ✓

## Iteration 3 Amendments

### Filesystem Boundary Clarification

- Every V2 workspace manifest includes `fixture_root`, a repository-relative directory under `evals/fixtures/`. `fixture_files` and declared `output_paths` are interpreted only relative to that root.
- Before copying any fixture path, the runner resolves its real path and rejects an absolute path, `..` traversal, or a symlink whose resolved target is outside `fixture_root`.
- A `source_checkout_readonly` verifier registry entry declares `readonly_roots`, a non-empty allowlist of repository-relative real paths it may read. The runner invokes it without writable add-directories, snapshots those roots before and after execution, and fails the verifier if it changes a tracked file.
- The live adapter snapshots the fixture workspace before execution. After execution it permits only: declared `output_paths`, runner-owned transient paths, and explicitly declared fixture scratch paths. Any other added, modified, deleted, or symlink-redirected file is `FAIL` with a diff summary in the redacted result record. Pre-existing fixture files remain read-only unless also declared as an output path.

### Revised Acceptance Criteria

18. The V2 validator and runner enforce `fixture_root` realpath containment, registry `readonly_roots`, and before/after workspace snapshots; tests cover symlink escape, undeclared output writes, and source-checkout mutation.

### Revised Confidence Gate

Confidence: 93/100 — PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 96 | Fixture and verifier filesystem boundaries are explicit. |
| Architecture compliance | 94 | Boundaries extend the evaluator-owned registry and workspace adapter. |
| Evidence quality | 93 | CLI behavior and local repository layout were checked. |
| Reuse verified | 91 | Existing fixture/validator patterns support a realpath and snapshot extension. |
| Root cause identified | 90 | Auth, egress, arbitrary command, and undeclared-write risks have explicit handling. |

### Step 4b.5 Re-check

- **Pass A — cross-section consistency:** the workspace manifest, verifier modes, artifact policy, and status rules use the same fixture/output boundary. ✓
- **Pass B — claim-to-reality:** the evaluator is local-only and its current fixture/agent-smoke structure supports evaluator-owned validation extensions. ✓
- **Pass C — schema:** fixture root, realpath containment, readonly roots, and output-path rules are now testable V2 schema/runner invariants. ✓
