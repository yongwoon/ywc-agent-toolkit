# ywc-infra-optimize

既に Provision された Infrastructure を改善する Skill です — Cost Right-Sizing、未使用 Resource の削除、Reserved/Spot への移行、Drift 検知と Remediation、Reliability Hardening を扱います。`ywc-refactor-clean` の SAFE/CAUTION/DANGER Tier 判定と Iron Law (3重 Witness) の原則を Infrastructure に適用した Safe Change-Loop Skill です。Cost/Utilization Signal は `ywc-performance-engineer` Persona を持つ Codex Worker が収集し、SAFE Item の実行は `ywc-cloud-engineer` Persona を持つ Codex Worker に Dispatch されます。CAUTION/DANGER Item は絶対に自動実行せず、Escalate のみ行います。Terraform が本 toolkit で唯一固定された IaC Tool であり、すべての実行は `terraform plan` までで、`apply` は行いません。

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [한국어 (요약 / summary)](./README.ko.md)

## 使うべき場面

- User が "インフラ最適化", "optimize infrastructure", "cost optimization", "right-sizing", "terraform drift", "인프라 개선해줘", "비용 최적화해줘" と言及した場合
- `ywc-infra-review` が発見した Cost/Drift/Reliability Finding を実際に Remediation したい場合
- 定期的な Infrastructure 最適化(コスト削減、未使用 Resource 整理) を行いたい場合

## 起動方法

```bash
$ywc-infra-optimize --scope infra/modules/compute
```

または自然言語で:

> 「未使用リソースを整理して」
> 「このインスタンスを right-sizing して」

## 入力

- (optional) `--scope <path>` — IaC Tree 全体ではなく単一の Terraform Module/Path に範囲を限定
- (optional) `--dry-run` — Gather+Classify のみ実行し、SAFE Item を実行せず Report のみ出力
- (optional) `--skip-verify-done` — 締めの `ywc-verify-done` Handoff を省略 (Upstream Caller が既に Verify を実行済みの場合のみ有効)

## 出力

- Drift/Cost/Utilization Signal に基づく SAFE/CAUTION/DANGER 分類 Report
- SAFE Item は Item ごとに 1 Commit で実行 (Bisectable)
- CAUTION/DANGER Item は実行せず Escalate のみ実施
- `ywc-verify-done` 形式の最終 Verification Block

## 関連 Skill

- `ywc-infra-review` — upstream。本 Skill が Remediation する Cost/Drift/Reliability Finding を診断
- `ywc-verify-done` — downstream。最終 Verification Claim
- `ywc-iac-author` — Escalate された CAUTION/DANGER Item の再作成経路
- `ywc-performance-engineer` / `ywc-cloud-engineer` Persona — それぞれ Cost/Utilization Signal 収集と SAFE Item 実行を担当する Worker
- `ywc-infra-design` — Greenfield Infrastructure 設計担当 (既存 Infrastructure の改善ではない)
- `ywc-refactor-clean` — 本 Skill が援用した SAFE/CAUTION/DANGER Iron Law の元祖 (Application Code 対象)
