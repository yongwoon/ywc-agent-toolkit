# Spec: ywc-toolkit-eval 2026-07-06 개선 백로그 실장

> Status: Draft (ywc-spec-validate 대기)
> Scale: Medium (~11 tasks, 4 모듈 접촉: skills / agents / evals / codex mirrors)
> Source: `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (2026-07-06 full sweep)
> Created: 2026-07-06

> **Operative Sections** (task-generator 우선순위): AC1·AC12·OQ1·NFR·FR1 은 `## Iteration 1 Amendments`가
> 권위 있는 최신본입니다. 원본 AC1/AC12/OQ1/NFR의 S1 산출·검증 문구는 `⚠️ SUPERSEDED` 표시된 대로
> Amendment로 대체되었습니다.

## Purpose

2026-07-06 `ywc-toolkit-eval --mode full --target all` 평가에서 도출된 개선 백로그 10건을
실장하여, 다음 회차 재평가 시 해당 항목들의 판단축 점수(S3 / A1) 및 커버리지 공백(S1)을
해소한다. 모든 변경은 스킬/에이전트의 **메타데이터·문서·평가 픽스처**에 국한되며, 어떤
스킬의 런타임 실행 로직도 재설계하지 않는다.

## Why

- `ywc-setup-language`는 신규 스킬로 `trigger-cases.json`에 케이스가 전무하여 활성화 정확도(S1)를
  검증할 수 없다(잠정 3점). 활성화는 전체 카탈로그 품질에 대한 최고 가중치 축이므로 최우선.
- S3=4(행동 효능) 5건, A1=4(역할 경계) 4건은 모두 "본문만으로 실행 불가한 한 단계" 또는
  "형제와의 소유권 경계 모호"에서 비롯된 경미하지만 실재하는 결함이다.
- 조기 수정 비용(줄 단위 편집)이 재평가 회차마다 반복 지적되는 비용보다 압도적으로 싸다.

## Scope

- `claude-code/skills/` 5개 스킬 SKILL.md 편집(project-docs, project-scaffold, merge-dependabot,
  product-review, tdd-ritual).
- `claude-code/agents/` 4개 에이전트 .md 편집(backend-coder, frontend-coder, doc-writer, qa-engineer).
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`에 `ywc-setup-language` 케이스 추가.
- 위 5개 스킬의 **Codex 미러**(`codex/skills/<skill>/SKILL.md`) 동기화 — 해당 결함이 미러에도
  존재하는 경우에 한함.
- 각 태스크 완료 후 `bash scripts/validate.sh` 및 대상 항목 `score.py` 재채점으로 검증.

## Out of Scope

- 스킬 런타임 로직/워크플로우 재설계 — 본 실장은 문서·메타데이터·픽스처 편집만 수행.
- `score.py` 채점 로직 또는 기계적 baseline(`history.mechanical.json`) 변경.
- `scorecard.md` / `history.json` 재생성 — 이들은 git-ignored 로컬 산출물이며, 재평가는 실장
  완료 후 별도 `ywc-toolkit-eval` 실행으로 수행.
- **Codex 에이전트** TOML 편집 — `codex/agents/`에는 해당 4개 에이전트의 미러가 없으므로 A1
  수정은 Claude Code 전용.
- `ywc-setup-language`의 Codex 대응 — Codex에는 `ywc-setup`(다른 스킬)만 존재하고, Codex 평가는
  `.codex/skills/ywc-codex-toolkit-eval`가 독립적으로 소유하므로 본 spec 대상 외.
- 다른 세션이 생성한 미추적 파일(`plan.md`, `docs/skill-agent-eval/codex/*`) — 본 실장과 무관.

## Existing Constraints Touched (file:line 인용)

| 대상 | 근거 위치 | 확인된 실제 상태 |
|---|---|---|
| product-review "P0/P1/P2" | `claude-code/skills/ywc-product-review/SKILL.md:26` | P0/P1/P2는 **Rationalization Defense의 excuse 문자열 내부**에만 등장. 워크플로우 본문(:75-77, :95)은 High/Medium/Low로 일관됨. 즉 실제 모순이 아니라 excuse 문구가 외래 어휘를 도입한 것 → **경미(clarify)** 로 재분류. |
| merge-dependabot 충돌 경로 | `SKILL.md:30` (defense) ↔ `:150-162` (수동 checkout+resolve) | 진짜 긴장. :30은 `@dependabot rebase` 권고, :150-162는 수동 해결 절차 제공. 두 경로의 적용 조건 명시 필요. |
| tdd-ritual 테스트 커맨드 | `SKILL.md:74` | `<run the test, scoped to just the new test>` placeholder 확정. 러너 추론 규칙 부재. |
| project-scaffold reference 로드 | `SKILL.md:80-85` | "Read language-specific Reference files" + 언어별 목록. 매칭 reference 부재 시 fallback 미명시. |
| project-docs 설명·본문 | 설명 `SKILL.md:4` (Specification을 doc 대상으로 명시하나 ywc-spec-writer anti-trigger 부재); 본문 `:70-75` (디렉토리/명명 결정을 `../references/project-docs-structure.md`로 외부화) | 둘 다 확정. anti-trigger 1건 추가 + reference 로드를 필수 Step으로 승격. |
| backend-coder Mission | `claude-code/agents/ywc-backend-coder.md:21-24` | "unit + integration tests that cover the [code]" — 설명의 anti-trigger("co-located ... SAME task")는 이미 정확하나 **본문 Mission이 그보다 넓음**. 본문을 설명에 맞춰 축소. |
| qa-engineer Mission | `claude-code/agents/ywc-qa-engineer.md:22-24`, `:77` | 본문이 E2E suites 저작 + ":77 'or reviewing them'"으로 e2e-test-strategy / impl-review와 중첩. |
| frontend-coder | `claude-code/agents/ywc-frontend-coder.md:19` 부근 | 컴포넌트 테스트 소유가 qa-engineer 단위 테스트와 중첩(backend와 동형 픽스). |
| doc-writer | `claude-code/agents/ywc-doc-writer.md:25` | scope umbrella가 3개 스킬 영역과 겹침; glossary는 ywc-ubiquitous-language 우선 라우팅 명시 필요. |
| trigger-cases 스키마 | `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` | 케이스 shape: `{id, prompt, expected, kind, impostor?, note?}`. kind ∈ positive/collision/negative. 커버리지 규칙: 항목당 positive≥3, collision(owner+impostor 합산)≥2. |
| Codex 미러 존재 | `codex/skills/{project-docs,project-scaffold,merge-dependabot,product-review,tdd-ritual}/` | 5개 모두 미러 존재 → SKILL.md 결함이 미러에도 있으면 동기화 필요. validate.sh가 sync 검증. |

## Acceptance Criteria

- **AC1** (setup-language): `trigger-cases.json`에 `expected: ywc-setup-language`인 positive ≥3, 그리고
  owner/impostor 합산 collision ≥2가 추가되고, `score.py --target claude-code/skills --item ywc-setup-language`가
  더 이상 `COV_LOW`를 보고하지 않으며 S1이 케이스 기반으로 산출된다.
  > ⚠️ SUPERSEDED by Iteration 1 — see §AC1′ (score.py는 S1을 산출하지 않음; coverage.sufficient 신호만 변경).
- **AC2** (project-docs): 설명에 `Specification 문서는 ywc-spec-writer 사용` 취지의 anti-trigger가 추가되고,
  본문에서 reference 로드가 문서 생성 전 **필수 단계**로 승격(또는 최소 디렉토리/명명 결정을 본문에 인라인)되어
  본문만으로 canonical "generate a doc" 시나리오가 실행 가능하다.
- **AC3** (project-scaffold): `SKILL.md:80` 부근에 매칭 language reference 부재 시 fallback 규칙("일반 원칙으로
  진행" 또는 "사용자에게 확인")이 명시된다.
- **AC4** (merge-dependabot): `:150-162` 수동 충돌 해결 경로와 `:30` `@dependabot rebase` 권고의 적용 조건이
  명시적으로 구분된다(예: "먼저 `@dependabot rebase`; rebase 실패 시에만 수동 해결").
- **AC5** (product-review): `:26` excuse 문자열이 High/Medium/Low 어휘로 통일되거나, 본 항목이 결함이 아님을
  근거와 함께 기록한다(둘 중 하나면 AC 충족).
- **AC6** (tdd-ritual): `:74` placeholder가 프로젝트 테스트 러너 추론 규칙("package.json/pyproject의 test
  스크립트 사용; 부재 시 사용자에게 확인")으로 대체된다.
- **AC7** (backend-coder): Mission이 "동일 태스크에서 저작한 코드에 대한 co-located 테스트"로 축소되어 설명의
  기존 anti-trigger와 일치한다.
- **AC8** (frontend-coder): 자체 소유 테스트가 "구현 중인 컴포넌트"로 한정되고 standalone/coverage-gap 테스트는
  ywc-qa-engineer로 라우팅됨이 본문에 명시된다.
- **AC9** (doc-writer): glossary 항목은 ywc-ubiquitous-language가 본 에이전트를 dispatch한다는 취지의 라우팅
  노트가 추가된다.
- **AC10** (qa-engineer): 본문의 "or reviewing them" 문구와 standalone E2E 저작 주장이 제거되고, E2E 전략은
  ywc-e2e-test-strategy 소유로 남는다.
- **AC11** (Codex sync): AC2~AC6로 변경된 5개 스킬의 결함이 Codex 미러에도 존재하는 경우 동일하게 반영되고,
  `bash scripts/validate.sh`가 exit 0.
- **AC12** (전체 검증): 모든 태스크 후 `bash scripts/validate.sh` exit 0, 그리고 재평가 시 대상 항목의 해당
  판단축이 5점(또는 setup-language S1이 케이스 기반 산출)으로 상승.
  > ⚠️ SUPERSEDED by Iteration 1 — see §AC12′ (완료 게이트와 다음-회차 기대치 분리; validate.sh는 eval 픽스처 미커버).

## Functional Requirements

- **FR1** → AC1: `trigger-cases.json`에 setup-language 케이스 세트 추가. positive는 ko/ja/en 혼합("출력 언어
  설정", "set project language", "言語設定"). collision은 실제로 경합하는 형제를 지목해야 함 —
  Open Question OQ1에서 후보 확정.
- **FR2** → AC2: project-docs 설명 anti-trigger 1줄 추가 + 본문 reference 로드 단계 승격. 설명 변경은 S1
  회귀 방지를 위해 기존 트리거 문구를 보존하고 anti-trigger만 append.
- **FR3** → AC3: project-scaffold Step 2에 fallback 문장 1개 추가.
- **FR4** → AC4: merge-dependabot 충돌 절차에 선행조건(`@dependabot rebase` 우선) 명문화.
- **FR5** → AC5: product-review :26 excuse 어휘 통일 또는 non-defect 기록.
- **FR6** → AC6: tdd-ritual :74 placeholder를 러너 추론 규칙으로 대체.
- **FR7** → AC7: backend-coder Mission 테스트 소유 범위 축소.
- **FR8** → AC8: frontend-coder 테스트 소유 범위 한정 + 라우팅 명시.
- **FR9** → AC9: doc-writer glossary 라우팅 노트 추가.
- **FR10** → AC10: qa-engineer 리뷰/E2E-저작 문구 정리.
- **FR11** → AC11: 변경된 스킬의 Codex 미러 동기화(필요 시).

## Edge Cases

- **EC1** (S1 회귀 위험): project-docs 설명에 anti-trigger를 추가할 때 문장이 과도해지면 기존 활성화(정밀도)를
  해칠 수 있다. append-only로 최소 변경하고, 재평가에서 project-docs 및 그 형제(spec-writer)의 S1 재현율이
  유지되는지 확인(양방향).
- **EC2** (collision 부재): setup-language가 충분히 고유하여 진짜 경합 형제가 없을 수 있다. 이 경우 collision을
  "per-call --lang override 요청"을 `expected: null`(negative)로 두는 것으로 대체하지 말 것 — 커버리지 규칙은
  collision을 요구하므로, 후보 형제(OQ1)를 지목하거나 규칙 예외를 eval 소유자가 승인해야 한다.
- **EC3** (Codex 미러 결함 부재): 5개 미러 중 일부는 해당 결함이 없을 수 있다(미러가 이미 다른 문구). 각 미러를
  개별 확인 후 diff가 있을 때만 편집 — 맹목적 복사 금지.
- **EC4** (validate.sh sync gate): Codex 미러 편집 시 `.githooks/pre-commit`이 `plugins/ywc-agent-toolkit` 동기화를
  트리거한다. 생성 패키지를 수기 편집하지 말고 sync 스크립트/훅에 위임.

## Non-Functional Requirements

- 각 태스크는 단일 항목만 변경하고 독립 커밋 → 재평가 시 항목별 점수 이동을 추적 가능하게.
- 문서 언어는 프로젝트 관례(문서=한국어, 기술용어=영어) 준수.
- 활성화 관련 편집(FR1/FR2)은 재평가로 정밀도/재현율 무회귀를 확인하기 전까지 완료로 간주하지 않음.

## Task Grouping 제안 (task-generator 힌트)

독립적·병렬 실행 가능. 3개 레인으로 묶을 수 있음:
1. **Eval 픽스처 레인**: FR1(setup-language 케이스) — evals만 접촉, 다른 레인과 무의존.
2. **스킬 문서 레인**: FR2~FR6 + FR11(Codex 미러) — 스킬별 독립 태스크, 각자 미러 동기화 포함.
3. **에이전트 경계 레인**: FR7~FR10 — 4개 에이전트 독립 태스크(단, 테스트 소유권은 상호 참조하므로
   backend/frontend/qa는 동일 "co-located vs standalone" 규칙을 공유해야 함 → 규칙 문구를 먼저 확정 후 3개에 적용).

## Open Questions

- **OQ1**: `ywc-setup-language`의 collision 형제 후보 확정 필요. 후보: (a) `ywc-project-mission`("프로젝트 설정"
  표면 경합), (b) 소비 스킬(`ywc-commit`/`ywc-create-pr`)에 대해 "커밋 메시지 언어 바꿔줘"류를 setup-language로
  라우팅해야 하는지 vs per-call override인지. eval 소유자(사용자) 판단 필요.
  > ⚠️ SUPERSEDED by Iteration 1 — see §OQ1′ (FR1 blocking으로 승격 + fallback 명시).
- **OQ2**: product-review(FR5)를 실제 편집할지, non-defect로 기록만 할지. 근거상 후자가 타당하나 최종 결정은
  사용자 몫.

## Confidence Gate

Confidence: 88/100 — PROCEED

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 92 | 10개 백로그 항목이 file:line으로 확정됨. |
| Architecture compliance | 95 | 문서/메타데이터 편집만; 구조 변경 없음. Step 3.5 advisor gate 불필요. |
| Evidence quality | 90 | 전 항목을 실제 파일에서 재검증(product-review 오탐 포함 정정). |
| Reuse verified | 85 | trigger-cases 스키마·validate.sh·score.py 재사용 확인. Codex 미러 sync 경로 확인. |
| Root cause identified | 80 | 대부분 확정. OQ1(collision 형제)·OQ2(product-review 편집 여부) 2건 미해결. |

## Iteration 1 Amendments

ywc-spec-validate Iteration 1 결과(Critical 1, Warning 4, Suggestion 1)를 반영. 실패 항목만 수정하며 나머지
원본 섹션은 그대로 유지한다. 근거는 실제 파일 검증(`score.py:269,340`, `scripts/validate.sh`, `git ls-files`).

### 실패 요인 (from ywc-spec-validate)

- **Critical**: AC1/AC12/Purpose가 "FR1이 score.py로 S1을 산출한다"고 오기술. 실제로 `score.py:340`은 coverage를
  signals-only로 두고 `axes.S1 = null`(Amendment A2)을 유지 — S1은 판단-tier 활성화 판정관이 산출.
- **Warning W1**: AC1의 `COV_LOW`는 score.py에 존재하지 않는 토큰(내 aggregate 라벨). 실제 신호는 `coverage.sufficient`.
- **Warning W2**: NFR ↔ Out of Scope 모순(재평가는 out of scope인데 완료 게이트가 점수 이동에 의존).
- **Warning W3**: `validate.sh`는 Claude-code eval 픽스처를 커버하지 않음(확인) — FR1 검증은 `score.py` coverage.
- **Warning W4**: OQ1(collision 형제)은 EC2상 사실상 FR1 blocking.
- **Suggestion**: AC10이 qa-engineer의 dispatched E2E 저작 능력까지 과도 축소할 위험.

### 개정된 Acceptance Criteria

- **§AC1′** (AC1 대체): `trigger-cases.json`에 `expected: ywc-setup-language`인 positive ≥3, owner/impostor 합산
  collision ≥2를 추가한다. 검증: `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills
  --item ywc-setup-language --format json`의 `signals.coverage.sufficient == true`이고, 실행 시 stderr의
  "N items below minimum" 경고에 ywc-setup-language가 더 이상 포함되지 않는다. **S1 자체는 본 태스크가 산출하지
  않는다** — S1은 후속 `ywc-toolkit-eval` 판단-tier 활성화 판정관이 신규 케이스로 산출한다.
- **§AC12′** (AC12 대체) — 두 부분으로 분리:
  - **완료 게이트(구현 시점 검증 가능)**: 모든 태스크 후 `bash scripts/validate.sh` exit 0, 그리고 편집된 각
    항목이 `score.py`(스킬/에이전트) 또는 `coverage.sufficient`(FR1) 기준으로 회귀 없음. `validate.sh`는 eval
    픽스처를 커버하지 않으므로 FR1의 게이트는 `score.py` coverage 단독이다.
  - **연기된 기대치(다음 회차)**: 대상 판단축(S3/A1/S1)의 5점(또는 setup-language S1 산출) 상승은 실장 완료 후
    별도 `ywc-toolkit-eval` 실행에서 확인하며, 본 실장의 완료 조건이 아니다(Out of Scope와 정합).

### 개정된 Open Question

- **§OQ1′** (OQ1 대체, FR1 **blocking**): FR1은 실재 경합 형제를 지목하는 collision ≥2를 요구하므로 OQ1 미해결
  시 FR1을 완료할 수 없다. 해결 경로: (1) 후보 형제 확정(권장: `ywc-project-mission` — "프로젝트 설정" 표면
  경합) 또는 (2) 진짜 경합 형제가 없다고 판단되면 eval 소유자(사용자)가 커버리지 규칙(collision≥2) 예외를
  명시 승인. **fallback**: 승인 시 collision을 negative로 대체하지 말고(EC2), `score.py`의 `COVERAGE_MIN_COLLISIONS`
  예외를 문서화한다. 이 결정 전까지 FR1 태스크는 착수 불가 상태로 표시한다.

### 개정된 Functional Requirement

- **§FR1′** (FR1 검증 문구 대체): positive는 ko/ja/en 혼합. collision은 §OQ1′에서 확정된 형제를 지목. 완료 검증은
  §AC1′의 `coverage.sufficient == true` — `validate.sh`가 아님.

### 개정된 Suggestion 반영 (AC10)

- **§AC10′** (AC10 정제): qa-engineer 본문에서 제거 대상은 **E2E 전략/소유권 주장**("or reviewing them",
  "E2E suites 저작을 스스로 소유")에 한정한다. `ywc-e2e-test-strategy`가 dispatch했을 때 codified E2E 테스트를
  **작성**하는 능력은 보존한다(에이전트 카탈로그 설명과 정합).

### Step 4b.5 재실행 (원본 + Amendment 전체)

- Pass A(교차 일관성): §AC1′↔§FR1′ 검증 문구 일치; §AC12′ 완료 게이트가 Out of Scope와 무모순; 신규 상태값·API
  없음. ✓
- Pass B(주장↔현실): §AC1′는 `score.py:269,340` 검증 반영; §AC12′의 "validate.sh 미커버"는 `scripts/validate.sh`
  grep으로 확인; trigger-cases.json git-tracked 확인(`git ls-files`). ✓
- Pass C(스키마): Data Model/DB 없음 — 해당 없음.

### 개정 Confidence Gate

Confidence: 90/100 — PROCEED. Critical 해소(S1 전제 정정), OQ1을 blocking으로 명시하여 미해결이 아닌 "결정
대기"로 상태화. 잔여는 OQ2(product-review 편집 여부, 비차단) 뿐.
