# ywc-infra-review

A skill that reviews already-authored IaC / cloud configuration before it is applied. It fans out to three lenses — security (misconfiguration, least-privilege), cost (right-sizing, waste), and reliability (SPOF, backups, health) — dispatching each to `ywc-security-engineer`, `ywc-performance-engineer`, and `ywc-cloud-engineer` (in review mode) respectively, then aggregates every finding by severity (Critical/High/Medium/Low). Any CRITICAL/HIGH finding recommends blocking apply. This skill never writes or modifies IaC itself — Terraform is the single fixed IaC tool for this toolkit, with AWS/GCP/Azure/K8s expressed through the Terraform providers.

## Localized Versions

- [한국어](./README.md)
- [日本語](./README.ja.md)
- [한국어 (요약)](./README.ko.md)

## When to Use

- The user says "infra review", "review my terraform", "IaC review", "인프라 리뷰해줘", "IaC 리뷰해줘", "terraform 검토해줘", "보안 그룹 점검해줘", "インフラレビューして"
- Terraform authored by `ywc-iac-author` needs a misconfiguration/cost/reliability check before apply
- Already-provisioned infrastructure needs a security-group, IAM-policy, or public-exposure check

## How to Invoke

```bash
/ywc-infra-review --scope infra/modules/network
```

Or in natural language:

> "review this terraform change"
> "check the security groups and IAM for the payments-api infrastructure"

## Inputs

- (optional) `--scope <path>` — restrict the review fan-out to a single Terraform module/path instead of the whole IaC tree
- (optional) `--skip-optimize-recommendation` — skip the closing `ywc-infra-optimize` recommendation (only valid when the upstream caller already schedules remediation itself)

## Outputs

- A severity-rated findings report aggregated across the security/cost/reliability 3-lens fan-out
- An explicit apply-blocking recommendation when a CRITICAL/HIGH finding is found
- A recommendation to run `ywc-infra-optimize` for remediation (or `ywc-iac-author` for re-authoring)

## Related Skills

- `ywc-iac-author` — upstream; produces the Terraform this skill reviews
- `ywc-infra-optimize` — downstream; executes remediation for cost/drift findings this skill surfaces
- `ywc-security-engineer` / `ywc-performance-engineer` / `ywc-cloud-engineer` (review mode) — the per-lens fan-out workers
- `ywc-security-audit` — handles app-code auth/injection review (not IaC misconfiguration)
- `ywc-impl-review` — handles general application code review (not infrastructure)
