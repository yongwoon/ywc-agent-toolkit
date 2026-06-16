# ywc-receive-review

Code review feedback を受け取った時に **performative agreement を遮断し、技術検証を強制** する attitude-layer discipline skill です。

## 何をするか

次の Iron Law を強制します:

> **VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.**

すべての reviewer comment に対して 6 段階の Response Pattern を順に実行します。

1. **READ** — 反応せずに全 feedback を読む (同意・反論・実装 tool 呼び出しはまだ無し)
2. **UNDERSTAND** — 技術要件を自分の言葉で再述。不明な項目があれば実装前に質問
3. **VERIFY** — File を開く / test を走らせる / grep で reviewer の主張を現状 codebase で確認
4. **EVALUATE** — この codebase の現状で suggestion が成立するか (互換性・既存決定・YAGNI・platform 制約)
5. **RESPOND** — Fix の文で acknowledge するか、技術的根拠で push back。**禁止**: 「You're absolutely right!」「Great point!」「Thanks!」
6. **IMPLEMENT** — 1 項目ずつ、それぞれ test、`ywc-verify-done` の verification block を surface

**禁止語彙** (full list は references/forbidden-acknowledgments.md):

| 禁止 | 代替 |
|---|---|
| "You're absolutely right!" | Fix を直接述べる: "Fixed — `<file:line>` now <behavior>" |
| "Great point!" / "Excellent feedback!" | 行動を述べるか質問を surface |
| "Thanks for catching that!" / "Thanks for the review!" | 削除。Fix そのものが感謝の表現 |
| "Let me implement that right now" (Step 3 前) | "Verifying before implementing: <check>" |

## いつ trigger されるか

- ユーザーが「リビュー受信」「review feedback」「コメント返信」などを言及した時
- `ywc-handle-pr-reviews` が inline-comment iteration で委任してきた時
- `ywc-finish-branch` post-CI bot review が応答を要求する時
- CodeRabbit / Codex Review / Claude Review への返信直前

## 使わない場面

- 自分が review する → `ywc-impl-review`
- PR を作る → `ywc-create-pr`
- PR comment fetch / threading / 返信の自動化 → `ywc-handle-pr-reviews` (この skill の attitude layer を呼び出す側)
- 完了 claim 検証 → `ywc-verify-done`

## 参考

詳細な Response Pattern、forbidden-acknowledgment list、pushback 条件、source-specific handling (human partner / external reviewer / bot) は [SKILL.md](./SKILL.md) を参照してください。元の process discipline は `superpowers:receiving-code-review` を参考にしつつ、`ywc-handle-pr-reviews` との関心分離 (attitude vs automation) に合わせて調整しています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)
