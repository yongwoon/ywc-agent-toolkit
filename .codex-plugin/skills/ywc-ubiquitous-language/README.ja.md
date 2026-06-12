# ywc-ubiquitous-language

プロジェクトのUbiquitous Language（共有 Domain 語彙）をドキュメントとして作成・管理するSkillです。開発者、Domain Expert、LLMが同一用語でコミュニケーションできるよう `docs/ubiquitous-language.md` を生成・維持します。

3つのModeをサポートします: **new**（インタビュー主導の新規作成）、**extract**（既存 Codebase からの用語抽出）、**update**（既存ドキュメントの更新）。

## 使用シナリオ

- プロジェクト開始時にチーム共通の Domain 用語集を作成したいとき
- 既存の Codebase を分析して、暗黙的に使用されている Domain 用語を文書化したいとき
- 新 Feature 追加後、用語集に新概念を追加したいとき
- LLM がプロジェクトの Domain 用語を正確に理解できるよう CLAUDE.md に参照を追加したいとき

## 使い方

```bash
/ywc-ubiquitous-language
```

または自然言語で呼び出し:

> "ユビキタス言語のドキュメントを作成して"
> "Domain 用語集を作って"
> "ubiquitous language を更新して"
> "Codebase から Domain 用語を抽出して"

### Mode 自動検出

| 条件 | 自動選択 Mode |
|------|-------------|
| `docs/ubiquitous-language.md` 存在 | `update` |
| ファイル不在 + Source ファイルあり（`src/`、`app/` 等） | `extract` |
| ファイル不在 + Source ファイルなし | `new` |

`--mode new|extract|update` で強制指定も可能。

## 入力

- (任意) Domain 説明 — "これは B2B EC サービスです"
- (任意) `--mode new|extract|update` — Mode を強制指定
- (任意) `--context <名前>` — 特定の Bounded Context のみを対象
- (任意) `--ddd` — DDD Type 列を追加（Entity / Value Object / Aggregate / Domain Event / Policy）
- (任意) `--output <パス>` — 出力ファイルパス（デフォルト: `docs/ubiquitous-language.md`）

## 出力

- `docs/ubiquitous-language.md` — Bounded Context 別の用語 Table
- 完了後: CLAUDE.md に `@docs/ubiquitous-language.md` の追加を推奨するメッセージを出力

## 出力例

```markdown
# Ubiquitous Language — ShopBot

<!-- updated: 2026-05-02 -->

## Bounded Contexts

| Context | Responsibility |
|---------|---------------|
| Order   | 注文の作成から完了までのライフサイクル |

---

## Order

| Term      | Korean    | Definition                              | Synonyms to Avoid |
|-----------|-----------|------------------------------------------|------------------|
| Order     | 주문      | Customer が商品の購入を確定した単位      | Cart, Purchase    |
| OrderItem | 주문 항목 | Order 内の単一 Product + 数量ペア（不変）| LineItem, CartItem |
```

## 関連 Skill

- `ywc-plan` — Spec 作成前に用語集を定義する際に併用
- `ywc-project-docs` — Project 全体の docs/ Directory 構造を生成（上流）
- `ywc-spec-validate` — Spec 内の用語が用語集と一致するかレビュー
- `ywc-task-generator` — 用語集確立後に Task 分解する際の下流
- `ywc-code-gen` — コード生成時に用語集の Canonical naming を適用
