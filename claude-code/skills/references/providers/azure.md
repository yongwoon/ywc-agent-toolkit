# Azure — Terraform Provider Reference

> Shared reference for the infra skill suite. Terraform is the single fixed IaC
> tool (design §7); this file describes Azure through the `hashicorp/azurerm`
> provider lens. Load only after Azure is the chosen provider (Progressive
> Disclosure — design §1). Bicep is intentionally out of scope (§7).

## Provider setup

```hcl
terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
  }
}
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
```

- The empty `features {}` block is required.
- Authenticate via Azure CLI / managed identity / OIDC — never a hardcoded
  client secret in `.tf`.
- Everything lives under a `azurerm_resource_group`; model it explicitly and
  scope the region there.

## Core service map (design input → Terraform resource)

| Concern | Primary resources |
|---|---|
| Network | `azurerm_virtual_network`, `azurerm_subnet`, `azurerm_network_security_group`, `azurerm_nat_gateway` |
| Identity | `azurerm_role_assignment`, `azurerm_user_assigned_identity`, `azurerm_role_definition` |
| Object store | `azurerm_storage_account` (+ `allow_nested_items_to_be_public = false`), `azurerm_storage_container` |
| Relational DB | `azurerm_mssql_server` / `_database`, `azurerm_postgresql_flexible_server` |
| Containers | `azurerm_kubernetes_cluster` (AKS), or `azurerm_container_app` |
| Serverless | `azurerm_linux_function_app`, `azurerm_service_plan` |
| Edge / DNS | `azurerm_dns_zone`, `azurerm_cdn_frontdoor_profile` |

## Lens anchors

- **Security** → RBAC role assignments at the narrowest scope (resource, not
  subscription), storage account public access disabled, private endpoints for
  data stores, TLS min version enforced. See [`../lenses/security.md`](../lenses/security.md).
- **Reliability** → Availability Zones for AKS node pools and databases,
  zone-redundant storage (ZRS/GZRS), geo-redundant backups. See
  [`../lenses/reliability.md`](../lenses/reliability.md).
- **Cost** → Reserved Instances / Savings Plans, Spot node pools for
  interruptible work, right-size SKUs, storage lifecycle to Cool/Archive. See
  [`../lenses/cost.md`](../lenses/cost.md).

## Azure-specific gotchas

- **Storage accounts default to allowing public blobs** — set
  `allow_nested_items_to_be_public = false` and disable
  `public_network_access` where possible.
- **RBAC scope creep** — assigning `Contributor`/`Owner` at subscription scope
  is the Azure analogue of an IAM wildcard; scope to the resource group or
  resource.
- **Resource group deletion cascades** — deleting an RG destroys everything in
  it; guard prod RGs and never `terraform destroy` casually.
- **SKU vs region availability** — some SKUs / zones are region-specific; a
  `plan` can succeed while `apply` fails on capacity.

## Terraform workflow

Author → `terraform fmt` → `validate` → `plan` → approved `apply`. See
[`../iac-tools/terraform.md`](../iac-tools/terraform.md).
