---
name: ywc-infra-design
description: >-
  (ywc) Use when designing cloud/infrastructure architecture before any IaC
  is written — requirements gathering, provider selection, network/compute/
  storage/IAM topology, and a reliability/cost/security 3-lens pre-check that
  produces infra-design.md, the input contract ywc-iac-author consumes.
  Triggers: "인프라 설계", "클라우드 아키텍처", "aws 구성 설계", "네트워크
  토폴로지", "infra design", "cloud architecture", "design the
  infrastructure", "インフラ設計", "クラウド構成", "ywc-infra-design". Do not
  use for writing the actual IaC (use ywc-iac-author), source-code folder
  layout (use ywc-project-scaffold), library/tech comparison alone (use
  ywc-tech-research — it feeds this skill's provider-selection step),
  reviewing already-provisioned infrastructure (use ywc-infra-review), or
  local worktree docker port collisions (use ywc-docker-isolate — dev-only,
  not prod infra).
category: spec
phase: planning
requires: []
advisor_budget: 2
---

# ywc-infra-design

**Announce at start:** "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."

This skill is the design-phase counterpart to `ywc-iac-author`: it gathers requirements, selects a provider, designs the network/compute/storage/IAM topology, pre-checks the design against the reliability/cost/security lenses, and records every material trade-off as an ADR entry — then writes `infra-design.md`, the input contract `ywc-iac-author` loads before authoring a single Terraform module. **This skill never writes IaC.** Terraform is the single fixed IaC tool for this toolkit (design §7); this skill's topology decisions are made with that realization in mind, but the actual `.tf` authoring is `ywc-iac-author`'s job.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "I'll sketch the design and start writing Terraform in the same pass" | Design and implementation are separate skills on purpose — `ywc-iac-author` consumes a finished `infra-design.md` as its input contract. Collapsing the two loses the reviewable checkpoint and risks re-deriving the topology mid-authoring, the exact drift `ywc-iac-author`'s Common Mistakes section warns against. |
| "Requirements gathering is obvious from the feature description, I'll skip to topology" | Traffic shape, data classification, RTO/RPO, and budget ceiling all change the topology answer (multi-AZ vs single-AZ, managed vs self-hosted DB, hot-standby vs backup-only). Skipping this step produces a topology that looks reasonable but is unverified against the actual constraints. |
| "I already have a favorite provider, I'll just declare it instead of calling ywc-tech-research" | Only skip the `ywc-tech-research` delegation when the provider is genuinely already decided (existing account, mandated vendor, explicit user statement — use `--provider` to record that). When it is actually undecided, picking a favorite instead of delegating the comparison is a design decision made without evidence. |
| "The 3-lens pre-check is what ywc-infra-review is for, I can skip it here" | `ywc-infra-review` reviews already-authored IaC after the fact. This skill's pre-check catches structural mistakes (public subnet for a database tier, no backup strategy, wildcard IAM by default) before a single line of Terraform exists — far cheaper to fix at design time than after authoring. |
| "The trade-offs are self-evident from the topology diagram, no need to write an ADR" | A topology diagram shows the *what*, not the *why*. Without an ADR entry, the next reader — or `ywc-iac-author` — cannot tell whether "no multi-region" was a deliberate cost trade-off or an oversight that should be revisited. |
| "This is a small change, infra-design.md is overkill" | Even a small, well-understood change should record its provider, topology, and trade-off in `infra-design.md`. `ywc-iac-author`'s Step 1 either loads this file or falls back to inline-intent clarification; skipping it silently degrades every downstream authoring pass to the weaker inline-intent path. |

**Violating the letter of these rules is violating the spirit.** A design pass that skips requirements, invents a provider, or omits the lens pre-check hands `ywc-iac-author` a topology no one actually verified.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--provider` | `--provider aws\|gcp\|azure\|k8s` | `--provider aws` | Declare an already-decided provider, skipping the `ywc-tech-research` delegation in Step 2. |
| `--scope` | `--scope <system-name>` | `--scope payments-api` | Restrict the design pass to a single service/system instead of the whole architecture. |
| `--skip-cloud-consult` | flag | `--skip-cloud-consult` | Skip the optional read-only `ywc-cloud-engineer` feasibility consult in Step 3. |

## Workflow

### Step 1: Requirements gathering

Gather and record, explicitly — this is the evidence base for every topology decision that follows:

- **Workload characteristics**: request pattern (read-heavy/write-heavy/mixed), synchronous vs batch vs event-driven, statefulness.
- **Traffic**: expected concurrency/RPS, peak vs steady-state, growth trajectory over the next 6–12 months.
- **Data**: volume, growth rate, classification (PII/PHI/none), retention requirements.
- **Regulatory / compliance**: data residency constraints, applicable frameworks (GDPR, HIPAA, SOC 2, industry-specific mandates).
- **Budget**: monthly ceiling or a per-unit cost target.
- **RTO/RPO**: acceptable downtime window and acceptable data-loss window.

Do not infer these from the feature description alone — ask the user for anything not already stated, and record the answers verbatim in the eventual `infra-design.md`.

### Step 2: Provider selection

If `--provider` was passed or the provider is otherwise already decided (existing account, mandated vendor, explicit user statement), record the decision and its rationale, then move to Step 3.

If the provider is genuinely undecided, delegate the AWS/GCP/Azure/K8s comparison to `/ywc-tech-research` — do not invent the comparison inline. Feed it this step's requirements (traffic, data, budget, compliance) as comparison criteria, and record its recommendation as the Provider Decision.

### Step 3: Topology design

Design, in this order:

- **Network**: VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths.
- **Compute**: service shape (managed container, VM, serverless/FaaS) matched to the workload characteristics from Step 1.
- **Storage**: database engine, object storage, cache layer, matched to the data profile from Step 1.
- **IAM / identity boundaries**: role structure, least-privilege boundaries, cross-account or cross-service trust relationships.

Unless `--skip-cloud-consult` was passed, optionally dispatch `Task(subagent_type: ywc-cloud-engineer)` in **read-only feasibility-consult mode** — carry the topology sketch and an explicit instruction that this dispatch authors nothing and runs no `terraform apply`/`plan`, it only flags feasibility concerns (quota limits, provider-specific gotchas, an unrealistic network layout) before the design is finalized.

### Step 4: Reliability / cost / security 3-lens pre-check

Read [`../references/lenses/reliability.md`](../references/lenses/reliability.md), [`../references/lenses/cost.md`](../references/lenses/cost.md), and [`../references/lenses/security.md`](../references/lenses/security.md), then pre-check the Step 3 topology against each lens's taxonomy. Record every finding — even a "no issue found" pass — so `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline instead of re-deriving it.

### Step 5: Trade-off records (ADR)

For every material decision from Steps 2–3 (provider choice, single-AZ vs multi-AZ, managed vs self-hosted database, network exposure boundary, etc.), write an Architecture Decision Record entry with four fields: **Context**, **Decision**, **Alternatives considered**, **Consequences**. A decision without an ADR entry is a decision no future reader can audit.

### Step 6: Output `infra-design.md`

Write `infra-design.md` at the project root (or the path implied by `--scope`) with the sections in Output Format below. This file is the input contract `ywc-iac-author`'s Step 1 loads — write it so that skill can proceed without re-asking any question this step already answered.

## Output Format

```text
# infra-design.md

## Requirements
- Workload: <pattern>
- Traffic: <RPS/concurrency, peak vs steady, growth>
- Data: <volume, classification, retention>
- Compliance: <frameworks, residency>
- Budget: <monthly ceiling / per-unit target>
- RTO/RPO: <downtime window> / <data-loss window>

## Provider Decision
Provider: <AWS|GCP|Azure|K8s>
Source: <--provider flag | already decided | ywc-tech-research recommendation>
Rationale: <1-3 lines>

## Topology
### Network
<VPC/VNet, subnets, public/private boundary>
### Compute
<service shape + rationale>
### Storage
<DB engine, object storage, cache>
### IAM / Identity Boundaries
<role structure, least-privilege boundaries, trust relationships>

## 3-Lens Pre-Check
- Reliability: <findings, or "no issue found">
- Cost: <findings, or "no issue found">
- Security: <findings, or "no issue found">

## ADR Log
### ADR-001: <decision title>
- Context: ...
- Decision: ...
- Alternatives considered: ...
- Consequences: ...
```

## Validation Checklist

Before declaring the design pass complete, verify:

- [ ] Requirements (workload, traffic, data, compliance, budget, RTO/RPO) were gathered explicitly, not inferred
- [ ] The provider decision was either explicitly declared (`--provider` or prior decision) or delegated to `ywc-tech-research` — never invented inline
- [ ] Topology covers all four dimensions: network, compute, storage, IAM/identity boundaries
- [ ] The reliability/cost/security 3-lens pre-check was run and every finding (including "no issue found") is recorded
- [ ] Every material trade-off has a corresponding ADR entry (Context / Decision / Alternatives / Consequences)
- [ ] `infra-design.md` was written with all five sections and is ready for `ywc-iac-author` to load directly

## Common Mistakes

- **Jumping straight to Terraform.** This skill's job ends at `infra-design.md` — writing `.tf` files in the same pass is `ywc-iac-author`'s scope, not this skill's.
- **Treating the cloud-engineer consult as authoring.** The Step 3 `ywc-cloud-engineer` dispatch is read-only feasibility feedback; if it starts producing `.tf` files, the dispatch instruction was wrong.
- **Skipping the lens pre-check because "the topology looks fine."** The taxonomy in each lens file catches exactly the mistakes that look fine on a quick read (public subnet for a DB, wildcard IAM) — that is why it exists as a checklist, not a gut check.
- **Writing ADR entries after the fact from memory.** Record each trade-off as it is decided in Step 5, not reconstructed at the end — reconstruction drops the alternatives that were actually considered.

## Integration

- **Upstream**: `ywc-tech-research` (provider comparison when undecided); direct user invocation when requirements and provider are already known.
- **Downstream**: `ywc-iac-author` (loads `infra-design.md` as its authoring input contract), then `ywc-infra-review` (reviews the resulting IaC before apply).
- **Consults**: `ywc-cloud-engineer` in read-only mode for topology feasibility, never for authoring.
- **Must not be paired with**: writing or modifying `.tf` files in the same pass — that boundary belongs to `ywc-iac-author`.

## References

| Reference | Use when |
|---|---|
| [`../references/lenses/reliability.md`](../references/lenses/reliability.md) | Step 4 — pre-checking topology for availability/resilience gaps |
| [`../references/lenses/cost.md`](../references/lenses/cost.md) | Step 4 — pre-checking topology for cost drivers and right-sizing |
| [`../references/lenses/security.md`](../references/lenses/security.md) | Step 4 — pre-checking topology for the IaC misconfiguration taxonomy |
| [`../references/providers/aws.md`](../references/providers/aws.md) | Provider decision is AWS — informs realistic topology choices |
| [`../references/providers/gcp.md`](../references/providers/gcp.md) | Provider decision is GCP — informs realistic topology choices |
| [`../references/providers/azure.md`](../references/providers/azure.md) | Provider decision is Azure — informs realistic topology choices |
| [`../references/providers/k8s.md`](../references/providers/k8s.md) | Provider decision includes Kubernetes/Helm (via Terraform providers) |
