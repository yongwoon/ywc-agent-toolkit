# ywc-impl-review

実装完了後、PR 作成前に仕様適合性を総合検証する Skill です。3つの Agent (Reviewer + Security + QA) を並列で実行します。

## 使用方法

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
```

## 実行 Agent

| Agent                 | 検証内容                                                |
| --------------------- | ------------------------------------------------------- |
| Reviewer Agent (opus) | 仕様に対する実装の漏れ/差異、コード品質、パターン一貫性 |
| Security Agent (opus) | OWASP Top 10、認証/認可の漏れ、Input Validation         |
| QA Agent (sonnet)     | Test Coverage 分析、漏れている Test Case の提案         |

## 出力形式

統合 Report — 3つの Agent の結果を Aggregator が統合し、重大度別の分類および修正優先順位を提供します。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
