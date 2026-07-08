# ywc-iac-author

Infrastructure-as-Code 作成 Skill です。Infrastructure 設計 (`ywc-infra-design` の成果物) または明示的に整理した inline intent を基に Terraform を作成し、Module 単位で `ywc-cloud-engineer` Persona を持つ Codex Worker へ Dispatch した後、`terraform validate` / `terraform plan` で検証し、apply 前に blast-radius summary を報告します。本 toolkit では **Terraform が唯一固定された IaC Tool** であり、Kubernetes/Helm Resource も Terraform の `kubernetes` / `helm` Provider で表現します — raw manifest や別の IaC Tool は使用しません。

## Localized Versions

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [한국어](./README.ko.md)

## 使うべき場面

- User が "IaC 作成", "terraform 作成", "インフラコード", "write terraform", "provision infrastructure", "IaC を書いて" と言及した場合
- `ywc-infra-design` の成果物 (`infra-design.md`) が準備済みで、実際の Terraform に落とし込む必要がある場合
- 小規模で理解度の高い Infrastructure 変更のため、別途 設計 Phase を経ずに inline intent でそのまま進めたい場合

## 起動方法

```bash
$ywc-iac-author --design-doc infra-design.md
```

または自然言語で:

> 「この設計を基に Terraform を作成して」
> 「network Module の IaC を作成して」

## 入力

- (optional) `--design-doc <path>` — 作成の基準とする `ywc-infra-design` の成果物。省略時は inline intent 確認に切り替え
- (optional) `--scope <module-path>` — 特定の Terraform Module に作成範囲を限定 (default: 設計から導出される全 Module)
- (optional) `--skip-review-recommendation` — 上位 caller が `ywc-infra-review` を別途スケジュールする場合のみ有効

## 出力

- Dispatch ごとに作成された Terraform Module — それぞれ `terraform validate` clean、`terraform plan` 完了
- IaC Authoring Report — blast-radius summary (add/change/destroy、stateful Resource への destructive change を明示)、state 取り扱い確認、Secret 外部化チェック
- `apply` 前の `ywc-infra-review` 実行推奨 (skip していない場合)

## 関連 Skill

- `ywc-infra-design` — upstream。本 Skill が読み込む `infra-design.md` を産出
- `ywc-cloud-engineer` — 各 Terraform Module を作成・検証する Worker Persona
- `ywc-infra-review` — downstream。Apply 前の推奨レビュー
- `ywc-infra-optimize` — 既存 Infrastructure の コスト/right-sizing 改善 (本 Skill の範囲外)
- `ywc-backend-coder` — Application Server / Business Logic (Infrastructure ではない)
- `ywc-docker-isolate` — Local Worktree の Docker Port 分離専用、Production Infrastructure ではない
