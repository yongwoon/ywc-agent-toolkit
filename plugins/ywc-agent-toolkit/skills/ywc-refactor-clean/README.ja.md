# ywc-refactor-clean

Detection tool (knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps) を起点とした dead code 削除 Skill です。Finding を SAFE / CAUTION / DANGER の三段 tier に分類し、各 item ごとに Test を実行してから commit します。Behavior 変更 (例えば duplicate consolidation の際に semantics の摺り合わせが必要なケース) は本 Skill の scope 外で、`ywc-tdd-ritual` + `ywc-code-gen` へ routing します。

## Localized Versions

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [한국어](./README.ko.md)

## 使うべき場面

- User が "dead code を消して" "knip を回して" "unused import を整理して" と言及した場合
- Sprint 終了後、monthly cleanup branch を切るとき
- `ywc-onboard-repo` が新規 repo 進入時、prior dead-code accumulation により architecture 把握が阻害される場合

## 起動方法

```bash
$ywc-refactor-clean --scope src/ --tier safe
```

または自然言語で:

> 「dead code を整理して」
> 「knip の結果を見て安全なものから消して」

## Iron Law

**3 つの witness なしに deletion しないこと** — (1) detection tool が flag、(2) grep で reference が 0、(3) 各 batch 後に Test が green。

## 入力

- (optional) `--scope <dir>` — detection / deletion の対象 path (default: repo root)
- (optional) `--tier safe | safe+caution | all` — どの tier まで進めるか (default: `safe`)
- (optional) `--dry-run` — report のみ出力、ファイルは変更しない
- (optional) `--skip-verify-done` — 上位 caller が verify-done を別途実行する場合のみ有効

## 出力

- Per-item 1-commit シリーズ (`chore(cleanup): remove unused <symbol> (knip)`)
- 最終 Verification Report (Output Format — `ywc-verify-done` の evidence block 形式を内包)
- DANGER tier に分類された item の一覧 (別 PR を推奨)

## 関連 Skill

- `ywc-verify-done` — Step 7 の mandatory handoff、PASS / FAIL evidence block format を提供
- `ywc-tdd-ritual` — consolidation が behavior 変更を伴う場合の routing 先
- `ywc-code-gen` — behavior 変更を伴う cleanup は本 Skill ではなくこちら
- `ywc-confidence-gate` — 境界事例 (CAUTION ↔ DANGER) を 5-次元 rubric で判定
- `ywc-onboard-repo` — 新規 repo 進入後の hygiene pass 起点 (upstream caller)
