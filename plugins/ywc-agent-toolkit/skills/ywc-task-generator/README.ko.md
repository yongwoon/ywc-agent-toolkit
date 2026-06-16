# Task Generator Skill

이 Codex Skill 은 Specification 을 dependency-safe 하고 reviewable 한 구현 Task 로 분해합니다.

일반적인 task decomposition 뿐 아니라, `git worktree` 와 분리된 Codex session 을 사용하는 병렬 실행까지 고려한 Task metadata 를 생성하도록 설계되어 있습니다.

## 사용 방법

### 기본 사용

Specification 을 제공하고 Task 생성을 요청합니다.

```text
/task-generator [Specification content]
```

기존 Task set 을 재정비하는 데도 사용할 수 있습니다.

```text
/task-generator refine docs/spec.md for parallel worktree execution.
```

### 언어 옵션

이 Skill 은 Korean, Japanese, English 출력을 지원합니다.

| 언어     | 예시                                 |
| -------- | ------------------------------------ |
| Korean   | `Output in Korean.`                  |
| Japanese | `日本語でタスクを生成してください。` |
| English  | `Generate tasks in English.`         |

언어를 지정하지 않으면 확인합니다.

Korean, Japanese 출력에서는 Technical 용어를 English 로 유지합니다.

### Granularity Mode 옵션

이 Skill 은 2 가지 task granularity mode 를 지원하며, **항상 어떤 mode 로 생성할지 사용자에게 확인합니다** (silent default 없음).

| Mode   | Size guideline         | 최적화 대상                                          |
|--------|------------------------|------------------------------------------------------|
| human  | ~10 files / ~300 LOC   | Per-PR human review                                  |
| llm    | ~25 files / ~800 LOC   | 단일 LLM agent session (isolated worktree) 실행 단위 |

Safety Invariants (DB migration 분리, Library 도입 분리, Phase hard gate, 완료 시 buildable) 는 두 mode 모두 동일하게 유지됩니다. 상세 규칙은 [references/granularity-modes.md](./references/granularity-modes.md) 를 참조하십시오.

## 출력 구조

### Task Directory

```text
tasks/
├── 000001-010-db-create-user-table/
│   ├── README.md
│   ├── task.md
│   └── test.md
├── 000001-020-api-user-registration/
│   ├── README.md
│   └── task.md
└── dependency-graph.md
```

### Task Naming

```text
[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```

- `PHASE`: 6자리 dependency stage (multi-year 프로젝트 확장을 고려한 headroom)
- `SEQUENCE`: 3자리, 10 단위 증가
- `CATEGORY`: `lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra`

### Task 완료

완료 후 merge 되면:

```text
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

## 핵심 원칙

| 원칙                            | 설명                                                 |
| ------------------------------- | ---------------------------------------------------- |
| Reviewability                   | 각 Task 는 대체로 1시간 이내 code review 가능한 크기 |
| Dependency Safety               | forward dependency 없이 순서대로 구현 가능해야 함    |
| DB Migration Separation         | Database migration 은 반드시 별도 Task               |
| Library Introduction Separation | 새 Library / Framework 도입은 분리                   |
| Single Concern                  | 1 Task = 1개의 주요 concern                          |
| Parallel Safety                 | isolated worktree 실행에 필요한 metadata 포함        |

## Parallel Worktree 운영 방법

Task 를 병렬로 실행할 가능성이 있다면, 생성된 Task set 에 운영용 metadata 가 포함되어야 합니다.

### Task 별 필수 Metadata

각 `README.md` 에 다음을 포함합니다.

- `Spec Reference` — Primary Sources (PRD / 기술설계서 link), Summary (2~5 문장 요약), Out of Scope (from spec) 가드레일. Spec 이 없는 housekeeping task 는 `N/A — no external spec` 로 명시 (section 자체를 생략하지 않음)
- `Ownership`
- `Shared Surfaces`
- `Conflicts With`
- `Parallelizable After`
- `Task Verify`

> Primary Sources 에 외부 URL (Notion, Confluence, Figma 등) 을 넣는 경우 project-level policy 가 필요합니다. Default 는 project-relative paths only 이며, `sequential-executor` skill 이 정책을 `Codex approval settings or the project-local policy file` 의 `taskExecutor.externalSpecUrls` 에 저장해 관리합니다.

### Ownership 과 Key Files

- `Key Files` 는 예상 변경 파일 목록입니다
- `Ownership` 은 실제 operating boundary 입니다
- 둘이 다르면 `Ownership` 을 기준으로 운영합니다

### Dependency Graph Scheduling

`tasks/dependency-graph.md` 는 여전히 execution order 의 source of truth 입니다.
병렬 작업을 전제로 할 때는 `Parallel Execution Notes` 를 추가해 다음을 적습니다.

- initial ready set
- 각 merge boundary 이후 runnable 해지는 Task
- dependency 가 아니라 conflict 때문에 함께 돌리면 안 되는 Task

### 추천 Prompt 추가 문구

병렬 실행에 적합한 결과를 얻으려면 아래 요구사항을 명시하는 것이 좋습니다.

```text
- Parallel Execution Metadata for every task
- Ownership as an operating boundary
- Conflicts With for shared contracts, schema, or config
- Parallel Execution Notes in dependency-graph.md
```

## Example Prompt

```text
/task-generator break down this specification into implementation tasks.

Requirements:
- Output in Korean.
- Assume tasks may be executed in parallel via git worktrees and separate Codex sessions.
- For every task README, include Ownership, Shared Surfaces, Conflicts With, Parallelizable After, and Task Verify.
- Ownership must be an operating boundary, not just a summary of expected files.
- In dependency-graph.md, include Parallel Execution Notes.

Specification:
[PASTE SPEC HERE]
```

## Trigger Keywords

이 Skill 이 잘 맞는 요청 예시:

- `task 생성`
- `task 분해`
- `spec to tasks`
- `refine existing tasks`
- `parallel worktree tasks`
