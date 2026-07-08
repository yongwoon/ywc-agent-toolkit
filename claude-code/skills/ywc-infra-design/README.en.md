# ywc-infra-design

Cloud/infrastructure architecture design skill. Before any IaC is written, it runs requirements gathering, provider selection, network/compute/storage/IAM topology design, and a reliability/cost/security 3-lens pre-check, records every material trade-off as an ADR (Architecture Decision Record), and produces `infra-design.md` — the input contract `ywc-iac-author` loads. This skill never writes IaC itself — **Terraform is the single fixed IaC tool** for this toolkit (design §7); the actual `.tf` authoring is `ywc-iac-author`'s job.

## Localized Versions

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## When to Use

- The user says "infra design", "cloud architecture", "design the infrastructure", "인프라 설계해줘", "클라우드 아키텍처 설계해줘", "aws 구성 설계해줘", "インフラ設計して"
- A new feature/service needs its infrastructure designed from scratch
- The provider is not yet decided and needs a comparison (delegated to `ywc-tech-research`)
- You want to avoid jumping straight to `ywc-iac-author` without a reviewed `infra-design.md`

## How to Invoke

```bash
/ywc-infra-design --provider aws
```

Or in natural language:

> "design the infrastructure for this service"
> "design the cloud architecture for payments-api"

## Inputs

- (optional) `--provider <aws|gcp|azure|k8s>` — declare an already-decided provider, skipping the `ywc-tech-research` delegation (Step 2)
- (optional) `--scope <system-name>` — restrict the design pass to a single service/system instead of the whole architecture
- (optional) `--skip-cloud-consult` — skip the Step 3 read-only `ywc-cloud-engineer` feasibility consult

## Outputs

- `infra-design.md` — an input contract document composed of Requirements / Provider Decision / Topology (network/compute/storage/IAM) / 3-Lens Pre-Check Results / ADR Log
- A finished design artifact `ywc-iac-author` can load directly at its Step 1

## Related Skills

- `ywc-tech-research` — upstream; handles the comparison when the provider is undecided and feeds its result into this skill
- `ywc-iac-author` — downstream; loads this skill's `infra-design.md` output to author the actual Terraform
- `ywc-infra-review` — downstream; reviews already-authored IaC (this skill designs infrastructure that has not been authored yet)
- `ywc-cloud-engineer` — the Step 3 read-only topology feasibility consult (not authoring)
- `ywc-project-scaffold` — source-code folder layout (not infrastructure architecture)
- `ywc-docker-isolate` — local worktree Docker port isolation only, not production infrastructure
