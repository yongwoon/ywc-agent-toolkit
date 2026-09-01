# Codex PR #223 적용 검토 — Review Artifact 테스트 강화

> Status: Draft
> Scale: Medium
> Created: 2026-08-26
> Author: Codex
> Spec Reference: [develop-with-llm PR #223](https://github.com/yongwoon/develop-with-llm/pull/223)

## Global Constraints

- `codex/skills/`가 Codex 소스 기준이며 `plugins/ywc-agent-toolkit/skills/`는 `bash scripts/sync-codex-plugin.sh`로 생성한다 (`codex/AGENTS.md`).
- Codex `SKILL.md` frontmatter에는 `name:`과 `description:`만 허용한다 (`AGENTS.md`).
- 저장소에는 패키지 매니저/빌드 파이프라인이 없으며, 필수 검증은 `bash scripts/validate.sh`이다 (`AGENTS.md`, `codex/AGENTS.md`).
- 테스트는 Python 표준 라이브러리와 기존 실행 파일(`bash`, `jq`)을 사용하고, GitHub 네트워크나 실제 `gh` 인증에 의존하지 않는다.

## Purpose

PR #223은 review-body-embedded CodeRabbit 보완 과정에서 Codex의 Nitpick 매핑/리뷰 억제 로직에 동작 테스트를 추가하고, Claude 쪽에는 `raw_fallback` 안전 규칙과 parser 테스트를 보강했다. 이 저장소의 Codex 구현에는 해당 Nitpick parser와 `raw_fallback` producer가 없으므로 PR diff를 그대로 이식할 수 없다.

적용 가능한 핵심은 “소스 문자열 존재 여부”에 그치지 않고 실제 운영 스크립트의 jq 정규화 동작을 결정적 fixture로 검증하는 테스트 방식이다. 현재 Codex collector의 계약을 보존하면서 회귀 방지 테스트를 추가한다.

## Scope

- `fetch-pr-review-artifacts.sh`를 실제로 실행하는 Python `unittest` harness 추가
- fake `gh` 명령과 임시 JSON fixture로 인증 사용자, review comments, issue comments, reviews, PR health 응답 제공
- 현재 collector가 생성하는 review thread, PR comment, review submission, status check, merge readiness 계약 검증
- 주소 처리 marker, self-response/reopen 상태, self-authored/empty/approval review filtering 검증
- Codex source와 generated marketplace package 동기화

## Out of Scope

- Claude 전용 `extract-coderabbit-nitpicks.py` 및 Nitpick fixture/parser 테스트 포팅
- Codex에 Nitpick artifact producer, `raw_fallback`, Nitpick fingerprint mapping 또는 review-ID 기반 억제 로직 추가
- 현재 normalized artifact schema, GitHub API 호출, 분류 정책, reply API 동작 변경
- 테스트 편의를 위한 jq production filter 분리나 인접 리팩터링
- generated marketplace 파일의 독립 편집

## Existing Constraints Touched

| Existing artifact | Verified behavior | New code's interaction |
|---|---|---|
| `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh:35-45` | `GH_REPO`가 없으면 `gh repo view`로 저장소를 찾고, `gh api user` 실패 시 exit 3을 반환한다. | 테스트에서는 명시적 repo와 fake `gh`를 사용해 실제 인증/API 호출을 차단한다. |
| `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh:47-66` | review comments, issue comments, reviews, PR health를 순서대로 fetch하며 실패를 exit 3으로 정규화한다. | fake `gh`가 각 정확한 호출에 fixture를 반환하도록 하고, 실패 경로를 선택적으로 검증한다. |
| `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh:74-126` | review thread는 root별로 묶이고, 최신 외부 reviewer comment와 최신 self-response의 시간 순서로 unresolved 여부를 결정한다. | unanswered, self-response 이후 suppress, newer reviewer reopen fixture를 실제 출력으로 검증한다. |
| `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh:128-163` | 외부 PR comment/review만 남기고 marker, self-authored, 비대상 review state, 빈 body, addressed fingerprint를 제외한다. | 각 filter의 포함/제외 결과와 normalized field를 assert한다. |
| `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh:165-197` | 실패/대기 status check와 clean이 아닌 merge 상태를 non-reply artifact로 출력하고, 성공/clean은 출력하지 않는다. | 실패·pending·성공·skipped·neutral 및 clean/behind/conflicting fixture를 검증한다. |
| `codex/AGENTS.md` | Codex source가 authoritative이고 marketplace package는 sync 산출물이다. | source 테스트를 추가한 뒤 sync를 실행하고 source/package parity를 검증한다. |

## Acceptance Criteria

- [ ] **AC1 — 실제 collector 실행**: 테스트가 복제한 jq filter만 실행하지 않고, fake `gh`와 fixture를 주입한 상태에서 `fetch-pr-review-artifacts.sh`를 subprocess로 실행한다.
- [ ] **AC2 — review thread 계약**: unanswered 외부 comment는 출력되고, 최신 self-response 뒤의 기존 comment는 억제되며, 그 뒤의 newer reviewer comment는 다시 출력된다.
- [ ] **AC3 — marker 억제**: PR-level addressed marker는 일치하는 fingerprint만 억제하고 unrelated artifact는 출력한다. legacy marker 동작은 현재 구현에 맞게 별도 검증한다.
- [ ] **AC4 — review submission 계약**: 외부 `COMMENTED`/`CHANGES_REQUESTED`의 non-empty review는 예상 normalized fields로 출력되고, approval·empty body·self-authored·marker review는 제외된다.
- [ ] **AC5 — health gate 계약**: failed/pending status check는 `status_check`로 출력되고 success/skipped/neutral은 제외되며, non-clean merge 상태는 `merge_readiness`로 출력되고 clean 상태는 제외된다.
- [ ] **AC6 — deterministic validation**: focused Python test, `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`, `bash scripts/install.sh --list --codex`, `bash scripts/validate.sh`가 통과한다.
- [ ] **AC7 — bundle parity**: `bash scripts/sync-codex-plugin.sh` 후 source 테스트와 `plugins/ywc-agent-toolkit/skills/ywc-handle-pr-reviews/scripts/`의 generated copy가 동일하다.
- [ ] **AC8 — 범위 경계**: 변경 diff에는 Codex Nitpick parser, `raw_fallback`, Claude 파일 또는 collector production behavior 변경이 포함되지 않는다.

## Outcome Oracle

- **Target**: `fetch-pr-review-artifacts.sh`의 현재 normalized artifact 계약을 실제 subprocess 테스트로 고정하고 Codex source/package parity를 유지한다.
- **Quality threshold**: AC1–AC8의 모든 assertion과 명시된 검증 명령이 통과하며, source와 generated marketplace test copy가 byte-for-byte 동일하다.
- **Evidence required**: focused `unittest` subprocess output, failure-path exit/stderr assertion, `bash -n`, `bash scripts/install.sh --list --codex`, `bash scripts/validate.sh`, sync 후 parity diff 결과.
- **Stop condition**: 모든 증거가 통과하면 task generation에 hand off한다. 실패 시 해당 fixture/test 명세만 amend하고, collector production behavior 또는 범위 밖 parser 이식은 시작하지 않는다.

## Blind Spot Pass

검토한 누락 가능성은 다음과 같다.

| Blind spot | Decision | Rationale / evidence |
|---|---|---|
| fake `gh`가 호출 순서를 잘못 재현해 테스트가 실제 collector 계약을 우회할 가능성 | `proceed` | FR-1 harness는 명령 경로와 API 경로를 구분하고, 각 호출별 fixture 응답 및 unexpected invocation을 실패시킨다. |
| optional health field 누락 시 어떤 fallback을 고정할지 불명확 | `proceed` | FR-2/AC5에서 status check의 `state` 우선순위와 merge readiness의 `UNKNOWN` fallback을 fixture별로 명시하고, 누락 필드 fixture를 별도 assertion으로 둔다. |
| generated package parity가 sync 실행만으로 검증되지 않을 가능성 | `proceed` | AC7은 sync 후 source/generated test 파일의 byte parity를 직접 assert하고 `validate.sh` 결과를 증거로 요구한다. |

이 pass에서는 추가 사용자 결정이 필요하지 않으며, 위 세 항목은 구현 task의 검증 증거로 닫는다.

## Functional Requirements

### FR-1: Isolated collector test harness

`codex/skills/ywc-handle-pr-reviews/scripts/test_fetch_pr_review_artifacts.py`를 추가한다. `tempfile.TemporaryDirectory`, `pathlib`, `subprocess`, `json`, `unittest`만 사용하고 fake `gh`는 호출 argv를 로그한 뒤 `api user`, 각 네 개의 artifact fetch 경로, `pr view`를 정확히 구분해 fixture 응답을 반환한다. 예상 밖 argv 또는 호출 순서는 테스트를 실패시킨다. 모든 임시 파일과 환경 변경은 테스트 종료 시 정리한다.

### FR-2: Preserve the current normalized contract

테스트는 collector의 실제 JSON stdout을 파싱해 `artifact_type`, `fingerprint`, `reply_api`, `id`, `body`, `path`, `line`, `user`, `state`, 그리고 health artifact의 URL/details 필드를 현재 출력 형태대로 assert한다. 테스트를 맞추기 위한 production schema 완화나 변경은 금지한다.

### FR-3: Cover the complete current artifact paths

fixture는 review thread, PR comment, review submission, status check, merge readiness 각각에 대해 출력/억제 결과를 포함해야 한다. 각 assertion은 artifact type과 fingerprint를 오류 메시지에 포함해 fixture mismatch와 production regression을 구분한다.

### FR-4: Keep PR #223's non-applicable behavior explicit

테스트 모듈과 이 spec은 현재 Codex tree에 `extract-coderabbit-nitpicks.py`, Nitpick artifact producer, `raw_fallback`이 없음을 전제로 한다. 향후 producer가 생길 때에만 parser fixture와 raw text 사용자 확인 guardrail을 별도 plan/amendment로 도입한다.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Determinism | GitHub API, `gh` authentication, wall-clock time, current user identity에 의존하지 않는다. |
| Portability | Python 3 표준 라이브러리와 portable Bash-compatible fake command를 사용한다. |
| Maintainability | behavior별로 작은 fixture를 구성하고, failure message에 기대 artifact의 type/fingerprint를 표시한다. |
| Safety | 실제 `${CODEX_HOME}`/`${CLAUDE_SKILLS_DIR}`에 쓰지 않고 temporary directory만 사용한다. |

## Data Model

N/A — no data model change.

## API Contract

N/A — no external API contract change. fake `gh`는 collector가 이미 소비하는 응답만 재현한다.

## Edge Cases

- **빈 issue comments**: marker 추출에서 실패하지 않고 unresolved review artifact를 계속 출력한다.
- **여러 comment가 있는 thread**: 최신 reviewer comment와 최신 self-response의 시간 순서를 기준으로 현재 동작을 검증한다.
- **legacy addressed marker**: fingerprint 기반 marker와 섞어 해석하지 않고 현재 script의 동작을 별도 fixture로 고정한다.
- **빈 review body**: 대상 state라도 현재 구현의 제외 동작을 관찰해 assertion으로 고정한다.
- **optional health field 누락**: status check는 `conclusion`, `status`, `state` 우선순위를 각각 fixture로 검증하고, merge readiness는 `mergeStateStatus` 누락 시 현재 `UNKNOWN` fallback을 검증하며 새 normalization 규칙을 만들지 않는다.
- **인증 실패**: 가능하면 fake `gh` 실패로 exit 3과 stderr contract를 한 테스트에서 보장한다.

## Dependencies

- Python 3 standard library (`unittest`, `json`, `tempfile`, `subprocess`, `pathlib`)
- 기존 `bash`, `jq`, `gh` command interface (`gh`는 테스트에서 fake로 대체)
- 기존 `bash scripts/sync-codex-plugin.sh`

## Implementation Tasks

1. current collector의 호출 순서와 JSON output을 fixture 설계표로 정리하고 fake `gh` harness를 추가한다.
2. thread/marker/review submission/status/merge readiness 동작 테스트를 추가한다.
3. focused test와 `bash -n`을 실행해 fixture mismatch와 실제 contract regression을 분리한다.
4. `bash scripts/sync-codex-plugin.sh`를 실행해 generated marketplace package를 갱신한다.
5. `bash scripts/install.sh --list --codex`와 `bash scripts/validate.sh`를 실행한다.
6. 최종 diff에서 Claude 파일, Nitpick parser, `raw_fallback`, production collector 변경이 없는지 확인한다.

## Open Questions

N/A — none identified for this scoped test-hardening change. Codex Nitpick support가 필요해지는 경우 parser ownership과 사용자 확인 UX를 별도 결정으로 다룬다.

## Confidence Gate

`ywc-confidence-gate` 결과:

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 94 | Codex collector 테스트와 bundle sync만 포함하고 Claude/Nitpick parser 이식은 명시적으로 제외했다. |
| Architecture compliance | 92 | 기존 `codex/skills/.../scripts/`, Python 표준 라이브러리, source-to-plugin sync 구조를 따른다. |
| Evidence quality | 95 | PR #223 commit diff와 현재 `AGENTS.md`, `codex/AGENTS.md`, collector, sync/validation scripts를 직접 확인했다. |
| Reuse verified | 88 | 현재 collector와 eval/script tree를 검색했으며 기존 collector test harness 또는 Codex Nitpick producer를 찾지 못했다. |
| Root cause identified | 90 | 적용 대상 문제는 Nitpick 기능 부재가 아니라, embedded jq normalization 계약의 실행 수준 회귀 테스트 부재다. |

**Aggregate: 92/100 — PROCEED.**

계산: `94×0.25 + 92×0.25 + 95×0.20 + 88×0.15 + 90×0.15 = 92.15`, 반올림 92.

## References

- [PR #223](https://github.com/yongwoon/develop-with-llm/pull/223)
- `codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- `codex/skills/ywc-handle-pr-reviews/SKILL.md`
- `codex/AGENTS.md`
- `AGENTS.md`

## Handoff

## Iteration 1 Amendments

- Added the required Outcome Oracle with target, threshold, evidence, and stop condition.
- Added a resolved Blind Spot Pass covering fake-`gh` routing, optional health fields, and source/package parity.
- Made fake-`gh` invocation validation and health-field precedence explicit without changing production behavior.

이 문서는 Medium-scale spec이다. 구현 전 다음 순서로 진행한다.

1. `$ywc-spec-validate --spec docs/ywc-plans/20260826-codex-pr223-review-artifact-test-hardening.md`
2. 검증 통과 후 `$ywc-task-generator`로 executable task directory를 생성한다.
3. task 생성 전에는 이 draft를 기준으로 구현을 시작하지 않는다. Critical finding이 있으면 `$ywc-plan --update-spec`로 해당 항목만 보완한다.
