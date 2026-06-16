# ywc-spec-validate

仕様作成完了後、task-generator 実行前に仕様品質を検証する Spec Reviewer Agent Skill です。

## 使用方法

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
/ywc-spec-validate --spec docs/ywc-plans/example.md --advisor-budget 0
```

## 検討観点

| 観点                 | 検討内容                                                  |
| -------------------- | --------------------------------------------------------- |
| 完成度               | 必須項目の欠落 (Error Handling, Edge Case, Pagination 等) |
| 一貫性               | 文書間の用語/Format/Data 構造の不一致                     |
| 実現可能性           | 現在の Stack で実装可能かどうか                           |
| 既存 Code との整合性 | 現在の DB Schema、API Route Pattern との競合有無          |

## 実行 Agent

- **Spec Reviewer Agent** (claude-opus-4-20250514)

## 出力形式

Critical / Warning / Suggestion の重大度別に分類し、各 Issue にファイル:行の参照および改善提案を付与します。

## Advisor Budget

`--advisor-budget <n>` はこの invocation の Phase 2 advisor budget です。省略時は default `2` と同等で、`0` は advisor escalation を無効化します。Report header には `Phase 2 advisor calls used: X of N (...)` と `Advisor budget status: available | disabled | exhausted | advisor-required | not-reported` が含まれます。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` Field に定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
