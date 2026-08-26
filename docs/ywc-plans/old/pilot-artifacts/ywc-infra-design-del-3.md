# Dispatch artifact: ywc-infra-design (deleted body, run 3)

**Key**: claude-code/skills/ywc-infra-design/SKILL.md:36-36
**Scenario**: I need help with the following: designing cloud/infrastructure architecture before any IaC is written — requirements gathering, provider selection, network/compute/storage/IAM topology, and a reliability/cost/security 3-lens pre-check that produces infra-design.md, the input contract ywc-iac-author consumes.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a refusal in the blocking sense, but the procedure requires pausing to ask the user clarifying questions before proceeding: Step 1 explicitly forbids inferring workload characteristics, traffic, data classification/retention, compliance/residency, budget, and RTO/RPO from the feature description alone, and none of these were supplied in the request. Work would resume once the user answers.

## Actions
- Read the ywc-infra-design procedure file only (already done)
- Announce at start: 'I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written.'
- Step 1: ask the user clarifying questions for each unanswered requirements field (workload characteristics, traffic/RPS/growth, data volume+classification+retention, compliance/residency, budget ceiling, RTO/RPO) rather than inferring them from the request text
- Pause and wait for user answers before proceeding to Step 2 (requirements not yet supplied in the request)
- Step 2: since no --provider flag and no prior decision/account/mandate was stated, invoke Skill tool with skill: ywc-tech-research, passing traffic/data/budget/compliance answers as comparison criteria for AWS/GCP/Azure/K8s
- Record the ywc-tech-research recommendation as the Provider Decision with rationale
- Step 3: design Network (VPC/VNet, subnet tiers, public/private boundary, ingress/egress), Compute (service shape matched to workload), Storage (DB engine, object storage, cache matched to data profile), IAM/identity boundaries (least-privilege roles, cross-account/service trust)
- Consult the matching provider reference file under claude-code/skills/ywc-infra-design/references/providers/ (aws.md/gcp.md/azure.md/k8s.md) for the chosen provider to ground topology choices
- Dispatch Task(subagent_type: ywc-cloud-engineer) in read-only feasibility-consult mode with the topology sketch and explicit instruction that it authors nothing and runs no terraform plan/apply, only flags feasibility concerns (unless --skip-cloud-consult were passed)
- Step 4: Read claude-code/skills/ywc-infra-design/references/lenses/reliability.md, cost.md, and security.md, then pre-check the topology against each lens's taxonomy, recording every finding including 'no issue found'
- Step 5: write an ADR entry (Context / Decision / Alternatives considered / Consequences) for every material decision from Steps 2-3 (provider choice, single-AZ vs multi-AZ, managed vs self-hosted DB, network exposure boundary, etc.) as each is decided, not reconstructed afterward
- Step 6: Write infra-design.md at the project root using the Write tool, following the exact Output Format template (Requirements, Provider Decision, Topology, 3-Lens Pre-Check, ADR Log)
- Run the Validation Checklist before declaring the pass complete: requirements gathered explicitly, provider decision declared or delegated (never invented), all four topology dimensions covered, 3-lens pre-check run and recorded, every trade-off has an ADR entry, infra-design.md written with all sections
- Explicitly refrain from creating or editing any .tf files or invoking ywc-iac-author in this same pass

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-infra-design-36-36.md (read only)
- infra-design.md (would be created at project root)
- claude-code/skills/ywc-infra-design/references/lenses/reliability.md (would be read)
- claude-code/skills/ywc-infra-design/references/lenses/cost.md (would be read)
- claude-code/skills/ywc-infra-design/references/lenses/security.md (would be read)
- claude-code/skills/ywc-infra-design/references/providers/<chosen-provider>.md (would be read)

## Gates enforced
- Requirements-gathering gate: do not infer workload/traffic/data/compliance/budget/RTO-RPO from the feature description alone; ask the user and record answers verbatim
- Provider-decision gate: never invent the AWS/GCP/Azure/K8s comparison inline; delegate to ywc-tech-research unless already decided or --provider given
- Topology completeness gate: must cover network, compute, storage, and IAM/identity boundaries before proceeding
- 3-lens pre-check gate: reliability/cost/security lens files must be read and every finding recorded, including 'no issue found'
- ADR completeness gate: every material trade-off (provider, AZ strategy, managed vs self-hosted DB, network exposure boundary) must have a Context/Decision/Alternatives/Consequences entry recorded at decision time, not reconstructed later
- Scope boundary gate: this pass must stop at infra-design.md and must not write or modify .tf files or invoke ywc-iac-author in the same pass
- Cloud-engineer consult gate: if dispatched, it must run in read-only feasibility mode only, never authoring or running terraform plan/apply
- Final validation checklist: all six items must be true before declaring the design pass complete

## Full narrative

I would open by announcing, verbatim as the procedure specifies: "I'm using the ywc-infra-design skill to design the cloud/infrastructure architecture before any IaC is written."

**Step 1 — Requirements gathering (blocking gate).** The request as given only states the *goal* (design cloud/infra architecture, produce infra-design.md) but supplies none of the six required requirement fields. Per the skill's explicit instruction — "Do not infer these from the feature description alone — ask the user for anything not already stated" — I would not guess. I would ask the user directly for:
- Workload characteristics (read-heavy/write-heavy/mixed, sync/batch/event-driven, stateful or not)
- Traffic (expected concurrency/RPS, peak vs steady-state, 6–12 month growth trajectory)
- Data profile (volume, growth rate, PII/PHI/none classification, retention requirements)
- Regulatory/compliance constraints (data residency, GDPR/HIPAA/SOC 2/industry mandates)
- Budget (monthly ceiling or per-unit cost target)
- RTO/RPO (acceptable downtime window and data-loss window)

I would record the answers verbatim once received, since they become the "Requirements" section of `infra-design.md` word-for-word.

**Step 2 — Provider selection.** No `--provider` flag was given, and nothing in the request indicates an existing account, mandated vendor, or explicit provider statement. Per the Rationalization Defense table's explicit guidance ("picking a favorite instead of delegating the comparison is a design decision made without evidence"), I would not invent an AWS/GCP/Azure/K8s comparison myself. I would invoke the Skill tool with `skill: ywc-tech-research`, feeding it the traffic/data/budget/compliance answers gathered in Step 1 as comparison criteria, and record its recommendation as the Provider Decision with a 1–3 line rationale and `Source: ywc-tech-research recommendation`.

**Step 3 — Topology design.** In this fixed order I would design:
- *Network*: VPC/VNet layout, subnet tiers (public/private/data), the public/private boundary, and ingress/egress paths (ALB/NAT gateway or equivalent for the chosen provider).
- *Compute*: service shape (managed container service, VM, or serverless/FaaS) matched to the Step 1 workload pattern.
- *Storage*: database engine, object storage, and cache layer matched to the Step 1 data profile (volume, classification, retention).
- *IAM/identity boundaries*: role structure, least-privilege boundaries, and any cross-account/cross-service trust relationships.

To ground these choices in provider-specific realism, I would Read the matching reference file, e.g. `claude-code/skills/ywc-infra-design/references/providers/aws.md` (or gcp.md/azure.md/k8s.md depending on the Step 2 outcome).

Since `--skip-cloud-consult` was not passed, I would dispatch `Task(subagent_type: ywc-cloud-engineer)` in explicit read-only feasibility-consult mode, carrying the topology sketch and an explicit instruction that this dispatch authors nothing and must not run `terraform plan`/`terraform apply` — it only flags feasibility concerns such as quota limits, provider-specific gotchas, or an unrealistic network layout. If that subagent's output showed any sign of producing `.tf` files, per the Common Mistakes section I would treat that as a dispatch-instruction error and disregard/redo it rather than accept generated IaC from this consult.

**Step 4 — Reliability/Cost/Security 3-lens pre-check.** I would Read the three lens reference files: `claude-code/skills/ywc-infra-design/references/lenses/reliability.md`, `.../cost.md`, and `.../security.md`. I would then walk the Step 3 topology against each lens's taxonomy and record every finding explicitly in the eventual output — including "no issue found" where nothing surfaces, since the procedure requires that null result to be recorded rather than omitted (so `ywc-iac-author` and `ywc-infra-review` inherit a documented baseline instead of re-deriving it).

**Step 5 — ADR log.** For every material decision surfaced in Steps 2–3 — the provider choice itself, single-AZ vs multi-AZ, managed vs self-hosted database, the network exposure boundary, and any other consequential trade-off — I would write an ADR entry with four fields (Context, Decision, Alternatives considered, Consequences) at the moment each decision is made, not reconstructed from memory afterward, per the Common Mistakes warning that reconstruction drops the alternatives actually considered.

**Step 6 — Output.** I would use the Write tool to create `infra-design.md` at the project root (or at the path implied by `--scope` if that flag had been passed — it was not, so project root), following the exact template: `## Requirements`, `## Provider Decision`, `## Topology` (Network/Compute/Storage/IAM subsections), `## 3-Lens Pre-Check`, `## ADR Log`.

**Final gate — Validation Checklist.** Before declaring the pass complete I would verify all six checklist items: requirements gathered explicitly (not inferred), provider decision declared or delegated (never invented inline), all four topology dimensions covered, the 3-lens pre-check run with every finding recorded, every material trade-off backed by an ADR entry, and `infra-design.md` written with all five sections ready for `ywc-iac-author` to load directly.

**Explicit scope boundary.** I would not write, generate, or touch any `.tf` files in this same pass, and would not invoke `ywc-iac-author` myself — per the skill's "Must not be paired with" rule, that boundary belongs strictly to the downstream `ywc-iac-author` skill, invoked separately once `infra-design.md` exists and the user is ready to proceed to authoring.

In practice, the very first concrete action I'd take — before any topology or provider work — is to stop and ask the user the Step 1 requirements questions, since the request as posed supplies none of the six mandatory fields and the procedure forbids inferring them.
