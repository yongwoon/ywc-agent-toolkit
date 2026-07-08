# ywc-infra-optimize

既に Provision された Infrastructure を改善するための保守的な planning Skill です — Cost Right-Sizing、未使用 Resource の削除、Reserved/Spot への移行、Drift 検知、Reliability Hardening を扱います。`ywc-refactor-clean` の SAFE/CAUTION/DANGER Tier 判定と Iron Law (3重 Witness) の原則を Infrastructure に適用しますが、Codex v1 では直接実行せず、分類と handoff のみを行います。Cost/Utilization Signal は `ywc-performance-engineer` Persona を持つ Codex Worker が収集し、必要に応じて read-only `ywc-cloud-engineer` Persona に feasibility / blast-radius advisory を依頼します。実際の Terraform 修正は `ywc-iac-author` に渡し、すべての分析は `terraform plan` までで、`apply` は行いません。

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
- SAFE Item についても実際の修正ではなく狭い次アクションを提案
- CAUTION/DANGER Item は実行せず Escalate のみ実施
- `ywc-verify-done` 形式の最終 Verification Block

## 関連 Skill

- `ywc-infra-review` — upstream。本 Skill が Remediation する Cost/Drift/Reliability Finding を診断
- `ywc-verify-done` — downstream。最終 Verification Claim
- `ywc-iac-author` — Escalate された CAUTION/DANGER Item の再作成経路
- `ywc-performance-engineer` / `ywc-cloud-engineer` Persona — それぞれ Cost/Utilization Signal 収集と read-only feasibility/blast-radius advisory を担当する Persona
- `ywc-infra-design` — Greenfield Infrastructure 設計担当 (既存 Infrastructure の改善ではない)
- `ywc-refactor-clean` — 本 Skill が援用した SAFE/CAUTION/DANGER Iron Law の元祖 (Application Code 対象)
