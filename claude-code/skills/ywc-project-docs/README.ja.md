# project-docs

プロジェクトの `docs/` ディレクトリ構造と規約に従って、韓国語または日本語ドキュメントを生成する Claude Code Skill です。

対象言語は自動推測しません。`--lang kr|ja` オプションがあればそれを使用し、なければ韓国語/日本語のどちらで作成するかを先に質問します。

## 使用方法

### 自動トリガー

以下の表現で Skill が自動的に起動します：

```
"문서 작성해줘"        (韓国語: 文書を書いて)
"문서 만들어줘"        (韓国語: 文書を作って)
"document this"
"write a doc"
"add to docs/"
"ドキュメント作成して"
"ドキュメントを書いて"
"文書作成"
```

### 手動呼び出し

```
/ywc-project-docs              # 言語選択 prompt を表示
/ywc-project-docs --lang kr    # 韓国語で直接作成
/ywc-project-docs --lang ja    # 日本語で直接作成
```

## Skill の役割

1. **言語選択** — `--lang` を優先し、なければ韓国語/日本語を質問して決定（自動推測しない）
2. **ディレクトリルーティング** — 目的に応じて適切な `docs/` 配下へ配置
3. **命名規則の適用** — 英小文字 + ハイフン、接尾辞を最小化
4. **文書構造の生成** — 関連文書ブロック、目次、セクション番号を自動付与
5. **相互参照** — 関連文書間の双方向リンクを追加
6. **言語ポリシー** — 本文は選択言語、技術用語は英語を維持（カタカナ転写禁止）
7. **読み取り順序** — `product → architecture → specification → plans` の順序を保証
8. **アンチパターンの防止** — フォルダ境界混在、重複保存、下書き/公式の混同を防止

## 主なディレクトリマッピング

### 主軸（コアドキュメント）

| リクエスト種別 | 配置先 |
|---|---|
| 製品目標、スコープ、PRD | `docs/product/` |
| System 設計、技術選択 | `docs/architecture/` |
| 機能別ルール、実装基準 | `docs/specification/` |
| 実装順序、milestone | `docs/plans/` |

### 補助軸（運用・資産・一時）

| リクエスト種別 | 配置先 |
|---|---|
| 運用手順、設定 Guide | `docs/manuals/` |
| 障害対応、Known Issue | `docs/troubleshooting/` |
| 画面案、Design 資産 | `docs/design/` |
| 文書用補助画像 | `docs/imgs/` |
| 未確定のアイデア、一時メモ | `docs/todo/` |

## 使用例

```
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md （韓国語）

"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md （韓国語）

"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md （日本語）
```

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean](./README.ko.md)
