# ywc-review-learnings

Project ごとの Code Review の好みを蓄積し、Review 品質を時間とともに高める Skill です。CodeRabbit の "learnings" の概念を runtime 非依存（特定 bot なしでも動作）の形で実装し、commit 可能な Markdown ファイル `docs/review-learnings.md` として管理します。`ywc-impl-review` が Review の直前にこのファイルを読み込んで適用します。

最も重要な性質は、各 learning が *何を（what）* だけでなく **なぜ（why）** まで記録する点です。Why があることで、類似するが同一ではない状況にも一般化でき、単なる keyword match に陥りません。

## 対応 Mode

- **read** — Review 対象の glob に一致する learning を読み込み Reviewer に注入
- **update** — feedback / 完了した review / PR bot comment から新規 learning を捕捉
- **list** — 現在の learning 一覧を表示
- **curate** — 古い・矛盾する learning を deprecate（hard-delete は禁止）

## 利用シナリオ

- Review で出た false positive を「この環境では問題ない」と学習させ、次回以降の再指摘を防ぎたいとき
- 繰り返される指摘（例: ownership-scoped query の owner-key 欠落）を先回りで捕捉する rule として蓄積したいとき
- CodeRabbit / Codex の PR comment のうち受け入れたものを internal review に取り込みたいとき
- Codex session が Project ごとの review の好みを自動的に理解するよう、AGENTS.md または CODEX.md に `docs/review-learnings.md` 参照を追加したいとき

## 使い方

```text
Use $ywc-review-learnings to update the project review learnings.
```

または自然言語で呼び出し:

> 「これは false positive だから学習しておいて」
> 「この path に適用される review learnings を読み込んで」
> 「PR #128 の CodeRabbit コメントを review 学習として残して」
> 「review learnings を整理して」

## 入力

- (任意) `--mode read|update|list|curate` — Mode を強制指定（省略時は自動判定）
- (任意) `--target <glob|path...>` — Review 対象 path
- (任意) `--source feedback|review|pr` — update 時の learning の出所（既定 `feedback`）
- (任意) `--pr <番号>` — `--source pr` と併用する bot comment harvest 対象 PR
- (任意) `--output <path>` — learning ファイル path（既定: `docs/review-learnings.md`）
- (任意) `--dry-run` — 書き込みせず CHANGESET のみ表示

## 出力

- `docs/review-learnings.md` — `ID / Scope / Category / Polarity / Rule / Why / Provenance` の Table
- update 時: 変更内容を明示する `Learnings added` 確認 block を出力
- ファイル初回作成時: AGENTS.md または CODEX.md に `docs/review-learnings.md` を読む project instruction の追加を勧める activation 案内を出力

## 出力例

```markdown
# Review Learnings — ShopBot

<!-- updated: 2026-06-13 -->

## Learnings

| ID   | Scope          | Category | Polarity       | Rule | Why | Provenance |
|------|----------------|----------|----------------|------|-----|-----------|
| L001 | `**/*.sql`     | Security | DO             | ownership-scoped table の全 query は owner-key 条件を明示する | App-layer filtering は query が WHERE owner_id=? を一つ忘れた瞬間に fail-open する | PR#42, 2026-06-13 |
| L002 | `**/*.test.ts` | Test     | FALSE-POSITIVE | test setup ファイルの top-level await を missing-await bug として指摘しない | runner が対応しており指摘は noise | dismissed PR#51, 2026-06-13 |
```

## 関連 Skill

- `ywc-impl-review` — Review 直前に read mode で呼び出し、Review 後に update mode で学習を蓄積
- `ywc-handle-pr-reviews` — dismiss された bot comment を `update --source pr` に流せる
- `ywc-ubiquitous-language` — 同一の per-project 知識ファイル architecture、異なる content 領域
- `ywc-receive-review` — Review feedback に *対応* する discipline。この Skill はその feedback が残した *持続的な教訓* を保存する
