# Azure — Terraform Provider Reference

> Shared infra provider reference for Azure. Load this only after Azure is the
> chosen provider.

## Provider Setup

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

- `features {}` is required.
- Authenticate through Azure CLI, managed identity, or OIDC.
- Scope resources through explicit resource groups.

## Service Map

| Concern | Primary resources |
|---|---|
| Network | `azurerm_virtual_network`, `azurerm_subnet`, `azurerm_network_security_group` |
| RBAC | `azurerm_role_assignment`, `azurerm_user_assigned_identity` |
| Storage | `azurerm_storage_account`, `azurerm_storage_container` |
| Database | `azurerm_mssql_server`, `azurerm_postgresql_flexible_server` |
| Containers | `azurerm_kubernetes_cluster`, `azurerm_container_app` |

## Azure Gotchas

- Disable public storage exposure explicitly.
- Treat subscription-scope `Owner` or `Contributor` as over-privilege.
- Remember resource-group deletion is a broad destroy operation.
- Check regional SKU and zone availability early.

## Lens Anchors

- [Security](../lenses/security.md)
- [Cost](../lenses/cost.md)
- [Reliability](../lenses/reliability.md)
- [Terraform workflow](../iac/terraform.md)
