# ywc-infra-optimize

A skill that improves already-provisioned infrastructure through conservative planning — cost right-sizing, unused-resource removal, reserved/spot adoption, drift detection, and reliability hardening. It applies `ywc-refactor-clean`'s SAFE/CAUTION/DANGER tiering and Iron Law (three witnesses) discipline to infrastructure as a planning loop. Cost/utilization signal is gathered by a Codex worker carrying the `ywc-performance-engineer` persona, and optional feasibility or blast-radius advice can come from the read-only `ywc-cloud-engineer` persona. This skill does not execute Terraform changes in Codex v1; it classifies and hands remediation back to `ywc-iac-author`. Terraform is the single fixed IaC tool for this toolkit; every analysis stops at `terraform plan` and never runs `apply`.

## Localized Versions

- [한국어](./README.md)
- [日本語](./README.ja.md)
- [한국어 (요약 / summary)](./README.ko.md)

## When to Use

- The user says "optimize infrastructure", "cost optimization", "right-sizing", "terraform drift", "인프라 개선해줘", "비용 최적화해줘", "미사용 리소스 정리해줘", "インフラ最適化して"
- Cost/drift/reliability findings surfaced by `ywc-infra-review` need to actually be remediated
- A scheduled infrastructure optimization pass (cost savings, unused-resource cleanup) is needed

## How to Invoke

```bash
$ywc-infra-optimize --scope infra/modules/compute
```

Or in natural language:

> "clean up unused resources"
> "right-size these instances"

## Inputs

- (optional) `--scope <path>` — restrict scope to a single Terraform module/path instead of the whole IaC tree
- (optional) `--dry-run` — run gather + classify only and emit the report without executing any SAFE item
- (optional) `--skip-verify-done` — skip the closing `ywc-verify-done` handoff (only valid when the upstream caller already runs verify)

## Outputs

- A SAFE/CAUTION/DANGER classification report based on drift/cost/utilization signals
- Recommended next actions for SAFE items, typically a narrow `ywc-iac-author` remediation pass
- CAUTION/DANGER items reported and escalated, never executed here
- A final verification block in `ywc-verify-done` shape

## Related Skills

- `ywc-infra-review` — upstream; diagnoses the cost/drift/reliability findings this skill remediates
- `ywc-verify-done` — downstream; final verification claim
- `ywc-iac-author` — re-authoring path for escalated CAUTION/DANGER items
- `ywc-performance-engineer` / `ywc-cloud-engineer` personas — the cost/utilization signal worker and the read-only feasibility/blast-radius advisor respectively
- `ywc-infra-design` — handles greenfield infrastructure design (not existing-infrastructure improvement)
- `ywc-refactor-clean` — the origin of the SAFE/CAUTION/DANGER Iron Law this skill borrows (application code, not infra)
