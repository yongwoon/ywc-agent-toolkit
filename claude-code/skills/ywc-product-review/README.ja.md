# Product Review Skill

## 概要

**ywc-product-review** は、進行中のプロジェクトを5つのビジネス・サービス観点から分析し、優先順位付きの改善 Feedback を提供する Claude Code Skill です。

コードベースと文書（README、企画書、Spec）を両方分析し、技術的なコード品質ではなく、**ユーザー価値・成長・リスク・市場観点**からの改善点を導き出します。

**主な機能:**

- 5つのビジネス観点からのプロジェクト分析
- コードベース + 文書の統合分析
- 🔴 High / 🟡 Medium / 🟢 Low 優先度 Report の自動生成
- 即時実行可能な改善提案を含む
- Executive Summary でコアインサイトを要約

**対象ユーザー:**

- サービス改善方向を探している Product Manager および開発者
- ビジネス観点でプロジェクトを点検したいチーム
- 「次に何を作るべきか？」の答えを求めているチーム

---

## 使い方

### Skill の呼び出し

Claude Code では以下のように呼び出します:

```
# 全体分析（5つの観点すべて）
/ywc-product-review

# 特定の観点のみ分析
/ywc-product-review user-value growth

# 文書を明示的に指定
/ywc-product-review @README.md @docs/spec.md
```

または自然言語で:

```
User: このプロジェクトをビジネス観点でレビューして
User: サービス改善ポイントを見つけて
User: 成長のために改善すべき点は何？
User: ユーザー価値の観点から不足している点を分析して
```

### 前提条件

- 分析対象プロジェクトのコードベースが現在の Directory にある、または
- README、企画書などの文書を参照できる状態であること

---

## 分析観点

### 5つのコア観点

| 観点タグ | 分析内容 | Reference ファイル |
|---|---|---|
| `[User Value]` | Job-to-be-Done、Value Proposition、未充足ニーズ | `references/user-value.md` |
| `[UX Flow]` | Onboarding、離脱ポイント、コアユーザー Journey | `references/ux-flow.md` |
| `[Growth]` | Retention、Viral Loop、Activation、Engagement | `references/growth.md` |
| `[Risk]` | ユーザー Pain Point、Churn 要因、未解決問題 | `references/risk.md` |
| `[Market]` | Feature 優先度、市場トレンド、競合 Gap | `references/market-timing.md` |

### 分析フロー

```
Context 収集（README + コードベース）
    ↓
Phase 1: 5つの観点 Subagent を並列実行（各 Sonnet）
├── User Value  ├── UX Flow  ├── Growth  ├── Risk  └── Market
    ↓
Phase 2: Opus Advisor（クロス観点の競合時、最大 2 回）
    ↓
優先度分類（High / Medium / Low）
    ↓
Report 生成 + Executive Summary
```

---

## 出力 Report 形式

分析完了後、以下の形式で結果を出力します:

```markdown
## Product Review Report: [Project Name]

**Analysis Date**: [日付]
**Perspectives Reviewed**: User Value · UX Flow · Growth · Risk · Market Timing

---

### 🔴 High Priority — 即時改善推奨

| # | Perspective   | Problem        | Evidence        | Suggestion      |
|---|---------------|----------------|-----------------|-----------------|
| 1 | [User Value]  | [問題説明]      | [コード/文書根拠] | [改善提案]      |

---

### 🟡 Medium Priority — 近期 Roadmap 検討

...

---

### 🟢 Low Priority — 中長期考慮

...

---

### Executive Summary

- **最大の機会**: [最高インパクトの改善点]
- **即時解決すべき課題**: [最も緊急な問題]
- **中長期方向性**: [サービスの次フェーズの方向]
```

---

## ファイル構造

```
ywc-product-review/
├── SKILL.md                        # Skill 定義と Workflow
├── README.md                       # 韓国語 Guide
├── README.en.md                    # English Guide
├── README.ja.md                    # このファイル（日本語 Guide）
├── README.ko.md                    # 韓国語 Guide（同内容）
└── references/
    ├── user-value.md               # ユーザー価値 Checklist
    ├── ux-flow.md                  # UX Flow Checklist
    ├── growth.md                   # Growth Mechanics Checklist
    ├── risk.md                     # Risk & Pain Points Checklist
    ├── market-timing.md            # Market Timing Checklist
    └── report-template.md          # Report 出力 Template
```

---

## 使用例

### Example 1: 全体観点の分析

```
User: このプロジェクトをビジネス観点でレビューして

Claude: プロジェクト構造と README を確認します。

[コードベースおよび文書の分析実行]

Phase 1: 5つの Subagent を並列実行中...
[User Value Subagent] Job-to-be-Done の明確さを確認中
[UX Flow Subagent] Onboarding とコアフローを分析中
[Growth Subagent] Retention と Viral メカニズムを確認中
[Risk Subagent] 未解決 Pain Point を探索中
[Market Subagent] 競合 Gap とタイミングを分析中
Phase 2: Opus Advisor がクロス観点の競合をレビュー中...

## Product Review Report: My Project

### 🔴 High Priority

| # | Perspective | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | [UX Flow] | Onboarding が5ステップ以上必要 | README の Quick Start が複雑 | 核心価値を2ステップ以内で体験できるよう簡素化 |
| 2 | [Growth] | Retention メカニズムがない | 再訪問を促す機能がない | 週次 Summary 通知または進捗 Dashboard を追加 |

...

### Executive Summary
- **最大の機会**: Onboarding の簡素化で Activation Rate を向上
- **即時解決すべき課題**: 再訪問誘導メカニズムの不在
- **中長期方向性**: Network Effect のある協業機能の導入
```

### Example 2: 特定観点のみ分析

```
User: Growth 観点のみで分析して

Claude: Growth Mechanics 観点で分析します。

[references/growth.md をロードして適用]

## Product Review Report: My Project
**Perspectives Reviewed**: Growth

### 🔴 High Priority
...
```

---

## Best Practices

### 1. 文書とコードを一緒に提供

コードベースだけでなく README、企画書、ユーザーインタビュー資料を合わせて提供すると、より深い分析が可能です:

```
User: @README.md @docs/product-spec.md を基に Product Review をして
```

### 2. 繰り返し活用で進化を追跡

機能追加や改善後に再実行して、改善前後を比較できます。

### 3. Executive Summary を Roadmap 入力として活用

High Priority 項目を Sprint または Milestone の入力として直接活用してください。

---

## 関連文書

### プロジェクト内部参照

- [UI/UX Review Skill](../ywc-ui-ux-review/README.ja.md) — UI/UX 観点の詳細レビュー（視覚デザイン、Information Architecture）

---

## バージョン情報

- **最終更新**: 2026-04-25
- **Skill Version**: 1.0
- **対応環境**: Claude Code

---

## License

この Skill は `develop-with-llm` プロジェクトの一部として、学習・参考目的で提供されます。
