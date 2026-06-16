# ywc-tech-research

技術調査および Library 比較を行う Research Agent Skill です。

## 使用方法

```text
/ywc-tech-research "Hono で Server-Sent Events を実装する方法"
```

## 使用シナリオ

| 状況                     | 例                                                       |
| ------------------------ | -------------------------------------------------------- |
| 仕様作成前               | "Web Analytics SDK Privacy-preserving 方式の比較"        |
| Library 選定             | "PostgreSQL Partition Table 集計 Performance 最適化戦略" |
| 実装中に行き詰まった場合 | "Rollup Tree-shaking Polyfill 問題の解決"                |

## 実行 Agent

- **Research Agent** (claude-sonnet-4-20250514)

## 出力形式

- 要約 (1-2文)
- 比較分析 (Table)
- 推奨方案および根拠
- Project 適用時の考慮事項
- 参考資料

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` Field に定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
