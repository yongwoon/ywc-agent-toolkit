# Codex Skills

Codex 전용 `ywc-*` Skill 목록입니다. 이 directory는 `bash scripts/install.sh --codex <skill-name>` 또는 `bash scripts/install.sh --all`을 통해 `${CODEX_HOME:-~/.codex}/skills`로 설치되는 source bundle입니다.

## PR Conflict & Merge-Readiness Resolution

PR을 생성, 수정, merge하는 skill(`ywc-create-pr`, `ywc-handle-pr-reviews`, `ywc-finish-branch`, `ywc-sequential-executor`, `ywc-parallel-executor`)은 canonical conflict 절차인 [`references/pr-conflict-resolution.md`](./references/pr-conflict-resolution.md)를 사용해야 합니다. `SKILL.md` 본문에 같은 logic을 중복 작성하지 말고, `pr-bot-polling.md`와 동일하게 `> **Action required**: Read [../references/pr-conflict-resolution.md]` 포인터를 둡니다.

이 reference는 놓치기 쉬운 두 가지 사실을 고정합니다:

- **CI status와 merge-readiness는 독립 gate입니다.** PR이 CI를 통과해도 base branch가 앞서 나가면 `CONFLICTING`일 수 있습니다. PR 완료 선언 또는 `gh pr merge` 직전에는 `gh pr view --json mergeable,mergeStateStatus`를 확인합니다.
- **PR-vs-base conflict는 feature branch에 base를 merge해서 해결합니다.** Rebase는 commit SHA를 재작성해 기존 PR review thread를 고아화하므로 사용하지 않습니다. `git merge --no-ff origin/<base>`는 SHA와 review history를 보존합니다.

실제 textual conflict는 1회 시도 후 사용자에게 surface하는 `BLOCKED` 상황입니다. Auto-resolve, force-push, `git merge --abort`는 하지 않습니다. 단순히 뒤처진 branch는 base를 merge하고 CI를 재검증합니다(최대 2 cycle, CI fix-loop budget과 동일).

## Skill 목록

아래 표는 **설치 Directory**, **내부 Skill Name**, **호출 예시**를 구분해서 보여줍니다. Codex는 skill metadata의 `description`과 사용자의 자연어 요청을 기준으로 skill을 활성화합니다.

| 설치 Directory | 내부 Skill Name | 호출 예시 | Description |
| --- | --- | --- | --- |
| `ywc-commit` | `ywc-commit` | "ywc-commit으로 commit 해줘" | 세션 작업물을 staged & commit (선택적 push), Repository commit convention 준수 |
| `ywc-create-pr` | `ywc-create-pr` | "ywc-create-pr로 PR 만들어줘" | 변경 사항을 Commit 하고 PR Template에 따라 Draft PR 생성 |
| `ywc-handle-pr-reviews` | `ywc-handle-pr-reviews` | "ywc-handle-pr-reviews로 review comment 처리해줘" | PR Review Comment 확인, 수정, 답변 자동화 |
| `ywc-finish-branch` | `ywc-finish-branch` | "ywc-finish-branch로 branch 마무리해줘" | Feature Branch delivery 단일 호출 (mark-ready / CI / merge / mark complete / cleanup) |
| `ywc-release-pr-list` | `ywc-release-pr-list` | "release PR list 정리해줘" | Release PR의 포함 PR/Author 목록을 정리하고 PR description 갱신 |
| `ywc-changelog-release-notes` | `ywc-changelog-release-notes` | "CHANGELOG와 release notes 작성해줘" | git log / PR 목록 기반 CHANGELOG.md 항목 및 User 대상 Release Notes 생성 |
| `ywc-merge-dependabot` | `ywc-merge-dependabot` | "Dependabot PR merge 해줘" | Dependabot PR 자동 Merge (CI 검증 + sequential / parallel-auto 처리) |
| `ywc-project-scaffold` | `ywc-project-scaffold` | "ywc-project-scaffold로 directory 구조 제안해줘" | 언어/Framework/Protocol/Architecture 조합별 Directory 구조 Markdown 생성 |
| `ywc-project-docs` | `ywc-project-docs` | "project docs를 한국어로 작성해줘" | 한국어/日本語 Project 문서 생성 (docs/ Directory 구조 준수) |
| `ywc-ubiquitous-language` | `ywc-ubiquitous-language` | "ubiquitous language 정리해줘" | 도메인 공유 어휘 문서 생성·추출·업데이트 |
| `ywc-task-generator` | `ywc-task-generator` | "spec을 task로 분해해줘" | Specification을 dependency-safe한 구현 Task로 분해 |
| `ywc-sequential-executor` | `ywc-sequential-executor` | "task를 순차 실행해줘" | Task를 순차 실행하고, `--aggregate-pr`에서는 work branch 누적 후 최종 PR 1개로 delivery |
| `ywc-parallel-executor` | `ywc-parallel-executor` | "독립 task를 병렬 실행해줘" | Git Worktree 격리 기반 Task 병렬 실행 |
| `ywc-docker-isolate` | `ywc-docker-isolate` | "worktree Docker port 격리해줘" | 병렬 worktree별 Docker Compose port isolation audit/setup/teardown |
| `ywc-code-gen` | `ywc-code-gen` | "plan대로 code generation 해줘" | Backend / Frontend / QA 병렬 Code 생성 |
| `ywc-impl-review` | `ywc-impl-review` | "구현 결과 review 해줘" | 구현 Review 및 specialist agent routing |
| `ywc-review-learnings` | `ywc-review-learnings` | "review learnings 학습해줘" | Project별 review 선호를 `docs/review-learnings.md`에 누적 |
| `ywc-spec-validate` | `ywc-spec-validate` | "spec 품질 검증해줘" | Specification 품질 Review |
| `ywc-spec-ready` | `ywc-spec-ready` | "spec을 task 생성 가능 상태로 수렴시켜줘" | spec readiness loop, advisor budget 기반 validate/update 반복 후 task-generator handoff |
| `ywc-spec-writer` | `ywc-spec-writer` | "specification을 갱신해줘" | Specification 작성·갱신 |
| `ywc-tech-research` | `ywc-tech-research` | "기술 조사해줘" | Library / Implementation 비교 및 기술 조사 |
| `ywc-plan` | `ywc-plan` | "이 아이디어를 plan/spec으로 정리해줘" | Rough idea → 구현 직전 artifact |
| `ywc-security-audit` | `ywc-security-audit` | "security audit 해줘" | OWASP Top 10 + application-specific threat 기반 Security Audit |
| `ywc-ui-ux-review` | `ywc-ui-ux-review` | "UI/UX review 해줘" | Code 정적 분석 + Live UI 탐색 기반 UI/UX Review |
| `ywc-design-renew` | `ywc-design-renew` | "AI slop 디자인 리뉴얼해줘" | Generic UI surface 리뉴얼 및 AI-slop tell 점검 |
| `ywc-product-review` | `ywc-product-review` | "제품 관점 review 해줘" | 사용자 가치·UX Flow·Growth·Risk·Market 관점 Feedback 생성 |
| `ywc-gen-testcase` | `ywc-gen-testcase` | "manual testcase 만들어줘" | PR / Task / git range / diff 기반 Testsheet 생성 |
| `ywc-e2e-test-strategy` | `ywc-e2e-test-strategy` | "Playwright E2E 전략 세워줘" | Playwright 기반 E2E 테스트 전략 설계 |
| `ywc-incident-postmortem` | `ywc-incident-postmortem` | "incident postmortem 작성해줘" | 프로덕션 장애 후 구조화된 Postmortem 작성 |
| `ywc-skill-author` | `ywc-skill-author` | "ywc skill 개선해줘" | 새 ywc-* skill 작성 또는 기존 skill 구조 개선 시 표준 규칙 강제 |
| `ywc-brainstorm` | `ywc-brainstorm` | "아이디어를 같이 구체화해줘" | Rough idea → 승인된 design 까지 Socratic dialogue |
| `ywc-verify-done` | `ywc-verify-done` | "완료 검증해줘" | 완료 선언 전 fresh verification evidence 강제 |
| `ywc-debug-rootcause` | `ywc-debug-rootcause` | "root cause 찾아줘" | Bug/test failure 시 4단계 root-cause investigation 강제 |
| `ywc-tdd-ritual` | `ywc-tdd-ritual` | "TDD로 구현해줘" | RED → GREEN → REFACTOR 강제 |
| `ywc-confidence-gate` | `ywc-confidence-gate` | "구현 전 confidence gate 해줘" | 구현 착수 직전 5차원 confidence 점수 강제 |
| `ywc-receive-review` | `ywc-receive-review` | "review feedback 대응해줘" | Review feedback 수신 시 performative agreement 차단 |
| `ywc-onboard-repo` | `ywc-onboard-repo` | "처음 보는 repo onboarding 해줘" | 기존 repo 진입 시 reconnaissance → Onboarding Guide + Starter AGENTS.md 생성 |
| `ywc-refactor-clean` | `ywc-refactor-clean` | "dead code 정리해줘" | dead code 제거 및 SAFE/CAUTION/DANGER tier 분류 |
| `ywc-agentic` | `ywc-agentic` | "이 goal을 agentic하게 구현해줘" | Goal → Plan → Execute → Evaluate → Repeat 자율 루프 |
| `ywc-worktrees` | `ywc-worktrees` | "worktree lifecycle 관리해줘" | git worktree lifecycle 관리 |

> **정리:** 설치 Directory와 내부 Skill Name은 동일하게 `ywc-*` 이름을 사용합니다. Codex에서 호출할 때는 자연어 요청에 skill 이름이나 trigger phrase를 포함하면 matching 정확도가 높아집니다.

## Skill Routing Guide

어떤 상황에서 어떤 Skill을 쓸지 빠르게 결정하기 위한 기준입니다.

### 시나리오별 Skill 선택

| 상황 | 사용할 Skill | 비고 |
|------|-------------|------|
| 기술/라이브러리 조사 | `ywc-tech-research` | Spec 작성 전 먼저 실행 |
| Rough idea → plan / spec 준비 | `ywc-plan` | Scale 자동 판정 후 Small=plan.md / Medium·Large=spec |
| 사양서 작성·갱신 | `ywc-spec-writer` | --full (신규 전체) / --from-task(s) / --from-commit / --from-pr(s) / --lang |
| Spec 품질 점검 | `ywc-spec-validate` | Task 분해 전 반드시 실행 |
| Spec → Task 분해 | `ywc-task-generator` | Spec Review 통과 후 |
| Task 순차 실행 | `ywc-sequential-executor` | 의존성 있는 Task 체인 |
| Task 병렬 실행 | `ywc-parallel-executor` | 독립 Task 다수 (Worktree 격리) |
| 전체 코드 생성 (API + UI + Test) | `ywc-code-gen` | 신규 Feature 풀스택 생성 |
| 구현 결과 검증 | `ywc-impl-review` | Executor 완료 후 또는 `--review` 플래그 |
| Review learning 누적 / 조회 | `ywc-review-learnings` | false positive, 반복 finding, project별 review 선호 저장 |
| 보안 감사 | `ywc-security-audit` | OWASP Top 10, PR 머지 전 |
| UI/UX 검토 | `ywc-ui-ux-review` | IA + Visual + WCAG 2.2 AA |
| 디자인 리뉴얼 / AI-slop 점검 | `ywc-design-renew` | 평범한·LLM-티 나는 디자인 개선 + slop gate |
| 서비스/제품 관점 검토 | `ywc-product-review` | 비즈니스 5축 분석 |
| 수동 테스트 시트 생성 | `ywc-gen-testcase` | PR 또는 Task 기준 (사람이 검증) |
| E2E 자동화 테스트 전략 / Playwright 설정 | `ywc-e2e-test-strategy` | --init (신규) / --audit (점검) / --flow (단일 Flow) |
| 작업물 Commit (선택적 Push) | `ywc-commit` | 세션 작업물만 staged & commit, repo convention 준수 |
| PR 생성 | `ywc-create-pr` | Commit + Draft PR 자동 생성 |
| Branch delivery (mark-ready / CI / merge / mark complete / cleanup) | `ywc-finish-branch` | Executor 내부에서 위임 호출 또는 standalone |
| PR Review 대응 | `ywc-handle-pr-reviews` | Review Comment 수정 + 답변 |
| Release PR 목록 정리 | `ywc-release-pr-list` | Release 브랜치 생성 시 |
| CHANGELOG / Release Notes 생성 | `ywc-changelog-release-notes` | Tag 생성 전 또는 ywc-release-pr-list 결과 기반 |
| 장애 발생 후 Postmortem 작성 | `ywc-incident-postmortem` | 프로덕션 장애 / 보안 사고 / 데이터 손실 후 |
| Dependabot PR 머지 | `ywc-merge-dependabot` | CI 확인 후 sequential 또는 ecosystem-grouped parallel-auto 자동 머지 |
| 도메인 용어집 / Ubiquitous Language 작성·관리 | `ywc-ubiquitous-language` | new (신규) / extract (코드 추출) / update (갱신) 자동 감지 |
| 신규 프로젝트 구조 생성 | `ywc-project-scaffold` | Directory 구조 Markdown 생성 |
| 한국어/일본어 문서 생성 | `ywc-project-docs` | docs/ 규약 준수 (`--lang kr` / `--lang ja`) |
| 새 ywc-* skill 작성 / 기존 skill 구조 개선 | `ywc-skill-author` | (메타 skill) 표준 규칙 강제 |
| Rough idea / "이런 거 만들고 싶은데" → 승인된 design | `ywc-brainstorm` | ywc-plan 의 Step 1.0 에서도 자동 위임. 6단계 Socratic dialogue (terminal = ywc-plan handoff) |
| 완료 선언 전 fresh 검증 (commit / PR / executor handoff 직전) | `ywc-verify-done` | "should/probably/seems" 금지. 5단계 Gate Function (IDENTIFY→RUN→READ→VERIFY→CLAIM) |
| Bug / test failure / build failure 의 root cause 조사 | `ywc-debug-rootcause` | 4-phase investigation. 3+ fix 실패 시 architecture 재논의 escape hatch |
| 새 feature / bug fix 를 TDD (RED-GREEN-REFACTOR) 로 구현 | `ywc-tdd-ritual` | "Watch it fail" 단계 필수. ywc-code-gen --tdd 가 delegate |
| 구현 착수 전 5차원 confidence 점수 (PROCEED / REVIEW / STOP) | `ywc-confidence-gate` | ywc-plan Step 2 후·executor boundary. ywc-impl-review 와 같은 rubric 사용 (score 비교 가능) |
| Review feedback (사람·bot) 받았을 때 verify 후 응답 | `ywc-receive-review` | ywc-handle-pr-reviews 의 attitude layer. 금지 어휘 ("You're absolutely right!", "Thanks!") |
| 기존 / 처음 보는 repo 진입 → Onboarding Guide + Starter AGENTS.md | `ywc-onboard-repo` | 4-phase reconnaissance (Glob+Grep). ywc-project-scaffold (신규 repo 생성) 의 inverse |
| Dead code / unused import / unused deps 제거 | `ywc-refactor-clean` | knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps + SAFE/CAUTION/DANGER tier |
| 자연어 목표 → 코드 구현까지 자동화 | `ywc-agentic` | 기존 ywc-* skill 을 자율 오케스트레이션 |

### 표준 개발 Pipeline

Spec 기반 개발의 권장 실행 순서:

```
ywc-ubiquitous-language # (필요 시) 도메인 용어집 수립 — new / extract / update
  ↓
ywc-tech-research       # (필요 시) 기술 조사
  ↓
ywc-plan                # Rough idea → plan.md (Small) 또는 spec (Medium/Large)
  ↓                       (Small path 는 곧바로 ywc-code-gen / executor 로 분기)
ywc-spec-writer        # (필요 시) 사양서 작성·갱신 — docs/specification/ 생성 또는 업데이트
  ↓
ywc-spec-validate         # Spec 품질 점검 — Critical 0건 확인
  ↓
ywc-task-generator      # Spec → Task 분해
  ↓
ywc-sequential-executor # Task 실행 (또는 ywc-parallel-executor)
  ↓
ywc-impl-review         # 구현 검증 (또는 --review 플래그로 자동 호출)
  ↓
ywc-security-audit      # (필요 시) Auth/External-facing 코드 보안 감사
  ↓
ywc-gen-testcase        # 수동 테스트 시트 생성
  ↓
ywc-e2e-test-strategy   # (필요 시) Playwright E2E 자동화 전략 수립 또는 Coverage 점검
  ↓
ywc-commit              # (executor 미사용 시) 작업물 commit
  ↓
ywc-create-pr           # PR 생성 (commit 포함)
  ↓
ywc-handle-pr-reviews   # Review 대응
  ↓
ywc-release-pr-list     # (Release PR 시) develop → main 머지 PR 목록 정리
  ↓
ywc-changelog-release-notes  # (Release 시) CHANGELOG.md + User Release Notes 생성
```

> **장애 발생 시 (Pipeline 외부, reactive)**: `ywc-incident-postmortem` 을 단독으로 실행한다. 장애로 인한 Patch Release가 이어질 경우 Pipeline을 재개하고 `ywc-changelog-release-notes` 에서 장애 관련 Fixed/Security 항목을 포함시킨다.

> **Note**: `ywc-create-pr` → CI 대기 → `ywc-handle-pr-reviews` → merge → cleanup 까지의 일련 흐름은 `ywc-finish-branch` 를 standalone 으로 호출해 한 번에 처리할 수도 있다. Executor (sequential / parallel) 가 내부적으로 위임 호출하는 경우 외부에서 별도 호출은 불필요.

### Executor 선택 기준

| 조건 | Skill |
|------|-------|
| Task에 의존성이 있고 순서가 중요함 | `ywc-sequential-executor` |
| 독립 Task가 2개 이상이고 병렬 실행으로 시간 절약 가능 | `ywc-parallel-executor` |
| 신규 Feature를 풀스택으로 한 번에 생성 (Backend + Frontend + QA 동시) | `ywc-code-gen` |

### Sequential Aggregate Delivery

`ywc-sequential-executor --aggregate-pr`는 range 실행에서 각 task를 별도 feature branch로 구현하되, Step 5에서 real base가 아니라 하나의 work branch로 local merge합니다. 마지막 task까지 work branch에 누적한 뒤 단일 work -> base PR을 만들고, ready 전환, CI, bot review, merge-readiness gate, merge, local base sync까지 완료해야 `DONE`입니다.

절차상 Step 2는 각 task branch를 work branch에서 만들고, Step 5는 해당 feature branch를 work branch로 local merge하며, 마지막 task 후 final step에서 work -> base PR을 생성·merge합니다.

```text
Use $ywc-sequential-executor to run tasks 001010..003020 with --aggregate-pr --group-name billing-rollout.
```

`--group-name <name>`은 aggregate mode에서만 유효하며 work branch를 `work/<name>`으로 고정합니다. 이름을 생략하면 executor가 base branch와 timestamp로 work branch를 만듭니다. Stale `.ywc-run-state.json`이 현재 요청 range와 맞지 않으면 자동 resume하지 않고, 저장된 run-state를 이어갈지 삭제하고 새 run으로 시작할지 명시 선택을 요구합니다.

## Validation

`ywc-task-generator` 변경 후에는 아래 공통 runner 로 정적 검증을 수행할 수 있습니다:

```bash
python3 ./tools/scripts/run_task_generator_evals.py
```

개별 bundle 만 확인하려면:

```bash
python3 ./tools/scripts/run_task_generator_evals.py --bundle claude
python3 ./tools/scripts/run_task_generator_evals.py --bundle codex
```

## HTML 출력 모드 (`--format html`)

### 도입 배경과 이유

AI가 생성한 100줄 이상의 Markdown 문서는 사람이 끝까지 읽지 않는 경향이 있습니다 — 위에서부터 훑어 내리다 닫아버리는 것이 일반적입니다. 산출물이 읽히지 않으면 그 문서는 의사결정을 이끌지 못합니다. AI coding tool 실무자들과 Andrej Karpathy가 공통으로 지적했듯, **AI가 사람에게 전달하는 결과물의 포맷은 사람이 가장 잘 받아들이는 형태여야 하며, 그것이 HTML입니다.** Markdown은 사람이 사람에게 쓰던 시대의 포맷이고, 지금은 AI가 사람을 위해 문서를 씁니다 — 포맷도 그 변화를 따라가야 합니다.

HTML이 Review/Report 산출물에서 Markdown보다 나은 이유:

- **정보 밀도** — 색상, severity 배지, SVG 다이어그램, layout 등 Markdown이 표현하지 못하는 것을 담습니다.
- **시각적 명확성** — tab, 접이식 섹션, 고정 요약 헤더로 긴 리포트도 한눈에 훑을 수 있습니다.
- **공유성** — self-contained `.html` 파일 1개는 브라우저에서 바로 열리고, 링크나 첨부로 그대로 전달됩니다.
- **인터랙션** — 체크박스, sign-off 상태, `Copy as Markdown` 버튼으로 정적 리포트가 조작 가능한 도구가 됩니다.

### 지원 Skill

사람이 읽고 의사결정하는 산출물을 생성하는 9개 Skill이 `--format html`을 지원합니다:

`ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`, `ywc-design-renew`

사용 예: `ywc-impl-review --spec docs/spec.md --code src/ --format html`

출력 규약 상세는 [`references/html-output.md`](./references/html-output.md)를 참조하십시오.

### ⚠️ Token 사용량 경고

**HTML 출력은 Markdown 대비 output token을 2~4배 더 사용하며, 그만큼 응답 시간도 길어집니다.** 이 때문에 `--format`의 기본값은 `markdown`이며, HTML은 `--format html`을 명시적으로 지정할 때만 활성화되는 opt-in 옵션입니다. 매번 HTML로 출력하기보다, 사람이 실제로 브라우저에서 읽고 의사결정해야 하는 리포트에 한해 선택적으로 사용하시기를 권장합니다. Markdown surface는 HTML 파일 내부에 보존되어 `Copy as Markdown` 버튼으로 추출되므로, downstream Skill 연동에는 영향이 없습니다.

### 적용하지 않는 산출물

`docs/specification/`의 사양서, `tasks/` 디렉터리, CHANGELOG, ubiquitous-language 용어집처럼 **Git에 commit되어 diff·grep 대상이 되는 canonical 문서**에는 HTML을 적용하지 않습니다. HTML은 diff noise를 유발하기 때문이며, 해당 Skill들은 `--format` flag 자체를 제공하지 않습니다.

## Skill 호출 방법

Codex에서 Skill을 호출하는 방법은 다음과 같습니다:

```bash
# 자연어로 호출 (Codex가 description 기반으로 matching)
"PR을 만들어줘"
"ywc-create-pr로 PR을 만들어줘"
"ywc-task-generator로 spec을 task로 분해해줘"
```

- **명시 호출**: 요청에 `ywc-*` skill 이름을 포함하면 matching이 가장 안정적입니다.
- **자연어 호출**: Skill의 `description`에 매칭되는 자연어를 입력하면 Codex가 해당 Skill을 활성화할 수 있습니다.

## Skill 작성 규칙

### Frontmatter 필수 필드

`SKILL.md`의 YAML Frontmatter에 다음 필드를 포함해야 합니다:

```yaml
---
name: my-skill # Skill 식별자 (필수)
description: ... # Skill 설명 및 Trigger 조건 (필수)
---
```

- `name`: Skill의 고유 식별자
- `description`: Skill이 **언제 활성화되어야 하는지**를 설명합니다. Codex는 자연어 입력과 이 필드를 기준으로 skill을 matching합니다.

Codex bundle의 `SKILL.md` frontmatter는 strict schema를 따릅니다. `name`과 `description` 외의 key는 넣지 않습니다. Tool 제한이나 runtime 의존성은 frontmatter가 아니라 본문 workflow와 `## Integration`에 설명합니다.

### Dynamic Context

Codex skill 본문은 실행 절차와 필요한 command를 명시하지만, command output을 frontmatter나 metadata로 자동 주입하지 않습니다. 최신 상태가 필요한 경우 workflow step에서 command를 직접 실행하도록 안내합니다.

**예시:**

```markdown
## Context

- Current branch: !`git branch --show-current`
- Changed files: !`git status --short`
```

위와 같이 command를 명시하면, skill을 수행하는 agent가 필요한 시점에 직접 실행해 근거를 확보할 수 있습니다.

### Bundled Resource

Skill Directory 내에 추가 파일(Template, Script, Reference 등)을 포함할 수 있습니다:

```
my-skill/
├── SKILL.md              # Skill 정의 (필수)
├── scripts/              # 반복 작업용 실행 Script
├── references/           # 필요 시 Context에 로드할 참조 문서
└── assets/               # Output에 사용할 Template, Icon 등
```

SKILL.md 본문에서 Bundled Resource를 명확히 참조하고, 언제 해당 파일을 읽어야 하는지 안내를 포함하는 것이 좋습니다.

**예시:**

```markdown
Plan 생성 시 `references/small-plan-template.md`의 Template 구조를 따릅니다.
```

## 적용 방법

### Project 전용 적용

특정 Project에서만 Skill을 사용하고 싶을 때 적용합니다.

**설정 경로:**

```
<project-root>/.codex/skills/<skill-name>/SKILL.md
```

**적용 방법:**

1. Project Root에 `.codex/skills/` Directory를 생성
2. 사용할 Skill 폴더를 해당 Directory에 복사
3. Codex가 해당 Project에서 작업 시 Skill을 인식

```bash
# 예시: ywc-create-pr를 project-local skill로 배치
mkdir -p <project-root>/.codex/skills/ywc-create-pr
cp -R codex/skills/ywc-create-pr <project-root>/.codex/skills/
```

**특징:**

- 해당 Project Directory에서 Codex를 실행할 때만 활성화
- Git Repository에 포함하여 팀원과 공유 가능
- Project 별로 다른 Skill 구성 가능

---

### Global 적용 (컴퓨터 전체)

모든 Project에서 공통으로 사용할 Skill을 설정할 때 적용합니다.

**설정 경로:**

```
${CODEX_HOME:-~/.codex}/skills/<skill-name>/SKILL.md
```

**적용 방법:**

1. Home Directory의 `${CODEX_HOME:-~/.codex}/skills/` Directory를 생성
2. 사용할 Skill 폴더를 해당 Directory에 복사
3. 어떤 Project에서든 Codex가 Skill을 인식

```bash
# 예시: ywc-create-pr를 global skill로 배치
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R codex/skills/ywc-create-pr "${CODEX_HOME:-$HOME/.codex}/skills/"
```

**모든 Skill 일괄 적용 (`scripts/install.sh`):**

이 Repository 의 Skill과 Agent를 `${CODEX_HOME:-~/.codex}` 아래로 일괄 설치하려면 번들된 install script를 사용합니다. 단순 `cp -R` 보다 안전합니다 — Skill 검증(`SKILL.md` 존재 확인), Agent 설치, 개별 Skill 선택, manifest 기반 prune을 지원합니다.

```bash
# 모든 Skill + Agent 설치
bash scripts/install.sh --all

# Skill 만 설치
bash scripts/install.sh --codex

# Agent 만 설치
bash scripts/install.sh --codex-agents

# 특정 Skill 만 설치 (Agent는 변경하지 않음)
bash scripts/install.sh --codex ywc-create-pr ywc-sequential-executor ywc-task-generator

# 목적지 override (sandbox, 다른 profile 등)
CODEX_HOME=/tmp/codex-home bash scripts/install.sh --all

# 도움말
bash scripts/install.sh --help
```

**동작 요약:**

- 각 Skill 에 대해 `<dest>/<skill-name>` Directory 를 **삭제 후 복사**합니다 (hard overwrite). "로컬 source tree 와 목적지를 동기화" 하는 workflow 전용입니다.
- full install 시 `agents/*.toml`도 `${CODEX_HOME:-~/.codex}/agents`로 복사합니다.
- 루트에 `SKILL.md` 가 없는 Directory (예: `scripts/` 자체) 는 자동으로 skip 되므로, 사고로 멀쩡한 목적지 Skill 을 덮어쓰는 일이 없습니다.
- 삭제 검증이 복사 **이전에** 수행되므로, 소스가 유효하지 않으면 목적지에 손을 대지 않습니다.
- 목적지 default 는 `${CODEX_HOME:-~/.codex}/skills` 및 `${CODEX_HOME:-~/.codex}/agents`입니다.
- 설치 후 Codex 를 재시작하면 새 Skill과 Agent가 로드됩니다.

> **주의:** 동일 이름의 기존 Global Skill 은 덮어써집니다. 보존이 필요하면 먼저 `${CODEX_HOME:-~/.codex}/skills/` 를 Backup 하거나, `CODEX_HOME`으로 다른 경로에 설치해보세요.

**Marketplace package 동기화:**

`codex/skills/`는 Codex skill의 source of truth입니다. `codex plugin add`로 설치되는 marketplace package는 `plugins/ywc-agent-toolkit/skills/`에 커밋되는 generated artifact이며, Codex는 설치 시 bash script를 실행하지 않습니다. 따라서 `codex/skills/`를 수정한 뒤 marketplace 설치도 최신으로 유지하려면 아래 명령을 실행하고 결과를 함께 커밋하세요.

```bash
bash scripts/sync-codex-plugin.sh
bash scripts/validate.sh
```

**특징:**

- 컴퓨터의 모든 Project에서 활성화
- 개인 Workflow에 맞는 공통 Skill 관리에 적합
- Git Repository에 포함되지 않으므로 팀원과 공유되지 않음

---

### 적용 범위 비교

| 항목      | Project 전용                | Global              |
| --------- | --------------------------- | ------------------- |
| 경로      | `<project>/.codex/skills/` | `${CODEX_HOME:-~/.codex}/skills/` |
| 적용 범위 | 해당 Project만              | 모든 Project        |
| 팀 공유   | Git을 통해 공유 가능        | 불가 (개인 설정)    |
| 사용 사례 | Project 고유 Workflow       | 개인 공통 Workflow  |

> **참고:** 동일한 이름의 Skill이 Project와 Global에 모두 존재할 경우, Project 전용 Skill을 더 구체적인 local override로 취급하는 것이 유지보수상 안전합니다.

## Directory 구조

```text
codex/
├── agents/                         # Codex custom agent TOML files
└── skills/
    ├── README.md                   # 이 catalog
    ├── references/                 # bundle 공통 reference
    └── ywc-<skill-name>/
        ├── SKILL.md                # Codex skill 본문
        ├── README.md               # Korean guide
        ├── README.en.md            # English guide
        ├── README.ja.md            # Japanese guide
        ├── README.ko.md            # Korean locale guide
        ├── agents/openai.yaml      # Codex UI metadata
│       ├── references/             # on-demand reference
│       ├── scripts/                # deterministic helper scripts
│       └── evals/evals.json        # objectively verifiable smoke fixtures
├── README.md
├── README.ko.md
├── README.en.md
├── README.ja.md
├── CHANGELOG.md
└── VERSION
```
