# Claude Code `ywc-auth-implement` Skill Implementation Spec

> Status: Draft
> Scale: Large
> Created: 2026-07-16
> Source: `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm/docs/ywc-plans/260715-002-claude-code-auth-implement-skill.md` (원본, 3회 iteration까지 수렴, Confidence Gate 93/100)
> Target: `claude-code/skills/` source root (Codex 미러는 `codex_auth_implement_skill.md`가 독립적으로 다룬다 — 두 root는 자동 동기화되지 않는다)

## Purpose

숙련된 개발자에게도 인증 기능(이메일/비밀번호, OAuth, MFA, 얕은 RBAC)을 안전하게 구현하는 작업은 난이도가 높고 시간이 오래 걸린다. `ywc-auth-implement`는 정책 인터뷰 → 스택 감지 → battle-tested 라이브러리 동적 추천 → `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer` 등 기존 Claude Code 전용 named agent로의 위임이라는 오케스트레이션 흐름으로 이 문제를 표준화한다.

## Anchors

| Anchor | Decision |
|---|---|
| What | `claude-code/skills/ywc-auth-implement/`를 SKILL.md, Tier 1 README 4종, 5개 references, evals와 함께 신설한다. |
| Why | 인증 작업은 정책 결정, 검증된 라이브러리 재사용, 필수 보안/E2E 게이트를 요구하며 즉흥적 스캐폴딩으로는 이를 충족할 수 없다. |
| Out of Scope | 실제 애플리케이션 인증 코드 구현, 신규 Claude Code agent 생성, stack playbook 사전 시딩, 법적 승인, Codex 번들 변경, `VERSION`/`CHANGELOG.md` 수동 편집. |
| Done When | `bash scripts/validate.sh`가 통과하고, `## Output Format` 4-값 enum이 존재하며, Claude Code 전용 named agent(`ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer`/`ywc-security-engineer`) 디스패치가 §3.5 규약을 준수하고, evals 5개 시나리오가 존재한다. |

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/skills/CLAUDE.md:74-96` | 신규 `ywc-*` skill 작성 시 `ywc-skill-author`를 먼저 호출해야 한다 | comply — FR-1에서 위임 |
| `claude-code/skills/CLAUDE.md:5-7` + 루트 `CLAUDE.md`("Skill Authoring Rules") | `README.md`(한국어)/`README.en.md`/`README.ja.md`/`README.ko.md` Tier 1 4종이 모두 필요하며 CI가 강제한다 — 로케일 분기를 만들지 않는 정책이 아니라 정확히 이 4개가 요구되는 정책이다 (Codex의 6-locale 요구사항과 다르다) | comply — FR-9에서 4종 작성 |
| `scripts/validate.sh:9-52` (`check_skill_dir`/`check_readme_set`) | frontmatter `name:`이 디렉토리명과 일치해야 하고 README 4종 존재를 검사한다 | comply — `name: ywc-auth-implement` |
| `claude-code/skills/ywc-skill-author/SKILL.md:48` (규칙 A15) | `description`은 공백 기준 80단어 이하(80 PASS, 81 FAIL)여야 한다 — Codex의 500-Unicode-char 제한과는 다른 기준이다 | comply — FR-1 |
| `claude-code/skills/CLAUDE.md:259-280` (§3.5) | `Task(subagent_type: ...)` 직접 디스패치 fan-out skill은 `references/subagent-status-actions.md` 링크와 §3.5의 **verbatim** Return-payload contract를 각 지시문에 넣어야 한다 | comply — FR-6(backend/frontend-coder)·FR-7(doc-writer)의 모든 prompt에 링크와 전문을 삽입. `ywc-security-audit`(FR-8)는 skill 호출이라 직접 적용 대상이 아님 |
| `claude-code/skills/ywc-infra-design/SKILL.md` (전체), `ywc-tdd-ritual/SKILL.md` (Workflow) | 오케스트레이터 skill은 인터뷰/문서화를 스스로 하고 구현은 전담 executor(named agent)에 위임한다. `ywc-tdd-ritual`은 named agent를 디스패치하는 wrapper가 아니라 RED → GREEN → REFACTOR 규율이다 | extend — 인증 skill이 `Task(subagent_type: ywc-backend-coder|ywc-frontend-coder)`를 직접 호출하되, 각 prompt에 `ywc-tdd-ritual`의 필수 cycle 및 검증 증거를 수행하라고 명시한다 |
| `claude-code/skills/ywc-security-audit/SKILL.md` (Arguments) | `--code <path>`, `--format markdown\|html`; Critical/High/Medium/Low 4단계 분류; Completion Status 미반환 | comply — FR-8에서 severity→Completion Status 매핑을 이 skill이 직접 수행 |
| `claude-code/skills/ywc-e2e-test-strategy/SKILL.md` (Mode selection rule) | `--init`/`--audit`/`--flow <name>` 상호 배타; `--flow`만 반복 호출 시 `playwright.config.*` 부재 상황에서 auto-detect가 우회되어 orphan spec 생성 위험 | comply — FR-8에서 config 부재 시 `--init`, 존재 시 `--audit`을 먼저 실행하고, 누락 flow에만 `--flow`를 적용한 뒤 fresh test evidence를 요구 |
| `claude-code/agents/` (디렉토리 확인) | `ywc-architect.md`/`ywc-backend-coder.md`/`ywc-doc-writer.md`/`ywc-frontend-coder.md`/`ywc-security-engineer.md` 실존 | comply — Integration/Dependencies 인용 전부 실존 확인 (Codex는 이 named agent catalog가 없다) |
| `find docs/ywc-plans -iname "*auth*"` 결과 | `codex_auth_implement_skill.md`가 이미 존재하며 동일한 원본 spec의 Codex 대응판으로, 파일명이 `<runtime>_auth_implement_skill.md` 스네이크케이스 패턴을 사용한다 | comply — 이 문서를 `claude_auth_implement_skill.md`로 명명해 동일 패턴을 따른다 |
| `find claude-code/skills -iname evals.json` (예: `ywc-commit`) | `claude-code` evals는 자연어 `prompt`/`expected_output` 형태이며 CI 자동 발견 대상이 아니다(Codex의 `run-codex-skill-contract-evals.sh`에 대응하는 러너가 claude-code 쪽엔 없다) | comply — FR-2에서 문서화 등급 패턴으로 작성, `"harness"` 필드 요구하지 않음 |

## Scope

- `claude-code/skills/ywc-auth-implement/`를 `SKILL.md` + `references/`(5개: `policy-interview.md`, `security-checklist.md`, `generic-fallback.md`, `legal-pages-template.md`, `rationalization-evidence.md`) + Tier 1 README 4종 + `evals/evals.json`으로 생성
- `claude-code/skills/README.md`(및 로케일 대응 파일이 있다면 함께)에 skill 등록
- Preflight Gate 5항목(멱등성 포함), 정책 인터뷰 9카테고리, 동적 라이브러리 추천, `ywc-tdd-ritual` 규율을 prompt에 적용한 direct implementation dispatch(`ywc-backend-coder`/`ywc-frontend-coder`), `ywc-doc-writer` 법적 페이지, `ywc-security-audit` severity 게이트, `ywc-e2e-test-strategy` 정책 조건부 검증과 fresh E2E evidence, `ywc-create-pr` 비차단 제안, `## Output Format` 4-값 enum 문서화

## Out of Scope

- 실제 프로젝트에 적용해 인증 기능을 구현하는 것 자체 (skill 완성 이후의 사용 단계)
- 전체 RBAC 정책 매트릭스 엔진 — v1은 `role` 컬럼 + 기본 role + 세션/JWT 클레임까지의 얕은 RBAC로 한정
- Stack-specific playbook(`references/stack-*.md`) 사전 시딩 — v1은 0개로 시작, 자기확장으로 축적
- `codex/skills/ywc-auth-implement/` 변경 — `codex_auth_implement_skill.md`가 독립적으로 다루며 두 root는 자동 동기화되지 않는다(`claude-code/skills/CLAUDE.md:402-409`)
- `ywc-skill-author`/`ywc-security-audit`/`ywc-tdd-ritual`/`ywc-doc-writer`/`ywc-e2e-test-strategy` 자체의 수정
- CI 자동 발견 output-contract eval harness 신규 구축 (Existing Constraints Touched 참조)
- `VERSION`/`CHANGELOG.md` 수동 편집 — Release Please가 소유

## Acceptance Criteria

- [ ] **AC1 — 패키지 계약**: `claude-code/skills/ywc-auth-implement/`에 SKILL.md, `references/` 5개 파일, README 4종, `evals/evals.json`이 존재하고 frontmatter `name: ywc-auth-implement`, `description`, `category`, `phase`, `requires`, `advisor_budget`을 갖는다. 관찰: `bash scripts/validate.sh` 통과.
- [ ] **AC2 — 활성화/description**: `description`이 80단어 이하(A15)이고 다국어 trigger/anti-trigger를 포함한다. 관찰: 단어 수 카운트 ≤80.
- [ ] **AC3 — Preflight 멱등성**: 브랜치 재사용, `.env.example` non-destructive 추가, 스택 미감지 시 `ywc-tech-research` 라우팅, 기존 인증 `new|extend|migrate` 필수 선택, 법적 초안 경고 5항목이 각각 독립 단계로 존재한다. 관찰: 5개 라벨 grep 매칭.
- [ ] **AC4 — 정책 인터뷰**: `references/policy-interview.md`에 9개 `##` 섹션(수단·MFA·세션·비밀번호·프로필·탈퇴·얕은RBAC·약관동의·남용방지)이 존재하고 각 섹션이 질문/응답-기본값/승인-유예 상태를 기록한다. 관찰: `grep -c "^## "` ≥ 9.
- [ ] **AC5 — 동적 추천**: 스택 근거와 승인된 정책만으로 추천이 이뤄지며, stack playbook이나 고정 지원 스택 목록이 도입되지 않고, 근거 불충분 시 `ywc-tech-research`로 라우팅한다. 관찰: 그렙 결과 0건(허용목록 서술) + 라우팅 문구 존재.
- [ ] **AC6 — Claude Code 오케스트레이션**: 경로가 `ywc-plan` → `ywc-spec-ready` → `Task(subagent_type: ywc-backend-coder\|ywc-frontend-coder)` (각 prompt에서 `ywc-tdd-ritual` cycle 준수) → `ywc-security-audit --code ...` → `ywc-e2e-test-strategy` → fresh E2E verification → 선택적 `ywc-create-pr`를 사용하며 Codex 전용 명령(`$ywc-code-gen` 등)을 쓰지 않는다. 관찰: Workflow 섹션 grep 매칭.
- [ ] **AC7 — 안전성/캐싱**: 직접 JWT/비밀번호/시크릿 crypto를 추천하지 않고, 법적 초안은 "법적 검토 전 임시본"을 명시하며, Critical/High 발견 시 E2E·PR·캐싱을 모두 skip한다. 관찰: grep 매칭 3건.
- [ ] **AC8 — Output 계약**: `## Output Format` 섹션이 리터럴로 존재하고 `DONE`/`DONE_WITH_CONCERNS`/`BLOCKED`/`NEEDS_CONTEXT` 4개 값을 모두 포함한다. 관찰: grep 매칭.
- [ ] **AC9 — Evals**: happy path·기존 인증 hard stop·알 수 없는 스택 라우팅·직접 crypto 거부·보안 실패 시 no-cache 5개 시나리오가 `claude-code/skills/ywc-auth-implement/evals/evals.json`에 존재한다(`"harness"` 필드 불요). 관찰: JSON 파싱 후 5개 시나리오 이름 매칭.
- [ ] **AC10 — 배포/검증**: `bash scripts/validate.sh` 전체가 통과하고, backend-coder/frontend-coder/doc-writer 3개 디스패치 지시문 각각에 §3.5 링크와 **verbatim** Return-payload contract가 존재하며(FR-8 security-audit는 grep 대상에서 제외), README 4종이 정확히 존재한다. 관찰: 아래 verification 명령 exit 0.

## Functional Requirements

### FR-1: Scaffold, frontmatter, progressive disclosure

`ywc-skill-author`로 표준 아티팩트 세트를 생성한다. `name`/`description`/`category: spec`/`phase: planning`/`requires: []`/`advisor_budget: 2`(Step 3.5 아키텍처 어드바이저 1회 + FR-8 severity 해석 보조 여유분) frontmatter를 `ywc-infra-design`과 동일한 형식으로 사용한다. `description`은 `(ywc) Use when...`으로 시작해 `Do not use for ...`로 끝나며 80단어 이하(A15)를 유지한다. SKILL.md는 500줄 이하를 유지하고, 재사용 가능한 체크리스트·인터뷰 필드·상세 전환 로직·근거는 5개 `references/`로 직접 링크한다. 의무 추출 대상은 (1) 9-category 정책 인터뷰 절차 요약, (2) E2E 정책 분기와 실행 체크리스트, (3) 동적 라이브러리 추천 로직이다. 서브에이전트 디스패치 prompt는 §3.5 규약을 눈에 보이게 유지해야 하므로 본문에 인라인으로 둔다. Preflight Gate·FR-8 severity 라우팅 표·Output Format 계약·Rationalization Defense 표도 본문에 인라인 유지한다.

### FR-2: Rationalization Defense

최소 5개의 근거-연결 Excuse/Reality 행을 작성한다. "OAuth만 필요하니 인터뷰 스킵", "직접 crypto/JWT 구현이 빠를 것 같다", "MFA는 나중에", "보안/E2E 통과 전 캐싱", "법적 초안을 최종본처럼 제시" 등을 거부하는 행을 포함한다. `references/rationalization-evidence.md`는 각 행동별 baseline 실패 근거와 forward-test 근거를 기록한다(애플리케이션 코드 실행 없이).

### FR-3: Idempotent preflight

프로젝트 가이드(`CLAUDE.md`/`AGENTS.md`), 매니페스트, 프레임워크/DB 근거, 브랜치, `.env.example`, `.gitignore`를 질문 전에 점검한다.

1. `feature/<auth-slug>` 브랜치가 이미 존재하면 재사용하고, 장기 브랜치에서만 새로 생성한다.
2. 누락된 시크릿 placeholder만 추가하며, 값을 덮어쓰거나 노출하지 않는다.
3. 스택 근거 불충분 시 `ywc-tech-research`로 라우팅하고 결정 후 재개한다.
4. 기존 인증 발견 시 사용자가 `new`/`extend`/`migrate`를 선택할 때까지 `NEEDS_CONTEXT`를 반환하며, 선택 전에는 스캐폴딩이나 디스패치를 하지 않는다.
5. 생성된 ToS/개인정보처리방침 초안은 항상 "법적 검토 전 임시본"으로 표시한다.

### FR-4: Policy interview (9 categories)

9개 카테고리를 한 번의 집중 라운드로 질문한다: 이메일/비밀번호 + OAuth 프로바이더 등록/redirect 준비 상태; MFA 등록/복구; 세션 저장·TTL·회전·철회·기기 관리; 재설정 및 해싱 라이브러리 경계; 프로필 필드; 탈퇴 재인증 및 보관 정책; 얕은-RBAC 역할/기본값/클레임; 동의 버전/수집/철회; 남용 방지 rate-limit·검증·복구 제어. `references/policy-interview.md`로 추출한다. 애플리케이션 대상 질문/산출물의 언어는 `claude-code/skills/references/language-resolution.md`의 canonical 체인(대상 프로젝트 `CLAUDE.md`/`AGENTS.md` Language Policy 우선)을 따르며 하드코딩된 언어 가정을 두지 않는다.

### FR-5: Dynamic recommendation and cache

스택 근거와 승인된(또는 명시적으로 위험 고지 후 유예된) 정책 기록만으로 battle-tested 라이브러리/관리형 서비스를 추천한다. v1은 stack playbook 0개로 시작한다. 근거가 부족하면 `references/generic-fallback.md` + 기존 Research & Reuse 절차(GitHub 검색/Context7/패키지 레지스트리)로 실시간 리서치하고 `ywc-tech-research`로 라우팅한다. 신규 playbook은 FR-8 보안 검토에서 Critical/High 0건이고 FR-8의 정책 조건부 E2E까지 통과한 뒤에만 caching-eligible이다. "지원 스택 목록" 개념 자체를 SKILL.md/references 어디에도 명시하지 않는다.

### FR-6: TDD 기반 구현 디스패치

`ywc-plan`으로 승인된 정책/추천을 전달해 계획/spec을 생성하고, Medium/Large는 `ywc-spec-ready`로 수렴시킨다. 이 skill이 `Task(subagent_type: ywc-backend-coder)` / `Task(subagent_type: ywc-frontend-coder)`를 직접 디스패치한다. `ywc-tdd-ritual`은 dispatcher가 아니므로 "그 아래"에 호출하는 것으로 표현하지 않는다. 대신 각 implementation prompt에 `ywc-tdd-ritual`의 RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Verify GREEN cycle, behavior별 verification evidence, 그리고 완료 주장 전 `ywc-verify-done`을 수행하라는 지시를 포함한다. 각 direct-dispatch prompt는 `references/subagent-status-actions.md` 링크와 그 §3.5 **Return-payload contract 전문을 verbatim**으로 포함한다.

### FR-7: 법적 페이지 작성 디스패치

`Task(subagent_type: ywc-doc-writer)`로 ToS/개인정보처리방침 초안과 가입 화면 동의 체크박스 UI 요구사항을 작성한다. FR-6과 동일하게 §3.5 링크와 **verbatim** Return-payload contract를 prompt에 포함한다. FR-3 항목 5의 "법적 검토 전 임시본" 고지를 산출물에 항상 포함하도록 지시문에 명시한다.

### FR-8: Security, E2E, PR gates

구현 후 `ywc-security-audit --code <auth-diff-path>`를 호출한다. `ywc-security-audit`는 skill 호출이므로 §3.5 직접 적용 대상이 아니며, 이 skill이 severity 결과를 아래 표에 따라 자신의 Completion Status로 직접 변환한다.

| Audit result | Route | Cache |
|---|---|---|
| Critical/High 0건 | 정책 조건부 E2E로 진행 | Pending — E2E 통과 후에만 Eligible |
| Critical/High 1건 이상 | `DONE_WITH_CONCERNS`; E2E·PR·캐싱 모두 skip; remediation/replan 후 재감사 | Not eligible |
| 감사 명령 실행 불가 | `BLOCKED`, 명령/오류 근거 포함 | Not eligible |
| 범위/신뢰 경계 불충분 | `NEEDS_CONTEXT`, 누락 항목 명시 | Not eligible |

E2E는 FR-4에서 승인된 항목만 커버한다(이메일/비밀번호 선택 시에만 가입/로그인/재설정, 탈퇴 활성화 시에만 탈퇴, 설정 완료된 각 OAuth 프로바이더마다 별도 flow). 먼저 `playwright.config.*`를 확인한다. 없으면 `ywc-e2e-test-strategy --init`을 1회 실행하고 생성된 flow를 확인한 뒤, 빠진 승인 flow에만 `--flow <name>`을 실행한다. 있으면 `--audit`으로 현재 coverage를 확인한 뒤, 빠진 승인 flow에만 `--flow <name>`을 실행한다. 어느 경우든 flow 생성은 통과가 아니다. 프로젝트의 실제 E2E command를 fresh 실행하고 `ywc-verify-done` 형식의 command·exit code·핵심 출력 증거를 남겨야 한다. Provider credential/테스트 환경 부재는 비-보안·명시적 유예인 경우만 `DONE_WITH_CONCERNS`, 그 외 `BLOCKED`. 게이트 통과 후에만 `ywc-create-pr`을 비차단으로 제안한다.

### FR-9: Output contract, README, catalogs

`## Output Format` 섹션에 이 저장소의 canonical Completion Status 관례(`claude-code/skills/references/subagent-status-actions.md`의 Status Responses 표, 및 `ywc-plan`/`ywc-spec-validate` 등 다수 `ywc-*` skill이 채택한 `## Output Format` 패턴)와 동일한 구조로 Completion Status enum(`DONE`/`DONE_WITH_CONCERNS`/`BLOCKED`/`NEEDS_CONTEXT`)을 정의한다. `ywc-infra-design`의 `## Output Format`은 자체 `infra-design.md` 산출물 템플릿만 담고 있어 이 enum을 포함하지 않으므로, frontmatter 필드 형식(FR-1)의 선례로만 인용하고 이 enum 자체의 선례로는 인용하지 않는다. 출력은 최소한 Preflight 결과, 9개 정책 인터뷰 요약, 추천 라이브러리/근거, 디스패치된 서브에이전트 목록(FR-6/FR-7/FR-8), Completion Status를 포함한다. Tier 1 README 4종(`README.md` 한국어, `README.en.md`, `README.ja.md`, `README.ko.md`)을 작성하고 기술 용어는 영어로 유지한다. `claude-code/skills/README.md`(존재 시)에 skill을 등록한다. `evals/evals.json`에 happy path·기존 인증 hard stop·알 수 없는 스택 라우팅·직접 crypto 거부·보안 실패 시 no-cache 5개 시나리오를 `ywc-commit/evals/evals.json`과 같은 자연어 `prompt`/`expected_output` 패턴으로 작성한다(`"harness"` 필드 불요). `VERSION`/`CHANGELOG.md`는 수동 편집하지 않는다.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Security | 손수 구현한 비밀번호 해싱/토큰 서명/시크릿 crypto를 추천하지 않으며, battle-tested 라이브러리/관리형 서비스를 우선한다. |
| Maintainability | SKILL.md는 약 500줄 이하, 30줄 초과 섹션은 FR-1의 의무 추출 목록에 따라 `references/`로 추출한다. |
| Portability | 스택 근거는 동적으로 감지하며, 고정 프레임워크 허용목록을 두지 않는다. |
| Idempotency | 브랜치/env 조치는 재실행 안전하고 비파괴적이다(FR-3). |
| Runtime fit | 설치된 Claude Code skill과 `claude-code/agents/`의 named agent에만 의존한다(Codex 전용 명령 사용 금지). Agent catalog가 없으면 대체 구현하지 않고 `BLOCKED`로 종료한다. |
| i18n | 번들 유지보수는 한국어 우선, 대상 프로젝트 산출물은 그 프로젝트의 언어 컨벤션(`language-resolution.md` 체인)을 따른다. |

## Data Model

N/A — skill/documentation 아티팩트만 변경된다. 하위 프로젝트에 `role` 컬럼 등을 제안할 수 있으나 그것은 하위 프로젝트의 스키마이지 이 spec의 데이터 모델이 아니다.

## API Contract

N/A — 네트워크 API 변경 없음. 구조화된 Output Format과 Completion Status가 이 skill의 문서화된 인터페이스다.

## Edge Cases

- **Agent catalog 미설치** (`claude-code/agents/` 부재): 인라인으로 대신 작성하지 않고 `BLOCKED`를 반환하며 필요한 설치 artifact를 명시한다.
- **알 수 없는 스택 + generic-fallback으로도 불충분**: `ywc-tech-research`로 에스컬레이션한다(추측 금지).
- **인터뷰 후보 외 OAuth 프로바이더 요청**: `AskUserQuestion` 자유 응답("기타")으로 자연 수용, 별도 분기 불필요.
- **description 80단어 초과 위험**: 핵심 trigger/anti-trigger만 남기고 상세는 본문으로 이관한다.
- **기존 인증 하드 스톱 후 재개**: 이미 수집한 스택 감지 결과를 재사용, 처음부터 다시 묻지 않는다.
- **Provider credential/테스트 환경 부재로 일부 E2E 불가**: FR-8 기준으로 분류하며 E2E 통과를 임의로 주장하지 않는다.
- **기존 브랜치/placeholder 존재**: 재생성/덮어쓰기 대신 재사용/스킵한다.

## Dependencies

- `ywc-skill-author` (FR-1)
- `ywc-tech-research` (FR-3, FR-5)
- `ywc-tdd-ritual`, `ywc-backend-coder`/`ywc-frontend-coder` agents (FR-6)
- `ywc-doc-writer` agent (FR-7)
- `ywc-security-audit` skill → `ywc-security-engineer` agent (FR-8)
- `ywc-e2e-test-strategy`, `ywc-verify-done` (FR-8)
- `ywc-create-pr` (FR-8, 비차단)
- `claude-code/skills/references/subagent-status-actions.md` (FR-6, FR-7)
- `claude-code/skills/references/language-resolution.md` (FR-4)
- `scripts/validate.sh`

## Implementation Plan

1. `ywc-skill-author` 컨벤션으로 shell, frontmatter, README 4종, 초기 `evals/evals.json`을 생성한다.
2. 본문(Rationalization Defense, Preflight, 인터뷰/추천 요약, implementation/legal direct-dispatch prompts의 §3.5 전문, 보안/E2E/verification 게이트, `## Output Format`)을 500줄 이내로 압축 작성한다.
3. `policy-interview.md`/`security-checklist.md`/`generic-fallback.md`/`legal-pages-template.md`/`rationalization-evidence.md` 5개 references를 작성한다(stack playbook은 추가하지 않는다).
4. 5개 routing eval을 추가하고, direct-dispatch prompt의 §3.5 전문과 Codex 전용 명령 부재를 확인한다.
5. `claude-code/skills/README.md`(존재 시) 카탈로그를 갱신하고 저장소 전체 검증을 실행한다.

## Verification

```bash
set -euo pipefail

python3 -m json.tool claude-code/skills/ywc-auth-implement/evals/evals.json >/dev/null

for file in policy-interview.md security-checklist.md generic-fallback.md \
  legal-pages-template.md rationalization-evidence.md; do
  test -f "claude-code/skills/ywc-auth-implement/references/$file"
done

for file in README.md README.en.md README.ja.md README.ko.md; do
  test -f "claude-code/skills/ywc-auth-implement/$file"
done

if rg -n '\$ywc-code-gen|\$ywc-' claude-code/skills/ywc-auth-implement; then
  exit 1
fi

for agent in ywc-backend-coder ywc-frontend-coder ywc-doc-writer; do
  rg -U -q "(?s)Task\\(subagent_type: ${agent}\\).*Return-payload contract" \
    claude-code/skills/ywc-auth-implement/SKILL.md
done

rg -q 'ywc-verify-done' claude-code/skills/ywc-auth-implement/SKILL.md

bash scripts/validate.sh
git diff --check
```

## Self-Consistency Pass

- **Pass A — AC ↔ FR**: AC1/2→FR-1; AC3→FR-3; AC4→FR-4; AC5→FR-5; AC6→FR-6/8; AC7→FR-5/8; AC8→FR-9; AC9→FR-2/9; AC10→FR-1/6/7. Orphan 없음.
- **Pass B — claim ↔ reality**: `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer`/`ywc-security-engineer` agent, `ywc-security-audit`/`ywc-e2e-test-strategy`의 실제 Arguments, `scripts/validate.sh`의 실제 README 4종 요구사항과 `ywc-skill-author` A15(80단어)를 이번 세션에서 직접 읽어 검증했다. 발명된 도구 동작 없음.
- **Pass C — schema invariants**: N/A — 스키마/마이그레이션/relation/HTTP contract 변경 없음.

## Confidence Gate

`ywc-confidence-gate`: **91/100 — PROCEED**.

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 93 | Source/target root, 제외 항목, 완료 근거가 명시적이다. |
| Architecture compliance | 91 | `ywc-infra-design`의 오케스트레이터/executor 분리 패턴, `claude-code/skills/CLAUDE.md`의 §3.5·README 4종·80단어 규칙을 준수한다. |
| Evidence quality | 92 | `validate.sh`, `ywc-skill-author/SKILL.md:48`, `ywc-security-audit`/`ywc-e2e-test-strategy` 실제 Arguments, `claude-code/agents/` 실존 목록을 이번 세션에서 직접 읽어 확인했다. |
| Reuse verified | 90 | 기존 skill/agent만으로 모든 lane을 커버하며 실존을 확인했다. |
| Root cause identified | 89 | 정책 파편화·직접 구현 시 보안 리스크라는 근본 원인을 정책 인터뷰 + 라이브러리 우선 추천으로 해소하며, 원본 spec의 근본 원인 분석을 상속한다. |

## Open Questions

N/A — none identified (README 정책 차이는 FR-9/AC10, description 길이 차이는 FR-1/AC2, evals harness 부재는 Existing Constraints Touched/AC9, stack playbook 시딩 범위는 FR-5에서 0개로 확정, RBAC 범위는 원본 사용자 확정을 상속).

## References

- [Source Claude Code auth plan](</Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm/docs/ywc-plans/260715-002-claude-code-auth-implement-skill.md>)
- [Codex sibling plan](./codex_auth_implement_skill.md)

## Handoff

✅ Spec drafted: `docs/ywc-plans/claude_auth_implement_skill.md`

Next: run `ywc-spec-ready --spec docs/ywc-plans/claude_auth_implement_skill.md`. After it reaches DONE, run `ywc-task-generator` before implementation.
