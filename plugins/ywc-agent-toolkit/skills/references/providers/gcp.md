# GCP — Terraform Provider Reference

> Shared reference for the infra skill suite. Terraform is the single fixed IaC
> tool (design §7); this file describes GCP through the `hashicorp/google`
> provider lens. Load only after GCP is the chosen provider (Progressive
> Disclosure — design §1).

## Provider setup

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

- Pin the provider `version` with `~>`.
- Authenticate via Application Default Credentials / Workload Identity
  Federation — never a service-account key JSON committed to the repo.
- Almost every resource requires an explicit `project`; set it on the provider
  or per-resource to avoid "project not found" applies.

## Core service map (design input → Terraform resource)

| Concern | Primary resources |
|---|---|
| Network | `google_compute_network`, `google_compute_subnetwork`, `google_compute_router` + `_nat`, `google_compute_firewall` |
| Identity | `google_service_account`, `google_project_iam_member` / `_binding`, `google_service_account_iam_member` (Workload Identity) |
| Object store | `google_storage_bucket` (+ `uniform_bucket_level_access = true`) |
| Relational DB | `google_sql_database_instance`, `google_sql_database`, `google_sql_user` |
| Containers | `google_container_cluster` + `google_container_node_pool` (GKE), or `google_cloud_run_v2_service` |
| Serverless | `google_cloudfunctions2_function`, `google_cloud_run_v2_service` |
| Edge / DNS | `google_compute_global_address`, `google_dns_record_set`, `google_compute_managed_ssl_certificate` |

## Lens anchors

- **Security** → `uniform_bucket_level_access` (kills per-object ACL sprawl),
  least-privilege IAM members (avoid `roles/owner`, `roles/editor`), firewall
  source ranges scoped, CMEK where required. See [`../lenses/security.md`](../lenses/security.md).
- **Reliability** → regional (not zonal) GKE clusters, Cloud SQL HA
  (`availability_type = "REGIONAL"`), multi-zone node pools, automated backups.
  See [`../lenses/reliability.md`](../lenses/reliability.md).
- **Cost** → committed-use discounts vs preemptible/Spot VMs, right-size
  machine types, GCS lifecycle to Nearline/Coldline, delete idle external IPs
  and disks. See [`../lenses/cost.md`](../lenses/cost.md).

## GCP-specific gotchas

- **Project-level IAM is additive and broad** — `google_project_iam_binding`
  is *authoritative* for a role (overwrites all members); prefer
  `google_project_iam_member` for additive grants to avoid clobbering.
- **APIs must be enabled first** — many resources fail until the matching
  `google_project_service` is enabled; model the dependency explicitly.
- **Zonal vs regional** — a zonal GKE cluster or zonal Cloud SQL instance is a
  single-AZ SPOF; choose regional for production.
- **Default network** — auto-created default VPC is permissive; create an
  explicit VPC and delete/avoid the default in production.

## Terraform workflow

Author → `terraform fmt` → `validate` → `plan` → approved `apply`. See
[`../iac-tools/terraform.md`](../iac-tools/terraform.md).
