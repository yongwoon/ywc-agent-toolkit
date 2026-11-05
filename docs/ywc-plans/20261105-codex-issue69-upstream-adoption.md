# Codex Issue #69 upstream 반영 구현 계획

## Purpose

2026-11-05에 조회한 [상위 issue #69](https://github.com/yongwoon/develop-with-llm/issues/69)의 `ywc-agent-tookit 에 반영해야할 PR` 13개를 검토하고, 현재 배포 번들의 Codex skill·agent에 필요한 차이를 이식한다. PR 제목/본문뿐 아니라 GitHub files API의 실제 diff를 기준으로 판단했다. #345는 100건 단위 pagination의 3페이지까지 확인했다. PR 본문의 초기 범위 설명과 최종 diff가 다를 때 최종 diff를 우선한다.

- What: 아래 FR-1~FR-10의 Codex 지침·계약·평가·배포 문서를 보완한다.
- Why: 상위 프로젝트에서 수정된 작업 분해, 진단, 리뷰, branch 안전성, 인수인계 계약이 현재 번들에 누락되어 있다.
- Out of Scope: Claude Code 소스 변경, 상위 레포 작업 이력/버전 복제, 실제 PR 대응·댓글·merge·remote 삭제, Terraform apply, 사용자 설치 디렉터리 변경, 이번 세션에서 구현 실행.
- Done When: 구현 후 AC-1~AC-10을 만족하고 필수 로컬 검증이 통과한다. 실제 runtime 미검증은 명시하며 정적 PASS로 대체하지 않는다.
- Scale: Medium. 신규 skill 3개와 기존 skill/agent 간 계약 변경을 포함하는 약 10개 구현 단위이며 단일 Small PR로 보지 않는다.
- 실행 방식: `ywc-plan --non-interactive`에 해당하는 계획 전용 경로. 산출물 검토와 task 생성은 명시된 후속 단계이며 이번 요청에서 자동 구현하지 않는다.

## Outcome Oracle

- Target: 상위 13개 PR의 필요한 동작을 현재 Codex 배포 구조로 제공한다.
- Quality threshold: AC 전부 충족, spec 검토 Critical/Warning 0, 필수 validation exit 0. 안전성 경로는 정상/거부/명령 실패를 각각 검증한다.
- Evidence required: PR별 diff, 아래 현재 소스 근거, 변경 전후 fixture/계약 평가, 임시 Git 저장소 시나리오, plugin sync 검사, 전체 validation 결과. runtime 검증은 별도 실행 기록이 있을 때만 PASS.
- Stop condition: 미해결 계약 충돌 또는 필수 검증 실패 시 구현 완료를 선언하지 않는다. live runtime을 실행하지 못하면 관련 항목을 UNVERIFIED로 보고하며 runtime 지원 보장을 하지 않는다.

## PR 검토 및 채택 결정

모든 PR 링크는 `yongwoon/develop-with-llm` 기준이다. 중복 변경은 행별 복제하지 않고 구현 단위로 합친다.

| PR | 최종 diff를 반영한 판단 | 반영 단위 |
|---|---|---|
| [#335](https://github.com/yongwoon/develop-with-llm/pull/335) | 직접 diff는 Claude 계열. 피드백 루프·질문 순서·TDD seam·작성 지침·retro/handoff 목적을 채택하되 Codex 포트 #345와 병합한다. Claude frontmatter/scorer는 복제하지 않는다. | FR-2,3,4 |
| [#337](https://github.com/yongwoon/develop-with-llm/pull/337) | Claude model+rule 표기는 제외. preview/summary에서 힌트를 누락하지 않는 목적만 #338의 Codex tier에 적용한다. | FR-1 |
| [#338](https://github.com/yongwoon/develop-with-llm/pull/338) | Codex required tier와 rationale, template/metadata/summary 계약 채택. 실제 model ID를 task에 고정하지 않는다. | FR-1 |
| [#340](https://github.com/yongwoon/develop-with-llm/pull/340) | A-005~007와 설치된 targeted linter의 증거 활용 채택. 현재 catalog 구조를 유지하며 추가한다. | FR-5 |
| [#341](https://github.com/yongwoon/develop-with-llm/pull/341) | Codex 직접 변경인 prompt-injection severity 예외 정합성을 채택. Claude 쪽 handoff 안전성·Docker 실패 처리·polling 목적은 현 Codex 흐름에 맞게 별도 채택. infra/FinOps는 #348에 통합한다. | FR-4,6,8 |
| [#342](https://github.com/yongwoon/develop-with-llm/pull/342) | Mission NG/CN을 Codex #348 포트 기준으로 채택. 현재 Mission 자체가 없으므로 section만 추가할 수 없다. | FR-7 |
| [#345](https://github.com/yongwoon/develop-with-llm/pull/345) | Codex root-cause caller/mode, brainstorm, TDD, Writing Levers, retro/handoff, metadata와 eval을 채택. Claude 주변 수정 전체를 일괄 복사하지 않는다. 상위 NOT CLEAR/live UNVERIFIED 상태를 승계한 보장으로 해석하지 않는다. | FR-2,3,4 |
| [#346](https://github.com/yongwoon/develop-with-llm/pull/346) | 본문은 Codex 제외라고 쓰지만 최종 diff에는 Codex guard가 있다. 열린 PR 조회 성공+파싱된 빈 결과, 실제 base와 remote tip 일치 확인을 채택한다. | FR-6 |
| [#347](https://github.com/yongwoon/develop-with-llm/pull/347) | 최종 diff에 Codex 구현 포함. existing-branch 및 PR 번호 고정/cwd guard/push refspec/보존 계약을 채택한다. upstream hardcoded script 경로는 제외한다. | FR-9 |
| [#348](https://github.com/yongwoon/develop-with-llm/pull/348) | bounded FinOps, applied-scope binding, Mission NG/CN 채택. 새 plan/diff와 기존 scoped evidence를 구분한다. | FR-7,8 |
| [#371](https://github.com/yongwoon/develop-with-llm/pull/371) | Claude 변경 목적을 Codex 후속 #372로 구현한다. 별도 이중 반영하지 않는다. | FR-10 |
| [#372](https://github.com/yongwoon/develop-with-llm/pull/372) | 새 Medium/Large 자동 수렴 및 opt-out, auth caller 중복 방지 채택. 기존 번들의 다른 계약은 유지한다. | FR-10 |
| [#391](https://github.com/yongwoon/develop-with-llm/pull/391) | 기능 중심 Changes와 endpoint 변경 시 API 표를 채택. Codex에 없는 Review Guide를 새 의존성으로 만들지 않는다. | FR-10 |

## Global Constraints

아래는 저장소 지침의 원문이다.

> Codex `SKILL.md` frontmatter must contain only those two fields; do not copy Claude-only fields such as `version`, `category`, or `requires`.

> Each skill requires `SKILL.md` plus Tier 1 localized README files: `README.md`, `README.en.md`, `README.ja.md`, and `README.ko.md`.

> Codex skills also require `agents/openai.yaml`.

> For Codex skills, `codex/skills/` is the source of truth. The marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from it by `bash scripts/sync-codex-plugin.sh`; do not edit the generated package first.

> Treat `bash scripts/validate.sh` as the required pre-PR test.

기존 Tier 2 README.zh/es가 있는 skill은 변경 내용을 함께 유지한다. 새 skill은 Tier 1을 필수로 제공한다. 버전은 이 저장소의 Release Please 흐름에 맡기며 상위 candidate VERSION을 복제하지 않는다.

## Existing Constraints Touched

| 현재 근거 | 현 동작과 보존/변경 경계 |
|---|---|
| `codex/skills/ywc-task-generator/SKILL.md:330`, `references/task-metadata-rules.md`, `references/README.md.template` | task 생성 계약에 Model Hint가 없다. 기존 preview 승인·Ownership·Hardening Evidence 계약을 유지하고 tier만 확장한다. |
| `codex/agents/ywc-root-cause-analyst.toml:13`, `:24`, `:39` | 가설 top-3를 일률 요구한다. mode별 출력으로 바꾸고 기존 Status/Summary/Finding counts 순서는 유지한다. |
| `codex/skills/ywc-debug-rootcause/SKILL.md:85`, `:101`, `:106` | 선택적 analyst pass와 단일 가설 실험, 3회 실패 gate가 있다. ranked 후보와 단일 실험을 구분한다. |
| `codex/skills/ywc-brainstorm/SKILL.md:116` | 기존 blind-spot와 승인 흐름을 유지하며 질문 이전 사실 조회·prerequisite 순서를 보강한다. |
| `codex/skills/ywc-impl-review/references/coderabbit-methodology.md:63` | static analysis는 이미 evidence다. 새 targeted rule 표만 확장하고 review 판정을 도구 출력으로 대체하지 않는다. |
| `codex/skills/ywc-finish-branch/SKILL.md:243`, `:295` | merge-delete 및 local cleanup이 존재한다. 별도 remote 삭제 guard 추가이며 cleanup 구현을 재작성하지 않는다. |
| `codex/skills/ywc-infra-review/SKILL.md:45`, `:59` | scope fan-out/3 lenses가 있다. read-only 경계와 동일 eligible scope를 유지하며 evidence 선별을 앞에 넣는다. |
| `codex/agents/ywc-performance-engineer.toml:2` | FinOps 범위는 이미 있다. 비용 비교 payload와 근거 누락 처리를 추가하고 현재 model/effort pin은 바꾸지 않는다. |
| `codex/skills/ywc-plan/SKILL.md:343`, `:364` | 현재 opt-in prompt다. auto-converge로 변경하되 non-interactive·Re-plan 종료를 보존한다. 설치된 로컬 skill과 번들 소스가 다름을 확인했다. |
| `codex/skills/ywc-create-pr/SKILL.md:85`, `:232`, `:252` | update는 Step 7 skip, project template 우선, Impact는 기존 diff 재사용이다. 새 본문 규칙도 같은 경계를 따른다. |
| `codex/skills/scripts/resolve-bundle-executable.py:94` | 설치 우선·허용된 source fallback 해석기가 있다. upstream `tools/codex-skill` 경로를 이식하지 않는다. |

조사 시 `codex/skills/ywc-mission`, `ywc-retro`, `ywc-handoff` 디렉터리는 없었다. 신규 skill 도입에 따른 catalog/install/plugin 검증을 포함한다. graph는 주로 실행 코드 중심이라 Markdown 계약은 대상 파일을 추가 조사했다.

조사한 local Git revision은 `42664d667fdb58ae45a35b6b000515515f6c5907`이다. 아래 immutable upstream merge snapshot을 사용한다. 앞 PR 표의 채택 항목은 approved-for-port, 제외/통합 항목은 그 행의 사유에 따른 deferred 또는 중복 통합 결정이다. 승인 범위는 표의 동작이며 upstream의 모든 파일을 복제한다는 의미가 아니다.

| PR | upstream merge SHA |
|---|---|
| #335 | `bcda4953421e33cc361d5d68e6c5e3675a5ef473` |
| #337 | `0725a315d6d6096c444f72260fe582595a1bcc9a` |
| #338 | `0622ba580d2ad2bf8c8936726dd400c00752ab3e` |
| #340 | `2b7c54058da6f15f6c16b9aee5de021fac35f42f` |
| #341 | `b529b0594f1db8534a34359f4bd625ae4f023d6a` |
| #342 | `de757e3c2c7b08e1f0d0b0d91d2edf3188e465fe` |
| #345 | `2ddca68bcbf49fa7152e7c97184ab3f99cae710f` |
| #346 | `6fe84d96e910d1d56137862366161ab0780d91f1` |
| #347 | `76200680f059d34d295b3f01da527c29ea782dc2` |
| #348 | `29068f9f690fbf09e0ace8d562e4fb846b4d1339` |
| #371 | `13b6577a459955b5f372b0c009fb30d3f44e320d` |
| #372 | `90d8f066178f2328a36dac4b6ab9f2c68f32989a` |
| #391 | `fbcfcd166415fe6a521e65d529ebde4d0d7970b8` |

신규 skill의 bounded primary source는 #345 SHA의 `tools/codex-skill/skills/ywc-retro/{SKILL.md,agents/openai.yaml,evals/evals.json}`, `tools/codex-skill/skills/ywc-handoff/{SKILL.md,agents/openai.yaml,evals/evals.json}`, #348 SHA의 `tools/codex-skill/skills/ywc-mission/{SKILL.md,references/mission-format.md,agents/openai.yaml,evals/evals.json}`이다. README는 각 skill directory의 upstream README.md를 참고하되 Tier 1은 이 번들 규칙으로 작성한다.

precedent caller 조사: `codex/skills/ywc-auth-implement/SKILL.md:40`(소유 수렴, FR-10 opt-out), `codex/skills/ywc-agentic/SKILL.md:118` 및 `:130`(소유 수렴, FR-10 opt-out와 profile 보존), `codex/skills/ywc-spec-ready/SKILL.md:63`(goal mode noninteractive, 변경 없음), agentic `:136` 및 spec-ready의 update-spec 호출(Re-plan 종료 유지)을 확인했다. 새 task-aware runtime routing은 조사한 현재 executor에 없으므로 이 범위에서 도입하지 않는다.

## Quality Gate Contract

N/A — no quality gate contract

## Module Boundaries

| 단위/소유 범위 | 생산 계약 | 소비자 |
|---|---|---|
| Task metadata: `ywc-task-generator/**` | advisory tier+rationale, preview/summary 일치 | task 검토자·기존 executor(실행 모델 선택 계약 변경 없음) |
| Diagnosis: analyst TOML, debug/incident/confidence skills | caller/mode 검증과 mode별 evidence | 각 caller의 원래 판정 gate |
| Session: 신규 retro/handoff, brainstorm/TDD/author | 개선 후보 또는 임시 인수인계 | 사용자·다음 세션 |
| Review safety: impl-review/security-audit/finish-branch | 검증된 finding·삭제 허용 조건 | 기존 review/delivery caller |
| Infra: mission/infra-review/performance agent | active anchors, eligible scope, bounded FinOps | mission reader·infra 3 lenses |
| PR lifecycle: worktrees/handle-pr-reviews/plan/auth/agentic/create-pr | branch identity·수렴 경계·PR 본문 | 기존 orchestration 및 사용자 |

각 구현 단위가 자신의 source/evals/README를 소유한다. 공통 catalog·plugin 생성물 변경은 마지막 배포 단계에서 모은다. task-generator는 이 문서의 FR/AC를 입력으로 소비하며 현재 세션에서는 task 파일을 생성하지 않는다.

## Functional Requirements / Implementation Steps

### FR-1 — Model Hint

- [ ] `ywc-task-generator/SKILL.md`, `references/{README.md.template,task-metadata-rules,output-and-validation}.md`와 관련 eval 수정.
- task마다 advisory `economy|standard|advanced` 및 근거 필수. economy는 좁고 명확한 non-critical 작업, standard는 기존 패턴의 일반 작업/난이도 근거 불충분, advanced는 architecture 판단/critical surface 작업이다. 불명확한 요구는 tier 상향 대신 NEEDS_CONTEXT다.
- 현재 번들에는 `codex/skills/references/subagent-model-routing.md`와 task-aware runtime routing이 없다. tier 정의의 canonical owner를 기존 `ywc-task-generator/references/task-metadata-rules.md`로 정한다. 힌트는 이 범위에서 정보 제공용이며 executor가 모델을 선택한다는 새 보장은 하지 않는다. task-aware routing 구현은 범위 밖이고 현재 세션 모델·specialist model pin·installer fallback은 보존한다.
- preview와 최종 summary에 Model Hint 열을 필수로 표시하고 README 값과 일치시킨다. effective model ID를 힌트로 강제하지 않는다.

### FR-2 — Root-cause mode와 피드백 루프

- [ ] `codex/agents/ywc-root-cause-analyst.toml`, `ywc-{debug-rootcause,incident-postmortem,confidence-gate}/SKILL.md`, debug references 및 caller/agent eval 수정.
- `debug_hypotheses ↔ ywc-debug-rootcause`, `incident_five_whys ↔ ywc-incident-postmortem`, `confidence_root_cause ↔ ywc-confidence-gate`를 정확히 검증한다. missing/unknown/mismatch는 NEEDS_CONTEXT이며 추론하지 않는다.
- debug는 3~5 ranked falsifiable 후보 중 한 번에 한 변수만 실험한다. incident는 5 Whys, confidence는 단일 cause candidate의 찬반 근거를 반환한다.
- debug 첫 단계에 실패를 관측할 최소 feedback loop와 catches/misses를 기록한다. 자동 재현 불가 시 수동 증거·제약을 명시하며 허위 RED를 만들지 않는다.
- 3회 실패 후 기본 중단. 4번째 시도는 debug mode에서 `Fix #4 signal: fix harder`와 `Next fix worth attempting: <one concrete minimal change>`가 별도 필드로 모두 evidence-linked일 때 한 번만 허용한다. 추가 무한 retry나 최종 architecture 판정 권한은 주지 않는다.

### FR-3 — Brainstorm·TDD·작성 지침

- [ ] `ywc-brainstorm/SKILL.md`, `ywc-tdd-ritual/{SKILL.md,references/red-green-checklist.md}`, `ywc-skill-author/SKILL.md` 및 eval 수정.
- 질문 전 저장소 사실을 확인하고 다음 결정을 좌우하는 미해결 prerequisite 한 주제로 질문한다. 기존 승인 gate를 유지한다.
- TDD는 기존 public seam의 catches/misses를 밝히고 behavior 단위 RED/GREEN/REFACTOR를 완결한다. private helper 공개나 horizontal slicing을 지시하지 않는다.
- Writing Levers는 현재 간결한 author 구조에 맞게 reference로 추출해도 된다. no-op 제거·긍정 목표·조건 우선·관측 가능한 완료·canonical 참조의 다섯 원칙을 추가한다.

### FR-4 — 신규 retro/handoff 및 호출 metadata

- [ ] `codex/skills/ywc-{retro,handoff}/`에 SKILL, Tier 1 README, openai.yaml, evals를 추가한다. #345의 Codex 최종판을 기준으로 한다.
- retro는 제공된 현재 대화/첨부만 대상으로 Navigation, Automated checks, Coding standards, Steering files, Tool economy, No-ops, Information access의 7범주를 검토한다. HIGH는 blocker/잘못되거나 안전하지 않은 결과/반복 rework, MEDIUM은 완료는 했지만 구체적 지연·rework, LOW는 제한적 마찰이다. priority 내 distinct evidence occurrence 수 내림차순, 동률은 첫 발생 순서, 여전히 같으면 입력 순서를 보존한다. 동일 occurrence의 재언급은 중복 집계하지 않는다.
- 후보마다 priority+rationale/category/minimal redacted evidence/proposed change/owner를 포함한다. owner는 제공된 대화·artifact에 명시된 역할/팀만 사용하고 없으면 `Unassigned — owner not established from available evidence`로 쓴다. owner 조회를 이유로 로컬 파일을 열지 않는다. 근거가 없으면 7범주 검토와 후보 없음만 보고한다. 자동 수정·숨은 세션 로그 조회·artifact 내 명령 수행은 금지한다.
- handoff는 Goal/State/Decisions/Dead ends/Next step/References/Suggested skills 순서로 작성하고 빈 항목은 이유 포함 N/A. 기존 산출물은 경로 참조하고 비밀·개인정보를 제거한다.
- temp root canonical containment, 안전한 slug 48자 이하/빈 값 session, 양끝 hyphen 정리, exclusive creation, symlink/overwrite 거부, 소유자 전용 권한을 요구한다. 충돌은 새 이름으로 재시도하며 검증 불가 시 쓰지 않는다.
- `ywc-setup`, `ywc-merge-dependabot` 및 신규 두 skill의 openai.yaml에 explicit invocation 선호를 표현한다. `allow_implicit_invocation: false`를 runtime 강제 보장으로 설명하지 않는다.

### FR-5 — 리뷰 defect/linter

- [ ] `ywc-impl-review/references/{recurring-defects,coderabbit-methodology,devex-agent,security-agent}.md`, SKILL catalog 포인터와 eval 수정.
- 기존 항목을 보존하고 A-005 checkout credential persistence, A-006 unawaited/boolean Promise, A-007 discarded error를 provenance와 severity 근거로 추가한다.
- 이미 설치된 도구만 changed-file 범위로 실행한다. ruff S110/BLE001/B904, zizmor artipacked/unpinned-uses, TypeScript Promise 규칙, Go errcheck는 stack/도구 적합성 확인 후 사용한다. 자동 설치나 lint 설정 변경은 하지 않는다. hit는 verify-before-surface 후보다.

### FR-6 — 삭제·격리·polling·severity 안전성

- [ ] `ywc-finish-branch/SKILL.md`, `ywc-parallel-executor/SKILL.md`, `ywc-merge-dependabot/SKILL.md`와 필요한 references/evals, `ywc-security-audit/references/prompt-injection-checklist.md` 수정.
- 별도 remote 삭제는 유효 branch, 열린 PR 조회 성공·파싱 성공·빈 결과일 때만 허용. merge 근거 삭제는 의도한 base와 현재 remote tip에 맞는 merged PR을 확인한다. local `--merged HEAD`만으로 판단하지 않는다.
- Docker 격리 필요 경로에서 미해석 127을 포함한 모든 nonzero는 BLOCKED이며 worker 실행 전 중단한다. 이미 같은 조건을 만족하는 부분은 수정하지 않는다.
- Dependabot Dockerfile FROM diff 검출을 구체화하고 rebase CI wait는 총 30분 deadline과 청크 간 상태를 보존한다. deadline을 새 청크마다 초기화하지 않으며 미완료를 성공 처리하지 않는다.
- prompt-injection severity는 개별 row의 조건만 적용하고 internal-only라는 이유만으로 일괄 downgrade하지 않는다. item 2의 downgrade 금지를 보존한다.

### FR-7 — Mission 신규 도입

- [ ] #348 merge 시점 Codex Mission의 완전한 SKILL과 `references/mission-format.md`, openai.yaml, evals를 조회해 `codex/skills/ywc-mission/`에 이식하고 Tier 1 README를 작성한다.
- durable why/success/rejected-approach 기본 계약에 optional Non-goals NG###(Reason 필수), Constraints CN###(Rationale 필수)를 추가한다. 안정적 ID·출처·deprecated 보존을 지킨다.
- 첫 확정 entry 때 section 생성, legacy mission 유효, read anchor에는 active NG/CN만 포함, 빈 변경은 no-op. onboarding scan이 사용자 intent를 임의 생성하지 않도록 한다.
- mode는 read/update/curate, 기본 출력은 `docs/mission.md`다. read는 파일 없음도 빈 anchor로 허용한다. update/curate는 전체 파일을 먼저 읽고 ADD/MODIFY/DEPRECATE CHANGESET을 제시한다. non-empty durable write는 정확한 CHANGESET에 대한 사용자 확인 이후만 수행하며 dry-run과 empty changeset은 쓰기/updated date 갱신 없이 종료한다. Mission은 active 하나, SC는 observable criterion+rationale, RA는 reason을 요구한다. deprecated ID는 재사용/삭제하지 않고 이력을 보존한다. optional section의 active 행이 0개가 되면 section을 제거하되 deprecated 행은 history에 남긴다. 최초 생성 시 AGENTS.md/CODEX.md 활성화 안내만 제공하고 해당 파일을 임의 수정하지 않는다.

### FR-8 — applied-scope·FinOps

- [ ] `ywc-infra-review/SKILL.md`, `codex/agents/ywc-performance-engineer.toml`, 관련 README와 eval 수정.
- scope evidence는 사용자 one-time attestation이다. `evidence_type=state_backend|apply_record|applied_commit`, `binding_target`(정확한 제출 path 집합 또는 해당 path들을 포함하는 applied commit SHA), `applied=yes|no`를 받는다. state backend가 존재한다는 일반 진술은 path binding이 아니다. cloud/state/apply system을 조회해 검증하지 않으며 repository/revision 필드를 추가 필수로 만들지 않는다.
- scoped-only에서 evidence missing/unbound/unapplied는 reviewer 0회와 BLOCKED다. valid binding이지만 제출 IaC content가 없거나 truncated면 NEEDS_CONTEXT다. `Scope evidence:` header에 유형·대상·거부 이유를 기록한다.
- mixed는 reviewable fresh plan/diff와 complete인 validly bound scoped content를 세 lens에 동일 전달한다. missing/unbound/unapplied scoped set만 전부 제외하고 header에 excluded path와 binding status를 기록한다. fresh payload가 없거나 valid binding content가 truncated이면 NEEDS_CONTEXT/reviewer 0회이며 excluded set을 fallback으로 쓰지 않는다. fresh-only/topology-only는 각각 해당 N/A header를 사용한다. 기존 topology packet 입력도 유지한다.
- FinOps는 제공된 bounded alternatives/utilization/cost 근거로 option별 cost/risk trade-off와 권고를 반환한다. 누락은 추정 가격·절약률 대신 NEEDS_CONTEXT. read-only agent는 inline payload만 반환하고 파일 작성 요구와 충돌하지 않게 aggregator가 보고서를 소유한다.

### FR-9 — PR review worktree

- [ ] `ywc-worktrees/SKILL.md`, `ywc-handle-pr-reviews/SKILL.md`, 필요한 references/cross-skill-graph/README/evals 수정.
- `--existing-branch <H>`는 `--base-branch`와 상호 배타. local 또는 exact origin ref를 사용하고 absent/network/checked-out/dirty/locked 상태를 구분한다. 기존 새 branch 생성 호출은 보존한다.
- `--worktree`는 명시적 positive PR 번호 필수. same-repository open PR만 허용하고 번호와 H를 invocation 내 고정한다. branch는 allowlist와 check-ref-format으로 검증한다.
- registered clean canonical worktree를 in-place/reused/created로 구분하고 exact ref fetch와 fast-forward만 허용한다. local-ahead/diverged는 BLOCKED. main checkout fallback은 없다.
- 매 읽기/수정/API/commit/push/CI 전에 cwd·root·branch를 재확인한다. cwd 재진입은 invocation 전체 한 번만 허용하며 반복 실패는 BLOCKED. push는 `HEAD:refs/heads/$H`로 한정한다.
- worktree mode 필수 명령 실패 후 retry/후속 mutation을 중단하고 이미 발생한 commit/push를 보고한다. created만 branch 보존 prune을 안내하고 reused/in-place를 자동 삭제하지 않는다. 기존 audit 분류는 유지한다.

### FR-10 — 수렴·PR 본문 및 배포 정합성

- [ ] `ywc-plan/SKILL.md`, `ywc-auth-implement/SKILL.md`, `ywc-agentic/SKILL.md`, `ywc-create-pr/{SKILL.md,references/pr-body-features-api.md}`와 README/evals 수정.
- 새 Medium/Large spec 뒤 기본 `ywc-spec-ready --spec <path>` 실행. `--no-converge`, `--non-interactive`, Small, Re-plan은 자동 실행 제외. 자체 수렴 auth caller는 --no-converge 전달. 기존 다른 caller도 조사해 중복 수렴을 막는다.
- agentic의 최초 planner 호출은 `ywc-plan --no-converge [--non-interactive] --artifact-profile agentic`로 바꾼다. interactive/noninteractive 모두 agentic이 readiness를 한 번 소유하며 기존 `## Result / Status / Scale / Artifact` producer authority와 artifact-profile을 보존한다. spec-ready goal mode의 noninteractive planner와 agentic/spec-ready Re-plan은 기존 종료 경계를 유지한다. `codex/skills/ywc-skill-author/references/cross-skill-graph.md`도 이 caller 경계를 반영한다.
- Changes는 기능별 무엇/적용 위치/의도이며 근거 없는 위치/의도는 생략한다. endpoint의 추가/삭제/요청·응답·auth·status 계약 변경 때만 Method+Path별 API 표를 생성한다. 내부 구현만 변경되면 표를 생략한다.
- API 행은 삭제→변경→신규 순서, host/token/query 값 제외. template 필수 section을 보존하고 Impact 뒤(없으면 본문/Design Background 뒤)에 배치한다. 기존 PR update의 Step 7 skip을 바꾸지 않는다.
- 신규 skill catalog/agent 문서·locale·실제 수량을 갱신한다. plugin은 source에서 재생성하며 upstream 평가 보고서/설치 스크립트/버전을 그대로 복제하지 않는다.

## Acceptance Criteria

| AC / FR | 입력 → 관측 가능한 결과 / 증거 |
|---|---|
| AC-1 / FR-1 | task 생성 시 각 README의 advisory tier+rationale와 preview/summary 값이 일치하며 누락/잘못된 tier는 평가 실패한다. executor 모델 선택과 specialist pin은 바뀌지 않는다. |
| AC-2 / FR-2 | 유효한 caller/mode 3쌍은 각 출력 shape를 충족하고 누락/교차 조합은 NEEDS_CONTEXT. debug 단일 실험과 4번째 시도 guard의 양쪽 분기를 fixture로 확인한다. |
| AC-3 / FR-3 | 저장소로 답할 수 있는 사실은 먼저 조사하고, TDD seam 한계를 기록하며 한 behavior cycle 이후 다음으로 진행하는 평가 사례가 통과한다. |
| AC-4 / FR-4 | retro 7범주/빈 결과/owner 미확정/정렬 평가 및 handoff 7section/redaction/path collision/symlink/권한/외부 경로 거부 사례를 통과한다. 실제 생성 미실행은 UNVERIFIED다. |
| AC-5 / FR-5 | A-005~007 양성/음성 사례와 도구 미설치 시 미설치 보고를 검증한다. linter hit만으로 finding을 확정하지 않는다. |
| AC-6 / FR-6 | open PR/nonparseable/API 실패/merged tip 불일치 시 remote 삭제 0회, isolation 127 시 worker 0회, polling 총 deadline 유지, severity row 우선을 source/expected-trace fixture로 확인한다. 실제 모델 호출 수는 live trace가 있을 때만 실행 PASS다. |
| AC-7 / FR-7 | legacy mission/read/update/빈 변경/deprecated NG/CN 사례에서 안정적 ID와 active-only anchor를 확인한다. 신규 skill 설치/list에도 나타난다. |
| AC-8 / FR-8 | scoped-only missing/unbound/unapplied는 BLOCKED/reviewer 0회, valid binding의 content 누락은 NEEDS_CONTEXT/0회다. mixed는 부적격 set만 제외하되 fresh/eligible content 누락이면 NEEDS_CONTEXT/0회다. 정상 입력은 lens eligible set 일치와 Scope evidence header를 확인하며 FinOps 근거 누락을 추정으로 채우지 않는다. |
| AC-9 / FR-9 | local/remote-only existing branch와 dirty/divergence의 Git 명령은 executable source recipe가 있으면 임시 repo에서 기계적 결과를 확인한다. flag 충돌/in-place/reuse/create 선택/cwd reset과 PR API trace는 source/expected-trace 계약으로 확인한다. 실제 모델의 선택·호출 실행은 live trace로만 주장한다. 기존 audit/cleanup helper 임시 Git 테스트는 필수다. |
| AC-10 / FR-10 | 새 spec 자동 1회, opt-out/noninteractive/Small/Re-plan 내부 자동 실행 0회, auth/agentic 소유 수렴 각각 1회 평가를 통과한다. agentic은 interactive/noninteractive 모두 확인하고 Result/Artifact profile이 보존된다. PR 본문은 API 변경 있음/없음/template/update/language 사례를 통과하며 plugin과 source가 동기화된다. |

## Dependencies / 구현 순서

1. FR-1 → FR-2 → FR-3 → FR-4: metadata, caller/agent 원자적 변경, 작성 흐름, 신규 session skill 순서.
2. FR-5 → FR-6: 리뷰 지침과 안전성 보완. 기존 reviewer agent의 model/권한 재설계는 하지 않는다.
3. FR-7 → FR-8: Mission 기본 계약과 infra evidence/FinOps를 각각 완결한다.
4. FR-9: worktrees producer를 먼저 완료한 뒤 review consumer를 연결한다.
5. FR-10: convergence caller와 PR 본문, 공통 catalog/locale/plugin을 마무리한다.

## Verification

구현 전 baseline과 구현 후 결과를 구분해 보관한다. 현재 계획 작성은 제품 동작을 검증하지 않는다.

```bash
git diff --check
python3 tests/codex_issue69_contract_test.py
python3 tests/codex_issue69_behavior_test.py
bash scripts/run-codex-skill-contract-evals.sh
bash scripts/check-codex-agent-evals.sh
bash scripts/install.sh --list --codex
bash scripts/install.sh --list --codex-agents
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

신규 skill 선택 설치와 agent-only 설치는 임시 CODEX_HOME에서 확인한다. 기존 사용자 설치 경로는 사용하지 않는다. 신규 평가에는 관련 clause 제거 시 실패하는 negative control을 포함하되 정적 fixture는 live 실행 증거로 표기하지 않는다. live Codex 호출 matrix/analyst mode/handoff 안전성은 명시적 실행 환경이 있을 때 별도 수행하며 성공 보장 없이 결과를 기록한다.

평가 어댑터/소유 경로: 각 skill의 `evals/evals.json`은 unique numeric `id`를 사용하고 upstream string ID는 `source_id`로 보존한다. `codex/agents/evals/evals.json`은 현 runner가 요구하는 non-empty `expectations`를 제공한다. 정적 clause와 금지 clause는 `tests/fixtures/codex-issue69/upstream-adoption/*.json`으로 추가하고 기존 `tests/codex_issue69_contract_test.py`에 연결한다. 스키마 검사는 behavioral trace나 live 실행으로 표기하지 않는다.

필수 실행형 검증은 신규 `tests/codex_issue69_behavior_test.py`와 `tests/fixtures/codex-issue69/upstream-behavior/`가 소유하며 위 명시적 명령으로 실행한다. 실제 실행 가능한 기존 경계는 `codex/skills/ywc-worktrees/scripts/{audit-worktrees,cleanup-worktree}.sh`와 Docker 격리 skill의 기존 setup helper다. 변경으로 영향을 받는 helper를 임시 repo/가짜 subprocess에서 호출하고 stdout/exit/파일·branch 보존을 확인한다. 이 runner는 기존 helper 테스트를 호출/확장하며 문서 속 새 옵션을 구현하는 production dispatcher를 만들지 않는다.

evidence map: AC-1~5/7/8/10과 AC-6/9의 Markdown-only 판단(create/fetch 선택, PR guard, cwd retry, polling)은 source assertion+입력/기대 trace fixture+독립 source 검토가 필수다. polling의 총 1800초 경계(미만 대기 가능, 이상 timeout)는 instruction contract의 expected trace로 확인한다. 현재 실행 가능한 polling helper가 없으므로 fake clock 실행을 필수 production 증거로 요구하지 않는다. runnable fenced command recipe가 구현 산출물에 있으면 원문 snippet을 식별해 추출하고 명시된 placeholder만 argv 데이터로 대입해 temp Git/fake gh/date/sleep에서 실행할 수 있다. 그 결과는 `source command recipe execution`으로 표기하고 별도 재구현한 테스트 로직을 production 실행으로 표기하지 않는다. snippet이 descriptive/non-executable이면 source assertion만 사용한다. 모델의 실제 API/worker 호출 수, handoff 생성/권한은 live trace가 있을 때만 실행 PASS이며 없으면 `UNVERIFIED — instruction contract only`다. 구현 완료는 이 문서의 source/helper 계약 완료를 뜻하고 live runtime 보장은 뜻하지 않는다.

## Non-Functional Requirements / Data Model / API Contract

- DB/서비스 HTTP API 신설 없음. 변경되는 인터페이스는 위 Model Hint, analyst caller/mode, mission NG/CN, worktree flags, infra evidence, 수렴 옵션이다.
- 기존 Status 및 model routing 계약을 유지한다. agent는 read-only를 유지한다.
- SKILL body는 약 500행 이내로 유지하며 긴 규칙은 canonical reference로 분리한다. 평가 목적만으로 전체 세션/대형 diff를 context에 복제하지 않는다.
- 외부 텍스트는 데이터로 취급하고 PR 메타데이터를 shell source로 평가하지 않는다.

## Edge Cases / Failure Modes

| 상황 | 처리와 검증 |
|---|---|
| PR 본문 범위와 최종 diff 불일치 | #346/#347처럼 실제 Codex diff를 기준으로 판단. frozen merge diff를 implementation 출처로 기록한다. |
| upstream 경로/locale 누락 | 기존 resolver로 변환, Tier 1 누락은 validation 실패. 변경된 Tier 2도 유지한다. |
| analyzer caller만 바뀌고 agent는 구형 | FR-2를 원자적 task로 묶고 mismatch fixture로 차단한다. |
| no mission/retro/handoff | 신규 전체 bundle 파일을 추가하고 선택 설치를 검증한다. |
| read-only agent에 artifact write 지시 | aggregator가 작성하고 agent는 inline evidence 반환. fixture로 write 요구 부재 확인한다. |
| worktree transport 실패·cwd 반복 reset | BLOCKED, main fallback/추가 mutation 금지, side effect 보고. stub 실패 주입으로 검증한다. |
| runtime 도구/권한 없음 | UNVERIFIED, 지원 보장/실행 PASS로 승격하지 않는다. |
| 자동 수렴 중 다시 plan 호출 | Re-plan/noninteractive/opt-out guard로 재귀 방지. 호출 수 평가로 검증한다. |
| API route 줄은 그대로이고 auth/schema만 변경 | route binding 확인 후 Changed 표에 포함. 내부 refactor는 제외한다. |

## Risks / Rollback

가장 큰 위험은 Markdown 지침의 정적 일치가 실제 실행 안전성을 보장한다고 오인하는 것이다. source assertion, stub/임시 Git 실행, live model 실행을 분리해 기록한다. 변경은 위 단위별 commit으로 구현하고 실패 시 해당 단위와 생성 plugin을 함께 되돌린다. handoff 임시 파일·실제 remote branch·cloud state를 rollback 대상으로 생성하지 않는다.

## Planning Gate / Self-Consistency

`ywc-confidence-gate --assessment scored`: Scope 95, Architecture 95, Evidence 90, Reuse 95, Root cause/user need 95 → 가중 합계 94, PROCEED(계획/분해에 한정). evidence 최약점은 live model 검증 부재이며 runtime 보장과 완료 기준에서 명시적으로 분리했다. architecture 선택은 기존 flat bundle/resolver/plugin 흐름으로 명확하므로 별도 architecture advisor는 생략한다.

Pass A: AC-1~10은 FR-1~10과 1:1 연결된다. Pass B: inherited behavior는 Existing Constraints Touched에 기록하고 upstream path를 직접 실행하지 않는다. Pass C: DB migration/schema 변경 없음으로 N/A. Blind Spot: 상위 #345의 runtime 검증이 완료됐다는 가정은 성립하지 않으므로 live/fixture 증거 구분을 유지한다.

## Open Questions / Next

N/A — 구현 범위를 바꾸는 미결정 사항은 식별하지 못했다. live 검증 환경의 availability는 실행 시 확인하고 미확인 상태를 보고한다.

다음은 `ywc-spec-ready --spec docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md`로 사양 검토·수렴이다. Critical/Warning 0인 DONE 이후 `ywc-task-generator`로 분해한다. 이 문서는 구현 완료 또는 readiness DONE 판정이 아니다.


## Amendment Log

### Iteration 1 — 2026-11-05

- Driven by: parallel ywc-spec-validate iteration 1, Critical 1 / Warning 6; 보고서 `20261105-codex-issue69-upstream-adoption.review-1.md`.
- Signatures: `completeness:agentic-convergence-owner`; `feasibility:missing-routing-policy`; `completeness:immutable-provenance`; `completeness:executable-evidence-gates`; `completeness:retro-contract`; `feasibility:eval-schema-adapter`; `compatibility:infra-scope-status-contract`.

| Section edited | What changed | Why |
|---|---|---|
| Existing Constraints Touched | local SHA, 13 merge SHAs, bounded new-skill source paths, caller sites | mutable PR/merge 시점만 제시했고 interactive agentic 경로를 누락함 |
| Module Boundaries | advisory consumer와 agentic owner 명시 | 존재하지 않는 existing runtime routing을 소비자로 가정함 |
| FR-1 — Model Hint | existing metadata reference에 advisory tier 정의, runtime routing 제외 | canonical routing file과 executor routing이 없음 |
| FR-4 — 신규 retro/handoff 및 호출 metadata | 7범주·priority·tie·owner/no-evidence를 명시 | 7범주 수와 정렬 이름만으로는 검증할 수 없음 |
| FR-7 — Mission 신규 도입 | read/update/curate 및 confirmed CHANGESET, history 경계 | n/a — additive; 새 skill 전체 계약의 핵심 쓰기 경계를 가시화함 |
| FR-8 — applied-scope·FinOps | attestation input, BLOCKED/NEEDS_CONTEXT, eligible/excluded header | upstream은 provider 조회가 아닌 attestation이며 generic failure 상태만으로는 분해 시 계약 선택이 흔들림 |
| FR-10 — 수렴·PR 본문 및 배포 정합성 | agentic no-converge와 Result/profile 보존 | interactive caller readiness 이중 실행 경로가 남아 있었음 |
| Acceptance Criteria | AC-1/8/10을 수정 계약과 동기화 | 이전 runtime 소비자·generic scope failure·auth-only 호출 수를 교정함 |
| Verification | eval schema adapter와 fixture/behavior runner 소유 경로·증거 등급 | structural eval을 실행형 시나리오 증거로 오인할 수 있었음 |


### Iteration 2 — 2026-11-05

- Driven by: parallel ywc-spec-validate iteration 2, Critical 0 / Warning 1 / Suggestion 0 after deduplication; Feasibility suggestion is the same executable-seam finding.
- Signatures: `completeness:markdown-executable-evidence-seam`.

| Section edited | What changed | Why |
|---|---|---|
| Verification | 기존 audit/cleanup/setup helper 실행, Markdown expected trace, 선택적 extracted command recipe, live trace를 구분 | 존재하지 않는 polling/create helper에 mandatory fake-clock 실행을 요구한 이전 문구 교정 |
| Acceptance Criteria | AC-6/9의 source/expected-trace와 helper 실행 증거를 명시 | 추상적인 호출 수/경로 선택을 실제 model 실행으로 오인할 여지를 제거 |
