# Mine Review History

すでに Merge された複数の PR を対象に Bot Review Comment（CodeRabbit / Codex Review / Claude Review）を一括で収集し、繰り返し出現する欠陥 Class を学習候補として提示する Claude Code Skill です。

## 概要

`ywc-review-learnings --mode update --source pr` は単一 PR を On-demand で扱い、`ywc-incident-postmortem` は単一 Incident のみを扱います。どちらの Skill も、導入以前に蓄積された PR History を遡って調査する経路を持っていませんでした。この Skill はその欠落を埋めます。

指定した範囲（件数または日付）の Merge 済み PR から Bot Comment を収集し、既存の `--source pr` 経路と同じ規則で各 Comment を Accept/Dismiss に分類します。分類された Comment は欠陥 Class 単位でまとめられ、`--min-recurrence`（既定値 3）以上の異なる PR にまたがって繰り返された Class のみを `ywc-review-learnings --mode update --source pr` へ昇格候補として渡します。`docs/review-learnings.md` はこの Skill が直接書き込むことはなく、昇格は必ず対象 Skill の確認 Gate を経由します。

### 主な機能

- `--limit` / `--since` で Scope を制限 — 無制限の既定 Scan は提供しない
- 既存の Accept/Dismiss 分類規則を Batch 規模にそのまま適用
- 反復の集計単位は Comment 数ではなく **異なる PR 数**
- 閾値未満の Class も Report には常に含まれる（省略なし）
- 実行のたびに調査 PR 数・収集/分類済み Comment 数・発見/昇格した欠陥 Class を Report

## 使い方

```text
/ywc-mine-review-history --limit 50
/ywc-mine-review-history --since 2026-01-01
/ywc-mine-review-history --limit 50 --min-recurrence 4
```

自然言語 Trigger は [SKILL.md](./SKILL.md) を参照してください。

## 前提条件

- `gh` CLI がインストールされ、認証済みであること
- `--limit` または `--since` のいずれか一方は必須

## 多言語版

- [English](./README.en.md)
- [Korean (Primary)](./README.md)
- [Korean](./README.ko.md)
