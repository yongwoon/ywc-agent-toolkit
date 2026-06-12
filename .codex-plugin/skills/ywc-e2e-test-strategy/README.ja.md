# ywc-e2e-test-strategy

Playwright を使った自動E2Eテスト戦略の設計・実装 Skill です。新規 project の Playwright 初期設定から、既存 project の Coverage 分析、特定 User Flow のテスト生成、GitHub Actions CI 連携まで一括対応します。

## 使用シナリオ

- **新規 project**: "Playwright を設定して"、"E2E テストをゼロから追加したい"
- **既存 project の監査**: "E2E coverage のギャップを確認して"、"Critical path が抜けていないか調べて"
- **単一 Flow 追加**: "ログイン flow の Playwright テストを書いて"、"決済 flow のE2E テスト作って"
- **CI 連携**: "GitHub Actions に E2E を組み込みたい"

## 使用方法

```bash
/ywc-e2e-test-strategy --init           # 新規 Playwright 設定
/ywc-e2e-test-strategy --audit          # 既存 Coverage 監査
/ywc-e2e-test-strategy --flow login     # 特定 Flow テスト生成
/ywc-e2e-test-strategy --init --ci      # 初期設定 + GitHub Actions 連携
```

または自然言語で:

> "E2Eテスト戦略を設計して"
> "Critical path を自動化して"
> "E2E coverage を確認して"

## Mode 一覧

| Mode | Flag | 使用タイミング |
|------|------|----------------|
| Init | `--init` | `playwright.config.*` が存在しない場合 |
| Audit | `--audit` | 既存 E2E テストがある場合 |
| Flow | `--flow <name>` | 特定 User Flow のテストを追加する場合 |

Flag なしで呼び出すと、ファイルシステムの状態から自動判別します。

## 出力物

- `playwright.config.ts` — 環境変数ベースの baseURL 設定
- `e2e/*.spec.ts` — Critical path ごとのテストファイル
- `.github/workflows/e2e.yml` — CI Workflow（`--ci` または `--init` 時）
- Audit report — Coverage ギャップと Flaky リスク分析

## 関連 Skill

- `ywc-gen-testcase` — 手動検証 Testsheet 生成（自動化ではなく人間が確認）
- `ywc-impl-review` — コードレベルの実装レビュー
- `ywc-security-audit` — 認証・入力処理のセキュリティ監査
