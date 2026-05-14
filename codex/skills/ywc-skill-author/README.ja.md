# ywc-skill-author

新しい ywc-* skill を作成、または既存 skill の構造を改善する際に利用する **メタ skill** です。18 個の production ywc-* skill から抽出した canonical な rule set (Frontmatter format、Rationalization Defense、multilingual triggers、progressive disclosure 等) を LLM が自動的に遵守するよう強制します。

## 使用シナリオ

- 新しい ywc-* skill をゼロから作成する場合
- 既存 ywc-* skill の frontmatter、body section、references 構造を改善する場合
- 18 個の ywc-* skill を canonical rule set 基準で audit する場合

## 使用方法

```bash
/ywc-skill-author
```

または自然言語での呼び出し:

> 「ywcスキル作成して」
> 「ywc skill を audit して」
> 「ywc skill の構造を upgrade して」

## 入力

- 新規 skill の場合: skill の目的、主要な trigger シナリオ
- audit の場合: 対象 skill directory のパス

## 出力

- 標準構造 (Frontmatter + Rationalization Defense + Workflow + Validation Checklist) の SKILL.md
- 必要に応じた `references/` 配下の補助 document
- 多言語 README set (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`)

## Core Rules

この skill が強制する標準は以下で構成されます:

- **Mandatory Rules**: Frontmatter / Body / Filesystem 領域の強制 rule (A1–A13)
- **Recommended Rules**: 状況別の推奨 rule (B1–B7)
- **Format Conventions**: Korean prose + English Technical 用語 policy 等
- **Anti-patterns**: Description workflow summary、stub code、`@` syntax 等の禁止 pattern

詳細は `SKILL.md` 本文と `references/` 配下の 4 つの document を参照してください。

## 関連 Skill

- `ywc-task-generator` — 同じ multilingual policy と reference 分離 pattern を適用
- 全ての ywc-* skill — 本 skill の rule に準拠

## 参考 Document

- `references/skill-template.md` — 新規 skill 開始 template
- `references/rationalization-defense-cookbook.md` — Rationalization Defense table 作成 guide
- `references/description-anti-patterns.md` — Description field の禁止 pattern
- `references/cross-skill-graph.md` — 18 個の ywc-* skill 間の dependency + cross-reference graph
