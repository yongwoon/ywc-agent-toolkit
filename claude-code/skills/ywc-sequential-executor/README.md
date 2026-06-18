# Sequential Executor Skill (ywc-sequential-executor)

ywc-task-generator Skill 로 생성된 Task 를 **순차적으로** 실행하는 Claude Code Skill 입니다. Branch 생성부터 구현, Commit, PR 생성, CI 확인, Merge, Local sync 까지의 전체 개발 Lifecycle 을 자동화합니다.

## Test-first, Deep Module, Critical Module Review

behavior change 는 test-first 입니다: bugfix 는 fix 전에 실패하는 regression test 를, 신규 동작은 구현 전에 실패하는 test 를 먼저 작성합니다(docs/config/mechanical task 은 예외). Public contract 변경 시 interface 를 body 보다 먼저 작성합니다(deep module). Task 의 Ownership 이 critical path(auth, payment, crypto, PII, external input)에 해당하면 `--review` 없이도 `/ywc-impl-review` 와 `/ywc-security-audit` 를 강제합니다. 자세한 내용은 `../references/tdd-deep-module-gray-box.md` 를 참고하세요.

단일 Task 실행뿐 아니라 연속된 Task range 를 지정하여 반복 실행하는 것도 지원합니다.

## Usage

### 기본 사용

단일 Task 를 실행합니다:

```text
/ywc-sequential-executor 000001-010-db-create-users-table
```

Phase+Sequence prefix 로도 지정할 수 있습니다:

```text
/ywc-sequential-executor 000001-010
```

### Range 실행

연속된 Task 를 순차적으로 반복 실행합니다:

```text
/ywc-sequential-executor 000001-010..000002-030
```

### 다음 Task 자동 감지

Task 를 지정하지 않으면 dependency graph 를 분석하여 실행 가능한 다음 Task 를 자동 선택합니다:

```text
/ywc-sequential-executor
```

### Option

| Option | 설명 | 예시 |
|--------|------|------|
| `--pr-lang <lang>` | PR title/description 언어 지정 | `--pr-lang ja` |
| `--tasks-dir <path>` | Tasks directory 경로 (default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--skip-ci-wait` | CI 대기 및 auto-merge skip (PR 생성만) | |
| `--draft` | Draft PR 생성, merge skip | |
| `--local-merge` | PR 없이 로컬에서 base branch 로 merge 후 push (Step 4 verification 은 동일하게 실행) | |
| `--aggregate-pr` | range 전체를 **work branch 1개 + PR 1개**로 delivery. 각 Task 를 `work/<name>` branch 에 순차 local-merge 한 뒤, 마지막에 work→base PR 1개로 ready→CI→bot→merge 까지 수행 | |
| `--group-name <name>` | work branch 이름(`work/<name>`) 지정. `--aggregate-pr` 전용, 생략 시 `work/<base>-<timestamp>` | `--group-name project-health` |
| `--base-branch <branch>` | Base branch 지정 (default: auto-detect) | `--base-branch develop` |
| `--dry-run` | 실행 계획만 표시 (Task 순서, dependency, mode). 실제 실행하지 않음 | |
| `--worktree` | range 전체를 **격리된 git worktree 1개** 안에서 실행하여 main checkout 을 비워 둡니다. run-level 격리 — Task 는 여전히 순차 실행. 독립 flag 로 4종 delivery mode·`--review` 와 결합 가능. 상세는 [references/worktree-run.md](./references/worktree-run.md) | `--worktree` |

> `--local-merge`, `--draft`, `--skip-ci-wait`, `--aggregate-pr` 는 상호 배타적입니다. 동시에 지정하면 Skill 이 중단되고 어떤 mode 인지 되묻습니다.
> `--local-merge` 는 **원격 CI 를 거치지 않으므로** 로컬 verification (lint/typecheck/test) 만이 merge 의 안전장치입니다. 민감한 변경에는 권장하지 않습니다.
> `--worktree` 는 위 mutual-exclusion 집단과 **독립**입니다 (5번째 멤버 아님). worktree 안에서 Docker stack 을 띄우면 host 의 기존 dev stack 과 host port 가 충돌할 수 있습니다 (host-isolation follow-up 소관). Task 가 순차 실행되므로 *병렬* 충돌은 발생하지 않습니다.

### Group 단위 실행 (`--aggregate-pr`)

여러 Task 를 **하나의 work branch 에 순차 누적한 뒤 group 당 PR 1개**로 delivery 하려는 경우 `--aggregate-pr` 를 사용합니다. range 전체가 다음 흐름으로 한 번에 처리됩니다:

1. `work/<name>` branch 를 base 에서 1회 생성
2. range 의 각 Task 를 **work branch 기준으로 순차 실행** (각 Task 는 work branch 에 local-merge → 다음 Task 는 갱신된 work branch 에서 분기)
3. 마지막 Task 종료 후 **work → base PR 1개** 생성 → ready → CI → bot review → merge → base sync
4. 완료 보고

real base(main)는 마지막 PR merge 전까지 **변경되지 않습니다**. parallel 의 worktree/wave 없이 순차로만 동작하므로 단순하고 안전합니다.

```text
/ywc-sequential-executor 000024-010..000025-030 --aggregate-pr --group-name project-health --review --pr-lang ko
```

- `--review`: 각 Task 가 work branch 에 합류하기 전 `/ywc-impl-review` 로 gate
- `--pr-lang ko`: 최종 PR title/description 언어 고정
- 실행 전 `--dry-run` 으로 Task 순서·생성될 work branch 를 미리 확인할 수 있습니다.

상세 절차는 [references/aggregate-pr.md](./references/aggregate-pr.md) 를 참고하십시오.

> 참고: 중단된 run 의 `.ywc-run-state.json` 이 남아 있으면 다음 실행이 그 state 로 resume 되어 새 range 가 무시될 수 있습니다. 새 range 를 의도한 경우 `.ywc-run-state.json` 을 먼저 정리하십시오.

## Execution Cycle

각 Task 에 대해 다음 Step 을 순서대로 실행합니다. **Range mode 에서는 Task 마다 전체 Cycle (Step 1 → Step 8) 을 반복합니다. 각 Task 는 독립적인 feature branch 를 사용합니다.**

### Range Mode 의 Task 별 Branch Lifecycle

**Normal mode (PR flow):**

```text
Task 마다: base branch checkout → pull → feature branch 생성 → 구현 → PR → CI → merge → 반복
```

**`--local-merge` mode:**

```text
Task 마다: base branch checkout → pull → feature branch 생성 → 구현 → local merge → push → 반복
```

**`--draft` / `--skip-ci-wait` mode:**

```text
Task 마다: 이전 feature branch 에서 분기 (chain branching) → 구현 → draft PR → 반복
```

### Step 상세

```text
Step 1: Dependency Validation & Spec Loading
  └─ Depends On 의 모든 Task 가 tasks/completed/ 에 있는지 확인
  └─ README.md 의 Spec Reference (Primary Sources / Summary / Out of Scope) 를 로드
  └─ 외부 URL 은 .claude/settings.local.json 의 taskExecutor.externalSpecUrls 정책에 따름

Step 2: Branch Creation (매 Task 마다 실행 — range 에서도 건너뛰지 않음)
  └─ (normal/local-merge) git checkout <base> && git pull && git checkout -b feature/<task-name>
  └─ (range+draft/skip-ci-wait) 이전 feature branch 에서 분기 (chain branching)

Step 3: Implementation
  └─ task.md 의 Implementation Steps 에 따라 구현, 적절한 단위로 Commit

Step 4: Task Verification
  └─ Task Verify command 및 lint/typecheck/test 실행

Step 5: PR Creation
  └─ create-pr Skill 호출 (security check, CI pre-push validation 포함)
  └─ (--local-merge) skip — PR 생성하지 않음

Step 6: CI Verification & Merge
  └─ gh pr checks --watch → gh pr merge --delete-branch
  └─ (--local-merge) git checkout base → git merge --no-ff feature/<task> → git push → git branch -d

Step 7: Local Sync
  └─ git checkout <base-branch> && git pull origin <base-branch>

Step 8: Mark Complete
  └─ mv tasks/<task-name> tasks/completed/<task-name> → commit
  └─ --local-merge range: 매 Task 마다 즉시 push
  └─ Normal PR range: push 는 마지막 Task 완료 후 한 번만 실행

Step 9: Next Task (Range mode)
  └─ 남은 Task 가 있으면 Step 1 로 돌아가 전체 Cycle 반복 (Step 2 포함)
```

## PR Language

`--pr-lang` 을 지정하지 않으면 다음 순서로 언어를 감지합니다:

1. **CLAUDE.md** — 언어 지시 확인 (예: `Git commits: Japanese`)
2. **AGENTS.md** — 언어 설정 확인
3. **최근 PR 이력** — 주로 사용된 언어 감지
4. **Fallback** — English

## Error Handling

| 상황 | 동작 |
|------|------|
| CI 실패 | 최대 2회 fix 시도 후 user 에게 알림 |
| Merge conflict | 중단 후 user 에게 수동 해결 요청 |
| CI timeout (30분 초과) | 상태 보고 후 user 에게 계속 대기할지 확인 |
| Dependency 미충족 | 미완료 dependency 목록 출력 후 중단 |
| Task 미발견 | 사용 가능한 Task 목록 표시 |

## Integration

이 Skill 은 다음 Skill 과 연동됩니다:

- **ywc-task-generator** — Task 생성 (upstream)
- **create-pr** — PR 생성 (Step 5 에서 호출)

## Example Prompt

### 단일 Task 실행 (Japanese PR)

```text
/ywc-sequential-executor 000001-010-db-create-users-table --pr-lang ja
```

### 전체 Range 실행

```text
/ywc-sequential-executor 000001-010..000003-020 --pr-lang ja
```

### Draft PR 만 생성 (merge 하지 않음)

```text
/ywc-sequential-executor 000001-010..000002-030 --draft --pr-lang ko
```

### Flag 충돌 시 동작

`--local-merge`, `--draft`, `--skip-ci-wait` 를 동시에 지정하면 Skill 은 실행을 중단하고 어떤 mode 를 의도했는지 되묻습니다. 이 세 flag 는 서로 다른 종료 상태를 만들기 때문입니다 (전자는 PR 없음 + merge 완료, 후자 둘은 PR 있음 + merge 없음).

```text
/ywc-sequential-executor 000001-010 --local-merge --draft
# → 중단. "local-merge 와 draft 는 상호 배타적입니다. 어떤 mode 를 원하시나요?"
```

### PR 없이 로컬 merge 만 실행

개인 project 나 hotfix 처럼 PR workflow 가 불필요할 때 사용합니다:

```text
/ywc-sequential-executor 000001-010-db-create-users-table --local-merge
```

Step 4 의 lint/typecheck/test 는 동일하게 실행되며, 통과하면 `git merge --no-ff` 로 base branch 에 병합되고 push 됩니다.

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
