# Reliability Lens — Availability & Resilience Checklist

> Shared reference for the infra skill suite. One of the three review lenses
> (security / cost / reliability, design §2.3). This is the lens the
> `ywc-cloud-engineer` worker self-reviews against, `ywc-infra-review` fans
> out, and `ywc-infra-design` designs toward (RTO/RPO).

## The reliability taxonomy

| # | Risk | Signal in Terraform | Fix |
|---|---|---|---|
| 1 | **Single point of failure** | one instance / one AZ / one node | Redundancy ≥ 2 across AZs |
| 2 | **Single-AZ data tier** | RDS/Cloud SQL/AKS DB not multi-AZ/regional | Multi-AZ RDS; regional GKE; ZRS storage |
| 3 | **No backups / no PITR** | DB without automated backups / retention 0 | Enable automated backups + point-in-time recovery |
| 4 | **No health checks** | LB/target group / K8s pod without health/readiness probe | Add health checks + readiness/liveness probes |
| 5 | **No autoscaling** | fixed desired count with variable load | ASG / HPA / cluster-autoscaler with min ≥ 2 |
| 6 | **No graceful degradation** | hard dependency with no timeout/retry/circuit | Timeouts, retries, and a fallback path |
| 7 | **Stateful destroy risk** | plan destroys a DB/volume/bucket | Snapshot first; `prevent_destroy` lifecycle on critical stores |
| 8 | **Single-region** | all resources in one region, no DR | Cross-region replica/backup sized to the RTO/RPO target |

## RTO / RPO anchoring

- **RTO** (recovery *time*) drives redundancy topology: hot standby (near-zero
  RTO) vs restore-from-backup (hours).
- **RPO** (recovery *point* / data loss) drives backup frequency and
  replication: synchronous replica (near-zero RPO) vs daily snapshot (up to 24h).
- Design (`ywc-infra-design`) records the target; review confirms the IaC meets it.

## Review procedure

1. For each changed resource, ask: what fails if one AZ / one node / one region
   goes down? Is there a backup, and has it been tested for restore?
2. Flag any plan that **destroys** a stateful resource — confirm a snapshot
   exists first.
3. Report risk + resource + concrete fix, and note the RTO/RPO implication.

## Boundary

- **In scope**: availability, redundancy, backup/recovery, health, scaling.
- **Out of scope**: security → [`security.md`](security.md); cost →
  [`cost.md`](cost.md). Reliability and cost pull in opposite directions
  (redundancy costs money) — surface the trade-off explicitly.

Provider-specific HA primitives live in
[`../providers/aws.md`](../providers/aws.md),
[`gcp.md`](../providers/gcp.md), [`azure.md`](../providers/azure.md),
[`k8s.md`](../providers/k8s.md).
