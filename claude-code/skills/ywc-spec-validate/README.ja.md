# ywc-spec-validate

仕様作成完了後、task-generator 実行前に仕様品質を検証する Spec Reviewer Agent Skill です。

## 使用方法

```text
/ywc-spec-validate --spec docs/outline/02-backend-api-design.md
```

## 検討観点

| 観点                 | 検討内容                                                  |
| -------------------- | --------------------------------------------------------- |
| 完成度               | 必須項目の欠落 (Error Handling, Edge Case, Pagination 等) |
| 一貫性               | 文書間の用語/Format/Data 構造の不一致                     |
| 実現可能性           | 現在の Stack で実装可能かどうか                           |
| 既存 Code との整合性 | 現在の DB Schema、API Route Pattern との競合有無          |

## 実行 Agent

### Phase 1 — 並列分析（Sonnet × 4）

| Subagent | 担当観点 |
|---|---|
| Completeness Subagent | 完成度 |
| Consistency Subagent | 一貫性 |
| Feasibility Subagent | 実現可能性 |
| Code Compatibility Subagent | 既存 Code との整合性 |

### Phase 2 — Advisor（Opus、最大 2 回）

曖昧な Finding に限り Opus Advisor が判断を提供します。`--advisor-budget <n>` で呼び出しごとの escalation 回数を制御でき、`--advisor-budget 0` の場合は escalation を無効化し、該当 Finding を通常の Suggestion として報告します（orchestrator の cost guard 用）。

## 出力形式

Critical / Warning / Suggestion の重大度別に分類し、各 Issue にファイル:行の参照および改善提案を付与します。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` Field に定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
