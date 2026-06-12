# ywc-plan

Rough idea を実装直前の状態(Small path の直接実行 plan、または Medium/Large path の spec document)に変換する事前 planning Skill です。Scale を自動判定し、適切な downstream Skill に routing します。

## 使用シナリオ

- ユーザーが "この feature の計画を立てて" と言ったとき
- Spec も task もまだなく、どこから始めればよいか分からないとき
- Small な変更なのか、Spec を書くべき変更なのかを判断したいとき
- `ywc-task-generator` の input となる spec を準備するとき

## 使用方法

```bash
/ywc-plan "<rough request>"
```

または自然言語で呼び出し:

> "Profile ページに通知設定を追加したいので、計画を立ててください"

## 入力

- 自然言語の変更要求 (rough idea, feature request, change description)

## 出力

Scale に応じて以下のいずれか:

| Scale | Output |
|---|---|
| Small | `./plan.md` — 直接実行可能な single-PR の計画書 |
| Medium / Large | `docs/ywc-plans/<slug>.md` — `ywc-spec-validate` と `ywc-task-generator` が消費する spec document |

各 path で明示的な handoff message が出力されます。

## 動作 Flow

1. **Clarify** — What / Why / Out of Scope / Done When の 4 つの anchor を一度に質問
2. **Investigate** — `AGENTS.md` / `CODEX.md` / `CLAUDE.md`, `package.json`, `docs/architecture/` などの essential file のみ read
3. **Assess Scale** — Small / Medium / Large から 1 つ選択 (曖昧なら Medium default)
4. **Branch** — Small なら `plan.md`、Medium/Large なら spec document を作成
5. **Handoff** — 次の Skill を明示的に表示 (実行は user が決定)

## Safety Invariants

以下のいずれかに該当する場合、自動で Medium 以上に escalate します:

- Database migration / schema 変更
- 新しい library / framework の導入
- 外部に公開される API contract の新設
- Authentication / authorization logic の変更
- 2 modules 以上にまたがる cross-cutting 変更

## 関連 Skill

- `ywc-tech-research` — Technology 選択が未定の場合、ywc-plan より先に
- `ywc-product-review` — Product / business の framing が不明確な場合、ywc-plan より先に
- `ywc-spec-validate` — Medium/Large path の次の step
- `ywc-task-generator` — Spec review 通過後の task 分解
- `ywc-code-gen` — Small path の直接実行 option
- `ywc-sequential-executor` / `ywc-parallel-executor` — Task 分解後の実行

## Triggering

この Skill の trigger 条件は [SKILL.md](./SKILL.md) の `description` field に定義されています。

## Localized Versions

- [Korean (default)](./README.md)
- [English](./README.en.md)
