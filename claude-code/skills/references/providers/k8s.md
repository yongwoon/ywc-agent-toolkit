# Kubernetes — Terraform Provider Reference

> Shared reference for the infra skill suite. Terraform is the single fixed IaC
> tool (design §7); Kubernetes and Helm resources are expressed through the
> Terraform `hashicorp/kubernetes` and `hashicorp/helm` providers — **not** raw
> `kubectl` manifests, Kustomize, or standalone Helm CLI. Load only after K8s is
> the target (Progressive Disclosure — design §1).

## Provider setup

```hcl
terraform {
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.0" }
    helm       = { source = "hashicorp/helm",       version = "~> 2.0" }
  }
}
provider "kubernetes" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_ca)
  # token / exec auth — never a static kubeconfig committed to the repo
}
provider "helm" {
  kubernetes { host = var.cluster_endpoint /* ...same auth... */ }
}
```

- Drive cluster auth from the cluster resource outputs (EKS/GKE/AKS), not a
  checked-in kubeconfig.
- Prefer `helm_release` for third-party charts; use `kubernetes_manifest` /
  typed resources for first-party workloads.

## Core object map (design input → Terraform resource)

| Concern | Primary resources |
|---|---|
| Workload | `kubernetes_deployment_v1`, `kubernetes_stateful_set_v1`, `kubernetes_job_v1` |
| Networking | `kubernetes_service_v1`, `kubernetes_ingress_v1`, `kubernetes_network_policy_v1` |
| Config | `kubernetes_config_map_v1`, `kubernetes_secret_v1` |
| Identity | `kubernetes_service_account_v1`, `kubernetes_role_v1` + `_role_binding_v1`, `kubernetes_cluster_role*` |
| Scaling | `kubernetes_horizontal_pod_autoscaler_v2` |
| Packaged apps | `helm_release` |

## Lens anchors

- **Security** → `kubernetes_network_policy_v1` default-deny, least-privilege
  (Cluster)Role RBAC (no wildcard `verbs`/`resources`), non-root
  `security_context`, secrets from an external store not plain
  `kubernetes_secret`. See [`../lenses/security.md`](../lenses/security.md).
- **Reliability** → `replicas ≥ 2`, `readiness`/`liveness` probes, pod
  `resources.requests`/`limits`, `PodDisruptionBudget`, topology spread across
  nodes/zones. See [`../lenses/reliability.md`](../lenses/reliability.md).
- **Cost** → right-size requests/limits (over-requesting wastes node capacity),
  HPA to scale to demand, cluster-autoscaler, spot/preemptible node pools for
  stateless work. See [`../lenses/cost.md`](../lenses/cost.md).

## Kubernetes-specific gotchas

- **No probes = no reliability** — without readiness probes a rolling update
  can route traffic to a not-ready pod; without liveness probes a wedged pod is
  never restarted.
- **No resource requests = noisy-neighbour + bad scheduling** — the scheduler
  packs blindly and one pod can starve a node.
- **`kubernetes_secret_v1` is base64, not encrypted** — treat as config;
  real secrets belong in an external manager surfaced via a CSI driver.
- **Namespaces are a soft boundary** — pair with NetworkPolicy + RBAC for real
  isolation.
- **`kubernetes_manifest` needs the CRD to exist at plan time** — ordering
  matters; apply CRDs (often via `helm_release`) before manifests that use them.

## Terraform workflow

Author → `terraform fmt` → `validate` → `plan` → approved `apply`. See
[`../iac-tools/terraform.md`](../iac-tools/terraform.md).
