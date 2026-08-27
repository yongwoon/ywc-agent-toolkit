# Spec: Task ID에 collaborator initials namespace 도입 (Claude Code 전용)

> **Operative Sections** — `ywc-task-generator`가 권위 있는 것으로 취급할 절:
> 본문 전 절 + `## Iteration 1 Amendments` + `## Iteration 2 Amendments`. 단 `## Out of Scope`의
> `flock` 항목과 `## Open Questions` Q1·Q2·Q3는 대체되었다 — 아래 SUPERSEDED 표시 참조.
> Open Questions에 유효하게 남은 항목은 **없다**.

- 작성일: 2026-08-26
- Scale: **Medium** (5개 skill × id 규약 변경, 4개 실행 스크립트 정규식, 문서/로케일 동기화)
- 원출처: [yongwoon/develop-with-llm PR #217](https://github.com/yongwoon/develop-with-llm/pull/217) — `feat(ywc-task-generator): PHASE 번호를 collaborator initials로 namespace` (merged 2026-08-14)
- Confidence Gate: **PROCEED (91)** — Scope 90 / Architecture 85 / Evidence 95 / Reuse 90 / Root cause 95

## Purpose

`ywc-task-generator`의 채번은 "로컬 스냅샷에서 가장 높은 PHASE + 1"이다. 이 방식은 **동시 실행을 탐지할 수 없다**. 두 명의 collaborator(또는 동일인의 두 worktree)가 각자 스캔하면 같은 PHASE를 독립적으로 계산하고, slug가 다르면 디렉터리 충돌도 `dependency-graph.md` merge conflict도 발생하지 않는다. 즉 **충돌이 조용히 성립하고**, 이후 `tasks/completed/`를 참조할 때 번호가 영구적으로 모호해진다.

PR #217은 이를 "번호를 사람별로 namespace한다"로 해결한다. 서로 다른 initials는 카운터를 공유하지 않으므로 충돌이 **구조적으로** 불가능해진다. 본 spec은 그 설계를 이 리포지토리의 `claude-code/` 트리에 이식한다.

## Scope

1. Task ID 문법 확장: `[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]` → `[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`
2. Collaborator initials 해석 규칙을 공유 reference로 신설하고, 프로젝트 `CLAUDE.md`의 canonical section에 1회 캐싱
3. `ywc-task-generator` Step 2의 채번 스캔을 (a) 해석된 initials로 한정하고 (b) `git worktree list`가 반환하는 모든 linked worktree의 `tasks/` 및 `tasks/completed/`를 union에 포함
4. ID를 파싱·검증하는 4개 스크립트의 정규식에 **선택적** initials prefix 추가 (legacy 무접두 id 계속 인식)
5. 규약을 문서화하는 SKILL.md / reference / template / evals / README 로케일 동기화

## Out of Scope

> ⚠️ SUPERSEDED by Iteration 1 — `flock` 항목은 §A2(git-ref 원자적 예약)로 대체됨.

- **`codex/` 트리 및 `plugins/ywc-agent-toolkit/`** — 사용자가 Claude Code 한정으로 지정. `plugins/`는 `codex/skills`에서만 생성됨을 확인(`.githooks/pre-commit:12`, `diff -q codex/skills/ywc-task-generator/SKILL.md plugins/.../SKILL.md` 동일)했으므로 본 변경으로 sync 대상이 되지 않는다.
- **`flock` 기반 동시성 락** — PR #217은 `git rev-parse --git-common-dir`에 exclusive lock을 건다. macOS(본 워크스테이션 플랫폼)에는 `flock(1)`이 기본 탑재되지 않아 그대로 이식하면 지시가 실패한다. worktree union만으로 "동일인·순차 실행" 충돌은 제거되며, 남는 것은 "동일인·동시 실행"의 초 단위 창이다. Open Questions Q1 참조.
- **기존 `tasks/completed/` 의 legacy id 리네임** — 무접두 id는 읽기 측에서 영구 지원한다. 마이그레이션 없음.
- **`ywc-setup-language`와 별도의 신규 setup skill 신설** — initials 쓰기는 1회성이므로 `ywc-task-generator`가 직접 수행한다 (YAGNI).
- PHASE 폭(6자리) 변경, SEQUENCE 규칙 변경, category 어휘 변경.

## Global Constraints

`CLAUDE.md`(프로젝트 루트)에서 그대로 인용:

- Skill 이름은 모든 배포 skill에서 `ywc-<kebab-case>` 를 따른다. SKILL.md는 ~500줄 이하로 유지하고 긴 섹션은 `references/`로 추출한다.
- 모든 skill 디렉터리는 `SKILL.md` + `README.md` / `README.en.md` / `README.ja.md` / `README.ko.md`(CI 강제)를 포함해야 하며, `README.zh.md` / `README.es.md`는 이미 존재하는 skill에서 함께 유지된다.
- 다른 skill을 `@skill-name`(force-load)으로 참조하지 않는다 — 이름으로만 참조한다.
- CI: `validate`(frontmatter + README 로케일 + `scripts/` shellcheck + `--list` dry run), `markdownlint`, `translation-check`(경고만, merge 차단 없음).
- 상위 워크스페이스 `CLAUDE.md`: 문서는 한국어, 코드/주석은 영어.

검증 커맨드(Step 2 확인): `bash scripts/validate.sh`, `bash scripts/install.sh --list`, `npx markdownlint-cli2`.

## Existing Constraints Touched

정규식을 실제로 강제하는 지점(모두 grep으로 전수 열거 — `claude-code/` 하위 `*.sh` / `*.py` / `*.json`에서 `{6}` 패턴 검색):

| 위치 | 현재 동작 | 영향 |
|---|---|---|
| `claude-code/skills/ywc-task-generator/scripts/next-task-number.sh:32` | `^([0-9]{6})-[0-9]{3}-` 로 PHASE 후보 판별 | initials 접두 디렉터리를 인식 못 함 → 반드시 수정 |
| 동 `:54` | `grep -oE '[0-9]{6}-[0-9]{3}-'` 로 graph 교차검증 | 동일 |
| 동 스크립트 전반 | `<tasks-dir>`와 `<tasks-dir>/completed`만 스캔, **worktree union 없음** | PR #217의 핵심 보강 지점 |
| `claude-code/skills/ywc-task-generator/scripts/scaffold-task-dir.sh:38` | `^[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$` 이름 검증 | 접두 id를 거부 → 반드시 수정 |
| `claude-code/skills/ywc-task-generator/scripts/compact-dependency-graph.py:43,45,46` | `PHASE_HEADING_RE` / `FULL_ID_RE` / `SHORT_ID_RE` | 접두 인식 + 부분매칭 방지 필요 |
| `claude-code/skills/ywc-finish-branch/scripts/build-pr-title.py:46,50` | `^(\d{6}-\d{3})-(.+)$`, `^(\d{6})-(.+)$` | 접두 id에서 PR 제목 prefix 추출 실패 |

ID 규약을 **산문으로 서술**하는 지점(문서 동기화 대상):

- `ywc-task-generator/SKILL.md:121,123,215,217,220,223,224,260,383,384`
- `ywc-task-generator/references/dependency-graph.md.template`, `references/execution-convention.md`
- `ywc-finish-branch/SKILL.md`, `ywc-gen-testcase/SKILL.md:53,360`, `ywc-sequential-executor/SKILL.md:49,174,270`, `ywc-parallel-executor/SKILL.md`, `ywc-worktrees/SKILL.md:49,50,53`
- 위 skill들의 `README.md` / `.en` / `.ja` / `.ko` / `.zh` / `.es`

재사용할 기존 패턴(신규 발명 아님):

- `claude-code/skills/references/language-resolution.md` — "공유 reference 1개 + `CLAUDE.md`의 canonical `## X` 섹션 + precedence chain" 구조. initials 해석은 이 형태를 그대로 따른다. (본 리포에는 `.ywc-config.json`도 `ywc-setup/scripts/write-config.sh`도 **존재하지 않음** — 전수 grep 결과 0건. 따라서 PR #217의 config 파일 방식은 그대로 이식하지 않는다.)
- `ywc-sequential-executor/evals/evals.json`, `ywc-task-generator/evals/evals.json` — legacy `001010` 형식과 신형 `000001-010` 형식 공존 시나리오가 이미 eval로 존재. 본 변경의 하위호환 eval은 같은 서술 방식을 따른다.

변경 불필요(열거했으나 손대지 않음):

- `claude-code/skills/**/*.md` — SKILL.md 본문에 인라인 정규식이 존재하는지 보완 grep(`[0-9]{6}` / `\d{6}` / `grep -oE`) 수행, **0건**. 따라서 위 6개 실행 지점이 정규식 강제 지점의 전수 집합이다.
- `claude-code/skills/ywc-parallel-executor/scripts/*.sh` — 6자리 PHASE 정규식 없음(grep 0건). worktree 이름을 task 이름으로 받아 그대로 전달만 하므로 접두 id가 투명하게 통과한다.
- 리포 자체의 `tasks/completed/000001-010-*` ~ `000006-020-*` 및 `tasks/dependency-graph.md` — legacy 무접두 id로 그대로 보존한다.

## Acceptance Criteria

- **AC1** — `.` 프로젝트 `CLAUDE.md`에 `## Task Initials` 섹션이 없고 `git config user.email`이 `yongwoon.kim@…`일 때, `ywc-task-generator`를 실행하면 `yk`를 파생해 1회 확인 질문을 하고, 승인 시 `CLAUDE.md`에 정확히 1개의 `## Task Initials` 섹션이 생성된다. 재실행 시 재파생·재질문이 없다. 확인: `grep -c '^## Task Initials' CLAUDE.md` → `1`.
- **AC2** — initials가 `yk`로 해석된 상태에서 새 batch를 생성하면, 모든 태스크 디렉터리명이 `^yk-[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$` 를 만족한다.
- **AC3** — `tasks/completed/`에 무접두 legacy id만 있고 `yk-` 항목이 없을 때, 신규 batch의 첫 PHASE는 **legacy 최대 PHASE + 1** 로 seed된다. 확인: 본 리포 실측 상태 — `bash claude-code/skills/ywc-task-generator/scripts/next-task-number.sh tasks` 가 `000082-010` 을 반환(디렉터리 최대 `000081`, graph 최대 `000083` 으로 drift 경고 동반)하므로, 첫 접두 batch는 `yk-000082-010-…` 이어야 한다. seed는 **디렉터리 스캔 결과**를 따르고 graph 값을 따르지 않는다.
- **AC4** — `yk-` 항목이 이미 존재하면 채번 스캔은 `yk-` 접두 항목만 비교 대상으로 삼는다. `ab-000050-010-…`가 존재해도 `yk`의 다음 PHASE에 영향을 주지 않는다. 확인: fixture 디렉터리로 `next-task-number.sh <dir> yk` 실행 → `ab-000050`을 무시.
- **AC5** — 동일 collaborator가 두 개의 linked worktree를 가질 때, 한쪽 worktree에서만 존재하는 `yk-000012-010-…`가 다른 worktree의 스캔 최대값에 반영된다. 확인: `git worktree add` fixture로 `next-task-number.sh` 실행 시 `000013-010` 반환.
- **AC6** — `compact-dependency-graph.py`가 `## Phase yk-000001` 헤딩과 `## Phase 000001` legacy 헤딩을 **둘 다** 정상 compact하며, `yk-000001-010`을 `000001-010`으로 부분매칭하지 않는다. 확인: 두 형식이 섞인 fixture로 실행 후 출력 diff 검사.
- **AC7** — `build-pr-title.py`가 `yk-000001-010-db-create-user-table` 입력에 대해 접두를 포함한 PR 제목 prefix를 산출하고, legacy `000001-010-…` 입력에 대한 기존 출력은 문자 단위로 불변이다.
- **AC8** — `scaffold-task-dir.sh`가 `yk-000001-010-db-x`(승인)와 `TOOLONG-000001-010-db-x`(exit 1)를 각각 올바르게 처리하고, legacy `000001-010-db-x`도 계속 승인한다.
- **AC9** — `bash scripts/validate.sh`, `bash scripts/install.sh --list`, `npx markdownlint-cli2` 가 모두 무회귀 통과한다.

## Functional Requirements

### FR1 — `references/initials-resolution.md` 신설 (AC1)

`claude-code/skills/references/initials-resolution.md` 를 `language-resolution.md`와 동형으로 작성한다. 내용:

- **Scope**: task id 채번 namespace 전용. 세션 언어·출력 언어와 무관.
- **Precedence chain**: `--initials` flag → 프로젝트 `CLAUDE.md`의 `## Task Initials` → 파생 + 1회 확인 → 캐싱.
- **파생 알고리즘**: `git config user.email`의 `@` 앞 local-part → `.`/`_`/`-` 로 분할 → 각 세그먼트 첫 글자 소문자 결합 (`yongwoon.kim` → `yk`). 2자 미만이면 원문의 앞 2–4자 소문자 영숫자. email 미설정 시 `user.name`.
- **검증**: `^[a-z0-9]{2,4}$`. 불일치 시 캐시된 값도 무효로 보고 재확인.
- **Canonical section 포맷**:

  ```markdown
  ## Task Initials

  - **Initials**: yk   <!-- ^[a-z0-9]{2,4}$ -->
  - Applies to: ywc-task-generator가 생성하는 task id의 INITIALS 세그먼트.
  ```

- **Numbering scope**: 해석된 initials 접두 항목만 비교, 모든 linked worktree union, legacy seed 규칙(FR3).

`language-resolution.md`와 마찬가지로 소비 skill은 `> **Action required**: Read [references/initials-resolution.md]` 지시로 참조하며 내용을 인라인 재서술하지 않는다.

### FR2 — `ywc-task-generator` Step 2에 initials 해석 삽입 (AC1, AC2)

- Step 2 서두에 "Resolve collaborator initials first" 를 추가한다. **태스크 존재 여부와 무관하게 매 실행 수행** — Step 7의 명명이 항상 INITIALS를 요구하기 때문.
- `--initials <value>` flag를 Arguments 표에 추가(검증 `^[a-z0-9]{2,4}$`, 최우선 순위).
- 캐싱 쓰기: `CLAUDE.md`의 `## Task Initials` 섹션 create-or-**replace** (append 금지 — `ywc-setup-language`의 중복 헤딩 방지 규칙과 동일).
- Rationalization Defense 표에 1행 추가: *"혼자 쓰는 리포라 initials는 과잉"* → *"두 번째 worktree가 생기는 순간 merge conflict 없이 조용히 충돌한다. 1회 질문의 비용은 0, 생략의 비용은 복구 불가능한 번호 모호성."*

### FR3 — 채번 스캔의 initials 한정 + worktree union + legacy seed (AC3, AC4, AC5)

`scripts/next-task-number.sh` 를 `next-task-number.sh [tasks-dir] [initials]` 로 확장한다.

- `initials` 인자가 주어지면 PHASE 후보 정규식은 `^<initials>-([0-9]{6})-[0-9]{3}-` 로 한정한다. 다른 initials 항목과 무접두 legacy 항목은 비교에서 제외한다.
- `initials` 인자가 없으면 현행 무접두 동작을 그대로 유지한다(하위호환).
- **worktree union**: `git worktree list --porcelain` 의 각 `worktree <path>` 에 대해 `<path>/<tasks-dir>` 와 `<path>/<tasks-dir>/completed` 를 동일 규칙으로 스캔해 max에 합산한다. 경로가 없으면 조용히 건너뛴다.
- **legacy seed 규칙**: `<initials>-` 접두 항목이 union 전체에서 0건이고 무접두 legacy 항목이 1건 이상이면, 첫 PHASE를 `legacy 최대 + 1` 로 seed한다. 이유 — 같은 `dependency-graph.md` 안에 `## Phase 000001`과 `## Phase yk-000001`이 공존하면 사람이 읽을 때 모호하다. 접두 항목이 1건이라도 있으면 이 규칙은 비활성화된다.
- 기존 graph 교차검증(STDERR drift 경고, 디렉터리 우선)은 initials-scoped 정규식으로 동일하게 유지한다.
- SKILL.md의 Step 2 및 Naming Convention 절(현행 `:121`, `:123`, `:224`)을 이 규칙을 인용하도록 갱신한다 — 규칙 본문은 한 곳(스크립트 주석 + `initials-resolution.md`)에만 둔다.

### FR4 — 스크립트 정규식에 선택적 접두 추가 (AC6, AC7, AC8)

| 파일 | 변경 |
|---|---|
| `scaffold-task-dir.sh:38` | `^([a-z0-9]{2,4}-)?[0-9]{6}-[0-9]{3}-[a-z]+-[a-z0-9-]+$` |
| `compact-dependency-graph.py:43` | `^##\s*Phase\s+(?:[a-z0-9]{2,4}-)?(\d{6})\b(.*)$` |
| `compact-dependency-graph.py:45` | `(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3}-[A-Za-z0-9][A-Za-z0-9-]*)` |
| `compact-dependency-graph.py:46` | `(?<![A-Za-z0-9-])((?:[a-z0-9]{2,4}-)?\d{6}-\d{3})(?![A-Za-z0-9-])` |
| `build-pr-title.py:46` | `^((?:[a-z0-9]{2,4}-)?\d{6}-\d{3})-(.+)$` |
| `build-pr-title.py:50` | `^((?:[a-z0-9]{2,4}-)?\d{6})-(.+)$` |

**핵심 주의**: `\b`는 `-` 앞뒤에서 성립하므로 `\b(\d{6}-\d{3})\b` 는 `yk-000001-010` 안의 `000001-010` 에 매칭된다. 따라서 lookbehind/lookahead로 경계를 명시해야 하며, 이 부분매칭 회귀는 AC6의 fixture로 반드시 검증한다.

`compact-dependency-graph.py`의 PHASE 그룹화는 접두를 포함한 전체 키(`yk-000001`)로 수행해야 한다 — 접두를 버리고 숫자만으로 묶으면 서로 다른 collaborator의 phase가 한 그룹으로 병합된다.

### FR5 — 문서·로케일 동기화 (AC9)

- `ywc-task-generator/SKILL.md` — Naming Convention 절(`[INITIALS]` 세그먼트 정의, 예시 `yk-000001-010-db-create-user-table`), Validation 체크리스트 2행.
- `references/dependency-graph.md.template` — `## Phase <initials>-NNNNNN` 헤딩 및 예시 id.
- `references/execution-convention.md` — `mv` 예시 및 디렉터리 트리 예시.
- `ywc-finish-branch` / `ywc-sequential-executor` / `ywc-parallel-executor` / `ywc-gen-testcase` / `ywc-worktrees` SKILL.md — task specifier·branch 명명 예시. prefix match 규칙은 "접두 유무와 무관하게 문자열 prefix 매칭"이므로 로직 변경 없이 예시와 1문장 설명만 갱신한다.
- 위 skill들의 `README.md` / `.en` / `.ja` / `.ko` / `.zh` / `.es` 동일 갱신. `translation-check`는 경고만 내지만 로케일은 함께 갱신한다.
- `ywc-task-generator/evals/evals.json` — initials 해석 및 legacy 공존 시나리오 1건 추가(기존 legacy 공존 eval 서술 방식을 따른다).

## Non-Functional Requirements

- **NFR1 (무회귀)** — initials가 해석되지 않은 상태(플래그 없음·섹션 없음·git config 없음)에서 모든 스크립트는 현행과 동일하게 동작해야 한다. 부재는 오류가 아니라 no-op이다 (`language-resolution.md`의 no-block invariant와 동일 원칙).
- **NFR2 (플랫폼)** — 스크립트는 macOS 기본 셸 도구만 사용한다. `flock`, GNU 전용 `grep -P`, GNU `sed -i` 금지.
- **NFR3 (단일 출처)** — 채번 규칙 본문은 `initials-resolution.md` + 스크립트 주석에만 존재한다. SKILL.md는 인용만 한다.
- **NFR4 (SKILL.md 길이)** — `ywc-task-generator/SKILL.md`가 ~500줄을 넘지 않도록, 추가 서술은 reference로 밀어낸다.

## ID Grammar Contract

```text
[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
    │          │        │          │             └─ [a-z0-9-]+
    │          │        │          └─ [a-z]+ (db, api, ui, lib, infra, docs, test, domain)
    │          │        └─ 3자리, 010부터 10 단위
    │          └─ 6자리
    └─ ^[a-z0-9]{2,4}$ — 생성 시 필수, 파싱 시 선택적(legacy 하위호환)
```

- **생성 측**(`ywc-task-generator`): 항상 접두를 붙인다.
- **파싱 측**(전 스크립트·전 executor): 접두 유무를 모두 받아들인다.
- 이 비대칭이 마이그레이션을 불필요하게 만드는 장치다.

## Edge Cases

| 상황 | 기대 동작 |
|---|---|
| `git config user.email` / `user.name` 둘 다 미설정 | 파생 실패 → 사용자에게 직접 입력 요청. 임의값을 발명하지 않는다. |
| 파생 결과가 `^[a-z0-9]{2,4}$` 불만족 (예: 한글 이름, 5자 이상) | 파생값을 제안하되 사용자 입력을 우선. 검증 실패 시 재질문. |
| `CLAUDE.md`에 `## Task Initials` 가 이미 2개 존재 | create-or-replace 원칙에 따라 첫 섹션을 갱신하고 나머지 중복 제거 후 정확히 1개 유지. |
| 두 collaborator가 같은 initials로 해석됨 (`yongwoon.kim`, `yuki.kato` → 둘 다 `yk`) | 구조적으로 감지 불가. 사용자가 확인 질문 단계에서 override하도록 프롬프트에 "이 프로젝트에서 이미 사용 중인 initials와 겹치지 않는지 확인" 문구를 넣는다. Q2 참조. |
| legacy 무접두와 `yk-` 접두가 한 `dependency-graph.md`에 공존 | 두 형식 모두 compact 대상. PHASE 그룹은 접두 포함 전체 키로 구분. |
| 접두 항목 0건 + legacy 0건 (빈 리포) | 첫 batch는 `<initials>-000001-010`. |
| `git worktree list` 가 linked worktree를 반환하지만 그 경로에 `tasks/` 없음 | 조용히 건너뛴다 (오류 아님). |
| 동일인이 두 worktree에서 **동시에** 실행 | 본 변경으로 좁혀지지만 완전 제거되지 않음. Q1 참조. |
| 접두를 포함한 branch 이름 `feature/yk-000001-010-…` | git ref로 유효. 별도 처리 불필요. |

## Critical Surfaces

없음 — 인증·결제·PII·외부 입력 경계를 건드리지 않는다. 다만 `next-task-number.sh` / `compact-dependency-graph.py` 는 **정규식 부분매칭 회귀**가 조용히 데이터(dependency graph)를 손상시킬 수 있으므로, 해당 두 파일의 변경은 fixture 기반 before/after diff 검증을 필수로 한다.

## Open Questions

> ⚠️ SUPERSEDED — Q1은 §A2, Q3은 §A7(Iteration 1), Q2는 §A9(Iteration 2)로 종결됨. 유효 항목 없음.

- **Q1 — `flock` 동시성 락을 지금 포함할 것인가?** 본 spec은 macOS 미탑재를 이유로 defer했다. 대안: `mkdir` 기반 잠금(POSIX 원자적)을 `next-task-number.sh`에 추가. 비용 ~10줄. 동일인이 두 worktree에서 **문자 그대로 동시에** 실행하는 빈도가 실제로 있는지에 따라 결정한다. 기본 권고: **defer**, 실제 충돌이 1회라도 관측되면 추가.
- **Q2 — initials 충돌(서로 다른 사람, 같은 이니셜) 감지를 자동화할 것인가?** 현재는 확인 질문의 문구로만 방어한다. 자동 감지는 "이미 존재하는 다른 initials 목록"을 스캔해 보여주는 정도(~5줄)로 가능하다. Medium 범위에 포함할지 판단 필요.
- **Q3 — 본 리포 자체의 `tasks/`를 접두 형식으로 전환할 것인가?** 현재 spec은 legacy 보존 + AC3의 seed 규칙으로 대응한다. 전환은 별도 결정.

## Iteration 1 Amendments

`ywc-spec-validate` iteration 1 결과(Critical 3 / Warning 3 / Suggestion 2, Gate 89)에 대한 수정. 본 절이 상충하는 원본 서술보다 우선한다.

### A1 — FR5에 공유 reference 레지스트리 추가 (Critical 1 대응)

FR5의 문서 동기화 목록에 다음을 **필수 항목으로** 추가한다:

- `claude-code/skills/CLAUDE.md` (현행 `:394-409`) — 공유 reference 단일 출처 규칙을 등록하는 canonical 레지스트리. 다음 세 가지를 기재한다:
  1. `references/initials-resolution.md` 를 `language-resolution.md` 와 동급의 공유 reference로 등록
  2. consuming-skill 목록에 `ywc-task-generator` 1건 (language의 6개 consumer와 달리 initials 소비자는 현재 1개)
  3. initials의 **no-block invariant** — `## Task Initials` 부재는 어떤 skill도 차단·지연·오류시키지 않는다

Precedent Site Coverage에서 이 site가 OMITTED로 판정된 것이 본 수정의 근거다. 상류 PR #217도 대응 파일을 갱신했다.

### A2 — FR6 신설: PHASE의 원자적 예약 (Critical 2 대응, Q1 종결)

`## Out of Scope`의 "`flock` 기반 동시성 락 defer" 및 Q1을 **철회**한다. `flock(1)` 부재는 사실이나, 그것이 "동시성 동작 자체를 정의하지 않을" 근거는 되지 못한다 (`ywc-spec-validate` Step 3.6: 공유 가변 상태의 동작과 경계는 필수, 기법은 자유).

**FR6 — PHASE 예약 (AC11)**

`next-task-number.sh` 가 PHASE `N` 을 확정하기 직전, git ref로 원자적 예약을 수행한다:

```bash
# refs/ 는 git common dir에 있으므로 모든 linked worktree가 공유한다
git update-ref "refs/ywc/task-phase/<initials>/<phase>" HEAD '' || { N=$((N+1)); continue; }
```

**실증 확인**(scratch 리포에서 실행):

| 호출 | 결과 |
|---|---|
| 1회차 `git update-ref refs/ywc/task-phase/yk/000082 HEAD ''` | `exit=0` |
| 2회차 (동일 ref) | `exit=128` — `cannot lock ref …: reference already exists` |
| `git branch -a` | `main` 만 표시 — 브랜치 목록 무영향 |

- `git update-ref <ref> <newvalue> ''` 의 빈 old-value는 "**해당 ref가 존재하지 않을 때만 생성**"을 의미하는 원자적 CAS다. 두 worktree가 같은 PHASE를 동시에 예약하면 정확히 한쪽만 성공한다.
- 실패한 쪽은 `N+1` 로 올려 재시도한다. 재시도 상한 100회, 초과 시 exit 1.
- ref는 **해제하지 않는다** — 로컬 할당 원장이며, 생성 후 중단된 실행이 있어도 번호 재사용을 막는다.
- ref는 `refs/heads/` 밖에 있으므로 push/fetch 대상이 아니고 브랜치 목록을 오염시키지 않는다.
- **별도 clone은 범위 밖** — git common dir를 공유하지 않으므로 예약이 보이지 않는다. initials namespace가 사람 단위 충돌을 이미 제거하므로 잔여 위험은 동일인이 두 clone을 동시에 쓰는 경우로 한정된다.

NFR2(macOS 이식성)를 위반하지 않는다 — `git update-ref` 는 플랫폼 무관이다.

### A3 — FR3의 graph 교차검증 scope 한정 (Critical 3 대응)

`next-task-number.sh` 의 drift 교차검증(현행 `:47-57`)을 다음과 같이 한정한다:

- graph 스캔 정규식도 동일 initials로 한정: `<initials>-[0-9]{6}-[0-9]{3}-`
- 해당 initials 항목이 graph에 **0건이면 비교를 건너뛴다** (경고 없음)

이 조항이 없으면, legacy 항목만 있는 graph에 대해 `graph_max=0` vs `max=000082` 로 **매 실행 허위 경고**가 발생한다. 본 리포는 실측 drift(graph `000083` / dirs `000081`)가 이미 있어 즉시 재현된다.

### A4 — sibling spec 소유권 선언 (Warning 1 대응)

`docs/ywc-plans/20260826-codex-pr217-collaborator-initials.md` 와의 관계를 명시한다:

- **ID 문법**(`[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`, `^[a-z0-9]{2,4}$`, 파싱 시 선택적 접두)은 **본 spec이 소유**하고 Codex spec은 참조한다. 두 트리의 task id는 상호 운용되어야 하므로 문법 분기는 허용되지 않는다.
- **initials 영속화 위치**는 의도된 분기다 — Claude Code는 `CLAUDE.md ## Task Initials`, Codex는 `.codex/ywc.json`. 각 트리의 기존 설정 관례를 따른 결과다.
- **동시성 기법**은 A2에서 sibling spec의 git-ref 예약 방식으로 **수렴**시켰다. 더 이상 분기가 아니다.

### A5 — `--initials` precedence AC 추가 (Warning 2 대응)

- **AC10** — precedence 3단이 각각 관찰 가능해야 한다: (a) `--initials ab` 를 전달하면 `CLAUDE.md` 의 `yk` 섹션이 있어도 `ab-` 접두가 생성된다. (b) 플래그 없고 섹션이 있으면 섹션 값이 쓰이고 파생·질문이 발생하지 않는다. (c) 둘 다 없으면 파생 + 1회 확인이 발생한다. 확인: 세 조건 각각 1회 실행 후 생성된 디렉터리명 접두 검사.
- **AC11** — 같은 PHASE에 대한 두 번째 `git update-ref … ''` 호출이 실패하고, 호출자가 `N+1` 로 재시도해 서로 다른 PHASE를 얻는다. 확인: 동일 ref에 대해 update-ref를 2회 실행 → 2회차 non-zero exit.

### A6 — worktree union 경로 정규화 (Warning 3 대응)

FR3의 worktree union에서 `<worktree-path>/<tasks-dir>` 결합 전에 `tasks-dir` 를 **현재 worktree 루트 기준 상대 경로로 정규화**한다. `tasks-dir` 가 절대 경로로 전달된 경우(실제 발생: 본 검증에서 절대 경로 호출) `git rev-parse --show-toplevel` 을 접두어로 제거해 상대화하고, 리포 밖 경로이면 union을 건너뛰고 현재 worktree만 스캔한다.

### A7 — Q3 종결 (Suggestion 1 대응)

**Q3를 "전환하지 않음"으로 확정한다.** 기존 `tasks/completed/` 의 무접두 id 81개 phase는 그대로 보존한다. 근거: ID 문법이 파싱 측에서 접두를 선택적으로 받으므로 전환의 실익이 없고, 전환은 `dependency-graph.md` 의 모든 상호참조를 다시 쓰는 비용을 발생시킨다. 이로써 AC3는 미해결 질문에 의존하지 않는다.

### A8 — CI 검증 수단 정정 (Suggestion 2 대응, AC9 개정)

Step 2에서 확인한 실제 CI 구성에 맞춰 AC9를 개정한다:

- **`.github/workflows/validate.yml:22` 의 shellcheck 는 `scandir: ./scripts` 로 한정**되어 있다. 즉 본 변경이 수정하는 `claude-code/skills/**/scripts/*.sh` 3개 파일은 **CI shellcheck 대상이 아니다**. NFR2(이식성) 검증은 CI에 의존할 수 없으므로, 변경된 각 스크립트에 대해 로컬에서 `shellcheck <path>` 를 수동 실행하는 것을 완료 조건에 포함한다.
- **`validate.yml:37` 의 toolkit eval 회귀 게이트**(`python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`)가 커밋된 baseline과 per-axis 점수를 비교해 하락 시 실패한다. 본 변경은 5개 SKILL.md를 수정하므로 점수 이동 가능성이 있다. 정당한 변동일 경우 baseline을 로컬에서 재생성해 커밋해야 한다.

개정된 **AC9** — 다음이 모두 통과한다:

1. `bash scripts/validate.sh`
2. `bash scripts/install.sh --list`
3. `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
4. markdownlint — CI(`markdownlint.yml:18-23`)와 **동일한 설정·범위**로 실행해야 한다. 기본 설정으로 돌리면 CI가 끄는 규칙(`MD013`/`MD060` 등)이 오탐을 낸다:

   ```bash
   printf '{"MD013":false,"MD031":false,"MD033":false,"MD037":false,"MD040":false,"MD060":false,"MD041":false}' > /tmp/ml.json
   npx markdownlint-cli2 --config /tmp/ml.json "README*.md" "CONTRIBUTING*.md" \
     "claude-code/skills/*/README*.md" "codex/skills/*/README*.md"
   ```

   범위가 README/CONTRIBUTING 한정이므로 **`docs/ywc-plans/**` 는 lint 대상이 아니다** — 본 spec 문서 자체의 lint 오류는 게이트가 아니다.
5. 변경된 3개 셸 스크립트 각각에 대한 로컬 `shellcheck` (CI 미커버, §A8)

## Iteration 2 Amendments

Suggestion 전용 보정 패스. Critical/Warning 수정 사이클이 아니므로 반복 상한에 계산되지 않는다.

### A9 — Q2 종결: initials 충돌 감지는 "디스크 스캔 목록 제시"로 한정 (Suggestion 1 대응)

**git authorship 기반 자동 감지는 채택하지 않는다.** 검토 중 다음을 실측했다:

| 측정 | 값 |
|---|---|
| `ls tasks/completed \| wc -l` (디스크) | 170 |
| `git ls-files tasks/completed` 기준 고유 디렉터리 (추적됨) | 34 |

즉 task 디렉터리의 **약 80%가 git에 추적되지 않는다**. `git log --diff-filter=A --format=%ae -1 -- <task-dir>` 로 생성자 이메일을 얻어 현재 사용자와 비교하는 방식은 추적된 20%에서만 신호가 나오고 나머지에서는 빈 문자열을 반환한다(실측 확인). 신호가 없는 것과 "충돌 없음"을 구분할 수 없으므로, 이 방식은 **거짓 안심**을 만든다. 채택하지 않는 편이 낫다.

대신 확인 질문 단계에서 **디스크 스캔으로 얻은 기존 initials 목록을 제시**한다 — 이 신호는 추적 여부와 무관하게 100% 가용하다:

- `<tasks-dir>`, `<tasks-dir>/completed`, 그리고 모든 linked worktree의 동일 경로에서 `^([a-z0-9]{2,4})-[0-9]{6}-[0-9]{3}-` 에 매칭되는 접두를 수집해 고유 목록을 만든다.
- 파생값이 그 목록에 **이미 존재하면** 확인 질문에 다음을 덧붙인다: "이 프로젝트에는 이미 `<initials>` 로 생성된 task가 N건 있습니다. 본인이 생성한 것이 아니라면 다른 값을 지정해 주세요."
- 목록에 없으면 통상 확인 질문만 한다.
- **차단하지 않는다** — 경고와 override 기회만 제공한다. 동일인의 재실행과 타인의 충돌을 기계적으로 구분할 방법이 없기 때문이다.

**AC12** — `yk-` task가 이미 존재하는 상태에서 파생 결과가 `yk` 일 때, 확인 질문에 기존 건수가 포함된다. 존재하지 않을 때는 포함되지 않는다.

### A10 — 예약 번호 소각 Edge Case 명시 (Suggestion 2 대응)

`## Edge Cases` 에 다음 행을 추가한다:

| 상황 | 기대 동작 |
|---|---|
| §A2의 예약 ref 생성 후 생성 실행이 중단되어 task 디렉터리가 만들어지지 않음 | 해당 PHASE는 **소각(burned)** 된다. 다음 실행의 디렉터리 스캔은 그 번호를 보지 못해 동일 번호를 계산하지만, `git update-ref` 가 exit 128로 거부하므로 `N+1` 재시도가 발생해 결과적으로 건너뛴다. 번호 연속성보다 재사용 방지를 우선한 의도된 동작이며, 별도 정리(GC)는 하지 않는다. |
| 예약 재시도가 100회 연속 실패 | exit 1로 중단하고 `refs/ywc/task-phase/<initials>/` 의 ref 개수를 함께 보고한다. 정상 상황에서 도달 불가능하므로 도달 시 원장 손상을 의심한다. |
