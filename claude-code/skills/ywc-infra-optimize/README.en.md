# ywc-infra-optimize

A skill that improves already-provisioned infrastructure — cost right-sizing, unused-resource removal, reserved/spot adoption, drift detection & remediation, and reliability hardening. It applies `ywc-refactor-clean`'s SAFE/CAUTION/DANGER tiering and Iron Law (three witnesses) discipline to infrastructure as a safe change loop. Cost/utilization signal is gathered by `ywc-performance-engineer`, and SAFE-item execution is dispatched to `ywc-cloud-engineer`. CAUTION/DANGER items are never auto-executed — they are escalated only. Terraform is the single fixed IaC tool for this toolkit; every execution stops at `terraform plan` and never runs `apply`.

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
/ywc-infra-optimize --scope infra/modules/compute
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
- Each SAFE item executed as its own commit (bisectable)
- CAUTION/DANGER items reported and escalated, never executed
- A final verification block in `ywc-verify-done` shape

## Related Skills

- `ywc-infra-review` — upstream; diagnoses the cost/drift/reliability findings this skill remediates
- `ywc-verify-done` — downstream; final verification claim
- `ywc-iac-author` — re-authoring path for escalated CAUTION/DANGER items
- `ywc-performance-engineer` / `ywc-cloud-engineer` — the cost/utilization signal worker and the SAFE-item execution worker respectively
- `ywc-infra-design` — handles greenfield infrastructure design (not existing-infrastructure improvement)
- `ywc-refactor-clean` — the origin of the SAFE/CAUTION/DANGER Iron Law this skill borrows (application code, not infra)
