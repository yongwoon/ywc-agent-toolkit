# ywc-impl-review

実装完了後、PR 作成前に仕様適合性を総合検証する Skill です。Phase 1 で 5つの Agent (Architecture / Design / Devex / Security / QA — Sonnet 4つ、Haiku 1つ) を並列で実行し、曖昧な finding は Phase 2 Opus Advisor にエスカレーションします。

## 使用方法

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
```

`--working-tree` は commit を作成せず、staged・unstaged・untracked の source 変更をレビューします。`--code` や `--git-range` と併用しないでください。

`--non-interactive`（デフォルト: 未設定 = interactive）は Step 7 の learnings 昇格確認 prompt を開きません。代わりに report の `Learning candidates (not promoted — non-interactive)` block に候補を列挙します。どちらの mode でもユーザー確認なしに `docs/review-learnings.md` へ書き込むことはありません。

## 実行 Agent

| Agent                  | 検証内容                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| Architecture (sonnet)  | Module 境界、Layering、Dependency 方向、構造的仕様適合性            |
| Design (sonnet)        | API/Interface 設計、Naming、Signature、Error Model、Contract 仕様適合性 |
| Devex (sonnet)         | 可読性、Error Message、Logging、Documentation、Debuggability        |
| Security (sonnet)      | OWASP Top 10 分析                                                    |
| QA (haiku)             | Test Coverage の欠落、不足している Test Case                        |

Phase 2 (opus) — 上記 5つの Agent のうち曖昧な finding のみをエスカレーションして再検討します（Budget: デフォルト 5回、`--advisor-budget` で調整可能、共有）。

## 出力形式

統合 Report — Aggregator が Phase 1 の finding と Phase 2 Advisor の判定を統合し、重大度別の分類および修正優先順位を提供します。各 finding には `[P1]`/`[P2]` marker で Phase 1/Phase 2 の provenance が示されます。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
- [Chinese](./README.zh.md)
- [Spanish](./README.es.md)
