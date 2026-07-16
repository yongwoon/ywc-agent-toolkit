# ywc-auth-implement

認証機能(email/password、OAuth、MFA、shallow RBAC)の実装を標準化する skill です。Policy Interview → Stack 検出 → battle-tested な Library/managed Service の動的推薦 → `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer` への dispatch という orchestration を行い、実際の application 認証 code はこの skill 自身では作成しません。

## 使用シナリオ

- ユーザーが「認証実装」「ログイン機能を追加して」「OAuth連携」と発言したとき
- 新規プロジェクトに email/password または OAuth ベースの認証を初めて導入するとき
- 既存の認証を拡張・移行する必要があるとき(`new`/`extend`/`migrate` の選択が必要)

## 使用方法

```bash
/ywc-auth-implement
```

または自然言語で呼び出す:

> 「認証を実装して」

## Input

- 必須: 対象プロジェクトの Framework/Database の根拠(自動検出、不足時は `ywc-tech-research` へ routing)
- 必須: Policy Interview 9カテゴリに対するユーザーの回答(手段/MFA/session/password/profile/退会/RBAC/consent/abuse防止)
- (任意) 既存認証が検出された場合の `new`/`extend`/`migrate` 選択

## Output

- Preflight 結果、Policy Interview の要約、推薦 Library/Service、dispatch された Subagent 一覧、Security/E2E Gate 結果、`## Output Format` の 4値 Completion Status(`DONE`/`DONE_WITH_CONCERNS`/`BLOCKED`/`NEEDS_CONTEXT`)

## 関連 Skill

- `ywc-backend-coder` / `ywc-frontend-coder` — TDD 規律下での実装 dispatch 対象
- `ywc-doc-writer` — 法的レビュー前の暫定版 ToS/Privacy Policy 草案の dispatch 対象
- `ywc-security-audit` / `ywc-e2e-test-strategy` — 実装後の Security/E2E Gate
- `ywc-tech-research` — Stack の根拠不足時のリアルタイムリサーチ routing
