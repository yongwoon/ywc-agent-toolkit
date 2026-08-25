# Claude Code Skill Bundle — SDLC v1.1 개선 계획 (ywc-agent-toolkit 반영본)

> Status: Draft
> Scale: Medium
> Created: 2026-07-15
> Scope root: `claude-code/` (this repository — `ywc-agent-toolkit`)
> Source plan: `develop-with-llm/docs/ywc-plans/260715-001-claude-code-sdlc-v11-improvements.md` (원본, `tools/claude-code/` 경로 기준)
> Sibling spec: `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` (codex 번들 대상, Large scale, 독립 scope — Existing Constraints Touched 참조)
> Path mapping: 원본의 `tools/claude-code/skills/…` → 이 저장소의 `claude-code/skills/…`

## Purpose

원본 계획(`develop-with-llm` 저장소)이 정의한 SDLC v1.1 개선 5개 지점을, 이 저장소(`ywc-agent-toolkit`)의 `claude-code/skills` 툴킷에 반영하기 위한 구현 계획이다. 개선 항목은 `ywc-tdd-ritual`, `ywc-plan`, `ywc-task-generator`, `ywc-impl-review` 4개 skill과 신규 공유 참조 파일 1개(`code-smell-baseline.md`)에 걸친다. 애플리케이션 코드 변경은 없으며, skill prompt 텍스트(SKILL.md·references)만 대상으로 한다.

원본은 `tools/claude-code/` 레이아웃(develop-with-llm 저장소)을 전제로 작성되었다. 이 반영본은 동일한 6개 FR을 이 저장소의 실제 파일 상태에 대해 재검증하고 경로를 재매핑한 것이다. 재검증 결과 라인 수만 근소하게 다를 뿐(아래 Existing Constraints Touched 참조) 모든 구조적 제약과 headroom 판단은 원본과 동일하게 성립한다.

## Scope

- `ywc-tdd-ritual`: Step 1(RED)에 "public seam 사전 스케치 → 기존 seam 우선 → 사용자 확인" 절차를 명시적으로 추가하고, Common Mistakes에 tautological-test 패턴을 추가한다. 대응 Rationalization Defense row 2개를 추가한다.
- `ywc-plan`: `references/spec-template.md`의 Acceptance Criteria 안내 문단에 seam 명명을 권장하는 한 줄을 추가한다(신규 최상위 섹션은 만들지 않음 — Existing Constraints Touched 참조).
- `ywc-task-generator`: Task Design Principles에 "Wide Refactor(expand→migrate→contract) 예외"를 5번째 원칙으로 추가한다.
- `ywc-impl-review`: Output Format에 `### Spec Traceability` 섹션(AC별 Implemented/Partial/Missing/Not Verifiable 분류)을 추가하고, 신규 공유 참조 파일 `references/code-smell-baseline.md`(Fowler 12-smell)를 만들어 `architecture-agent.md`/`design-agent.md`에서 참조한다.
- 위 4개 skill 각각에 대해 `ywc-skill-author`의 Validation Checklist를 실행하고 `bash scripts/validate.sh` 통과를 확인한다.

## Out of Scope

- `codex/skills/`, `plugins/ywc-agent-toolkit/`(Codex marketplace mirror) 등 다른 root의 수정 — 이 저장소의 `claude-code/skills/CLAUDE.md` "Codex-skill: Maintained Independently" 규칙에 따라 두 root는 독립 관리되며 자동 전파 의무가 없다. codex 쪽 동일 개선은 이미 별도 sibling plan(`codex-skill-sdlc-v11-improvements.md`, Large scale, Draft)이 존재하며 이 spec과 독립적으로 진행한다.
- Wayfinder류 decision-map skill 신설, `ywc-task-generator`의 approval-preview gate, `ywc-tech-research`의 artifact 영속화 — 이들은 codex sibling plan의 범위이며, claude-code 쪽 포팅 여부는 이 spec의 Open Questions에만 기록하고 별도 후속 계획으로 남긴다.
- Throwaway prototype skill 신설 — 원 검토에서 우선순위 낮음으로 분류, 이번 범위에서 제외.
- `ywc-brainstorm` 수정 — 기존 구현이 이미 one-question-at-a-time·confirmation gate·facts-vs-decisions 구분을 충족(원 review 결과).
- 신규 6번째 impl-review subagent 도입 — FR-4는 기존 5-subagent Phase1/Phase2 산출물을 aggregation만 하며, 신규 워커를 추가하지 않는다(codex sibling의 "aggregate-only, no sixth worker in v1" 결정과 동일 원칙).

## Existing Constraints Touched

원본의 `tools/claude-code/…` 경로를 이 저장소 `claude-code/…` 경로로 재매핑하고, 각 파일의 현재 상태를 직접 읽어 재검증했다. 라인 수는 이 저장소 기준(원본 값은 괄호로 병기).

| Existing artifact (this repo) | Verified behavior (직접 읽고 확인) | Planned interaction |
|---|---|---|
| `claude-code/skills/ywc-plan/references/spec-template.md` (읽음) | "Testing Decisions" 섹션은 존재하지 않음. `## Acceptance Criteria`(line 48) 아래 "Preferred form for each AC:"(line 52) 안내 문단이 있음 | Acceptance Criteria 섹션의 설명 문단에 seam 명명 권장 한 줄만 추가. 신규 최상위 섹션 생성하지 않음(원 review의 "Testing Decisions 섹션에 추가" 가정은 부정확 — 이 spec에서 정정) |
| `claude-code/skills/ywc-tdd-ritual/SKILL.md` (188 lines; 원본 184, cap 500) | Step 1(RED)에 seam 사전합의 절차 없음. Common Mistakes 5개 항목에 tautological-test 패턴 없음. Rationalization Defense 표 존재 | Step 1에 `### Seams` 서브섹션 추가(~15줄), Common Mistakes에 6번째 항목 추가(~8줄), Rationalization Defense 표에 대응 row 2개 추가 |
| `claude-code/skills/ywc-tdd-ritual/references/test-shape-cookbook.md` (존재 확인) | seam 관련 예시가 산재하나 사전 합의·사용자 확인 절차는 없음 | 변경 없음 — 절차는 SKILL.md 본문(workflow prose, A14 예외로 Tier 2 유지)에서 처리하고 이 파일을 예시 pointer로 교차 참조 |
| `claude-code/skills/ywc-task-generator/SKILL.md` (423 lines; 원본 440, cap 500, headroom ~77줄) | Task Design Principles(line 55)는 4개 원칙: 1. Reviewability(57) / 2. Dependency Safety(67) / 3. Database Migration Separation(74) / 4. Library Introduction Separation(80). Wide Refactor 예외 없음 | 5번째 원칙 `### 5. Wide Refactor Exception (Expand-Contract)` 추가는 inline 15~20줄 이내로 제한. 상세 worked example이 필요하면 `references/example-decomposition.md`(신규)에 추가하고 SKILL.md에는 1줄 pointer만 |
| `claude-code/skills/ywc-task-generator/references/example-decomposition.md` | 미존재 | FR-3 worked example이 20줄을 넘을 때에만 신규 생성(조건부). 기존 references/에 `granularity-modes.md` 등 static content 파일이 다수 있어 신규 파일 추가는 관례와 합치 |
| `claude-code/skills/ywc-impl-review/SKILL.md` (218 lines; 원본 215, cap 500) | `## Output Format`(line 101) 아래 `### Testing (QA)`(127) → `### Fix Priority`(131) 순서. Spec 적합성 통합 섹션 없음. `--spec` argument는 현재 **required**(line 36). BLOCKED = "spec file missing"(line 169). `--format markdown\|html` 지원(line 44), HTML mode 규약(line 174) | Testing (QA)와 Fix Priority 사이에 `### Spec Traceability` 섹션 추가(~20줄). FR-4에서 `--spec`을 **optional**로 변경(생략=No spec available/valid, 공급됐으나 missing=BLOCKED 현행 유지). Spec Traceability matrix는 HTML mode에서도 렌더 |
| `claude-code/skills/ywc-impl-review/references/architecture-agent.md` (읽음) | Structural Spec Conformance 등 dimension 존재하나 Fowler 12-smell 명시 목록 없음 | 파일 말미에 `code-smell-baseline.md` 참조 pointer 추가(1줄) |
| `claude-code/skills/ywc-impl-review/references/design-agent.md` (읽음) | Naming Consistency dimension 존재하나 Mysterious Name 등 Fowler 용어 미사용 | Naming Consistency 절에 `code-smell-baseline.md` 참조 pointer 추가(1줄) |
| `claude-code/skills/ywc-impl-review/references/recurring-defects.md` (상단 읽음) | bot-reviewer 데이터 기반 카탈로그(데이터 계층, NULL 처리, concurrency 등). "공유 catalog, 여러 agent 파일이 참조" 패턴의 정본 | FR-5의 `code-smell-baseline.md`는 이 파일과 동일한 공유-catalog 패턴을 따르되 성격이 다른 구조적 리팩터링 카탈로그. 항목 중복 시 code-smell-baseline.md에서 `recurring-defects.md` 참조로 위임(Edge Cases 참조) |
| `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md` | 미존재 | FR-5에서 신규 생성 |
| `claude-code/skills/CLAUDE.md` 및 `claude-code/skills/ywc-skill-author/SKILL.md` (읽음) | CLAUDE.md "Authoring or Restructuring `ywc-*` Skills"가 body section 추가·신규 참조 파일 생성 시 `ywc-skill-author` 선행 호출을 의무화(typo/link fix 예외에 해당하지 않음). A8 body ≤500 lines, A14 Tier 3 extraction >30줄 static content(workflow prose 예외) | 4개 대상 skill의 모든 수정은 이 rule set을 준수하며, 수정 완료 후 Validation Checklist를 각 skill에 대해 개별 실행(Dependencies 참조) |
| `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` (sibling, Status: Draft, Large scale, 읽음) | codex 번들 대상. `Spec Traceability` matrix를 AC별 `Implemented`/`Partial`/`Missing`/`Not Verifiable` + scope-creep note, "No spec available" fallback, "aggregate-only, no sixth worker in v1"로 설계 | claude-code FR-4의 분류 체계·용어를 이 sibling과 동일하게 정렬(용어 drift 방지 확인 완료). claude-code는 기존 5-subagent Phase1/Phase2·`[P1]`/`[P2]` 마커·severity 기호 체계를 그대로 유지한 채 aggregation만 추가 |

## Acceptance Criteria

각 AC는 `When <trigger>, system does <behavior>, observable as <concrete check>` 형태를 지향한다. skill prompt 텍스트 변경이므로 trigger는 "구현 반영 후", observable은 grep/wc 명령으로 표현한다.

- [ ] **AC1 — Seam 사전합의**: 구현 반영 후, `ywc-tdd-ritual` Step 1(RED)에 "테스트할 public seam을 사전에 스케치하고, 기존 seam을 우선하며, 사용자 확인을 받는다"는 절차가 명시되고 대응 Rationalization Defense row가 존재한다. observable: `grep -n "Seam" claude-code/skills/ywc-tdd-ritual/SKILL.md`가 신규 서브섹션과 RD row를 반환.
- [ ] **AC2 — Tautological test 차단**: 구현 반영 후, `ywc-tdd-ritual` Common Mistakes에 "assertion이 코드와 동일한 로직으로 기댓값을 재계산해 구조적으로 실패할 수 없는 테스트" 패턴이 구체적 예시(`expect(add(a,b)).toBe(a+b)` 류)와 함께 존재한다. observable: `grep -ni "tautolog" claude-code/skills/ywc-tdd-ritual/SKILL.md`가 신규 항목을 반환.
- [ ] **AC3 — Wide Refactor 예외**: 구현 반영 후, `ywc-task-generator` Task Design Principles에 5번째 원칙으로 "blast radius가 전체 코드베이스에 걸치는 기계적 변경은 vertical slice 예외이며 expand → migrate(batch) → contract로 시퀀싱한다"가 명시되고 SKILL.md 본문이 500줄을 넘지 않는다. observable: `wc -l claude-code/skills/ywc-task-generator/SKILL.md` ≤ 500 그리고 `grep -n "Wide Refactor" …`가 신규 섹션을 반환.
- [ ] **AC4 — Spec Traceability 섹션**: 구현 반영 후, `ywc-impl-review` Output Format의 Testing (QA)와 Fix Priority 사이에 `### Spec Traceability`가 추가되어 각 AC를 `Criterion`/`Status`/`Evidence`/`Scope-creep note` 열의 matrix로 제시하며, `Status`는 Implemented/Partial/Missing/Not Verifiable 4단계로 분류한다. `--spec`이 **생략**되면 valid로 간주해 "No spec available — Spec Traceability skipped"만 출력하고, `--spec`이 **공급됐으나 파일이 없거나 읽을 수 없으면** BLOCKED로 처리한다(현행 line 169 semantics 유지). Markdown/HTML(`--format html`) 양쪽에서 동일하게 렌더된다. observable: `grep -n "Spec Traceability" claude-code/skills/ywc-impl-review/SKILL.md`가 Testing과 Fix Priority 사이 line 번호를 반환하고, `--spec` argument 항목이 optional로 갱신됨.
- [ ] **AC5 — Fowler smell baseline**: 구현 반영 후, 신규 `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md`가 12개 smell(Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest)을 "정의 → 발견 신호 → 수정 방향" 형태로 포함하고, 3원칙(repo 문서 우선 / judgement call / tooling 강제 항목 skip)이 명시되며, `architecture-agent.md`와 `design-agent.md` 양쪽에서 pointer로 참조된다. observable: 파일 존재 + 두 agent 파일에서 `grep -n "code-smell-baseline"`가 각각 1건 이상 반환.
- [ ] **AC6 — spec-template 경량 반영**: 구현 반영 후, `ywc-plan`의 `spec-template.md` Acceptance Criteria 안내 문단에 seam 명명 권장 한 줄이 추가되되 신규 최상위 섹션은 생기지 않는다. observable: `grep -ni "seam" claude-code/skills/ywc-plan/references/spec-template.md`가 Acceptance Criteria 섹션 내 한 줄을 반환하고, `grep -c "^## " …` 값이 변경 전과 동일.
- [ ] **AC7 — Skill-author + CI 검증 통과**: 5개 항목 반영 후, `ywc-skill-author` Validation Checklist(Frontmatter/Body/Filesystem/Progressive Disclosure)를 4개 수정 skill 각각에 대해 실행한 결과가 전부 PASS이고 `bash scripts/validate.sh`가 통과한다. observable: validate.sh exit code 0.

## Functional Requirements

FR-1~FR-6는 각각 하나의 skill/파일 변경 단위이며 AC1~AC6와 1:1 대응한다(AC1↔FR-1 … AC6↔FR-6). AC7(검증 통과)은 신규 콘텐츠를 추가하지 않는 **cross-cutting 검증 기준**이므로 별도 FR을 두지 않고, FR-1~FR-6 각각의 구현 완료 시점에 실행하는 공통 게이트로 취급한다(Dependencies 섹션 참조).

### FR-1: TDD Seam 사전합의 절차 (`ywc-tdd-ritual`) — AC1

Step 1(RED)에 `### Seams` 서브섹션을 추가한다.

- 새 behavior의 테스트를 작성하기 전에 "이 테스트가 관측할 public boundary(seam)가 무엇인가"를 한 문장으로 적는다.
- 기존 seam이 있으면 그것을 우선한다(신규 seam 추가는 최후 수단).
- Seam이 불명확하거나 여러 개로 나뉠 수 있는 경우, 진행 전에 사용자에게 확인한다("What's the public interface, and which seam should we test?" 형태의 질문).
- `references/test-shape-cookbook.md`를 이 절차의 구체적 예시로 교차 참조한다(신규 파일 생성 없음, 기존 파일을 pointer로 연결).
- Rationalization Defense 표에 "seam 확인은 오버헤드다, 테스트 대상이 뻔하다" 류 row를 1개 이상 추가하고, 위 Workflow 단계로 wiring한다(ywc-skill-author B9 준수).

### FR-2: Tautological Test Anti-pattern 문서화 (`ywc-tdd-ritual`) — AC2

Common Mistakes 섹션에 6번째 항목을 추가한다(현재 5개 항목 + 1개 추가는 30줄 미만이므로 A14 기준 인라인 유지).

- 패턴명: "Tautological assertion — 기댓값을 프로덕션 코드와 동일한 로직으로 재계산".
- 예시: `expect(add(a, b)).toBe(a + b)`, 손으로 동일하게 파생한 snapshot, 자기 자신과 비교하는 constant assertion.
- 교정 방향: 기댓값은 독립적 출처(리터럴 값, worked example, spec)에서 가져와야 한다.
- Rationalization Defense 표에 "테스트 통과했으니 됐다, 로직이 코드와 같아도 상관없다" 류 row를 1개 추가.

### FR-3: Wide Refactor(Expand-Contract) 예외 (`ywc-task-generator`) — AC3

`## Task Design Principles`에 5번째 원칙 `### 5. Wide Refactor Exception (Expand-Contract)`을 추가한다.

- Blast radius가 코드베이스 전체에 걸치는 기계적 변경(컬럼 rename, 공유 타입 retype 등)은 vertical slice 원칙의 예외임을 명시.
- 시퀀싱 규칙: **expand**(신구 형태 병존 추가, 아무것도 깨지지 않음) → **migrate**(blast radius 단위로 batch 분할, 각 batch가 독립 task, CI green 유지) → **contract**(구형 제거, 모든 migrate batch 완료 후에만).
- 각 migrate batch task는 이전 batch task를 `Depends On`으로 명시.
- **500줄 cap 리스크 대응**: 원칙 설명 자체는 15~20줄 이내로 제한(headroom ~77줄이나 절제 유지). 상세 worked example이 필요하면 `references/example-decomposition.md`(신규)에 별도 절로 추가하고 SKILL.md에는 1줄 pointer만 남긴다.
- Rationalization Defense 표에 "이것도 결국 컬럼 하나 바꾸는 거라 작은 task다" 류 row를 1개 추가.

### FR-4: Spec Traceability 섹션 (`ywc-impl-review`) — AC4

`## Output Format`의 `### Testing (QA)`와 `### Fix Priority` 사이에 `### Spec Traceability` 섹션을 추가한다.

- **Matrix 구조**: 각 Acceptance Criterion을 `Criterion` / `Status` / `Evidence` / `Scope-creep note` 4개 열의 matrix로 제시한다. `Status`는 `Implemented` / `Partial` / `Missing` / `Not Verifiable` 4단계(codex sibling Amendment C와 동일 용어).
- **근거(Evidence) 규칙**: `Implemented`/`Partial`의 Evidence는 반드시 `file:line`, named test/output, 또는 command output이어야 한다. **task 이름이나 commit 메시지로 구현 여부를 추론하지 않는다**(codex Amendment C의 anti-inference 규칙). 근거는 Architecture 서브에이전트의 "Structural Spec Conformance" 및 Design 서브에이전트의 "Contract Spec Conformance" 파인딩에서 추출한다 — 신규 워커를 추가하지 않고 기존 Phase 1 5-subagent 산출물을 aggregation한다.
- **`Not Verifiable` 정밀 semantics**: 특정 AC가 존재하나 admissible evidence가 없을 때에만 사용한다 — spec 자체가 없는 "No spec available" 상태와는 구분한다(codex Amendment C).
- **`--spec` optional화 및 상태 분기**: `--spec`을 optional로 변경한다(현행 argument table은 required). `--spec`이 **생략**되면 valid로 간주해 5개 lane은 그대로 실행하되 aggregate 출력에 `### Spec Traceability` → "No spec available"만 두고 AC 행·상태를 만들지 않는다. `--spec`이 **공급됐으나 파일이 없거나 읽을 수 없으면** BLOCKED로 처리한다(현행 line 169의 "spec file missing → BLOCKED" semantics 유지 — 이 분기가 codex Amendment C의 핵심 정밀화이며, 두 경우를 혼동하지 않는다).
- Scope creep(스펙에 없는 동작)은 각 행의 `Scope-creep note` 또는 별도 sub-bullet으로 보고한다.
- **HTML parity**: `--format html`(line 44/174) 모드에서도 `### Spec Traceability` matrix가 동일하게 렌더되어야 한다. html-output 규약([../references/html-output.md])을 따르며, Markdown surface는 파일 내에 보존된다.
- `## Confidence Gate`의 "Evidence quality" 차원과 자연스럽게 연결됨을 한 줄로 교차 참조한다(중복 서술 없이 pointer만).
- 기존 5-subagent Phase1/Phase2 구조·`[P1]`/`[P2]` 마커·severity 기호 체계는 그대로 유지한다.

### FR-5: Fowler Code Smell Baseline (`ywc-impl-review`) — AC5

신규 파일 `claude-code/skills/ywc-impl-review/references/code-smell-baseline.md`를 생성한다.

- `references/recurring-defects.md`와 동일한 "공유 catalog, 여러 agent 파일이 참조" 패턴을 따른다(중복 방지).
- 12개 Fowler smell을 "정의 → 발견 신호 → 수정 방향" 형태의 표로 정리한다.
- 상단에 3가지 원칙을 명시: (1) 프로젝트가 문서화한 표준이 항상 baseline을 override, (2) 모든 항목은 hard violation이 아닌 judgement call, (3) tooling(linter 등)이 이미 강제하는 항목은 skip — 이는 기존 `ywc-impl-review`의 `--profile chill` 기본값·"nitpick 억제" 철학과 합치한다.
- `architecture-agent.md`(구조적 smell 다수: Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest)와 `design-agent.md`(Mysterious Name — Naming Consistency 절)에서 각각 1줄 pointer로 참조한다. Duplicated Code는 pointer 위치를 architecture-agent.md 우선으로 둔다.

### FR-6: spec-template Seam 포인터 (`ywc-plan`) — AC6

`references/spec-template.md`의 `## Acceptance Criteria` 섹션 설명 문단(Preferred form 예시 앞)에 한 줄을 추가한다.

- 문구 예시: "AC를 작성하기 전에 이 그룹이 검증할 test seam(공개 경계)을 한 문장으로 명명하는 것을 권장한다 — 상세 절차는 `ywc-tdd-ritual`의 Seams를 따른다."
- 신규 최상위 섹션(`## Testing Decisions` 등)은 만들지 않는다 — Existing Constraints Touched에서 확인했듯 그런 섹션은 없다.
- `ywc-tdd-ritual`(FR-1)을 정식 출처로 가리키고, 동일 규칙을 두 파일에 중복 서술하지 않는다. (FR 간 의존: FR-1의 `### Seams` 명칭 확정 후 이 pointer 문구 작성.)

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Body 길이 제약 | 4개 수정 대상 SKILL.md 모두 A8(≤500 lines) 준수. `ywc-task-generator`(423줄)와 `ywc-impl-review`(218줄)는 FR 반영 후 즉시 `wc -l`로 재확인 |
| Progressive Disclosure | 신규 정적 콘텐츠(≥30줄, 예: FR-5의 code-smell-baseline.md)는 A14에 따라 반드시 `references/`로 분리. Workflow/절차 prose(FR-1, FR-2, FR-3의 핵심 규칙)는 길이와 무관하게 SKILL.md 본문(Tier 2) 유지 |
| RD row 커버리지 | FR-1/FR-2/FR-3처럼 새로운 discretionary discipline을 도입하는 항목은 각각 Rationalization Defense 표에 대응 row를 추가하고 해당 Workflow 단계로 wiring(A7 + B9). FR-4/FR-5는 subagent 참조 파일·리포트 구조 변경이므로 신규 RD row 필수는 아님 |
| CI 검증 | 모든 변경 후 `bash scripts/validate.sh`(skill 구조·frontmatter·README locale·shellcheck·`--list` dry run)와 markdownlint 통과 필수 |

## Critical Surfaces

N/A — 애플리케이션 런타임 코드나 사용자 데이터를 다루지 않는 skill prompt 텍스트 변경.

## Data Model

N/A — 데이터 모델 변경 없음.

## API Contract

N/A — API 변경 없음.

## Edge Cases

- **`ywc-task-generator` 500줄 cap 초과 위험**: FR-3 반영 시 inline 설명이 20줄을 넘으면 즉시 worked example을 `references/example-decomposition.md`로 이동해 headroom을 확보한다. 구현 중 `wc -l`을 매 편집 후 확인.
- **codex sibling과의 용어·계약 drift**: FR-4는 sibling(`codex-skill-sdlc-v11-improvements.md`) **Amendment C**(3차 수렴 완료본)와 다음 계약을 정렬했다 — (1) 4단계 Status 용어(Implemented/Partial/Missing/Not Verifiable), (2) matrix 열 구조(Criterion/Status/Evidence/Scope-creep note), (3) anti-inference 규칙(task 이름·commit 메시지로 추론 금지), (4) `--spec` optional화 + "생략=No spec/valid, 공급됐으나 missing=BLOCKED" 분기, (5) `Not Verifiable` = "AC는 있으나 evidence 없음"(No spec available와 구분), (6) HTML parity. 구현 시 sibling Amendment C 문구가 이후 변경되었는지 한 번 재확인한다. 단 claude-code는 기존 5-subagent Phase1/Phase2·`[P1]`/`[P2]`·severity 기호 체계를 유지하며 sibling의 codex-특유 요소(worker 용어 등)는 포팅하지 않는다.
- **Fowler smell과 기존 `recurring-defects.md`의 중복**: `recurring-defects.md`는 bot-reviewer 데이터 기반 카탈로그(데이터 계층, NULL 처리, concurrency 등)이고 Fowler smell은 구조적 리팩터링 카탈로그로 성격이 다르다. 구현 시 두 카탈로그 항목이 겹치지 않는지(예: Shotgun Surgery vs error-swallowing) 한 번 대조하고, 겹치면 code-smell-baseline.md 쪽에서 "recurring-defects.md §N 참조"로 위임한다.
- **`ywc-plan`의 spec-template.md 변경 최소화**: 원 review는 "Testing Decisions 섹션에 추가"를 가정했으나 실제로 그 섹션이 없음이 확인됨(Existing Constraints Touched 참조). 구현자가 이 spec을 보지 않고 원 review 메모만 보고 작업하면 존재하지 않는 섹션을 새로 만드는 실수를 할 수 있다 — AC6이 이를 명시적으로 금지.
- **README locale 파일 영향 없음 확인**: 이번 변경은 SKILL.md 본문·references만 대상이며 README(`.md`/`.en.md`/`.ja.md`/`.ko.md`) 변경을 요구하지 않는다. 신규 skill 디렉터리를 만들지 않으므로 `validate.sh`의 Tier 1 README locale 검사에 추가 대응이 불필요하다.

## Dependencies

- **`ywc-skill-author` 선행 실행 필수**: 이 저장소 `claude-code/skills/CLAUDE.md`의 "Authoring or Restructuring `ywc-*` Skills" 규칙에 따라, 4개 skill의 구조(frontmatter/body section/references)를 수정하기 전에 `ywc-skill-author`를 먼저 호출해 canonical rule set을 로드한다. 이번 변경은 body section 추가(새 서브섹션, 새 RD row)와 신규 참조 파일 생성을 포함하므로 "ad-hoc minor edit"(typo/link fix) 예외에 해당하지 않는다.
- **FR 간 의존**: FR-6(spec-template pointer)은 FR-1(ywc-tdd-ritual Seams)을 정식 출처로 가리키므로, FR-1의 `### Seams` 서브섹션 명칭이 확정된 뒤 FR-6의 pointer 문구를 작성한다.
- **codex sibling과의 순서**: 서로 다른 root(claude-code vs codex)이므로 독립 진행 가능. FR-4 구현 시 sibling의 Spec Traceability 문구를 재확인해 용어 정렬만 유지한다(현재 이미 일치).

## Open Questions

- [ ] codex sibling plan의 Wayfinder / task approval gate / tech-research artifact 영속화를 claude-code 쪽에도 포팅할 가치가 있는지 — 별도 후속 검토 대상으로 남김.
- [ ] `ywc-impl-review`의 Spec Traceability가 실제 리뷰에서 리포트 길이를 얼마나 늘리는지(토큰 비용) — 아직 실측 없음. 초기 구현 후 1~2회 실제 리뷰에 적용해 관찰하고, 과도하면 `--profile chill`처럼 opt-in화 검토.
- [ ] codex sibling **Amendment D**가 도입한 bundle-wide 500-char description-limit validator 규칙을 claude-code 쪽에도 적용할지 — codex는 6개 이상의 over-limit description을 발견해 `scripts/validate.sh`에 결정론적 검사를 추가했다. claude-code/skills에도 유사 over-limit description이 있는지, `validate.sh`에 동일 검사를 넣을지는 이 spec 범위 밖의 별도 후속 검토 대상. (이 plan의 FR은 description 텍스트를 건드리지 않는다.)

## References

- `develop-with-llm/docs/ywc-plans/260715-001-claude-code-sdlc-v11-improvements.md` — 이 반영본의 원본 계획(`tools/claude-code/` 경로 기준)
- `docs/ywc-plans/codex-skill-sdlc-v11-improvements.md` — codex 번들 대상 sibling plan (FR-4 용어 정렬의 근거)
- `claude-code/skills/ywc-skill-author/SKILL.md` 및 `claude-code/skills/ywc-skill-author/references/` — 이번 변경이 준수해야 하는 canonical rule set
- `claude-code/skills/CLAUDE.md` — "Authoring or Restructuring `ywc-*` Skills", "Codex-skill: Maintained Independently" 규칙 근거
- `claude-code/skills/ywc-impl-review/references/recurring-defects.md` — FR-5가 미러링할 공유-catalog 패턴 정본

## Next Step

이 계획은 Medium-scale 변경이므로, 구현 전 `ywc-spec-ready --spec docs/ywc-plans/claude-code-sdlc-v11-improvements.md`로 Critical/Warning을 수렴시킨 뒤 `ywc-task-generator`로 세분화하는 것을 권장한다. 다만 6개 FR이 이미 파일 단위로 명확히 분리되어 있어, 소규모 판단으로 `ywc-skill-author` 선행 호출 후 FR 단위로 직접 구현 → 각 skill별 `ywc-skill-author` Validation Checklist + `bash scripts/validate.sh` 실행도 대안 경로로 유효하다.
