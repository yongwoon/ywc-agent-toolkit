# Sequential Executor Skill

ywc-task-generator Skill 로 생성된 Task 를 실행하는 Codex Skill 입니다. Branch 생성부터 구현, Commit, PR 생성, CI 확인, Merge, Local sync 까지의 전체 개발 Lifecycle 을 자동화합니다.

단일 Task 실행뿐 아니라 연속된 Task range 를 지정하여 반복 실행하는 것도 지원합니다.

## Usage

### 기본 사용

단일 Task 를 실행합니다:

```text
Use $ywc-sequential-executor to execute task 001010-db-create-users-table.
```

Phase+Sequence prefix 로도 지정할 수 있습니다:

```text
Use $ywc-sequential-executor to execute task 001010.
```

### Range 실행

연속된 Task 를 순차적으로 반복 실행합니다:

```text
Use $ywc-sequential-executor to run tasks 001010..002030.
```

### Aggregate PR 실행

연속된 Task 를 하나의 work branch에 누적하고, 마지막에 work -> base PR 하나로 전달합니다:

```text
Use $ywc-sequential-executor to run tasks 001010..003020 with --aggregate-pr --group-name billing-rollout.
```

`--aggregate-pr` mode에서는 각 Task가 별도 feature branch에서 구현되지만, Step 5 delivery는 real base가 아니라 `work/<name>` branch로 local merge됩니다. 마지막 Task까지 누적된 뒤 final PR lifecycle이 실행되며, 해당 work -> base PR이 merge되기 전에는 real base branch가 변경되지 않습니다.

### 다음 Task 자동 감지

Task 를 지정하지 않으면 dependency graph 를 분석하여 실행 가능한 다음 Task 를 자동 선택합니다:

```text
Use $ywc-sequential-executor to pick the next ready task from tasks/.
```

### Option

| Option | 설명 | 예시 |
|--------|------|------|
| `--pr-lang <lang>` | PR title/description 언어 지정 | `--pr-lang ja` |
| `--tasks-dir <path>` | Tasks directory 경로 (default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--skip-ci-wait` | CI 대기 및 auto-merge skip (PR 생성만) | |
| `--draft` | Draft PR 생성, merge skip | |
| `--local-merge` | PR 없이 로컬에서 base branch 로 merge 후 push (Step 4 verification 은 동일하게 실행) | |
| `--aggregate-pr` | Range 를 하나의 work branch에 누적한 뒤 final work -> base PR 1개로 delivery | `--aggregate-pr` |
| `--group-name <name>` | Aggregate work branch 이름 지정 (`work/<name>`). `--aggregate-pr`에서만 유효 | `--group-name billing-rollout` |
| `--base-branch <branch>` | Base branch 지정 (default: auto-detect) | `--base-branch develop` |
| `--worktree` | 전체 invocation을 단일 run worktree에서 실행. Delivery mode가 아니므로 다른 mode flag와 조합 가능 | `--worktree` |
| `--dry-run` | 실행 계획만 표시 (Task 순서, dependency, mode). 실제 실행하지 않음 | |

> `--local-merge`, `--draft`, `--skip-ci-wait`, `--aggregate-pr` 는 상호 배타적입니다. 동시에 지정하면 Skill 이 중단되고 어떤 mode 인지 되묻습니다.
> `--group-name`은 `--aggregate-pr` 없이 사용할 수 없습니다.
> `--worktree` 는 delivery mode 가 아니라 execution-location flag 입니다.
> `--local-merge` 는 **원격 CI 를 거치지 않으므로** 로컬 verification (lint/typecheck/test) 만이 merge 의 안전장치입니다. 민감한 변경에는 권장하지 않습니다.

## Contract / TDD baseline

동작 변경 task는 구현 전에 changed public contracts와 critical internals를 기록하고, failing test 또는 contract assertion을 먼저 확인합니다. docs-only, config-only, mechanical, no-harness 경우는 명시적인 TDD exception으로 보고합니다. Completion report에는 changed contracts, contract tests, critical internals, exceptions가 포함됩니다.

## Execution Cycle

각 Task 에 대해 다음 Step 을 순서대로 실행합니다. Range mode 에서는 Task 마다 전체 Cycle 을 반복합니다.

```text
Step 1: Dependency Validation & Spec Loading
  └─ Depends On 의 모든 Task 가 tasks/completed/ 에 있는지 확인
  └─ README.md 의 Spec Reference (Primary Sources / Summary / Out of Scope) 를 로드
  └─ 외부 URL 은 .codex/settings.local.json 의 ywDevSequentialExecutor.externalSpecUrls 정책에 따름

Step 2: Branch Creation
  └─ git checkout -b feature/<task-name>
  └─ (--aggregate-pr) work branch 에서 feature branch 생성
  └─ (range+draft/skip-ci-wait) 이전 feature branch 에서 분기 (chain branching)

Step 3: Implementation
  └─ task.md 의 Implementation Steps 에 따라 구현, 적절한 단위로 Commit

Step 4: Task Verification
  └─ Task Verify command 및 lint/typecheck/test 실행

Step 5: Delivery
  └─ ywc-finish-branch Skill 호출
  └─ PR 생성, CI 확인, merge, Mark Complete, branch cleanup 을 mode별로 처리
  └─ (--aggregate-pr) 각 Task 는 work branch 로 local merge

Step 6: Next Task (Range mode)
  └─ 남은 Task 가 있으면 Step 1 로 이동

Step 7: Final Aggregate PR (--aggregate-pr only)
  └─ 마지막 Task 이후 work -> base PR 생성
  └─ ready 전환, CI 확인, bot review, merge-readiness gate, merge, local base sync 완료
```

## Worktree Run

`--worktree` 는 sequential range 전체를 main checkout 밖의 단일 run worktree에서 실행합니다. Task 순서, per-task feature branch, verification, `ywc-finish-branch` delivery semantics는 그대로 유지되며, git command / file edit / verification / transition gate만 `$WT` context로 redirect됩니다.

```text
Use $ywc-sequential-executor to run tasks 001010..003020 with --worktree --pr-lang ko.
```

State는 `$WT/.ywc-run-state.json`에 저장되며, non-DONE 상태에서는 `$WT`와 integration branch를 보존해 resume할 수 있게 합니다. DONE cleanup에서는 run worktree를 prune하되 non-aggregate mode의 integration branch는 follow-up PR을 위해 보존합니다.

## Aggregate PR Lifecycle

`--aggregate-pr`는 range 전체를 group delivery로 취급합니다. Executor는 먼저 base branch에서 `work/<group-name>` 또는 자동 생성된 `work/<base-branch>-<timestamp>` branch를 만들고 push합니다. 이후 각 Task feature branch는 최신 work branch에서 분기하며, Task 완료 시 `ywc-finish-branch --local-merge --base-branch <work-branch>` 의미로 work branch에 누적됩니다.

마지막 Task가 work branch에 merge되면 executor는 work branch에서 단일 PR을 base branch로 생성합니다. 이 final PR은 draft 해제, CI watch, bot review polling, merge-readiness 확인, merge, local base sync까지 완료되어야 합니다. Work branch에 Task completion marker commits가 이미 있으므로 final PR merge 후 완료 표시를 다시 만들지 않습니다.

Stale `.ywc-run-state.json` guard도 이 mode에 적용됩니다. 저장된 run-state의 range 또는 args가 현재 명시 요청과 맞지 않으면 자동 resume하지 않고, 저장된 run을 계속할지 `.ywc-run-state.json`을 삭제하고 새 run으로 시작할지 선택을 요구합니다.

## PR Language

`--pr-lang` 을 지정하지 않으면 다음 순서로 언어를 감지합니다:

1. **AGENTS.md / CODEX.md / CLAUDE.md** — 언어 지시 확인 (예: `Git commits: Japanese`)
2. **최근 PR 이력** — 주로 사용된 언어 감지
3. **Fallback** — English

## Error Handling

| 상황 | 동작 |
|------|------|
| CI 실패 | 최대 2회 fix 시도 후 user 에게 알림 |
| Merge conflict | 중단 후 user 에게 수동 해결 요청 |
| CI timeout (30분 초과) | 상태 보고 후 user 에게 계속 대기할지 확인 |
| Dependency 미충족 | 미완료 dependency 목록 출력 후 중단 |
| Task 미발견 | 사용 가능한 Task 목록 표시 |
| Stale run-state mismatch | 자동 resume 중단, 저장된 run-state resume 또는 삭제 후 새 실행 중 선택 요청 |

## Integration

이 Skill 은 다음 Skill 과 연동됩니다:

- **ywc-task-generator** — Task 생성 (upstream)
- **ywc-create-pr** — PR 생성 (Step 5 에서 호출)
- **ywc-finish-branch** — PR/local merge, task 완료 표시, branch cleanup

## Example Prompt

### 단일 Task 실행 (Japanese PR)

```text
Use $ywc-sequential-executor to execute task 001010-db-create-users-table with --pr-lang ja.
```

### 전체 Range 실행

```text
Use $ywc-sequential-executor to run tasks 001010..003020 with --pr-lang ja.
```

### Draft PR 만 생성 (merge 하지 않음)

```text
Use $ywc-sequential-executor to run tasks 001010..002030 with --draft --pr-lang ko.
```

### Aggregate PR 로 Range 하나를 PR 하나로 전달

```text
Use $ywc-sequential-executor to run tasks 001010..003020 with --aggregate-pr --group-name billing-rollout --pr-lang ko.
```

이 mode는 각 Task를 work branch에 누적하고, 마지막에 work -> base PR 하나만 생성합니다.

### Flag 충돌 시 동작

`--local-merge`, `--draft`, `--skip-ci-wait`, `--aggregate-pr` 를 동시에 지정하면 Skill 은 실행을 중단하고 어떤 mode 를 의도했는지 되묻습니다. 이 네 flag 는 서로 다른 종료 상태를 만들기 때문입니다.

```text
Use $ywc-sequential-executor to execute task 001010 with --local-merge --draft.
# → 중단. "local-merge 와 draft 는 상호 배타적입니다. 어떤 mode 를 원하시나요?"
```

### PR 없이 로컬 merge 만 실행

개인 project 나 hotfix 처럼 PR workflow 가 불필요할 때 사용합니다:

```text
Use $ywc-sequential-executor to execute task 001010-db-create-users-table with --local-merge.
```

Step 4 의 lint/typecheck/test 는 동일하게 실행되며, 통과하면 `git merge --no-ff` 로 base branch 에 병합되고 push 됩니다.

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.
