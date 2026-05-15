# ywc-agentic (Agentic Orchestrator)

自然言語の目標を 1 つ受け取り、既存の `ywc-*` skill を自律的にオーケストレーションしてコード実装まで完了する Skill です。**Plan → Execute → Evaluate → Repeat** loop により、`ywc-impl-review` の評価を通過するか、ユーザー定義の反復上限に達するまで再計画を繰り返します。

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## 使用方法

```text
/ywc-agentic "ユーザー認証 API の実装"                     # 自然言語の目標を入力
/ywc-agentic --goal "検索機能の追加" --max-iterations 5    # 反復上限を指定
/ywc-agentic "決済モジュールの実装" --executor parallel    # Executor を強制指定
/ywc-agentic "リファクタリング作業" --resume               # 既存の tasks/ から再開
/ywc-agentic "目標" --dry-run                              # 段階計画のみ出力
```

## Option

| Option                 | 説明                                                              |
| ---------------------- | ----------------------------------------------------------------- |
| `<goal>`               | 達成する目標の自然言語による説明 (positional、必須)               |
| `--goal <text>`        | positional `<goal>` の代替 (両方指定時は positional 優先)         |
| `--max-iterations <n>` | 最大 loop 反復回数 (default: 3、自動で引き上げない安全弁)         |
| `--executor <mode>`    | Executor の強制指定: sequential / parallel / auto (default: auto) |
| `--tasks-dir <path>`   | Task directory および agentic-log.md のパス (default: tasks/)     |
| `--resume`             | Plan Phase をスキップし既存の tasks/ から再開                     |
| `--dry-run`            | 段階計画のみ出力し skill は実行しない                             |
| `--terse`              | 最小出力 (phase header と最終 report のみ)                        |
| `--pr-lang <lang>`     | PR タイトル・説明の言語 (default: auto、CLAUDE.md から推論)       |

## 実行フロー

1. Goal の受信・検証
2. プロジェクト context の検出 → Resume / Full Mode の決定
3. Plan Phase — `ywc-plan` を呼び出し (Re-plan 時は `--update-spec`)
4. Task Phase — `ywc-task-generator` を呼び出し (Medium/Large のみ)
5. Execute Phase — Executor を `--local-merge` で実行 (Small Path は `ywc-code-gen`)
6. Evaluate Phase — `ywc-impl-review --git-range` で元の spec に対し評価
7. Loop Control — Pass で終了 / Fail で再計画 / 反復上限到達時は部分完了 report
8. Iteration Log — `tasks/agentic-log.md` に append
9. Completion Report

## Small Path と Medium/Large Path

| Path              | 条件                              | 実行                                                        |
| ----------------- | --------------------------------- | ----------------------------------------------------------- |
| Small Path        | `ywc-plan` が Small と判定        | `ywc-code-gen` を直接呼び出し (Task Phase・Executor を省略) |
| Medium/Large Path | `ywc-plan` が Medium/Large と判定 | `ywc-spec-validate` → `ywc-task-generator` → Executor       |

## オーケストレーション対象 Skill

`ywc-plan` · `ywc-spec-validate` · `ywc-task-generator` · `ywc-sequential-executor` / `ywc-parallel-executor` · `ywc-impl-review` · `ywc-code-gen`

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
