# AWS — Terraform Provider Reference

> Shared infra provider reference for AWS. Load this only after AWS is the
> chosen provider.

## Provider Setup

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" {
  region = var.region
  default_tags { tags = local.common_tags }
}
```

- Pin provider versions.
- Authenticate through environment, SSO, or assumed roles.
- Use default tags for ownership and cost allocation.

## Service Map

| Concern | Primary resources |
|---|---|
| Network | `aws_vpc`, `aws_subnet`, `aws_route_table`, `aws_nat_gateway`, `aws_security_group` |
| IAM | `aws_iam_role`, `aws_iam_policy`, `aws_iam_role_policy_attachment` |
| State and storage | `aws_s3_bucket`, `aws_s3_bucket_public_access_block` |
| Database | `aws_db_instance`, `aws_rds_cluster`, `aws_db_subnet_group` |
| Containers | `aws_ecs_cluster`, `aws_ecs_service`, `aws_eks_cluster`, `aws_eks_node_group` |

## AWS Gotchas

- Pair buckets with public-access blocking.
- Treat `0.0.0.0/0` ingress on admin or data ports as a security finding.
- Watch NAT gateway hourly and transfer costs.
- Prefer Multi-AZ and backup-enabled data services for production.

## Lens Anchors

- [Security](../lenses/security.md)
- [Cost](../lenses/cost.md)
- [Reliability](../lenses/reliability.md)
- [Terraform workflow](../iac/terraform.md)
