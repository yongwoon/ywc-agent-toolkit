# ywc-infra-review

既に作成された IaC / Cloud Configuration を Apply する前にレビューする Skill です。Security(オコンフィグ・Least-Privilege)/Cost(Right-Sizing・無駄)/Reliability(SPOF・Backup・Health) の 3-lens に Fan-out し、それぞれ `ywc-security-engineer`、`ywc-performance-engineer`、`ywc-cloud-engineer`(Review Mode) の Persona を持つ Codex Worker に Dispatch した上で、すべての Finding を Severity(Critical/High/Medium/Low)で取りまとめます。CRITICAL/HIGH の Finding が見つかった場合は Apply の Blocking を推奨します。本 Skill は IaC を直接作成・修正しません — Terraform が本 toolkit で唯一固定された IaC Tool であり、AWS/GCP/Azure/K8s は Terraform Provider として扱われます。

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [한국어 (요약)](./README.ko.md)

## 使うべき場面

- User が "インフラレビュー", "infra review", "review my terraform", "IaC review", "인프라 리뷰해줘", "terraform 검토해줘" と言及した場合
- `ywc-iac-author` で作成された Terraform を Apply する前に オコンフィグ/コスト/信頼性を点検したい場合
- 既に Provision された Infrastructure の Security Group、IAM Policy、Public Exposure を点検したい場合

## 起動方法

```bash
$ywc-infra-review --scope infra/modules/network
```

または自然言語で:

> 「この Terraform の変更をレビューして」
> 「payments-api インフラの Security Group と IAM を点検して」

## 入力

- (optional) `--scope <path>` — IaC Tree 全体ではなく単一の Terraform Module/Path にレビュー範囲を限定
- (optional) `--skip-optimize-recommendation` — 締めの `ywc-infra-optimize` 推奨を省略 (Upstream Caller が既に Remediation をスケジュール済みの場合のみ有効)

## 出力

- Security/Cost/Reliability の 3-lens Severity-rated Findings を取りまとめた Report
- CRITICAL/HIGH の Finding 発見時は Apply Blocking を推奨
- Remediation 実行のための `ywc-infra-optimize` (または再作成のための `ywc-iac-author`) の推奨

## 関連 Skill

- `ywc-iac-author` — upstream。本 Skill がレビューする Terraform を産出
- `ywc-infra-optimize` — downstream。本 Skill が発見した Cost/Drift Finding の Remediation を実行
- `ywc-security-engineer` / `ywc-performance-engineer` / `ywc-cloud-engineer`(Review Mode) の Persona — 各 Lens の Fan-out Worker
- `ywc-security-audit` — App-code の Auth/Injection Review 担当 (IaC オコンフィグではない)
- `ywc-impl-review` — 一般的な Application Code Review 担当 (Infrastructure ではない)
