# FinOps — Cloud Cost Analysis for `ywc-performance-engineer`

> Reference for the `ywc-performance-engineer` agent when its scope includes
> cloud infrastructure cost (Terraform `.tf` files, instance/SKU sizing,
> pricing model, storage tiers, data transfer). This extends the agent's
> application-performance review (latency / bundle / Web Vitals) with a
> **cloud-cost / right-sizing** lens. It is the performance-engineer's deeper
> companion to the shared review lens at [`lenses/cost.md`](lenses/cost.md) —
> same taxonomy, agent-facing depth (magnitude + concrete remediation).

## Scope boundary

- **In scope for this reference**: infrastructure cost — compute right-sizing,
  pricing model (on-demand vs reserved vs spot), storage tiering, idle/orphaned
  resources, data-transfer/egress.
- **Still application performance** (the agent's primary lens): backend latency,
  frontend bundle/render, Core Web Vitals. This reference adds the infra-cost
  surface when the diff includes `.tf` files.

## The cost taxonomy (magnitude-rated)

| Class | Terraform signal | How to size the finding | Remediation |
|---|---|---|---|
| **Over-provisioned compute** | instance/SKU larger than the workload's p95; fixed large node pools | Estimate the monthly $ delta between chosen and right-sized SKU | Right-size to observed utilization; enable autoscaling with `min ≥ 2` |
| **On-demand for steady load** | 24/7 baseline on on-demand pricing | Reserved/committed discount is typically 30–60% vs on-demand | Savings Plans / Reserved Instances / committed-use — only after utilization is proven |
| **On-demand for interruptible load** | batch / stateless / fault-tolerant work on full-price compute | Spot is typically 60–90% cheaper | Spot / preemptible / Spot node pools with graceful interruption handling |
| **Idle / orphaned** | unattached EBS/PD, unused EIP/static IP, idle NAT gateway, stopped-but-billed | Direct monthly waste — highest-confidence savings | Delete now; add orphan-creation alerting |
| **Hot storage for cold data** | everything in S3 Standard / GCS Standard | Lifecycle to IA/Nearline → Glacier/Coldline is 40–95% cheaper per GB | Add lifecycle rules keyed on access age |
| **Data-transfer / egress** | cross-AZ / cross-region / internet egress chatter | Egress is a silent per-GB cost; cross-AZ adds up at scale | Co-locate; private endpoints; edge caching; keep chatty services same-AZ |
| **Over-requested K8s pods** | `resources.requests` >> actual usage | Wasted node capacity = wasted node cost | Right-size requests; HPA; cluster-autoscaler; bin-pack |
| **24/7 non-prod** | prod-sized non-prod running around the clock | Off-hours is ~65% of the week | Scale-to-zero / scheduled shutdown in non-prod |

## Review procedure (when `.tf` is in scope)

1. For each changed resource, ask: sized to real demand? right pricing model?
   anything left orphaned?
2. Quantify the finding by **magnitude**, not just name — an order-of-magnitude
   monthly $ delta is enough for review; exact figures need a cost calculator.
3. Separate **now savings** (delete idle — do immediately) from **commitment
   savings** (reserved/committed — only after utilization is proven), the same
   evidence discipline the agent applies to performance budgets.
4. Surface the **cost ↔ reliability tension** explicitly: cost pushes toward
   fewer/smaller resources, reliability toward redundancy. Do not silently
   optimize availability away — name the trade-off for the caller to decide.

## Handoff

- The **reliability** side of the trade-off is the infra-review reliability lens
  / [`lenses/reliability.md`](lenses/reliability.md).
- The **security** side (public buckets, open SG) is
  [`iac-security.md`](iac-security.md) / [`lenses/security.md`](lenses/security.md).
- Provider-specific pricing levers live in
  [`providers/aws.md`](providers/aws.md),
  [`providers/gcp.md`](providers/gcp.md),
  [`providers/azure.md`](providers/azure.md),
  [`providers/k8s.md`](providers/k8s.md).
