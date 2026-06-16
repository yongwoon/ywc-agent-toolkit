# ywc-incident-postmortem

本番環境のインシデント発生後に、構造化されたPostmortem文書を作成するSkillです。
Timeline再構成、Root Cause分析（5 Whys）、影響範囲の評価、再発防止Action Item生成、
およびオプションでClient向けのsanitized報告書も生成します。

## 使用シナリオ

| 状況 | 具体例 |
|------|--------|
| サービス障害 | DB接続失敗、Deploy後のサーバーダウン、CDN障害 |
| セキュリティインシデント | API Key漏洩、認証回避、不審なアクセス |
| データ損失・破損 | Migration失敗、誤ったデータ削除 |
| 決済エラー | 二重課金、決済失敗ループ |
| パフォーマンス急落 | Deploy後のResponse Time急上昇 |

## 使用方法

```
/ywc-incident-postmortem             # 対話型Draftモード（デフォルト）
/ywc-incident-postmortem --template  # 空のTemplateを出力
/ywc-incident-postmortem --client    # Client向けsanitized報告書も生成
```

## 出力物

- **Internal Postmortem** — 技術詳細、Timeline、5 Whys、Action Itemを含む完全文書
- **Client Report**（--client指定時）— 内部情報を除いたUser影響中心のサマリー

## 関連Skill

- `ywc-security-audit` — インシデント**予防**のためのセキュリティ監査（事前）
- `ywc-impl-review` — 一般的なコード品質Review
- `ywc-changelog-release-notes` — Patch Release後の変更履歴ドキュメント作成
