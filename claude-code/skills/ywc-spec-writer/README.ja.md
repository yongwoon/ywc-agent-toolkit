# ywc-spec-writer

Project specification writer。`docs/specification/` directory を作成・維持します。開発者と非開発者の両方が読める markdown 形式の仕様書を作成します。Program code なしで、目標・機能・Data Model・User Flow・非機能要件を記述します。

## 使用シナリオ

- **新規 project**: Specification がない project に初めて全体仕様書を作成するとき
- **Task ベース更新**: `ywc-task-generator` で作成した単一 task 文書を仕様書に反映するとき
- **Task Range / Multi 更新**: 複数 task（range・glob・multi-id）を一度に反映するとき
- **PR ベース更新**: 1 つまたは複数の PR diff と narrative で仕様書を更新するとき
- **Commit 後同期**: Code 変更後に仕様書と同期するとき
- **全体更新**: 仕様書全体を最新状態に再生成するとき

## 使用方法

```bash
/ywc-spec-writer                          # 自動モード（最近の commit ベース更新）
/ywc-spec-writer --full                   # 全体仕様書生成（確認が必要）
/ywc-spec-writer --update                 # 全体仕様書再生成
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-tasks 000002-010..000003-020   # Task range（phase 跨ぎ可）
/ywc-spec-writer --from-tasks 000002-* 000003-010      # Glob + 単一 ID 混在
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --from-pr 42                          # 単一 PR
/ywc-spec-writer --from-prs 42 43 51                   # 複数 PR（union diff）
/ywc-spec-writer --setup-hook             # Git hook インストール
/ywc-spec-writer --lang en                # 英語で作成
```

## 入力

- (任意) `--full` / `--update` — 全体生成または更新
- (任意) `--from-task <path>` — 単一 task directory パス
- (任意) `--from-tasks <id-or-pattern> ...` — Task range / glob / multi-id（active + completed 両方を探索）
- (任意) `--from-commit <ref>` — commit 参照（デフォルト: `HEAD`）
- (任意) `--from-pr <num>` — 単一 PR（gh CLI 必須）
- (任意) `--from-prs <num> ...` — 複数 PR の union diff（重複 file は自動 dedup）
- (任意) `--lang ko|ja|en` — 出力言語（デフォルト: `ko`）
- (任意) `--setup-hook` — Git pre-commit hook インストール

> `--from-pr` / `--from-prs` を使う場合は `gh` CLI が install・authenticate 済みである必要があります。PR title / body / `headRefOid` は spec 作成時の narrative context と audit trail として記録されます。

## 出力

```
docs/specification/
├── README.md              # Index + 変更履歴
├── 01-overview.md         # Project 概要
├── 02-features.md         # 機能要件（User Story 形式）
├── 03-data.md             # Data model
├── 04-interfaces.md       # 外部 Interface
├── 05-user-flows.md       # User Flow
├── 06-requirements.md     # 非機能要件
└── 07-glossary.md         # 用語集
```

## 非開発者への共有 (HTML Export)

`docs/specification/` は version controlled canonical document であるため markdown のまま維持されます。PM・client・非開発者の stakeholder に共有する際は、read-only な export script を使用します:

```bash
python3 tools/scripts/spec-to-html.py
# 出力: claudedocs/spec-export-YYYY-MM-DD.html
```

- Self-contained な HTML 1 file（Section ごとの tab + Copy as Markdown）
- 外部 dependency なし（Python 3 stdlib のみ）
- Canonical markdown source は変更されない — 一方向 derivation

Skill 自体には `--format html` を追加しません。Canonical doc に HTML を emit しない規約は [references/html-output.md](../references/html-output.md) §1 に定義されています。

## 関連 Skill

- `ywc-plan` — 機能計画を立てて仕様書作成の input を提供
- `ywc-spec-validate` — 作成した仕様書の品質を検証
- `ywc-task-generator` — 検証済み仕様書を task に分解
- `ywc-ubiquitous-language` — domain 用語を仕様書の語彙と整合
