# Cost Lens — FinOps Review Checklist

> Shared reference for the infra skill suite. One of the three review lenses
> (security / cost / reliability, design §2.3). `ywc-infra-review` fans this
> lens out; `ywc-infra-optimize` drives right-sizing/cleanup from it;
> `ywc-infra-design` produces the initial cost estimate against it.

## The cost taxonomy

| # | Cost driver | Signal | Optimization |
|---|---|---|---|
| 1 | **Over-provisioned compute** | instance/SKU larger than utilization; fixed large node pools | Right-size to observed p95; enable autoscaling |
| 2 | **On-demand for steady load** | 24/7 baseline on on-demand pricing | Reserved Instances / Savings Plans / committed-use discounts |
| 3 | **On-demand for interruptible load** | batch/stateless work on full-price compute | Spot / preemptible / Spot node pools |
| 4 | **Idle / orphaned resources** | unattached EBS/PD, unused EIP/static IP, idle NAT gateway, stopped-but-billed | Delete; alert on orphan creation |
| 5 | **Hot storage for cold data** | everything in S3 Standard / GCS Standard | Lifecycle to IA/Nearline → Glacier/Coldline/Archive |
| 6 | **Data-transfer / egress** | cross-AZ / cross-region / internet egress chatter | Co-locate; use private endpoints; cache at edge |
| 7 | **Over-requested K8s pods** | `requests` >> actual usage | Right-size requests; HPA; cluster-autoscaler; bin-pack |
| 8 | **Redundant environments** | prod-sized non-prod running 24/7 | Scale-to-zero / schedule off-hours shutdown in non-prod |

## Review procedure

1. For each changed resource, ask: is it sized to real demand, on the right
   pricing model, and does it leave anything orphaned?
2. Estimate the monthly delta of the change (order of magnitude is enough for
   review — exact figures need a cost calculator).
3. Distinguish **now** savings (delete idle) from **commitment** savings
   (reserved/committed — only after utilization is proven).

## Boundary

- **In scope**: cost/right-sizing/waste of the infrastructure.
- **Out of scope**: security misconfiguration → [`security.md`](security.md);
  availability/SPOF → [`reliability.md`](reliability.md). Note the tension:
  cost pushes toward fewer/smaller resources, reliability toward redundancy —
  surface the trade-off, do not silently optimize one away.

Provider-specific pricing levers live in
[`../providers/aws.md`](../providers/aws.md),
[`gcp.md`](../providers/gcp.md), [`azure.md`](../providers/azure.md),
[`k8s.md`](../providers/k8s.md).
