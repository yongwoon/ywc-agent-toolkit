# Dispatch artifact: ywc-infra-design (original body, run 3)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The user's request restates the general capability (design cloud/infra architecture, produce infra-design.md) but supplies none of the Step 1 requirements the procedure mandates be gathered explicitly and never inferred: workload characteristics, traffic/growth, data volume and classification, compliance/residency constraints, budget ceiling, and RTO/RPO. It also does not state whether a cloud provider is already decided or should be compared via /ywc-tech-research, nor whether the design should be scoped to a single system (--scope) or cover the whole architecture. Per the skill's explicit Rationalization Defense entry ("Requirements gathering is obvious from the feature description, I'll skip to topology") and Step 1's directive ("Do not infer these from the feature description alone — ask the user for anything not already stated"), the correct action is to pause after the announcement and ask the user for these six requirement categories plus the provider-decision status and scope before any topology, provider selection, lens pre-check, or infra-design.md content is produced.

## Actions
- Announce at start: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."
- Check invocation for --provider, --scope, --skip-cloud-consult flags (none supplied)
- Step 1: ask the user explicit requirements-gathering questions (workload pattern, traffic/RPS and growth, data volume/classification/retention, compliance/residency, budget ceiling, RTO/RPO) rather than inferring them from the request text
- Pause and wait for user answers before proceeding to Step 2
- Step 2 (once requirements are known): if provider is not already decided, dispatch /ywc-tech-research with the gathered requirements as comparison criteria (AWS vs GCP vs Azure vs K8s) instead of inventing a recommendation inline; if already decided, record decision + rationale directly
- Step 3: design topology in order — Network (VPC/subnet tiers, public/private boundary, ingress/egress), Compute (service shape matched to workload), Storage (DB engine, object storage, cache matched to data profile), IAM/identity boundaries (least-privilege roles, cross-account/service trust)
- Unless --skip-cloud-consult is passed, dispatch Task(subagent_type: ywc-cloud-engineer) in read-only feasibility-consult mode with explicit instruction that it authors nothing and runs no terraform plan/apply
- Step 4: Read ../references/lenses/reliability.md, ../references/lenses/cost.md, ../references/lenses/security.md and pre-check the topology against each taxonomy, recording every finding including 'no issue found'
- Read the relevant ../references/providers/<provider>.md file to ground topology choices in provider-realistic constraints
- Step 5: write an ADR entry (Context / Decision / Alternatives considered / Consequences) for every material decision from Steps 2-3 as each decision is made, not reconstructed afterward
- Step 6: Write infra-design.md at the project root (or --scope path) following the Output Format template with all sections: Requirements, Provider Decision, Topology, 3-Lens Pre-Check, ADR Log
- Run through the Validation Checklist before declaring the design pass complete
- Explicitly refuse to jump to writing Terraform/.tf files in this same pass — that is ywc-iac-author's scope

## Files touched
- claude-code/skills/ywc-infra-design/SKILL.md (read only, procedure source)
- claude-code/skills/references/lenses/reliability.md (read, Step 4)
- claude-code/skills/references/lenses/cost.md (read, Step 4)
- claude-code/skills/references/lenses/security.md (read, Step 4)
- claude-code/skills/references/providers/aws.md or gcp.md/azure.md/k8s.md (read, whichever provider is decided)
- infra-design.md (create/write at project root or --scope path, Step 6 output)

## Gates enforced
- Requirements-not-inferred gate (Step 1): do not proceed to topology design until workload, traffic, data, compliance, budget, and RTO/RPO are explicitly stated by the user, not guessed from the feature description
- Provider-decision gate (Step 2): never invent a provider comparison inline — either an explicit prior decision/--provider flag is recorded, or the comparison is delegated to /ywc-tech-research
- Cloud-engineer consult is read-only (Step 3): if dispatched, it must not author .tf files or run terraform plan/apply
- 3-lens pre-check completeness gate (Step 4): every lens (reliability/cost/security) must have a recorded finding, including explicit 'no issue found' entries — cannot be skipped because 'the topology looks fine'
- ADR completeness gate (Step 5): every material trade-off (provider choice, single-AZ vs multi-AZ, managed vs self-hosted DB, network exposure boundary, etc.) must have a four-field ADR entry recorded at decision time, not reconstructed from memory afterward
- Output-contract gate (Step 6 / Validation Checklist): infra-design.md must contain all five required sections and be usable by ywc-iac-author without re-asking questions this pass already answered
- Scope boundary gate: this skill must not write or modify any .tf files in the same pass — that boundary belongs strictly to ywc-iac-author

## Full narrative

Having read claude-code/skills/ywc-infra-design/SKILL.md in full, here is exactly how I would proceed if this request came in as a live task.

First, I would announce the skill per the required opening line: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."

Next I would check the request for the skill's three arguments — `--provider`, `--scope`, `--skip-cloud-consult`. None were supplied, so I default to: provider undecided (must be resolved via Step 2), scope is the whole architecture (no `--scope` path), and the optional `ywc-cloud-engineer` consult stays in play for Step 3.

At this point I would stop and not proceed into Step 2 topology work, because Step 1 (Requirements gathering) is explicit that these six categories must be gathered and recorded, not inferred from the feature description: workload characteristics (request pattern, sync/batch/event-driven, statefulness), traffic (RPS/concurrency, peak vs steady-state, 6–12 month growth), data (volume, growth rate, classification — PII/PHI/none, retention), regulatory/compliance (data residency, GDPR/HIPAA/SOC2/industry mandates), budget (monthly ceiling or per-unit target), and RTO/RPO (downtime and data-loss windows). The user's message names the deliverable and process but supplies none of these six answers, and the skill's own Rationalization Defense table calls out exactly this shortcut ("Requirements gathering is obvious from the feature description, I'll skip to topology") as invalid — traffic shape, data classification, and RTO/RPO all change the topology answer (multi-AZ vs single-AZ, managed vs self-hosted DB, hot-standby vs backup-only).

So rather than guessing at a workload profile or inventing plausible numbers, I would ask the user directly for:
1. What is the system/service being designed, and is this a new build or adding infra to an existing system?
2. Workload shape: read-heavy, write-heavy, or mixed; synchronous request/response, batch, or event-driven; stateful or stateless?
3. Expected traffic: peak and steady-state RPS/concurrency, and the growth trajectory expected over the next 6–12 months?
4. Data: volume today and growth rate, data classification (PII/PHI/none), and retention requirements?
5. Compliance/regulatory constraints: data residency requirements, and any applicable frameworks (GDPR, HIPAA, SOC 2, industry-specific)?
6. Budget: a monthly ceiling or a per-unit cost target?
7. RTO/RPO: acceptable downtime window and acceptable data-loss window?
8. Is the cloud provider already decided (existing account, mandated vendor)? If so, which — AWS, GCP, Azure, or K8s — and why? If not, I would delegate the comparison to `/ywc-tech-research` rather than picking one myself.
9. Should this design cover the whole architecture, or a single service/system (equivalent to `--scope`)?

Only after receiving these answers would I proceed to the remainder of the procedure, and I would carry it out exactly as specified:

- **Step 2 (Provider selection)**: if the user's answer to question 8 names a provider with a stated rationale (existing account, mandated vendor, explicit preference), I record that as the Provider Decision directly. If genuinely undecided, I would dispatch `/ywc-tech-research`, feeding it the traffic, data, budget, and compliance answers from Step 1 as comparison criteria, and record its recommendation — I would not invent an AWS/GCP/Azure/K8s comparison inline myself.

- **Step 3 (Topology design)**: in strict order — Network (VPC/VNet layout, subnet tiers, public/private boundary, ingress/egress paths), Compute (managed container vs VM vs serverless/FaaS, matched to the Step 1 workload characteristics), Storage (database engine, object storage, cache layer, matched to the Step 1 data profile), and IAM/identity boundaries (role structure, least-privilege boundaries, cross-account/cross-service trust). Unless the user passes `--skip-cloud-consult`, I would then dispatch `Task(subagent_type: ywc-cloud-engineer)` in read-only feasibility-consult mode, explicitly instructing it that this dispatch authors nothing and must not run `terraform plan` or `terraform apply` — it only flags feasibility concerns such as quota limits, provider-specific gotchas, or an unrealistic network layout.

- **Step 4 (3-lens pre-check)**: I would read `claude-code/skills/references/lenses/reliability.md`, `claude-code/skills/references/lenses/cost.md`, and `claude-code/skills/references/lenses/security.md`, then pre-check the Step 3 topology against each lens's taxonomy, recording every finding — including an explicit "no issue found" where nothing was flagged — so downstream `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline rather than re-deriving it. I would also read the matching provider reference file (`references/providers/aws.md`, `gcp.md`, `azure.md`, or `k8s.md`) to ground the topology choices in realistic provider constraints.

- **Step 5 (ADR log)**: for every material decision surfaced in Steps 2–3 — provider choice, single-AZ vs multi-AZ, managed vs self-hosted database, network exposure boundary, and similar — I would write a four-field Architecture Decision Record entry (Context, Decision, Alternatives considered, Consequences) as the decision is made, not reconstructed from memory at the end, since reconstruction tends to drop the alternatives that were actually weighed.

- **Step 6 (Output)**: I would write `infra-design.md` at the project root (or at the `--scope`-implied path if scoping was requested) using the exact Output Format template from the skill: `## Requirements`, `## Provider Decision`, `## Topology` (with Network/Compute/Storage/IAM subsections), `## 3-Lens Pre-Check`, and `## ADR Log`. This file is the input contract that `ywc-iac-author`'s Step 1 loads, so it needs to be complete enough that skill never has to re-ask a question this pass already answered.

Before declaring the pass complete I would run through the skill's Validation Checklist: requirements gathered explicitly (not inferred); provider decision either explicitly declared or delegated to `/ywc-tech-research`, never invented; topology covers all four dimensions; the 3-lens pre-check ran with every finding recorded; every material trade-off has a corresponding ADR entry; and `infra-design.md` was written with all five sections.

Throughout, I would explicitly not write or modify any `.tf` files in this same pass — the skill's Common Mistakes and Integration sections are unambiguous that authoring Terraform is `ywc-iac-author`'s scope, and collapsing the two loses the reviewable checkpoint between design and implementation. If, hypothetically, I felt tempted to just sketch a topology and start writing Terraform to save a round trip, that is precisely the first entry in the Rationalization Defense table, and the correct response is to keep the design pass and the authoring pass as two separate, reviewable steps.

Given all of the above, my actual first move on this request — before touching topology, provider, or infra-design.md at all — is to ask the user for the Step 1 requirements answers and the provider/scope status rather than to proceed on assumptions.
