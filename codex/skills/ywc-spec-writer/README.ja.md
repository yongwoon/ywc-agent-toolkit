# ywc-spec-writer

Project specification writer。`docs/specification/` directory を作成・維持します。開発者と非開発者の両方が読める markdown 形式の仕様書を作成します。Program code なしで、目標・機能・Data Model・User Flow・非機能要件を記述します。

## 使用シナリオ

- **新規 project**: Specification がない project に初めて全体仕様書を作成するとき
- **Task ベース更新**: `ywc-task-generator` で作成した task 文書を仕様書に反映するとき
- **Commit 後同期**: Code 変更後に仕様書と同期するとき
- **全体更新**: 仕様書全体を最新状態に再生成するとき

## 使用方法

```bash
/ywc-spec-writer                          # 自動モード（最近の commit ベース更新）
/ywc-spec-writer --full                   # 全体仕様書生成（確認が必要）
/ywc-spec-writer --update                 # 全体仕様書再生成
/ywc-spec-writer --from-task tasks/000002-010-api-user/
/ywc-spec-writer --from-commit HEAD
/ywc-spec-writer --setup-hook             # Git hook インストール
/ywc-spec-writer --lang en                # 英語で作成
```

## 入力

- (任意) `--full` / `--update` — 全体生成または更新
- (任意) `--from-task <path>` — task directory パス
- (任意) `--from-commit <ref>` — commit 参照（デフォルト: `HEAD`）
- (任意) `--lang ko|ja|en` — 出力言語（デフォルト: `ko`）
- (任意) `--setup-hook` — Git pre-commit hook インストール

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

## 関連 Skill

- `ywc-plan` — 機能計画を立てて仕様書作成の input を提供
- `ywc-spec-validate` — 作成した仕様書の品質を検証
- `ywc-task-generator` — 検証済み仕様書を task に分解
- `ywc-ubiquitous-language` — domain 用語を仕様書の語彙と整合
