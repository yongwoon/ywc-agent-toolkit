# ywc-parallel-executor (Parallel Executor)

task-generator が生成した Task を Agent が並列で実行する Skill です。dependency-graph.md を分析し、Wave ベースの並列実行 + Git Worktree 分離を行います。

## 使用方法

```text
/ywc-parallel-executor 000001-010-db-create-events           # 単一 Task
/ywc-parallel-executor 000001-010..000002-040                     # 範囲指定 (並列)
/ywc-parallel-executor --all                              # 全体実行
/ywc-parallel-executor 000001-010..000002-040 --review            # 並列 + 自動 Review
/ywc-parallel-executor 000001-010..000002-040 --local-merge       # PR なし Local merge
/ywc-parallel-executor 000001-010..000002-040 --draft             # Draft PR 作成
```

## Option

| Option | 説明 |
|--------|------|
| `--tasks-dir <path>` | Tasks directory パス (default: tasks/) |
| `--review` | 各 Task 完了後 /ywc-impl-review を自動実行します (組み合わせ可能) |
| `--local-merge` | PR なし、base-branch push のみ (デフォルト動作) |
| `--draft` | 全体完了後に Draft PR を作成します |
| `--per-task-pr` | Task ごとに個別 PR を作成します |

## 実行フロー

1. dependency-graph.md の Parse
2. Wave 計画の策定 (Topological Sort)
3. Wave 単位で実行: Worktree 作成 → Agent 並列実行 → Merge → Worktree 削除

## Task → Agent 自動マッピング

| Category | Agent |
|----------|-------|
| db, api, domain, lib, worker | Backend Agent (sonnet) |
| ui | Frontend Agent (sonnet) |
| test | QA Agent (sonnet) |
| infra | DevOps Agent (sonnet) |
| refactor | Reviewer Agent (opus) |

Agent Hint で Override が可能です:
```markdown
## Parallel Execution Metadata
- Agent Hint: frontend
```

## sequential-executor との比較

| 状況 | 推奨ツール |
|------|-----------|
| 小規模作業 (1-3 Task) | sequential-executor |
| 順次依存性が強い作業 | sequential-executor |
| 大規模作業 (4+ Task) | /ywc-parallel-executor |
| 並列可能な Task が多い場合 | /ywc-parallel-executor |

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
