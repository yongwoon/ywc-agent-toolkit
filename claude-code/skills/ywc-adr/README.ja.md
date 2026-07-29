# ywc-adr

Projectの Architecture Decision Record(ADR)を管理する Skill です。元に戻しにくく、Context なしでは意外に見え、実際の trade-off の結果であるアーキテクチャ決定を、`docs/adr/NNNN-<slug>.md` — 決定ひとつにつきファイルひとつ、immutable-ish な形式で記録します。`ywc-review-learnings` / `ywc-project-mission` と同じ stateful-file family に属しますが、保存形式は異なります — 蓄積される単一ファイルではなく、決定ごとに独立したファイルです。

これまで `ywc-plan` の Step 3.5(Architectural Advisor Gate)が下す判断は、その plan の `architecture-verdict.md` にのみ残り、そこで消えていました。3つの基準(元に戻しにくい + Context なしでは意外 + 実際の trade-off)を満たす決定であれば、この Skill がその判断を `ADR-0007` のような安定した ID で引用できる記録として残します。

## 対応 Mode

- **new** — 新しい決定を記録(必要に応じて既存 ADR を supersede)
- **read** — Planning/Review のために関連する ADR を要約して読み込み
- **list** — 全 ADR とその Status を一覧表示
- **curate** — 後続 ADR がないまま Context が失われた ADR を Deprecated にする

**Family との意図的な違い:** `docs/review-learnings.md` や `docs/project-mission.md` と異なり、この Skill は `@docs/adr/` 形式の CLAUDE.md 自動読み込み案内を出力しません。単一ファイルは毎セッション事前読み込みしてもコストが低い一方、ADR ディレクトリは際限なく増え、多くは現在のリクエストと無関係だからです。代わりに `read` mode で必要な時に `--target` で絞り込んで読み込みます。

## 使用シナリオ

- `ywc-plan` Step 3.5 の architecture verdict が 3 つの基準を満たした時、その判断を durable な ADR として残したい時
- 過去の決定を覆す新しい決定を下し、なぜ方向転換したのか記録を残したい時(supersede)
- 新しい spec を書く前に、既に確定したアーキテクチャ決定と矛盾しないか確認したい時
- もはや有効でない古い ADR を整理したい時

## 使用方法

```bash
/ywc-adr
```

または自然言語で呼び出し:

> "この決定を ADR として記録して"
> "どんな ADR がある?"
> "ADR-0004 はもう有効じゃないから整理して"

## 入力

- (任意) `--mode new|read|list|curate` — Mode を強制指定(省略時は自動判定)
- (任意) `--supersedes <ADR-NNNN>` — `new` mode で置き換える既存 ADR
- (任意) `--target <path|area>` — `read` mode で ADR に記録された `Scope` フィールドがこの path/area と重なるかで絞り込み(Scope 未記録の ADR は `repo-wide` として扱う)
- (任意) `--source plan|manual` — 決定の出所(デフォルト `manual`)
- (任意) `--output <ディレクトリ>` — ADR ディレクトリのパス(デフォルト: `docs/adr/`)
- (任意) `--dry-run` — 書き込みせず CHANGESET のみ表示

## 出力

- `docs/adr/NNNN-<slug>.md` — Title / Status / Date / Provenance / Scope と Context / Decision / Alternatives Considered / Consequences セクションを備えたファイル
- `new` mode 時: 新しい ID(該当する場合は superseded ID も)を明示する `ADR recorded` 確認 block を出力
- `curate` mode 時: deprecate した各 ID とその理由を明示する `ADR curated` 確認 block を出力
- CLAUDE.md 自動読み込み案内は出力しない(意図的 — 上記参照)

## 出力例

```markdown
# ADR-0007: Deliver webhooks asynchronously via a queue

**Status:** Accepted
**Date:** 2026-07-29
**Provenance:** ywc-plan Step 3.5, plan docs/ywc-plans/webhook-delivery.md

## Context
...

## Decision
We will deliver webhooks through a durable queue, not inline in the request handler.

## Alternatives Considered
- Synchronous delivery with a timeout — rejected because ...
- Third-party delivery service — rejected because ...

## Consequences
...
```

## 関連 Skill

- `ywc-plan` — Step 3.5(Architectural Advisor Gate)がこの Skill の `new --source plan` を opt-in で提案し、Step 2 が `read` mode で既存 ADR と矛盾しないか確認
- `ywc-architect` — この Skill が記録する trade-off 判断を作り出す read-only advisor(自身では保存しない)
- `ywc-review-learnings` / `ywc-project-mission` — 同じ stateful-file family(ユーザー確認後に書き込み、ファイル不在時も無停止)、異なるドメインと保存形式
