# Task Generator Skill

Specification 을 분석하여 dependency-safe 하고 reviewable 한 구현 Task 를 생성하는 Codex Skill 입니다.

이 Skill 은 일반적인 task decomposition 뿐 아니라, `git worktree` 와 분리된 Codex session 을 사용하는 병렬 실행까지 고려한 Task metadata 를 생성하도록 설계되어 있습니다.

## Usage

### Basic Usage

Give the Skill a specification and ask it to generate tasks:

```text
$ywc-task-generator [Specification content]
```

You can also point it at an existing spec or task set:

```text
$ywc-task-generator refine docs/spec.md for parallel worktree execution.
```

### Language Options

The Skill supports 5 output languages. Accepted `--lang` values are `ko`, `ja`, `en`, `es`, and `zh`; long names (`korean`, `japanese`, `english`, `spanish`, `chinese`) remain backward-compatible aliases:

| Language | Example |
|----------|---------|
| Korean | `Output in Korean.` |
| Japanese | `日本語でタスクを生成してください。` |
| English | `Generate tasks in English.` |
| Chinese | `Generate task docs in Chinese.` |
| Spanish | `Generate tasks in Spanish.` |

If the user does not specify a language, the Skill resolves it through shared YWC language policy: `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` / `CLAUDE.md` > `~/.codex/ywc.json` > ask user.

For Korean, Japanese, Chinese, and Spanish outputs, technical terms remain in English:

- Korean: `Database 연결 설정`
- Japanese: `Database connection 設定`
- Chinese: `Database 连接设置`
- Spanish: `Configuración de Database connection`

Technical terms kept in English:
> API, Backend, Frontend, Database, Cache, Service, Repository, Application, Component, Module, Framework, Library, Request, Response, Schema, Model, Controller, Test, Debug, Deploy, Build, Configuration, Docker, Container, Server, Client, Router, Middleware

### Granularity Mode Options

Skill 은 두 가지 task granularity mode 를 지원합니다. 표준 option 은 `--mode human|llm` 이며, `--granularity human|llm` 도 backward-compatible alias 로 인식합니다. 두 option 이 모두 없을 때만 사용자에게 어떤 mode 로 생성할지 확인합니다 (silent default 없음).

| Mode   | Size guideline         | 최적화 대상                                          |
|--------|------------------------|------------------------------------------------------|
| human  | ~10 files / ~300 LOC   | Per-PR 단위의 human review                           |
| llm    | ~25 files / ~800 LOC   | 단일 LLM agent 세션 (isolated worktree) 실행 단위     |

두 mode 모두 Safety Invariants (DB migration 분리, Library 도입 분리, Phase hard gate, 완료 시 buildable) 는 동일하게 유지됩니다. 상세 규칙은 [references/granularity-modes.md](./references/granularity-modes.md) 를 참조하십시오.

## Preview Approval Workflow

`ywc-task-generator` 는 persisted preview approval flow 도 지원합니다.

- `--spec <path>`: persisted preview 와 auditable task write 의 canonical input
- `--preview-only`: preview artifact 만 기록
- `--preview-path <path>`: custom preview artifact path
- `--approve-preview`: 승인된 preview 를 re-decomposition 없이 consume
- `--non-interactive`: autonomous caller 가 승인된 preview 를 consume 할 때 필요

Preview identity 는 `spec_path`, `tasks_dir`, `lang`, `mode`, `preview_path`,
`preview_revision`, `preview_digest` 를 함께 묶어야 합니다. stale digest,
missing spec, path traversal, symlink escape, non-Markdown preview path 는
모두 `NEEDS_CONTEXT` 로 중단해야 합니다.

## Output Structure

### Task Directory

```text
tasks/
├── docs/ywc-plans/billing.task-preview.md
├── yk-000001-010-db-create-user-table/
│   ├── README.md
│   ├── task.md
│   └── test.md
├── 000001-020-api-user-registration/
│   ├── README.md
│   └── task.md
└── dependency-graph.md
```

Persisted preview artifact 는 다음 approval evidence 를 포함하는 것이
canonical contract 입니다.

```text
Preview Path: docs/ywc-plans/billing.task-preview.md
Preview Revision: rev-003
Preview Digest: sha256:...
Spec Path: docs/ywc-plans/billing.md
Tasks Dir: tasks/
Mode: llm
Refactor Phase: phase-2
Batch ID: billing-refactor-a
Depends On: 000001-020-api-billing-contract
```

### Task Naming

```text
[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```

- `PHASE`: 6 digits, dependency stage (multi-year 프로젝트 확장을 고려한 headroom)
- `SEQUENCE`: 3 digits, increments by 10
- `CATEGORY`: `lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra` | `config`

### Task Completion

After completion and merge:

```text
mv tasks/yk-000001-010-db-create-user-table tasks/completed/yk-000001-010-db-create-user-table
```

## Core Principles

| Principle | Description |
|-----------|-------------|
| Reviewability | Each task should be reviewable within about 1 hour |
| Dependency Safety | No forward dependency; each task is implementable at its position |
| DB Migration Separation | Database migration must be its own task |
| Library Introduction Separation | New libraries and frameworks must be isolated |
| Single Concern | One task should represent one primary concern |
| Parallel Safety | Tasks should include enough metadata for isolated worktree execution |

## Parallel Worktree Operation

When tasks may be executed in parallel via isolated worktrees or agent sessions, the generated task set should include operational metadata.

### Required Metadata Per Task

Each `README.md` should include:

- `Spec Reference`: Primary Sources (links to PRD / tech design), Summary (2–5 sentence orientation), and Out of Scope (from spec) — the guardrail against scope creep. Use `N/A — no external spec` for housekeeping tasks rather than omitting the section.
- `Ownership`: the edit boundary for the task
- `Shared Surfaces`: shared contracts or boundaries that may create conflicts
- `Conflicts With`: tasks that must not run in parallel
- `Parallelizable After`: the minimum merged baseline required before the task can start safely
- `Task Verify`: commands that prove the task is done

> External URLs in `Primary Sources` (Notion, Confluence, Figma, etc.) are gated by a project-level policy — default is project-relative paths only. The `sequential-executor` skill handles the policy and stores the decision in `Codex approval settings or the project-local policy file` under `taskExecutor.externalSpecUrls`.

### Ownership vs Key Files

- `Key Files` is a forecast of expected touched files
- `Ownership` is the operating boundary for the implementer or agent
- If they differ, `Ownership` is authoritative

### Dependency Graph Scheduling

`tasks/dependency-graph.md` remains the source of truth for execution order.  
When parallel work is expected, it should also include `Parallel Execution Notes` describing:

- the initial ready set
- which tasks become runnable after each merge boundary
- which tasks are blocked by conflicts rather than dependency order

### Recommended Prompt Additions

For parallel-friendly output, explicitly ask for:

```text
- Parallel Execution Metadata for every task
- Ownership as an operating boundary
- Conflicts With for shared contracts, schema, or config
- Parallel Execution Notes in dependency-graph.md
```

## Example Prompt

```text
$ywc-task-generator break down this specification into implementation tasks.

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

This Skill is a good match for requests such as:

- `task 생성`, `task 분해`, `작업 분해`
- `spec to tasks`, `task breakdown`, `implementation tasks`
- `refine existing tasks`
- `parallel worktree tasks`

## Validation

Shared static eval runner 로 skill bundle 의 structural convention (markers, eval schema 등) 을 검증할 수 있습니다.

```bash
# ywc-task-generator 만 검증 (6-digit phase, Granularity Mode section 등 확인)
python3 ../../../scripts/run_task_generator_evals.py --bundle yw_claude

# 존재하는 모든 bundle 자동 검증 (missing bundle 은 gracefully skip)
python3 ../../../scripts/run_task_generator_evals.py --bundle all
```

Runner 는 LLM 호출 없이 static marker 기반 검증만 수행합니다 — SKILL.md, templates, evals.json, README set 의 구조적 계약 위반을 탐지합니다. Output 품질 회귀 탐지는 별도 LLM-judge runner 가 추가되기 전까지 manual review 에 의존합니다.

### Pre-commit hook (optional)

Repository root 의 `.pre-commit-config.yaml` 로 commit 단계 자동 실행을 활성화할 수 있습니다.

```bash
brew install pre-commit   # macOS, 또는: pip install pre-commit
pre-commit install        # 한 번만 실행 — repo 별 git hook 설치
```

이후 `ywc-task-generator` skill 파일 또는 runner script 를 수정하는 commit 마다 runner 가 자동 실행되어, 규약 위반 시 commit 이 차단됩니다. Skill 파일을 건드리지 않는 다른 commit 은 영향을 받지 않습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
