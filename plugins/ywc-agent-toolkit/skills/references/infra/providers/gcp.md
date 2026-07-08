# GCP — Terraform Provider Reference

> Shared infra provider reference for GCP. Load this only after GCP is the
> chosen provider.

## Provider Setup

```hcl
terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}
provider "google" {
  project = var.project_id
  region  = var.region
}
```

- Pin provider versions.
- Use ADC or workload identity rather than service-account keys in source.
- Model project and region explicitly.

## Service Map

| Concern | Primary resources |
|---|---|
| Network | `google_compute_network`, `google_compute_subnetwork`, `google_compute_firewall` |
| IAM | `google_service_account`, `google_project_iam_member`, `google_service_account_iam_member` |
| Storage | `google_storage_bucket` |
| Database | `google_sql_database_instance`, `google_sql_database` |
| Containers | `google_container_cluster`, `google_container_node_pool`, `google_cloud_run_v2_service` |

## GCP Gotchas

- Prefer additive IAM resources over authoritative bindings unless replacement is intentional.
- Enable required project services before dependent resources.
- Avoid zonal production primitives when regional alternatives exist.
- Replace the default VPC with explicit network design for real environments.

## Lens Anchors

- [Security](../lenses/security.md)
- [Cost](../lenses/cost.md)
- [Reliability](../lenses/reliability.md)
- [Terraform workflow](../iac/terraform.md)
