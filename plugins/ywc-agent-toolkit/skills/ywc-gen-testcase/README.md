# Gen Testcase Skill (ywc-gen-testcase)

GitHub PR, 구현 완료된 Task directory, Task directory range, Git range, 또는 현재 git diff 를 입력으로 받아 **개발자용 Section A (pre-merge gate) 와 QA/Browser용 Section B (pre-release gate) 로 분리된 Checkbox 기반 Testsheet** 를 생성하는 Codex Skill 입니다. Default 출력은 Markdown 이며, `--format html` 로 browser sign-off 용 interactive HTML 을 생성할 수 있습니다. Default 출력 경로는 project 의 `docs/test-case/` folder 입니다.

`ywc-sequential-executor` 나 `ywc-merge-dependabot` 로 Ship 된 변경을 Backend 엔지니어와 QA/PM/Product Owner 가 각자 자신의 Section 에서 독립적으로 Sign-off 할 수 있도록 설계되어 있어, Merge gate 와 Release gate 를 명확히 분리합니다.

## Usage

### 기본 사용

PR URL 로 Testsheet 를 생성합니다:

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

같은 Repository 내라면 PR 번호만으로도 지정 가능합니다:

```text
/ywc-gen-testcase 250
```

### Task 기반 생성

```text
/ywc-gen-testcase 000001-010-db-create-users-table
```

### Task Range 기반 생성

`000012-010..000019-010`처럼 두 endpoint 가 task prefix 형태이면, Skill 은 Git Range 보다 먼저 inclusive Task Range 로 해석합니다. `<tasks-dir>` 의 task directory basename 을 사전 순(번호 prefix → 실행 순서)으로 정렬하고, 시작 task 부터 끝 task 까지의 task.md / README.md 를 모두 읽어 Scenario 의 source 로 사용합니다.

```text
/ywc-gen-testcase 000012-010..000019-010 --lang ja
```

> Endpoint 가 누락되거나 모호하면 stop 하고 사용자에게 묻습니다. `git rev-parse` 로 fallback 하지 않습니다.
> 시작 task 가 끝 task 보다 뒤에 있으면 의도가 역방향인지 stop 하고 확인합니다.
> Branch / tag / SHA 가 우연히 task prefix 처럼 보일 때는 `--range A..B` 로 명시적 Git range 를 강제할 수 있습니다.

### Git Range 기반 생성

Commit 범위를 직접 지정합니다. SHA, Tag, Branch, `HEAD~N` 모두 accept 됩니다.

```text
/ywc-gen-testcase v1.2..v1.3
/ywc-gen-testcase HEAD~5..HEAD
/ywc-gen-testcase main..feature-x
/ywc-gen-testcase --range abc1234..def5678
```

> Range 는 **two-dot `A..B` 형식만 지원**합니다. Three-dot `A...B` 는 merge-base semantics 로 scope 이 silently 바뀌기 때문에 거부됩니다.
> Range HEAD 가 open/merged PR 에 속해 있으면 (80% 이상 commit 겹침) Skill 이 자동으로 PR mode 사용을 제안합니다 — PR body / label / Acceptance Criteria 가 포함되어 Scenario 품질이 높아지기 때문입니다.
> Commit message 품질이 낮으면 (headline 70% 이상이 10 자 이하) 경고 후 진행 여부를 확인합니다.

### 현재 Diff 기반 생성

```text
/ywc-gen-testcase --from-diff
```

### Option

| Option | 설명 | 예시 |
| --- | --- | --- |
| `--output-dir <path>` | 출력 Directory (default: `docs/test-case/`) | `--output-dir ./qa/manual-tests` |
| `--lang <code>` | Testsheet 언어 (`ja`, `ko`, `en`). default: auto-detect | `--lang ja` |
| `--filename <name>` | Filename override (`.md` 제외) | `--filename release-v2-smoke` |
| `--tasks-dir <path>` | Tasks directory 경로 (Task / Task Range 입력에 사용; default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--format <fmt>` | 출력 형식 (`markdown` \| `html`). default: `markdown` | `--format html` |
| `--include-regression` | Regression Section (B.3) 추가 | |
| `--audience <who>` | `dev` \| `qa` \| `both`. default: `both` (A+B 통합) | `--audience qa` |
| `--split` | 물리적으로 `<slug>-dev.md` + `<slug>-qa.md` 2 파일로 분할 | |
| `--force-single` | L tier 에서도 split 제안 없이 단일 파일 강제 | |
| `--no-toc` | M/L tier 의 TOC 자동 삽입 생략 | |
| `--from-diff` | 현재 `git diff HEAD` 기반 생성 | |
| `--range <spec>` | Git range 명시적 지정 (`A..B` 형식). Positional 과 동일 | `--range v1.2..v1.3` |
| `--dry-run` | 생성 계획만 표시 (파일 작성 안 함) | |

> PR identifier, Task specifier, Task Range (positional `<task>..<task>`), Git Range (positional `A..B` 또는 `--range`), `--from-diff` 는 상호 배타적입니다. `--split` 와 `--force-single` 도 상호 배타적입니다. 동시에 지정하면 Skill 이 중단되고 어떤 mode 인지 되묻습니다.

## 두 개의 Audience, 두 개의 Gate

Testsheet 의 핵심 설계는 "누가 언제 어떤 도구로 테스트하는가" 에 따른 **Section 분리**입니다.

| Section | 대상 | 사용 도구 | Gate |
| --- | --- | --- | --- |
| **A. Developer Verification** | Backend / DB / DevOps 엔지니어 | psql, gh CLI, curl, docker | **Pre-merge** — Contract, Migration, Worker, Container |
| **B. QA / Browser Verification** | QA, PM, Product Owner, Designer | Chrome + DevTools, 관리 UI, test origin | **Pre-release** — End-user 체감 및 Browser observable effect |

Dev 와 QA 가 동시에 진행 가능하며, 각자 자기 Section 만 확인하면 됩니다.

## Tier 자동 결정

Scenario 수에 따라 Layout 이 자동 결정됩니다.

| Tier | Scenario 수 | Layout |
| --- | --- | --- |
| **S** | ≤ 20 | 단일 파일, A/B Section, TOC / 접이식 없음 |
| **M** | 21–40 | 단일 파일, A/B Section, 상단 자동 TOC + Prerequisites/Edge Cases 접이식 (`<details>`) |
| **L** | > 40 | User 에게 단일 파일 / `--split` / Phase 분할 중 선택 요청 후 진행 |

이 자동화 덕분에 대부분의 PR 에서 별도 고민 없이 읽기 좋은 Testsheet 가 생성되며, 초대형 PR 에서는 과도하게 긴 파일을 만들지 않도록 안전장치가 동작합니다.

## Execution Cycle

```text
Step 1: Input Resolution
  └─ PR: gh pr view / gh pr diff 로 metadata 와 diff 확보
  └─ Task: <tasks-dir>/<name>/ (완료 시 completed/ 우선) 의 task.md / README.md 로드
  └─ Diff: git diff HEAD + 최근 commit log 확보

Step 2: Audience and Surface Classification
  └─ Audience: A (Developer) / B (QA/Browser) 태그
  └─ Surface: UI / Database / API / Background job / Configuration / Docs
  └─ Browser-observable effect 가 있으면 Backend-only PR 에도 B Section 포함

Step 3: Scenario Generation
  └─ 각 (audience, surface) 조합별 2–5 개 Scenario
  └─ Scenario 당 Goal / Preconditions / Steps / Expected / Checkbox
  └─ Source 우선순위: PR body 또는 Task Acceptance Criteria > Commit message > Surface > Diff edge case

Step 4: Tier Decision
  └─ Scenario 수 집계 → S / M / L 판정
  └─ L tier 는 user 에게 진행 방식 확인 후 진행

Step 5: Write the Testsheet
  └─ Single file (default) 또는 Split (--split / --audience)
  └─ M/L 은 TOC + 접이식 Prerequisites/Edge Cases
  └─ 동일 경로에 파일 존재 시 `-v<N>` suffix (overwrite 금지)

Step 6: Validate & Report
  └─ 파일 존재, Checkbox 수, Expected 존재, TOC anchor 확인
  └─ Tier / Audience / Surface 요약 보고
```

## Default Filename Rule

| Input | Single file (default) | `--split` |
| --- | --- | --- |
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| Task | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Task Range | `tasks-<start-prefix>-<end-prefix>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Range | `range-<short-start>-<short-end>-<slug>.md` (Tag 양끝이면 `range-v1.2-v1.3-<slug>.md`) | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

## Testsheet 구조 (Single-file default)

```text
1. Summary
2. Prerequisites
   2.0 Common (공통)
   2.A Dev-only
   2.B QA-only
A. Developer Verification  [Pre-merge gate]
   A.1 Database / Table
   A.2 API
   A.3 Background Jobs / Workers
   A.4 Configuration
   A.5 Dev Edge Cases
   A.6 Dev Sign-off
B. QA / Browser Verification  [Pre-release gate]
   B.1 UI / Browser Scenarios
   B.2 User-visible Edge Cases
   B.3 Regression (--include-regression 지정 시)
   B.4 QA Sign-off
Appendix (optional)
```

YAML Front Matter 는 `dev_tester` / `dev_status` / `qa_tester` / `qa_status` 가 분리되어 각 Gate 를 독립 추적할 수 있습니다.

각 Scenario 는 반드시 **구체적인 Expected 결과** 를 포함합니다. "동작하는지 확인" 같은 막연한 표현은 금지입니다.

## Length Management Guidelines

Testsheet 가 과도하게 길어지는 것을 막기 위한 Skill 내장 원칙:

1. **Prerequisites 는 Common + Audience-별 suffix 로 분리** — 중복 금지
2. **20 줄 초과 verification query / script 는 `scripts/qa/*.sql` 등으로 추출** 후 경로 참조만 기재
3. **Regression 은 기존 Testsheet 링크로 축약** (중복 작성 금지)
4. **긴 Troubleshooting / Payload 예시는 `## Appendix` 로 이동** 후 본문에서 링크

위 원칙을 자동으로 적용하므로 대부분의 M tier Testsheet 가 ~800 lines 이내로 수렴합니다.

## Language Detection

`--lang` 미지정 시 다음 순서:

1. **CLAUDE.md / AGENTS.md** 의 언어 directive (`PR言語: 日本語`, `Documentation: Korean` 등)
2. **Recent testsheets** 의 주요 언어
3. **Project README.md** 의 언어
4. **Fallback** — English

YAML Front Matter, Section 번호, Template 골격은 `--lang` 과 무관하게 영어 고정 (Tooling reference point).

## Error Handling

| 상황 | 동작 |
| --- | --- |
| Input 미지정 | 중단 후 PR/Task/`--from-diff` 요청 |
| 복수 input 지정 | 중단 후 어떤 mode 인지 확인 |
| `--split` + `--force-single` 동시 지정 | 중단 후 어느 쪽 의도인지 확인 |
| `gh` 미인증 (PR input) | `gh auth login` 안내 후 중단 |
| PR 미발견 | PR 번호 보고 후 중단 |
| Task 미발견 | 유사 이름 Task 목록 (fuzzy match) 표시 후 중단 |
| Diff 비어 있음 | "nothing to test" 보고 후 중단 |
| Output directory 쓰기 불가 | 실패 경로 보고 후 중단 (silent fallback 금지) |
| 동일 경로 파일 존재 | `-v<N>` suffix 자동 부여 |
| L tier 감지 + `--split`/`--force-single` 미지정 | 중단 후 user 에게 진행 방식 확인 |

## Integration

- **ywc-sequential-executor** — Testsheet 대상 PR/Task 생성 (upstream)
- **ywc-parallel-executor** — 병렬 실행 PR 생성 (upstream)
- **ywc-merge-dependabot** — Release 전 Smoke Testsheet 용 dependency PR 생성 (upstream)

## Example Prompt

### PR URL 로 생성 (Default: 단일 파일 A+B)

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

### 물리적 Split (dev / qa 2 파일)

```text
/ywc-gen-testcase 250 --split --lang ja
```

### QA-only Testsheet (QA 팀 전달용)

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### 초대형 PR 이지만 단일 파일 고정

```text
/ywc-gen-testcase 250 --force-single
```

### Task 기반 + Regression 포함

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Task Range (시작 task 부터 끝 task 까지 inclusive)

```text
/ywc-gen-testcase 000012-010..000019-010 --lang ja
```

### Git Range (Tag 사이)

```text
/ywc-gen-testcase v1.2..v1.3 --lang ja
```

### Pre-PR local range

```text
/ywc-gen-testcase HEAD~5..HEAD
```

### Dry-run

```text
/ywc-gen-testcase 250 --dry-run
```

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
