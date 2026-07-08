# AWS — Terraform Provider Reference

> Shared reference for the infra skill suite (`ywc-infra-design`,
> `ywc-iac-author`, `ywc-infra-review`, `ywc-infra-optimize`). Terraform is the
> single fixed IaC tool (design §7); this file describes AWS through the
> `hashicorp/aws` provider lens. Load this file only after AWS is the chosen
> provider (Progressive Disclosure — design §1).

## Provider setup

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" {
  region = var.region
  default_tags { tags = local.common_tags }   # tag every resource by default
}
```

- Pin the provider `version` with `~>`; never leave it floating.
- Use `default_tags` so cost-allocation and ownership tags are not forgotten
  per-resource.
- Authenticate via environment / SSO / assumed role — never a hardcoded
  `access_key` / `secret_key` in `.tf`.

## Core service map (design input → Terraform resource)

| Concern | Primary resources |
|---|---|
| Network | `aws_vpc`, `aws_subnet`, `aws_route_table`, `aws_nat_gateway`, `aws_internet_gateway`, `aws_security_group` |
| Identity | `aws_iam_role`, `aws_iam_policy`, `aws_iam_role_policy_attachment`, `aws_iam_openid_connect_provider` (IRSA) |
| Object store | `aws_s3_bucket` + `aws_s3_bucket_public_access_block`, `_versioning`, `_server_side_encryption_configuration` |
| Relational DB | `aws_db_instance` / `aws_rds_cluster` (Aurora), `aws_db_subnet_group` |
| Containers | `aws_ecs_cluster` / `aws_ecs_service` (Fargate), or `aws_eks_cluster` + `aws_eks_node_group` |
| Serverless | `aws_lambda_function`, `aws_apigatewayv2_api` |
| Edge / DNS | `aws_cloudfront_distribution`, `aws_route53_record`, `aws_acm_certificate` |

## Well-Architected mapping (quick lens anchors)

- **Security** → least-privilege IAM (no `"*"` actions/resources), S3 public
  access block on, SG ingress scoped (no `0.0.0.0/0` to admin ports),
  encryption at rest (KMS) and in transit (TLS). See
  [`../lenses/security.md`](../lenses/security.md).
- **Reliability** → multi-AZ subnets, RDS Multi-AZ / read replicas, ASG or
  ECS/EKS desired-count ≥ 2, automated backups + PITR, health checks. See
  [`../lenses/reliability.md`](../lenses/reliability.md).
- **Cost** → right-size instance families, Savings Plans / Reserved / Spot for
  steady vs bursty, S3 lifecycle to IA/Glacier, delete idle NAT gateways and
  unattached EBS/EIP. See [`../lenses/cost.md`](../lenses/cost.md).

## AWS-specific gotchas

- **S3 buckets are public unless blocked** — always pair a bucket with
  `aws_s3_bucket_public_access_block` (all four flags `true`).
- **IAM eventual consistency** — a freshly created role may not be assumable
  immediately; `terraform apply` retries usually cover it, but flaky first
  applies are normal.
- **NAT gateways bill per-hour + per-GB** — a frequent silent cost; one per AZ
  for HA, but consolidate in non-prod.
- **Security groups vs NACLs** — SGs are stateful (return traffic auto-allowed);
  NACLs are stateless. Prefer SGs for app-tier rules.
- **`force_destroy` on S3 / ECR** — off by default; a bucket with objects will
  block `terraform destroy` unless set (use with care in prod).

## Terraform workflow

Author → `terraform fmt` → `terraform validate` → `terraform plan` (review
blast radius) → human-approved `apply`. See
[`../iac-tools/terraform.md`](../iac-tools/terraform.md) for the full workflow
and state/secret externalization guards.
