# Task Generator Skill

この Codex Skill は、Specification を dependency-safe で reviewable な実装 Task に分解します。

通常の task decomposition だけでなく、`git worktree` と分離された Codex session による parallel execution も考慮した Task metadata を生成する想定です。

## 使い方

### 基本的な使い方

Specification を渡して Task 生成を依頼します。

```text
/task-generator [Specification content]
```

既存の Task set を再整理する用途にも使えます。

```text
/task-generator refine docs/spec.md for parallel worktree execution.
```

### 言語オプション

この Skill は Korean、Japanese、English の出力に対応します。

| 言語 | 例 |
|------|----|
| Korean | `Output in Korean.` |
| Japanese | `日本語でタスクを生成してください。` |
| English | `Generate tasks in English.` |

言語指定がない場合は確認します。

Korean / Japanese で書く場合も、Technical terms は English のまま維持します。

### Granularity Mode オプション

この Skill は 2 種類の task granularity mode をサポートし、**常にどちらの mode で生成するかをユーザーに確認**します (silent default なし)。

| Mode   | Size guideline         | 最適化対象                                          |
|--------|------------------------|-----------------------------------------------------|
| human  | ~10 files / ~300 LOC   | PR 単位の human review                              |
| llm    | ~25 files / ~800 LOC   | 単一 LLM agent session (isolated worktree) 実行単位 |

Safety Invariants (DB migration 分離、Library 導入分離、Phase hard gate、完了時 buildable) は両 mode で同一です。詳細は [references/granularity-modes.md](./references/granularity-modes.md) を参照してください。

## 出力構造

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

- `PHASE`: 6 桁の dependency stage (multi-year な project 成長に備えた headroom)
- `SEQUENCE`: 3 桁、10 刻み
- `CATEGORY`: `lib` | `db` | `api` | `domain` | `worker` | `ui` | `test` | `refactor` | `infra`

### Task 完了

完了して merge された後:

```text
mv tasks/000001-010-db-create-user-table tasks/completed/000001-010-db-create-user-table
```

## Core Principles

| 原則 | 説明 |
|------|------|
| Reviewability | 各 Task はおおむね 1 時間以内で code review できるサイズ |
| Dependency Safety | forward dependency なしで順番に実装できること |
| DB Migration Separation | Database migration は必ず独立した Task にする |
| Library Introduction Separation | 新しい Library / Framework 導入は独立させる |
| Single Concern | 1 Task = 1 つの主要 concern |
| Parallel Safety | isolated worktree 実行のための metadata を含める |

## Parallel Worktree Operation

Task を parallel execution する可能性がある場合、生成される Task set には運用用 metadata を含めるべきです。

### 各 Task に必要な Metadata

各 `README.md` には以下を含めます。

- `Spec Reference` — Primary Sources (PRD / tech design への link)、Summary (2〜5 文の orientation)、Out of Scope (from spec) の guardrail。spec が存在しない housekeeping task は section を省略せず `N/A — no external spec` と明記します。
- `Ownership`
- `Shared Surfaces`
- `Conflicts With`
- `Parallelizable After`
- `Task Verify`

> Primary Sources に外部 URL (Notion, Confluence, Figma など) を含める場合は project-level policy が必要です。Default は project-relative paths のみで、`sequential-executor` skill が policy を `Codex approval settings or the project-local policy file` の `taskExecutor.externalSpecUrls` に保存して管理します。

### Ownership と Key Files

- `Key Files` は予想される変更対象の一覧
- `Ownership` は実際の operating boundary
- 両者が異なる場合は `Ownership` を優先します

### Dependency Graph Scheduling

`tasks/dependency-graph.md` は execution order の source of truth のままです。  
parallel work を想定する場合は、さらに `Parallel Execution Notes` を入れて以下を示します。

- initial ready set
- merge 後に runnable になる Task
- dependency ではなく conflict によって blocked される Task

### 推奨 Prompt 追記

parallel-friendly な出力を得るには、明示的に次を要求します。

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

この Skill が有効なリクエスト例:

- `task 生成`
- `task breakdown`
- `spec to tasks`
- `refine existing tasks`
- `parallel worktree tasks`
