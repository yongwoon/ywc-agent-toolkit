# ywc-infra-design

Cloud/Infrastructure Architecture を設計する Skill です。IaC を一行でも書く前に、Requirements Gathering、Provider 選定、Network/Compute/Storage/IAM Topology 設計、Reliability/Cost/Security 3-lens Pre-check を行い、すべての主要な Trade-off を ADR(Architecture Decision Record) 形式で記録した上で、`ywc-iac-author` が読み込む Input Contract である `infra-design.md` を産出します。本 Skill は IaC を直接作成しません — 本 toolkit では **Terraform が唯一固定された IaC Tool** であり、実際の `.tf` 作成は `ywc-iac-author` の役割です。

## Localized Versions

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [한국어](./README.ko.md)

## 使うべき場面

- User が "インフラ設計", "クラウド構成", "infra design", "cloud architecture", "design the infrastructure", "인프라 설계해줘" と言及した場合
- 新しい Feature/Service のために Infrastructure を最初から設計する必要がある場合
- Provider がまだ決定しておらず比較が必要な場合 (`ywc-tech-research` へ delegate)
- 既存の `infra-design.md` なしにいきなり `ywc-iac-author` へ進むことを避けたい場合

## 起動方法

```bash
$ywc-infra-design --provider aws
```

または自然言語で:

> 「この Service の Infrastructure を設計して」
> 「payments-api のクラウドアーキテクチャを設計して」

## 入力

- (optional) `--provider <aws|gcp|azure|k8s>` — 既に決定済みの Provider を明示し、`ywc-tech-research` への delegation (Step 2) を省略
- (optional) `--scope <system-name>` — Architecture 全体ではなく単一の Service/System に設計範囲を限定
- (optional) `--skip-cloud-consult` — Step 3 の read-only `ywc-cloud-engineer` Persona feasibility consult を省略

## 出力

- `infra-design.md` — Requirements / Provider Decision / Topology (Network/Compute/Storage/IAM) / 3-Lens Pre-Check Results / ADR Log で構成された Input Contract 文書
- `ywc-iac-author` が Step 1 でそのまま読み込める完結した設計成果物

## 関連 Skill

- `ywc-tech-research` — upstream。Provider が未決定の場合の比較を担当し、本 Skill に結果を供給
- `ywc-iac-author` — downstream。本 Skill が産出した `infra-design.md` を読み込み実際の Terraform を作成
- `ywc-infra-review` — downstream。作成済みの IaC をレビュー (本 Skill はまだ作成されていない Infrastructure を設計)
- `ywc-cloud-engineer` — Step 3 の read-only topology feasibility consult (authoring ではない)
- `ywc-project-scaffold` — Source Code Folder Layout 担当 (Infrastructure Architecture ではない)
- `ywc-docker-isolate` — Local Worktree の Docker Port 分離専用、Production Infrastructure ではない
