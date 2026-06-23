# ywc-project-mission

Project の durable な Mission / North-Star、測定可能な Success Criteria、Out-of-Scope non-goal を `docs/project-mission.md` という commit 可能な Markdown ファイルに永続化する Skill です。`ywc-review-learnings` と同じ stateful-file architecture（特定 runtime 非依存）に従い、`ywc-plan` が新しい request を clarify する前にこのファイルを読み込み、すべての planning session を同じ north-star で framing します。

要点は、feature が終われば破棄される一回限りの plan と異なり、Mission はどの単一 feature よりも長く生き残る *durable* な意図を記録する点です。各 entry は provenance と date を残すため、現在の commitment と破棄された方向を区別できます。

## 対応 Mode

- **read** — Mission を読み込んで planning を framing（通常 `ywc-plan` が呼び出す）
- **update** — 確認済みの source から Mission / Success Criteria / non-goal を capture・修正
- **list** — 現在の Mission を表示
- **curate** — stale または superseded な entry を deprecate（hard-delete 禁止）

## 使用シナリオ

- Brainstorm で整理した Mission（What+Why）と Success Criteria（Done When）を Project 単位で永続化したいとき
- 毎回の planning で north-star を再導出せず、`ywc-plan` が同じ Mission で質問と Acceptance Criteria を framing するようにしたいとき
- 「これはこの Project が決してやらない」という durable な non-goal を明示的に残したいとき
- LLM が Project Mission を自動的に理解するよう CLAUDE.md に `@docs/project-mission.md` 参照を追加したいとき

## 使い方

```bash
/ywc-project-mission
```

または自然言語で呼び出し:

> "この Project Mission を覚えておいて"
> "Success Criteria を整理して"
> "現在の Project Mission は何だった?"

## 入力

- (任意) `--mode read|update|list|curate` — Mode を強制指定（省略時は自動判定）
- (任意) `--source brainstorm|plan` — update 時の Mission/criterion の出所 provenance（既定 `brainstorm`）
- (任意) `--output <path>` — Mission ファイル path（既定: `docs/project-mission.md`）
- (任意) `--dry-run` — 書き込みせず CHANGESET のみ表示

## 出力

- `docs/project-mission.md` — Mission / North-Star、Success Criteria table（`ID | Criterion | Source | Added | Status`）、Out of Scope、自動管理される Change Log
- update 時: ADD / MODIFY / DEPRECATE CHANGESET を確認後、確定 entry のみ記録し、`Mission updated` 確認 block を出力
- 初回ファイル作成時: CLAUDE.md に `@docs/project-mission.md` 追加を促す activation 案内を 1 回出力
- 同一内容での再実行時（idempotent）: 空の CHANGESET → ファイル書き込みなし、date bump なし

## 他の Skill との関係

- `ywc-brainstorm` — Step 6 Handoff で Mission（What+Why）と Success Criteria（Done When）を `update --source brainstorm` で永続化を提案（opt-in）
- `ywc-plan` — Step 1 で read mode で Mission を読み込み、質問と Acceptance Criteria を framing
- `ywc-review-learnings` — 同じ per-project stateful-file architecture（read/update/list/curate、ユーザー確認後に書き込み）、異なる domain（durable な意図 vs review 選好）
- `ywc-ubiquitous-language` — domain *語彙* を管理。この Skill は domain *意図* を保存（混同注意）
