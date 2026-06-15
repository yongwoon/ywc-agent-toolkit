# ywc-spec-ready (Spec Readiness Loop)

`ywc-plan` が生成した spec を `ywc-spec-validate` の `DONE` 状態まで自動的に収束させる Skill です。各 iteration で `ywc-spec-validate` を実行し、`DONE_WITH_CONCERNS` の場合は `ywc-plan --update-spec` で amendment を追加して再検証します。`DONE` に到達すると `ywc-task-generator` への handoff 案内のみを出力して**停止**します（task-generator を自動実行しません）。

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

既存の `ywc-agentic` の loop は `ywc-impl-review`（コード評価）を中心に回り、`ywc-spec-validate` を**1回のみ**実行します。この Skill はその欠けている inner loop ——**複数回の spec 収束**—— を担います。

## 使い方

```text
/ywc-spec-ready --spec docs/ywc-plans/feature.md                       # デフォルト (max 5 iteration)
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-iterations 8    # 反復上限を指定
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-advisor-calls 2 # advisor cost guard
/ywc-spec-ready --spec docs/ywc-plans/feature.md --dry-run             # command sequence のみ出力
```

## Option

| Option                   | 説明                                                              |
| ------------------------ | --------------------------------------------------------------- |
| `--spec <path>`          | 収束対象の spec ファイル（必須、`ywc-plan` の成果物）。不在時は `NEEDS_CONTEXT` |
| `--max-iterations <n>`   | Validation loop の上限 (default: 5、自動増加しない safety valve)    |
| `--max-advisor-calls <n>`| 全 iteration 累積の Opus advisor budget (default: 4、cost guard)  |
| `--log <path>`           | append-only loop log (default: `<spec-dir>/<slug>.spec-ready-log.md`) |
| `--dry-run`              | 計画された command sequence のみ出力、sibling skill を呼び出さない |
| `--lang <lang>`          | Report/handoff の言語 (default: auto、CLAUDE.md から推論)         |
| `--focus <area>`         | `ywc-spec-validate` へ転送                                        |
| `--format <fmt>`         | `ywc-spec-validate` へ転送 (markdown / html)                      |
| `--terse`                | 最小出力（phase header と最終 report のみ）                        |

## 実行フロー

1. Pre-flight —— `--spec` の存在確認、`<slug>` の導出、`--dry-run` 分岐
2. Iteration Loop —— `ywc-spec-validate` → Status Routing →（DONE_WITH_CONCERNS 時）guard 評価 → `ywc-plan --update-spec` → log → 反復
3. Hard Stop —— `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / parse 不能 時に即停止
4. Handoff —— `DONE` 到達時に `ywc-task-generator` の案内を出力して停止
5. Completion Report —— 単一 report（最終行は Completion Status）

## 無限 loop 防止ガード

| ガード | 停止条件 |
| --- | --- |
| Iteration cap | `iteration >= --max-iterations` かつ status ≠ DONE |
| 非減少 Critical | Critical 増加、または 2 連続 iteration で非減少（signature overlap） |
| 同一 signature 再出現 | 同一 Critical signature が re-plan 後に連続出現 |
| 同一 amendment scope | 新しい amendment scope が直前と同一（recursion guard） |

詳細なルールは [references/convergence.md](references/convergence.md)、log schema は [references/loop-log.md](references/loop-log.md) を参照。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
