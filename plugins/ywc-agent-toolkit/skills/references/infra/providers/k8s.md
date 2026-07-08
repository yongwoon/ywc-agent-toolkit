# Kubernetes — Terraform Provider Reference

> Shared infra provider reference for Kubernetes via the Terraform
> `kubernetes` and `helm` providers. Raw manifests, Kustomize, and standalone
> Helm flows are out of scope.

## Provider Setup

```hcl
terraform {
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.0" }
    helm       = { source = "hashicorp/helm",       version = "~> 2.0" }
  }
}
```

- Drive auth from cluster outputs rather than checked-in kubeconfig.
- Use `helm_release` for third-party charts and typed resources or
  `kubernetes_manifest` for first-party workloads.

## Object Map

| Concern | Primary resources |
|---|---|
| Workload | `kubernetes_deployment_v1`, `kubernetes_stateful_set_v1`, `kubernetes_job_v1` |
| Network | `kubernetes_service_v1`, `kubernetes_ingress_v1`, `kubernetes_network_policy_v1` |
| Identity | `kubernetes_service_account_v1`, `kubernetes_role_v1`, `kubernetes_cluster_role_v1` |
| Scaling | `kubernetes_horizontal_pod_autoscaler_v2` |
| Packaging | `helm_release` |

## Kubernetes Gotchas

- Missing readiness or liveness probes is a reliability defect.
- Missing resource requests creates noisy-neighbor and scheduling risk.
- Kubernetes secrets are only base64-encoded; keep real secrets external.
- Namespaces are not enough isolation without RBAC and network policy.
- `kubernetes_manifest` requires CRDs to exist before dependent manifests plan.

## Lens Anchors

- [Security](../lenses/security.md)
- [Cost](../lenses/cost.md)
- [Reliability](../lenses/reliability.md)
- [Terraform workflow](../iac/terraform.md)
