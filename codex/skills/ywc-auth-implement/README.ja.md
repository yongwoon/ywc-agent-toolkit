# ywc-auth-implement

認証の意図を、ポリシー・セキュリティ監査・E2E ゲート付きの実装経路へ変換する Codex オーケストレーション Skill です。シークレットを出力したり、JWT・パスワード・暗号処理を自作するよう勧めたりしません。

## 使用するとき

- ログイン、OAuth、セッション、アカウント削除を計画するとき
- 既存認証を `new`、`extend`、`migrate` のどれにするか決めるとき
- プロジェクトの証拠から実績あるライブラリまたは管理サービスを選ぶとき

## 実行

```text
$ywc-auth-implement
```

読み取り専用の事前確認と 9 セクションのポリシー面談の後、次の経路を表示するだけで、自動実行はしません。medium/large の作業では `$ywc-spec-ready` が `DONE` になって初めて表示します。

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Critical/High の監査結果では E2E、PR 提案、キャッシュを省略し、remediation と再監査が完了するまで経路は `DONE_WITH_CONCERNS` のまま終了します。法務文書は常に `법적 검토 전 임시본` と表示します。
