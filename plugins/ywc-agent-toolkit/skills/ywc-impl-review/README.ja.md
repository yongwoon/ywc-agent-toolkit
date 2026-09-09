# ywc-impl-review

実装完了後、PR 作成前に仕様適合性を総合検証する Skill です。Phase 1 で 5つの Agent (Architecture / Design / Devex / Security / QA) を並列で実行し、曖昧な finding は Phase 2 Advisor にエスカレーションします。

Worker の実行前に、空の対象または 200 ファイルを超える対象を拒否します。`--base`、`--git-range`、`--working-tree` の diff 対象では追加・削除行の合計が 5,000 行を超える場合も拒否し、`--code` はパスのみの対象なのでファイル数だけを制限します。拒否時には正確な件数と最大のファイルを報告します。

Phase 1 後、Critical/High の finding は `file:line` と主張された重大度だけを渡す blind 独立検証を受けます。結果は `reproduced`、`verification-failed`、`verification-error`、`cap-unverified` に分け、検証呼び出しは Phase 2 Advisor の budget を消費しません。`[P1]`/`[P2]` の provenance と検証状態は別の情報です。

## 使用方法

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --base main
```

`--working-tree` は commit を作成せず、staged・unstaged・untracked の source 変更をレビューします。`--base <ref>` は `git merge-base <ref> HEAD` から `HEAD` までをレビューし、指定した ref と解決された merge-base をレポートします。`--git-range A..B` は明示的な二端点比較として維持します。4つの target mode のうち正確に1つが必須で、互いに排他的です。

## 実行 Agent

| Agent                  | 検証内容                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| Architecture           | Module 境界、Layering、Dependency 方向、構造的仕様適合性            |
| Design                 | API/Interface 設計、Naming、Signature、Error Model、Contract 仕様適合性 |
| Devex                  | 可読性、Error Message、Logging、Documentation、Debuggability        |
| Security               | OWASP Top 10 分析                                                    |
| QA                     | Test Coverage の欠落、不足している Test Case                        |

Phase 2 Advisor — 上記 5つの Agent のうち曖昧な finding のみをエスカレーションして再検討します（Budget: デフォルト 5回、`--advisor-budget` で調整可能、共有）。独立検証の呼び出しはこの budget の対象外です。

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
